"""
AIC AI Platform File Storage Service
S3-compatible object storage with access control and versioning
"""

import asyncio
import hashlib
import json
import logging
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, BinaryIO
from pathlib import Path
import mimetypes

from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel, Field
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import redis
from sqlalchemy import create_engine, Column, String, DateTime, Text, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import requests
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import aiofiles
from PIL import Image
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="AIC AI Platform File Storage Service",
    description="S3-compatible object storage with access control and versioning",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/file_storage")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
S3_BUCKET = os.getenv("S3_BUCKET", "aic-aipaas-storage")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")  # For MinIO or other S3-compatible services
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "104857600"))  # 100MB
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,gif,pdf,txt,csv,json,parquet,pkl,pt,pth,onnx,zip,tar,gz").split(",")

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis client
redis_client = redis.from_url(REDIS_URL)

# S3 client
s3_client = boto3.client(
    's3',
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-west-2")
)

# Prometheus metrics
file_uploads_total = Counter('file_uploads_total', 'Total file uploads', ['file_type', 'status'])
file_downloads_total = Counter('file_downloads_total', 'Total file downloads', ['file_type'])
storage_usage_bytes = Gauge('storage_usage_bytes', 'Storage usage in bytes', ['user_id'])
file_operations_duration = Histogram('file_operations_duration_seconds', 'File operation duration', ['operation'])

# Database Models
class FileMetadata(Base):
    __tablename__ = "file_metadata"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String)
    checksum = Column(String, nullable=False)
    owner_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    access_level = Column(String, default="private")  # private, public, shared
    tags = Column(Text)  # JSON
    metadata = Column(Text)  # JSON
    version = Column(Integer, default=1)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)

class FileAccess(Base):
    __tablename__ = "file_access"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    file_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    access_type = Column(String, nullable=False)  # read, write, delete
    granted_by = Column(String, nullable=False)
    granted_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

class FileVersion(Base):
    __tablename__ = "file_versions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    file_id = Column(String, nullable=False)
    version = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    checksum = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

# Pydantic Models
class FileUploadResponse(BaseModel):
    id: str
    filename: str
    file_size: int
    content_type: str
    checksum: str
    upload_url: Optional[str] = None
    created_at: datetime

class FileMetadataResponse(BaseModel):
    id: str
    filename: str
    original_filename: str
    file_size: int
    content_type: str
    owner_id: str
    created_at: datetime
    updated_at: datetime
    access_level: str
    tags: List[str]
    version: int
    download_url: Optional[str] = None

class FileAccessRequest(BaseModel):
    user_id: str
    access_type: str = Field(..., regex="^(read|write|delete)$")
    expires_hours: int = Field(default=24, ge=1, le=8760)  # Max 1 year

class FileSearchRequest(BaseModel):
    query: Optional[str] = None
    file_type: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    access_level: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    limit: int = Field(default=50, le=1000)
    offset: int = Field(default=0, ge=0)

# Dependency functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token with auth service"""
    try:
        response = requests.post(
            f"{AUTH_SERVICE_URL}/auth/validate",
            headers={"Authorization": f"Bearer {credentials.credentials}"},
            timeout=5
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        return response.json()
    except requests.RequestException:
        raise HTTPException(status_code=401, detail="Authentication service unavailable")

# Helper functions
def calculate_file_checksum(file_content: bytes) -> str:
    """Calculate MD5 checksum of file content"""
    return hashlib.md5(file_content).hexdigest()

def get_file_extension(filename: str) -> str:
    """Get file extension"""
    return Path(filename).suffix.lower().lstrip('.')

def is_allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    extension = get_file_extension(filename)
    return extension in ALLOWED_EXTENSIONS

def generate_s3_key(user_id: str, file_id: str, filename: str) -> str:
    """Generate S3 object key"""
    return f"users/{user_id}/files/{file_id}/{filename}"

def generate_presigned_url(s3_key: str, expiration: int = 3600, operation: str = "get_object") -> str:
    """Generate presigned URL for S3 object"""
    try:
        if operation == "get_object":
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': S3_BUCKET, 'Key': s3_key},
                ExpiresIn=expiration
            )
        elif operation == "put_object":
            url = s3_client.generate_presigned_url(
                'put_object',
                Params={'Bucket': S3_BUCKET, 'Key': s3_key},
                ExpiresIn=expiration
            )
        else:
            raise ValueError(f"Unsupported operation: {operation}")
        
        return url
    except ClientError as e:
        logger.error(f"Failed to generate presigned URL: {e}")
        return None

def check_file_access(file_id: str, user_id: str, access_type: str, db: Session) -> bool:
    """Check if user has access to file"""
    
    # Get file metadata
    file_metadata = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()
    if not file_metadata:
        return False
    
    # Owner has full access
    if file_metadata.owner_id == user_id:
        return True
    
    # Check public access
    if file_metadata.access_level == "public" and access_type == "read":
        return True
    
    # Check explicit access grants
    access_grant = db.query(FileAccess).filter(
        FileAccess.file_id == file_id,
        FileAccess.user_id == user_id,
        FileAccess.access_type == access_type
    ).first()
    
    if access_grant:
        # Check if access has expired
        if access_grant.expires_at and access_grant.expires_at < datetime.utcnow():
            return False
        return True
    
    return False

def process_image(file_content: bytes, max_size: tuple = (1920, 1080)) -> bytes:
    """Process and optimize image"""
    try:
        image = Image.open(io.BytesIO(file_content))
        
        # Convert to RGB if necessary
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        
        # Resize if too large
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save optimized image
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=85, optimize=True)
        return output.getvalue()
        
    except Exception as e:
        logger.warning(f"Failed to process image: {e}")
        return file_content

# API Endpoints
@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "service": "file-storage",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.post("/files/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    access_level: str = Form(default="private"),
    tags: str = Form(default="[]"),
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Upload a file"""
    
    user_id = user_info.get("user", "unknown")
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Read file content
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"File too large. Max size: {MAX_FILE_SIZE} bytes")
    
    # Process image files
    content_type = file.content_type or mimetypes.guess_type(file.filename)[0] or "application/octet-stream"
    if content_type.startswith('image/'):
        file_content = process_image(file_content)
        file_size = len(file_content)
    
    # Calculate checksum
    checksum = calculate_file_checksum(file_content)
    
    # Generate file ID and S3 key
    file_id = str(uuid.uuid4())
    s3_key = generate_s3_key(user_id, file_id, file.filename)
    
    try:
        # Upload to S3
        with file_operations_duration.labels(operation="upload").time():
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=s3_key,
                Body=file_content,
                ContentType=content_type,
                Metadata={
                    'original-filename': file.filename,
                    'owner-id': user_id,
                    'checksum': checksum
                }
            )
        
        # Parse tags
        try:
            tags_list = json.loads(tags)
        except json.JSONDecodeError:
            tags_list = []
        
        # Store metadata in database
        file_metadata = FileMetadata(
            id=file_id,
            filename=file.filename,
            original_filename=file.filename,
            file_path=s3_key,
            file_size=file_size,
            content_type=content_type,
            checksum=checksum,
            owner_id=user_id,
            access_level=access_level,
            tags=json.dumps(tags_list)
        )
        
        db.add(file_metadata)
        db.commit()
        db.refresh(file_metadata)
        
        # Update metrics
        file_uploads_total.labels(
            file_type=get_file_extension(file.filename),
            status="success"
        ).inc()
        
        # Update storage usage
        current_usage = redis_client.get(f"storage_usage:{user_id}")
        new_usage = int(current_usage or 0) + file_size
        redis_client.set(f"storage_usage:{user_id}", new_usage)
        storage_usage_bytes.labels(user_id=user_id).set(new_usage)
        
        logger.info(f"File uploaded successfully: {file_id}")
        
        return FileUploadResponse(
            id=file_id,
            filename=file.filename,
            file_size=file_size,
            content_type=content_type,
            checksum=checksum,
            created_at=file_metadata.created_at
        )
        
    except ClientError as e:
        logger.error(f"S3 upload failed: {e}")
        file_uploads_total.labels(
            file_type=get_file_extension(file.filename),
            status="error"
        ).inc()
        raise HTTPException(status_code=500, detail="File upload failed")

@app.get("/files/{file_id}", response_model=FileMetadataResponse)
async def get_file_metadata(
    file_id: str,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get file metadata"""
    
    user_id = user_info.get("user", "unknown")
    
    # Check access
    if not check_file_access(file_id, user_id, "read", db):
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get file metadata
    file_metadata = db.query(FileMetadata).filter(
        FileMetadata.id == file_id,
        FileMetadata.is_deleted == False
    ).first()
    
    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Generate download URL
    download_url = generate_presigned_url(file_metadata.file_path, expiration=3600)
    
    return FileMetadataResponse(
        id=file_metadata.id,
        filename=file_metadata.filename,
        original_filename=file_metadata.original_filename,
        file_size=file_metadata.file_size,
        content_type=file_metadata.content_type,
        owner_id=file_metadata.owner_id,
        created_at=file_metadata.created_at,
        updated_at=file_metadata.updated_at,
        access_level=file_metadata.access_level,
        tags=json.loads(file_metadata.tags) if file_metadata.tags else [],
        version=file_metadata.version,
        download_url=download_url
    )

@app.get("/files/{file_id}/download")
async def download_file(
    file_id: str,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Download a file"""
    
    user_id = user_info.get("user", "unknown")
    
    # Check access
    if not check_file_access(file_id, user_id, "read", db):
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get file metadata
    file_metadata = db.query(FileMetadata).filter(
        FileMetadata.id == file_id,
        FileMetadata.is_deleted == False
    ).first()
    
    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Get file from S3
        with file_operations_duration.labels(operation="download").time():
            response = s3_client.get_object(Bucket=S3_BUCKET, Key=file_metadata.file_path)
            file_content = response['Body'].read()
        
        # Update metrics
        file_downloads_total.labels(
            file_type=get_file_extension(file_metadata.filename)
        ).inc()
        
        # Return file as streaming response
        return StreamingResponse(
            io.BytesIO(file_content),
            media_type=file_metadata.content_type,
            headers={
                "Content-Disposition": f"attachment; filename={file_metadata.original_filename}",
                "Content-Length": str(file_metadata.file_size)
            }
        )
        
    except ClientError as e:
        logger.error(f"S3 download failed: {e}")
        raise HTTPException(status_code=500, detail="File download failed")

@app.delete("/files/{file_id}")
async def delete_file(
    file_id: str,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Delete a file"""
    
    user_id = user_info.get("user", "unknown")
    
    # Check access
    if not check_file_access(file_id, user_id, "delete", db):
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get file metadata
    file_metadata = db.query(FileMetadata).filter(
        FileMetadata.id == file_id,
        FileMetadata.is_deleted == False
    ).first()
    
    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Delete from S3
        with file_operations_duration.labels(operation="delete").time():
            s3_client.delete_object(Bucket=S3_BUCKET, Key=file_metadata.file_path)
        
        # Mark as deleted in database
        file_metadata.is_deleted = True
        file_metadata.deleted_at = datetime.utcnow()
        db.commit()
        
        # Update storage usage
        current_usage = redis_client.get(f"storage_usage:{user_id}")
        new_usage = max(0, int(current_usage or 0) - file_metadata.file_size)
        redis_client.set(f"storage_usage:{user_id}", new_usage)
        storage_usage_bytes.labels(user_id=user_id).set(new_usage)
        
        logger.info(f"File deleted successfully: {file_id}")
        
        return {"message": "File deleted successfully"}
        
    except ClientError as e:
        logger.error(f"S3 delete failed: {e}")
        raise HTTPException(status_code=500, detail="File deletion failed")

@app.post("/files/{file_id}/access")
async def grant_file_access(
    file_id: str,
    request: FileAccessRequest,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Grant file access to another user"""
    
    user_id = user_info.get("user", "unknown")
    
    # Check if user owns the file
    file_metadata = db.query(FileMetadata).filter(
        FileMetadata.id == file_id,
        FileMetadata.owner_id == user_id,
        FileMetadata.is_deleted == False
    ).first()
    
    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found or access denied")
    
    # Create access grant
    expires_at = datetime.utcnow() + timedelta(hours=request.expires_hours)
    
    access_grant = FileAccess(
        file_id=file_id,
        user_id=request.user_id,
        access_type=request.access_type,
        granted_by=user_id,
        expires_at=expires_at
    )
    
    db.add(access_grant)
    db.commit()
    db.refresh(access_grant)
    
    return {
        "id": access_grant.id,
        "file_id": file_id,
        "user_id": request.user_id,
        "access_type": request.access_type,
        "expires_at": expires_at.isoformat()
    }

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)

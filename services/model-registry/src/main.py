"""
AIC AI Platform Model Registry Service
Model versioning, metadata management, and promotion workflows
"""

import json
import logging
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import mlflow
import mlflow.tracking
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType
from sqlalchemy import create_engine, Column, String, DateTime, Text, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import requests
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import boto3
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="AIC AI Platform Model Registry Service",
    description="Model versioning, metadata management, and promotion workflows",
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
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/model_registry")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
S3_BUCKET = os.getenv("S3_BUCKET", "aic-aipaas-models")

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MLflow setup
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow_client = MlflowClient()

# S3 client
s3_client = boto3.client('s3')

# Prometheus metrics
model_registrations_total = Counter('model_registrations_total', 'Total model registrations')
model_promotions_total = Counter('model_promotions_total', 'Total model promotions', ['from_stage', 'to_stage'])
active_models_total = Gauge('active_models_total', 'Total active models')
model_versions_total = Gauge('model_versions_total', 'Total model versions')

# Enums
class ModelStage(str, Enum):
    DEVELOPMENT = "Development"
    STAGING = "Staging"
    PRODUCTION = "Production"
    ARCHIVED = "Archived"

class ModelStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"

# Database Models
class ModelMetadata(Base):
    __tablename__ = "model_metadata"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    owner_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    tags = Column(Text)  # JSON array
    use_case = Column(String)
    framework = Column(String)
    algorithm = Column(String)
    dataset_info = Column(Text)  # JSON
    performance_metrics = Column(Text)  # JSON
    status = Column(String, default=ModelStatus.ACTIVE)

class ModelVersion(Base):
    __tablename__ = "model_versions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    model_name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    mlflow_run_id = Column(String)
    stage = Column(String, default=ModelStage.DEVELOPMENT)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, nullable=False)
    description = Column(Text)
    metrics = Column(Text)  # JSON
    parameters = Column(Text)  # JSON
    artifacts = Column(Text)  # JSON
    model_size = Column(Integer)  # bytes
    checksum = Column(String)
    approval_status = Column(String, default="pending")  # pending, approved, rejected
    approved_by = Column(String)
    approved_at = Column(DateTime)

class ModelPromotion(Base):
    __tablename__ = "model_promotions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    model_name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    from_stage = Column(String, nullable=False)
    to_stage = Column(String, nullable=False)
    promoted_by = Column(String, nullable=False)
    promoted_at = Column(DateTime, default=datetime.utcnow)
    reason = Column(Text)
    approval_required = Column(Boolean, default=False)
    approved_by = Column(String)
    approved_at = Column(DateTime)

Base.metadata.create_all(bind=engine)

# Pydantic Models
class ModelRegistrationRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    use_case: Optional[str] = None
    framework: str = Field(..., description="pytorch, tensorflow, sklearn, etc.")
    algorithm: Optional[str] = None
    dataset_info: Optional[Dict[str, Any]] = None

class ModelVersionRequest(BaseModel):
    model_name: str
    version: Optional[str] = None  # Auto-generated if not provided
    mlflow_run_id: str
    description: Optional[str] = None
    stage: ModelStage = ModelStage.DEVELOPMENT

class ModelPromotionRequest(BaseModel):
    model_name: str
    version: str
    to_stage: ModelStage
    reason: Optional[str] = None

class ModelResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    owner_id: str
    created_at: datetime
    updated_at: datetime
    tags: List[str]
    use_case: Optional[str]
    framework: str
    algorithm: Optional[str]
    status: str
    latest_version: Optional[str]
    versions_count: int

class ModelVersionResponse(BaseModel):
    id: str
    model_name: str
    version: str
    stage: str
    created_at: datetime
    created_by: str
    description: Optional[str]
    metrics: Optional[Dict[str, Any]]
    parameters: Optional[Dict[str, Any]]
    model_size: Optional[int]
    approval_status: str

class ModelPromotionResponse(BaseModel):
    id: str
    model_name: str
    version: str
    from_stage: str
    to_stage: str
    promoted_by: str
    promoted_at: datetime
    reason: Optional[str]
    approval_required: bool

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
def get_mlflow_run_info(run_id: str) -> Dict[str, Any]:
    """Get MLflow run information"""
    try:
        run = mlflow_client.get_run(run_id)
        return {
            "metrics": run.data.metrics,
            "parameters": run.data.params,
            "tags": run.data.tags,
            "artifacts": [artifact.path for artifact in mlflow_client.list_artifacts(run_id)],
            "status": run.info.status,
            "start_time": run.info.start_time,
            "end_time": run.info.end_time
        }
    except Exception as e:
        logger.error(f"Failed to get MLflow run info: {e}")
        return {}

def calculate_model_checksum(model_path: str) -> str:
    """Calculate model checksum for integrity verification"""
    import hashlib
    hash_md5 = hashlib.md5()
    try:
        with open(model_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception:
        return ""

def get_model_size(model_path: str) -> int:
    """Get model file size in bytes"""
    try:
        return os.path.getsize(model_path)
    except Exception:
        return 0

# API Endpoints
@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "service": "model-registry",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.post("/models", response_model=ModelResponse)
async def register_model(
    request: ModelRegistrationRequest,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Register a new model"""
    
    user_id = user_info.get("user", "unknown")
    
    # Check if model name already exists
    existing_model = db.query(ModelMetadata).filter(ModelMetadata.name == request.name).first()
    if existing_model:
        raise HTTPException(status_code=400, detail="Model name already exists")
    
    # Create model metadata
    model = ModelMetadata(
        name=request.name,
        description=request.description,
        owner_id=user_id,
        tags=json.dumps(request.tags),
        use_case=request.use_case,
        framework=request.framework,
        algorithm=request.algorithm,
        dataset_info=json.dumps(request.dataset_info) if request.dataset_info else None
    )
    
    db.add(model)
    db.commit()
    db.refresh(model)
    
    # Create MLflow registered model
    try:
        mlflow_client.create_registered_model(
            name=request.name,
            description=request.description,
            tags=dict(zip(request.tags, ["true"] * len(request.tags))) if request.tags else None
        )
    except Exception as e:
        logger.warning(f"Failed to create MLflow registered model: {e}")
    
    model_registrations_total.inc()
    active_models_total.inc()
    
    return ModelResponse(
        id=model.id,
        name=model.name,
        description=model.description,
        owner_id=model.owner_id,
        created_at=model.created_at,
        updated_at=model.updated_at,
        tags=json.loads(model.tags) if model.tags else [],
        use_case=model.use_case,
        framework=model.framework,
        algorithm=model.algorithm,
        status=model.status,
        latest_version=None,
        versions_count=0
    )

@app.get("/models", response_model=List[ModelResponse])
async def list_models(
    skip: int = 0,
    limit: int = 50,
    framework: Optional[str] = None,
    use_case: Optional[str] = None,
    status: Optional[str] = None,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """List models with filtering"""
    
    query = db.query(ModelMetadata)
    
    if framework:
        query = query.filter(ModelMetadata.framework == framework)
    if use_case:
        query = query.filter(ModelMetadata.use_case == use_case)
    if status:
        query = query.filter(ModelMetadata.status == status)
    
    models = query.offset(skip).limit(limit).all()
    
    result = []
    for model in models:
        # Get version count and latest version
        versions = db.query(ModelVersion).filter(ModelVersion.model_name == model.name).all()
        latest_version = max(versions, key=lambda v: v.created_at).version if versions else None
        
        result.append(ModelResponse(
            id=model.id,
            name=model.name,
            description=model.description,
            owner_id=model.owner_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            tags=json.loads(model.tags) if model.tags else [],
            use_case=model.use_case,
            framework=model.framework,
            algorithm=model.algorithm,
            status=model.status,
            latest_version=latest_version,
            versions_count=len(versions)
        ))
    
    return result

@app.get("/models/{model_name}", response_model=ModelResponse)
async def get_model(
    model_name: str,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get model details"""
    
    model = db.query(ModelMetadata).filter(ModelMetadata.name == model_name).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # Get version information
    versions = db.query(ModelVersion).filter(ModelVersion.model_name == model_name).all()
    latest_version = max(versions, key=lambda v: v.created_at).version if versions else None
    
    return ModelResponse(
        id=model.id,
        name=model.name,
        description=model.description,
        owner_id=model.owner_id,
        created_at=model.created_at,
        updated_at=model.updated_at,
        tags=json.loads(model.tags) if model.tags else [],
        use_case=model.use_case,
        framework=model.framework,
        algorithm=model.algorithm,
        status=model.status,
        latest_version=latest_version,
        versions_count=len(versions)
    )

@app.post("/models/{model_name}/versions", response_model=ModelVersionResponse)
async def create_model_version(
    model_name: str,
    request: ModelVersionRequest,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create a new model version"""
    
    user_id = user_info.get("user", "unknown")
    
    # Verify model exists
    model = db.query(ModelMetadata).filter(ModelMetadata.name == model_name).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # Get MLflow run information
    run_info = get_mlflow_run_info(request.mlflow_run_id)
    
    # Generate version if not provided
    version = request.version
    if not version:
        existing_versions = db.query(ModelVersion).filter(ModelVersion.model_name == model_name).all()
        version_numbers = [int(v.version) for v in existing_versions if v.version.isdigit()]
        version = str(max(version_numbers, default=0) + 1)
    
    # Create model version in MLflow
    try:
        model_version = mlflow_client.create_model_version(
            name=model_name,
            source=f"runs:/{request.mlflow_run_id}/model",
            run_id=request.mlflow_run_id,
            description=request.description
        )
        
        # Set stage
        if request.stage != ModelStage.DEVELOPMENT:
            mlflow_client.transition_model_version_stage(
                name=model_name,
                version=model_version.version,
                stage=request.stage.value
            )
    except Exception as e:
        logger.error(f"Failed to create MLflow model version: {e}")
        raise HTTPException(status_code=500, detail="Failed to create model version in MLflow")
    
    # Create version record
    version_record = ModelVersion(
        model_name=model_name,
        version=version,
        mlflow_run_id=request.mlflow_run_id,
        stage=request.stage.value,
        created_by=user_id,
        description=request.description,
        metrics=json.dumps(run_info.get("metrics", {})),
        parameters=json.dumps(run_info.get("parameters", {})),
        artifacts=json.dumps(run_info.get("artifacts", []))
    )
    
    db.add(version_record)
    db.commit()
    db.refresh(version_record)
    
    model_versions_total.inc()
    
    return ModelVersionResponse(
        id=version_record.id,
        model_name=version_record.model_name,
        version=version_record.version,
        stage=version_record.stage,
        created_at=version_record.created_at,
        created_by=version_record.created_by,
        description=version_record.description,
        metrics=json.loads(version_record.metrics) if version_record.metrics else None,
        parameters=json.loads(version_record.parameters) if version_record.parameters else None,
        model_size=version_record.model_size,
        approval_status=version_record.approval_status
    )

@app.get("/models/{model_name}/versions", response_model=List[ModelVersionResponse])
async def list_model_versions(
    model_name: str,
    stage: Optional[ModelStage] = None,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """List model versions"""
    
    query = db.query(ModelVersion).filter(ModelVersion.model_name == model_name)
    
    if stage:
        query = query.filter(ModelVersion.stage == stage.value)
    
    versions = query.order_by(ModelVersion.created_at.desc()).all()
    
    return [
        ModelVersionResponse(
            id=version.id,
            model_name=version.model_name,
            version=version.version,
            stage=version.stage,
            created_at=version.created_at,
            created_by=version.created_by,
            description=version.description,
            metrics=json.loads(version.metrics) if version.metrics else None,
            parameters=json.loads(version.parameters) if version.parameters else None,
            model_size=version.model_size,
            approval_status=version.approval_status
        )
        for version in versions
    ]

@app.post("/models/{model_name}/versions/{version}/promote", response_model=ModelPromotionResponse)
async def promote_model(
    model_name: str,
    version: str,
    request: ModelPromotionRequest,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Promote model to different stage"""
    
    user_id = user_info.get("user", "unknown")
    
    # Get model version
    model_version = db.query(ModelVersion).filter(
        ModelVersion.model_name == model_name,
        ModelVersion.version == version
    ).first()
    
    if not model_version:
        raise HTTPException(status_code=404, detail="Model version not found")
    
    current_stage = model_version.stage
    target_stage = request.to_stage.value
    
    # Validate promotion path
    valid_promotions = {
        ModelStage.DEVELOPMENT: [ModelStage.STAGING],
        ModelStage.STAGING: [ModelStage.PRODUCTION, ModelStage.ARCHIVED],
        ModelStage.PRODUCTION: [ModelStage.ARCHIVED]
    }
    
    if ModelStage(current_stage) not in valid_promotions or request.to_stage not in valid_promotions[ModelStage(current_stage)]:
        raise HTTPException(status_code=400, detail=f"Invalid promotion from {current_stage} to {target_stage}")
    
    # Create promotion record
    promotion = ModelPromotion(
        model_name=model_name,
        version=version,
        from_stage=current_stage,
        to_stage=target_stage,
        promoted_by=user_id,
        reason=request.reason,
        approval_required=(target_stage == ModelStage.PRODUCTION)
    )
    
    db.add(promotion)
    
    # Update model version stage if no approval required
    if not promotion.approval_required:
        model_version.stage = target_stage
        
        # Update in MLflow
        try:
            mlflow_client.transition_model_version_stage(
                name=model_name,
                version=version,
                stage=target_stage
            )
        except Exception as e:
            logger.error(f"Failed to update MLflow stage: {e}")
    
    db.commit()
    db.refresh(promotion)
    
    model_promotions_total.labels(from_stage=current_stage, to_stage=target_stage).inc()
    
    return ModelPromotionResponse(
        id=promotion.id,
        model_name=promotion.model_name,
        version=promotion.version,
        from_stage=promotion.from_stage,
        to_stage=promotion.to_stage,
        promoted_by=promotion.promoted_by,
        promoted_at=promotion.promoted_at,
        reason=promotion.reason,
        approval_required=promotion.approval_required
    )

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)

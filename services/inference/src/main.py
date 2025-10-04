"""
AIC AI Platform Inference Service
Real-time and batch model serving with auto-scaling and A/B testing
"""

import asyncio
import json
import logging
import os
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import hashlib

import torch
import torch.nn as nn
import numpy as np
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import redis
import boto3
from sqlalchemy import create_engine, Column, String, DateTime, Text, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import requests
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import mlflow
import mlflow.pytorch
from PIL import Image
import io
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="AIC AI Platform Inference Service",
    description="Real-time and batch model serving with A/B testing",
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
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/inference")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
S3_BUCKET = os.getenv("S3_BUCKET", "aic-aipaas-models")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
MODEL_CACHE_TTL = int(os.getenv("MODEL_CACHE_TTL", "3600"))  # 1 hour

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis client for caching
redis_client = redis.from_url(REDIS_URL)

# MLflow setup
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# S3 client
s3_client = boto3.client('s3')

# Prometheus metrics
inference_requests_total = Counter('inference_requests_total', 'Total inference requests', ['model_id', 'version', 'status'])
inference_duration = Histogram('inference_duration_seconds', 'Inference duration', ['model_id', 'version'])
active_models = Gauge('active_models_total', 'Number of active models')
model_cache_hits = Counter('model_cache_hits_total', 'Model cache hits')
model_cache_misses = Counter('model_cache_misses_total', 'Model cache misses')
batch_inference_queue_size = Gauge('batch_inference_queue_size', 'Batch inference queue size')

# Global model cache
model_cache = {}
model_metadata_cache = {}

# Database Models
class InferenceEndpoint(Base):
    __tablename__ = "inference_endpoints"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    model_id = Column(String, nullable=False)
    model_version = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    status = Column(String, default="active")  # active, inactive, deploying, failed
    endpoint_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    config = Column(Text)  # JSON configuration
    performance_metrics = Column(Text)  # JSON metrics
    ab_test_config = Column(Text)  # A/B testing configuration

class InferenceRequest(Base):
    __tablename__ = "inference_requests"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    endpoint_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    request_type = Column(String, nullable=False)  # realtime, batch
    status = Column(String, default="pending")  # pending, processing, completed, failed
    input_data = Column(Text)  # JSON input data
    output_data = Column(Text)  # JSON output data
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    processing_time = Column(Float)
    error_message = Column(Text)
    model_version_used = Column(String)

Base.metadata.create_all(bind=engine)

# Pydantic Models
class ModelConfig(BaseModel):
    framework: str = "pytorch"
    input_shape: List[int] = Field(default_factory=list)
    output_shape: List[int] = Field(default_factory=list)
    preprocessing: Dict[str, Any] = Field(default_factory=dict)
    postprocessing: Dict[str, Any] = Field(default_factory=dict)
    batch_size: int = 32
    max_batch_delay: float = 0.1  # seconds
    device: str = "auto"  # auto, cpu, cuda

class ABTestConfig(BaseModel):
    enabled: bool = False
    traffic_split: Dict[str, float] = Field(default_factory=dict)  # version -> percentage
    success_metric: str = "accuracy"
    min_requests: int = 100

class EndpointRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    model_id: str
    model_version: str = "latest"
    config: ModelConfig = ModelConfig()
    ab_test_config: ABTestConfig = ABTestConfig()
    auto_scaling: bool = True
    min_replicas: int = 1
    max_replicas: int = 10

class InferenceInput(BaseModel):
    data: Union[List[List[float]], List[str], str, Dict[str, Any]]
    parameters: Dict[str, Any] = Field(default_factory=dict)

class InferenceOutput(BaseModel):
    predictions: Union[List[float], List[List[float]], List[str], Dict[str, Any]]
    confidence: Optional[List[float]] = None
    model_version: str
    processing_time: float
    request_id: str

class BatchInferenceRequest(BaseModel):
    endpoint_id: str
    input_data: List[InferenceInput]
    callback_url: Optional[str] = None
    priority: int = Field(default=1, ge=1, le=5)

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

# Model management functions
class ModelManager:
    """Manages model loading, caching, and inference"""
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    async def load_model(self, model_id: str, version: str = "latest") -> Dict[str, Any]:
        """Load model from MLflow or S3"""
        cache_key = f"{model_id}:{version}"
        
        # Check cache first
        if cache_key in model_cache:
            model_cache_hits.inc()
            return model_cache[cache_key]
        
        model_cache_misses.inc()
        
        try:
            # Try loading from MLflow first
            model_uri = f"models:/{model_id}/{version}"
            model = mlflow.pytorch.load_model(model_uri, map_location=self.device)
            
            # Get model metadata
            client = mlflow.tracking.MlflowClient()
            model_version = client.get_model_version(model_id, version)
            
            model_info = {
                "model": model,
                "version": version,
                "metadata": {
                    "creation_timestamp": model_version.creation_timestamp,
                    "last_updated_timestamp": model_version.last_updated_timestamp,
                    "description": model_version.description,
                    "tags": model_version.tags
                },
                "loaded_at": datetime.utcnow()
            }
            
            # Cache the model
            model_cache[cache_key] = model_info
            active_models.inc()
            
            logger.info(f"Loaded model {model_id}:{version} from MLflow")
            return model_info
            
        except Exception as e:
            logger.error(f"Failed to load model from MLflow: {e}")
            
            # Fallback to S3
            try:
                s3_key = f"models/{model_id}/{version}/model.pth"
                local_path = f"/tmp/{model_id}_{version}_model.pth"
                
                s3_client.download_file(S3_BUCKET, s3_key, local_path)
                model = torch.load(local_path, map_location=self.device)
                
                model_info = {
                    "model": model,
                    "version": version,
                    "metadata": {"source": "s3"},
                    "loaded_at": datetime.utcnow()
                }
                
                model_cache[cache_key] = model_info
                active_models.inc()
                
                logger.info(f"Loaded model {model_id}:{version} from S3")
                return model_info
                
            except Exception as s3_error:
                logger.error(f"Failed to load model from S3: {s3_error}")
                raise HTTPException(status_code=404, detail=f"Model {model_id}:{version} not found")
    
    def preprocess_input(self, data: Any, config: Dict[str, Any]) -> torch.Tensor:
        """Preprocess input data based on configuration"""
        
        if isinstance(data, str):
            # Handle base64 encoded images
            if data.startswith('data:image'):
                # Remove data URL prefix
                data = data.split(',')[1]
            
            # Decode base64 image
            image_data = base64.b64decode(data)
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if specified
            if 'resize' in config:
                size = config['resize']
                image = image.resize((size[1], size[0]))
            
            # Convert to tensor
            import torchvision.transforms as transforms
            transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=config.get('mean', [0.485, 0.456, 0.406]),
                    std=config.get('std', [0.229, 0.224, 0.225])
                )
            ])
            
            tensor = transform(image).unsqueeze(0)
            
        elif isinstance(data, list):
            # Handle numerical data
            tensor = torch.tensor(data, dtype=torch.float32)
            if tensor.dim() == 1:
                tensor = tensor.unsqueeze(0)
        else:
            # Assume it's already a tensor or numpy array
            tensor = torch.tensor(data, dtype=torch.float32)
        
        return tensor.to(self.device)
    
    def postprocess_output(self, output: torch.Tensor, config: Dict[str, Any]) -> Dict[str, Any]:
        """Postprocess model output"""
        
        # Convert to numpy
        if output.is_cuda:
            output = output.cpu()
        output_np = output.detach().numpy()
        
        # Apply softmax for classification
        if config.get('apply_softmax', False):
            output_np = torch.softmax(torch.tensor(output_np), dim=-1).numpy()
        
        # Get top-k predictions
        top_k = config.get('top_k', 1)
        if top_k > 1 and output_np.ndim > 1:
            top_indices = np.argsort(output_np, axis=-1)[:, -top_k:]
            top_values = np.take_along_axis(output_np, top_indices, axis=-1)
            
            return {
                "predictions": top_values.tolist(),
                "indices": top_indices.tolist(),
                "confidence": top_values.max(axis=-1).tolist()
            }
        else:
            return {
                "predictions": output_np.tolist(),
                "confidence": output_np.max(axis=-1).tolist() if output_np.ndim > 1 else [float(output_np.max())]
            }
    
    async def predict(self, model_info: Dict[str, Any], input_data: Any, config: ModelConfig) -> Dict[str, Any]:
        """Run inference on input data"""
        
        model = model_info["model"]
        model.eval()
        
        start_time = time.time()
        
        with torch.no_grad():
            # Preprocess input
            input_tensor = self.preprocess_input(input_data, config.preprocessing)
            
            # Run inference
            output = model(input_tensor)
            
            # Postprocess output
            result = self.postprocess_output(output, config.postprocessing)
        
        processing_time = time.time() - start_time
        
        return {
            **result,
            "processing_time": processing_time,
            "model_version": model_info["version"]
        }

# Global model manager
model_manager = ModelManager()

# API Endpoints
@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "service": "inference",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "active_models": len(model_cache)
    }

@app.post("/endpoints")
async def create_endpoint(
    request: EndpointRequest,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create a new inference endpoint"""
    
    user_id = user_info.get("user", "unknown")
    
    # Verify model exists
    try:
        await model_manager.load_model(request.model_id, request.model_version)
    except HTTPException:
        raise HTTPException(status_code=400, detail="Model not found or cannot be loaded")
    
    # Create endpoint
    endpoint = InferenceEndpoint(
        name=request.name,
        model_id=request.model_id,
        model_version=request.model_version,
        user_id=user_id,
        config=json.dumps(request.config.dict()),
        ab_test_config=json.dumps(request.ab_test_config.dict()),
        endpoint_url=f"/predict/{request.name}"
    )
    
    db.add(endpoint)
    db.commit()
    db.refresh(endpoint)
    
    return {
        "id": endpoint.id,
        "name": endpoint.name,
        "endpoint_url": endpoint.endpoint_url,
        "status": endpoint.status,
        "created_at": endpoint.created_at
    }

@app.post("/predict/{endpoint_name}", response_model=InferenceOutput)
async def predict(
    endpoint_name: str,
    input_data: InferenceInput,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Real-time inference endpoint"""
    
    user_id = user_info.get("user", "unknown")
    
    # Get endpoint
    endpoint = db.query(InferenceEndpoint).filter(
        InferenceEndpoint.name == endpoint_name,
        InferenceEndpoint.user_id == user_id,
        InferenceEndpoint.status == "active"
    ).first()
    
    if not endpoint:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    
    # Parse configuration
    config = ModelConfig(**json.loads(endpoint.config))
    ab_config = ABTestConfig(**json.loads(endpoint.ab_test_config))
    
    # A/B testing logic
    model_version = endpoint.model_version
    if ab_config.enabled and ab_config.traffic_split:
        import random
        rand_val = random.random()
        cumulative = 0
        for version, percentage in ab_config.traffic_split.items():
            cumulative += percentage
            if rand_val <= cumulative:
                model_version = version
                break
    
    request_id = str(uuid.uuid4())
    
    try:
        # Load model
        model_info = await model_manager.load_model(endpoint.model_id, model_version)
        
        # Run inference
        start_time = time.time()
        result = await model_manager.predict(model_info, input_data.data, config)
        processing_time = time.time() - start_time
        
        # Log request
        inference_req = InferenceRequest(
            endpoint_id=endpoint.id,
            user_id=user_id,
            request_type="realtime",
            status="completed",
            input_data=json.dumps(input_data.dict()),
            output_data=json.dumps(result),
            processing_time=processing_time,
            model_version_used=model_version
        )
        db.add(inference_req)
        db.commit()
        
        # Update metrics
        inference_requests_total.labels(
            model_id=endpoint.model_id,
            version=model_version,
            status="success"
        ).inc()
        inference_duration.labels(
            model_id=endpoint.model_id,
            version=model_version
        ).observe(processing_time)
        
        return InferenceOutput(
            predictions=result["predictions"],
            confidence=result.get("confidence"),
            model_version=model_version,
            processing_time=processing_time,
            request_id=request_id
        )
        
    except Exception as e:
        logger.error(f"Inference failed: {e}")
        
        # Log failed request
        inference_req = InferenceRequest(
            endpoint_id=endpoint.id,
            user_id=user_id,
            request_type="realtime",
            status="failed",
            input_data=json.dumps(input_data.dict()),
            error_message=str(e),
            model_version_used=model_version
        )
        db.add(inference_req)
        db.commit()
        
        inference_requests_total.labels(
            model_id=endpoint.model_id,
            version=model_version,
            status="error"
        ).inc()
        
        raise HTTPException(status_code=500, detail=f"Inference failed: {e}")

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

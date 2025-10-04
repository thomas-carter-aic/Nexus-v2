"""
AIC AI Platform Model Training Service
Distributed training orchestration with Kubernetes Jobs and GPU resource management
"""

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import optuna
import mlflow
import mlflow.pytorch
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import redis
import boto3
from sqlalchemy import create_engine, Column, String, DateTime, Text, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import requests
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="AIC AI Platform Model Training Service",
    description="Distributed model training orchestration with GPU resource management",
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
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/model_training")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
S3_BUCKET = os.getenv("S3_BUCKET", "aic-aipaas-models")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis client
redis_client = redis.from_url(REDIS_URL)

# Kubernetes client
try:
    config.load_incluster_config()
except:
    config.load_kube_config()
k8s_batch_v1 = client.BatchV1Api()
k8s_core_v1 = client.CoreV1Api()

# MLflow setup
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Prometheus metrics
training_jobs_total = Counter('training_jobs_total', 'Total number of training jobs', ['status'])
training_duration = Histogram('training_duration_seconds', 'Training job duration')
active_training_jobs = Gauge('active_training_jobs', 'Number of active training jobs')
gpu_utilization = Gauge('gpu_utilization_percent', 'GPU utilization percentage', ['node', 'gpu_id'])

# Database Models
class TrainingJob(Base):
    __tablename__ = "training_jobs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, running, completed, failed, cancelled
    config = Column(Text)  # JSON configuration
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    model_path = Column(String)
    metrics = Column(Text)  # JSON metrics
    hyperparameters = Column(Text)  # JSON hyperparameters
    resource_requirements = Column(Text)  # JSON resource specs
    k8s_job_name = Column(String)
    experiment_id = Column(String)
    run_id = Column(String)

Base.metadata.create_all(bind=engine)

# Pydantic Models
class ResourceRequirements(BaseModel):
    cpu: str = "2"
    memory: str = "4Gi"
    gpu: int = 1
    gpu_type: str = "nvidia.com/gpu"
    storage: str = "10Gi"

class TrainingConfig(BaseModel):
    framework: str = Field(..., description="pytorch or tensorflow")
    model_type: str = Field(..., description="Model architecture type")
    dataset_path: str = Field(..., description="Path to training dataset")
    hyperparameters: Dict[str, Any] = Field(default_factory=dict)
    epochs: int = Field(default=10, ge=1, le=1000)
    batch_size: int = Field(default=32, ge=1)
    learning_rate: float = Field(default=0.001, gt=0)
    distributed: bool = Field(default=False)
    num_workers: int = Field(default=1, ge=1, le=8)
    optimization_config: Optional[Dict[str, Any]] = None
    early_stopping: bool = Field(default=True)
    checkpoint_interval: int = Field(default=5, ge=1)

class TrainingJobRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    config: TrainingConfig
    resource_requirements: ResourceRequirements = ResourceRequirements()
    priority: int = Field(default=1, ge=1, le=5)
    tags: List[str] = Field(default_factory=list)

class TrainingJobResponse(BaseModel):
    id: str
    name: str
    status: str
    config: Dict[str, Any]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]
    model_path: Optional[str]
    metrics: Optional[Dict[str, Any]]
    resource_requirements: Dict[str, Any]
    experiment_id: Optional[str]
    run_id: Optional[str]

class HyperparameterOptimizationRequest(BaseModel):
    base_config: TrainingConfig
    optimization_config: Dict[str, Any]
    n_trials: int = Field(default=10, ge=1, le=100)
    timeout: int = Field(default=3600, ge=60)  # seconds

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

# Training orchestration functions
def create_k8s_training_job(job_id: str, config: TrainingConfig, resources: ResourceRequirements, user_id: str) -> str:
    """Create Kubernetes Job for model training"""
    
    job_name = f"training-job-{job_id[:8]}"
    
    # Container environment variables
    env_vars = [
        client.V1EnvVar(name="JOB_ID", value=job_id),
        client.V1EnvVar(name="USER_ID", value=user_id),
        client.V1EnvVar(name="MLFLOW_TRACKING_URI", value=MLFLOW_TRACKING_URI),
        client.V1EnvVar(name="S3_BUCKET", value=S3_BUCKET),
        client.V1EnvVar(name="DISTRIBUTED", value=str(config.distributed)),
        client.V1EnvVar(name="NUM_WORKERS", value=str(config.num_workers)),
    ]
    
    # Resource requirements
    resource_requirements = client.V1ResourceRequirements(
        requests={
            "cpu": resources.cpu,
            "memory": resources.memory,
            resources.gpu_type: str(resources.gpu)
        },
        limits={
            "cpu": resources.cpu,
            "memory": resources.memory,
            resources.gpu_type: str(resources.gpu)
        }
    )
    
    # Volume mounts for model storage
    volume_mounts = [
        client.V1VolumeMount(
            name="model-storage",
            mount_path="/models"
        ),
        client.V1VolumeMount(
            name="data-storage",
            mount_path="/data"
        )
    ]
    
    volumes = [
        client.V1Volume(
            name="model-storage",
            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                claim_name="model-storage-pvc"
            )
        ),
        client.V1Volume(
            name="data-storage",
            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                claim_name="data-storage-pvc"
            )
        )
    ]
    
    # Container specification
    container = client.V1Container(
        name="trainer",
        image="aic-aipaas/model-trainer:latest",
        env=env_vars,
        resources=resource_requirements,
        volume_mounts=volume_mounts,
        command=["python", "/app/trainer.py"],
        args=[json.dumps(config.dict())]
    )
    
    # Pod specification
    pod_spec = client.V1PodSpec(
        containers=[container],
        volumes=volumes,
        restart_policy="Never",
        node_selector={"workload-type": "ai-training"} if resources.gpu > 0 else None,
        tolerations=[
            client.V1Toleration(
                key="nvidia.com/gpu",
                operator="Equal",
                value="true",
                effect="NoSchedule"
            )
        ] if resources.gpu > 0 else None
    )
    
    # Job specification
    job_spec = client.V1JobSpec(
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={
                    "app": "model-training",
                    "job-id": job_id,
                    "user-id": user_id
                }
            ),
            spec=pod_spec
        ),
        backoff_limit=3,
        ttl_seconds_after_finished=86400  # 24 hours
    )
    
    # Job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(
            name=job_name,
            labels={
                "app": "model-training",
                "job-id": job_id,
                "user-id": user_id
            }
        ),
        spec=job_spec
    )
    
    try:
        k8s_batch_v1.create_namespaced_job(namespace="ai-services", body=job)
        logger.info(f"Created Kubernetes job: {job_name}")
        return job_name
    except ApiException as e:
        logger.error(f"Failed to create Kubernetes job: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create training job: {e}")

async def monitor_training_job(job_id: str, k8s_job_name: str):
    """Monitor training job progress"""
    db = SessionLocal()
    try:
        while True:
            # Check Kubernetes job status
            try:
                job = k8s_batch_v1.read_namespaced_job(name=k8s_job_name, namespace="ai-services")
                job_status = job.status
                
                # Update database based on job status
                db_job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
                if not db_job:
                    break
                
                if job_status.succeeded:
                    db_job.status = "completed"
                    db_job.completed_at = datetime.utcnow()
                    training_jobs_total.labels(status="completed").inc()
                    active_training_jobs.dec()
                elif job_status.failed:
                    db_job.status = "failed"
                    db_job.completed_at = datetime.utcnow()
                    db_job.error_message = "Training job failed"
                    training_jobs_total.labels(status="failed").inc()
                    active_training_jobs.dec()
                elif job_status.active:
                    if db_job.status == "pending":
                        db_job.status = "running"
                        db_job.started_at = datetime.utcnow()
                        active_training_jobs.inc()
                
                db.commit()
                
                if db_job.status in ["completed", "failed", "cancelled"]:
                    break
                    
            except ApiException as e:
                logger.error(f"Error monitoring job {job_id}: {e}")
                break
            
            await asyncio.sleep(30)  # Check every 30 seconds
            
    finally:
        db.close()

def optimize_hyperparameters(job_id: str, base_config: TrainingConfig, opt_config: Dict[str, Any], n_trials: int):
    """Hyperparameter optimization using Optuna"""
    
    def objective(trial):
        # Create trial-specific configuration
        trial_config = base_config.copy()
        
        # Sample hyperparameters based on optimization config
        for param, config in opt_config.items():
            if config["type"] == "float":
                value = trial.suggest_float(param, config["low"], config["high"])
            elif config["type"] == "int":
                value = trial.suggest_int(param, config["low"], config["high"])
            elif config["type"] == "categorical":
                value = trial.suggest_categorical(param, config["choices"])
            else:
                continue
            
            # Update configuration
            if param == "learning_rate":
                trial_config.learning_rate = value
            elif param == "batch_size":
                trial_config.batch_size = value
            elif param in trial_config.hyperparameters:
                trial_config.hyperparameters[param] = value
        
        # Run training with trial configuration
        # This would typically submit a training job and wait for results
        # For now, we'll simulate with a dummy metric
        return simulate_training_metric(trial_config)
    
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)
    
    return {
        "best_params": study.best_params,
        "best_value": study.best_value,
        "n_trials": len(study.trials)
    }

def simulate_training_metric(config: TrainingConfig) -> float:
    """Simulate training metric for hyperparameter optimization"""
    # This is a placeholder - in reality, this would run actual training
    import random
    base_score = 0.8
    lr_factor = min(1.0, config.learning_rate * 1000)  # Prefer moderate learning rates
    batch_factor = min(1.0, config.batch_size / 64)    # Prefer reasonable batch sizes
    return base_score * lr_factor * batch_factor + random.uniform(-0.1, 0.1)

# API Endpoints
@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "service": "model-training",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.post("/training/jobs", response_model=TrainingJobResponse)
async def create_training_job(
    request: TrainingJobRequest,
    background_tasks: BackgroundTasks,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create a new training job"""
    
    user_id = user_info.get("user", "unknown")
    
    # Create training job record
    job = TrainingJob(
        name=request.name,
        user_id=user_id,
        config=json.dumps(request.config.dict()),
        resource_requirements=json.dumps(request.resource_requirements.dict()),
        status="pending"
    )
    
    db.add(job)
    db.commit()
    db.refresh(job)
    
    try:
        # Create Kubernetes job
        k8s_job_name = create_k8s_training_job(
            job.id, 
            request.config, 
            request.resource_requirements,
            user_id
        )
        
        # Update job with Kubernetes job name
        job.k8s_job_name = k8s_job_name
        db.commit()
        
        # Start monitoring in background
        background_tasks.add_task(monitor_training_job, job.id, k8s_job_name)
        
        training_jobs_total.labels(status="created").inc()
        
        return TrainingJobResponse(
            id=job.id,
            name=job.name,
            status=job.status,
            config=json.loads(job.config),
            created_at=job.created_at,
            started_at=job.started_at,
            completed_at=job.completed_at,
            error_message=job.error_message,
            model_path=job.model_path,
            metrics=json.loads(job.metrics) if job.metrics else None,
            resource_requirements=json.loads(job.resource_requirements),
            experiment_id=job.experiment_id,
            run_id=job.run_id
        )
        
    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Failed to create training job: {e}")

@app.get("/training/jobs", response_model=List[TrainingJobResponse])
async def list_training_jobs(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """List training jobs"""
    
    user_id = user_info.get("user", "unknown")
    
    query = db.query(TrainingJob).filter(TrainingJob.user_id == user_id)
    
    if status:
        query = query.filter(TrainingJob.status == status)
    
    jobs = query.offset(offset).limit(limit).all()
    
    return [
        TrainingJobResponse(
            id=job.id,
            name=job.name,
            status=job.status,
            config=json.loads(job.config),
            created_at=job.created_at,
            started_at=job.started_at,
            completed_at=job.completed_at,
            error_message=job.error_message,
            model_path=job.model_path,
            metrics=json.loads(job.metrics) if job.metrics else None,
            resource_requirements=json.loads(job.resource_requirements),
            experiment_id=job.experiment_id,
            run_id=job.run_id
        )
        for job in jobs
    ]

@app.get("/training/jobs/{job_id}", response_model=TrainingJobResponse)
async def get_training_job(
    job_id: str,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get training job details"""
    
    user_id = user_info.get("user", "unknown")
    
    job = db.query(TrainingJob).filter(
        TrainingJob.id == job_id,
        TrainingJob.user_id == user_id
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Training job not found")
    
    return TrainingJobResponse(
        id=job.id,
        name=job.name,
        status=job.status,
        config=json.loads(job.config),
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
        error_message=job.error_message,
        model_path=job.model_path,
        metrics=json.loads(job.metrics) if job.metrics else None,
        resource_requirements=json.loads(job.resource_requirements),
        experiment_id=job.experiment_id,
        run_id=job.run_id
    )

@app.delete("/training/jobs/{job_id}")
async def cancel_training_job(
    job_id: str,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Cancel a training job"""
    
    user_id = user_info.get("user", "unknown")
    
    job = db.query(TrainingJob).filter(
        TrainingJob.id == job_id,
        TrainingJob.user_id == user_id
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Training job not found")
    
    if job.status in ["completed", "failed", "cancelled"]:
        raise HTTPException(status_code=400, detail="Cannot cancel completed job")
    
    try:
        # Delete Kubernetes job
        if job.k8s_job_name:
            k8s_batch_v1.delete_namespaced_job(
                name=job.k8s_job_name,
                namespace="ai-services",
                body=client.V1DeleteOptions(propagation_policy="Background")
            )
        
        # Update job status
        job.status = "cancelled"
        job.completed_at = datetime.utcnow()
        db.commit()
        
        training_jobs_total.labels(status="cancelled").inc()
        active_training_jobs.dec()
        
        return {"message": "Training job cancelled successfully"}
        
    except ApiException as e:
        logger.error(f"Failed to cancel job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to cancel training job")

@app.post("/training/optimize")
async def optimize_hyperparameters_endpoint(
    request: HyperparameterOptimizationRequest,
    background_tasks: BackgroundTasks,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Start hyperparameter optimization"""
    
    user_id = user_info.get("user", "unknown")
    
    # Create optimization job
    job = TrainingJob(
        name=f"optimization-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
        user_id=user_id,
        config=json.dumps(request.base_config.dict()),
        status="running"
    )
    
    db.add(job)
    db.commit()
    db.refresh(job)
    
    # Start optimization in background
    def run_optimization():
        try:
            result = optimize_hyperparameters(
                job.id,
                request.base_config,
                request.optimization_config,
                request.n_trials
            )
            
            # Update job with results
            db_session = SessionLocal()
            db_job = db_session.query(TrainingJob).filter(TrainingJob.id == job.id).first()
            if db_job:
                db_job.status = "completed"
                db_job.completed_at = datetime.utcnow()
                db_job.metrics = json.dumps(result)
                db_session.commit()
            db_session.close()
            
        except Exception as e:
            logger.error(f"Optimization failed: {e}")
            db_session = SessionLocal()
            db_job = db_session.query(TrainingJob).filter(TrainingJob.id == job.id).first()
            if db_job:
                db_job.status = "failed"
                db_job.error_message = str(e)
                db_job.completed_at = datetime.utcnow()
                db_session.commit()
            db_session.close()
    
    background_tasks.add_task(run_optimization)
    
    return {"job_id": job.id, "message": "Hyperparameter optimization started"}

@app.get("/training/resources/gpu")
async def get_gpu_resources(user_info: dict = Depends(verify_token)):
    """Get available GPU resources"""
    
    try:
        nodes = k8s_core_v1.list_node(label_selector="workload-type=ai-training")
        gpu_info = []
        
        for node in nodes.items:
            node_name = node.metadata.name
            allocatable = node.status.allocatable or {}
            capacity = node.status.capacity or {}
            
            gpu_allocatable = int(allocatable.get("nvidia.com/gpu", 0))
            gpu_capacity = int(capacity.get("nvidia.com/gpu", 0))
            
            if gpu_capacity > 0:
                gpu_info.append({
                    "node": node_name,
                    "gpu_capacity": gpu_capacity,
                    "gpu_allocatable": gpu_allocatable,
                    "gpu_used": gpu_capacity - gpu_allocatable
                })
        
        return {"gpu_nodes": gpu_info}
        
    except ApiException as e:
        logger.error(f"Failed to get GPU resources: {e}")
        raise HTTPException(status_code=500, detail="Failed to get GPU resources")

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

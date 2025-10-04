"""
AIC AI Platform Feature Store Service
Feature definition, storage, and serving with Feast integration
"""

import json
import logging
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
from feast import FeatureStore, Entity, FeatureView, Field as FeastField, FileSource, ValueType
from feast.types import Float32, Float64, Int32, Int64, String, Bool, UnixTimestamp
import redis
from sqlalchemy import create_engine, Column, String, DateTime, Text, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import requests
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import boto3
import pyarrow as pa
import pyarrow.parquet as pq

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="AIC AI Platform Feature Store Service",
    description="Feature definition, storage, and serving with data quality monitoring",
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
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/feature_store")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
S3_BUCKET = os.getenv("S3_BUCKET", "aic-aipaas-features")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
FEAST_REPO_PATH = os.getenv("FEAST_REPO_PATH", "/feast_repo")

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis client
redis_client = redis.from_url(REDIS_URL)

# S3 client
s3_client = boto3.client('s3')

# Initialize Feast
os.makedirs(FEAST_REPO_PATH, exist_ok=True)
feast_store = FeatureStore(repo_path=FEAST_REPO_PATH)

# Prometheus metrics
feature_requests_total = Counter('feature_requests_total', 'Total feature requests', ['feature_view', 'type'])
feature_serving_duration = Histogram('feature_serving_duration_seconds', 'Feature serving duration')
feature_quality_score = Gauge('feature_quality_score', 'Feature quality score', ['feature_view'])
active_feature_views = Gauge('active_feature_views_total', 'Total active feature views')

# Database Models
class FeatureDefinition(Base):
    __tablename__ = "feature_definitions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    owner_id = Column(String, nullable=False)
    feature_view_name = Column(String, nullable=False)
    data_type = Column(String, nullable=False)
    source_table = Column(String)
    transformation_logic = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    tags = Column(Text)  # JSON
    status = Column(String, default="active")
    quality_metrics = Column(Text)  # JSON

class FeatureViewDefinition(Base):
    __tablename__ = "feature_view_definitions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    owner_id = Column(String, nullable=False)
    entity_name = Column(String, nullable=False)
    source_config = Column(Text)  # JSON
    features = Column(Text)  # JSON list of feature names
    ttl_seconds = Column(Integer, default=86400)  # 24 hours
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="active")

class FeatureServingLog(Base):
    __tablename__ = "feature_serving_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    feature_view_name = Column(String, nullable=False)
    entity_keys = Column(Text)  # JSON
    features_requested = Column(Text)  # JSON
    features_served = Column(Text)  # JSON
    serving_time = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String)
    request_type = Column(String)  # online, offline

Base.metadata.create_all(bind=engine)

# Pydantic Models
class FeatureSchema(BaseModel):
    name: str
    dtype: str  # float32, float64, int32, int64, string, bool
    description: Optional[str] = None

class DataSourceConfig(BaseModel):
    type: str  # file, bigquery, redshift, snowflake
    path: Optional[str] = None  # For file sources
    query: Optional[str] = None  # For SQL sources
    timestamp_field: str = "event_timestamp"
    created_timestamp_field: Optional[str] = None

class FeatureViewRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    entity_name: str
    features: List[FeatureSchema]
    source: DataSourceConfig
    ttl_hours: int = Field(default=24, ge=1, le=8760)  # Max 1 year
    tags: List[str] = Field(default_factory=list)

class EntityRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    value_type: str = "string"  # string, int32, int64
    join_keys: List[str] = Field(default_factory=list)

class FeatureServingRequest(BaseModel):
    feature_view: str
    entities: Dict[str, Union[str, int, List[Union[str, int]]]]
    features: Optional[List[str]] = None  # If None, return all features
    full_feature_names: bool = False

class OfflineFeatureRequest(BaseModel):
    feature_views: List[str]
    entity_df: Dict[str, Any]  # Pandas DataFrame as dict
    features: Optional[List[str]] = None

class FeatureQualityMetrics(BaseModel):
    completeness: float  # Percentage of non-null values
    uniqueness: float    # Percentage of unique values
    validity: float      # Percentage of valid values
    consistency: float   # Consistency score
    timeliness: float    # Data freshness score

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
def get_feast_value_type(dtype: str) -> ValueType:
    """Convert string dtype to Feast ValueType"""
    type_mapping = {
        "float32": ValueType.FLOAT,
        "float64": ValueType.DOUBLE,
        "int32": ValueType.INT32,
        "int64": ValueType.INT64,
        "string": ValueType.STRING,
        "bool": ValueType.BOOL,
        "timestamp": ValueType.UNIX_TIMESTAMP
    }
    return type_mapping.get(dtype.lower(), ValueType.STRING)

def create_feast_entity(name: str, description: str, value_type: str, join_keys: List[str]) -> Entity:
    """Create Feast entity"""
    return Entity(
        name=name,
        description=description,
        value_type=get_feast_value_type(value_type),
        join_keys=join_keys or [name]
    )

def create_feast_feature_view(
    name: str,
    entities: List[str],
    features: List[FeatureSchema],
    source: DataSourceConfig,
    ttl: timedelta,
    description: str = None
) -> FeatureView:
    """Create Feast feature view"""
    
    # Create data source
    if source.type == "file":
        data_source = FileSource(
            path=source.path,
            timestamp_field=source.timestamp_field,
            created_timestamp_column=source.created_timestamp_field
        )
    else:
        # For other source types, we'd need to implement specific connectors
        raise HTTPException(status_code=400, detail=f"Source type {source.type} not supported yet")
    
    # Create feature fields
    feature_fields = []
    for feature in features:
        feature_fields.append(
            FeastField(
                name=feature.name,
                dtype=get_feast_value_type(feature.dtype)
            )
        )
    
    return FeatureView(
        name=name,
        entities=entities,
        schema=feature_fields,
        source=data_source,
        ttl=ttl,
        description=description
    )

def calculate_feature_quality(df: pd.DataFrame, feature_name: str) -> FeatureQualityMetrics:
    """Calculate feature quality metrics"""
    if feature_name not in df.columns:
        return FeatureQualityMetrics(
            completeness=0.0,
            uniqueness=0.0,
            validity=0.0,
            consistency=0.0,
            timeliness=0.0
        )
    
    series = df[feature_name]
    total_count = len(series)
    
    # Completeness: percentage of non-null values
    completeness = (total_count - series.isnull().sum()) / total_count if total_count > 0 else 0.0
    
    # Uniqueness: percentage of unique values
    uniqueness = series.nunique() / total_count if total_count > 0 else 0.0
    
    # Validity: percentage of valid values (non-null, non-infinite)
    if series.dtype in ['float64', 'float32']:
        valid_count = series.replace([np.inf, -np.inf], np.nan).notna().sum()
    else:
        valid_count = series.notna().sum()
    validity = valid_count / total_count if total_count > 0 else 0.0
    
    # Consistency: coefficient of variation (for numerical data)
    if series.dtype in ['float64', 'float32', 'int64', 'int32'] and series.std() != 0:
        consistency = 1.0 - min(series.std() / abs(series.mean()), 1.0) if series.mean() != 0 else 0.5
    else:
        consistency = 0.8  # Default for categorical data
    
    # Timeliness: based on data freshness (simplified)
    timeliness = 1.0  # Assume data is fresh for now
    
    return FeatureQualityMetrics(
        completeness=completeness,
        uniqueness=uniqueness,
        validity=validity,
        consistency=consistency,
        timeliness=timeliness
    )

# API Endpoints
@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "service": "feature-store",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.post("/entities")
async def create_entity(
    request: EntityRequest,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create a new entity"""
    
    user_id = user_info.get("user", "unknown")
    
    try:
        # Create Feast entity
        entity = create_feast_entity(
            name=request.name,
            description=request.description,
            value_type=request.value_type,
            join_keys=request.join_keys
        )
        
        # Apply to Feast store
        feast_store.apply([entity])
        
        return {
            "name": request.name,
            "description": request.description,
            "value_type": request.value_type,
            "join_keys": request.join_keys or [request.name],
            "created_by": user_id,
            "created_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to create entity: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create entity: {e}")

@app.post("/feature-views")
async def create_feature_view(
    request: FeatureViewRequest,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create a new feature view"""
    
    user_id = user_info.get("user", "unknown")
    
    # Check if feature view already exists
    existing = db.query(FeatureViewDefinition).filter(
        FeatureViewDefinition.name == request.name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Feature view already exists")
    
    try:
        # Create Feast feature view
        ttl = timedelta(hours=request.ttl_hours)
        feature_view = create_feast_feature_view(
            name=request.name,
            entities=[request.entity_name],
            features=request.features,
            source=request.source,
            ttl=ttl,
            description=request.description
        )
        
        # Apply to Feast store
        feast_store.apply([feature_view])
        
        # Store in database
        feature_view_def = FeatureViewDefinition(
            name=request.name,
            description=request.description,
            owner_id=user_id,
            entity_name=request.entity_name,
            source_config=json.dumps(request.source.dict()),
            features=json.dumps([f.dict() for f in request.features]),
            ttl_seconds=request.ttl_hours * 3600
        )
        
        db.add(feature_view_def)
        db.commit()
        db.refresh(feature_view_def)
        
        active_feature_views.inc()
        
        return {
            "id": feature_view_def.id,
            "name": feature_view_def.name,
            "description": feature_view_def.description,
            "entity_name": feature_view_def.entity_name,
            "features": json.loads(feature_view_def.features),
            "ttl_hours": request.ttl_hours,
            "created_at": feature_view_def.created_at.isoformat(),
            "status": feature_view_def.status
        }
        
    except Exception as e:
        logger.error(f"Failed to create feature view: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create feature view: {e}")

@app.get("/feature-views")
async def list_feature_views(
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """List all feature views"""
    
    feature_views = db.query(FeatureViewDefinition).filter(
        FeatureViewDefinition.status == "active"
    ).all()
    
    return [
        {
            "id": fv.id,
            "name": fv.name,
            "description": fv.description,
            "entity_name": fv.entity_name,
            "features": json.loads(fv.features),
            "ttl_hours": fv.ttl_seconds // 3600,
            "created_at": fv.created_at.isoformat(),
            "updated_at": fv.updated_at.isoformat(),
            "status": fv.status
        }
        for fv in feature_views
    ]

@app.post("/features/online")
async def get_online_features(
    request: FeatureServingRequest,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get online features for real-time inference"""
    
    user_id = user_info.get("user", "unknown")
    
    try:
        start_time = datetime.utcnow()
        
        # Prepare entity DataFrame
        entity_rows = []
        if isinstance(list(request.entities.values())[0], list):
            # Multiple entities
            for i in range(len(list(request.entities.values())[0])):
                row = {key: values[i] for key, values in request.entities.items()}
                entity_rows.append(row)
        else:
            # Single entity
            entity_rows.append(request.entities)
        
        entity_df = pd.DataFrame(entity_rows)
        
        # Get features from Feast
        feature_vector = feast_store.get_online_features(
            features=[f"{request.feature_view}:{feature}" for feature in (request.features or [])],
            entity_rows=entity_df.to_dict('records')
        )
        
        # Convert to response format
        result = feature_vector.to_dict()
        
        # Log serving request
        serving_time = (datetime.utcnow() - start_time).total_seconds()
        
        log_entry = FeatureServingLog(
            feature_view_name=request.feature_view,
            entity_keys=json.dumps(request.entities),
            features_requested=json.dumps(request.features),
            features_served=json.dumps(list(result.keys())),
            serving_time=serving_time,
            user_id=user_id,
            request_type="online"
        )
        db.add(log_entry)
        db.commit()
        
        # Update metrics
        feature_requests_total.labels(
            feature_view=request.feature_view,
            type="online"
        ).inc()
        feature_serving_duration.observe(serving_time)
        
        return {
            "features": result,
            "serving_time": serving_time,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get online features: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get online features: {e}")

@app.post("/features/offline")
async def get_offline_features(
    request: OfflineFeatureRequest,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get offline features for training"""
    
    user_id = user_info.get("user", "unknown")
    
    try:
        start_time = datetime.utcnow()
        
        # Convert entity_df dict back to DataFrame
        entity_df = pd.DataFrame(request.entity_df)
        
        # Prepare feature references
        feature_refs = []
        for fv_name in request.feature_views:
            if request.features:
                for feature in request.features:
                    feature_refs.append(f"{fv_name}:{feature}")
            else:
                # Get all features from feature view
                fv_def = db.query(FeatureViewDefinition).filter(
                    FeatureViewDefinition.name == fv_name
                ).first()
                if fv_def:
                    features = json.loads(fv_def.features)
                    for feature in features:
                        feature_refs.append(f"{fv_name}:{feature['name']}")
        
        # Get historical features
        training_df = feast_store.get_historical_features(
            entity_df=entity_df,
            features=feature_refs
        ).to_df()
        
        # Convert to response format
        result = training_df.to_dict('records')
        
        serving_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Log serving request
        log_entry = FeatureServingLog(
            feature_view_name=",".join(request.feature_views),
            entity_keys=json.dumps({"count": len(entity_df)}),
            features_requested=json.dumps(request.features),
            features_served=json.dumps(list(training_df.columns.tolist())),
            serving_time=serving_time,
            user_id=user_id,
            request_type="offline"
        )
        db.add(log_entry)
        db.commit()
        
        # Update metrics
        for fv_name in request.feature_views:
            feature_requests_total.labels(
                feature_view=fv_name,
                type="offline"
            ).inc()
        
        return {
            "features": result,
            "row_count": len(result),
            "serving_time": serving_time,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get offline features: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get offline features: {e}")

@app.get("/feature-views/{feature_view_name}/quality")
async def get_feature_quality(
    feature_view_name: str,
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get feature quality metrics"""
    
    try:
        # Get feature view definition
        fv_def = db.query(FeatureViewDefinition).filter(
            FeatureViewDefinition.name == feature_view_name
        ).first()
        
        if not fv_def:
            raise HTTPException(status_code=404, detail="Feature view not found")
        
        # Load sample data for quality analysis
        source_config = json.loads(fv_def.source_config)
        
        if source_config["type"] == "file":
            # Load data from file
            df = pd.read_parquet(source_config["path"])
        else:
            raise HTTPException(status_code=400, detail="Quality analysis not supported for this source type")
        
        # Calculate quality metrics for each feature
        features = json.loads(fv_def.features)
        quality_metrics = {}
        
        for feature in features:
            feature_name = feature["name"]
            metrics = calculate_feature_quality(df, feature_name)
            quality_metrics[feature_name] = metrics.dict()
            
            # Update Prometheus metric
            overall_score = (
                metrics.completeness + metrics.validity + 
                metrics.consistency + metrics.timeliness
            ) / 4
            feature_quality_score.labels(feature_view=feature_view_name).set(overall_score)
        
        return {
            "feature_view": feature_view_name,
            "quality_metrics": quality_metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get feature quality: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get feature quality: {e}")

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)

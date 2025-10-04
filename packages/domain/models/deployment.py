"""
Simplified Deployment domain model for testing.
"""

from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class DeploymentStatus(str, Enum):
    """Deployment status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class Deployment(BaseModel):
    """Simplified Deployment domain model."""
    
    id: str
    application_id: str
    version: str
    status: DeploymentStatus = DeploymentStatus.PENDING
    strategy: str = "rolling"
    progress: int = 0
    logs: list = []
    created_at: datetime = datetime.now()
    completed_at: Optional[datetime] = None
    
    class Config:
        use_enum_values = True

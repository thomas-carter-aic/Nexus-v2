"""
Simplified Application domain model for testing.
"""

from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class ApplicationStatus(str, Enum):
    """Application status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    DEPLOYING = "deploying"


class Application(BaseModel):
    """Simplified Application domain model."""
    
    id: str
    name: str
    status: ApplicationStatus = ApplicationStatus.PENDING
    image: Optional[str] = None
    cpu: float = 0.5
    memory: int = 512
    replicas: int = 1
    environment: Dict[str, str] = {}
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
    class Config:
        use_enum_values = True

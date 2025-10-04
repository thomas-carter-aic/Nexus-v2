"""
Simplified Resource domain model for testing.
"""

from typing import Optional
from pydantic import BaseModel


class ResourceRequirements(BaseModel):
    """Simplified Resource requirements model."""
    
    cpu: float = 0.5  # CPU cores
    memory: int = 512  # Memory in MB
    storage: int = 1024  # Storage in MB
    network_bandwidth: Optional[int] = None  # Network bandwidth in Mbps
    
    def __str__(self) -> str:
        return f"CPU: {self.cpu}, Memory: {self.memory}MB, Storage: {self.storage}MB"

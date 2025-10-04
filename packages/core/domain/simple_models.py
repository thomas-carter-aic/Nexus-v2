"""
Simplified Domain Models for Build Testing

This module contains simplified versions of the domain models
that can be used for build verification without complex dependencies.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4


class ApplicationStatus(Enum):
    """Enumeration of possible application states"""
    PENDING = "pending"
    BUILDING = "building"
    DEPLOYING = "deploying"
    RUNNING = "running"
    SCALING = "scaling"
    UPDATING = "updating"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"
    MAINTENANCE = "maintenance"


class ScalingStrategy(Enum):
    """Different scaling strategies supported by the platform"""
    MANUAL = "manual"
    REACTIVE = "reactive"
    PREDICTIVE = "predictive"
    SCHEDULED = "scheduled"
    HYBRID = "hybrid"


@dataclass(frozen=True)
class UserId:
    """Value object representing a unique user identifier"""
    value: str
    
    def __post_init__(self):
        if not self.value or not isinstance(self.value, str):
            raise ValueError("UserId must be a non-empty string")


@dataclass(frozen=True)
class ApplicationId:
    """Value object representing a unique application identifier"""
    value: UUID
    
    def __post_init__(self):
        if not isinstance(self.value, UUID):
            raise ValueError("ApplicationId must be a UUID")
    
    @classmethod
    def generate(cls) -> 'ApplicationId':
        """Generate a new unique application ID"""
        return cls(uuid4())


@dataclass(frozen=True)
class ResourceRequirements:
    """Value object representing resource requirements for an application"""
    cpu_cores: float
    memory_mb: int
    storage_gb: int
    network_bandwidth_mbps: Optional[int] = None
    gpu_count: Optional[int] = None
    
    def __post_init__(self):
        if self.cpu_cores <= 0:
            raise ValueError("CPU cores must be positive")
        if self.memory_mb <= 0:
            raise ValueError("Memory must be positive")
        if self.storage_gb <= 0:
            raise ValueError("Storage must be positive")


@dataclass(frozen=True)
class ScalingConfiguration:
    """Value object representing scaling configuration for an application"""
    strategy: ScalingStrategy
    min_instances: int
    max_instances: int
    target_cpu_utilization: Optional[float] = None
    target_memory_utilization: Optional[float] = None
    
    def __post_init__(self):
        if self.min_instances < 1:
            raise ValueError("Minimum instances must be at least 1")
        if self.max_instances < self.min_instances:
            raise ValueError("Maximum instances must be >= minimum instances")


class Application:
    """
    Simplified Application aggregate for build testing.
    """
    
    def __init__(self, 
                 application_id: ApplicationId,
                 name: str,
                 user_id: UserId,
                 resource_requirements: ResourceRequirements,
                 scaling_config: ScalingConfiguration):
        """Initialize a new application aggregate."""
        if not name or not isinstance(name, str):
            raise ValueError("Application name must be a non-empty string")
        
        self._id = application_id
        self._name = name
        self._user_id = user_id
        self._resource_requirements = resource_requirements
        self._scaling_config = scaling_config
        self._status = ApplicationStatus.PENDING
        self._current_instance_count = scaling_config.min_instances
        self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()
        self._version = 1
        self._events = []
    
    @property
    def id(self) -> ApplicationId:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def user_id(self) -> UserId:
        return self._user_id
    
    @property
    def status(self) -> ApplicationStatus:
        return self._status
    
    @property
    def resource_requirements(self) -> ResourceRequirements:
        return self._resource_requirements
    
    @property
    def scaling_config(self) -> ScalingConfiguration:
        return self._scaling_config
    
    @property
    def current_instance_count(self) -> int:
        return self._current_instance_count
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    @property
    def version(self) -> int:
        return self._version
    
    def deploy(self) -> None:
        """Deploy the application."""
        if self._status != ApplicationStatus.PENDING:
            raise ValueError(f"Cannot deploy application in {self._status.value} status")
        
        self._status = ApplicationStatus.DEPLOYING
        self._updated_at = datetime.utcnow()
        self._version += 1
        self._events.append(f"Deployment started at {self._updated_at}")
    
    def mark_as_running(self) -> None:
        """Mark the application as successfully running."""
        if self._status != ApplicationStatus.DEPLOYING:
            raise ValueError(f"Cannot mark application as running from {self._status.value} status")
        
        self._status = ApplicationStatus.RUNNING
        self._updated_at = datetime.utcnow()
        self._version += 1
        self._events.append(f"Application running at {self._updated_at}")
    
    def scale(self, new_instance_count: int, reason: str, ai_confidence: Optional[float] = None) -> None:
        """Scale the application to a new instance count."""
        if new_instance_count < self._scaling_config.min_instances:
            raise ValueError(f"Cannot scale below minimum instances ({self._scaling_config.min_instances})")
        if new_instance_count > self._scaling_config.max_instances:
            raise ValueError(f"Cannot scale above maximum instances ({self._scaling_config.max_instances})")
        
        if new_instance_count == self._current_instance_count:
            return
        
        previous_count = self._current_instance_count
        self._current_instance_count = new_instance_count
        self._status = ApplicationStatus.SCALING
        self._updated_at = datetime.utcnow()
        self._version += 1
        
        self._events.append(f"Scaled from {previous_count} to {new_instance_count}: {reason}")
    
    def get_uncommitted_events(self) -> List[str]:
        """Get the list of uncommitted events (simplified)"""
        return self._events.copy()
    
    def mark_events_as_committed(self) -> None:
        """Mark all events as committed"""
        self._events.clear()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the application to a dictionary representation"""
        return {
            'id': str(self._id.value),
            'name': self._name,
            'user_id': self._user_id.value,
            'status': self._status.value,
            'current_instance_count': self._current_instance_count,
            'resource_requirements': {
                'cpu_cores': self._resource_requirements.cpu_cores,
                'memory_mb': self._resource_requirements.memory_mb,
                'storage_gb': self._resource_requirements.storage_gb,
                'network_bandwidth_mbps': self._resource_requirements.network_bandwidth_mbps,
                'gpu_count': self._resource_requirements.gpu_count
            },
            'scaling_config': {
                'strategy': self._scaling_config.strategy.value,
                'min_instances': self._scaling_config.min_instances,
                'max_instances': self._scaling_config.max_instances,
                'target_cpu_utilization': self._scaling_config.target_cpu_utilization,
                'target_memory_utilization': self._scaling_config.target_memory_utilization
            },
            'created_at': self._created_at.isoformat(),
            'updated_at': self._updated_at.isoformat(),
            'version': self._version
        }

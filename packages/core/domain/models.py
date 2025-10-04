"""
Domain Models for AI-Native PaaS Platform

This module defines the core domain models that represent the business entities
and value objects in the PaaS platform. These models are framework-agnostic
and contain the essential business logic.

Architecture Pattern: Domain-Driven Design (DDD) with Clean Architecture
- Entities: Objects with identity that persist over time
- Value Objects: Immutable objects defined by their attributes
- Aggregates: Consistency boundaries for related entities
- Domain Events: Represent significant business occurrences
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from uuid import UUID, uuid4
import json


class ApplicationStatus(Enum):
    """Enumeration of possible application states in the platform"""
    PENDING = "pending"           # Application deployment initiated but not started
    BUILDING = "building"         # Application is being built and containerized
    DEPLOYING = "deploying"       # Application is being deployed to runtime environment
    RUNNING = "running"           # Application is successfully running and serving traffic
    SCALING = "scaling"           # Application is being scaled up or down
    UPDATING = "updating"         # Application is being updated with new version
    STOPPING = "stopping"         # Application is being gracefully stopped
    STOPPED = "stopped"           # Application has been stopped and is not serving traffic
    FAILED = "failed"             # Application deployment or runtime has failed
    MAINTENANCE = "maintenance"   # Application is in maintenance mode


class ScalingStrategy(Enum):
    """Different scaling strategies supported by the platform"""
    MANUAL = "manual"             # Manual scaling controlled by user
    REACTIVE = "reactive"         # Reactive scaling based on current metrics
    PREDICTIVE = "predictive"     # AI-driven predictive scaling based on patterns
    SCHEDULED = "scheduled"       # Time-based scheduled scaling
    HYBRID = "hybrid"             # Combination of multiple strategies


class EventType(Enum):
    """Types of domain events that can occur in the system"""
    APPLICATION_CREATED = "application_created"
    APPLICATION_DEPLOYED = "application_deployed"
    APPLICATION_SCALED = "application_scaled"
    APPLICATION_UPDATED = "application_updated"
    APPLICATION_DELETED = "application_deleted"
    DEPLOYMENT_STARTED = "deployment_started"
    DEPLOYMENT_COMPLETED = "deployment_completed"
    DEPLOYMENT_FAILED = "deployment_failed"
    SCALING_TRIGGERED = "scaling_triggered"
    SCALING_COMPLETED = "scaling_completed"
    ERROR_OCCURRED = "error_occurred"
    PERFORMANCE_ANOMALY_DETECTED = "performance_anomaly_detected"
    COST_OPTIMIZATION_APPLIED = "cost_optimization_applied"
    PLUGIN_INSTALLED = "plugin_installed"
    PLUGIN_UPDATED = "plugin_updated"
    PLUGIN_REMOVED = "plugin_removed"


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
    cpu_cores: float                    # Number of CPU cores required
    memory_mb: int                      # Memory requirement in megabytes
    storage_gb: int                     # Storage requirement in gigabytes
    network_bandwidth_mbps: Optional[int] = None  # Network bandwidth in Mbps
    gpu_count: Optional[int] = None     # Number of GPUs required
    
    def __post_init__(self):
        # Validate resource requirements are positive
        if self.cpu_cores <= 0:
            raise ValueError("CPU cores must be positive")
        if self.memory_mb <= 0:
            raise ValueError("Memory must be positive")
        if self.storage_gb <= 0:
            raise ValueError("Storage must be positive")
        if self.network_bandwidth_mbps is not None and self.network_bandwidth_mbps <= 0:
            raise ValueError("Network bandwidth must be positive")
        if self.gpu_count is not None and self.gpu_count < 0:
            raise ValueError("GPU count cannot be negative")
    
    def scale(self, factor: float) -> 'ResourceRequirements':
        """Scale resource requirements by a given factor"""
        return ResourceRequirements(
            cpu_cores=self.cpu_cores * factor,
            memory_mb=int(self.memory_mb * factor),
            storage_gb=int(self.storage_gb * factor),
            network_bandwidth_mbps=int(self.network_bandwidth_mbps * factor) if self.network_bandwidth_mbps else None,
            gpu_count=int(self.gpu_count * factor) if self.gpu_count else None
        )


@dataclass(frozen=True)
class ScalingConfiguration:
    """Value object representing scaling configuration for an application"""
    strategy: ScalingStrategy           # The scaling strategy to use
    min_instances: int                  # Minimum number of instances
    max_instances: int                  # Maximum number of instances
    target_cpu_utilization: Optional[float] = None    # Target CPU utilization percentage
    target_memory_utilization: Optional[float] = None # Target memory utilization percentage
    scale_up_cooldown_seconds: int = 300              # Cooldown period after scaling up
    scale_down_cooldown_seconds: int = 300            # Cooldown period after scaling down
    custom_metrics: Optional[Dict[str, Any]] = None   # Custom metrics for scaling decisions
    
    def __post_init__(self):
        # Validate scaling configuration parameters
        if self.min_instances < 1:
            raise ValueError("Minimum instances must be at least 1")
        if self.max_instances < self.min_instances:
            raise ValueError("Maximum instances must be >= minimum instances")
        if self.target_cpu_utilization is not None and not (0 < self.target_cpu_utilization <= 100):
            raise ValueError("Target CPU utilization must be between 0 and 100")
        if self.target_memory_utilization is not None and not (0 < self.target_memory_utilization <= 100):
            raise ValueError("Target memory utilization must be between 0 and 100")
        if self.scale_up_cooldown_seconds < 0:
            raise ValueError("Scale up cooldown cannot be negative")
        if self.scale_down_cooldown_seconds < 0:
            raise ValueError("Scale down cooldown cannot be negative")


@dataclass
class DomainEvent:
    """Base class for all domain events in the system"""
    aggregate_id: UUID                                 # ID of the aggregate that generated the event
    event_type: EventType                              # Type of the event
    event_id: UUID = field(default_factory=uuid4)     # Unique identifier for the event
    timestamp: datetime = field(default_factory=datetime.utcnow)  # When the event occurred
    version: int = field(default=1)                   # Event schema version for evolution
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional event metadata
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary for serialization"""
        return {
            'event_id': str(self.event_id),
            'event_type': self.event_type.value,
            'aggregate_id': str(self.aggregate_id),
            'timestamp': self.timestamp.isoformat(),
            'version': self.version,
            'metadata': self.metadata,
            'data': self._get_event_data()
        }
    
    def _get_event_data(self) -> Dict[str, Any]:
        """Get event-specific data (to be implemented by subclasses)"""
        return {}


@dataclass
class ApplicationCreatedEvent:
    """Event raised when a new application is created"""
    aggregate_id: UUID
    application_name: str
    user_id: UserId
    resource_requirements: ResourceRequirements
    event_id: UUID = field(default_factory=uuid4)
    event_type: EventType = field(default=EventType.APPLICATION_CREATED)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: int = field(default=1)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary for serialization"""
        return {
            'event_id': str(self.event_id),
            'event_type': self.event_type.value,
            'aggregate_id': str(self.aggregate_id),
            'timestamp': self.timestamp.isoformat(),
            'version': self.version,
            'metadata': self.metadata,
            'data': self._get_event_data()
        }
    
    def _get_event_data(self) -> Dict[str, Any]:
        return {
            'application_name': self.application_name,
            'user_id': self.user_id.value,
            'resource_requirements': {
                'cpu': self.resource_requirements.cpu,
                'memory': self.resource_requirements.memory,
                'storage': self.resource_requirements.storage
            }
        }
    
    def _get_event_data(self) -> Dict[str, Any]:
        return {
            'application_name': self.application_name,
            'user_id': self.user_id.value,
            'resource_requirements': {
                'cpu_cores': self.resource_requirements.cpu_cores,
                'memory_mb': self.resource_requirements.memory_mb,
                'storage_gb': self.resource_requirements.storage_gb,
                'network_bandwidth_mbps': self.resource_requirements.network_bandwidth_mbps,
                'gpu_count': self.resource_requirements.gpu_count
            }
        }


@dataclass
class ApplicationScaledEvent:
    """Event raised when an application is scaled"""
    aggregate_id: UUID
    previous_instance_count: int
    new_instance_count: int
    scaling_reason: str
    event_id: UUID = field(default_factory=uuid4)
    event_type: EventType = field(default=EventType.APPLICATION_SCALED)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: int = field(default=1)
    metadata: Dict[str, Any] = field(default_factory=dict)
    ai_prediction_confidence: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary for serialization"""
        return {
            'event_id': str(self.event_id),
            'event_type': self.event_type.value,
            'aggregate_id': str(self.aggregate_id),
            'timestamp': self.timestamp.isoformat(),
            'version': self.version,
            'metadata': self.metadata,
            'data': self._get_event_data()
        }
    
    def _get_event_data(self) -> Dict[str, Any]:
        return {
            'previous_instance_count': self.previous_instance_count,
            'new_instance_count': self.new_instance_count,
            'scaling_reason': self.scaling_reason,
            'ai_prediction_confidence': self.ai_prediction_confidence
        }
    
    def _get_event_data(self) -> Dict[str, Any]:
        return {
            'previous_instance_count': self.previous_instance_count,
            'new_instance_count': self.new_instance_count,
            'scaling_reason': self.scaling_reason,
            'ai_prediction_confidence': self.ai_prediction_confidence
        }


class Application:
    """
    Application aggregate root representing a deployed application in the PaaS platform.
    
    This is the main entity that encapsulates all application-related business logic
    and maintains consistency across related operations. It follows the aggregate
    pattern from Domain-Driven Design.
    """
    
    def __init__(self, 
                 application_id: ApplicationId,
                 name: str,
                 user_id: UserId,
                 resource_requirements: ResourceRequirements,
                 scaling_config: ScalingConfiguration):
        """
        Initialize a new application aggregate.
        
        Args:
            application_id: Unique identifier for the application
            name: Human-readable name for the application
            user_id: ID of the user who owns the application
            resource_requirements: Resource requirements for the application
            scaling_config: Scaling configuration for the application
        """
        # Validate input parameters
        if not name or not isinstance(name, str):
            raise ValueError("Application name must be a non-empty string")
        
        # Initialize aggregate state
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
        
        # Domain events that have occurred but not yet been published
        self._uncommitted_events: List[DomainEvent] = []
        
        # Raise domain event for application creation
        self._raise_event(ApplicationCreatedEvent(
            aggregate_id=self._id.value,
            application_name=self._name,
            user_id=self._user_id,
            resource_requirements=self._resource_requirements
        ))
    
    @property
    def id(self) -> ApplicationId:
        """Get the application ID"""
        return self._id
    
    @property
    def name(self) -> str:
        """Get the application name"""
        return self._name
    
    @property
    def user_id(self) -> UserId:
        """Get the user ID who owns this application"""
        return self._user_id
    
    @property
    def status(self) -> ApplicationStatus:
        """Get the current application status"""
        return self._status
    
    @property
    def resource_requirements(self) -> ResourceRequirements:
        """Get the resource requirements for this application"""
        return self._resource_requirements
    
    @property
    def scaling_config(self) -> ScalingConfiguration:
        """Get the scaling configuration for this application"""
        return self._scaling_config
    
    @property
    def current_instance_count(self) -> int:
        """Get the current number of running instances"""
        return self._current_instance_count
    
    @property
    def created_at(self) -> datetime:
        """Get the creation timestamp"""
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        """Get the last update timestamp"""
        return self._updated_at
    
    @property
    def version(self) -> int:
        """Get the current version of the aggregate"""
        return self._version
    
    def get_uncommitted_events(self) -> List[DomainEvent]:
        """Get the list of uncommitted domain events"""
        return self._uncommitted_events.copy()
    
    def mark_events_as_committed(self) -> None:
        """Mark all uncommitted events as committed (called after persistence)"""
        self._uncommitted_events.clear()
    
    def deploy(self) -> None:
        """
        Deploy the application to the runtime environment.
        
        This method transitions the application from PENDING to DEPLOYING status
        and raises appropriate domain events.
        """
        if self._status != ApplicationStatus.PENDING:
            raise ValueError(f"Cannot deploy application in {self._status.value} status")
        
        self._status = ApplicationStatus.DEPLOYING
        self._updated_at = datetime.utcnow()
        self._version += 1
        
        # Raise deployment started event
        self._raise_event(DomainEvent(
            aggregate_id=self._id.value,
            event_type=EventType.DEPLOYMENT_STARTED,
            metadata={'previous_status': ApplicationStatus.PENDING.value}
        ))
    
    def mark_as_running(self) -> None:
        """
        Mark the application as successfully running.
        
        This method is called when the deployment process completes successfully.
        """
        if self._status != ApplicationStatus.DEPLOYING:
            raise ValueError(f"Cannot mark application as running from {self._status.value} status")
        
        self._status = ApplicationStatus.RUNNING
        self._updated_at = datetime.utcnow()
        self._version += 1
        
        # Raise deployment completed event
        self._raise_event(DomainEvent(
            aggregate_id=self._id.value,
            event_type=EventType.DEPLOYMENT_COMPLETED,
            metadata={'instance_count': self._current_instance_count}
        ))
    
    def scale(self, new_instance_count: int, reason: str, ai_confidence: Optional[float] = None) -> None:
        """
        Scale the application to a new instance count.
        
        Args:
            new_instance_count: The target number of instances
            reason: Human-readable reason for the scaling operation
            ai_confidence: Confidence score from AI prediction (if applicable)
        """
        # Validate scaling parameters
        if new_instance_count < self._scaling_config.min_instances:
            raise ValueError(f"Cannot scale below minimum instances ({self._scaling_config.min_instances})")
        if new_instance_count > self._scaling_config.max_instances:
            raise ValueError(f"Cannot scale above maximum instances ({self._scaling_config.max_instances})")
        
        if new_instance_count == self._current_instance_count:
            return  # No scaling needed
        
        # Store previous state for event
        previous_count = self._current_instance_count
        
        # Update application state
        self._current_instance_count = new_instance_count
        self._status = ApplicationStatus.SCALING
        self._updated_at = datetime.utcnow()
        self._version += 1
        
        # Raise scaling event
        self._raise_event(ApplicationScaledEvent(
            aggregate_id=self._id.value,
            previous_instance_count=previous_count,
            new_instance_count=new_instance_count,
            scaling_reason=reason,
            ai_prediction_confidence=ai_confidence
        ))
    
    def update_resource_requirements(self, new_requirements: ResourceRequirements) -> None:
        """
        Update the resource requirements for the application.
        
        Args:
            new_requirements: New resource requirements
        """
        if self._status not in [ApplicationStatus.RUNNING, ApplicationStatus.STOPPED]:
            raise ValueError(f"Cannot update resources while application is {self._status.value}")
        
        self._resource_requirements = new_requirements
        self._updated_at = datetime.utcnow()
        self._version += 1
        
        # Raise update event
        self._raise_event(DomainEvent(
            aggregate_id=self._id.value,
            event_type=EventType.APPLICATION_UPDATED,
            metadata={'update_type': 'resource_requirements'}
        ))
    
    def update_scaling_config(self, new_config: ScalingConfiguration) -> None:
        """
        Update the scaling configuration for the application.
        
        Args:
            new_config: New scaling configuration
        """
        # Validate that current instance count is within new limits
        if self._current_instance_count < new_config.min_instances:
            raise ValueError("Current instance count is below new minimum")
        if self._current_instance_count > new_config.max_instances:
            raise ValueError("Current instance count is above new maximum")
        
        self._scaling_config = new_config
        self._updated_at = datetime.utcnow()
        self._version += 1
        
        # Raise update event
        self._raise_event(DomainEvent(
            aggregate_id=self._id.value,
            event_type=EventType.APPLICATION_UPDATED,
            metadata={'update_type': 'scaling_configuration'}
        ))
    
    def stop(self) -> None:
        """Stop the application gracefully"""
        if self._status not in [ApplicationStatus.RUNNING, ApplicationStatus.SCALING]:
            raise ValueError(f"Cannot stop application in {self._status.value} status")
        
        self._status = ApplicationStatus.STOPPING
        self._updated_at = datetime.utcnow()
        self._version += 1
        
        # Raise stopping event
        self._raise_event(DomainEvent(
            aggregate_id=self._id.value,
            event_type=EventType.APPLICATION_UPDATED,
            metadata={'action': 'stop'}
        ))
    
    def mark_as_stopped(self) -> None:
        """Mark the application as stopped"""
        if self._status != ApplicationStatus.STOPPING:
            raise ValueError(f"Cannot mark as stopped from {self._status.value} status")
        
        self._status = ApplicationStatus.STOPPED
        self._current_instance_count = 0
        self._updated_at = datetime.utcnow()
        self._version += 1
    
    def mark_as_failed(self, error_details: str) -> None:
        """Mark the application as failed with error details"""
        self._status = ApplicationStatus.FAILED
        self._updated_at = datetime.utcnow()
        self._version += 1
        
        # Raise error event
        self._raise_event(DomainEvent(
            aggregate_id=self._id.value,
            event_type=EventType.ERROR_OCCURRED,
            metadata={'error_details': error_details, 'previous_status': self._status.value}
        ))
    
    def _raise_event(self, event: DomainEvent) -> None:
        """Add a domain event to the uncommitted events list"""
        self._uncommitted_events.append(event)
    
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
                'target_memory_utilization': self._scaling_config.target_memory_utilization,
                'scale_up_cooldown_seconds': self._scaling_config.scale_up_cooldown_seconds,
                'scale_down_cooldown_seconds': self._scaling_config.scale_down_cooldown_seconds,
                'custom_metrics': self._scaling_config.custom_metrics
            },
            'created_at': self._created_at.isoformat(),
            'updated_at': self._updated_at.isoformat(),
            'version': self._version
        }


@dataclass(frozen=True)
class PluginId:
    """Value object representing a unique plugin identifier"""
    value: str
    
    def __post_init__(self):
        if not self.value or not isinstance(self.value, str):
            raise ValueError("PluginId must be a non-empty string")


@dataclass(frozen=True)
class PluginVersion:
    """Value object representing a plugin version using semantic versioning"""
    major: int
    minor: int
    patch: int
    
    def __post_init__(self):
        if self.major < 0 or self.minor < 0 or self.patch < 0:
            raise ValueError("Version numbers must be non-negative")
    
    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
    
    @classmethod
    def from_string(cls, version_string: str) -> 'PluginVersion':
        """Parse a version string into a PluginVersion object"""
        try:
            parts = version_string.split('.')
            if len(parts) != 3:
                raise ValueError("Version must have exactly 3 parts")
            return cls(int(parts[0]), int(parts[1]), int(parts[2]))
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid version string: {version_string}") from e
    
    def is_compatible_with(self, other: 'PluginVersion') -> bool:
        """Check if this version is compatible with another version"""
        # Simple compatibility: same major version
        return self.major == other.major


class PluginStatus(Enum):
    """Enumeration of possible plugin states"""
    PENDING = "pending"           # Plugin installation initiated
    INSTALLING = "installing"     # Plugin is being installed
    ACTIVE = "active"            # Plugin is active and running
    INACTIVE = "inactive"        # Plugin is installed but not active
    UPDATING = "updating"        # Plugin is being updated
    UNINSTALLING = "uninstalling"  # Plugin is being removed
    FAILED = "failed"            # Plugin installation or operation failed


@dataclass
class Plugin:
    """
    Plugin entity representing an installed plugin in the platform.
    
    Plugins extend the platform functionality and are managed through
    a secure lifecycle with proper validation and sandboxing.
    """
    
    def __init__(self,
                 plugin_id: PluginId,
                 name: str,
                 version: PluginVersion,
                 description: str,
                 author: str,
                 application_id: ApplicationId):
        """
        Initialize a new plugin entity.
        
        Args:
            plugin_id: Unique identifier for the plugin
            name: Human-readable name of the plugin
            version: Version of the plugin
            description: Description of plugin functionality
            author: Author or organization that created the plugin
            application_id: ID of the application this plugin is associated with
        """
        if not name or not isinstance(name, str):
            raise ValueError("Plugin name must be a non-empty string")
        if not description or not isinstance(description, str):
            raise ValueError("Plugin description must be a non-empty string")
        if not author or not isinstance(author, str):
            raise ValueError("Plugin author must be a non-empty string")
        
        self._id = plugin_id
        self._name = name
        self._version = version
        self._description = description
        self._author = author
        self._application_id = application_id
        self._status = PluginStatus.PENDING
        self._installed_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()
        self._configuration: Dict[str, Any] = {}
        self._resource_usage: Dict[str, float] = {}
        
        # Domain events for plugin lifecycle
        self._uncommitted_events: List[DomainEvent] = []
        
        # Raise plugin installation event
        self._raise_event(DomainEvent(
            aggregate_id=self._application_id.value,
            event_type=EventType.PLUGIN_INSTALLED,
            metadata={
                'plugin_id': self._id.value,
                'plugin_name': self._name,
                'plugin_version': str(self._version),
                'plugin_author': self._author
            }
        ))
    
    @property
    def id(self) -> PluginId:
        """Get the plugin ID"""
        return self._id
    
    @property
    def name(self) -> str:
        """Get the plugin name"""
        return self._name
    
    @property
    def version(self) -> PluginVersion:
        """Get the plugin version"""
        return self._version
    
    @property
    def status(self) -> PluginStatus:
        """Get the current plugin status"""
        return self._status
    
    @property
    def application_id(self) -> ApplicationId:
        """Get the associated application ID"""
        return self._application_id
    
    @property
    def configuration(self) -> Dict[str, Any]:
        """Get the plugin configuration"""
        return self._configuration.copy()
    
    @property
    def resource_usage(self) -> Dict[str, float]:
        """Get the current resource usage metrics"""
        return self._resource_usage.copy()
    
    def activate(self) -> None:
        """Activate the plugin"""
        if self._status != PluginStatus.INACTIVE:
            raise ValueError(f"Cannot activate plugin in {self._status.value} status")
        
        self._status = PluginStatus.ACTIVE
        self._updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate the plugin"""
        if self._status != PluginStatus.ACTIVE:
            raise ValueError(f"Cannot deactivate plugin in {self._status.value} status")
        
        self._status = PluginStatus.INACTIVE
        self._updated_at = datetime.utcnow()
    
    def update_configuration(self, new_config: Dict[str, Any]) -> None:
        """Update the plugin configuration"""
        self._configuration = new_config.copy()
        self._updated_at = datetime.utcnow()
    
    def update_resource_usage(self, usage_metrics: Dict[str, float]) -> None:
        """Update the resource usage metrics"""
        self._resource_usage = usage_metrics.copy()
        self._updated_at = datetime.utcnow()
    
    def get_uncommitted_events(self) -> List[DomainEvent]:
        """Get the list of uncommitted domain events"""
        return self._uncommitted_events.copy()
    
    def mark_events_as_committed(self) -> None:
        """Mark all uncommitted events as committed"""
        self._uncommitted_events.clear()
    
    def _raise_event(self, event: DomainEvent) -> None:
        """Add a domain event to the uncommitted events list"""
        self._uncommitted_events.append(event)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the plugin to a dictionary representation"""
        return {
            'id': self._id.value,
            'name': self._name,
            'version': str(self._version),
            'description': self._description,
            'author': self._author,
            'application_id': str(self._application_id.value),
            'status': self._status.value,
            'configuration': self._configuration,
            'resource_usage': self._resource_usage,
            'installed_at': self._installed_at.isoformat(),
            'updated_at': self._updated_at.isoformat()
        }

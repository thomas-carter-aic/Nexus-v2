"""
Application Services for AI-Native PaaS Platform

This module contains the application services that orchestrate business operations
and coordinate between domain models and infrastructure services. These services
implement the use cases of the system and maintain the application's business logic.

Architecture Pattern: Clean Architecture Application Layer
- Use Cases: High-level business operations
- Application Services: Coordinate domain objects and infrastructure
- Command/Query Handlers: Handle specific operations
- Event Handlers: React to domain events
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from ..domain.models import (
    Application, ApplicationId, ApplicationStatus, UserId,
    ResourceRequirements, ScalingConfiguration, ScalingStrategy,
    Plugin, PluginId, PluginVersion, PluginStatus,
    DomainEvent, EventType
)


# Configure logging for application services
logger = logging.getLogger(__name__)


class ApplicationRepository(ABC):
    """
    Abstract repository interface for Application aggregate persistence.
    
    This interface defines the contract for persisting and retrieving
    Application aggregates, following the Repository pattern from DDD.
    """
    
    @abstractmethod
    async def save(self, application: Application) -> None:
        """
        Save an application aggregate to persistent storage.
        
        Args:
            application: The application aggregate to save
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, application_id: ApplicationId) -> Optional[Application]:
        """
        Retrieve an application by its unique identifier.
        
        Args:
            application_id: The unique identifier of the application
            
        Returns:
            The application aggregate if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: UserId) -> List[Application]:
        """
        Retrieve all applications owned by a specific user.
        
        Args:
            user_id: The user identifier
            
        Returns:
            List of applications owned by the user
        """
        pass
    
    @abstractmethod
    async def delete(self, application_id: ApplicationId) -> bool:
        """
        Delete an application from persistent storage.
        
        Args:
            application_id: The unique identifier of the application to delete
            
        Returns:
            True if the application was deleted, False if not found
        """
        pass


class EventStore(ABC):
    """
    Abstract interface for event store operations.
    
    The event store is responsible for persisting domain events
    and providing event streams for event sourcing and CQRS patterns.
    """
    
    @abstractmethod
    async def append_events(self, aggregate_id: str, events: List[DomainEvent], expected_version: int) -> None:
        """
        Append events to the event stream for an aggregate.
        
        Args:
            aggregate_id: The unique identifier of the aggregate
            events: List of domain events to append
            expected_version: Expected version for optimistic concurrency control
        """
        pass
    
    @abstractmethod
    async def get_events(self, aggregate_id: str, from_version: int = 0) -> List[DomainEvent]:
        """
        Retrieve events for an aggregate from a specific version.
        
        Args:
            aggregate_id: The unique identifier of the aggregate
            from_version: Starting version number (inclusive)
            
        Returns:
            List of domain events for the aggregate
        """
        pass
    
    @abstractmethod
    async def get_all_events(self, event_types: Optional[List[EventType]] = None) -> List[DomainEvent]:
        """
        Retrieve all events, optionally filtered by event types.
        
        Args:
            event_types: Optional list of event types to filter by
            
        Returns:
            List of domain events matching the criteria
        """
        pass


class AIScalingService(ABC):
    """
    Abstract interface for AI-powered scaling decisions.
    
    This service uses machine learning models to make intelligent
    scaling decisions based on historical patterns and current metrics.
    """
    
    @abstractmethod
    async def predict_scaling_need(self, application: Application, current_metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Predict if scaling is needed based on current metrics and historical patterns.
        
        Args:
            application: The application to analyze
            current_metrics: Current performance metrics
            
        Returns:
            Dictionary containing scaling prediction with confidence score
        """
        pass
    
    @abstractmethod
    async def optimize_resource_allocation(self, application: Application) -> ResourceRequirements:
        """
        Optimize resource allocation based on usage patterns.
        
        Args:
            application: The application to optimize
            
        Returns:
            Optimized resource requirements
        """
        pass


class ApplicationService:
    """
    Application service for managing application lifecycle operations.
    
    This service coordinates between domain models, repositories, and
    infrastructure services to implement application management use cases.
    """
    
    def __init__(self, 
                 application_repository: ApplicationRepository,
                 event_store: EventStore,
                 ai_scaling_service: AIScalingService):
        """
        Initialize the application service with required dependencies.
        
        Args:
            application_repository: Repository for application persistence
            event_store: Event store for domain events
            ai_scaling_service: AI service for scaling decisions
        """
        self._application_repository = application_repository
        self._event_store = event_store
        self._ai_scaling_service = ai_scaling_service
    
    async def create_application(self,
                               name: str,
                               user_id: UserId,
                               resource_requirements: ResourceRequirements,
                               scaling_config: Optional[ScalingConfiguration] = None) -> ApplicationId:
        """
        Create a new application with the specified configuration.
        
        Args:
            name: Human-readable name for the application
            user_id: ID of the user creating the application
            resource_requirements: Resource requirements for the application
            scaling_config: Optional scaling configuration (defaults will be used if not provided)
            
        Returns:
            The unique identifier of the created application
        """
        logger.info(f"Creating new application '{name}' for user {user_id.value}")
        
        # Generate unique application ID
        application_id = ApplicationId.generate()
        
        # Use default scaling configuration if not provided
        if scaling_config is None:
            scaling_config = ScalingConfiguration(
                strategy=ScalingStrategy.PREDICTIVE,  # Default to AI-driven scaling
                min_instances=1,
                max_instances=10,
                target_cpu_utilization=70.0,
                target_memory_utilization=80.0
            )
        
        # Create application aggregate
        application = Application(
            application_id=application_id,
            name=name,
            user_id=user_id,
            resource_requirements=resource_requirements,
            scaling_config=scaling_config
        )
        
        # Persist application and events
        await self._save_application_with_events(application)
        
        logger.info(f"Successfully created application {application_id.value}")
        return application_id
    
    async def deploy_application(self, application_id: ApplicationId) -> None:
        """
        Deploy an application to the runtime environment.
        
        Args:
            application_id: The unique identifier of the application to deploy
        """
        logger.info(f"Deploying application {application_id.value}")
        
        # Retrieve application from repository
        application = await self._application_repository.get_by_id(application_id)
        if not application:
            raise ValueError(f"Application {application_id.value} not found")
        
        # Initiate deployment process
        application.deploy()
        
        # Persist updated application and events
        await self._save_application_with_events(application)
        
        logger.info(f"Application {application_id.value} deployment initiated")
    
    async def scale_application(self, 
                              application_id: ApplicationId,
                              target_instances: Optional[int] = None,
                              force_scaling: bool = False) -> None:
        """
        Scale an application using AI-driven or manual scaling decisions.
        
        Args:
            application_id: The unique identifier of the application to scale
            target_instances: Optional target instance count for manual scaling
            force_scaling: Whether to force scaling even if AI doesn't recommend it
        """
        logger.info(f"Scaling application {application_id.value}")
        
        # Retrieve application from repository
        application = await self._application_repository.get_by_id(application_id)
        if not application:
            raise ValueError(f"Application {application_id.value} not found")
        
        if application.status != ApplicationStatus.RUNNING:
            raise ValueError(f"Cannot scale application in {application.status.value} status")
        
        # Determine scaling decision
        if target_instances is not None:
            # Manual scaling
            scaling_reason = f"Manual scaling to {target_instances} instances"
            ai_confidence = None
            new_instance_count = target_instances
        else:
            # AI-driven scaling
            current_metrics = await self._get_current_metrics(application_id)
            scaling_prediction = await self._ai_scaling_service.predict_scaling_need(
                application, current_metrics
            )
            
            if not scaling_prediction.get('should_scale', False) and not force_scaling:
                logger.info(f"AI recommends no scaling for application {application_id.value}")
                return
            
            new_instance_count = scaling_prediction.get('recommended_instances', application.current_instance_count)
            scaling_reason = scaling_prediction.get('reason', 'AI-driven scaling')
            ai_confidence = scaling_prediction.get('confidence', 0.0)
        
        # Perform scaling operation
        application.scale(
            new_instance_count=new_instance_count,
            reason=scaling_reason,
            ai_confidence=ai_confidence
        )
        
        # Persist updated application and events
        await self._save_application_with_events(application)
        
        logger.info(f"Application {application_id.value} scaled to {new_instance_count} instances")
    
    async def update_application_resources(self,
                                         application_id: ApplicationId,
                                         new_requirements: ResourceRequirements) -> None:
        """
        Update the resource requirements for an application.
        
        Args:
            application_id: The unique identifier of the application
            new_requirements: New resource requirements
        """
        logger.info(f"Updating resources for application {application_id.value}")
        
        # Retrieve application from repository
        application = await self._application_repository.get_by_id(application_id)
        if not application:
            raise ValueError(f"Application {application_id.value} not found")
        
        # Update resource requirements
        application.update_resource_requirements(new_requirements)
        
        # Persist updated application and events
        await self._save_application_with_events(application)
        
        logger.info(f"Resources updated for application {application_id.value}")
    
    async def stop_application(self, application_id: ApplicationId) -> None:
        """
        Stop a running application gracefully.
        
        Args:
            application_id: The unique identifier of the application to stop
        """
        logger.info(f"Stopping application {application_id.value}")
        
        # Retrieve application from repository
        application = await self._application_repository.get_by_id(application_id)
        if not application:
            raise ValueError(f"Application {application_id.value} not found")
        
        # Stop the application
        application.stop()
        
        # Persist updated application and events
        await self._save_application_with_events(application)
        
        logger.info(f"Application {application_id.value} stop initiated")
    
    async def get_application(self, application_id: ApplicationId) -> Optional[Application]:
        """
        Retrieve an application by its unique identifier.
        
        Args:
            application_id: The unique identifier of the application
            
        Returns:
            The application if found, None otherwise
        """
        return await self._application_repository.get_by_id(application_id)
    
    async def get_user_applications(self, user_id: UserId) -> List[Application]:
        """
        Retrieve all applications owned by a specific user.
        
        Args:
            user_id: The user identifier
            
        Returns:
            List of applications owned by the user
        """
        return await self._application_repository.get_by_user_id(user_id)
    
    async def delete_application(self, application_id: ApplicationId) -> bool:
        """
        Delete an application and all associated resources.
        
        Args:
            application_id: The unique identifier of the application to delete
            
        Returns:
            True if the application was deleted, False if not found
        """
        logger.info(f"Deleting application {application_id.value}")
        
        # Retrieve application to ensure it exists and can be deleted
        application = await self._application_repository.get_by_id(application_id)
        if not application:
            return False
        
        if application.status not in [ApplicationStatus.STOPPED, ApplicationStatus.FAILED]:
            raise ValueError(f"Cannot delete application in {application.status.value} status")
        
        # Delete from repository
        deleted = await self._application_repository.delete(application_id)
        
        if deleted:
            logger.info(f"Application {application_id.value} deleted successfully")
        
        return deleted
    
    async def _save_application_with_events(self, application: Application) -> None:
        """
        Save application and publish its uncommitted events.
        
        Args:
            application: The application aggregate to save
        """
        # Get uncommitted events before saving
        events = application.get_uncommitted_events()
        
        # Save application to repository
        await self._application_repository.save(application)
        
        # Append events to event store
        if events:
            await self._event_store.append_events(
                aggregate_id=str(application.id.value),
                events=events,
                expected_version=application.version - len(events)
            )
        
        # Mark events as committed
        application.mark_events_as_committed()
    
    async def _get_current_metrics(self, application_id: ApplicationId) -> Dict[str, float]:
        """
        Get current performance metrics for an application.
        
        This is a placeholder method that would integrate with monitoring services
        to retrieve real-time metrics like CPU usage, memory usage, request rate, etc.
        
        Args:
            application_id: The unique identifier of the application
            
        Returns:
            Dictionary of current performance metrics
        """
        # TODO: Integrate with actual monitoring service (CloudWatch, etc.)
        # For now, return mock metrics
        return {
            'cpu_utilization': 65.0,
            'memory_utilization': 70.0,
            'request_rate': 150.0,
            'response_time': 200.0,
            'error_rate': 0.5
        }


class PluginRepository(ABC):
    """
    Abstract repository interface for Plugin entity persistence.
    """
    
    @abstractmethod
    async def save(self, plugin: Plugin) -> None:
        """Save a plugin to persistent storage"""
        pass
    
    @abstractmethod
    async def get_by_id(self, plugin_id: PluginId) -> Optional[Plugin]:
        """Retrieve a plugin by its unique identifier"""
        pass
    
    @abstractmethod
    async def get_by_application_id(self, application_id: ApplicationId) -> List[Plugin]:
        """Retrieve all plugins for a specific application"""
        pass
    
    @abstractmethod
    async def delete(self, plugin_id: PluginId) -> bool:
        """Delete a plugin from persistent storage"""
        pass


class PluginService:
    """
    Application service for managing plugin lifecycle operations.
    
    This service handles plugin installation, configuration, activation,
    and removal with proper security validation and resource management.
    """
    
    def __init__(self,
                 plugin_repository: PluginRepository,
                 event_store: EventStore):
        """
        Initialize the plugin service with required dependencies.
        
        Args:
            plugin_repository: Repository for plugin persistence
            event_store: Event store for domain events
        """
        self._plugin_repository = plugin_repository
        self._event_store = event_store
    
    async def install_plugin(self,
                           plugin_id: PluginId,
                           name: str,
                           version: PluginVersion,
                           description: str,
                           author: str,
                           application_id: ApplicationId) -> None:
        """
        Install a new plugin for an application.
        
        Args:
            plugin_id: Unique identifier for the plugin
            name: Human-readable name of the plugin
            version: Version of the plugin
            description: Description of plugin functionality
            author: Author or organization that created the plugin
            application_id: ID of the application to install the plugin for
        """
        logger.info(f"Installing plugin {plugin_id.value} for application {application_id.value}")
        
        # Check if plugin is already installed
        existing_plugin = await self._plugin_repository.get_by_id(plugin_id)
        if existing_plugin:
            raise ValueError(f"Plugin {plugin_id.value} is already installed")
        
        # Create plugin entity
        plugin = Plugin(
            plugin_id=plugin_id,
            name=name,
            version=version,
            description=description,
            author=author,
            application_id=application_id
        )
        
        # Save plugin and events
        await self._save_plugin_with_events(plugin)
        
        logger.info(f"Plugin {plugin_id.value} installed successfully")
    
    async def activate_plugin(self, plugin_id: PluginId) -> None:
        """
        Activate an installed plugin.
        
        Args:
            plugin_id: The unique identifier of the plugin to activate
        """
        logger.info(f"Activating plugin {plugin_id.value}")
        
        plugin = await self._plugin_repository.get_by_id(plugin_id)
        if not plugin:
            raise ValueError(f"Plugin {plugin_id.value} not found")
        
        plugin.activate()
        await self._save_plugin_with_events(plugin)
        
        logger.info(f"Plugin {plugin_id.value} activated successfully")
    
    async def deactivate_plugin(self, plugin_id: PluginId) -> None:
        """
        Deactivate an active plugin.
        
        Args:
            plugin_id: The unique identifier of the plugin to deactivate
        """
        logger.info(f"Deactivating plugin {plugin_id.value}")
        
        plugin = await self._plugin_repository.get_by_id(plugin_id)
        if not plugin:
            raise ValueError(f"Plugin {plugin_id.value} not found")
        
        plugin.deactivate()
        await self._save_plugin_with_events(plugin)
        
        logger.info(f"Plugin {plugin_id.value} deactivated successfully")
    
    async def configure_plugin(self, plugin_id: PluginId, configuration: Dict[str, Any]) -> None:
        """
        Update the configuration for a plugin.
        
        Args:
            plugin_id: The unique identifier of the plugin
            configuration: New configuration dictionary
        """
        logger.info(f"Configuring plugin {plugin_id.value}")
        
        plugin = await self._plugin_repository.get_by_id(plugin_id)
        if not plugin:
            raise ValueError(f"Plugin {plugin_id.value} not found")
        
        plugin.update_configuration(configuration)
        await self._save_plugin_with_events(plugin)
        
        logger.info(f"Plugin {plugin_id.value} configured successfully")
    
    async def get_application_plugins(self, application_id: ApplicationId) -> List[Plugin]:
        """
        Retrieve all plugins for a specific application.
        
        Args:
            application_id: The unique identifier of the application
            
        Returns:
            List of plugins installed for the application
        """
        return await self._plugin_repository.get_by_application_id(application_id)
    
    async def uninstall_plugin(self, plugin_id: PluginId) -> bool:
        """
        Uninstall a plugin and clean up its resources.
        
        Args:
            plugin_id: The unique identifier of the plugin to uninstall
            
        Returns:
            True if the plugin was uninstalled, False if not found
        """
        logger.info(f"Uninstalling plugin {plugin_id.value}")
        
        plugin = await self._plugin_repository.get_by_id(plugin_id)
        if not plugin:
            return False
        
        if plugin.status == PluginStatus.ACTIVE:
            plugin.deactivate()
            await self._save_plugin_with_events(plugin)
        
        deleted = await self._plugin_repository.delete(plugin_id)
        
        if deleted:
            logger.info(f"Plugin {plugin_id.value} uninstalled successfully")
        
        return deleted
    
    async def _save_plugin_with_events(self, plugin: Plugin) -> None:
        """
        Save plugin and publish its uncommitted events.
        
        Args:
            plugin: The plugin entity to save
        """
        # Get uncommitted events before saving
        events = plugin.get_uncommitted_events()
        
        # Save plugin to repository
        await self._plugin_repository.save(plugin)
        
        # Append events to event store
        if events:
            await self._event_store.append_events(
                aggregate_id=str(plugin.application_id.value),
                events=events,
                expected_version=0  # Plugin events are associated with application aggregate
            )
        
        # Mark events as committed
        plugin.mark_events_as_committed()

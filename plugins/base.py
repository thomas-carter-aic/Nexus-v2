"""
Base classes and interfaces for the plugin system.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from enum import Enum
import asyncio
from datetime import datetime


class PluginType(Enum):
    """Plugin types supported by the platform."""
    MONITORING = "monitoring"
    DEPLOYMENT = "deployment"
    SCALING = "scaling"
    SECURITY = "security"
    ANALYTICS = "analytics"
    INTEGRATION = "integration"
    AI_MODEL = "ai_model"


class PluginStatus(Enum):
    """Plugin execution status."""
    INACTIVE = "inactive"
    ACTIVE = "active"
    ERROR = "error"
    SUSPENDED = "suspended"


@dataclass
class PluginMetadata:
    """Plugin metadata and configuration."""
    name: str
    version: str
    description: str
    author: str
    plugin_type: PluginType
    dependencies: List[str]
    permissions: List[str]
    config_schema: Dict[str, Any]
    min_platform_version: str
    max_platform_version: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class PluginContext:
    """Context provided to plugins during execution."""
    application_id: str
    user_id: str
    environment: str
    platform_version: str
    metrics_api: Any
    storage_api: Any
    event_api: Any
    http_client: Any
    logger: Any
    config: Dict[str, Any]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == 'production'


class PluginBase(ABC):
    """Base class for all platform plugins."""
    
    def __init__(self, metadata: PluginMetadata):
        self.metadata = metadata
        self.status = PluginStatus.INACTIVE
        self.last_execution = None
        self.error_count = 0
        self.max_errors = 5
        
    @abstractmethod
    async def initialize(self, context: PluginContext) -> bool:
        """
        Initialize the plugin with the provided context.
        
        Args:
            context: Plugin execution context
            
        Returns:
            True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def execute(self, context: PluginContext, **kwargs) -> Dict[str, Any]:
        """
        Execute the plugin's main functionality.
        
        Args:
            context: Plugin execution context
            **kwargs: Additional execution parameters
            
        Returns:
            Dictionary containing execution results
        """
        pass
    
    @abstractmethod
    async def cleanup(self, context: PluginContext) -> None:
        """
        Cleanup resources when plugin is deactivated.
        
        Args:
            context: Plugin execution context
        """
        pass
    
    async def health_check(self, context: PluginContext) -> Dict[str, Any]:
        """
        Perform health check on the plugin.
        
        Args:
            context: Plugin execution context
            
        Returns:
            Health status information
        """
        return {
            "status": self.status.value,
            "last_execution": self.last_execution,
            "error_count": self.error_count,
            "healthy": self.error_count < self.max_errors
        }
    
    def validate_permissions(self, required_permissions: List[str]) -> bool:
        """
        Validate that plugin has required permissions.
        
        Args:
            required_permissions: List of required permissions
            
        Returns:
            True if all permissions are granted
        """
        return all(perm in self.metadata.permissions for perm in required_permissions)
    
    def increment_error_count(self):
        """Increment error count and suspend if threshold exceeded."""
        self.error_count += 1
        if self.error_count >= self.max_errors:
            self.status = PluginStatus.SUSPENDED
    
    def reset_error_count(self):
        """Reset error count after successful execution."""
        self.error_count = 0
        if self.status == PluginStatus.SUSPENDED:
            self.status = PluginStatus.ACTIVE


class MonitoringPlugin(PluginBase):
    """Base class for monitoring plugins."""
    
    @abstractmethod
    async def collect_metrics(self, context: PluginContext) -> Dict[str, Any]:
        """Collect custom metrics."""
        pass
    
    @abstractmethod
    async def generate_alerts(self, context: PluginContext, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate alerts based on metrics."""
        pass


class DeploymentPlugin(PluginBase):
    """Base class for deployment plugins."""
    
    @abstractmethod
    async def pre_deployment(self, context: PluginContext, deployment_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute before deployment."""
        pass
    
    @abstractmethod
    async def post_deployment(self, context: PluginContext, deployment_result: Dict[str, Any]) -> Dict[str, Any]:
        """Execute after deployment."""
        pass


class ScalingPlugin(PluginBase):
    """Base class for scaling plugins."""
    
    @abstractmethod
    async def calculate_scaling_decision(self, context: PluginContext, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate scaling decision based on metrics."""
        pass


class SecurityPlugin(PluginBase):
    """Base class for security plugins."""
    
    @abstractmethod
    async def scan_vulnerabilities(self, context: PluginContext, target: str) -> Dict[str, Any]:
        """Scan for security vulnerabilities."""
        pass
    
    @abstractmethod
    async def validate_compliance(self, context: PluginContext, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate compliance requirements."""
        pass


class AnalyticsPlugin(PluginBase):
    """Base class for analytics plugins."""
    
    @abstractmethod
    async def analyze_data(self, context: PluginContext, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze provided data."""
        pass
    
    @abstractmethod
    async def generate_insights(self, context: PluginContext, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights from analysis."""
        pass


class IntegrationPlugin(PluginBase):
    """Base class for integration plugins."""
    
    @abstractmethod
    async def sync_data(self, context: PluginContext, source: str, destination: str) -> Dict[str, Any]:
        """Synchronize data between systems."""
        pass


class AIModelPlugin(PluginBase):
    """Base class for AI model plugins."""
    
    @abstractmethod
    async def predict(self, context: PluginContext, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make predictions using the AI model."""
        pass
    
    @abstractmethod
    async def train(self, context: PluginContext, training_data: Dict[str, Any]) -> Dict[str, Any]:
        """Train the AI model with new data."""
        pass
    
    @abstractmethod
    async def evaluate(self, context: PluginContext, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate model performance."""
        pass

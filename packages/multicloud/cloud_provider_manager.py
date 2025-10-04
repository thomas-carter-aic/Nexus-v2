"""
Multi-Cloud Provider Manager

This module provides unified management and abstraction layer for multiple cloud providers
including AWS, Azure, Google Cloud Platform, and other cloud services.
"""

import asyncio
import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from uuid import UUID, uuid4
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class CloudProvider(Enum):
    """Supported cloud providers"""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ALIBABA_CLOUD = "alibaba_cloud"
    IBM_CLOUD = "ibm_cloud"
    ORACLE_CLOUD = "oracle_cloud"
    DIGITAL_OCEAN = "digital_ocean"
    LINODE = "linode"


class ServiceType(Enum):
    """Types of cloud services"""
    COMPUTE = "compute"
    STORAGE = "storage"
    DATABASE = "database"
    NETWORKING = "networking"
    SECURITY = "security"
    AI_ML = "ai_ml"
    ANALYTICS = "analytics"
    MONITORING = "monitoring"
    CONTAINER = "container"
    SERVERLESS = "serverless"


class ResourceStatus(Enum):
    """Status of cloud resources"""
    CREATING = "creating"
    RUNNING = "running"
    STOPPED = "stopped"
    DELETING = "deleting"
    ERROR = "error"
    UNKNOWN = "unknown"


@dataclass
class ProviderConfig:
    """Configuration for a cloud provider"""
    provider: CloudProvider
    region: str
    credentials: Dict[str, str]
    default_settings: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    priority: int = 1  # Lower number = higher priority
    cost_factor: float = 1.0  # Relative cost multiplier
    performance_factor: float = 1.0  # Relative performance multiplier
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'provider': self.provider.value,
            'region': self.region,
            'credentials': '***REDACTED***',  # Never expose credentials
            'default_settings': self.default_settings,
            'enabled': self.enabled,
            'priority': self.priority,
            'cost_factor': self.cost_factor,
            'performance_factor': self.performance_factor
        }


@dataclass
class CloudResource:
    """Represents a cloud resource across providers"""
    resource_id: str
    provider: CloudProvider
    service_type: ServiceType
    resource_type: str
    name: str
    region: str
    status: ResourceStatus
    configuration: Dict[str, Any] = field(default_factory=dict)
    tags: Dict[str, str] = field(default_factory=dict)
    cost_per_hour: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'resource_id': self.resource_id,
            'provider': self.provider.value,
            'service_type': self.service_type.value,
            'resource_type': self.resource_type,
            'name': self.name,
            'region': self.region,
            'status': self.status.value,
            'configuration': self.configuration,
            'tags': self.tags,
            'cost_per_hour': self.cost_per_hour,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class CloudProviderInterface(ABC):
    """Abstract interface for cloud provider implementations"""
    
    @abstractmethod
    async def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Authenticate with the cloud provider"""
        pass
    
    @abstractmethod
    async def create_resource(self, service_type: ServiceType, 
                            resource_type: str, config: Dict[str, Any]) -> CloudResource:
        """Create a new resource"""
        pass
    
    @abstractmethod
    async def get_resource(self, resource_id: str) -> Optional[CloudResource]:
        """Get resource by ID"""
        pass
    
    @abstractmethod
    async def list_resources(self, service_type: Optional[ServiceType] = None) -> List[CloudResource]:
        """List all resources"""
        pass
    
    @abstractmethod
    async def update_resource(self, resource_id: str, config: Dict[str, Any]) -> CloudResource:
        """Update resource configuration"""
        pass
    
    @abstractmethod
    async def delete_resource(self, resource_id: str) -> bool:
        """Delete a resource"""
        pass
    
    @abstractmethod
    async def get_pricing(self, service_type: ServiceType, 
                         resource_type: str, region: str) -> Dict[str, float]:
        """Get pricing information"""
        pass
    
    @abstractmethod
    async def get_regions(self) -> List[str]:
        """Get available regions"""
        pass


class AWSProvider(CloudProviderInterface):
    """AWS cloud provider implementation"""
    
    def __init__(self):
        self.authenticated = False
        self.session = None
        
    async def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Authenticate with AWS"""
        try:
            # In production, this would use boto3 session
            access_key = credentials.get('access_key_id')
            secret_key = credentials.get('secret_access_key')
            
            if not access_key or not secret_key:
                return False
                
            # Mock authentication for now
            self.authenticated = True
            logger.info("AWS authentication successful")
            return True
            
        except Exception as e:
            logger.error(f"AWS authentication failed: {e}")
            return False
            
    async def create_resource(self, service_type: ServiceType, 
                            resource_type: str, config: Dict[str, Any]) -> CloudResource:
        """Create AWS resource"""
        if not self.authenticated:
            raise ValueError("Not authenticated with AWS")
            
        # Mock resource creation
        resource_id = f"aws-{resource_type}-{str(uuid4())[:8]}"
        
        resource = CloudResource(
            resource_id=resource_id,
            provider=CloudProvider.AWS,
            service_type=service_type,
            resource_type=resource_type,
            name=config.get('name', resource_id),
            region=config.get('region', 'us-east-1'),
            status=ResourceStatus.CREATING,
            configuration=config,
            cost_per_hour=self._get_mock_cost(service_type, resource_type)
        )
        
        # Simulate creation time
        await asyncio.sleep(0.1)
        resource.status = ResourceStatus.RUNNING
        
        logger.info(f"Created AWS resource: {resource_id}")
        return resource
        
    async def get_resource(self, resource_id: str) -> Optional[CloudResource]:
        """Get AWS resource by ID"""
        # Mock implementation
        if resource_id.startswith('aws-'):
            return CloudResource(
                resource_id=resource_id,
                provider=CloudProvider.AWS,
                service_type=ServiceType.COMPUTE,
                resource_type="ec2_instance",
                name=f"instance-{resource_id[-8:]}",
                region="us-east-1",
                status=ResourceStatus.RUNNING
            )
        return None
        
    async def list_resources(self, service_type: Optional[ServiceType] = None) -> List[CloudResource]:
        """List AWS resources"""
        # Mock implementation
        resources = []
        for i in range(3):
            resource = CloudResource(
                resource_id=f"aws-instance-{i:03d}",
                provider=CloudProvider.AWS,
                service_type=ServiceType.COMPUTE,
                resource_type="ec2_instance",
                name=f"web-server-{i+1}",
                region="us-east-1",
                status=ResourceStatus.RUNNING,
                cost_per_hour=0.10
            )
            resources.append(resource)
            
        return resources
        
    async def update_resource(self, resource_id: str, config: Dict[str, Any]) -> CloudResource:
        """Update AWS resource"""
        resource = await self.get_resource(resource_id)
        if resource:
            resource.configuration.update(config)
            resource.updated_at = datetime.utcnow()
            return resource
        raise ValueError(f"Resource {resource_id} not found")
        
    async def delete_resource(self, resource_id: str) -> bool:
        """Delete AWS resource"""
        # Mock implementation
        logger.info(f"Deleted AWS resource: {resource_id}")
        return True
        
    async def get_pricing(self, service_type: ServiceType, 
                         resource_type: str, region: str) -> Dict[str, float]:
        """Get AWS pricing"""
        # Mock pricing data
        pricing = {
            'hourly_rate': self._get_mock_cost(service_type, resource_type),
            'monthly_rate': self._get_mock_cost(service_type, resource_type) * 24 * 30,
            'storage_gb_month': 0.023,
            'data_transfer_gb': 0.09
        }
        return pricing
        
    async def get_regions(self) -> List[str]:
        """Get AWS regions"""
        return [
            'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
            'eu-west-1', 'eu-west-2', 'eu-central-1',
            'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1'
        ]
        
    def _get_mock_cost(self, service_type: ServiceType, resource_type: str) -> float:
        """Get mock cost for resource type"""
        cost_map = {
            ServiceType.COMPUTE: 0.10,
            ServiceType.STORAGE: 0.023,
            ServiceType.DATABASE: 0.20,
            ServiceType.NETWORKING: 0.05,
            ServiceType.CONTAINER: 0.15
        }
        return cost_map.get(service_type, 0.10)


class AzureProvider(CloudProviderInterface):
    """Azure cloud provider implementation"""
    
    def __init__(self):
        self.authenticated = False
        
    async def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Authenticate with Azure"""
        try:
            tenant_id = credentials.get('tenant_id')
            client_id = credentials.get('client_id')
            client_secret = credentials.get('client_secret')
            
            if not all([tenant_id, client_id, client_secret]):
                return False
                
            # Mock authentication
            self.authenticated = True
            logger.info("Azure authentication successful")
            return True
            
        except Exception as e:
            logger.error(f"Azure authentication failed: {e}")
            return False
            
    async def create_resource(self, service_type: ServiceType, 
                            resource_type: str, config: Dict[str, Any]) -> CloudResource:
        """Create Azure resource"""
        if not self.authenticated:
            raise ValueError("Not authenticated with Azure")
            
        resource_id = f"azure-{resource_type}-{str(uuid4())[:8]}"
        
        resource = CloudResource(
            resource_id=resource_id,
            provider=CloudProvider.AZURE,
            service_type=service_type,
            resource_type=resource_type,
            name=config.get('name', resource_id),
            region=config.get('region', 'East US'),
            status=ResourceStatus.CREATING,
            configuration=config,
            cost_per_hour=self._get_mock_cost(service_type, resource_type)
        )
        
        await asyncio.sleep(0.1)
        resource.status = ResourceStatus.RUNNING
        
        logger.info(f"Created Azure resource: {resource_id}")
        return resource
        
    async def get_resource(self, resource_id: str) -> Optional[CloudResource]:
        """Get Azure resource by ID"""
        if resource_id.startswith('azure-'):
            return CloudResource(
                resource_id=resource_id,
                provider=CloudProvider.AZURE,
                service_type=ServiceType.COMPUTE,
                resource_type="virtual_machine",
                name=f"vm-{resource_id[-8:]}",
                region="East US",
                status=ResourceStatus.RUNNING
            )
        return None
        
    async def list_resources(self, service_type: Optional[ServiceType] = None) -> List[CloudResource]:
        """List Azure resources"""
        resources = []
        for i in range(2):
            resource = CloudResource(
                resource_id=f"azure-vm-{i:03d}",
                provider=CloudProvider.AZURE,
                service_type=ServiceType.COMPUTE,
                resource_type="virtual_machine",
                name=f"app-server-{i+1}",
                region="East US",
                status=ResourceStatus.RUNNING,
                cost_per_hour=0.12
            )
            resources.append(resource)
            
        return resources
        
    async def update_resource(self, resource_id: str, config: Dict[str, Any]) -> CloudResource:
        """Update Azure resource"""
        resource = await self.get_resource(resource_id)
        if resource:
            resource.configuration.update(config)
            resource.updated_at = datetime.utcnow()
            return resource
        raise ValueError(f"Resource {resource_id} not found")
        
    async def delete_resource(self, resource_id: str) -> bool:
        """Delete Azure resource"""
        logger.info(f"Deleted Azure resource: {resource_id}")
        return True
        
    async def get_pricing(self, service_type: ServiceType, 
                         resource_type: str, region: str) -> Dict[str, float]:
        """Get Azure pricing"""
        pricing = {
            'hourly_rate': self._get_mock_cost(service_type, resource_type),
            'monthly_rate': self._get_mock_cost(service_type, resource_type) * 24 * 30,
            'storage_gb_month': 0.025,
            'data_transfer_gb': 0.087
        }
        return pricing
        
    async def get_regions(self) -> List[str]:
        """Get Azure regions"""
        return [
            'East US', 'East US 2', 'West US', 'West US 2',
            'West Europe', 'North Europe', 'UK South',
            'Southeast Asia', 'East Asia', 'Japan East'
        ]
        
    def _get_mock_cost(self, service_type: ServiceType, resource_type: str) -> float:
        """Get mock cost for resource type"""
        cost_map = {
            ServiceType.COMPUTE: 0.12,
            ServiceType.STORAGE: 0.025,
            ServiceType.DATABASE: 0.22,
            ServiceType.NETWORKING: 0.06,
            ServiceType.CONTAINER: 0.16
        }
        return cost_map.get(service_type, 0.12)


class GCPProvider(CloudProviderInterface):
    """Google Cloud Platform provider implementation"""
    
    def __init__(self):
        self.authenticated = False
        
    async def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Authenticate with GCP"""
        try:
            project_id = credentials.get('project_id')
            service_account_key = credentials.get('service_account_key')
            
            if not project_id or not service_account_key:
                return False
                
            # Mock authentication
            self.authenticated = True
            logger.info("GCP authentication successful")
            return True
            
        except Exception as e:
            logger.error(f"GCP authentication failed: {e}")
            return False
            
    async def create_resource(self, service_type: ServiceType, 
                            resource_type: str, config: Dict[str, Any]) -> CloudResource:
        """Create GCP resource"""
        if not self.authenticated:
            raise ValueError("Not authenticated with GCP")
            
        resource_id = f"gcp-{resource_type}-{str(uuid4())[:8]}"
        
        resource = CloudResource(
            resource_id=resource_id,
            provider=CloudProvider.GCP,
            service_type=service_type,
            resource_type=resource_type,
            name=config.get('name', resource_id),
            region=config.get('region', 'us-central1'),
            status=ResourceStatus.CREATING,
            configuration=config,
            cost_per_hour=self._get_mock_cost(service_type, resource_type)
        )
        
        await asyncio.sleep(0.1)
        resource.status = ResourceStatus.RUNNING
        
        logger.info(f"Created GCP resource: {resource_id}")
        return resource
        
    async def get_resource(self, resource_id: str) -> Optional[CloudResource]:
        """Get GCP resource by ID"""
        if resource_id.startswith('gcp-'):
            return CloudResource(
                resource_id=resource_id,
                provider=CloudProvider.GCP,
                service_type=ServiceType.COMPUTE,
                resource_type="compute_instance",
                name=f"instance-{resource_id[-8:]}",
                region="us-central1",
                status=ResourceStatus.RUNNING
            )
        return None
        
    async def list_resources(self, service_type: Optional[ServiceType] = None) -> List[CloudResource]:
        """List GCP resources"""
        resources = []
        for i in range(2):
            resource = CloudResource(
                resource_id=f"gcp-instance-{i:03d}",
                provider=CloudProvider.GCP,
                service_type=ServiceType.COMPUTE,
                resource_type="compute_instance",
                name=f"worker-{i+1}",
                region="us-central1",
                status=ResourceStatus.RUNNING,
                cost_per_hour=0.095
            )
            resources.append(resource)
            
        return resources
        
    async def update_resource(self, resource_id: str, config: Dict[str, Any]) -> CloudResource:
        """Update GCP resource"""
        resource = await self.get_resource(resource_id)
        if resource:
            resource.configuration.update(config)
            resource.updated_at = datetime.utcnow()
            return resource
        raise ValueError(f"Resource {resource_id} not found")
        
    async def delete_resource(self, resource_id: str) -> bool:
        """Delete GCP resource"""
        logger.info(f"Deleted GCP resource: {resource_id}")
        return True
        
    async def get_pricing(self, service_type: ServiceType, 
                         resource_type: str, region: str) -> Dict[str, float]:
        """Get GCP pricing"""
        pricing = {
            'hourly_rate': self._get_mock_cost(service_type, resource_type),
            'monthly_rate': self._get_mock_cost(service_type, resource_type) * 24 * 30,
            'storage_gb_month': 0.020,
            'data_transfer_gb': 0.085
        }
        return pricing
        
    async def get_regions(self) -> List[str]:
        """Get GCP regions"""
        return [
            'us-central1', 'us-east1', 'us-west1', 'us-west2',
            'europe-west1', 'europe-west2', 'europe-west3',
            'asia-southeast1', 'asia-east1', 'asia-northeast1'
        ]
        
    def _get_mock_cost(self, service_type: ServiceType, resource_type: str) -> float:
        """Get mock cost for resource type"""
        cost_map = {
            ServiceType.COMPUTE: 0.095,
            ServiceType.STORAGE: 0.020,
            ServiceType.DATABASE: 0.18,
            ServiceType.NETWORKING: 0.045,
            ServiceType.CONTAINER: 0.14
        }
        return cost_map.get(service_type, 0.095)


class CloudProviderManager:
    """
    Unified manager for multiple cloud providers with intelligent orchestration
    """
    
    def __init__(self):
        self.providers: Dict[CloudProvider, CloudProviderInterface] = {}
        self.configurations: Dict[CloudProvider, ProviderConfig] = {}
        self.resources: Dict[str, CloudResource] = {}
        
        # Initialize provider implementations
        self.providers[CloudProvider.AWS] = AWSProvider()
        self.providers[CloudProvider.AZURE] = AzureProvider()
        self.providers[CloudProvider.GCP] = GCPProvider()
        
    async def add_provider(self, config: ProviderConfig) -> bool:
        """Add and configure a cloud provider"""
        try:
            provider_impl = self.providers.get(config.provider)
            if not provider_impl:
                raise ValueError(f"Unsupported provider: {config.provider}")
                
            # Authenticate with the provider
            authenticated = await provider_impl.authenticate(config.credentials)
            if not authenticated:
                raise ValueError(f"Authentication failed for {config.provider}")
                
            self.configurations[config.provider] = config
            logger.info(f"Added cloud provider: {config.provider.value}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add provider {config.provider}: {e}")
            return False
            
    async def remove_provider(self, provider: CloudProvider) -> bool:
        """Remove a cloud provider"""
        if provider in self.configurations:
            del self.configurations[provider]
            logger.info(f"Removed cloud provider: {provider.value}")
            return True
        return False
        
    async def create_resource(self, provider: CloudProvider, service_type: ServiceType,
                            resource_type: str, config: Dict[str, Any]) -> CloudResource:
        """Create a resource on a specific provider"""
        if provider not in self.configurations:
            raise ValueError(f"Provider {provider} not configured")
            
        provider_impl = self.providers[provider]
        resource = await provider_impl.create_resource(service_type, resource_type, config)
        
        # Store resource in local registry
        self.resources[resource.resource_id] = resource
        
        return resource
        
    async def get_resource(self, resource_id: str) -> Optional[CloudResource]:
        """Get a resource by ID from any provider"""
        # Check local registry first
        if resource_id in self.resources:
            return self.resources[resource_id]
            
        # Search across all providers
        for provider_impl in self.providers.values():
            resource = await provider_impl.get_resource(resource_id)
            if resource:
                self.resources[resource_id] = resource
                return resource
                
        return None
        
    async def list_all_resources(self, service_type: Optional[ServiceType] = None) -> List[CloudResource]:
        """List resources across all configured providers"""
        all_resources = []
        
        for provider, config in self.configurations.items():
            if not config.enabled:
                continue
                
            try:
                provider_impl = self.providers[provider]
                resources = await provider_impl.list_resources(service_type)
                all_resources.extend(resources)
                
                # Update local registry
                for resource in resources:
                    self.resources[resource.resource_id] = resource
                    
            except Exception as e:
                logger.error(f"Failed to list resources from {provider}: {e}")
                
        return all_resources
        
    async def get_optimal_provider(self, service_type: ServiceType, 
                                 region_preference: Optional[str] = None,
                                 cost_priority: float = 0.5,
                                 performance_priority: float = 0.5) -> Optional[CloudProvider]:
        """Get the optimal provider based on cost and performance factors"""
        
        best_provider = None
        best_score = -1
        
        for provider, config in self.configurations.items():
            if not config.enabled:
                continue
                
            try:
                # Calculate score based on cost and performance factors
                cost_score = 1.0 / config.cost_factor  # Lower cost = higher score
                performance_score = config.performance_factor
                
                # Weighted score
                total_score = (cost_score * cost_priority + 
                             performance_score * performance_priority)
                
                # Bonus for region preference
                if region_preference:
                    provider_impl = self.providers[provider]
                    regions = await provider_impl.get_regions()
                    if region_preference in regions:
                        total_score *= 1.2
                        
                if total_score > best_score:
                    best_score = total_score
                    best_provider = provider
                    
            except Exception as e:
                logger.error(f"Error evaluating provider {provider}: {e}")
                
        return best_provider
        
    async def get_cost_comparison(self, service_type: ServiceType, 
                                resource_type: str, region: str) -> Dict[CloudProvider, Dict[str, float]]:
        """Compare costs across all providers"""
        cost_comparison = {}
        
        for provider, config in self.configurations.items():
            if not config.enabled:
                continue
                
            try:
                provider_impl = self.providers[provider]
                pricing = await provider_impl.get_pricing(service_type, resource_type, region)
                cost_comparison[provider] = pricing
                
            except Exception as e:
                logger.error(f"Failed to get pricing from {provider}: {e}")
                
        return cost_comparison
        
    async def migrate_resource(self, resource_id: str, 
                             target_provider: CloudProvider) -> CloudResource:
        """Migrate a resource to a different provider"""
        # Get source resource
        source_resource = await self.get_resource(resource_id)
        if not source_resource:
            raise ValueError(f"Resource {resource_id} not found")
            
        if source_resource.provider == target_provider:
            return source_resource  # Already on target provider
            
        # Create equivalent resource on target provider
        target_resource = await self.create_resource(
            target_provider,
            source_resource.service_type,
            source_resource.resource_type,
            source_resource.configuration
        )
        
        # TODO: Implement data migration logic
        logger.info(f"Migrated resource {resource_id} from {source_resource.provider} to {target_provider}")
        
        return target_resource
        
    async def get_provider_status(self) -> Dict[CloudProvider, Dict[str, Any]]:
        """Get status of all configured providers"""
        status = {}
        
        for provider, config in self.configurations.items():
            try:
                provider_impl = self.providers[provider]
                regions = await provider_impl.get_regions()
                resources = await provider_impl.list_resources()
                
                status[provider] = {
                    'enabled': config.enabled,
                    'region': config.region,
                    'priority': config.priority,
                    'cost_factor': config.cost_factor,
                    'performance_factor': config.performance_factor,
                    'available_regions': len(regions),
                    'active_resources': len(resources),
                    'status': 'healthy'
                }
                
            except Exception as e:
                status[provider] = {
                    'enabled': config.enabled,
                    'status': 'error',
                    'error': str(e)
                }
                
        return status


# Example usage
async def example_multi_cloud_manager():
    """Example of using the multi-cloud manager"""
    
    # Create multi-cloud manager
    manager = CloudProviderManager()
    
    # Configure AWS
    aws_config = ProviderConfig(
        provider=CloudProvider.AWS,
        region='us-east-1',
        credentials={
            'access_key_id': 'AKIA...',
            'secret_access_key': 'secret...'
        },
        priority=1,
        cost_factor=1.0,
        performance_factor=1.0
    )
    
    # Configure Azure
    azure_config = ProviderConfig(
        provider=CloudProvider.AZURE,
        region='East US',
        credentials={
            'tenant_id': 'tenant-id',
            'client_id': 'client-id',
            'client_secret': 'client-secret'
        },
        priority=2,
        cost_factor=1.1,
        performance_factor=0.95
    )
    
    # Add providers
    await manager.add_provider(aws_config)
    await manager.add_provider(azure_config)
    
    # Get optimal provider for compute workload
    optimal_provider = await manager.get_optimal_provider(
        ServiceType.COMPUTE,
        cost_priority=0.7,
        performance_priority=0.3
    )
    print(f"Optimal provider for compute: {optimal_provider}")
    
    # Create resource on optimal provider
    if optimal_provider:
        resource = await manager.create_resource(
            optimal_provider,
            ServiceType.COMPUTE,
            "instance",
            {
                'name': 'web-server-1',
                'instance_type': 't3.medium',
                'region': 'us-east-1'
            }
        )
        print(f"Created resource: {resource.resource_id}")
        
    # List all resources across providers
    all_resources = await manager.list_all_resources()
    print(f"Total resources across all providers: {len(all_resources)}")
    
    # Get cost comparison
    cost_comparison = await manager.get_cost_comparison(
        ServiceType.COMPUTE, "instance", "us-east-1"
    )
    print("Cost comparison:")
    for provider, pricing in cost_comparison.items():
        print(f"  {provider.value}: ${pricing.get('hourly_rate', 0):.3f}/hour")
        
    # Get provider status
    status = await manager.get_provider_status()
    print("Provider status:")
    for provider, info in status.items():
        print(f"  {provider.value}: {info['status']}")


if __name__ == "__main__":
    asyncio.run(example_multi_cloud_manager())

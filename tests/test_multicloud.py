"""
Tests for Multi-Cloud Management Module

This module contains comprehensive tests for the multi-cloud management functionality
including provider management, resource operations, cost optimization, and migration.
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock

from src.multicloud import (
    CloudProvider,
    ServiceType,
    ResourceStatus,
    ProviderConfig,
    CloudResource,
    CloudProviderManager,
    AWSProvider,
    AzureProvider,
    GCPProvider
)


class TestProviderConfig:
    """Test ProviderConfig class"""
    
    def test_provider_config_creation(self):
        """Test creating a provider configuration"""
        config = ProviderConfig(
            provider=CloudProvider.AWS,
            region='us-east-1',
            credentials={'access_key_id': 'test', 'secret_access_key': 'test'},
            priority=1,
            cost_factor=1.0,
            performance_factor=1.0
        )
        
        assert config.provider == CloudProvider.AWS
        assert config.region == 'us-east-1'
        assert config.enabled is True
        assert config.priority == 1
        
    def test_provider_config_to_dict(self):
        """Test converting provider config to dictionary"""
        config = ProviderConfig(
            provider=CloudProvider.AZURE,
            region='East US',
            credentials={'tenant_id': 'test', 'client_id': 'test'},
            priority=2
        )
        
        config_dict = config.to_dict()
        assert config_dict['provider'] == 'azure'
        assert config_dict['region'] == 'East US'
        assert config_dict['credentials'] == '***REDACTED***'
        assert config_dict['priority'] == 2


class TestCloudResource:
    """Test CloudResource class"""
    
    def test_cloud_resource_creation(self):
        """Test creating a cloud resource"""
        resource = CloudResource(
            resource_id='test-resource-001',
            provider=CloudProvider.AWS,
            service_type=ServiceType.COMPUTE,
            resource_type='ec2_instance',
            name='web-server-1',
            region='us-east-1',
            status=ResourceStatus.RUNNING,
            cost_per_hour=0.10
        )
        
        assert resource.resource_id == 'test-resource-001'
        assert resource.provider == CloudProvider.AWS
        assert resource.service_type == ServiceType.COMPUTE
        assert resource.status == ResourceStatus.RUNNING
        assert resource.cost_per_hour == 0.10
        
    def test_cloud_resource_to_dict(self):
        """Test converting cloud resource to dictionary"""
        resource = CloudResource(
            resource_id='test-resource-002',
            provider=CloudProvider.GCP,
            service_type=ServiceType.DATABASE,
            resource_type='cloud_sql',
            name='app-database',
            region='us-central1',
            status=ResourceStatus.CREATING
        )
        
        resource_dict = resource.to_dict()
        assert resource_dict['resource_id'] == 'test-resource-002'
        assert resource_dict['provider'] == 'gcp'
        assert resource_dict['service_type'] == 'database'
        assert resource_dict['status'] == 'creating'


class TestAWSProvider:
    """Test AWS provider implementation"""
    
    @pytest.fixture
    def aws_provider(self):
        """Create AWS provider instance"""
        return AWSProvider()
        
    @pytest.mark.asyncio
    async def test_aws_authentication_success(self, aws_provider):
        """Test successful AWS authentication"""
        credentials = {
            'access_key_id': 'AKIAIOSFODNN7EXAMPLE',
            'secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
        }
        
        result = await aws_provider.authenticate(credentials)
        assert result is True
        assert aws_provider.authenticated is True
        
    @pytest.mark.asyncio
    async def test_aws_authentication_failure(self, aws_provider):
        """Test failed AWS authentication"""
        credentials = {'access_key_id': 'invalid'}
        
        result = await aws_provider.authenticate(credentials)
        assert result is False
        assert aws_provider.authenticated is False
        
    @pytest.mark.asyncio
    async def test_aws_create_resource(self, aws_provider):
        """Test creating AWS resource"""
        # Authenticate first
        await aws_provider.authenticate({
            'access_key_id': 'test',
            'secret_access_key': 'test'
        })
        
        config = {
            'name': 'test-instance',
            'instance_type': 't3.micro',
            'region': 'us-east-1'
        }
        
        resource = await aws_provider.create_resource(
            ServiceType.COMPUTE, 'ec2_instance', config
        )
        
        assert resource.provider == CloudProvider.AWS
        assert resource.service_type == ServiceType.COMPUTE
        assert resource.resource_type == 'ec2_instance'
        assert resource.status == ResourceStatus.RUNNING
        assert resource.resource_id.startswith('aws-ec2_instance-')
        
    @pytest.mark.asyncio
    async def test_aws_list_resources(self, aws_provider):
        """Test listing AWS resources"""
        await aws_provider.authenticate({
            'access_key_id': 'test',
            'secret_access_key': 'test'
        })
        
        resources = await aws_provider.list_resources()
        assert len(resources) == 3
        assert all(r.provider == CloudProvider.AWS for r in resources)
        
    @pytest.mark.asyncio
    async def test_aws_get_pricing(self, aws_provider):
        """Test getting AWS pricing"""
        await aws_provider.authenticate({
            'access_key_id': 'test',
            'secret_access_key': 'test'
        })
        
        pricing = await aws_provider.get_pricing(
            ServiceType.COMPUTE, 'ec2_instance', 'us-east-1'
        )
        
        assert 'hourly_rate' in pricing
        assert 'monthly_rate' in pricing
        assert pricing['hourly_rate'] > 0
        
    @pytest.mark.asyncio
    async def test_aws_get_regions(self, aws_provider):
        """Test getting AWS regions"""
        regions = await aws_provider.get_regions()
        assert len(regions) > 0
        assert 'us-east-1' in regions
        assert 'us-west-2' in regions


class TestAzureProvider:
    """Test Azure provider implementation"""
    
    @pytest.fixture
    def azure_provider(self):
        """Create Azure provider instance"""
        return AzureProvider()
        
    @pytest.mark.asyncio
    async def test_azure_authentication_success(self, azure_provider):
        """Test successful Azure authentication"""
        credentials = {
            'tenant_id': 'test-tenant',
            'client_id': 'test-client',
            'client_secret': 'test-secret'
        }
        
        result = await azure_provider.authenticate(credentials)
        assert result is True
        assert azure_provider.authenticated is True
        
    @pytest.mark.asyncio
    async def test_azure_create_resource(self, azure_provider):
        """Test creating Azure resource"""
        await azure_provider.authenticate({
            'tenant_id': 'test',
            'client_id': 'test',
            'client_secret': 'test'
        })
        
        config = {
            'name': 'test-vm',
            'vm_size': 'Standard_B1s',
            'region': 'East US'
        }
        
        resource = await azure_provider.create_resource(
            ServiceType.COMPUTE, 'virtual_machine', config
        )
        
        assert resource.provider == CloudProvider.AZURE
        assert resource.service_type == ServiceType.COMPUTE
        assert resource.resource_type == 'virtual_machine'
        assert resource.status == ResourceStatus.RUNNING
        
    @pytest.mark.asyncio
    async def test_azure_list_resources(self, azure_provider):
        """Test listing Azure resources"""
        await azure_provider.authenticate({
            'tenant_id': 'test',
            'client_id': 'test',
            'client_secret': 'test'
        })
        
        resources = await azure_provider.list_resources()
        assert len(resources) == 2
        assert all(r.provider == CloudProvider.AZURE for r in resources)


class TestGCPProvider:
    """Test GCP provider implementation"""
    
    @pytest.fixture
    def gcp_provider(self):
        """Create GCP provider instance"""
        return GCPProvider()
        
    @pytest.mark.asyncio
    async def test_gcp_authentication_success(self, gcp_provider):
        """Test successful GCP authentication"""
        credentials = {
            'project_id': 'test-project',
            'service_account_key': '{"type": "service_account"}'
        }
        
        result = await gcp_provider.authenticate(credentials)
        assert result is True
        assert gcp_provider.authenticated is True
        
    @pytest.mark.asyncio
    async def test_gcp_create_resource(self, gcp_provider):
        """Test creating GCP resource"""
        await gcp_provider.authenticate({
            'project_id': 'test',
            'service_account_key': 'test'
        })
        
        config = {
            'name': 'test-instance',
            'machine_type': 'e2-micro',
            'zone': 'us-central1-a'
        }
        
        resource = await gcp_provider.create_resource(
            ServiceType.COMPUTE, 'compute_instance', config
        )
        
        assert resource.provider == CloudProvider.GCP
        assert resource.service_type == ServiceType.COMPUTE
        assert resource.resource_type == 'compute_instance'
        assert resource.status == ResourceStatus.RUNNING


class TestCloudProviderManager:
    """Test CloudProviderManager class"""
    
    @pytest.fixture
    def manager(self):
        """Create CloudProviderManager instance"""
        return CloudProviderManager()
        
    @pytest.fixture
    def aws_config(self):
        """Create AWS configuration"""
        return ProviderConfig(
            provider=CloudProvider.AWS,
            region='us-east-1',
            credentials={'access_key_id': 'test', 'secret_access_key': 'test'},
            priority=1,
            cost_factor=1.0,
            performance_factor=1.0
        )
        
    @pytest.fixture
    def azure_config(self):
        """Create Azure configuration"""
        return ProviderConfig(
            provider=CloudProvider.AZURE,
            region='East US',
            credentials={'tenant_id': 'test', 'client_id': 'test', 'client_secret': 'test'},
            priority=2,
            cost_factor=1.1,
            performance_factor=0.95
        )
        
    @pytest.mark.asyncio
    async def test_add_provider_success(self, manager, aws_config):
        """Test successfully adding a provider"""
        result = await manager.add_provider(aws_config)
        assert result is True
        assert CloudProvider.AWS in manager.configurations
        
    @pytest.mark.asyncio
    async def test_add_provider_authentication_failure(self, manager):
        """Test adding provider with authentication failure"""
        config = ProviderConfig(
            provider=CloudProvider.AWS,
            region='us-east-1',
            credentials={'access_key_id': 'invalid'},  # Missing secret key
            priority=1
        )
        
        result = await manager.add_provider(config)
        assert result is False
        assert CloudProvider.AWS not in manager.configurations
        
    @pytest.mark.asyncio
    async def test_remove_provider(self, manager, aws_config):
        """Test removing a provider"""
        await manager.add_provider(aws_config)
        
        result = await manager.remove_provider(CloudProvider.AWS)
        assert result is True
        assert CloudProvider.AWS not in manager.configurations
        
    @pytest.mark.asyncio
    async def test_create_resource(self, manager, aws_config):
        """Test creating a resource through manager"""
        await manager.add_provider(aws_config)
        
        config = {
            'name': 'test-resource',
            'instance_type': 't3.micro'
        }
        
        resource = await manager.create_resource(
            CloudProvider.AWS,
            ServiceType.COMPUTE,
            'ec2_instance',
            config
        )
        
        assert resource.provider == CloudProvider.AWS
        assert resource.resource_id in manager.resources
        
    @pytest.mark.asyncio
    async def test_get_resource(self, manager, aws_config):
        """Test getting a resource by ID"""
        await manager.add_provider(aws_config)
        
        # Create a resource first
        config = {'name': 'test-resource'}
        created_resource = await manager.create_resource(
            CloudProvider.AWS,
            ServiceType.COMPUTE,
            'ec2_instance',
            config
        )
        
        # Get the resource
        retrieved_resource = await manager.get_resource(created_resource.resource_id)
        assert retrieved_resource is not None
        assert retrieved_resource.resource_id == created_resource.resource_id
        
    @pytest.mark.asyncio
    async def test_list_all_resources(self, manager, aws_config, azure_config):
        """Test listing resources across all providers"""
        await manager.add_provider(aws_config)
        await manager.add_provider(azure_config)
        
        resources = await manager.list_all_resources()
        
        # Should have resources from both AWS (3) and Azure (2)
        assert len(resources) == 5
        
        aws_resources = [r for r in resources if r.provider == CloudProvider.AWS]
        azure_resources = [r for r in resources if r.provider == CloudProvider.AZURE]
        
        assert len(aws_resources) == 3
        assert len(azure_resources) == 2
        
    @pytest.mark.asyncio
    async def test_get_optimal_provider_cost_priority(self, manager, aws_config, azure_config):
        """Test getting optimal provider with cost priority"""
        # AWS has lower cost factor (1.0 vs 1.1)
        await manager.add_provider(aws_config)
        await manager.add_provider(azure_config)
        
        optimal = await manager.get_optimal_provider(
            ServiceType.COMPUTE,
            cost_priority=1.0,
            performance_priority=0.0
        )
        
        assert optimal == CloudProvider.AWS
        
    @pytest.mark.asyncio
    async def test_get_optimal_provider_performance_priority(self, manager, aws_config, azure_config):
        """Test getting optimal provider with performance priority"""
        # AWS has better performance factor (1.0 vs 0.95)
        await manager.add_provider(aws_config)
        await manager.add_provider(azure_config)
        
        optimal = await manager.get_optimal_provider(
            ServiceType.COMPUTE,
            cost_priority=0.0,
            performance_priority=1.0
        )
        
        assert optimal == CloudProvider.AWS
        
    @pytest.mark.asyncio
    async def test_get_cost_comparison(self, manager, aws_config, azure_config):
        """Test getting cost comparison across providers"""
        await manager.add_provider(aws_config)
        await manager.add_provider(azure_config)
        
        comparison = await manager.get_cost_comparison(
            ServiceType.COMPUTE,
            'instance',
            'us-east-1'
        )
        
        assert CloudProvider.AWS in comparison
        assert CloudProvider.AZURE in comparison
        assert 'hourly_rate' in comparison[CloudProvider.AWS]
        assert 'hourly_rate' in comparison[CloudProvider.AZURE]
        
    @pytest.mark.asyncio
    async def test_migrate_resource(self, manager, aws_config, azure_config):
        """Test migrating a resource between providers"""
        await manager.add_provider(aws_config)
        await manager.add_provider(azure_config)
        
        # Create resource on AWS
        config = {'name': 'migrate-test'}
        aws_resource = await manager.create_resource(
            CloudProvider.AWS,
            ServiceType.COMPUTE,
            'instance',
            config
        )
        
        # Migrate to Azure
        azure_resource = await manager.migrate_resource(
            aws_resource.resource_id,
            CloudProvider.AZURE
        )
        
        assert azure_resource.provider == CloudProvider.AZURE
        assert azure_resource.service_type == aws_resource.service_type
        assert azure_resource.resource_id != aws_resource.resource_id
        
    @pytest.mark.asyncio
    async def test_get_provider_status(self, manager, aws_config, azure_config):
        """Test getting provider status"""
        await manager.add_provider(aws_config)
        await manager.add_provider(azure_config)
        
        status = await manager.get_provider_status()
        
        assert CloudProvider.AWS in status
        assert CloudProvider.AZURE in status
        
        aws_status = status[CloudProvider.AWS]
        assert aws_status['enabled'] is True
        assert aws_status['status'] == 'healthy'
        assert 'active_resources' in aws_status
        assert 'available_regions' in aws_status
        
    @pytest.mark.asyncio
    async def test_disabled_provider_excluded(self, manager):
        """Test that disabled providers are excluded from operations"""
        config = ProviderConfig(
            provider=CloudProvider.AWS,
            region='us-east-1',
            credentials={'access_key_id': 'test', 'secret_access_key': 'test'},
            enabled=False  # Disabled
        )
        
        await manager.add_provider(config)
        
        # Should not find optimal provider since AWS is disabled
        optimal = await manager.get_optimal_provider(ServiceType.COMPUTE)
        assert optimal is None
        
        # Should not include resources from disabled provider
        resources = await manager.list_all_resources()
        assert len(resources) == 0


class TestMultiCloudIntegration:
    """Integration tests for multi-cloud functionality"""
    
    @pytest.mark.asyncio
    async def test_full_multi_cloud_workflow(self):
        """Test complete multi-cloud workflow"""
        manager = CloudProviderManager()
        
        # Configure multiple providers
        aws_config = ProviderConfig(
            provider=CloudProvider.AWS,
            region='us-east-1',
            credentials={'access_key_id': 'test', 'secret_access_key': 'test'},
            priority=1,
            cost_factor=1.0
        )
        
        azure_config = ProviderConfig(
            provider=CloudProvider.AZURE,
            region='East US',
            credentials={'tenant_id': 'test', 'client_id': 'test', 'client_secret': 'test'},
            priority=2,
            cost_factor=1.1
        )
        
        gcp_config = ProviderConfig(
            provider=CloudProvider.GCP,
            region='us-central1',
            credentials={'project_id': 'test', 'service_account_key': 'test'},
            priority=3,
            cost_factor=0.95
        )
        
        # Add all providers
        await manager.add_provider(aws_config)
        await manager.add_provider(azure_config)
        await manager.add_provider(gcp_config)
        
        # Get optimal provider (should be GCP due to lowest cost)
        optimal = await manager.get_optimal_provider(
            ServiceType.COMPUTE,
            cost_priority=1.0,
            performance_priority=0.0
        )
        assert optimal == CloudProvider.GCP
        
        # Create resource on optimal provider
        resource = await manager.create_resource(
            optimal,
            ServiceType.COMPUTE,
            'instance',
            {'name': 'optimal-instance'}
        )
        assert resource.provider == CloudProvider.GCP
        
        # List all resources across providers
        all_resources = await manager.list_all_resources()
        assert len(all_resources) == 7  # 3 AWS + 2 Azure + 2 GCP
        
        # Get cost comparison
        costs = await manager.get_cost_comparison(
            ServiceType.COMPUTE, 'instance', 'us-east-1'
        )
        assert len(costs) == 3
        
        # Verify provider status
        status = await manager.get_provider_status()
        assert len(status) == 3
        assert all(info['status'] == 'healthy' for info in status.values())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

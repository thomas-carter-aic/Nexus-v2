"""
Tests for Edge Computing Module

This module contains comprehensive tests for the edge computing functionality
including edge management, orchestration, CDN integration, and IoT device management.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock

from src.edge import (
    EdgeLocation,
    EdgeProvider,
    EdgeCapability,
    EdgeWorkload,
    EdgeDeployment,
    EdgeManager,
    CDNIntegration,
    IoTDeviceManager,
    EdgeOrchestrator,
    WorkloadPlacement,
    EdgeScalingPolicy,
    EdgeLoadBalancer
)

from src.edge.edge_manager import WorkloadType, DeploymentStatus
from src.edge.edge_orchestrator import PlacementStrategy, ScalingTrigger, LoadBalancingAlgorithm


class TestEdgeLocation:
    """Test EdgeLocation class"""
    
    def test_edge_location_creation(self):
        """Test creating an edge location"""
        location = EdgeLocation(
            location_id='test-location-001',
            provider=EdgeProvider.AWS_WAVELENGTH,
            region='us-east-1',
            city='New York',
            country='USA',
            latitude=40.7128,
            longitude=-74.0060,
            capabilities={EdgeCapability.COMPUTE, EdgeCapability.STORAGE},
            capacity={'cpu_cores': 64, 'memory_gb': 256},
            cost_per_hour={EdgeCapability.COMPUTE: 0.15}
        )
        
        assert location.location_id == 'test-location-001'
        assert location.provider == EdgeProvider.AWS_WAVELENGTH
        assert location.city == 'New York'
        assert EdgeCapability.COMPUTE in location.capabilities
        assert location.capacity['cpu_cores'] == 64
        
    def test_edge_location_to_dict(self):
        """Test converting edge location to dictionary"""
        location = EdgeLocation(
            location_id='test-location-002',
            provider=EdgeProvider.AZURE_EDGE_ZONES,
            region='west-us',
            city='Los Angeles',
            country='USA',
            latitude=34.0522,
            longitude=-118.2437
        )
        
        location_dict = location.to_dict()
        assert location_dict['location_id'] == 'test-location-002'
        assert location_dict['provider'] == 'azure_edge_zones'
        assert location_dict['city'] == 'Los Angeles'
        assert location_dict['enabled'] is True


class TestEdgeWorkload:
    """Test EdgeWorkload class"""
    
    def test_edge_workload_creation(self):
        """Test creating an edge workload"""
        workload = EdgeWorkload(
            workload_id='workload-001',
            name='Test Web App',
            workload_type=WorkloadType.WEB_APPLICATION,
            application_id='web-app-001',
            image='nginx:latest',
            resource_requirements={'cpu_cores': 2, 'memory_gb': 4},
            target_locations=['location-1', 'location-2']
        )
        
        assert workload.workload_id == 'workload-001'
        assert workload.workload_type == WorkloadType.WEB_APPLICATION
        assert workload.resource_requirements['cpu_cores'] == 2
        assert len(workload.target_locations) == 2
        
    def test_edge_workload_to_dict(self):
        """Test converting edge workload to dictionary"""
        workload = EdgeWorkload(
            workload_id='workload-002',
            name='API Service',
            workload_type=WorkloadType.API_GATEWAY,
            application_id='api-001',
            image='api:v1.0'
        )
        
        workload_dict = workload.to_dict()
        assert workload_dict['workload_id'] == 'workload-002'
        assert workload_dict['workload_type'] == 'api_gateway'
        assert workload_dict['name'] == 'API Service'


class TestEdgeDeployment:
    """Test EdgeDeployment class"""
    
    def test_edge_deployment_creation(self):
        """Test creating an edge deployment"""
        deployment = EdgeDeployment(
            deployment_id='deploy-001',
            workload_id='workload-001',
            location_id='location-001',
            status=DeploymentStatus.RUNNING,
            instances=3,
            endpoint_url='https://edge.example.com/app'
        )
        
        assert deployment.deployment_id == 'deploy-001'
        assert deployment.status == DeploymentStatus.RUNNING
        assert deployment.instances == 3
        assert deployment.endpoint_url == 'https://edge.example.com/app'
        
    def test_edge_deployment_to_dict(self):
        """Test converting edge deployment to dictionary"""
        deployment = EdgeDeployment(
            deployment_id='deploy-002',
            workload_id='workload-002',
            location_id='location-002',
            status=DeploymentStatus.DEPLOYING
        )
        
        deployment_dict = deployment.to_dict()
        assert deployment_dict['deployment_id'] == 'deploy-002'
        assert deployment_dict['status'] == 'deploying'
        assert deployment_dict['instances'] == 1  # default


class TestCDNIntegration:
    """Test CDN integration functionality"""
    
    @pytest.fixture
    def cdn_integration(self):
        """Create CDN integration instance"""
        return CDNIntegration()
        
    @pytest.mark.asyncio
    async def test_configure_cdn_success(self, cdn_integration):
        """Test successful CDN configuration"""
        config = {'api_key': 'test-key', 'zone_id': 'test-zone'}
        result = await cdn_integration.configure_cdn('cloudflare', config)
        
        assert result is True
        assert cdn_integration.cdn_providers['cloudflare']['api_key'] == 'test-key'
        
    @pytest.mark.asyncio
    async def test_configure_cdn_invalid_provider(self, cdn_integration):
        """Test CDN configuration with invalid provider"""
        config = {'api_key': 'test-key'}
        result = await cdn_integration.configure_cdn('invalid_provider', config)
        
        assert result is False
        
    @pytest.mark.asyncio
    async def test_create_distribution(self, cdn_integration):
        """Test creating CDN distribution"""
        origins = ['https://edge1.example.com', 'https://edge2.example.com']
        config = {'cache_behaviors': {'default': {'ttl': 3600}}}
        
        distribution_id = await cdn_integration.create_distribution(
            'workload-001', origins, config
        )
        
        assert distribution_id.startswith('dist-workload-001-')
        
    @pytest.mark.asyncio
    async def test_update_cache_policy(self, cdn_integration):
        """Test updating cache policy"""
        policy = {'ttl': 7200, 'compress': True}
        result = await cdn_integration.update_cache_policy('dist-001', policy)
        
        assert result is True
        assert cdn_integration.cache_policies['dist-001'] == policy
        
    @pytest.mark.asyncio
    async def test_purge_cache(self, cdn_integration):
        """Test cache purging"""
        result = await cdn_integration.purge_cache('dist-001', ['/api/*', '/static/*'])
        assert result is True


class TestIoTDeviceManager:
    """Test IoT device management functionality"""
    
    @pytest.fixture
    def iot_manager(self):
        """Create IoT device manager instance"""
        return IoTDeviceManager()
        
    @pytest.mark.asyncio
    async def test_register_device(self, iot_manager):
        """Test registering IoT device"""
        device_info = {
            'type': 'sensor',
            'location': {'latitude': 40.7128, 'longitude': -74.0060},
            'capabilities': ['temperature', 'humidity'],
            'edge_location': 'edge-nyc-001'
        }
        
        result = await iot_manager.register_device('device-001', device_info)
        assert result is True
        assert 'device-001' in iot_manager.devices
        assert iot_manager.devices['device-001']['device_type'] == 'sensor'
        
    @pytest.mark.asyncio
    async def test_update_device_status(self, iot_manager):
        """Test updating device status"""
        # Register device first
        await iot_manager.register_device('device-002', {'type': 'actuator'})
        
        result = await iot_manager.update_device_status('device-002', 'offline')
        assert result is True
        assert iot_manager.devices['device-002']['status'] == 'offline'
        
    @pytest.mark.asyncio
    async def test_get_device_telemetry(self, iot_manager):
        """Test getting device telemetry"""
        telemetry = await iot_manager.get_device_telemetry('device-001')
        assert isinstance(telemetry, list)
        
    @pytest.mark.asyncio
    async def test_send_command(self, iot_manager):
        """Test sending command to device"""
        # Register device first
        await iot_manager.register_device('device-003', {'type': 'actuator'})
        
        command = {'action': 'turn_on', 'duration': 300}
        result = await iot_manager.send_command('device-003', command)
        assert result is True


class TestEdgeManager:
    """Test EdgeManager class"""
    
    @pytest.fixture
    def edge_manager(self):
        """Create EdgeManager instance"""
        return EdgeManager()
        
    @pytest.mark.asyncio
    async def test_add_edge_location(self, edge_manager):
        """Test adding edge location"""
        location = EdgeLocation(
            location_id='custom-location-001',
            provider=EdgeProvider.CLOUDFLARE_WORKERS,
            region='global',
            city='Global',
            country='Global',
            latitude=0.0,
            longitude=0.0
        )
        
        result = await edge_manager.add_edge_location(location)
        assert result is True
        assert 'custom-location-001' in edge_manager.edge_locations
        
    @pytest.mark.asyncio
    async def test_get_edge_locations(self, edge_manager):
        """Test getting edge locations"""
        # Get all locations
        all_locations = await edge_manager.get_edge_locations()
        assert len(all_locations) >= 4  # Initial sample locations
        
        # Filter by provider
        aws_locations = await edge_manager.get_edge_locations(
            provider=EdgeProvider.AWS_WAVELENGTH
        )
        assert len(aws_locations) >= 1
        assert all(loc.provider == EdgeProvider.AWS_WAVELENGTH for loc in aws_locations)
        
        # Filter by capability
        compute_locations = await edge_manager.get_edge_locations(
            capability=EdgeCapability.COMPUTE
        )
        assert len(compute_locations) >= 1
        assert all(EdgeCapability.COMPUTE in loc.capabilities for loc in compute_locations)
        
    @pytest.mark.asyncio
    async def test_create_workload(self, edge_manager):
        """Test creating workload"""
        workload = EdgeWorkload(
            workload_id='test-workload-001',
            name='Test Application',
            workload_type=WorkloadType.WEB_APPLICATION,
            application_id='test-app',
            image='nginx:latest'
        )
        
        result = await edge_manager.create_workload(workload)
        assert result is True
        assert 'test-workload-001' in edge_manager.workloads
        
    @pytest.mark.asyncio
    async def test_deploy_workload(self, edge_manager):
        """Test deploying workload"""
        # Create workload first
        workload = EdgeWorkload(
            workload_id='deploy-test-001',
            name='Deploy Test App',
            workload_type=WorkloadType.MICROSERVICE,
            application_id='deploy-app',
            image='app:latest'
        )
        await edge_manager.create_workload(workload)
        
        # Deploy workload
        deployment_ids = await edge_manager.deploy_workload('deploy-test-001')
        assert len(deployment_ids) > 0
        
        # Check deployments were created
        for deployment_id in deployment_ids:
            assert deployment_id in edge_manager.deployments
            deployment = edge_manager.deployments[deployment_id]
            assert deployment.workload_id == 'deploy-test-001'
            assert deployment.status == DeploymentStatus.RUNNING
            
    @pytest.mark.asyncio
    async def test_find_optimal_locations(self, edge_manager):
        """Test finding optimal locations"""
        workload = EdgeWorkload(
            workload_id='optimal-test-001',
            name='Optimal Test App',
            workload_type=WorkloadType.WEB_APPLICATION,
            application_id='optimal-app',
            image='web:latest'
        )
        
        user_locations = [
            {'latitude': 40.7128, 'longitude': -74.0060},  # New York
            {'latitude': 34.0522, 'longitude': -118.2437}  # Los Angeles
        ]
        
        optimal_locations = await edge_manager.find_optimal_locations(
            workload, user_locations, max_locations=2
        )
        
        assert len(optimal_locations) <= 2
        assert all(isinstance(loc_id, str) for loc_id in optimal_locations)
        
    @pytest.mark.asyncio
    async def test_scale_deployment(self, edge_manager):
        """Test scaling deployment"""
        # Create and deploy workload first
        workload = EdgeWorkload(
            workload_id='scale-test-001',
            name='Scale Test App',
            workload_type=WorkloadType.API_GATEWAY,
            application_id='scale-app',
            image='api:latest'
        )
        await edge_manager.create_workload(workload)
        deployment_ids = await edge_manager.deploy_workload('scale-test-001')
        
        # Check if deployments were created
        assert len(deployment_ids) > 0, "No deployments were created"
        
        # Scale deployment
        deployment_id = deployment_ids[0]
        result = await edge_manager.scale_deployment(deployment_id, 5)
        assert result is True
        
        deployment = edge_manager.deployments[deployment_id]
        assert deployment.instances == 5
        
    @pytest.mark.asyncio
    async def test_get_workload_analytics(self, edge_manager):
        """Test getting workload analytics"""
        # Create and deploy workload first
        workload = EdgeWorkload(
            workload_id='analytics-test-001',
            name='Analytics Test App',
            workload_type=WorkloadType.WEB_APPLICATION,
            application_id='analytics-app',
            image='web:latest'
        )
        await edge_manager.create_workload(workload)
        await edge_manager.deploy_workload('analytics-test-001')
        
        analytics = await edge_manager.get_workload_analytics('analytics-test-001')
        
        assert analytics['workload_id'] == 'analytics-test-001'
        assert 'total_deployments' in analytics
        assert 'active_deployments' in analytics
        assert 'total_requests_per_second' in analytics
        assert analytics['total_deployments'] > 0
        
    @pytest.mark.asyncio
    async def test_get_edge_status(self, edge_manager):
        """Test getting edge status"""
        status = await edge_manager.get_edge_status()
        
        assert 'edge_locations' in status
        assert 'workloads' in status
        assert 'deployments' in status
        assert 'capacity' in status
        assert 'performance' in status
        
        assert status['edge_locations']['total'] >= 4  # Initial locations
        assert isinstance(status['capacity']['total_cpu_cores'], int)


class TestWorkloadPlacement:
    """Test WorkloadPlacement class"""
    
    def test_workload_placement_creation(self):
        """Test creating workload placement"""
        placement = WorkloadPlacement(
            placement_id='placement-001',
            workload_id='workload-001',
            strategy=PlacementStrategy.BALANCED,
            selected_locations=['loc-1', 'loc-2'],
            placement_score=85.5,
            reasoning={'strategy': 'balanced', 'factors': ['cost', 'latency']}
        )
        
        assert placement.placement_id == 'placement-001'
        assert placement.strategy == PlacementStrategy.BALANCED
        assert len(placement.selected_locations) == 2
        assert placement.placement_score == 85.5
        
    def test_workload_placement_to_dict(self):
        """Test converting placement to dictionary"""
        placement = WorkloadPlacement(
            placement_id='placement-002',
            workload_id='workload-002',
            strategy=PlacementStrategy.LATENCY_OPTIMIZED,
            selected_locations=['loc-3'],
            placement_score=92.0
        )
        
        placement_dict = placement.to_dict()
        assert placement_dict['placement_id'] == 'placement-002'
        assert placement_dict['strategy'] == 'latency_optimized'
        assert placement_dict['placement_score'] == 92.0


class TestEdgeOrchestrator:
    """Test EdgeOrchestrator class"""
    
    @pytest.fixture
    def edge_manager(self):
        """Create EdgeManager instance"""
        return EdgeManager()
        
    @pytest.fixture
    def orchestrator(self, edge_manager):
        """Create EdgeOrchestrator instance"""
        return EdgeOrchestrator(edge_manager)
        
    @pytest.mark.asyncio
    async def test_create_intelligent_placement(self, orchestrator, edge_manager):
        """Test creating intelligent placement"""
        # Create workload first
        workload = EdgeWorkload(
            workload_id='placement-test-001',
            name='Placement Test App',
            workload_type=WorkloadType.WEB_APPLICATION,
            application_id='placement-app',
            image='web:latest'
        )
        await edge_manager.create_workload(workload)
        
        user_locations = [
            {'latitude': 40.7128, 'longitude': -74.0060}  # New York
        ]
        
        placement = await orchestrator.create_intelligent_placement(
            'placement-test-001',
            PlacementStrategy.LATENCY_OPTIMIZED,
            user_locations,
            {'max_locations': 2}
        )
        
        assert placement.workload_id == 'placement-test-001'
        assert placement.strategy == PlacementStrategy.LATENCY_OPTIMIZED
        assert len(placement.selected_locations) <= 2
        assert placement.placement_score > 0
        assert placement.placement_id in orchestrator.placements
        
    @pytest.mark.asyncio
    async def test_create_scaling_policy(self, orchestrator):
        """Test creating scaling policy"""
        policy = EdgeScalingPolicy(
            policy_id='policy-001',
            workload_id='workload-001',
            trigger=ScalingTrigger.CPU_UTILIZATION,
            threshold_up=80.0,
            threshold_down=20.0,
            min_instances=1,
            max_instances=10
        )
        
        result = await orchestrator.create_scaling_policy(policy)
        assert result is True
        assert 'policy-001' in orchestrator.scaling_policies
        
    @pytest.mark.asyncio
    async def test_create_load_balancer(self, orchestrator):
        """Test creating load balancer"""
        load_balancer = EdgeLoadBalancer(
            lb_id='lb-001',
            name='Test Load Balancer',
            workload_id='workload-001',
            algorithm=LoadBalancingAlgorithm.ROUND_ROBIN,
            target_deployments=['deploy-1', 'deploy-2']
        )
        
        result = await orchestrator.create_load_balancer(load_balancer)
        assert result is True
        assert 'lb-001' in orchestrator.load_balancers
        
    @pytest.mark.asyncio
    async def test_get_workload_insights(self, orchestrator, edge_manager):
        """Test getting workload insights"""
        # Create workload and placement
        workload = EdgeWorkload(
            workload_id='insights-test-001',
            name='Insights Test App',
            workload_type=WorkloadType.API_GATEWAY,
            application_id='insights-app',
            image='api:latest'
        )
        await edge_manager.create_workload(workload)
        
        await orchestrator.create_intelligent_placement(
            'insights-test-001',
            PlacementStrategy.BALANCED,
            [],
            {'max_locations': 1}
        )
        
        insights = await orchestrator.get_workload_insights('insights-test-001')
        
        assert insights['workload_id'] == 'insights-test-001'
        assert 'placement_info' in insights
        assert 'scaling_history' in insights
        assert 'traffic_patterns' in insights
        assert 'recommendations' in insights
        
    @pytest.mark.asyncio
    async def test_get_orchestrator_status(self, orchestrator):
        """Test getting orchestrator status"""
        status = await orchestrator.get_orchestrator_status()
        
        assert 'placements' in status
        assert 'scaling_policies' in status
        assert 'load_balancers' in status
        
        assert isinstance(status['placements']['total'], int)
        assert isinstance(status['scaling_policies']['total'], int)
        assert isinstance(status['load_balancers']['total'], int)


class TestEdgeIntegration:
    """Integration tests for edge computing functionality"""
    
    @pytest.mark.asyncio
    async def test_full_edge_workflow(self):
        """Test complete edge computing workflow"""
        # Create edge manager and orchestrator
        edge_manager = EdgeManager()
        orchestrator = EdgeOrchestrator(edge_manager)
        
        # Create workload
        workload = EdgeWorkload(
            workload_id='integration-test-001',
            name='Integration Test App',
            workload_type=WorkloadType.WEB_APPLICATION,
            application_id='integration-app',
            image='nginx:latest',
            resource_requirements={'cpu_cores': 2, 'memory_gb': 4}
        )
        
        # Create workload
        await edge_manager.create_workload(workload)
        
        # Create intelligent placement
        user_locations = [
            {'latitude': 40.7128, 'longitude': -74.0060},  # New York
            {'latitude': 34.0522, 'longitude': -118.2437}  # Los Angeles
        ]
        
        placement = await orchestrator.create_intelligent_placement(
            'integration-test-001',
            PlacementStrategy.BALANCED,
            user_locations,
            {'max_locations': 2}
        )
        
        # Deploy workload to selected locations
        deployment_ids = await edge_manager.deploy_workload(
            'integration-test-001',
            placement.selected_locations
        )
        
        # Create scaling policy
        scaling_policy = EdgeScalingPolicy(
            policy_id='integration-policy-001',
            workload_id='integration-test-001',
            trigger=ScalingTrigger.CPU_UTILIZATION,
            threshold_up=70.0,
            threshold_down=30.0
        )
        await orchestrator.create_scaling_policy(scaling_policy)
        
        # Create load balancer
        load_balancer = EdgeLoadBalancer(
            lb_id='integration-lb-001',
            name='Integration Load Balancer',
            workload_id='integration-test-001',
            algorithm=LoadBalancingAlgorithm.LEAST_RESPONSE_TIME,
            target_deployments=deployment_ids
        )
        await orchestrator.create_load_balancer(load_balancer)
        
        # Verify everything was created
        assert len(deployment_ids) > 0
        assert placement.placement_id in orchestrator.placements
        assert 'integration-policy-001' in orchestrator.scaling_policies
        assert 'integration-lb-001' in orchestrator.load_balancers
        
        # Get analytics and insights
        analytics = await edge_manager.get_workload_analytics('integration-test-001')
        insights = await orchestrator.get_workload_insights('integration-test-001')
        
        assert analytics['workload_id'] == 'integration-test-001'
        assert insights['workload_id'] == 'integration-test-001'
        assert analytics['total_deployments'] == len(deployment_ids)
        
        # Test scaling
        if deployment_ids:
            result = await edge_manager.scale_deployment(deployment_ids[0], 3)
            assert result is True
            
        # Get final status
        edge_status = await edge_manager.get_edge_status()
        orchestrator_status = await orchestrator.get_orchestrator_status()
        
        assert edge_status['workloads']['total'] >= 1
        assert orchestrator_status['placements']['total'] >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

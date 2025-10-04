"""
Edge Computing Manager

This module provides comprehensive edge computing management capabilities including
edge location management, workload deployment, CDN integration, and IoT device management.
"""

import asyncio
import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union, Set
from dataclasses import dataclass, field
from uuid import UUID, uuid4
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class EdgeProvider(Enum):
    """Supported edge computing providers"""
    AWS_WAVELENGTH = "aws_wavelength"
    AZURE_EDGE_ZONES = "azure_edge_zones"
    GCP_EDGE_LOCATIONS = "gcp_edge_locations"
    CLOUDFLARE_WORKERS = "cloudflare_workers"
    FASTLY_COMPUTE = "fastly_compute"
    AKAMAI_EDGE = "akamai_edge"
    CDN77_EDGE = "cdn77_edge"
    STACKPATH_EDGE = "stackpath_edge"


class EdgeCapability(Enum):
    """Edge computing capabilities"""
    COMPUTE = "compute"
    STORAGE = "storage"
    CDN = "cdn"
    ANALYTICS = "analytics"
    AI_INFERENCE = "ai_inference"
    IOT_GATEWAY = "iot_gateway"
    STREAMING = "streaming"
    CACHING = "caching"
    SECURITY = "security"
    NETWORKING = "networking"


class WorkloadType(Enum):
    """Types of edge workloads"""
    WEB_APPLICATION = "web_application"
    API_GATEWAY = "api_gateway"
    MICROSERVICE = "microservice"
    STATIC_CONTENT = "static_content"
    STREAMING_SERVICE = "streaming_service"
    IOT_PROCESSOR = "iot_processor"
    AI_INFERENCE = "ai_inference"
    EDGE_ANALYTICS = "edge_analytics"
    CACHE_SERVICE = "cache_service"
    SECURITY_SERVICE = "security_service"


class DeploymentStatus(Enum):
    """Edge deployment status"""
    PENDING = "pending"
    DEPLOYING = "deploying"
    RUNNING = "running"
    SCALING = "scaling"
    UPDATING = "updating"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class EdgeLocation:
    """Represents an edge computing location"""
    location_id: str
    provider: EdgeProvider
    region: str
    city: str
    country: str
    latitude: float
    longitude: float
    capabilities: Set[EdgeCapability] = field(default_factory=set)
    capacity: Dict[str, Any] = field(default_factory=dict)
    current_load: Dict[str, float] = field(default_factory=dict)
    latency_to_regions: Dict[str, float] = field(default_factory=dict)
    cost_per_hour: Dict[EdgeCapability, float] = field(default_factory=dict)
    availability_zone: Optional[str] = None
    network_tier: str = "premium"
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'location_id': self.location_id,
            'provider': self.provider.value,
            'region': self.region,
            'city': self.city,
            'country': self.country,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'capabilities': [cap.value for cap in self.capabilities],
            'capacity': self.capacity,
            'current_load': self.current_load,
            'latency_to_regions': self.latency_to_regions,
            'cost_per_hour': {cap.value: cost for cap, cost in self.cost_per_hour.items()},
            'availability_zone': self.availability_zone,
            'network_tier': self.network_tier,
            'enabled': self.enabled,
            'created_at': self.created_at.isoformat()
        }


@dataclass
class EdgeWorkload:
    """Represents a workload deployed to edge locations"""
    workload_id: str
    name: str
    workload_type: WorkloadType
    application_id: str
    image: str
    configuration: Dict[str, Any] = field(default_factory=dict)
    resource_requirements: Dict[str, Any] = field(default_factory=dict)
    target_locations: List[str] = field(default_factory=list)
    routing_rules: Dict[str, Any] = field(default_factory=dict)
    scaling_policy: Dict[str, Any] = field(default_factory=dict)
    health_check: Dict[str, Any] = field(default_factory=dict)
    environment_variables: Dict[str, str] = field(default_factory=dict)
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'workload_id': self.workload_id,
            'name': self.name,
            'workload_type': self.workload_type.value,
            'application_id': self.application_id,
            'image': self.image,
            'configuration': self.configuration,
            'resource_requirements': self.resource_requirements,
            'target_locations': self.target_locations,
            'routing_rules': self.routing_rules,
            'scaling_policy': self.scaling_policy,
            'health_check': self.health_check,
            'environment_variables': self.environment_variables,
            'tags': self.tags,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


@dataclass
class EdgeDeployment:
    """Represents a deployment of a workload to an edge location"""
    deployment_id: str
    workload_id: str
    location_id: str
    status: DeploymentStatus
    instances: int = 1
    endpoint_url: Optional[str] = None
    health_status: str = "unknown"
    metrics: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
    deployed_at: Optional[datetime] = None
    last_updated: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'deployment_id': self.deployment_id,
            'workload_id': self.workload_id,
            'location_id': self.location_id,
            'status': self.status.value,
            'instances': self.instances,
            'endpoint_url': self.endpoint_url,
            'health_status': self.health_status,
            'metrics': self.metrics,
            'logs': self.logs[-10:],  # Keep only last 10 log entries
            'error_message': self.error_message,
            'deployed_at': self.deployed_at.isoformat() if self.deployed_at else None,
            'last_updated': self.last_updated.isoformat()
        }


class CDNIntegration:
    """CDN integration for edge content delivery"""
    
    def __init__(self):
        self.cdn_providers = {
            'cloudflare': {'api_key': None, 'zone_id': None},
            'fastly': {'api_key': None, 'service_id': None},
            'akamai': {'client_token': None, 'access_token': None},
            'aws_cloudfront': {'access_key': None, 'secret_key': None}
        }
        self.cache_policies = {}
        
    async def configure_cdn(self, provider: str, config: Dict[str, str]) -> bool:
        """Configure CDN provider"""
        try:
            if provider not in self.cdn_providers:
                raise ValueError(f"Unsupported CDN provider: {provider}")
                
            self.cdn_providers[provider].update(config)
            logger.info(f"Configured CDN provider: {provider}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to configure CDN provider {provider}: {e}")
            return False
            
    async def create_distribution(self, workload_id: str, 
                                origins: List[str], config: Dict[str, Any]) -> str:
        """Create CDN distribution for workload"""
        try:
            distribution_id = f"dist-{workload_id}-{str(uuid4())[:8]}"
            
            # Mock CDN distribution creation
            distribution_config = {
                'distribution_id': distribution_id,
                'origins': origins,
                'cache_behaviors': config.get('cache_behaviors', {}),
                'custom_error_responses': config.get('error_responses', {}),
                'price_class': config.get('price_class', 'PriceClass_All'),
                'enabled': True,
                'status': 'InProgress'
            }
            
            # Simulate distribution deployment
            await asyncio.sleep(0.1)
            distribution_config['status'] = 'Deployed'
            distribution_config['domain_name'] = f"{distribution_id}.cloudfront.net"
            
            logger.info(f"Created CDN distribution: {distribution_id}")
            return distribution_id
            
        except Exception as e:
            logger.error(f"Failed to create CDN distribution: {e}")
            raise
            
    async def update_cache_policy(self, distribution_id: str, 
                                policy: Dict[str, Any]) -> bool:
        """Update cache policy for distribution"""
        try:
            self.cache_policies[distribution_id] = policy
            logger.info(f"Updated cache policy for distribution: {distribution_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update cache policy: {e}")
            return False
            
    async def purge_cache(self, distribution_id: str, 
                         paths: List[str] = None) -> bool:
        """Purge cache for distribution"""
        try:
            if paths is None:
                paths = ["/*"]  # Purge all
                
            # Mock cache purge
            await asyncio.sleep(0.1)
            logger.info(f"Purged cache for distribution {distribution_id}: {paths}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to purge cache: {e}")
            return False


class IoTDeviceManager:
    """IoT device management for edge computing"""
    
    def __init__(self):
        self.devices = {}
        self.device_groups = {}
        self.telemetry_data = {}
        
    async def register_device(self, device_id: str, 
                            device_info: Dict[str, Any]) -> bool:
        """Register IoT device"""
        try:
            device = {
                'device_id': device_id,
                'device_type': device_info.get('type', 'generic'),
                'location': device_info.get('location', {}),
                'capabilities': device_info.get('capabilities', []),
                'edge_location': device_info.get('edge_location'),
                'status': 'online',
                'last_seen': datetime.utcnow(),
                'registered_at': datetime.utcnow()
            }
            
            self.devices[device_id] = device
            logger.info(f"Registered IoT device: {device_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register device {device_id}: {e}")
            return False
            
    async def update_device_status(self, device_id: str, status: str) -> bool:
        """Update device status"""
        if device_id in self.devices:
            self.devices[device_id]['status'] = status
            self.devices[device_id]['last_seen'] = datetime.utcnow()
            return True
        return False
        
    async def get_device_telemetry(self, device_id: str, 
                                 time_range: Optional[timedelta] = None) -> List[Dict[str, Any]]:
        """Get device telemetry data"""
        if device_id not in self.telemetry_data:
            return []
            
        telemetry = self.telemetry_data[device_id]
        
        if time_range:
            cutoff_time = datetime.utcnow() - time_range
            telemetry = [t for t in telemetry if t['timestamp'] >= cutoff_time]
            
        return telemetry
        
    async def send_command(self, device_id: str, command: Dict[str, Any]) -> bool:
        """Send command to IoT device"""
        try:
            if device_id not in self.devices:
                raise ValueError(f"Device {device_id} not found")
                
            # Mock command sending
            await asyncio.sleep(0.1)
            logger.info(f"Sent command to device {device_id}: {command}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send command to device {device_id}: {e}")
            return False


class EdgeManager:
    """
    Comprehensive edge computing manager for distributed application deployment
    """
    
    def __init__(self):
        self.edge_locations: Dict[str, EdgeLocation] = {}
        self.workloads: Dict[str, EdgeWorkload] = {}
        self.deployments: Dict[str, EdgeDeployment] = {}
        self.cdn_integration = CDNIntegration()
        self.iot_manager = IoTDeviceManager()
        
        # Initialize with sample edge locations
        self._initialize_edge_locations()
        
    def _initialize_edge_locations(self):
        """Initialize sample edge locations"""
        sample_locations = [
            {
                'location_id': 'aws-wavelength-us-east-1',
                'provider': EdgeProvider.AWS_WAVELENGTH,
                'region': 'us-east-1',
                'city': 'New York',
                'country': 'USA',
                'latitude': 40.7128,
                'longitude': -74.0060,
                'capabilities': {EdgeCapability.COMPUTE, EdgeCapability.STORAGE, EdgeCapability.AI_INFERENCE},
                'capacity': {'cpu_cores': 64, 'memory_gb': 256, 'storage_gb': 1000},
                'cost_per_hour': {EdgeCapability.COMPUTE: 0.15, EdgeCapability.STORAGE: 0.02}
            },
            {
                'location_id': 'azure-edge-west-us',
                'provider': EdgeProvider.AZURE_EDGE_ZONES,
                'region': 'west-us',
                'city': 'Los Angeles',
                'country': 'USA',
                'latitude': 34.0522,
                'longitude': -118.2437,
                'capabilities': {EdgeCapability.COMPUTE, EdgeCapability.CDN, EdgeCapability.STREAMING},
                'capacity': {'cpu_cores': 48, 'memory_gb': 192, 'storage_gb': 800},
                'cost_per_hour': {EdgeCapability.COMPUTE: 0.18, EdgeCapability.CDN: 0.05}
            },
            {
                'location_id': 'gcp-edge-europe-west1',
                'provider': EdgeProvider.GCP_EDGE_LOCATIONS,
                'region': 'europe-west1',
                'city': 'London',
                'country': 'UK',
                'latitude': 51.5074,
                'longitude': -0.1278,
                'capabilities': {EdgeCapability.COMPUTE, EdgeCapability.ANALYTICS, EdgeCapability.IOT_GATEWAY},
                'capacity': {'cpu_cores': 32, 'memory_gb': 128, 'storage_gb': 500},
                'cost_per_hour': {EdgeCapability.COMPUTE: 0.16, EdgeCapability.ANALYTICS: 0.08}
            },
            {
                'location_id': 'cloudflare-workers-global',
                'provider': EdgeProvider.CLOUDFLARE_WORKERS,
                'region': 'global',
                'city': 'Global',
                'country': 'Global',
                'latitude': 0.0,
                'longitude': 0.0,
                'capabilities': {EdgeCapability.COMPUTE, EdgeCapability.CDN, EdgeCapability.SECURITY},
                'capacity': {'cpu_cores': 1000, 'memory_gb': 2000, 'storage_gb': 10000},
                'cost_per_hour': {EdgeCapability.COMPUTE: 0.05, EdgeCapability.CDN: 0.01}
            }
        ]
        
        for location_data in sample_locations:
            location = EdgeLocation(**location_data)
            self.edge_locations[location.location_id] = location
            
    async def add_edge_location(self, location: EdgeLocation) -> bool:
        """Add new edge location"""
        try:
            self.edge_locations[location.location_id] = location
            logger.info(f"Added edge location: {location.location_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add edge location: {e}")
            return False
            
    async def get_edge_locations(self, provider: Optional[EdgeProvider] = None,
                               capability: Optional[EdgeCapability] = None) -> List[EdgeLocation]:
        """Get edge locations with optional filtering"""
        locations = list(self.edge_locations.values())
        
        if provider:
            locations = [loc for loc in locations if loc.provider == provider]
            
        if capability:
            locations = [loc for loc in locations if capability in loc.capabilities]
            
        return locations
        
    async def find_optimal_locations(self, workload: EdgeWorkload,
                                   user_locations: List[Dict[str, float]],
                                   max_locations: int = 3) -> List[str]:
        """Find optimal edge locations for workload deployment"""
        try:
            suitable_locations = []
            
            for location in self.edge_locations.values():
                if not location.enabled:
                    continue
                    
                # Check if location has required capabilities
                required_caps = self._get_required_capabilities(workload.workload_type)
                if not required_caps.issubset(location.capabilities):
                    continue
                    
                # Calculate score based on latency, cost, and capacity
                score = await self._calculate_location_score(
                    location, workload, user_locations
                )
                
                suitable_locations.append((location.location_id, score))
                
            # Sort by score and return top locations
            suitable_locations.sort(key=lambda x: x[1], reverse=True)
            return [loc_id for loc_id, _ in suitable_locations[:max_locations]]
            
        except Exception as e:
            logger.error(f"Failed to find optimal locations: {e}")
            return []
            
    def _get_required_capabilities(self, workload_type: WorkloadType) -> Set[EdgeCapability]:
        """Get required capabilities for workload type"""
        capability_map = {
            WorkloadType.WEB_APPLICATION: {EdgeCapability.COMPUTE},
            WorkloadType.API_GATEWAY: {EdgeCapability.COMPUTE},
            WorkloadType.MICROSERVICE: {EdgeCapability.COMPUTE},
            WorkloadType.STATIC_CONTENT: {EdgeCapability.CDN, EdgeCapability.STORAGE},
            WorkloadType.STREAMING_SERVICE: {EdgeCapability.STREAMING, EdgeCapability.CDN},
            WorkloadType.IOT_PROCESSOR: {EdgeCapability.IOT_GATEWAY, EdgeCapability.COMPUTE},
            WorkloadType.AI_INFERENCE: {EdgeCapability.AI_INFERENCE, EdgeCapability.COMPUTE},
            WorkloadType.EDGE_ANALYTICS: {EdgeCapability.ANALYTICS, EdgeCapability.COMPUTE},
            WorkloadType.CACHE_SERVICE: {EdgeCapability.CACHING, EdgeCapability.STORAGE},
            WorkloadType.SECURITY_SERVICE: {EdgeCapability.SECURITY, EdgeCapability.NETWORKING}
        }
        
        return capability_map.get(workload_type, {EdgeCapability.COMPUTE})
        
    async def _calculate_location_score(self, location: EdgeLocation,
                                      workload: EdgeWorkload,
                                      user_locations: List[Dict[str, float]]) -> float:
        """Calculate score for edge location"""
        try:
            score = 0.0
            
            # Latency score (lower latency = higher score)
            avg_latency = self._calculate_average_latency(location, user_locations)
            latency_score = max(0, 100 - avg_latency)  # 100ms = 0 score, 0ms = 100 score
            score += latency_score * 0.4
            
            # Cost score (lower cost = higher score)
            required_caps = self._get_required_capabilities(workload.workload_type)
            avg_cost = sum(location.cost_per_hour.get(cap, 0.1) for cap in required_caps) / len(required_caps)
            cost_score = max(0, 100 - (avg_cost * 500))  # $0.20/hour = 0 score
            score += cost_score * 0.3
            
            # Capacity score (more available capacity = higher score)
            cpu_utilization = location.current_load.get('cpu', 0)
            capacity_score = max(0, 100 - cpu_utilization)
            score += capacity_score * 0.3
            
            return score
            
        except Exception as e:
            logger.error(f"Failed to calculate location score: {e}")
            return 0.0
            
    def _calculate_average_latency(self, location: EdgeLocation,
                                 user_locations: List[Dict[str, float]]) -> float:
        """Calculate average latency to user locations"""
        if not user_locations:
            return 50.0  # Default latency
            
        total_latency = 0.0
        for user_loc in user_locations:
            # Simple distance-based latency calculation
            lat_diff = abs(location.latitude - user_loc.get('latitude', 0))
            lon_diff = abs(location.longitude - user_loc.get('longitude', 0))
            distance = (lat_diff + lon_diff) * 111  # Rough km conversion
            latency = min(distance * 0.1, 200)  # Max 200ms latency
            total_latency += latency
            
        return total_latency / len(user_locations)
        
    async def create_workload(self, workload: EdgeWorkload) -> bool:
        """Create new edge workload"""
        try:
            self.workloads[workload.workload_id] = workload
            logger.info(f"Created edge workload: {workload.workload_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create workload: {e}")
            return False
            
    async def deploy_workload(self, workload_id: str,
                            target_locations: Optional[List[str]] = None) -> List[str]:
        """Deploy workload to edge locations"""
        try:
            if workload_id not in self.workloads:
                raise ValueError(f"Workload {workload_id} not found")
                
            workload = self.workloads[workload_id]
            
            # Use specified locations or find optimal ones
            if target_locations:
                locations = target_locations
            else:
                locations = await self.find_optimal_locations(workload, [])
                
            deployment_ids = []
            
            for location_id in locations:
                if location_id not in self.edge_locations:
                    logger.warning(f"Edge location {location_id} not found")
                    continue
                    
                deployment_id = f"deploy-{workload_id}-{location_id}-{str(uuid4())[:8]}"
                
                deployment = EdgeDeployment(
                    deployment_id=deployment_id,
                    workload_id=workload_id,
                    location_id=location_id,
                    status=DeploymentStatus.DEPLOYING
                )
                
                # Simulate deployment process
                await self._execute_deployment(deployment)
                
                self.deployments[deployment_id] = deployment
                deployment_ids.append(deployment_id)
                
            logger.info(f"Deployed workload {workload_id} to {len(deployment_ids)} locations")
            return deployment_ids
            
        except Exception as e:
            logger.error(f"Failed to deploy workload {workload_id}: {e}")
            return []
            
    async def _execute_deployment(self, deployment: EdgeDeployment) -> bool:
        """Execute deployment to edge location"""
        try:
            # Simulate deployment steps
            await asyncio.sleep(0.1)  # Simulate deployment time
            
            # Update deployment status
            deployment.status = DeploymentStatus.RUNNING
            deployment.deployed_at = datetime.utcnow()
            deployment.endpoint_url = f"https://{deployment.location_id}.edge.example.com/{deployment.workload_id}"
            deployment.health_status = "healthy"
            
            # Initialize metrics
            deployment.metrics = {
                'cpu_usage': 25.0,
                'memory_usage': 40.0,
                'requests_per_second': 100.0,
                'response_time_ms': 15.0,
                'error_rate': 0.1
            }
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to execute deployment {deployment.deployment_id}: {e}")
            deployment.status = DeploymentStatus.ERROR
            deployment.error_message = str(e)
            return False
            
    async def get_workload_deployments(self, workload_id: str) -> List[EdgeDeployment]:
        """Get all deployments for a workload"""
        return [
            deployment for deployment in self.deployments.values()
            if deployment.workload_id == workload_id
        ]
        
    async def scale_deployment(self, deployment_id: str, instances: int) -> bool:
        """Scale deployment instances"""
        try:
            if deployment_id not in self.deployments:
                raise ValueError(f"Deployment {deployment_id} not found")
                
            deployment = self.deployments[deployment_id]
            deployment.status = DeploymentStatus.SCALING
            
            # Simulate scaling
            await asyncio.sleep(0.1)
            
            deployment.instances = instances
            deployment.status = DeploymentStatus.RUNNING
            deployment.last_updated = datetime.utcnow()
            
            logger.info(f"Scaled deployment {deployment_id} to {instances} instances")
            return True
            
        except Exception as e:
            logger.error(f"Failed to scale deployment {deployment_id}: {e}")
            return False
            
    async def update_workload(self, workload_id: str, updates: Dict[str, Any]) -> bool:
        """Update workload configuration"""
        try:
            if workload_id not in self.workloads:
                raise ValueError(f"Workload {workload_id} not found")
                
            workload = self.workloads[workload_id]
            
            # Update workload configuration
            for key, value in updates.items():
                if hasattr(workload, key):
                    setattr(workload, key, value)
                    
            workload.updated_at = datetime.utcnow()
            
            # Update all deployments
            deployments = await self.get_workload_deployments(workload_id)
            for deployment in deployments:
                deployment.status = DeploymentStatus.UPDATING
                await self._execute_deployment(deployment)
                
            logger.info(f"Updated workload {workload_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update workload {workload_id}: {e}")
            return False
            
    async def delete_workload(self, workload_id: str) -> bool:
        """Delete workload and all its deployments"""
        try:
            if workload_id not in self.workloads:
                raise ValueError(f"Workload {workload_id} not found")
                
            # Delete all deployments
            deployments = await self.get_workload_deployments(workload_id)
            for deployment in deployments:
                await self.delete_deployment(deployment.deployment_id)
                
            # Delete workload
            del self.workloads[workload_id]
            
            logger.info(f"Deleted workload {workload_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete workload {workload_id}: {e}")
            return False
            
    async def delete_deployment(self, deployment_id: str) -> bool:
        """Delete specific deployment"""
        try:
            if deployment_id not in self.deployments:
                raise ValueError(f"Deployment {deployment_id} not found")
                
            deployment = self.deployments[deployment_id]
            deployment.status = DeploymentStatus.STOPPING
            
            # Simulate cleanup
            await asyncio.sleep(0.1)
            
            deployment.status = DeploymentStatus.STOPPED
            del self.deployments[deployment_id]
            
            logger.info(f"Deleted deployment {deployment_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete deployment {deployment_id}: {e}")
            return False
            
    async def get_deployment_metrics(self, deployment_id: str) -> Dict[str, Any]:
        """Get metrics for specific deployment"""
        if deployment_id not in self.deployments:
            return {}
            
        deployment = self.deployments[deployment_id]
        return deployment.metrics
        
    async def get_workload_analytics(self, workload_id: str) -> Dict[str, Any]:
        """Get analytics for workload across all deployments"""
        try:
            deployments = await self.get_workload_deployments(workload_id)
            
            if not deployments:
                return {}
                
            # Aggregate metrics
            total_requests = sum(d.metrics.get('requests_per_second', 0) for d in deployments)
            avg_response_time = sum(d.metrics.get('response_time_ms', 0) for d in deployments) / len(deployments)
            avg_error_rate = sum(d.metrics.get('error_rate', 0) for d in deployments) / len(deployments)
            
            analytics = {
                'workload_id': workload_id,
                'total_deployments': len(deployments),
                'active_deployments': len([d for d in deployments if d.status == DeploymentStatus.RUNNING]),
                'total_instances': sum(d.instances for d in deployments),
                'total_requests_per_second': total_requests,
                'average_response_time_ms': avg_response_time,
                'average_error_rate': avg_error_rate,
                'deployment_locations': [d.location_id for d in deployments],
                'health_status': 'healthy' if all(d.health_status == 'healthy' for d in deployments) else 'degraded'
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Failed to get workload analytics: {e}")
            return {}
            
    async def get_edge_status(self) -> Dict[str, Any]:
        """Get overall edge computing status"""
        try:
            total_locations = len(self.edge_locations)
            active_locations = len([loc for loc in self.edge_locations.values() if loc.enabled])
            total_workloads = len(self.workloads)
            total_deployments = len(self.deployments)
            active_deployments = len([d for d in self.deployments.values() if d.status == DeploymentStatus.RUNNING])
            
            # Calculate total capacity and utilization
            total_cpu_cores = sum(loc.capacity.get('cpu_cores', 0) for loc in self.edge_locations.values())
            total_memory_gb = sum(loc.capacity.get('memory_gb', 0) for loc in self.edge_locations.values())
            
            status = {
                'edge_locations': {
                    'total': total_locations,
                    'active': active_locations,
                    'providers': list(set(loc.provider.value for loc in self.edge_locations.values()))
                },
                'workloads': {
                    'total': total_workloads,
                    'types': list(set(w.workload_type.value for w in self.workloads.values()))
                },
                'deployments': {
                    'total': total_deployments,
                    'active': active_deployments,
                    'status_breakdown': self._get_deployment_status_breakdown()
                },
                'capacity': {
                    'total_cpu_cores': total_cpu_cores,
                    'total_memory_gb': total_memory_gb,
                    'average_utilization': self._calculate_average_utilization()
                },
                'performance': {
                    'average_response_time_ms': self._calculate_average_response_time(),
                    'total_requests_per_second': self._calculate_total_requests(),
                    'average_error_rate': self._calculate_average_error_rate()
                }
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to get edge status: {e}")
            return {}
            
    def _get_deployment_status_breakdown(self) -> Dict[str, int]:
        """Get breakdown of deployment statuses"""
        status_counts = {}
        for deployment in self.deployments.values():
            status = deployment.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        return status_counts
        
    def _calculate_average_utilization(self) -> float:
        """Calculate average resource utilization across locations"""
        if not self.edge_locations:
            return 0.0
            
        total_utilization = sum(
            loc.current_load.get('cpu', 0) for loc in self.edge_locations.values()
        )
        return total_utilization / len(self.edge_locations)
        
    def _calculate_average_response_time(self) -> float:
        """Calculate average response time across deployments"""
        if not self.deployments:
            return 0.0
            
        total_response_time = sum(
            d.metrics.get('response_time_ms', 0) for d in self.deployments.values()
        )
        return total_response_time / len(self.deployments)
        
    def _calculate_total_requests(self) -> float:
        """Calculate total requests per second across deployments"""
        return sum(
            d.metrics.get('requests_per_second', 0) for d in self.deployments.values()
        )
        
    def _calculate_average_error_rate(self) -> float:
        """Calculate average error rate across deployments"""
        if not self.deployments:
            return 0.0
            
        total_error_rate = sum(
            d.metrics.get('error_rate', 0) for d in self.deployments.values()
        )
        return total_error_rate / len(self.deployments)


# Example usage
async def example_edge_manager():
    """Example of using the edge manager"""
    
    # Create edge manager
    manager = EdgeManager()
    
    # Create a workload
    workload = EdgeWorkload(
        workload_id='web-app-001',
        name='E-commerce Web App',
        workload_type=WorkloadType.WEB_APPLICATION,
        application_id='ecommerce-app',
        image='nginx:latest',
        resource_requirements={
            'cpu_cores': 2,
            'memory_gb': 4,
            'storage_gb': 10
        },
        environment_variables={
            'NODE_ENV': 'production',
            'API_URL': 'https://api.example.com'
        }
    )
    
    # Create workload
    await manager.create_workload(workload)
    
    # Deploy to optimal locations
    deployment_ids = await manager.deploy_workload('web-app-001')
    print(f"Deployed to {len(deployment_ids)} locations: {deployment_ids}")
    
    # Get workload analytics
    analytics = await manager.get_workload_analytics('web-app-001')
    print(f"Workload analytics: {analytics}")
    
    # Scale a deployment
    if deployment_ids:
        await manager.scale_deployment(deployment_ids[0], 3)
        
    # Get edge status
    status = await manager.get_edge_status()
    print(f"Edge status: {status}")
    
    # Configure CDN
    await manager.cdn_integration.configure_cdn('cloudflare', {
        'api_key': 'your-api-key',
        'zone_id': 'your-zone-id'
    })
    
    # Create CDN distribution
    distribution_id = await manager.cdn_integration.create_distribution(
        'web-app-001',
        ['https://edge1.example.com', 'https://edge2.example.com'],
        {'cache_behaviors': {'default': {'ttl': 3600}}}
    )
    print(f"Created CDN distribution: {distribution_id}")


if __name__ == "__main__":
    asyncio.run(example_edge_manager())

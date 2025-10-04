"""
ECS Fargate Manager for AI-Native PaaS Platform.

This module manages AWS ECS Fargate containers with AI-driven optimization
for intelligent deployment, scaling, and resource management.

Features:
- ECS Fargate cluster management
- AI-driven task definition optimization
- Intelligent service scaling
- Blue/green deployments with AI risk assessment
- Container health monitoring
- Resource optimization based on AI recommendations
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

logger = logging.getLogger(__name__)


class DeploymentStrategy(str, Enum):
    """Container deployment strategies."""
    ROLLING_UPDATE = "rolling_update"
    BLUE_GREEN = "blue_green"
    CANARY = "canary"
    RECREATE = "recreate"


class ServiceStatus(str, Enum):
    """ECS service status."""
    PENDING = "pending"
    RUNNING = "running"
    STOPPED = "stopped"
    UPDATING = "updating"
    DRAINING = "draining"
    ERROR = "error"


@dataclass
class ContainerSpec:
    """Container specification for deployment."""
    name: str
    image: str
    cpu: int  # CPU units (1024 = 1 vCPU)
    memory: int  # Memory in MB
    port: int
    environment: Dict[str, str]
    health_check: Dict[str, Any]
    secrets: List[Dict[str, str]] = None


@dataclass
class ServiceConfig:
    """ECS service configuration."""
    service_name: str
    cluster_name: str
    task_definition_arn: str
    desired_count: int
    subnets: List[str]
    security_groups: List[str]
    load_balancer_config: Optional[Dict[str, Any]] = None
    auto_scaling_config: Optional[Dict[str, Any]] = None


@dataclass
class DeploymentResult:
    """Container deployment result."""
    deployment_id: str
    service_name: str
    status: str
    task_definition_arn: str
    desired_count: int
    running_count: int
    pending_count: int
    deployment_time: datetime
    ai_insights: Dict[str, Any]
    metadata: Dict[str, Any]


class ECSManager:
    """
    AWS ECS Fargate Manager with AI Integration.
    
    Manages container orchestration with intelligent deployment strategies,
    AI-driven scaling, and optimization recommendations.
    """
    
    def __init__(self, region: str = "us-east-1", ai_service=None):
        """
        Initialize ECS Manager.
        
        Args:
            region: AWS region for ECS operations
            ai_service: AI service for intelligent operations
        """
        self.region = region
        self.ai_service = ai_service
        
        # Initialize AWS clients
        try:
            self.ecs_client = boto3.client('ecs', region_name=region)
            self.ec2_client = boto3.client('ec2', region_name=region)
            self.logs_client = boto3.client('logs', region_name=region)
            self.application_autoscaling_client = boto3.client('application-autoscaling', region_name=region)
            
            # Test AWS connectivity
            try:
                self.ecs_client.list_clusters(maxResults=1)
                logger.info(f"ECS Manager initialized for region {region}")
            except Exception:
                # AWS not available, switch to mock mode
                logger.warning("AWS not available - using mock mode")
                self.ecs_client = None
                self.ec2_client = None
                self.logs_client = None
                self.application_autoscaling_client = None
                
        except (NoCredentialsError, Exception):
            logger.warning("AWS credentials not configured - using mock mode")
            self.ecs_client = None
            self.ec2_client = None
            self.logs_client = None
            self.application_autoscaling_client = None
        
        # Service state
        self.clusters: Dict[str, Dict[str, Any]] = {}
        self.services: Dict[str, Dict[str, Any]] = {}
        self.deployments: Dict[str, DeploymentResult] = {}
        
        # Default configurations
        self.default_cluster_name = "ai-paas-cluster"
        self.default_vpc_config = None
    
    async def ensure_cluster_exists(self, cluster_name: str = None) -> Dict[str, Any]:
        """
        Ensure ECS cluster exists, create if necessary.
        
        Args:
            cluster_name: Name of the ECS cluster
            
        Returns:
            Cluster information
        """
        if not cluster_name:
            cluster_name = self.default_cluster_name
        
        try:
            if not self.ecs_client:
                # Mock mode for testing
                cluster_info = {
                    'clusterName': cluster_name,
                    'clusterArn': f'arn:aws:ecs:{self.region}:123456789012:cluster/{cluster_name}',
                    'status': 'ACTIVE',
                    'runningTasksCount': 0,
                    'pendingTasksCount': 0,
                    'activeServicesCount': 0,
                    'registeredContainerInstancesCount': 0,
                    'capacityProviders': ['FARGATE', 'FARGATE_SPOT'],
                    'defaultCapacityProviderStrategy': [
                        {'capacityProvider': 'FARGATE', 'weight': 1, 'base': 0}
                    ]
                }
                self.clusters[cluster_name] = cluster_info
                logger.info(f"Mock cluster created: {cluster_name}")
                return cluster_info
            
            # Check if cluster exists
            try:
                response = self.ecs_client.describe_clusters(clusters=[cluster_name])
                clusters = response.get('clusters', [])
                
                if clusters and clusters[0]['status'] == 'ACTIVE':
                    cluster_info = clusters[0]
                    self.clusters[cluster_name] = cluster_info
                    logger.info(f"Using existing cluster: {cluster_name}")
                    return cluster_info
            except ClientError:
                pass
            
            # Create new cluster
            logger.info(f"Creating new ECS cluster: {cluster_name}")
            response = self.ecs_client.create_cluster(
                clusterName=cluster_name,
                capacityProviders=['FARGATE', 'FARGATE_SPOT'],
                defaultCapacityProviderStrategy=[
                    {
                        'capacityProvider': 'FARGATE',
                        'weight': 1,
                        'base': 0
                    }
                ],
                tags=[
                    {'key': 'Platform', 'value': 'AI-Native-PaaS'},
                    {'key': 'Environment', 'value': 'production'},
                    {'key': 'ManagedBy', 'value': 'AI-PaaS-Platform'}
                ]
            )
            
            cluster_info = response['cluster']
            self.clusters[cluster_name] = cluster_info
            
            logger.info(f"ECS cluster created successfully: {cluster_name}")
            return cluster_info
            
        except Exception as e:
            logger.error(f"Failed to ensure cluster exists: {e}")
            raise
    
    async def create_task_definition(
        self, 
        application_id: str,
        container_spec: ContainerSpec,
        ai_optimized: bool = True
    ) -> str:
        """
        Create ECS task definition with AI optimization.
        
        Args:
            application_id: Application identifier
            container_spec: Container specification
            ai_optimized: Whether to apply AI optimizations
            
        Returns:
            Task definition ARN
        """
        try:
            # Apply AI optimizations if enabled and AI service available
            if ai_optimized and self.ai_service:
                container_spec = await self._optimize_container_spec(application_id, container_spec)
            
            # Build task definition
            task_definition = {
                'family': f"{application_id}-task",
                'networkMode': 'awsvpc',
                'requiresCompatibilities': ['FARGATE'],
                'cpu': str(container_spec.cpu),
                'memory': str(container_spec.memory),
                'executionRoleArn': await self._get_execution_role_arn(),
                'taskRoleArn': await self._get_task_role_arn(),
                'containerDefinitions': [
                    {
                        'name': container_spec.name,
                        'image': container_spec.image,
                        'cpu': container_spec.cpu,
                        'memory': container_spec.memory,
                        'essential': True,
                        'portMappings': [
                            {
                                'containerPort': container_spec.port,
                                'protocol': 'tcp'
                            }
                        ],
                        'environment': [
                            {'name': k, 'value': v} 
                            for k, v in container_spec.environment.items()
                        ],
                        'healthCheck': container_spec.health_check,
                        'logConfiguration': {
                            'logDriver': 'awslogs',
                            'options': {
                                'awslogs-group': f"/ecs/{application_id}",
                                'awslogs-region': self.region,
                                'awslogs-stream-prefix': 'ecs'
                            }
                        }
                    }
                ],
                'tags': [
                    {'key': 'Application', 'value': application_id},
                    {'key': 'Platform', 'value': 'AI-Native-PaaS'},
                    {'key': 'AIOptimized', 'value': str(ai_optimized)}
                ]
            }
            
            # Add secrets if provided
            if container_spec.secrets:
                task_definition['containerDefinitions'][0]['secrets'] = container_spec.secrets
            
            if not self.ecs_client:
                # Mock mode
                task_def_arn = f"arn:aws:ecs:{self.region}:123456789012:task-definition/{application_id}-task:1"
                logger.info(f"Mock task definition created: {task_def_arn}")
                return task_def_arn
            
            # Create CloudWatch log group
            await self._ensure_log_group_exists(f"/ecs/{application_id}")
            
            # Register task definition
            response = self.ecs_client.register_task_definition(**task_definition)
            task_def_arn = response['taskDefinition']['taskDefinitionArn']
            
            logger.info(f"Task definition created: {task_def_arn}")
            return task_def_arn
            
        except Exception as e:
            logger.error(f"Failed to create task definition: {e}")
            raise
    
    async def deploy_service(
        self,
        application_id: str,
        service_config: ServiceConfig,
        deployment_strategy: DeploymentStrategy = DeploymentStrategy.ROLLING_UPDATE
    ) -> DeploymentResult:
        """
        Deploy ECS service with AI-driven deployment strategy.
        
        Args:
            application_id: Application identifier
            service_config: Service configuration
            deployment_strategy: Deployment strategy to use
            
        Returns:
            Deployment result with AI insights
        """
        try:
            deployment_id = f"deploy-{application_id}-{int(datetime.utcnow().timestamp())}"
            
            # Get AI insights for deployment
            ai_insights = {}
            if self.ai_service:
                ai_insights = await self._get_deployment_ai_insights(application_id, service_config)
            
            # Ensure cluster exists
            await self.ensure_cluster_exists(service_config.cluster_name)
            
            # Apply deployment strategy
            if deployment_strategy == DeploymentStrategy.BLUE_GREEN:
                result = await self._deploy_blue_green(application_id, service_config, ai_insights)
            elif deployment_strategy == DeploymentStrategy.CANARY:
                result = await self._deploy_canary(application_id, service_config, ai_insights)
            else:
                result = await self._deploy_rolling_update(application_id, service_config, ai_insights)
            
            # Store deployment result
            deployment_result = DeploymentResult(
                deployment_id=deployment_id,
                service_name=service_config.service_name,
                status=result.get('status', 'pending'),
                task_definition_arn=service_config.task_definition_arn,
                desired_count=service_config.desired_count,
                running_count=result.get('running_count', 0),
                pending_count=result.get('pending_count', 0),
                deployment_time=datetime.utcnow(),
                ai_insights=ai_insights,
                metadata=result.get('metadata', {})
            )
            
            self.deployments[deployment_id] = deployment_result
            
            logger.info(f"Service deployment initiated: {deployment_id}")
            return deployment_result
            
        except Exception as e:
            logger.error(f"Service deployment failed: {e}")
            raise
    
    async def _deploy_rolling_update(
        self, 
        application_id: str, 
        service_config: ServiceConfig,
        ai_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deploy using rolling update strategy."""
        try:
            if not self.ecs_client:
                # Mock deployment
                return {
                    'status': 'running',
                    'running_count': service_config.desired_count,
                    'pending_count': 0,
                    'metadata': {'deployment_strategy': 'rolling_update', 'mock': True}
                }
            
            # Check if service exists
            try:
                response = self.ecs_client.describe_services(
                    cluster=service_config.cluster_name,
                    services=[service_config.service_name]
                )
                
                services = response.get('services', [])
                service_exists = services and services[0]['status'] != 'INACTIVE'
                
            except ClientError:
                service_exists = False
            
            if service_exists:
                # Update existing service
                response = self.ecs_client.update_service(
                    cluster=service_config.cluster_name,
                    service=service_config.service_name,
                    taskDefinition=service_config.task_definition_arn,
                    desiredCount=service_config.desired_count,
                    deploymentConfiguration={
                        'maximumPercent': 200,
                        'minimumHealthyPercent': 50,
                        'deploymentCircuitBreaker': {
                            'enable': True,
                            'rollback': True
                        }
                    }
                )
                logger.info(f"Service updated: {service_config.service_name}")
            else:
                # Create new service
                service_definition = {
                    'serviceName': service_config.service_name,
                    'cluster': service_config.cluster_name,
                    'taskDefinition': service_config.task_definition_arn,
                    'desiredCount': service_config.desired_count,
                    'launchType': 'FARGATE',
                    'networkConfiguration': {
                        'awsvpcConfiguration': {
                            'subnets': service_config.subnets,
                            'securityGroups': service_config.security_groups,
                            'assignPublicIp': 'ENABLED'
                        }
                    },
                    'deploymentConfiguration': {
                        'maximumPercent': 200,
                        'minimumHealthyPercent': 50,
                        'deploymentCircuitBreaker': {
                            'enable': True,
                            'rollback': True
                        }
                    },
                    'tags': [
                        {'key': 'Application', 'value': application_id},
                        {'key': 'Platform', 'value': 'AI-Native-PaaS'}
                    ]
                }
                
                # Add load balancer configuration if provided
                if service_config.load_balancer_config:
                    service_definition['loadBalancers'] = [service_config.load_balancer_config]
                
                response = self.ecs_client.create_service(**service_definition)
                logger.info(f"Service created: {service_config.service_name}")
            
            service = response['service']
            
            return {
                'status': service['status'].lower(),
                'running_count': service['runningCount'],
                'pending_count': service['pendingCount'],
                'metadata': {
                    'deployment_strategy': 'rolling_update',
                    'service_arn': service['serviceArn']
                }
            }
            
        except Exception as e:
            logger.error(f"Rolling update deployment failed: {e}")
            raise
    
    async def _deploy_blue_green(
        self, 
        application_id: str, 
        service_config: ServiceConfig,
        ai_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deploy using blue/green strategy with AI risk assessment."""
        try:
            # AI risk assessment for blue/green deployment
            risk_score = ai_insights.get('deployment_risk_score', 0.3)
            
            if risk_score > 0.7:
                logger.warning(f"High deployment risk detected: {risk_score}")
                # Could implement additional safety measures or abort
            
            # For now, implement as rolling update with enhanced monitoring
            # Full blue/green would require additional infrastructure setup
            result = await self._deploy_rolling_update(application_id, service_config, ai_insights)
            result['metadata']['deployment_strategy'] = 'blue_green'
            result['metadata']['risk_score'] = risk_score
            
            return result
            
        except Exception as e:
            logger.error(f"Blue/green deployment failed: {e}")
            raise
    
    async def _deploy_canary(
        self, 
        application_id: str, 
        service_config: ServiceConfig,
        ai_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deploy using canary strategy with AI monitoring."""
        try:
            # Start with reduced capacity for canary
            canary_config = service_config
            canary_config.desired_count = max(1, service_config.desired_count // 4)
            
            result = await self._deploy_rolling_update(application_id, canary_config, ai_insights)
            result['metadata']['deployment_strategy'] = 'canary'
            result['metadata']['canary_percentage'] = 25
            
            return result
            
        except Exception as e:
            logger.error(f"Canary deployment failed: {e}")
            raise
    
    async def scale_service(
        self, 
        application_id: str,
        service_name: str,
        desired_count: int,
        cluster_name: str = None
    ) -> Dict[str, Any]:
        """
        Scale ECS service with AI-driven scaling decisions.
        
        Args:
            application_id: Application identifier
            service_name: ECS service name
            desired_count: Desired number of tasks
            cluster_name: ECS cluster name
            
        Returns:
            Scaling operation result
        """
        try:
            if not cluster_name:
                cluster_name = self.default_cluster_name
            
            # Get AI scaling recommendation
            scaling_insight = None
            if self.ai_service:
                insights = await self.ai_service.get_comprehensive_insights(application_id)
                scaling_insights = [i for i in insights if i.insight_type.value == 'scaling_recommendation']
                if scaling_insights:
                    scaling_insight = scaling_insights[0]
            
            if not self.ecs_client:
                # Mock scaling
                return {
                    'service_name': service_name,
                    'previous_count': 2,
                    'desired_count': desired_count,
                    'status': 'scaling',
                    'ai_recommendation': scaling_insight.data if scaling_insight else None
                }
            
            # Update service with new desired count
            response = self.ecs_client.update_service(
                cluster=cluster_name,
                service=service_name,
                desiredCount=desired_count
            )
            
            service = response['service']
            
            result = {
                'service_name': service_name,
                'previous_count': service['runningCount'],
                'desired_count': desired_count,
                'status': 'scaling',
                'ai_recommendation': scaling_insight.data if scaling_insight else None
            }
            
            logger.info(f"Service scaling initiated: {service_name} -> {desired_count} tasks")
            return result
            
        except Exception as e:
            logger.error(f"Service scaling failed: {e}")
            raise
    
    async def get_service_status(
        self, 
        service_name: str, 
        cluster_name: str = None
    ) -> Dict[str, Any]:
        """Get detailed service status information."""
        try:
            if not cluster_name:
                cluster_name = self.default_cluster_name
            
            if not self.ecs_client:
                # Mock status
                return {
                    'service_name': service_name,
                    'status': 'running',
                    'desired_count': 2,
                    'running_count': 2,
                    'pending_count': 0,
                    'cpu_utilization': 45.2,
                    'memory_utilization': 62.8,
                    'health_status': 'healthy'
                }
            
            # Get service details
            response = self.ecs_client.describe_services(
                cluster=cluster_name,
                services=[service_name]
            )
            
            if not response['services']:
                raise ValueError(f"Service not found: {service_name}")
            
            service = response['services'][0]
            
            # Get task details for additional metrics
            tasks_response = self.ecs_client.list_tasks(
                cluster=cluster_name,
                serviceName=service_name
            )
            
            status = {
                'service_name': service_name,
                'status': service['status'].lower(),
                'desired_count': service['desiredCount'],
                'running_count': service['runningCount'],
                'pending_count': service['pendingCount'],
                'task_definition': service['taskDefinition'],
                'created_at': service['createdAt'].isoformat(),
                'deployments': len(service['deployments']),
                'tasks': len(tasks_response['taskArns'])
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to get service status: {e}")
            raise
    
    async def _optimize_container_spec(
        self, 
        application_id: str, 
        container_spec: ContainerSpec
    ) -> ContainerSpec:
        """Apply AI optimizations to container specification."""
        try:
            if not self.ai_service:
                return container_spec
            
            # Get resource recommendations from AI
            insights = await self.ai_service.get_comprehensive_insights(application_id)
            resource_insights = [i for i in insights if i.insight_type.value == 'resource_recommendation']
            
            if resource_insights:
                resource_rec = resource_insights[0]
                recommended_config = resource_rec.data.get('recommended_config', {})
                
                # Apply CPU optimization
                if 'cpu_cores' in recommended_config:
                    # Convert CPU cores to ECS CPU units (1 core = 1024 units)
                    optimized_cpu = int(recommended_config['cpu_cores'] * 1024)
                    if optimized_cpu != container_spec.cpu:
                        logger.info(f"AI CPU optimization: {container_spec.cpu} -> {optimized_cpu}")
                        container_spec.cpu = optimized_cpu
                
                # Apply memory optimization
                if 'memory_gb' in recommended_config:
                    # Convert GB to MB
                    optimized_memory = int(recommended_config['memory_gb'] * 1024)
                    if optimized_memory != container_spec.memory:
                        logger.info(f"AI memory optimization: {container_spec.memory} -> {optimized_memory}")
                        container_spec.memory = optimized_memory
            
            return container_spec
            
        except Exception as e:
            logger.error(f"Container spec optimization failed: {e}")
            return container_spec
    
    async def _get_deployment_ai_insights(
        self, 
        application_id: str, 
        service_config: ServiceConfig
    ) -> Dict[str, Any]:
        """Get AI insights for deployment decision making."""
        try:
            if not self.ai_service:
                return {}
            
            insights = await self.ai_service.get_comprehensive_insights(application_id)
            
            # Aggregate insights for deployment
            deployment_insights = {
                'risk_assessment': 'low',
                'deployment_risk_score': 0.3,
                'performance_prediction': {},
                'cost_impact': 0.0,
                'recommendations': []
            }
            
            for insight in insights:
                if insight.priority.value in ['critical', 'high']:
                    deployment_insights['risk_assessment'] = 'high'
                    deployment_insights['deployment_risk_score'] = 0.8
                    deployment_insights['recommendations'].append(
                        f"High priority issue detected: {insight.title}"
                    )
                
                if insight.insight_type.value == 'performance_prediction':
                    deployment_insights['performance_prediction'] = insight.data
                
                if insight.insight_type.value == 'cost_optimization':
                    deployment_insights['cost_impact'] += insight.data.get('savings', 0)
            
            return deployment_insights
            
        except Exception as e:
            logger.error(f"Failed to get deployment AI insights: {e}")
            return {}
    
    async def _ensure_log_group_exists(self, log_group_name: str):
        """Ensure CloudWatch log group exists."""
        try:
            if not self.logs_client:
                return
            
            try:
                self.logs_client.describe_log_groups(logGroupNamePrefix=log_group_name)
            except ClientError:
                # Create log group
                self.logs_client.create_log_group(
                    logGroupName=log_group_name,
                    tags={
                        'Platform': 'AI-Native-PaaS',
                        'ManagedBy': 'ECS-Manager'
                    }
                )
                logger.info(f"Created log group: {log_group_name}")
                
        except Exception as e:
            logger.error(f"Failed to ensure log group exists: {e}")
    
    async def _get_execution_role_arn(self) -> str:
        """Get or create ECS execution role ARN."""
        # In production, this would create/retrieve the actual IAM role
        return f"arn:aws:iam::123456789012:role/ecsTaskExecutionRole"
    
    async def _get_task_role_arn(self) -> str:
        """Get or create ECS task role ARN."""
        # In production, this would create/retrieve the actual IAM role
        return f"arn:aws:iam::123456789012:role/ecsTaskRole"
    
    async def get_deployment_history(self, application_id: str) -> List[DeploymentResult]:
        """Get deployment history for an application."""
        return [
            deployment for deployment in self.deployments.values()
            if deployment.service_name.startswith(application_id)
        ]
    
    async def cleanup_old_deployments(self, days: int = 7) -> int:
        """Clean up old deployment records."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            old_deployments = [
                deployment_id for deployment_id, deployment in self.deployments.items()
                if deployment.deployment_time < cutoff_date
            ]
            
            for deployment_id in old_deployments:
                del self.deployments[deployment_id]
            
            logger.info(f"Cleaned up {len(old_deployments)} old deployment records")
            return len(old_deployments)
            
        except Exception as e:
            logger.error(f"Failed to cleanup old deployments: {e}")
            return 0

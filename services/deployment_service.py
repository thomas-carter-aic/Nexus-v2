"""
AI-Powered Deployment Service

This module implements intelligent application deployment with AI-driven
optimization, blue/green deployments, automated rollback, and comprehensive
monitoring integration.

Key Features:
- Blue/green deployment strategy for zero-downtime deployments
- AI-driven deployment optimization and risk assessment
- Automated rollback on failure detection
- Integration with monitoring and alerting systems
- Container image management and versioning
- Configuration management and secrets handling
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import boto3
from botocore.exceptions import ClientError

from ..core.domain.models import Application, ApplicationId, ApplicationStatus
from ..core.application.services import EventStore
from ..infrastructure.aws_services import InfrastructureError


# Configure logging for deployment service
logger = logging.getLogger(__name__)


class DeploymentStrategy(Enum):
    """Supported deployment strategies"""
    BLUE_GREEN = "blue_green"
    ROLLING = "rolling"
    CANARY = "canary"
    RECREATE = "recreate"


class DeploymentStatus(Enum):
    """Deployment operation status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class DeploymentRisk(Enum):
    """AI-assessed deployment risk levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DeploymentService:
    """
    Intelligent deployment service that manages application deployments
    with AI-driven optimization and automated risk management.
    """
    
    def __init__(self,
                 ecs_client: Optional[boto3.client] = None,
                 ecr_client: Optional[boto3.client] = None,
                 cloudwatch_client: Optional[boto3.client] = None,
                 sagemaker_client: Optional[boto3.client] = None,
                 event_store: Optional[EventStore] = None,
                 region_name: str = 'us-east-1'):
        """
        Initialize the deployment service with AWS clients and dependencies.
        
        Args:
            ecs_client: AWS ECS client for container orchestration
            ecr_client: AWS ECR client for container registry operations
            cloudwatch_client: AWS CloudWatch client for monitoring
            sagemaker_client: AWS SageMaker client for AI predictions
            event_store: Event store for publishing deployment events
            region_name: AWS region name
        """
        self._ecs = ecs_client or boto3.client('ecs', region_name=region_name)
        self._ecr = ecr_client or boto3.client('ecr', region_name=region_name)
        self._cloudwatch = cloudwatch_client or boto3.client('cloudwatch', region_name=region_name)
        self._sagemaker = sagemaker_client or boto3.client('sagemaker', region_name=region_name)
        self._event_store = event_store
        self._region_name = region_name
        
        # Deployment configuration
        self._cluster_name = 'paas-cluster'
        self._default_strategy = DeploymentStrategy.BLUE_GREEN
        self._health_check_timeout_seconds = 300  # 5 minutes
        self._rollback_threshold_error_rate = 5.0  # 5% error rate triggers rollback
        self._ai_risk_model_name = 'paas-deployment-risk-predictor'
        
        # Deployment tracking
        self._active_deployments: Dict[str, Dict[str, Any]] = {}
    
    async def deploy_application(self,
                               application: Application,
                               container_image: str,
                               environment_variables: Optional[Dict[str, str]] = None,
                               deployment_strategy: Optional[DeploymentStrategy] = None) -> str:
        """
        Deploy an application using intelligent deployment strategies.
        
        Args:
            application: Application aggregate to deploy
            container_image: Container image URI to deploy
            environment_variables: Optional environment variables for the application
            deployment_strategy: Optional deployment strategy (defaults to blue/green)
            
        Returns:
            Deployment ID for tracking the deployment progress
        """
        deployment_id = f"deploy-{application.id.value}-{int(datetime.utcnow().timestamp())}"
        strategy = deployment_strategy or self._default_strategy
        
        logger.info(f"Starting deployment {deployment_id} for application {application.id.value} "
                   f"using {strategy.value} strategy")
        
        try:
            # Assess deployment risk using AI
            risk_assessment = await self._assess_deployment_risk(
                application=application,
                container_image=container_image,
                strategy=strategy
            )
            
            logger.info(f"Deployment risk assessment: {risk_assessment['risk_level']} "
                       f"(confidence: {risk_assessment['confidence']:.2f})")
            
            # Initialize deployment tracking
            deployment_info = {
                'deployment_id': deployment_id,
                'application_id': str(application.id.value),
                'strategy': strategy.value,
                'status': DeploymentStatus.PENDING.value,
                'risk_assessment': risk_assessment,
                'container_image': container_image,
                'environment_variables': environment_variables or {},
                'started_at': datetime.utcnow().isoformat(),
                'health_checks': [],
                'metrics': {}
            }
            
            self._active_deployments[deployment_id] = deployment_info
            
            # Execute deployment based on strategy
            if strategy == DeploymentStrategy.BLUE_GREEN:
                await self._execute_blue_green_deployment(deployment_id, application, container_image, environment_variables)
            elif strategy == DeploymentStrategy.ROLLING:
                await self._execute_rolling_deployment(deployment_id, application, container_image, environment_variables)
            elif strategy == DeploymentStrategy.CANARY:
                await self._execute_canary_deployment(deployment_id, application, container_image, environment_variables)
            else:
                await self._execute_recreate_deployment(deployment_id, application, container_image, environment_variables)
            
            return deployment_id
            
        except Exception as e:
            logger.error(f"Deployment {deployment_id} failed: {str(e)}")
            await self._handle_deployment_failure(deployment_id, str(e))
            raise DeploymentError(f"Deployment failed: {str(e)}")
    
    async def get_deployment_status(self, deployment_id: str) -> Dict[str, Any]:
        """
        Get the current status of a deployment.
        
        Args:
            deployment_id: Unique identifier of the deployment
            
        Returns:
            Dictionary containing deployment status and details
        """
        if deployment_id not in self._active_deployments:
            raise ValueError(f"Deployment {deployment_id} not found")
        
        deployment_info = self._active_deployments[deployment_id]
        
        # Update with latest metrics if deployment is in progress
        if deployment_info['status'] == DeploymentStatus.IN_PROGRESS.value:
            await self._update_deployment_metrics(deployment_id)
        
        return deployment_info.copy()
    
    async def rollback_deployment(self, deployment_id: str, reason: str = "Manual rollback") -> bool:
        """
        Rollback a deployment to the previous version.
        
        Args:
            deployment_id: Unique identifier of the deployment to rollback
            reason: Reason for the rollback
            
        Returns:
            True if rollback was successful, False otherwise
        """
        logger.info(f"Initiating rollback for deployment {deployment_id}: {reason}")
        
        if deployment_id not in self._active_deployments:
            raise ValueError(f"Deployment {deployment_id} not found")
        
        deployment_info = self._active_deployments[deployment_id]
        
        try:
            # Execute rollback based on original deployment strategy
            strategy = DeploymentStrategy(deployment_info['strategy'])
            application_id = deployment_info['application_id']
            
            if strategy == DeploymentStrategy.BLUE_GREEN:
                success = await self._rollback_blue_green_deployment(deployment_id)
            elif strategy == DeploymentStrategy.ROLLING:
                success = await self._rollback_rolling_deployment(deployment_id)
            elif strategy == DeploymentStrategy.CANARY:
                success = await self._rollback_canary_deployment(deployment_id)
            else:
                success = await self._rollback_recreate_deployment(deployment_id)
            
            if success:
                deployment_info['status'] = DeploymentStatus.ROLLED_BACK.value
                deployment_info['rollback_reason'] = reason
                deployment_info['rolled_back_at'] = datetime.utcnow().isoformat()
                
                logger.info(f"Successfully rolled back deployment {deployment_id}")
            else:
                logger.error(f"Failed to rollback deployment {deployment_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error during rollback of deployment {deployment_id}: {str(e)}")
            return False
    
    async def _assess_deployment_risk(self,
                                    application: Application,
                                    container_image: str,
                                    strategy: DeploymentStrategy) -> Dict[str, Any]:
        """
        Use AI to assess the risk of a deployment based on multiple factors.
        
        Args:
            application: Application being deployed
            container_image: Container image being deployed
            strategy: Deployment strategy being used
            
        Returns:
            Risk assessment with risk level and confidence score
        """
        try:
            # Gather deployment context for risk assessment
            deployment_context = await self._gather_deployment_context(application, container_image)
            
            # Prepare feature vector for AI model
            risk_features = {
                'application_age_days': (datetime.utcnow() - application.created_at).days,
                'current_instance_count': application.current_instance_count,
                'deployment_strategy': strategy.value,
                'resource_cpu_cores': application.resource_requirements.cpu_cores,
                'resource_memory_mb': application.resource_requirements.memory_mb,
                'recent_deployment_count': deployment_context['recent_deployments'],
                'recent_error_rate': deployment_context['recent_error_rate'],
                'traffic_volume': deployment_context['traffic_volume'],
                'time_since_last_deployment_hours': deployment_context['hours_since_last_deployment'],
                'container_image_size_mb': deployment_context.get('image_size_mb', 0),
                'has_database_dependencies': deployment_context.get('has_database', False),
                'has_external_dependencies': deployment_context.get('has_external_deps', False)
            }
            
            # Invoke AI risk assessment model
            input_data = json.dumps({'instances': [risk_features]})
            
            response = self._sagemaker.invoke_endpoint(
                EndpointName=self._ai_risk_model_name,
                ContentType='application/json',
                Body=input_data
            )
            
            result = json.loads(response['Body'].read().decode())
            
            risk_level = DeploymentRisk(result.get('risk_level', 'medium'))
            confidence = float(result.get('confidence', 0.5))
            risk_factors = result.get('risk_factors', [])
            
            return {
                'risk_level': risk_level.value,
                'confidence': confidence,
                'risk_factors': risk_factors,
                'assessment_timestamp': datetime.utcnow().isoformat(),
                'model_version': result.get('model_version', 'unknown')
            }
            
        except Exception as e:
            logger.warning(f"AI risk assessment failed, using fallback: {str(e)}")
            return self._get_fallback_risk_assessment(application, strategy)
    
    async def _execute_blue_green_deployment(self,
                                           deployment_id: str,
                                           application: Application,
                                           container_image: str,
                                           environment_variables: Dict[str, str]) -> None:
        """
        Execute blue/green deployment strategy for zero-downtime deployment.
        
        Args:
            deployment_id: Unique deployment identifier
            application: Application to deploy
            container_image: Container image to deploy
            environment_variables: Environment variables for the application
        """
        deployment_info = self._active_deployments[deployment_id]
        deployment_info['status'] = DeploymentStatus.IN_PROGRESS.value
        
        logger.info(f"Executing blue/green deployment {deployment_id}")
        
        try:
            service_name = f"app-{application.id.value}"
            green_service_name = f"{service_name}-green"
            
            # Step 1: Create green environment with new version
            await self._create_green_environment(
                deployment_id=deployment_id,
                application=application,
                service_name=green_service_name,
                container_image=container_image,
                environment_variables=environment_variables
            )
            
            # Step 2: Wait for green environment to be healthy
            green_healthy = await self._wait_for_service_health(
                service_name=green_service_name,
                timeout_seconds=self._health_check_timeout_seconds
            )
            
            if not green_healthy:
                raise DeploymentError("Green environment failed health checks")
            
            # Step 3: Perform traffic switch from blue to green
            await self._switch_traffic_to_green(
                deployment_id=deployment_id,
                blue_service=service_name,
                green_service=green_service_name
            )
            
            # Step 4: Monitor green environment for stability
            stability_check = await self._monitor_deployment_stability(
                deployment_id=deployment_id,
                service_name=green_service_name,
                duration_minutes=5
            )
            
            if not stability_check['stable']:
                logger.warning(f"Green environment unstable: {stability_check['reason']}")
                await self._rollback_blue_green_deployment(deployment_id)
                raise DeploymentError(f"Deployment unstable: {stability_check['reason']}")
            
            # Step 5: Clean up blue environment
            await self._cleanup_blue_environment(deployment_id, service_name)
            
            # Mark deployment as completed
            deployment_info['status'] = DeploymentStatus.COMPLETED.value
            deployment_info['completed_at'] = datetime.utcnow().isoformat()
            
            logger.info(f"Blue/green deployment {deployment_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Blue/green deployment {deployment_id} failed: {str(e)}")
            await self._handle_deployment_failure(deployment_id, str(e))
            raise
    
    async def _create_green_environment(self,
                                      deployment_id: str,
                                      application: Application,
                                      service_name: str,
                                      container_image: str,
                                      environment_variables: Dict[str, str]) -> None:
        """
        Create the green environment for blue/green deployment.
        
        Args:
            deployment_id: Deployment identifier
            application: Application being deployed
            service_name: Name of the green service
            container_image: Container image to deploy
            environment_variables: Environment variables
        """
        logger.debug(f"Creating green environment {service_name} for deployment {deployment_id}")
        
        try:
            # Create task definition for the new version
            task_definition = await self._create_task_definition(
                application=application,
                container_image=container_image,
                environment_variables=environment_variables,
                task_family=f"{service_name}-task"
            )
            
            # Create ECS service for green environment
            service_response = self._ecs.create_service(
                cluster=self._cluster_name,
                serviceName=service_name,
                taskDefinition=task_definition['taskDefinitionArn'],
                desiredCount=application.current_instance_count,
                launchType='FARGATE',
                networkConfiguration={
                    'awsvpcConfiguration': {
                        'subnets': await self._get_private_subnets(),
                        'securityGroups': await self._get_security_groups(),
                        'assignPublicIp': 'DISABLED'
                    }
                },
                loadBalancers=[
                    {
                        'targetGroupArn': await self._get_target_group_arn(application.id.value),
                        'containerName': f"app-{application.id.value}",
                        'containerPort': 8080
                    }
                ],
                healthCheckGracePeriodSeconds=60,
                tags=[
                    {'key': 'DeploymentId', 'value': deployment_id},
                    {'key': 'Environment', 'value': 'green'},
                    {'key': 'ApplicationId', 'value': str(application.id.value)}
                ]
            )
            
            # Update deployment info
            deployment_info = self._active_deployments[deployment_id]
            deployment_info['green_service_arn'] = service_response['service']['serviceArn']
            deployment_info['task_definition_arn'] = task_definition['taskDefinitionArn']
            
            logger.info(f"Green environment {service_name} created successfully")
            
        except ClientError as e:
            logger.error(f"Failed to create green environment: {str(e)}")
            raise DeploymentError(f"Failed to create green environment: {str(e)}")
    
    async def _wait_for_service_health(self, service_name: str, timeout_seconds: int) -> bool:
        """
        Wait for ECS service to become healthy.
        
        Args:
            service_name: Name of the ECS service
            timeout_seconds: Maximum time to wait for health
            
        Returns:
            True if service becomes healthy, False if timeout
        """
        logger.debug(f"Waiting for service {service_name} to become healthy")
        
        start_time = datetime.utcnow()
        timeout_time = start_time + timedelta(seconds=timeout_seconds)
        
        while datetime.utcnow() < timeout_time:
            try:
                # Check service status
                response = self._ecs.describe_services(
                    cluster=self._cluster_name,
                    services=[service_name]
                )
                
                services = response.get('services', [])
                if not services:
                    logger.warning(f"Service {service_name} not found")
                    await asyncio.sleep(10)
                    continue
                
                service = services[0]
                running_count = service.get('runningCount', 0)
                desired_count = service.get('desiredCount', 0)
                
                # Check if all tasks are running and healthy
                if running_count == desired_count and desired_count > 0:
                    # Additional health check through load balancer
                    if await self._check_load_balancer_health(service_name):
                        logger.info(f"Service {service_name} is healthy")
                        return True
                
                logger.debug(f"Service {service_name} health: {running_count}/{desired_count} tasks running")
                await asyncio.sleep(10)
                
            except ClientError as e:
                logger.warning(f"Error checking service health: {str(e)}")
                await asyncio.sleep(10)
        
        logger.warning(f"Service {service_name} failed to become healthy within {timeout_seconds} seconds")
        return False
    
    async def _monitor_deployment_stability(self,
                                          deployment_id: str,
                                          service_name: str,
                                          duration_minutes: int) -> Dict[str, Any]:
        """
        Monitor deployment stability after traffic switch.
        
        Args:
            deployment_id: Deployment identifier
            service_name: Name of the service to monitor
            duration_minutes: Duration to monitor in minutes
            
        Returns:
            Dictionary with stability assessment
        """
        logger.info(f"Monitoring stability for deployment {deployment_id} for {duration_minutes} minutes")
        
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        stability_metrics = {
            'error_rates': [],
            'response_times': [],
            'cpu_utilization': [],
            'memory_utilization': []
        }
        
        while datetime.utcnow() < end_time:
            try:
                # Collect metrics from CloudWatch
                metrics = await self._collect_service_metrics(service_name)
                
                stability_metrics['error_rates'].append(metrics.get('error_rate', 0.0))
                stability_metrics['response_times'].append(metrics.get('response_time', 0.0))
                stability_metrics['cpu_utilization'].append(metrics.get('cpu_utilization', 0.0))
                stability_metrics['memory_utilization'].append(metrics.get('memory_utilization', 0.0))
                
                # Check for immediate stability issues
                if metrics.get('error_rate', 0.0) > self._rollback_threshold_error_rate:
                    return {
                        'stable': False,
                        'reason': f"High error rate: {metrics['error_rate']:.2f}%",
                        'metrics': stability_metrics
                    }
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.warning(f"Error collecting stability metrics: {str(e)}")
                await asyncio.sleep(30)
        
        # Analyze overall stability
        avg_error_rate = sum(stability_metrics['error_rates']) / len(stability_metrics['error_rates']) if stability_metrics['error_rates'] else 0.0
        
        is_stable = avg_error_rate < self._rollback_threshold_error_rate
        
        return {
            'stable': is_stable,
            'reason': f"Average error rate: {avg_error_rate:.2f}%" if not is_stable else "Deployment stable",
            'metrics': stability_metrics,
            'average_error_rate': avg_error_rate
        }
    
    async def _gather_deployment_context(self, application: Application, container_image: str) -> Dict[str, Any]:
        """
        Gather contextual information for deployment risk assessment.
        
        Args:
            application: Application being deployed
            container_image: Container image being deployed
            
        Returns:
            Dictionary with deployment context information
        """
        context = {
            'recent_deployments': 0,
            'recent_error_rate': 0.0,
            'traffic_volume': 0.0,
            'hours_since_last_deployment': 24.0,  # Default to 24 hours
            'image_size_mb': 0,
            'has_database': False,
            'has_external_deps': False
        }
        
        try:
            # Get recent deployment history (last 7 days)
            # This would query deployment history from database/event store
            # For now, using placeholder values
            
            # Get recent error rates from CloudWatch
            error_metrics = await self._get_recent_error_metrics(application.id.value)
            context['recent_error_rate'] = error_metrics.get('average_error_rate', 0.0)
            
            # Get traffic volume
            traffic_metrics = await self._get_traffic_metrics(application.id.value)
            context['traffic_volume'] = traffic_metrics.get('requests_per_minute', 0.0)
            
            # Get container image information
            image_info = await self._get_container_image_info(container_image)
            context['image_size_mb'] = image_info.get('size_mb', 0)
            
            return context
            
        except Exception as e:
            logger.warning(f"Error gathering deployment context: {str(e)}")
            return context
    
    def _get_fallback_risk_assessment(self, application: Application, strategy: DeploymentStrategy) -> Dict[str, Any]:
        """
        Provide fallback risk assessment when AI model is unavailable.
        
        Args:
            application: Application being deployed
            strategy: Deployment strategy
            
        Returns:
            Fallback risk assessment
        """
        # Simple rule-based risk assessment
        risk_level = DeploymentRisk.MEDIUM
        risk_factors = []
        
        # Higher risk for larger applications
        if application.current_instance_count > 10:
            risk_level = DeploymentRisk.HIGH
            risk_factors.append("Large scale deployment")
        
        # Lower risk for blue/green deployments
        if strategy == DeploymentStrategy.BLUE_GREEN:
            if risk_level == DeploymentRisk.HIGH:
                risk_level = DeploymentRisk.MEDIUM
            risk_factors.append("Blue/green strategy reduces risk")
        
        return {
            'risk_level': risk_level.value,
            'confidence': 0.6,  # Lower confidence for rule-based assessment
            'risk_factors': risk_factors,
            'assessment_timestamp': datetime.utcnow().isoformat(),
            'model_version': 'fallback-rules-v1'
        }
    
    async def _handle_deployment_failure(self, deployment_id: str, error_message: str) -> None:
        """
        Handle deployment failure by updating status and triggering cleanup.
        
        Args:
            deployment_id: Failed deployment identifier
            error_message: Error message describing the failure
        """
        if deployment_id in self._active_deployments:
            deployment_info = self._active_deployments[deployment_id]
            deployment_info['status'] = DeploymentStatus.FAILED.value
            deployment_info['error_message'] = error_message
            deployment_info['failed_at'] = datetime.utcnow().isoformat()
            
            # Attempt cleanup of any created resources
            await self._cleanup_failed_deployment(deployment_id)
    
    # Placeholder methods for other deployment strategies and helper functions
    async def _execute_rolling_deployment(self, deployment_id: str, application: Application, container_image: str, environment_variables: Dict[str, str]) -> None:
        """Placeholder for rolling deployment implementation"""
        raise NotImplementedError("Rolling deployment not yet implemented")
    
    async def _execute_canary_deployment(self, deployment_id: str, application: Application, container_image: str, environment_variables: Dict[str, str]) -> None:
        """Placeholder for canary deployment implementation"""
        raise NotImplementedError("Canary deployment not yet implemented")
    
    async def _execute_recreate_deployment(self, deployment_id: str, application: Application, container_image: str, environment_variables: Dict[str, str]) -> None:
        """Placeholder for recreate deployment implementation"""
        raise NotImplementedError("Recreate deployment not yet implemented")


class DeploymentError(Exception):
    """Exception raised when deployment operations fail"""
    pass

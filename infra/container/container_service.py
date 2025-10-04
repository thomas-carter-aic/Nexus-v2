"""
Container Service for AI-Native PaaS Platform.

This module provides a high-level container management interface that
integrates ECS management with AI-driven optimization and monitoring.

Features:
- Application container lifecycle management
- AI-driven deployment strategies
- Intelligent scaling and optimization
- Health monitoring and auto-recovery
- Cost optimization integration
- Performance monitoring
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import json

from .ecs_manager import ECSManager, ContainerSpec, ServiceConfig, DeploymentStrategy, DeploymentResult

logger = logging.getLogger(__name__)


class ContainerHealth(str, Enum):
    """Container health status."""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    STARTING = "starting"
    UNKNOWN = "unknown"


@dataclass
class ApplicationContainer:
    """Application container configuration."""
    application_id: str
    name: str
    image: str
    version: str
    cpu_cores: float
    memory_gb: float
    port: int
    environment_variables: Dict[str, str]
    health_check_path: str = "/health"
    replicas: int = 1
    auto_scaling: bool = True


@dataclass
class ContainerMetrics:
    """Container performance metrics."""
    application_id: str
    cpu_utilization: float
    memory_utilization: float
    network_in: float
    network_out: float
    request_count: int
    response_time: float
    error_rate: float
    timestamp: datetime


@dataclass
class ScalingEvent:
    """Container scaling event."""
    application_id: str
    event_type: str  # scale_up, scale_down, auto_scale
    previous_count: int
    new_count: int
    reason: str
    timestamp: datetime
    ai_triggered: bool = False


class ContainerService:
    """
    High-level container management service with AI integration.
    
    Provides application-focused container operations with intelligent
    optimization, monitoring, and management capabilities.
    """
    
    def __init__(self, region: str = "us-east-1", ai_service=None):
        """
        Initialize Container Service.
        
        Args:
            region: AWS region for container operations
            ai_service: AI service for intelligent operations
        """
        self.region = region
        self.ai_service = ai_service
        self.ecs_manager = ECSManager(region, ai_service)
        
        # Service state
        self.applications: Dict[str, ApplicationContainer] = {}
        self.metrics_history: Dict[str, List[ContainerMetrics]] = {}
        self.scaling_events: Dict[str, List[ScalingEvent]] = {}
        self.health_status: Dict[str, ContainerHealth] = {}
        
        # Configuration
        self.default_cluster = "ai-paas-cluster"
        self.monitoring_interval = 60  # seconds
        self.auto_scaling_enabled = True
        
        logger.info("Container Service initialized")
    
    async def deploy_application(
        self, 
        app_container: ApplicationContainer,
        deployment_strategy: DeploymentStrategy = DeploymentStrategy.ROLLING_UPDATE,
        ai_optimized: bool = True
    ) -> Any:
        """
        Deploy application container with AI optimization.
        
        Args:
            app_container: Application container configuration
            deployment_strategy: Deployment strategy to use
            ai_optimized: Whether to apply AI optimizations
            
        Returns:
            Deployment object with status and details
        """
        try:
            logger.info(f"Deploying application: {app_container.application_id}")
            
            # Store application configuration
            self.applications[app_container.application_id] = app_container
            
            # Apply AI optimizations if enabled
            if ai_optimized and self.ai_service:
                app_container = await self._apply_ai_optimizations(app_container)
            
            # Create container specification
            container_spec = ContainerSpec(
                name=app_container.name,
                image=f"{app_container.image}:{app_container.version}",
                cpu=int(app_container.cpu_cores * 1024),  # Convert to ECS CPU units
                memory=int(app_container.memory_gb * 1024),  # Convert to MB
                port=app_container.port,
                environment=app_container.environment_variables,
                health_check={
                    'command': [
                        'CMD-SHELL',
                        f'curl -f http://localhost:{app_container.port}{app_container.health_check_path} || exit 1'
                    ],
                    'interval': 30,
                    'timeout': 5,
                    'retries': 3,
                    'startPeriod': 60
                }
            )
            
            # Create task definition
            task_def_arn = await self.ecs_manager.create_task_definition(
                app_container.application_id,
                container_spec,
                ai_optimized
            )
            
            # Configure service
            service_config = ServiceConfig(
                service_name=f"{app_container.application_id}-service",
                cluster_name=self.default_cluster,
                task_definition_arn=task_def_arn,
                desired_count=app_container.replicas,
                subnets=await self._get_default_subnets(),
                security_groups=await self._get_default_security_groups(),
                auto_scaling_config={
                    'enabled': app_container.auto_scaling,
                    'min_capacity': 1,
                    'max_capacity': max(10, app_container.replicas * 3),
                    'target_cpu_utilization': 70.0,
                    'target_memory_utilization': 80.0
                } if app_container.auto_scaling else None
            )
            
            # Deploy service
            deployment_result = await self.ecs_manager.deploy_service(
                app_container.application_id,
                service_config,
                deployment_strategy
            )
            
            # Create deployment object
            from datetime import datetime
            
            # Simple deployment object for testing
            class SimpleDeployment:
                def __init__(self, deployment_id, application_id, version):
                    self.id = deployment_id
                    self.application_id = application_id
                    self.version = version
                    self.status = "in_progress"
                    self.strategy = deployment_strategy.value
                    self.progress = 25
                    self.logs = [f"Deployment initiated with strategy: {deployment_strategy.value}"]
                    self.created_at = deployment_result.deployment_time
            
            deployment = SimpleDeployment(
                deployment_result.deployment_id,
                app_container.application_id,
                app_container.version
            )
            
            # Initialize health monitoring
            self.health_status[app_container.application_id] = ContainerHealth.STARTING
            
            # Start monitoring task
            asyncio.create_task(self._monitor_application(app_container.application_id))
            
            logger.info(f"Application deployment initiated: {deployment.id}")
            return deployment
            
        except Exception as e:
            logger.error(f"Application deployment failed: {e}")
            raise
    
    async def scale_application(
        self, 
        application_id: str, 
        target_replicas: int,
        reason: str = "manual"
    ) -> ScalingEvent:
        """
        Scale application containers.
        
        Args:
            application_id: Application identifier
            target_replicas: Target number of replicas
            reason: Reason for scaling
            
        Returns:
            Scaling event details
        """
        try:
            if application_id not in self.applications:
                raise ValueError(f"Application not found: {application_id}")
            
            app_container = self.applications[application_id]
            previous_count = app_container.replicas
            
            # Update application configuration
            app_container.replicas = target_replicas
            
            # Scale ECS service
            service_name = f"{application_id}-service"
            scaling_result = await self.ecs_manager.scale_service(
                application_id,
                service_name,
                target_replicas,
                self.default_cluster
            )
            
            # Create scaling event
            scaling_event = ScalingEvent(
                application_id=application_id,
                event_type="scale_up" if target_replicas > previous_count else "scale_down",
                previous_count=previous_count,
                new_count=target_replicas,
                reason=reason,
                timestamp=datetime.utcnow(),
                ai_triggered=reason.startswith("ai_")
            )
            
            # Store scaling event
            if application_id not in self.scaling_events:
                self.scaling_events[application_id] = []
            self.scaling_events[application_id].append(scaling_event)
            
            logger.info(f"Application scaled: {application_id} {previous_count} -> {target_replicas}")
            return scaling_event
            
        except Exception as e:
            logger.error(f"Application scaling failed: {e}")
            raise
    
    async def get_application_status(self, application_id: str) -> Dict[str, Any]:
        """
        Get comprehensive application status.
        
        Args:
            application_id: Application identifier
            
        Returns:
            Application status with metrics and health information
        """
        try:
            if application_id not in self.applications:
                raise ValueError(f"Application not found: {application_id}")
            
            app_container = self.applications[application_id]
            service_name = f"{application_id}-service"
            
            # Get ECS service status
            service_status = await self.ecs_manager.get_service_status(
                service_name, self.default_cluster
            )
            
            # Get latest metrics
            latest_metrics = None
            if application_id in self.metrics_history and self.metrics_history[application_id]:
                latest_metrics = self.metrics_history[application_id][-1]
            
            # Get health status
            health = self.health_status.get(application_id, ContainerHealth.UNKNOWN)
            
            # Get AI insights
            ai_insights = []
            if self.ai_service:
                insights = await self.ai_service.get_comprehensive_insights(application_id)
                ai_insights = [
                    {
                        'type': insight.insight_type.value,
                        'priority': insight.priority.value,
                        'title': insight.title,
                        'description': insight.description,
                        'confidence': insight.confidence
                    }
                    for insight in insights[:5]  # Top 5 insights
                ]
            
            status = {
                'application_id': application_id,
                'name': app_container.name,
                'version': app_container.version,
                'status': service_status.get('status', 'unknown'),
                'health': health.value,
                'replicas': {
                    'desired': service_status.get('desired_count', 0),
                    'running': service_status.get('running_count', 0),
                    'pending': service_status.get('pending_count', 0)
                },
                'resources': {
                    'cpu_cores': app_container.cpu_cores,
                    'memory_gb': app_container.memory_gb
                },
                'metrics': asdict(latest_metrics) if latest_metrics else None,
                'ai_insights': ai_insights,
                'last_updated': datetime.utcnow().isoformat()
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to get application status: {e}")
            raise
    
    async def get_application_logs(
        self, 
        application_id: str, 
        lines: int = 100,
        since: Optional[datetime] = None
    ) -> List[str]:
        """
        Get application container logs.
        
        Args:
            application_id: Application identifier
            lines: Number of log lines to retrieve
            since: Get logs since this timestamp
            
        Returns:
            List of log lines
        """
        try:
            # In a real implementation, this would fetch from CloudWatch Logs
            # For now, return simulated logs
            
            if since is None:
                since = datetime.utcnow() - timedelta(hours=1)
            
            # Simulate realistic application logs
            logs = []
            for i in range(min(lines, 50)):
                timestamp = since + timedelta(minutes=i)
                log_entries = [
                    f"[{timestamp.isoformat()}] INFO: Application {application_id} started successfully",
                    f"[{timestamp.isoformat()}] INFO: Health check endpoint responding",
                    f"[{timestamp.isoformat()}] INFO: Processed 45 requests in last minute",
                    f"[{timestamp.isoformat()}] DEBUG: Memory usage: 234MB/512MB",
                    f"[{timestamp.isoformat()}] INFO: CPU utilization: 23%"
                ]
                logs.extend(log_entries[:2])  # Add 2 entries per iteration
            
            return logs[-lines:] if logs else []
            
        except Exception as e:
            logger.error(f"Failed to get application logs: {e}")
            return [f"Error retrieving logs: {str(e)}"]
    
    async def stop_application(self, application_id: str) -> bool:
        """
        Stop application containers.
        
        Args:
            application_id: Application identifier
            
        Returns:
            True if successful
        """
        try:
            if application_id not in self.applications:
                raise ValueError(f"Application not found: {application_id}")
            
            # Scale down to 0 replicas
            await self.scale_application(application_id, 0, "stop_requested")
            
            # Update health status
            self.health_status[application_id] = ContainerHealth.UNHEALTHY
            
            logger.info(f"Application stopped: {application_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop application: {e}")
            return False
    
    async def restart_application(self, application_id: str) -> bool:
        """
        Restart application containers.
        
        Args:
            application_id: Application identifier
            
        Returns:
            True if successful
        """
        try:
            if application_id not in self.applications:
                raise ValueError(f"Application not found: {application_id}")
            
            app_container = self.applications[application_id]
            
            # Force new deployment to restart containers
            await self.deploy_application(
                app_container, 
                DeploymentStrategy.ROLLING_UPDATE,
                ai_optimized=True
            )
            
            logger.info(f"Application restart initiated: {application_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restart application: {e}")
            return False
    
    async def _apply_ai_optimizations(self, app_container: ApplicationContainer) -> ApplicationContainer:
        """Apply AI-driven optimizations to application configuration."""
        try:
            if not self.ai_service:
                return app_container
            
            # Get AI insights for optimization
            insights = await self.ai_service.get_comprehensive_insights(app_container.application_id)
            
            # Apply resource recommendations
            resource_insights = [i for i in insights if i.insight_type.value == 'resource_recommendation']
            if resource_insights:
                resource_rec = resource_insights[0]
                recommended_config = resource_rec.data.get('recommended_config', {})
                
                if 'cpu_cores' in recommended_config:
                    optimized_cpu = recommended_config['cpu_cores']
                    if optimized_cpu != app_container.cpu_cores:
                        logger.info(f"AI CPU optimization: {app_container.cpu_cores} -> {optimized_cpu}")
                        app_container.cpu_cores = optimized_cpu
                
                if 'memory_gb' in recommended_config:
                    optimized_memory = recommended_config['memory_gb']
                    if optimized_memory != app_container.memory_gb:
                        logger.info(f"AI memory optimization: {app_container.memory_gb} -> {optimized_memory}")
                        app_container.memory_gb = optimized_memory
                
                if 'instance_count' in recommended_config:
                    optimized_replicas = recommended_config['instance_count']
                    if optimized_replicas != app_container.replicas:
                        logger.info(f"AI replica optimization: {app_container.replicas} -> {optimized_replicas}")
                        app_container.replicas = optimized_replicas
            
            return app_container
            
        except Exception as e:
            logger.error(f"AI optimization failed: {e}")
            return app_container
    
    async def _monitor_application(self, application_id: str):
        """Background monitoring task for application health and metrics."""
        try:
            while application_id in self.applications:
                # Collect metrics
                metrics = await self._collect_application_metrics(application_id)
                if metrics:
                    # Store metrics
                    if application_id not in self.metrics_history:
                        self.metrics_history[application_id] = []
                    
                    self.metrics_history[application_id].append(metrics)
                    
                    # Keep only recent metrics (last 24 hours)
                    cutoff_time = datetime.utcnow() - timedelta(hours=24)
                    self.metrics_history[application_id] = [
                        m for m in self.metrics_history[application_id]
                        if m.timestamp > cutoff_time
                    ]
                    
                    # Update health status
                    await self._update_health_status(application_id, metrics)
                    
                    # Check for auto-scaling triggers
                    if self.auto_scaling_enabled:
                        await self._check_auto_scaling(application_id, metrics)
                
                # Wait for next monitoring cycle
                await asyncio.sleep(self.monitoring_interval)
                
        except Exception as e:
            logger.error(f"Application monitoring failed: {e}")
    
    async def _collect_application_metrics(self, application_id: str) -> Optional[ContainerMetrics]:
        """Collect current application metrics."""
        try:
            # In a real implementation, this would collect from CloudWatch or other monitoring
            # For now, simulate realistic metrics
            
            import random
            
            # Simulate metrics with some variability
            base_cpu = 40 + random.uniform(-15, 25)
            base_memory = 60 + random.uniform(-20, 20)
            
            metrics = ContainerMetrics(
                application_id=application_id,
                cpu_utilization=max(0, min(100, base_cpu)),
                memory_utilization=max(0, min(100, base_memory)),
                network_in=random.uniform(100, 1000),  # KB/s
                network_out=random.uniform(50, 500),   # KB/s
                request_count=random.randint(50, 200),
                response_time=random.uniform(80, 200),  # ms
                error_rate=random.uniform(0, 2),        # %
                timestamp=datetime.utcnow()
            )
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect metrics: {e}")
            return None
    
    async def _update_health_status(self, application_id: str, metrics: ContainerMetrics):
        """Update application health status based on metrics."""
        try:
            # Simple health assessment based on metrics
            if metrics.error_rate > 5.0:
                health = ContainerHealth.UNHEALTHY
            elif metrics.cpu_utilization > 90 or metrics.memory_utilization > 95:
                health = ContainerHealth.UNHEALTHY
            elif metrics.response_time > 1000:  # > 1 second
                health = ContainerHealth.UNHEALTHY
            else:
                health = ContainerHealth.HEALTHY
            
            # Update health status if changed
            current_health = self.health_status.get(application_id, ContainerHealth.UNKNOWN)
            if health != current_health:
                self.health_status[application_id] = health
                logger.info(f"Health status updated: {application_id} -> {health.value}")
            
        except Exception as e:
            logger.error(f"Failed to update health status: {e}")
    
    async def _check_auto_scaling(self, application_id: str, metrics: ContainerMetrics):
        """Check if auto-scaling should be triggered."""
        try:
            if application_id not in self.applications:
                return
            
            app_container = self.applications[application_id]
            if not app_container.auto_scaling:
                return
            
            current_replicas = app_container.replicas
            
            # Simple auto-scaling logic
            scale_up_threshold = 75.0
            scale_down_threshold = 25.0
            
            should_scale_up = (
                metrics.cpu_utilization > scale_up_threshold or 
                metrics.memory_utilization > scale_up_threshold
            )
            
            should_scale_down = (
                metrics.cpu_utilization < scale_down_threshold and 
                metrics.memory_utilization < scale_down_threshold and
                current_replicas > 1
            )
            
            if should_scale_up and current_replicas < 10:
                new_replicas = min(10, current_replicas + 1)
                await self.scale_application(
                    application_id, 
                    new_replicas, 
                    f"ai_auto_scale_up_cpu_{metrics.cpu_utilization:.1f}_mem_{metrics.memory_utilization:.1f}"
                )
            
            elif should_scale_down:
                new_replicas = max(1, current_replicas - 1)
                await self.scale_application(
                    application_id, 
                    new_replicas, 
                    f"ai_auto_scale_down_cpu_{metrics.cpu_utilization:.1f}_mem_{metrics.memory_utilization:.1f}"
                )
            
        except Exception as e:
            logger.error(f"Auto-scaling check failed: {e}")
    
    async def _get_default_subnets(self) -> List[str]:
        """Get default subnets for ECS service."""
        # In production, this would query actual VPC subnets
        return [
            "subnet-12345678",
            "subnet-87654321"
        ]
    
    async def _get_default_security_groups(self) -> List[str]:
        """Get default security groups for ECS service."""
        # In production, this would query actual security groups
        return ["sg-12345678"]
    
    async def get_scaling_history(self, application_id: str) -> List[ScalingEvent]:
        """Get scaling event history for an application."""
        return self.scaling_events.get(application_id, [])
    
    async def get_metrics_history(
        self, 
        application_id: str, 
        hours: int = 24
    ) -> List[ContainerMetrics]:
        """Get metrics history for an application."""
        if application_id not in self.metrics_history:
            return []
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return [
            metrics for metrics in self.metrics_history[application_id]
            if metrics.timestamp > cutoff_time
        ]
    
    async def get_all_applications(self) -> List[Dict[str, Any]]:
        """Get status of all managed applications."""
        applications = []
        
        for app_id in self.applications.keys():
            try:
                status = await self.get_application_status(app_id)
                applications.append(status)
            except Exception as e:
                logger.error(f"Failed to get status for {app_id}: {e}")
        
        return applications

"""
Environment Manager for AI-Native PaaS Platform.

This module manages multiple deployment environments with AI-driven
configuration optimization and automated promotion workflows.

Features:
- Multi-environment orchestration (dev, staging, production)
- Environment-specific configuration management
- Automated promotion pipelines
- AI-driven environment optimization
- Configuration drift detection
- Environment health monitoring
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import copy

from .infrastructure_manager import InfrastructureManager, Environment, InfrastructureConfig

logger = logging.getLogger(__name__)


class PromotionStatus(str, Enum):
    """Environment promotion status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class ConfigurationDrift(str, Enum):
    """Configuration drift severity."""
    NONE = "none"
    MINOR = "minor"
    MAJOR = "major"
    CRITICAL = "critical"


@dataclass
class EnvironmentSpec:
    """Environment specification and configuration."""
    environment: Environment
    region: str
    infrastructure_config: InfrastructureConfig
    application_config: Dict[str, Any]
    secrets_config: Dict[str, str]
    scaling_config: Dict[str, Any]
    monitoring_config: Dict[str, Any]
    backup_config: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PromotionPipeline:
    """Environment promotion pipeline configuration."""
    pipeline_id: str
    source_environment: Environment
    target_environment: Environment
    promotion_strategy: str
    validation_steps: List[str]
    approval_required: bool
    rollback_enabled: bool
    notification_channels: List[str]


@dataclass
class PromotionResult:
    """Environment promotion result."""
    promotion_id: str
    pipeline: PromotionPipeline
    status: PromotionStatus
    started_at: datetime
    completed_at: Optional[datetime]
    validation_results: Dict[str, Any]
    deployment_results: Dict[str, Any]
    rollback_executed: bool
    error_message: Optional[str]
    metadata: Dict[str, Any]


class EnvironmentManager:
    """
    Multi-environment management with AI optimization.
    
    Orchestrates multiple deployment environments with intelligent
    configuration management and automated promotion workflows.
    """
    
    def __init__(self, infrastructure_manager: InfrastructureManager, ai_service=None):
        """
        Initialize Environment Manager.
        
        Args:
            infrastructure_manager: Infrastructure manager instance
            ai_service: AI service for intelligent optimization
        """
        self.infrastructure_manager = infrastructure_manager
        self.ai_service = ai_service
        
        # Manager state
        self.environments: Dict[Environment, EnvironmentSpec] = {}
        self.promotion_pipelines: Dict[str, PromotionPipeline] = {}
        self.promotion_history: List[PromotionResult] = []
        self.active_promotions: Dict[str, PromotionResult] = {}
        
        # Configuration
        self.default_promotion_strategy = "blue_green"
        self.drift_check_interval = 3600  # 1 hour
        
        # Initialize default promotion pipelines
        self._initialize_promotion_pipelines()
        
        logger.info("Environment Manager initialized")
    
    def _initialize_promotion_pipelines(self):
        """Initialize default promotion pipelines."""
        
        # Development to Staging pipeline
        dev_to_staging = PromotionPipeline(
            pipeline_id="dev-to-staging",
            source_environment=Environment.DEVELOPMENT,
            target_environment=Environment.STAGING,
            promotion_strategy="rolling_update",
            validation_steps=[
                "unit_tests",
                "integration_tests",
                "security_scan",
                "performance_baseline"
            ],
            approval_required=False,
            rollback_enabled=True,
            notification_channels=["slack://dev-team"]
        )
        
        # Staging to Production pipeline
        staging_to_prod = PromotionPipeline(
            pipeline_id="staging-to-production",
            source_environment=Environment.STAGING,
            target_environment=Environment.PRODUCTION,
            promotion_strategy="blue_green",
            validation_steps=[
                "integration_tests",
                "load_tests",
                "security_scan",
                "compliance_check",
                "disaster_recovery_test"
            ],
            approval_required=True,
            rollback_enabled=True,
            notification_channels=["slack://ops-team", "email://ops@company.com"]
        )
        
        self.promotion_pipelines["dev-to-staging"] = dev_to_staging
        self.promotion_pipelines["staging-to-production"] = staging_to_prod
    
    async def create_environment(
        self, 
        environment: Environment,
        base_config: Optional[EnvironmentSpec] = None,
        ai_optimized: bool = True
    ) -> EnvironmentSpec:
        """
        Create new environment with AI optimization.
        
        Args:
            environment: Environment to create
            base_config: Base configuration to use
            ai_optimized: Whether to apply AI optimizations
            
        Returns:
            Environment specification
        """
        try:
            logger.info(f"Creating environment: {environment.value}")
            
            # Create base configuration if not provided
            if not base_config:
                base_config = self._create_default_environment_spec(environment)
            
            # Apply AI optimizations if enabled
            if ai_optimized and self.ai_service:
                base_config = await self._apply_ai_environment_optimizations(base_config)
            
            # Deploy infrastructure
            deployment_result = await self.infrastructure_manager.deploy_environment(
                base_config.infrastructure_config
            )
            
            if deployment_result.status.value != 'deployed':
                raise RuntimeError(f"Infrastructure deployment failed: {deployment_result.status}")
            
            # Store environment specification
            self.environments[environment] = base_config
            
            logger.info(f"Environment created successfully: {environment.value}")
            return base_config
            
        except Exception as e:
            logger.error(f"Environment creation failed: {e}")
            raise
    
    def _create_default_environment_spec(self, environment: Environment) -> EnvironmentSpec:
        """Create default environment specification."""
        
        # Environment-specific configurations
        if environment == Environment.PRODUCTION:
            infrastructure_config = InfrastructureConfig(
                environment=environment,
                region="us-east-1",
                vpc_cidr="10.0.0.0/16",
                availability_zones=["us-east-1a", "us-east-1b", "us-east-1c"],
                enable_nat_gateway=True,
                enable_flow_logs=True,
                backup_retention_days=30,
                monitoring_enabled=True,
                security_hardening_enabled=True
            )
            
            scaling_config = {
                "min_instances": 2,
                "max_instances": 20,
                "target_cpu_utilization": 60.0,
                "scale_up_cooldown": 300,
                "scale_down_cooldown": 600
            }
            
        elif environment == Environment.STAGING:
            infrastructure_config = InfrastructureConfig(
                environment=environment,
                region="us-east-1",
                vpc_cidr="10.1.0.0/16",
                availability_zones=["us-east-1a", "us-east-1b"],
                enable_nat_gateway=True,
                enable_flow_logs=True,
                backup_retention_days=7,
                monitoring_enabled=True,
                security_hardening_enabled=True
            )
            
            scaling_config = {
                "min_instances": 1,
                "max_instances": 5,
                "target_cpu_utilization": 70.0,
                "scale_up_cooldown": 180,
                "scale_down_cooldown": 300
            }
            
        else:  # Development
            infrastructure_config = InfrastructureConfig(
                environment=environment,
                region="us-east-1",
                vpc_cidr="10.2.0.0/16",
                availability_zones=["us-east-1a"],
                enable_nat_gateway=False,
                enable_flow_logs=False,
                backup_retention_days=3,
                monitoring_enabled=True,
                security_hardening_enabled=False
            )
            
            scaling_config = {
                "min_instances": 1,
                "max_instances": 3,
                "target_cpu_utilization": 80.0,
                "scale_up_cooldown": 120,
                "scale_down_cooldown": 180
            }
        
        return EnvironmentSpec(
            environment=environment,
            region=infrastructure_config.region,
            infrastructure_config=infrastructure_config,
            application_config={
                "log_level": "INFO" if environment == Environment.PRODUCTION else "DEBUG",
                "debug_mode": environment != Environment.PRODUCTION,
                "feature_flags": {
                    "new_ui": environment != Environment.PRODUCTION,
                    "beta_features": environment == Environment.DEVELOPMENT
                }
            },
            secrets_config={
                "database_password": f"{environment.value}_db_password",
                "api_keys": f"{environment.value}_api_keys",
                "certificates": f"{environment.value}_certificates"
            },
            scaling_config=scaling_config,
            monitoring_config={
                "metrics_retention_days": 30 if environment == Environment.PRODUCTION else 7,
                "detailed_monitoring": environment == Environment.PRODUCTION,
                "alerting_enabled": environment != Environment.DEVELOPMENT,
                "dashboard_enabled": True
            },
            backup_config={
                "enabled": environment != Environment.DEVELOPMENT,
                "frequency": "daily" if environment == Environment.PRODUCTION else "weekly",
                "retention_days": infrastructure_config.backup_retention_days,
                "cross_region_backup": environment == Environment.PRODUCTION
            }
        )
    
    async def _apply_ai_environment_optimizations(self, env_spec: EnvironmentSpec) -> EnvironmentSpec:
        """Apply AI-driven optimizations to environment specification."""
        try:
            if not self.ai_service:
                return env_spec
            
            # Get AI insights for environment optimization
            insights = await self.ai_service.get_comprehensive_insights(
                f"environment-{env_spec.environment.value}"
            )
            
            optimizations_applied = []
            
            # Apply cost optimization insights
            cost_insights = [i for i in insights if i.insight_type.value == 'cost_optimization']
            for insight in cost_insights:
                if insight.confidence > 0.7:
                    # Optimize scaling configuration
                    if 'max_instances' in insight.data:
                        recommended_max = insight.data['max_instances']
                        if recommended_max < env_spec.scaling_config['max_instances']:
                            env_spec.scaling_config['max_instances'] = recommended_max
                            optimizations_applied.append("AI-optimized max instances")
            
            # Apply resource recommendations
            resource_insights = [i for i in insights if i.insight_type.value == 'resource_recommendation']
            for insight in resource_insights:
                if insight.confidence > 0.8:
                    recommended_config = insight.data.get('recommended_config', {})
                    
                    # Optimize CPU utilization targets
                    if 'target_cpu_utilization' in recommended_config:
                        env_spec.scaling_config['target_cpu_utilization'] = recommended_config['target_cpu_utilization']
                        optimizations_applied.append("AI-optimized CPU utilization target")
            
            # Apply performance optimizations
            performance_insights = [i for i in insights if i.insight_type.value == 'performance_prediction']
            for insight in performance_insights:
                if insight.confidence > 0.75:
                    # Optimize cooldown periods based on performance predictions
                    if insight.data.get('predicted_response_time', 0) > 200:
                        # Faster scaling for high response times
                        env_spec.scaling_config['scale_up_cooldown'] = max(60, env_spec.scaling_config['scale_up_cooldown'] // 2)
                        optimizations_applied.append("AI-optimized scaling cooldown")
            
            logger.info(f"Applied {len(optimizations_applied)} AI optimizations to environment")
            return env_spec
            
        except Exception as e:
            logger.error(f"AI environment optimization failed: {e}")
            return env_spec
    
    async def promote_environment(
        self, 
        pipeline_id: str,
        version: str,
        auto_approve: bool = False
    ) -> PromotionResult:
        """
        Promote application between environments.
        
        Args:
            pipeline_id: Promotion pipeline identifier
            version: Application version to promote
            auto_approve: Whether to auto-approve if approval required
            
        Returns:
            Promotion result
        """
        try:
            if pipeline_id not in self.promotion_pipelines:
                raise ValueError(f"Promotion pipeline not found: {pipeline_id}")
            
            pipeline = self.promotion_pipelines[pipeline_id]
            promotion_id = f"promotion-{pipeline_id}-{int(datetime.utcnow().timestamp())}"
            
            logger.info(f"Starting environment promotion: {promotion_id}")
            
            # Initialize promotion result
            promotion_result = PromotionResult(
                promotion_id=promotion_id,
                pipeline=pipeline,
                status=PromotionStatus.PENDING,
                started_at=datetime.utcnow(),
                completed_at=None,
                validation_results={},
                deployment_results={},
                rollback_executed=False,
                error_message=None,
                metadata={"version": version, "auto_approve": auto_approve}
            )
            
            # Store active promotion
            self.active_promotions[promotion_id] = promotion_result
            
            # Start promotion task
            asyncio.create_task(self._execute_promotion(promotion_result, auto_approve))
            
            logger.info(f"Environment promotion initiated: {promotion_id}")
            return promotion_result
            
        except Exception as e:
            logger.error(f"Environment promotion failed: {e}")
            raise
    
    async def _execute_promotion(self, promotion_result: PromotionResult, auto_approve: bool):
        """Execute environment promotion pipeline."""
        try:
            promotion_result.status = PromotionStatus.IN_PROGRESS
            pipeline = promotion_result.pipeline
            
            # Step 1: Validation
            logger.info(f"Running validation steps for {promotion_result.promotion_id}")
            validation_success = await self._run_validation_steps(promotion_result)
            
            if not validation_success:
                promotion_result.status = PromotionStatus.FAILED
                promotion_result.error_message = "Validation steps failed"
                return
            
            # Step 2: Approval (if required)
            if pipeline.approval_required and not auto_approve:
                logger.info(f"Waiting for approval: {promotion_result.promotion_id}")
                approval_granted = await self._wait_for_approval(promotion_result)
                
                if not approval_granted:
                    promotion_result.status = PromotionStatus.FAILED
                    promotion_result.error_message = "Approval not granted"
                    return
            
            # Step 3: Deployment
            logger.info(f"Executing deployment for {promotion_result.promotion_id}")
            deployment_success = await self._execute_deployment(promotion_result)
            
            if not deployment_success:
                if pipeline.rollback_enabled:
                    logger.info(f"Initiating rollback for {promotion_result.promotion_id}")
                    await self._execute_rollback(promotion_result)
                    promotion_result.status = PromotionStatus.ROLLED_BACK
                else:
                    promotion_result.status = PromotionStatus.FAILED
                return
            
            # Step 4: Post-deployment validation
            logger.info(f"Running post-deployment validation for {promotion_result.promotion_id}")
            post_validation_success = await self._run_post_deployment_validation(promotion_result)
            
            if not post_validation_success and pipeline.rollback_enabled:
                logger.info(f"Post-deployment validation failed, rolling back: {promotion_result.promotion_id}")
                await self._execute_rollback(promotion_result)
                promotion_result.status = PromotionStatus.ROLLED_BACK
                return
            
            # Promotion completed successfully
            promotion_result.status = PromotionStatus.COMPLETED
            promotion_result.completed_at = datetime.utcnow()
            
            logger.info(f"Environment promotion completed successfully: {promotion_result.promotion_id}")
            
        except Exception as e:
            logger.error(f"Promotion execution failed: {e}")
            promotion_result.status = PromotionStatus.FAILED
            promotion_result.error_message = str(e)
        
        finally:
            # Move to history and cleanup
            self.promotion_history.append(promotion_result)
            if promotion_result.promotion_id in self.active_promotions:
                del self.active_promotions[promotion_result.promotion_id]
    
    async def _run_validation_steps(self, promotion_result: PromotionResult) -> bool:
        """Run validation steps for promotion."""
        try:
            pipeline = promotion_result.pipeline
            validation_results = {}
            
            for step in pipeline.validation_steps:
                logger.info(f"Running validation step: {step}")
                
                # Simulate validation steps
                await asyncio.sleep(1)  # Simulate validation time
                
                if step == "unit_tests":
                    result = {"passed": 95, "failed": 5, "success_rate": 95.0}
                    validation_results[step] = result
                    
                elif step == "integration_tests":
                    result = {"passed": 28, "failed": 2, "success_rate": 93.3}
                    validation_results[step] = result
                    
                elif step == "security_scan":
                    result = {"vulnerabilities": 0, "warnings": 2, "status": "passed"}
                    validation_results[step] = result
                    
                elif step == "performance_baseline":
                    result = {"avg_response_time": 85.2, "throughput": 1250, "status": "passed"}
                    validation_results[step] = result
                    
                elif step == "load_tests":
                    result = {"max_rps": 2000, "avg_response_time": 120, "error_rate": 0.1, "status": "passed"}
                    validation_results[step] = result
                    
                elif step == "compliance_check":
                    result = {"compliance_score": 98.5, "issues": 0, "status": "passed"}
                    validation_results[step] = result
                    
                else:
                    result = {"status": "passed", "message": f"Validation step {step} completed"}
                    validation_results[step] = result
            
            promotion_result.validation_results = validation_results
            
            # Check if all validations passed
            all_passed = all(
                result.get("status") == "passed" or 
                result.get("success_rate", 0) >= 90.0
                for result in validation_results.values()
            )
            
            return all_passed
            
        except Exception as e:
            logger.error(f"Validation steps failed: {e}")
            return False
    
    async def _wait_for_approval(self, promotion_result: PromotionResult) -> bool:
        """Wait for promotion approval."""
        # In production, this would integrate with approval systems
        # For now, simulate approval after a short delay
        await asyncio.sleep(2)
        logger.info(f"Promotion approved (simulated): {promotion_result.promotion_id}")
        return True
    
    async def _execute_deployment(self, promotion_result: PromotionResult) -> bool:
        """Execute deployment to target environment."""
        try:
            pipeline = promotion_result.pipeline
            
            # Simulate deployment based on strategy
            if pipeline.promotion_strategy == "blue_green":
                await asyncio.sleep(3)  # Simulate blue/green deployment
                deployment_result = {
                    "strategy": "blue_green",
                    "status": "success",
                    "green_environment_ready": True,
                    "traffic_switched": True,
                    "blue_environment_cleaned": True
                }
            elif pipeline.promotion_strategy == "rolling_update":
                await asyncio.sleep(2)  # Simulate rolling update
                deployment_result = {
                    "strategy": "rolling_update",
                    "status": "success",
                    "instances_updated": 3,
                    "update_success_rate": 100.0
                }
            else:
                await asyncio.sleep(1)  # Simulate basic deployment
                deployment_result = {
                    "strategy": pipeline.promotion_strategy,
                    "status": "success"
                }
            
            promotion_result.deployment_results = deployment_result
            return deployment_result["status"] == "success"
            
        except Exception as e:
            logger.error(f"Deployment execution failed: {e}")
            promotion_result.deployment_results = {"status": "failed", "error": str(e)}
            return False
    
    async def _run_post_deployment_validation(self, promotion_result: PromotionResult) -> bool:
        """Run post-deployment validation."""
        try:
            # Simulate post-deployment health checks
            await asyncio.sleep(1)
            
            health_check_results = {
                "application_health": "healthy",
                "database_connectivity": "healthy",
                "external_services": "healthy",
                "performance_metrics": {
                    "avg_response_time": 95.2,
                    "error_rate": 0.05,
                    "throughput": 1180
                }
            }
            
            promotion_result.validation_results["post_deployment"] = health_check_results
            
            # Check if all health checks passed
            return health_check_results["application_health"] == "healthy"
            
        except Exception as e:
            logger.error(f"Post-deployment validation failed: {e}")
            return False
    
    async def _execute_rollback(self, promotion_result: PromotionResult):
        """Execute rollback for failed promotion."""
        try:
            logger.info(f"Executing rollback for {promotion_result.promotion_id}")
            
            # Simulate rollback
            await asyncio.sleep(2)
            
            rollback_result = {
                "status": "success",
                "previous_version_restored": True,
                "traffic_restored": True,
                "rollback_time_seconds": 45
            }
            
            promotion_result.deployment_results["rollback"] = rollback_result
            promotion_result.rollback_executed = True
            
            logger.info(f"Rollback completed for {promotion_result.promotion_id}")
            
        except Exception as e:
            logger.error(f"Rollback execution failed: {e}")
            promotion_result.deployment_results["rollback"] = {"status": "failed", "error": str(e)}
    
    async def detect_configuration_drift(self, environment: Environment) -> Dict[str, Any]:
        """Detect configuration drift in environment."""
        try:
            if environment not in self.environments:
                return {"error": f"Environment not found: {environment.value}"}
            
            env_spec = self.environments[environment]
            
            # Get current infrastructure status
            current_status = await self.infrastructure_manager.get_environment_status(environment)
            
            # Compare with expected configuration
            drift_analysis = {
                "environment": environment.value,
                "drift_detected": False,
                "drift_severity": ConfigurationDrift.NONE,
                "drift_details": [],
                "last_check": datetime.utcnow().isoformat()
            }
            
            # Simulate drift detection
            import random
            if random.random() < 0.1:  # 10% chance of drift
                drift_analysis.update({
                    "drift_detected": True,
                    "drift_severity": ConfigurationDrift.MINOR,
                    "drift_details": [
                        "Security group rules modified outside of IaC",
                        "Instance tags missing or incorrect"
                    ]
                })
            
            return drift_analysis
            
        except Exception as e:
            logger.error(f"Configuration drift detection failed: {e}")
            return {"error": str(e)}
    
    async def get_environment_health(self, environment: Environment) -> Dict[str, Any]:
        """Get comprehensive environment health status."""
        try:
            if environment not in self.environments:
                return {"error": f"Environment not found: {environment.value}"}
            
            env_spec = self.environments[environment]
            
            # Get infrastructure status
            infra_status = await self.infrastructure_manager.get_environment_status(environment)
            
            # Get configuration drift
            drift_status = await self.detect_configuration_drift(environment)
            
            # Simulate application health
            app_health = {
                "status": "healthy",
                "services": {
                    "api": "healthy",
                    "database": "healthy",
                    "cache": "healthy",
                    "monitoring": "healthy"
                },
                "performance": {
                    "avg_response_time": 85.2,
                    "error_rate": 0.1,
                    "throughput": 1250
                }
            }
            
            # Overall health assessment
            overall_health = "healthy"
            if drift_status.get("drift_severity") == ConfigurationDrift.CRITICAL.value:
                overall_health = "degraded"
            elif infra_status.get("status") != "deployed":
                overall_health = "unhealthy"
            
            return {
                "environment": environment.value,
                "overall_health": overall_health,
                "infrastructure": infra_status,
                "application": app_health,
                "configuration_drift": drift_status,
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Environment health check failed: {e}")
            return {"error": str(e)}
    
    async def get_promotion_history(self, limit: int = 10) -> List[PromotionResult]:
        """Get promotion history."""
        return sorted(self.promotion_history, key=lambda x: x.started_at, reverse=True)[:limit]
    
    async def get_active_promotions(self) -> List[PromotionResult]:
        """Get currently active promotions."""
        return list(self.active_promotions.values())
    
    async def cancel_promotion(self, promotion_id: str) -> bool:
        """Cancel active promotion."""
        if promotion_id not in self.active_promotions:
            return False
        
        promotion = self.active_promotions[promotion_id]
        promotion.status = PromotionStatus.FAILED
        promotion.error_message = "Promotion cancelled by user"
        promotion.completed_at = datetime.utcnow()
        
        logger.info(f"Promotion cancelled: {promotion_id}")
        return True

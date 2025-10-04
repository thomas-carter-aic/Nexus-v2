"""
Test suite for Production Infrastructure components.
Tests infrastructure management, environment orchestration, and monitoring.
"""

import pytest
import sys
import asyncio
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_production_infrastructure_imports():
    """Test that production infrastructure components can be imported."""
    try:
        from infrastructure.deployment.infrastructure_manager import InfrastructureManager, Environment
        from infrastructure.deployment.environment_manager import EnvironmentManager
        from infrastructure.monitoring.monitoring_service import MonitoringService
        
        assert True, "Production infrastructure components imported successfully"
    except ImportError as e:
        pytest.fail(f"Failed to import production infrastructure components: {e}")


@pytest.mark.asyncio
async def test_infrastructure_manager():
    """Test Infrastructure Manager functionality."""
    try:
        from infrastructure.deployment.infrastructure_manager import (
            InfrastructureManager, InfrastructureConfig, Environment
        )
        from ai.service import AIService
        
        # Initialize with AI service
        ai_service = AIService()
        infra_manager = InfrastructureManager(ai_service)
        
        # Test infrastructure configuration
        config = InfrastructureConfig(
            environment=Environment.DEVELOPMENT,
            region="us-east-1",
            vpc_cidr="10.0.0.0/16",
            availability_zones=["us-east-1a", "us-east-1b"],
            ai_optimization_enabled=True
        )
        
        # Test dry run deployment
        deployment_result = await infra_manager.deploy_environment(config, dry_run=True)
        
        assert deployment_result is not None
        assert deployment_result.environment == Environment.DEVELOPMENT
        assert deployment_result.status.value in ['deployed', 'deploying']
        assert len(deployment_result.resources_created) > 0
        assert deployment_result.cost_estimate > 0
        
        # Test environment status
        status = await infra_manager.get_environment_status(Environment.DEVELOPMENT)
        assert status is not None
        assert 'environment' in status
        assert status['environment'] == Environment.DEVELOPMENT.value
        
        # Test cost analysis
        cost_analysis = await infra_manager.get_cost_analysis(Environment.DEVELOPMENT)
        assert cost_analysis is not None
        assert 'estimated_monthly_cost' in cost_analysis
        assert cost_analysis['estimated_monthly_cost'] > 0
        
        print("✅ Infrastructure Manager test passed")
        
    except Exception as e:
        pytest.fail(f"Infrastructure Manager test failed: {e}")


@pytest.mark.asyncio
async def test_environment_manager():
    """Test Environment Manager functionality."""
    try:
        from infrastructure.deployment.infrastructure_manager import InfrastructureManager
        from infrastructure.deployment.environment_manager import EnvironmentManager, Environment
        from ai.service import AIService
        
        # Initialize services
        ai_service = AIService()
        infra_manager = InfrastructureManager(ai_service)
        env_manager = EnvironmentManager(infra_manager, ai_service)
        
        # Test environment creation
        env_spec = await env_manager.create_environment(
            Environment.DEVELOPMENT, ai_optimized=True
        )
        
        assert env_spec is not None
        assert env_spec.environment == Environment.DEVELOPMENT
        assert env_spec.infrastructure_config is not None
        assert env_spec.scaling_config is not None
        
        # Test environment health
        health = await env_manager.get_environment_health(Environment.DEVELOPMENT)
        assert health is not None
        assert 'environment' in health
        assert 'overall_health' in health
        
        # Test configuration drift detection
        drift = await env_manager.detect_configuration_drift(Environment.DEVELOPMENT)
        assert drift is not None
        assert 'drift_detected' in drift
        assert 'drift_severity' in drift
        
        # Test promotion pipeline
        promotion = await env_manager.promote_environment(
            "dev-to-staging", "1.0.0", auto_approve=True
        )
        
        assert promotion is not None
        assert promotion.pipeline.source_environment == Environment.DEVELOPMENT
        assert promotion.pipeline.target_environment == Environment.STAGING
        
        print("✅ Environment Manager test passed")
        
    except Exception as e:
        pytest.fail(f"Environment Manager test failed: {e}")


@pytest.mark.asyncio
async def test_monitoring_service():
    """Test Monitoring Service functionality."""
    try:
        from infrastructure.monitoring.monitoring_service import (
            MonitoringService, MetricType, AlertSeverity
        )
        from ai.service import AIService
        
        # Initialize with AI service
        ai_service = AIService()
        monitoring_service = MonitoringService(ai_service)
        
        # Test metric collection
        success = await monitoring_service.collect_metric(
            "test_metric",
            75.5,
            "Percent",
            {"application": "test-app"},
            MetricType.APPLICATION
        )
        assert success is True
        
        # Wait a moment for metric to be processed
        await asyncio.sleep(0.1)
        
        # Test metric retrieval
        metrics = await monitoring_service.get_metrics("test_metric")
        assert isinstance(metrics, list)
        
        # Test dashboard data
        dashboard_data = await monitoring_service.get_dashboard_data("system-overview")
        assert dashboard_data is not None
        assert 'dashboard_id' in dashboard_data
        assert dashboard_data['dashboard_id'] == "system-overview"
        assert 'widgets' in dashboard_data
        
        # Test system health
        health = await monitoring_service.get_system_health()
        assert health is not None
        assert 'overall_status' in health
        assert 'components' in health
        assert 'metrics_summary' in health
        
        # Test alert history
        alert_history = await monitoring_service.get_alert_history(limit=10)
        assert isinstance(alert_history, list)
        
        print("✅ Monitoring Service test passed")
        
    except Exception as e:
        pytest.fail(f"Monitoring Service test failed: {e}")


@pytest.mark.asyncio
async def test_ai_integration():
    """Test AI integration with production infrastructure."""
    try:
        from infrastructure.deployment.infrastructure_manager import (
            InfrastructureManager, InfrastructureConfig, Environment
        )
        from infrastructure.monitoring.monitoring_service import MonitoringService
        from ai.service import AIService
        
        # Initialize with AI service
        ai_service = AIService()
        infra_manager = InfrastructureManager(ai_service)
        monitoring_service = MonitoringService(ai_service)
        
        # Test AI-optimized infrastructure deployment
        config = InfrastructureConfig(
            environment=Environment.STAGING,
            region="us-east-1",
            ai_optimization_enabled=True,
            cost_optimization_enabled=True
        )
        
        deployment_result = await infra_manager.deploy_environment(config, dry_run=True)
        
        assert deployment_result is not None
        assert len(deployment_result.ai_optimizations_applied) > 0
        
        # Test AI-enhanced monitoring
        await monitoring_service.collect_metric(
            "cpu_utilization", 85.0, "Percent", {"source": "ai-test"}
        )
        
        # Wait for AI processing
        await asyncio.sleep(1)
        
        # Get dashboard with AI insights
        dashboard_data = await monitoring_service.get_dashboard_data("system-overview")
        if 'ai_insights' in dashboard_data:
            assert isinstance(dashboard_data['ai_insights'], list)
        
        print("✅ AI Integration test passed")
        
    except Exception as e:
        pytest.fail(f"AI Integration test failed: {e}")


def test_production_infrastructure_dependencies():
    """Test that production infrastructure dependencies are available."""
    try:
        import boto3
        import asyncio
        from datetime import datetime, timedelta
        from dataclasses import dataclass
        from enum import Enum
        import json
        
        # Test basic functionality
        assert datetime.utcnow() is not None
        assert json.dumps({"test": "data"}) is not None
        
        print("✅ Production infrastructure dependencies available")
        
    except ImportError as e:
        pytest.fail(f"Production infrastructure dependencies not available: {e}")


if __name__ == "__main__":
    # Run tests individually for debugging
    print("🏗️ Testing Production Infrastructure...")
    
    # Test imports
    test_production_infrastructure_imports()
    print("✅ Production infrastructure imports test passed")
    
    # Test dependencies
    test_production_infrastructure_dependencies()
    print("✅ Production infrastructure dependencies test passed")
    
    # Run async tests
    async def run_async_tests():
        await test_infrastructure_manager()
        print("✅ Infrastructure Manager test passed")
        
        await test_environment_manager()
        print("✅ Environment Manager test passed")
        
        await test_monitoring_service()
        print("✅ Monitoring Service test passed")
        
        await test_ai_integration()
        print("✅ AI Integration test passed")
    
    # Run async tests
    asyncio.run(run_async_tests())
    
    print("\n🎉 All production infrastructure tests passed successfully!")

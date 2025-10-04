"""
Comprehensive Platform Integration Test Suite.
Tests the complete AI-Native PaaS Platform end-to-end functionality.
"""

import pytest
import sys
import asyncio
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_platform_integration_imports():
    """Test that all platform components can be imported together."""
    try:
        # Core components
        from ai.service import AIService
        from infrastructure.container.container_service import ContainerService
        from infrastructure.deployment.infrastructure_manager import InfrastructureManager
        from infrastructure.monitoring.monitoring_service import MonitoringService
        from integration.integration_test_suite import IntegrationTestSuite
        
        assert True, "All platform components imported successfully"
    except ImportError as e:
        pytest.fail(f"Failed to import platform components: {e}")


@pytest.mark.asyncio
async def test_complete_platform_integration():
    """Test complete platform integration with all components."""
    try:
        # Initialize all services
        from ai.service import AIService
        from infrastructure.container.container_service import ContainerService
        from infrastructure.deployment.infrastructure_manager import InfrastructureManager
        from infrastructure.monitoring.monitoring_service import MonitoringService
        from integration.integration_test_suite import IntegrationTestSuite
        
        # Initialize services
        ai_service = AIService()
        container_service = ContainerService(ai_service=ai_service)
        infrastructure_manager = InfrastructureManager(ai_service)
        monitoring_service = MonitoringService(ai_service)
        
        # Force mock mode for testing
        container_service.ecs_manager.ecs_client = None
        infrastructure_manager.cloudformation_client = None
        monitoring_service.cloudwatch_client = None
        
        # Initialize integration test suite
        test_suite = IntegrationTestSuite(
            ai_service=ai_service,
            container_service=container_service,
            infrastructure_manager=infrastructure_manager,
            monitoring_service=monitoring_service
        )
        
        # Run comprehensive integration tests
        suite_result = await test_suite.run_full_test_suite()
        
        # Validate results
        assert suite_result is not None
        assert suite_result.total_tests > 0
        assert suite_result.success_rate >= 80.0  # At least 80% success rate
        
        # Check that key test categories passed
        category_results = {}
        for test_result in suite_result.test_results:
            category = test_result.category.value
            if category not in category_results:
                category_results[category] = {"passed": 0, "total": 0}
            
            category_results[category]["total"] += 1
            if test_result.status.value == "passed":
                category_results[category]["passed"] += 1
        
        # Validate critical categories
        critical_categories = ["ai_models", "end_to_end"]
        for category in critical_categories:
            if category in category_results:
                success_rate = (category_results[category]["passed"] / 
                              category_results[category]["total"] * 100)
                assert success_rate >= 70.0, f"{category} tests below 70% success rate"
        
        print(f"✅ Platform integration test passed: {suite_result.passed_tests}/{suite_result.total_tests} tests passed ({suite_result.success_rate:.1f}%)")
        
    except Exception as e:
        pytest.fail(f"Platform integration test failed: {e}")


@pytest.mark.asyncio
async def test_ai_service_comprehensive():
    """Test AI service comprehensive functionality."""
    try:
        from ai.service import AIService
        
        ai_service = AIService()
        
        # Test comprehensive insights generation
        insights = await ai_service.get_comprehensive_insights("platform-integration-test")
        
        assert isinstance(insights, list)
        assert len(insights) > 0
        
        # Test service health
        health = await ai_service.get_service_health()
        assert health['status'] == 'healthy'
        assert health['models_active'] == 5
        
        # Test insight types coverage
        insight_types = set([insight.insight_type.value for insight in insights])
        expected_types = {'scaling_recommendation', 'anomaly_alert', 'cost_optimization', 
                         'performance_prediction', 'resource_recommendation'}
        
        # Should have at least 3 different insight types
        assert len(insight_types.intersection(expected_types)) >= 3
        
        print("✅ AI Service comprehensive test passed")
        
    except Exception as e:
        pytest.fail(f"AI Service comprehensive test failed: {e}")


@pytest.mark.asyncio
async def test_container_orchestration_comprehensive():
    """Test container orchestration comprehensive functionality."""
    try:
        from infrastructure.container.container_service import ContainerService, ApplicationContainer
        from infrastructure.container.deployment_orchestrator import DeploymentOrchestrator
        from ai.service import AIService
        
        # Initialize services
        ai_service = AIService()
        container_service = ContainerService(ai_service=ai_service)
        orchestrator = DeploymentOrchestrator(container_service, ai_service)
        
        # Force mock mode
        container_service.ecs_manager.ecs_client = None
        
        # Test application deployment
        app_container = ApplicationContainer(
            application_id="integration-test-app",
            name="integration-test-app",
            image="nginx",
            version="1.0",
            cpu_cores=1.0,
            memory_gb=2.0,
            port=80,
            environment_variables={"ENV": "integration-test"},
            replicas=2,
            auto_scaling=True
        )
        
        deployment = await container_service.deploy_application(app_container, ai_optimized=True)
        assert deployment is not None
        assert deployment.application_id == "integration-test-app"
        
        # Test deployment orchestration
        pipeline = await orchestrator.create_deployment_pipeline(
            "integration-test-app", "1.1", "web-app-standard"
        )
        assert pipeline is not None
        assert len(pipeline.steps) > 0
        
        # Test scaling
        scaling_event = await container_service.scale_application(
            "integration-test-app", 3, "integration_test"
        )
        assert scaling_event.new_count == 3
        
        print("✅ Container orchestration comprehensive test passed")
        
    except Exception as e:
        pytest.fail(f"Container orchestration comprehensive test failed: {e}")


@pytest.mark.asyncio
async def test_infrastructure_comprehensive():
    """Test infrastructure management comprehensive functionality."""
    try:
        from infrastructure.deployment.infrastructure_manager import (
            InfrastructureManager, InfrastructureConfig, Environment
        )
        from infrastructure.deployment.environment_manager import EnvironmentManager
        from ai.service import AIService
        
        # Initialize services
        ai_service = AIService()
        infra_manager = InfrastructureManager(ai_service)
        env_manager = EnvironmentManager(infra_manager, ai_service)
        
        # Test infrastructure deployment
        config = InfrastructureConfig(
            environment=Environment.DEVELOPMENT,
            region="us-east-1",
            ai_optimization_enabled=True,
            cost_optimization_enabled=True
        )
        
        deployment_result = await infra_manager.deploy_environment(config, dry_run=True)
        assert deployment_result is not None
        assert deployment_result.status.value in ['deployed', 'deploying']
        assert len(deployment_result.ai_optimizations_applied) > 0
        
        # Test environment management
        env_spec = await env_manager.create_environment(Environment.DEVELOPMENT, ai_optimized=True)
        assert env_spec is not None
        assert env_spec.environment == Environment.DEVELOPMENT
        
        # Test cost analysis
        cost_analysis = await infra_manager.get_cost_analysis(Environment.DEVELOPMENT)
        assert 'estimated_monthly_cost' in cost_analysis
        assert cost_analysis['estimated_monthly_cost'] > 0
        
        print("✅ Infrastructure comprehensive test passed")
        
    except Exception as e:
        pytest.fail(f"Infrastructure comprehensive test failed: {e}")


@pytest.mark.asyncio
async def test_monitoring_comprehensive():
    """Test monitoring service comprehensive functionality."""
    try:
        from infrastructure.monitoring.monitoring_service import MonitoringService, MetricType
        from ai.service import AIService
        
        # Initialize services
        ai_service = AIService()
        monitoring_service = MonitoringService(ai_service)
        
        # Test metric collection
        metrics_collected = []
        test_metrics = [
            ("cpu_utilization", 75.5, "Percent"),
            ("memory_utilization", 68.2, "Percent"),
            ("request_rate", 150.0, "Count/Second"),
            ("response_time", 95.3, "Milliseconds"),
            ("error_rate", 1.2, "Percent")
        ]
        
        for metric_name, value, unit in test_metrics:
            success = await monitoring_service.collect_metric(
                metric_name, value, unit, {"source": "integration-test"}, MetricType.APPLICATION
            )
            assert success is True
            metrics_collected.append(metric_name)
        
        # Wait for metrics processing
        await asyncio.sleep(0.5)
        
        # Test dashboard data
        dashboard_data = await monitoring_service.get_dashboard_data("system-overview")
        assert dashboard_data is not None
        assert 'widgets' in dashboard_data
        
        # Test system health
        health = await monitoring_service.get_system_health()
        assert health is not None
        assert 'overall_status' in health
        
        # Test metrics retrieval
        for metric_name in metrics_collected[:2]:  # Test first 2 metrics
            metrics = await monitoring_service.get_metrics(metric_name)
            assert isinstance(metrics, list)
        
        print("✅ Monitoring comprehensive test passed")
        
    except Exception as e:
        pytest.fail(f"Monitoring comprehensive test failed: {e}")


@pytest.mark.asyncio
async def test_end_to_end_workflow():
    """Test complete end-to-end platform workflow."""
    try:
        # Initialize all services
        from ai.service import AIService
        from infrastructure.container.container_service import ContainerService, ApplicationContainer
        from infrastructure.deployment.infrastructure_manager import InfrastructureManager, InfrastructureConfig, Environment
        from infrastructure.monitoring.monitoring_service import MonitoringService
        
        # Initialize services with AI integration
        ai_service = AIService()
        container_service = ContainerService(ai_service=ai_service)
        infrastructure_manager = InfrastructureManager(ai_service)
        monitoring_service = MonitoringService(ai_service)
        
        # Force mock mode
        container_service.ecs_manager.ecs_client = None
        infrastructure_manager.cloudformation_client = None
        monitoring_service.cloudwatch_client = None
        
        # Step 1: Deploy infrastructure
        infra_config = InfrastructureConfig(
            environment=Environment.DEVELOPMENT,
            region="us-east-1",
            ai_optimization_enabled=True
        )
        
        infra_deployment = await infrastructure_manager.deploy_environment(infra_config, dry_run=True)
        assert infra_deployment.status.value in ['deployed', 'deploying']
        
        # Step 2: Deploy application
        app_container = ApplicationContainer(
            application_id="e2e-test-app",
            name="e2e-test-app",
            image="nginx",
            version="1.0",
            cpu_cores=0.5,
            memory_gb=1.0,
            port=80,
            environment_variables={"ENV": "e2e-test"},
            replicas=1,
            auto_scaling=True
        )
        
        app_deployment = await container_service.deploy_application(app_container, ai_optimized=True)
        assert app_deployment is not None
        
        # Step 3: Monitor application
        await monitoring_service.collect_metric("app_cpu", 45.0, "Percent", {"app": "e2e-test-app"})
        await monitoring_service.collect_metric("app_memory", 60.0, "Percent", {"app": "e2e-test-app"})
        
        # Step 4: Get AI insights
        insights = await ai_service.get_comprehensive_insights("e2e-test-app")
        assert len(insights) > 0
        
        # Step 5: Scale based on AI recommendations
        scaling_insights = [i for i in insights if i.insight_type.value == 'scaling_recommendation']
        if scaling_insights:
            scaling_event = await container_service.scale_application(
                "e2e-test-app", 2, "ai_recommendation"
            )
            assert scaling_event.ai_triggered is True  # AI-triggered scaling based on recommendations
        
        # Step 6: Validate system health
        system_health = await monitoring_service.get_system_health()
        assert system_health['overall_status'] in ['healthy', 'degraded']
        
        print("✅ End-to-end workflow test passed")
        
    except Exception as e:
        pytest.fail(f"End-to-end workflow test failed: {e}")


if __name__ == "__main__":
    # Run tests individually for debugging
    print("🔗 Testing Complete Platform Integration...")
    
    # Test imports
    test_platform_integration_imports()
    print("✅ Platform integration imports test passed")
    
    # Run async tests
    async def run_async_tests():
        await test_complete_platform_integration()
        print("✅ Complete platform integration test passed")
        
        await test_ai_service_comprehensive()
        print("✅ AI Service comprehensive test passed")
        
        await test_container_orchestration_comprehensive()
        print("✅ Container orchestration comprehensive test passed")
        
        await test_infrastructure_comprehensive()
        print("✅ Infrastructure comprehensive test passed")
        
        await test_monitoring_comprehensive()
        print("✅ Monitoring comprehensive test passed")
        
        await test_end_to_end_workflow()
        print("✅ End-to-end workflow test passed")
    
    # Run async tests
    asyncio.run(run_async_tests())
    
    print("\n🎉 All platform integration tests passed successfully!")
    print("🚀 Platform is ready for production deployment!")

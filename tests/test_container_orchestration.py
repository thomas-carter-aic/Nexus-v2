"""
Test suite for Container Orchestration components.
Tests ECS management, container service, and deployment orchestration.
"""

import pytest
import sys
import asyncio
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_container_orchestration_imports():
    """Test that container orchestration components can be imported."""
    try:
        from infrastructure.container.ecs_manager import ECSManager, ContainerSpec, ServiceConfig
        from infrastructure.container.container_service import ContainerService, ApplicationContainer
        from infrastructure.container.deployment_orchestrator import DeploymentOrchestrator, DeploymentPipeline
        
        assert True, "Container orchestration components imported successfully"
    except ImportError as e:
        pytest.fail(f"Failed to import container orchestration components: {e}")


@pytest.mark.asyncio
async def test_ecs_manager():
    """Test ECS Manager functionality."""
    try:
        from infrastructure.container.ecs_manager import ECSManager, ContainerSpec
        
        # Initialize ECS Manager (force mock mode)
        ecs_manager = ECSManager(region="us-east-1")
        # Force mock mode
        ecs_manager.ecs_client = None
        ecs_manager.ec2_client = None
        ecs_manager.logs_client = None
        ecs_manager.application_autoscaling_client = None
        
        # Test cluster creation
        cluster_info = await ecs_manager.ensure_cluster_exists("test-cluster")
        assert cluster_info is not None
        assert cluster_info['clusterName'] == "test-cluster"
        
        # Test container spec
        container_spec = ContainerSpec(
            name="test-app",
            image="nginx:latest",
            cpu=512,
            memory=1024,
            port=80,
            environment={"ENV": "test"},
            health_check={
                'command': ['CMD-SHELL', 'curl -f http://localhost:80/health || exit 1'],
                'interval': 30,
                'timeout': 5,
                'retries': 3
            }
        )
        
        # Test task definition creation
        task_def_arn = await ecs_manager.create_task_definition(
            "test-app-1", container_spec, ai_optimized=False
        )
        assert task_def_arn is not None
        assert "test-app-1-task" in task_def_arn
        
        print("✅ ECS Manager test passed")
        
    except Exception as e:
        pytest.fail(f"ECS Manager test failed: {e}")


@pytest.mark.asyncio
async def test_container_service():
    """Test Container Service functionality."""
    try:
        from infrastructure.container.container_service import ContainerService, ApplicationContainer
        from ai.service import AIService
        
        # Initialize services
        ai_service = AIService()
        container_service = ContainerService(region="us-east-1", ai_service=ai_service)
        
        # Force mock mode
        container_service.ecs_manager.ecs_client = None
        container_service.ecs_manager.ec2_client = None
        container_service.ecs_manager.logs_client = None
        container_service.ecs_manager.application_autoscaling_client = None
        
        # Create application container configuration
        app_container = ApplicationContainer(
            application_id="test-web-app",
            name="test-web-app",
            image="nginx",
            version="1.21",
            cpu_cores=0.5,
            memory_gb=1.0,
            port=80,
            environment_variables={"ENV": "test", "DEBUG": "false"},
            replicas=2,
            auto_scaling=True
        )
        
        # Test application deployment
        deployment = await container_service.deploy_application(
            app_container, ai_optimized=True
        )
        
        assert deployment is not None
        assert deployment.application_id == "test-web-app"
        assert deployment.version == "1.21"
        
        # Test application status
        status = await container_service.get_application_status("test-web-app")
        assert status['application_id'] == "test-web-app"
        assert status['name'] == "test-web-app"
        assert 'replicas' in status
        assert 'resources' in status
        
        # Test scaling
        scaling_event = await container_service.scale_application(
            "test-web-app", 3, "test_scaling"
        )
        assert scaling_event.application_id == "test-web-app"
        assert scaling_event.new_count == 3
        
        # Test logs retrieval
        logs = await container_service.get_application_logs("test-web-app", lines=10)
        assert isinstance(logs, list)
        assert len(logs) > 0
        
        print("✅ Container Service test passed")
        
    except Exception as e:
        pytest.fail(f"Container Service test failed: {e}")


@pytest.mark.asyncio
async def test_deployment_orchestrator():
    """Test Deployment Orchestrator functionality."""
    try:
        from infrastructure.container.deployment_orchestrator import (
            DeploymentOrchestrator, DeploymentPipeline, DeploymentPhase
        )
        from infrastructure.container.container_service import ContainerService
        from ai.service import AIService
        
        # Initialize services
        ai_service = AIService()
        container_service = ContainerService(ai_service=ai_service)
        
        # Force mock mode
        container_service.ecs_manager.ecs_client = None
        container_service.ecs_manager.ec2_client = None
        container_service.ecs_manager.logs_client = None
        container_service.ecs_manager.application_autoscaling_client = None
        
        orchestrator = DeploymentOrchestrator(container_service, ai_service)
        
        # Test pipeline creation
        pipeline = await orchestrator.create_deployment_pipeline(
            application_id="test-orchestration-app",
            version="1.0.0",
            template_name="web-app-standard"
        )
        
        assert pipeline is not None
        assert pipeline.application_id == "test-orchestration-app"
        assert pipeline.version == "1.0.0"
        assert len(pipeline.steps) > 0
        
        # Test deployment execution
        execution = await orchestrator.execute_deployment(pipeline, auto_approve=True)
        
        assert execution is not None
        assert execution.pipeline.application_id == "test-orchestration-app"
        assert execution.status.value in ['pending', 'in_progress']
        
        # Wait a bit for execution to progress
        await asyncio.sleep(2)
        
        # Test getting deployment status
        status = await orchestrator.get_deployment_status(execution.execution_id)
        assert status is not None
        assert status.execution_id == execution.execution_id
        
        # Test blue/green pipeline
        bg_pipeline = await orchestrator.create_deployment_pipeline(
            application_id="test-bg-app",
            version="2.0.0",
            template_name="blue-green-standard"
        )
        
        assert bg_pipeline.strategy == "blue_green"
        assert bg_pipeline.approval_required == True
        
        print("✅ Deployment Orchestrator test passed")
        
    except Exception as e:
        pytest.fail(f"Deployment Orchestrator test failed: {e}")


@pytest.mark.asyncio
async def test_ai_integration():
    """Test AI integration with container orchestration."""
    try:
        from infrastructure.container.container_service import ContainerService, ApplicationContainer
        from infrastructure.container.deployment_orchestrator import DeploymentOrchestrator
        from ai.service import AIService
        
        # Initialize with AI service
        ai_service = AIService()
        container_service = ContainerService(ai_service=ai_service)
        
        # Force mock mode
        container_service.ecs_manager.ecs_client = None
        container_service.ecs_manager.ec2_client = None
        container_service.ecs_manager.logs_client = None
        container_service.ecs_manager.application_autoscaling_client = None
        
        orchestrator = DeploymentOrchestrator(container_service, ai_service)
        
        # Create application with AI optimization
        app_container = ApplicationContainer(
            application_id="ai-optimized-app",
            name="ai-optimized-app",
            image="nginx",
            version="1.0",
            cpu_cores=1.0,
            memory_gb=2.0,
            port=80,
            environment_variables={},
            replicas=1,
            auto_scaling=True
        )
        
        # Deploy with AI optimization
        deployment = await container_service.deploy_application(
            app_container, ai_optimized=True
        )
        
        assert deployment is not None
        
        # Create pipeline with AI risk assessment
        pipeline = await orchestrator.create_deployment_pipeline(
            "ai-optimized-app", "1.1", "web-app-standard"
        )
        
        # Execute deployment (AI risk assessment will be performed)
        execution = await orchestrator.execute_deployment(pipeline, auto_approve=True)
        
        # Wait for AI risk assessment step
        await asyncio.sleep(3)
        
        # Check if AI insights were generated
        status = await orchestrator.get_deployment_status(execution.execution_id)
        if status and 'ai_risk_assessment' in status.step_results:
            risk_assessment = status.step_results['ai_risk_assessment']['result']
            assert hasattr(risk_assessment, 'risk_level')
            assert hasattr(risk_assessment, 'risk_score')
        
        print("✅ AI Integration test passed")
        
    except Exception as e:
        pytest.fail(f"AI Integration test failed: {e}")


def test_container_orchestration_dependencies():
    """Test that container orchestration dependencies are available."""
    try:
        import boto3
        import asyncio
        from datetime import datetime
        from dataclasses import dataclass
        from enum import Enum
        
        # Test basic functionality
        assert datetime.utcnow() is not None
        
        print("✅ Container orchestration dependencies available")
        
    except ImportError as e:
        pytest.fail(f"Container orchestration dependencies not available: {e}")


if __name__ == "__main__":
    # Run tests individually for debugging
    print("🚢 Testing Container Orchestration...")
    
    # Test imports
    test_container_orchestration_imports()
    print("✅ Container orchestration imports test passed")
    
    # Test dependencies
    test_container_orchestration_dependencies()
    print("✅ Container orchestration dependencies test passed")
    
    # Run async tests
    async def run_async_tests():
        await test_ecs_manager()
        print("✅ ECS Manager test passed")
        
        await test_container_service()
        print("✅ Container Service test passed")
        
        await test_deployment_orchestrator()
        print("✅ Deployment Orchestrator test passed")
        
        await test_ai_integration()
        print("✅ AI Integration test passed")
    
    # Run async tests
    asyncio.run(run_async_tests())
    
    print("\n🎉 All container orchestration tests passed successfully!")

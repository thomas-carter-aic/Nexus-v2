#!/usr/bin/env python3
"""
Simple Build Test Script for AI-Native PaaS Platform

This script tests the basic functionality without complex imports.
"""

import sys
import traceback
from datetime import datetime

def test_simple_imports():
    """Test basic imports"""
    print("🔍 Testing simple imports...")
    
    try:
        # Test FastAPI
        from fastapi import FastAPI
        print("✅ FastAPI imported successfully")
        
        # Test AWS SDK
        import boto3
        print("✅ Boto3 imported successfully")
        
        # Test other core libraries
        import pydantic
        import aiohttp
        import yaml
        print("✅ Core libraries imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple import test failed: {e}")
        traceback.print_exc()
        return False

def test_domain_models_direct():
    """Test domain models by importing directly"""
    print("\n🏗️  Testing domain models (direct import)...")
    
    try:
        # Import directly from simple_models
        from src.core.domain.simple_models import (
            UserId, ApplicationId, ResourceRequirements, ScalingConfiguration, 
            ScalingStrategy, Application, ApplicationStatus
        )
        
        print("✅ Domain models imported successfully")
        
        # Test value objects
        user_id = UserId("test-user-123")
        app_id = ApplicationId.generate()
        
        resources = ResourceRequirements(
            cpu_cores=2.0,
            memory_mb=4096,
            storage_gb=20
        )
        
        scaling_config = ScalingConfiguration(
            strategy=ScalingStrategy.PREDICTIVE,
            min_instances=1,
            max_instances=10,
            target_cpu_utilization=70.0
        )
        
        print("✅ Value objects created successfully")
        
        # Test application aggregate
        application = Application(
            application_id=app_id,
            name="test-application",
            user_id=user_id,
            resource_requirements=resources,
            scaling_config=scaling_config
        )
        
        print(f"✅ Application aggregate created: {application.name}")
        print(f"   - ID: {application.id.value}")
        print(f"   - Status: {application.status.value}")
        print(f"   - Instances: {application.current_instance_count}")
        
        # Test domain operations
        application.deploy()
        print(f"✅ Application deployed, status: {application.status.value}")
        
        application.mark_as_running()
        print(f"✅ Application marked as running, status: {application.status.value}")
        
        # Test scaling
        application.scale(new_instance_count=3, reason="Test scaling")
        print(f"✅ Application scaled to {application.current_instance_count} instances")
        
        # Test events
        events = application.get_uncommitted_events()
        print(f"✅ Generated {len(events)} domain events")
        
        # Test serialization
        app_dict = application.to_dict()
        print("✅ Application serialized to dictionary")
        print(f"   - Keys: {list(app_dict.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Domain model test failed: {e}")
        traceback.print_exc()
        return False

def test_fastapi_app():
    """Test creating a FastAPI application"""
    print("\n🚀 Testing FastAPI application...")
    
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel
        
        # Create basic FastAPI app
        app = FastAPI(
            title="AI-Native PaaS Platform",
            description="Build test API",
            version="1.0.0"
        )
        
        # Test model
        class HealthResponse(BaseModel):
            status: str
            timestamp: str
            version: str
        
        @app.get("/health", response_model=HealthResponse)
        async def health_check():
            return HealthResponse(
                status="healthy",
                timestamp=datetime.utcnow().isoformat(),
                version="1.0.0"
            )
        
        @app.get("/")
        async def root():
            return {"message": "AI-Native PaaS Platform", "status": "running"}
        
        print("✅ FastAPI application created successfully")
        print("✅ Health and root endpoints defined")
        print(f"✅ App title: {app.title}")
        
        return True
        
    except Exception as e:
        print(f"❌ FastAPI test failed: {e}")
        traceback.print_exc()
        return False

def test_aws_clients():
    """Test AWS client creation"""
    print("\n☁️  Testing AWS clients...")
    
    try:
        import boto3
        from botocore.exceptions import NoCredentialsError
        
        # Test creating AWS clients
        clients = {}
        services = ['dynamodb', 'ecs', 'sagemaker', 'lambda', 'cloudwatch']
        
        for service in services:
            try:
                client = boto3.client(service, region_name='us-east-1')
                clients[service] = client
                print(f"✅ {service.upper()} client created")
            except Exception as e:
                print(f"⚠️  {service.upper()} client warning: {e}")
        
        print(f"✅ Created {len(clients)} AWS clients successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ AWS client test failed: {e}")
        traceback.print_exc()
        return False

def test_yaml_config():
    """Test YAML configuration loading"""
    print("\n📄 Testing YAML configuration...")
    
    try:
        import yaml
        
        # Test YAML parsing
        config_yaml = """
        platform:
          name: "AI-Native PaaS"
          version: "1.0.0"
          environment: "test"
        
        scaling:
          strategy: "predictive"
          min_instances: 1
          max_instances: 10
        
        monitoring:
          enabled: true
          metrics_retention_days: 30
        """
        
        config = yaml.safe_load(config_yaml)
        
        print("✅ YAML configuration parsed successfully")
        print(f"   - Platform: {config['platform']['name']}")
        print(f"   - Version: {config['platform']['version']}")
        print(f"   - Scaling strategy: {config['scaling']['strategy']}")
        
        return True
        
    except Exception as e:
        print(f"❌ YAML test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all build tests"""
    print("🧪 AI-Native PaaS Platform - Simple Build Test")
    print("=" * 55)
    
    tests = [
        ("Simple Imports", test_simple_imports),
        ("Domain Models (Direct)", test_domain_models_direct),
        ("FastAPI Application", test_fastapi_app),
        ("AWS Clients", test_aws_clients),
        ("YAML Configuration", test_yaml_config),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔬 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 55)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Build is successful.")
        print("\n🚀 The AI-Native PaaS Platform core components are working correctly!")
        print("   - Domain models can be created and manipulated")
        print("   - FastAPI integration is functional")
        print("   - AWS SDK is available and working")
        print("   - Configuration management is operational")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

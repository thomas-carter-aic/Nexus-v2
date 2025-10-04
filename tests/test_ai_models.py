"""
Test suite for AI/ML models in the AI-Native PaaS Platform.
Tests core AI functionality and model integration.
"""

import pytest
import sys
import asyncio
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_ai_models_import():
    """Test that AI models can be imported successfully."""
    try:
        from ai.models.scaling_predictor import ScalingPredictor, ScalingAction
        from ai.models.anomaly_detector import AnomalyDetector, AnomalySeverity
        from ai.models.cost_optimizer import CostOptimizer, OptimizationStrategy
        from ai.models.performance_predictor import PerformancePredictor, PerformanceMetric
        from ai.models.resource_recommender import ResourceRecommender, WorkloadType
        from ai.service import AIService, AIInsightType
        
        assert True, "AI models imported successfully"
    except ImportError as e:
        pytest.fail(f"Failed to import AI models: {e}")


@pytest.mark.asyncio
async def test_scaling_predictor():
    """Test scaling predictor functionality."""
    try:
        from ai.models.scaling_predictor import ScalingPredictor
        
        predictor = ScalingPredictor()
        
        # Test scaling recommendation
        recommendation = await predictor.generate_scaling_recommendation(
            application_id="test-app-1",
            current_instances=2
        )
        
        assert recommendation is not None
        assert recommendation.application_id == "test-app-1"
        assert recommendation.current_instances == 2
        assert recommendation.confidence >= 0.0
        assert recommendation.confidence <= 1.0
        
        print(f"✅ Scaling recommendation: {recommendation.action} (confidence: {recommendation.confidence:.2f})")
        
    except Exception as e:
        pytest.fail(f"Scaling predictor test failed: {e}")


@pytest.mark.asyncio
async def test_anomaly_detector():
    """Test anomaly detection functionality."""
    try:
        from ai.models.anomaly_detector import AnomalyDetector
        
        detector = AnomalyDetector()
        
        # Test anomaly detection
        anomalies = await detector.detect_anomalies("test-app-2")
        
        assert isinstance(anomalies, list)
        
        if anomalies:
            anomaly = anomalies[0]
            assert anomaly.application_id == "test-app-2"
            assert anomaly.confidence >= 0.0
            assert anomaly.confidence <= 1.0
            assert len(anomaly.recommended_actions) > 0
            
            print(f"✅ Anomaly detected: {anomaly.anomaly_type} (severity: {anomaly.severity})")
        else:
            print("✅ No anomalies detected (normal behavior)")
        
    except Exception as e:
        pytest.fail(f"Anomaly detector test failed: {e}")


@pytest.mark.asyncio
async def test_cost_optimizer():
    """Test cost optimization functionality."""
    try:
        from ai.models.cost_optimizer import CostOptimizer, OptimizationStrategy
        
        optimizer = CostOptimizer()
        
        # Test cost analysis
        cost_analysis = await optimizer.analyze_current_costs("test-app-3")
        
        assert isinstance(cost_analysis, dict)
        assert 'total_monthly_cost' in cost_analysis
        assert cost_analysis['total_monthly_cost'] > 0
        
        # Test optimization recommendations
        recommendations = await optimizer.generate_optimization_recommendations(
            "test-app-3", OptimizationStrategy.BALANCED
        )
        
        assert isinstance(recommendations, list)
        
        if recommendations:
            rec = recommendations[0]
            assert rec.application_id == "test-app-3"
            assert rec.confidence >= 0.0
            assert rec.confidence <= 1.0
            
            print(f"✅ Cost optimization: ${rec.savings:.2f} savings ({rec.savings_percentage:.1f}%)")
        else:
            print("✅ No cost optimizations needed")
        
    except Exception as e:
        pytest.fail(f"Cost optimizer test failed: {e}")


@pytest.mark.asyncio
async def test_performance_predictor():
    """Test performance prediction functionality."""
    try:
        from ai.models.performance_predictor import PerformancePredictor
        
        predictor = PerformancePredictor()
        
        # Test response time prediction
        response_time_pred = await predictor.predict_response_time(
            application_id="test-app-4",
            target_load=1000,
            resource_config={'cpu_cores': 2, 'memory_gb': 4}
        )
        
        assert response_time_pred is not None
        assert response_time_pred.application_id == "test-app-4"
        assert response_time_pred.predicted_value > 0
        assert response_time_pred.confidence_score >= 0.0
        assert response_time_pred.confidence_score <= 1.0
        
        # Test throughput prediction
        throughput_pred = await predictor.predict_throughput(
            application_id="test-app-4",
            resource_config={'cpu_cores': 2, 'memory_gb': 4},
            instance_count=2
        )
        
        assert throughput_pred is not None
        assert throughput_pred.predicted_value > 0
        
        print(f"✅ Performance prediction: {response_time_pred.predicted_value:.1f}ms response time")
        print(f"✅ Throughput prediction: {throughput_pred.predicted_value:.0f} RPS")
        
    except Exception as e:
        pytest.fail(f"Performance predictor test failed: {e}")


@pytest.mark.asyncio
async def test_resource_recommender():
    """Test resource recommendation functionality."""
    try:
        from ai.models.resource_recommender import ResourceRecommender, OptimizationGoal
        
        recommender = ResourceRecommender()
        
        # Test resource recommendation
        current_config = {
            'instance_type': 't3.medium',
            'instance_count': 2,
            'cpu_cores': 2,
            'memory_gb': 4
        }
        
        metrics = {
            'avg_cpu_utilization': 65,
            'avg_memory_utilization': 70,
            'avg_request_rate': 500,
            'avg_response_time': 120,
            'avg_error_rate': 1.2
        }
        
        recommendation = await recommender.generate_recommendation(
            application_id="test-app-5",
            current_config=current_config,
            metrics=metrics,
            optimization_goal=OptimizationGoal.BALANCED
        )
        
        assert recommendation is not None
        assert recommendation.application_id == "test-app-5"
        assert recommendation.confidence >= 0.0
        assert recommendation.confidence <= 1.0
        assert len(recommendation.reasoning) > 0
        
        print(f"✅ Resource recommendation: {recommendation.workload_type} workload")
        print(f"   Recommended: {recommendation.recommended_config.get('instance_type', 'N/A')}")
        
    except Exception as e:
        pytest.fail(f"Resource recommender test failed: {e}")


@pytest.mark.asyncio
async def test_ai_service_integration():
    """Test AI service integration and orchestration."""
    try:
        from ai.service import AIService
        
        ai_service = AIService()
        
        # Test comprehensive insights
        insights = await ai_service.get_comprehensive_insights("test-app-6")
        
        assert isinstance(insights, list)
        
        # Test service health
        health = await ai_service.get_service_health()
        
        assert isinstance(health, dict)
        assert 'status' in health
        assert health['status'] in ['healthy', 'unhealthy']
        
        print(f"✅ AI Service integration: {len(insights)} insights generated")
        print(f"✅ Service health: {health['status']}")
        
        if insights:
            high_priority_insights = [i for i in insights if i.priority in ['high', 'critical']]
            print(f"   High priority insights: {len(high_priority_insights)}")
        
    except Exception as e:
        pytest.fail(f"AI service integration test failed: {e}")


def test_ai_dependencies():
    """Test that AI/ML dependencies are available."""
    try:
        import numpy as np
        import pandas as pd
        import sklearn
        import scipy
        
        # Test basic functionality
        arr = np.array([1, 2, 3, 4, 5])
        assert arr.mean() == 3.0
        
        df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        assert len(df) == 3
        
        print("✅ AI/ML dependencies available and functional")
        
    except ImportError as e:
        pytest.fail(f"AI/ML dependencies not available: {e}")


if __name__ == "__main__":
    # Run tests individually for debugging
    print("🧪 Testing AI Models...")
    
    # Test imports
    test_ai_models_import()
    print("✅ AI models import test passed")
    
    # Test dependencies
    test_ai_dependencies()
    print("✅ AI dependencies test passed")
    
    # Run async tests
    async def run_async_tests():
        await test_scaling_predictor()
        print("✅ Scaling predictor test passed")
        
        await test_anomaly_detector()
        print("✅ Anomaly detector test passed")
        
        await test_cost_optimizer()
        print("✅ Cost optimizer test passed")
        
        await test_performance_predictor()
        print("✅ Performance predictor test passed")
        
        await test_resource_recommender()
        print("✅ Resource recommender test passed")
        
        await test_ai_service_integration()
        print("✅ AI service integration test passed")
    
    # Run async tests
    asyncio.run(run_async_tests())
    
    print("\n🎉 All AI model tests passed successfully!")

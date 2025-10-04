"""
Tests for AI/ML Edge Optimization Module

This module contains comprehensive tests for the AI/ML edge optimization functionality
including model management, optimization, and monitoring.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock

from src.ai_edge import (
    AIEdgeManager,
    AIModel,
    ModelDeployment,
    InferenceEndpoint,
    FederatedLearningJob,
    AIWorkloadType,
    ModelFormat,
    OptimizationTarget,
    AIEdgeOptimizer,
    ModelPlacementStrategy,
    InferenceOptimizationType,
    AIEdgeMonitor,
    InferenceMetrics,
    AIAnomalyDetector,
    ModelPerformanceTracker
)

from src.ai_edge.ai_edge_manager import ModelStatus
from src.ai_edge.ai_edge_monitor import AnomalyType


class TestAIModel:
    """Test AIModel class"""
    
    def test_ai_model_creation(self):
        """Test creating an AI model"""
        model = AIModel(
            model_id='test-model-001',
            name='Test CNN Model',
            version='1.0.0',
            model_format=ModelFormat.TENSORFLOW,
            workload_type=AIWorkloadType.COMPUTER_VISION,
            model_size_mb=150.0,
            input_shape=[224, 224, 3],
            output_shape=[1000],
            framework_version='2.8.0',
            model_path='/models/test/model.pb'
        )
        
        assert model.model_id == 'test-model-001'
        assert model.model_format == ModelFormat.TENSORFLOW
        assert model.workload_type == AIWorkloadType.COMPUTER_VISION
        assert model.model_size_mb == 150.0
        assert model.input_shape == [224, 224, 3]
        
    def test_ai_model_to_dict(self):
        """Test converting AI model to dictionary"""
        model = AIModel(
            model_id='test-model-002',
            name='Test NLP Model',
            version='2.0.0',
            model_format=ModelFormat.PYTORCH,
            workload_type=AIWorkloadType.NLP_PROCESSING,
            model_size_mb=500.0,
            input_shape=[512],
            output_shape=[768],
            framework_version='1.9.0',
            model_path='/models/nlp/model.pth'
        )
        
        model_dict = model.to_dict()
        assert model_dict['model_id'] == 'test-model-002'
        assert model_dict['model_format'] == 'pytorch'
        assert model_dict['workload_type'] == 'nlp_processing'
        assert model_dict['model_size_mb'] == 500.0


class TestModelDeployment:
    """Test ModelDeployment class"""
    
    def test_model_deployment_creation(self):
        """Test creating a model deployment"""
        deployment = ModelDeployment(
            deployment_id='deploy-001',
            model_id='model-001',
            edge_location_id='edge-us-east-1',
            status=ModelStatus.RUNNING,
            optimization_target=OptimizationTarget.LATENCY,
            resource_allocation={'cpu_cores': 2, 'memory_mb': 4096}
        )
        
        assert deployment.deployment_id == 'deploy-001'
        assert deployment.status == ModelStatus.RUNNING
        assert deployment.optimization_target == OptimizationTarget.LATENCY
        assert deployment.resource_allocation['cpu_cores'] == 2
        
    def test_model_deployment_to_dict(self):
        """Test converting model deployment to dictionary"""
        deployment = ModelDeployment(
            deployment_id='deploy-002',
            model_id='model-002',
            edge_location_id='edge-eu-west-1',
            status=ModelStatus.DEPLOYING,
            optimization_target=OptimizationTarget.THROUGHPUT
        )
        
        deployment_dict = deployment.to_dict()
        assert deployment_dict['deployment_id'] == 'deploy-002'
        assert deployment_dict['status'] == 'deploying'
        assert deployment_dict['optimization_target'] == 'throughput'


class TestInferenceEndpoint:
    """Test InferenceEndpoint class"""
    
    def test_inference_endpoint_creation(self):
        """Test creating an inference endpoint"""
        endpoint = InferenceEndpoint(
            endpoint_id='endpoint-001',
            deployment_id='deploy-001',
            endpoint_url='https://edge.example.com/predict',
            model_id='model-001',
            edge_location_id='edge-us-east-1',
            max_batch_size=8,
            timeout_ms=3000
        )
        
        assert endpoint.endpoint_id == 'endpoint-001'
        assert endpoint.endpoint_url == 'https://edge.example.com/predict'
        assert endpoint.max_batch_size == 8
        assert endpoint.timeout_ms == 3000
        
    def test_inference_endpoint_to_dict(self):
        """Test converting inference endpoint to dictionary"""
        endpoint = InferenceEndpoint(
            endpoint_id='endpoint-002',
            deployment_id='deploy-002',
            endpoint_url='https://edge2.example.com/predict',
            model_id='model-002',
            edge_location_id='edge-eu-west-1'
        )
        
        endpoint_dict = endpoint.to_dict()
        assert endpoint_dict['endpoint_id'] == 'endpoint-002'
        assert endpoint_dict['endpoint_url'] == 'https://edge2.example.com/predict'


class TestFederatedLearningJob:
    """Test FederatedLearningJob class"""
    
    def test_federated_learning_job_creation(self):
        """Test creating a federated learning job"""
        job = FederatedLearningJob(
            job_id='fl-job-001',
            name='Test FL Job',
            model_id='model-001',
            participating_locations=['edge-1', 'edge-2', 'edge-3'],
            rounds=10,
            min_participants=2
        )
        
        assert job.job_id == 'fl-job-001'
        assert job.name == 'Test FL Job'
        assert len(job.participating_locations) == 3
        assert job.rounds == 10
        
    def test_federated_learning_job_to_dict(self):
        """Test converting federated learning job to dictionary"""
        job = FederatedLearningJob(
            job_id='fl-job-002',
            name='Advanced FL Job',
            model_id='model-002',
            participating_locations=['edge-a', 'edge-b'],
            differential_privacy=True
        )
        
        job_dict = job.to_dict()
        assert job_dict['job_id'] == 'fl-job-002'
        assert job_dict['differential_privacy'] is True


class TestAIEdgeManager:
    """Test AIEdgeManager class"""
    
    @pytest.fixture
    def ai_manager(self):
        """Create AIEdgeManager instance"""
        return AIEdgeManager()
        
    @pytest.fixture
    def sample_model(self):
        """Create sample AI model"""
        return AIModel(
            model_id='resnet50-test',
            name='ResNet-50 Test',
            version='1.0.0',
            model_format=ModelFormat.TENSORFLOW,
            workload_type=AIWorkloadType.COMPUTER_VISION,
            model_size_mb=98.0,
            input_shape=[224, 224, 3],
            output_shape=[1000],
            framework_version='2.8.0',
            model_path='/models/resnet50/model.pb'
        )
        
    @pytest.mark.asyncio
    async def test_register_model(self, ai_manager, sample_model):
        """Test registering an AI model"""
        result = await ai_manager.register_model(sample_model)
        
        assert result is True
        assert 'resnet50-test' in ai_manager.models
        assert 'resnet50-test' in ai_manager.model_registry
        
    @pytest.mark.asyncio
    async def test_register_invalid_model(self, ai_manager):
        """Test registering an invalid model"""
        invalid_model = AIModel(
            model_id='',  # Invalid empty ID
            name='Invalid Model',
            version='1.0.0',
            model_format=ModelFormat.TENSORFLOW,
            workload_type=AIWorkloadType.COMPUTER_VISION,
            model_size_mb=0,  # Invalid size
            input_shape=[],  # Invalid shape
            output_shape=[],  # Invalid shape
            framework_version='2.8.0',
            model_path='/models/invalid/model.pb'
        )
        
        result = await ai_manager.register_model(invalid_model)
        assert result is False
        
    @pytest.mark.asyncio
    async def test_deploy_model(self, ai_manager, sample_model):
        """Test deploying AI model"""
        await ai_manager.register_model(sample_model)
        
        deployment_ids = await ai_manager.deploy_model(
            'resnet50-test',
            ['edge-us-east-1', 'edge-eu-west-1'],
            OptimizationTarget.LATENCY
        )
        
        assert len(deployment_ids) == 2
        assert all(dep_id in ai_manager.deployments for dep_id in deployment_ids)
        
        # Check deployment details
        deployment = ai_manager.deployments[deployment_ids[0]]
        assert deployment.model_id == 'resnet50-test'
        assert deployment.status == ModelStatus.RUNNING
        assert deployment.optimization_target == OptimizationTarget.LATENCY
        
    @pytest.mark.asyncio
    async def test_create_inference_endpoint(self, ai_manager, sample_model):
        """Test creating inference endpoint"""
        await ai_manager.register_model(sample_model)
        deployment_ids = await ai_manager.deploy_model(
            'resnet50-test',
            ['edge-us-east-1'],
            OptimizationTarget.THROUGHPUT
        )
        
        # The endpoint is already created during deployment
        # Let's verify it exists and has the right properties
        assert len(deployment_ids) > 0
        deployment = ai_manager.deployments[deployment_ids[0]]
        assert deployment.endpoint_url is not None
        
        # Find the endpoint created during deployment
        endpoint = None
        for ep in ai_manager.endpoints.values():
            if ep.deployment_id == deployment_ids[0]:
                endpoint = ep
                break
                
        assert endpoint is not None
        assert endpoint.model_id == 'resnet50-test'
        assert endpoint.edge_location_id == 'edge-us-east-1'
        
    @pytest.mark.asyncio
    async def test_create_federated_learning_job(self, ai_manager, sample_model):
        """Test creating federated learning job"""
        await ai_manager.register_model(sample_model)
        
        fl_job = FederatedLearningJob(
            job_id='fl-resnet-001',
            name='Federated ResNet Training',
            model_id='resnet50-test',
            participating_locations=['edge-1', 'edge-2', 'edge-3'],
            rounds=5,
            min_participants=2
        )
        
        result = await ai_manager.create_federated_learning_job(fl_job)
        
        assert result is True
        assert 'fl-resnet-001' in ai_manager.federated_jobs
        
    @pytest.mark.asyncio
    async def test_get_ai_edge_status(self, ai_manager, sample_model):
        """Test getting AI edge status"""
        await ai_manager.register_model(sample_model)
        await ai_manager.deploy_model('resnet50-test', ['edge-us-east-1'])
        
        status = await ai_manager.get_ai_edge_status()
        
        assert 'models' in status
        assert 'deployments' in status
        assert 'endpoints' in status
        assert status['models']['total'] == 1
        assert status['deployments']['total'] == 1


class TestAIEdgeOptimizer:
    """Test AIEdgeOptimizer class"""
    
    @pytest.fixture
    def ai_manager(self):
        """Create AIEdgeManager instance"""
        return AIEdgeManager()
        
    @pytest.fixture
    def optimizer(self, ai_manager):
        """Create AIEdgeOptimizer instance"""
        return AIEdgeOptimizer(ai_manager)
        
    @pytest.fixture
    def sample_model(self):
        """Create sample AI model"""
        return AIModel(
            model_id='mobilenet-test',
            name='MobileNet Test',
            version='1.0.0',
            model_format=ModelFormat.TENSORFLOW,
            workload_type=AIWorkloadType.COMPUTER_VISION,
            model_size_mb=14.0,
            input_shape=[224, 224, 3],
            output_shape=[1000],
            framework_version='2.8.0',
            model_path='/models/mobilenet/model.pb'
        )
        
    @pytest.mark.asyncio
    async def test_optimize_model_placement(self, optimizer, ai_manager, sample_model):
        """Test optimizing model placement"""
        await ai_manager.register_model(sample_model)
        
        user_locations = [
            {'latitude': 40.7128, 'longitude': -74.0060},  # New York
            {'latitude': 51.5074, 'longitude': -0.1278}    # London
        ]
        
        optimal_locations = await optimizer.optimize_model_placement(
            'mobilenet-test',
            ModelPlacementStrategy.LATENCY_AWARE,
            {'max_locations': 2},
            user_locations
        )
        
        assert len(optimal_locations) <= 2
        assert all(isinstance(loc_id, str) for loc_id in optimal_locations)
        
    @pytest.mark.asyncio
    async def test_optimize_model_inference(self, optimizer, ai_manager, sample_model):
        """Test optimizing model inference"""
        await ai_manager.register_model(sample_model)
        
        optimization_result = await optimizer.optimize_model_inference(
            'mobilenet-test',
            [InferenceOptimizationType.QUANTIZATION, InferenceOptimizationType.PRUNING]
        )
        
        assert optimization_result.success is True
        assert optimization_result.model_id == 'mobilenet-test'
        assert 'latency_ms' in optimization_result.original_metrics
        assert 'latency_ms' in optimization_result.optimized_metrics
        assert len(optimization_result.improvement_percentage) > 0
        
    @pytest.mark.asyncio
    async def test_get_optimization_recommendations(self, optimizer, ai_manager, sample_model):
        """Test getting optimization recommendations"""
        await ai_manager.register_model(sample_model)
        
        recommendations = await optimizer.get_optimization_recommendations(
            'mobilenet-test',
            OptimizationTarget.LATENCY
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Check recommendation structure
        for rec in recommendations:
            assert 'type' in rec
            assert 'priority' in rec
            assert 'expected_improvement' in rec


class TestInferenceMetrics:
    """Test InferenceMetrics class"""
    
    def test_inference_metrics_creation(self):
        """Test creating inference metrics"""
        metrics = InferenceMetrics(
            timestamp=datetime.utcnow(),
            model_id='test-model',
            deployment_id='test-deployment',
            edge_location_id='test-location',
            latency_ms=45.5,
            throughput_rps=120.0,
            accuracy=0.85,
            error_rate=0.01,
            cpu_utilization=65.0,
            memory_utilization=55.0,
            request_count=100
        )
        
        assert metrics.model_id == 'test-model'
        assert metrics.latency_ms == 45.5
        assert metrics.throughput_rps == 120.0
        assert metrics.accuracy == 0.85
        
    def test_inference_metrics_to_dict(self):
        """Test converting inference metrics to dictionary"""
        metrics = InferenceMetrics(
            timestamp=datetime.utcnow(),
            model_id='test-model-2',
            deployment_id='test-deployment-2',
            edge_location_id='test-location-2',
            latency_ms=30.0,
            throughput_rps=150.0
        )
        
        metrics_dict = metrics.to_dict()
        assert metrics_dict['model_id'] == 'test-model-2'
        assert metrics_dict['latency_ms'] == 30.0
        assert metrics_dict['throughput_rps'] == 150.0


class TestModelPerformanceTracker:
    """Test ModelPerformanceTracker class"""
    
    @pytest.fixture
    def tracker(self):
        """Create ModelPerformanceTracker instance"""
        return ModelPerformanceTracker('test-model', window_size=100)
        
    @pytest.fixture
    def sample_metrics(self):
        """Create sample metrics"""
        return InferenceMetrics(
            timestamp=datetime.utcnow(),
            model_id='test-model',
            deployment_id='test-deployment',
            edge_location_id='test-location',
            latency_ms=50.0,
            throughput_rps=100.0,
            error_rate=0.01,
            cpu_utilization=60.0,
            memory_utilization=50.0,
            request_count=50
        )
        
    def test_add_metrics(self, tracker, sample_metrics):
        """Test adding metrics to tracker"""
        tracker.add_metrics(sample_metrics)
        
        assert len(tracker.metrics_history) == 1
        assert tracker.metrics_history[0] == sample_metrics
        
    def test_get_current_performance(self, tracker, sample_metrics):
        """Test getting current performance"""
        # Add multiple metrics
        for i in range(5):
            metrics = InferenceMetrics(
                timestamp=datetime.utcnow(),
                model_id='test-model',
                deployment_id='test-deployment',
                edge_location_id='test-location',
                latency_ms=50.0 + i,
                throughput_rps=100.0 + i,
                error_rate=0.01,
                cpu_utilization=60.0,
                memory_utilization=50.0,
                request_count=50
            )
            tracker.add_metrics(metrics)
            
        performance = tracker.get_current_performance()
        
        assert 'average_latency_ms' in performance
        assert 'average_throughput_rps' in performance
        assert 'average_error_rate' in performance
        assert performance['average_latency_ms'] > 50.0
        
    def test_detect_performance_anomalies(self, tracker):
        """Test detecting performance anomalies"""
        # Add metrics with high latency
        high_latency_metrics = InferenceMetrics(
            timestamp=datetime.utcnow(),
            model_id='test-model',
            deployment_id='test-deployment',
            edge_location_id='test-location',
            latency_ms=1500.0,  # Very high latency
            throughput_rps=10.0,
            error_rate=0.1,  # High error rate
            cpu_utilization=90.0,  # High CPU
            memory_utilization=50.0,
            request_count=10
        )
        
        tracker.add_metrics(high_latency_metrics)
        
        thresholds = {
            'max_latency_ms': 500,
            'max_error_rate': 0.05,
            'max_cpu_utilization': 80
        }
        
        anomalies = tracker.detect_performance_anomalies(thresholds)
        
        assert len(anomalies) > 0
        assert any(a['type'] == 'high_latency' for a in anomalies)
        assert any(a['type'] == 'high_error_rate' for a in anomalies)


class TestAIAnomalyDetector:
    """Test AIAnomalyDetector class"""
    
    @pytest.fixture
    def detector(self):
        """Create AIAnomalyDetector instance"""
        return AIAnomalyDetector()
        
    @pytest.fixture
    def normal_metrics(self):
        """Create normal metrics"""
        return InferenceMetrics(
            timestamp=datetime.utcnow(),
            model_id='test-model',
            deployment_id='test-deployment',
            edge_location_id='test-location',
            latency_ms=50.0,
            throughput_rps=100.0,
            accuracy=0.85,
            error_rate=0.01,
            cpu_utilization=60.0,
            memory_utilization=50.0,
            request_count=100
        )
        
    @pytest.fixture
    def anomalous_metrics(self):
        """Create anomalous metrics"""
        return InferenceMetrics(
            timestamp=datetime.utcnow(),
            model_id='test-model',
            deployment_id='test-deployment',
            edge_location_id='test-location',
            latency_ms=1000.0,  # High latency
            throughput_rps=10.0,
            accuracy=0.60,  # Low accuracy
            error_rate=0.15,  # High error rate
            cpu_utilization=95.0,  # High CPU
            memory_utilization=90.0,  # High memory
            request_count=10
        )
        
    @pytest.mark.asyncio
    async def test_detect_normal_metrics(self, detector, normal_metrics):
        """Test detecting anomalies in normal metrics"""
        anomalies = await detector.detect_anomalies(normal_metrics)
        
        # Should detect no anomalies for normal metrics
        assert len(anomalies) == 0
        
    @pytest.mark.asyncio
    async def test_detect_anomalous_metrics(self, detector, anomalous_metrics):
        """Test detecting anomalies in anomalous metrics"""
        anomalies = await detector.detect_anomalies(anomalous_metrics)
        
        # Should detect multiple anomalies
        assert len(anomalies) > 0
        
        # Check for specific anomaly types
        anomaly_types = [a.anomaly_type for a in anomalies]
        assert AnomalyType.PERFORMANCE_DEGRADATION in anomaly_types
        assert AnomalyType.ERROR_SPIKE in anomaly_types
        assert AnomalyType.RESOURCE_SPIKE in anomaly_types


class TestAIEdgeMonitor:
    """Test AIEdgeMonitor class"""
    
    @pytest.fixture
    def ai_manager(self):
        """Create AIEdgeManager instance"""
        return AIEdgeManager()
        
    @pytest.fixture
    def monitor(self, ai_manager):
        """Create AIEdgeMonitor instance"""
        return AIEdgeMonitor(ai_manager)
        
    @pytest.fixture
    def sample_metrics(self):
        """Create sample metrics"""
        return InferenceMetrics(
            timestamp=datetime.utcnow(),
            model_id='monitor-test-model',
            deployment_id='monitor-test-deployment',
            edge_location_id='monitor-test-location',
            latency_ms=75.0,
            throughput_rps=80.0,
            accuracy=0.82,
            error_rate=0.02,
            cpu_utilization=70.0,
            memory_utilization=60.0,
            request_count=120
        )
        
    @pytest.mark.asyncio
    async def test_start_stop_monitoring(self, monitor):
        """Test starting and stopping monitoring"""
        await monitor.start_monitoring()
        assert monitor.monitoring_active is True
        
        await monitor.stop_monitoring()
        assert monitor.monitoring_active is False
        
    @pytest.mark.asyncio
    async def test_collect_metrics(self, monitor, sample_metrics):
        """Test collecting metrics"""
        await monitor.collect_metrics(sample_metrics)
        
        assert len(monitor.metrics_buffer) == 1
        assert 'monitor-test-model' in monitor.performance_trackers
        
    @pytest.mark.asyncio
    async def test_get_model_performance_summary(self, monitor, sample_metrics):
        """Test getting model performance summary"""
        await monitor.collect_metrics(sample_metrics)
        
        summary = await monitor.get_model_performance_summary('monitor-test-model')
        
        assert summary['model_id'] == 'monitor-test-model'
        assert 'current_performance' in summary
        assert 'health_score' in summary
        assert 'recommendations' in summary
        
    @pytest.mark.asyncio
    async def test_get_monitoring_dashboard(self, monitor, sample_metrics):
        """Test getting monitoring dashboard"""
        await monitor.collect_metrics(sample_metrics)
        
        dashboard = await monitor.get_monitoring_dashboard()
        
        assert 'overview' in dashboard
        assert 'model_health' in dashboard
        assert 'recent_anomalies' in dashboard
        assert dashboard['overview']['total_models_monitored'] == 1


class TestAIEdgeIntegration:
    """Integration tests for AI edge functionality"""
    
    @pytest.mark.asyncio
    async def test_full_ai_edge_workflow(self):
        """Test complete AI edge workflow"""
        # Create components
        ai_manager = AIEdgeManager()
        optimizer = AIEdgeOptimizer(ai_manager)
        monitor = AIEdgeMonitor(ai_manager)
        
        # Create and register model
        model = AIModel(
            model_id='integration-test-model',
            name='Integration Test Model',
            version='1.0.0',
            model_format=ModelFormat.TENSORFLOW,
            workload_type=AIWorkloadType.COMPUTER_VISION,
            model_size_mb=50.0,
            input_shape=[224, 224, 3],
            output_shape=[10],
            framework_version='2.8.0',
            model_path='/models/integration/model.pb'
        )
        
        await ai_manager.register_model(model)
        
        # Optimize placement
        optimal_locations = await optimizer.optimize_model_placement(
            'integration-test-model',
            ModelPlacementStrategy.LATENCY_AWARE,
            {'max_locations': 2}
        )
        
        # If no locations returned, use default locations
        if not optimal_locations:
            optimal_locations = ['edge-us-east-1', 'edge-eu-west-1']
        
        # Deploy model
        deployment_ids = await ai_manager.deploy_model(
            'integration-test-model',
            optimal_locations,
            OptimizationTarget.BALANCED
        )
        
        # Create endpoints
        endpoint_ids = []
        for deployment_id in deployment_ids:
            endpoint_id = await ai_manager.create_inference_endpoint(deployment_id)
            if endpoint_id:
                endpoint_ids.append(endpoint_id)
                
        # Optimize inference
        optimization_result = await optimizer.optimize_model_inference(
            'integration-test-model',
            [InferenceOptimizationType.QUANTIZATION]
        )
        
        # Start monitoring
        await monitor.start_monitoring()
        
        # Collect metrics
        metrics = InferenceMetrics(
            timestamp=datetime.utcnow(),
            model_id='integration-test-model',
            deployment_id=deployment_ids[0] if deployment_ids else 'test-deployment',
            edge_location_id=optimal_locations[0] if optimal_locations else 'test-location',
            latency_ms=35.0,
            throughput_rps=150.0,
            accuracy=0.88,
            error_rate=0.005,
            cpu_utilization=55.0,
            memory_utilization=45.0,
            request_count=200
        )
        
        await monitor.collect_metrics(metrics)
        
        # Verify results
        assert len(deployment_ids) > 0
        assert len(endpoint_ids) > 0
        assert optimization_result.success is True
        
        # Get final status
        ai_status = await ai_manager.get_ai_edge_status()
        performance_summary = await monitor.get_model_performance_summary('integration-test-model')
        dashboard = await monitor.get_monitoring_dashboard()
        
        assert ai_status['models']['total'] == 1
        assert ai_status['deployments']['active'] > 0
        assert performance_summary['model_id'] == 'integration-test-model'
        assert dashboard['overview']['total_models_monitored'] == 1
        
        # Stop monitoring
        await monitor.stop_monitoring()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

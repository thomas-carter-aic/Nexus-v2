"""
Tests for Autonomous Self-Healing Infrastructure Module

This module contains comprehensive tests for the autonomous infrastructure functionality
including predictive maintenance and self-optimization capabilities.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock

from src.autonomous.predictive_maintenance import (
    PredictiveMaintenanceEngine,
    FailurePrediction,
    MaintenanceAction,
    InfrastructureHealth,
    PredictionModel,
    FailureType,
    MaintenanceType,
    HealthStatus
)

from src.autonomous.self_optimizer import (
    SelfOptimizer,
    OptimizationStrategy,
    ArchitectureRefactor,
    PerformanceOptimizer,
    ResourceOptimizer,
    OptimizationType,
    OptimizationScope,
    RefactorType
)


class TestFailurePrediction:
    """Test FailurePrediction class"""
    
    def test_failure_prediction_creation(self):
        """Test creating a failure prediction"""
        prediction = FailurePrediction(
            prediction_id='pred-001',
            resource_id='web-server-1',
            resource_type='compute_instance',
            failure_type=FailureType.PERFORMANCE_DEGRADATION,
            probability=0.85,
            time_to_failure=timedelta(hours=6),
            confidence=0.92,
            impact_severity='high',
            affected_services=['web-service', 'api-service']
        )
        
        assert prediction.prediction_id == 'pred-001'
        assert prediction.failure_type == FailureType.PERFORMANCE_DEGRADATION
        assert prediction.probability == 0.85
        assert prediction.confidence == 0.92
        assert len(prediction.affected_services) == 2
        
    def test_failure_prediction_to_dict(self):
        """Test converting failure prediction to dictionary"""
        prediction = FailurePrediction(
            prediction_id='pred-002',
            resource_id='db-server-1',
            resource_type='database',
            failure_type=FailureType.HARDWARE_FAILURE,
            probability=0.75,
            time_to_failure=timedelta(hours=12),
            confidence=0.88,
            impact_severity='critical'
        )
        
        pred_dict = prediction.to_dict()
        assert pred_dict['prediction_id'] == 'pred-002'
        assert pred_dict['failure_type'] == 'hardware_failure'
        assert pred_dict['probability'] == 0.75
        assert pred_dict['impact_severity'] == 'critical'


class TestMaintenanceAction:
    """Test MaintenanceAction class"""
    
    def test_maintenance_action_creation(self):
        """Test creating a maintenance action"""
        action = MaintenanceAction(
            action_id='action-001',
            prediction_id='pred-001',
            resource_id='web-server-1',
            action_type=MaintenanceType.PREDICTIVE,
            description='Scale up resources to prevent performance degradation',
            priority=8,
            estimated_duration=timedelta(hours=2),
            estimated_cost=1500.0,
            automation_possible=True
        )
        
        assert action.action_id == 'action-001'
        assert action.action_type == MaintenanceType.PREDICTIVE
        assert action.priority == 8
        assert action.automation_possible is True
        assert action.status == 'pending'
        
    def test_maintenance_action_to_dict(self):
        """Test converting maintenance action to dictionary"""
        action = MaintenanceAction(
            action_id='action-002',
            prediction_id='pred-002',
            resource_id='db-server-1',
            action_type=MaintenanceType.EMERGENCY,
            description='Replace failing hardware component',
            priority=10,
            estimated_duration=timedelta(hours=4),
            estimated_cost=5000.0,
            requires_approval=True
        )
        
        action_dict = action.to_dict()
        assert action_dict['action_id'] == 'action-002'
        assert action_dict['action_type'] == 'emergency'
        assert action_dict['priority'] == 10
        assert action_dict['requires_approval'] is True


class TestInfrastructureHealth:
    """Test InfrastructureHealth class"""
    
    def test_infrastructure_health_creation(self):
        """Test creating infrastructure health assessment"""
        health = InfrastructureHealth(
            resource_id='web-server-1',
            resource_type='compute_instance',
            health_status=HealthStatus.WARNING,
            health_score=75.5,
            metrics={'cpu_utilization': 82.0, 'memory_usage': 68.0},
            anomalies=['High CPU utilization'],
            uptime_percentage=99.8
        )
        
        assert health.resource_id == 'web-server-1'
        assert health.health_status == HealthStatus.WARNING
        assert health.health_score == 75.5
        assert 'cpu_utilization' in health.metrics
        assert len(health.anomalies) == 1
        
    def test_infrastructure_health_to_dict(self):
        """Test converting infrastructure health to dictionary"""
        health = InfrastructureHealth(
            resource_id='db-server-1',
            resource_type='database',
            health_status=HealthStatus.HEALTHY,
            health_score=92.3,
            uptime_percentage=99.95
        )
        
        health_dict = health.to_dict()
        assert health_dict['resource_id'] == 'db-server-1'
        assert health_dict['health_status'] == 'healthy'
        assert health_dict['health_score'] == 92.3
        assert health_dict['uptime_percentage'] == 99.95


class TestPredictionModel:
    """Test PredictionModel class"""
    
    @pytest.fixture
    def prediction_model(self):
        """Create PredictionModel instance"""
        return PredictionModel("ensemble")
        
    @pytest.mark.asyncio
    async def test_model_training(self, prediction_model):
        """Test training prediction model"""
        training_data = [
            {'cpu_utilization': 80, 'memory_usage': 70, 'failed': 0},
            {'cpu_utilization': 95, 'memory_usage': 90, 'failed': 1},
            {'cpu_utilization': 60, 'memory_usage': 50, 'failed': 0}
        ]
        
        result = await prediction_model.train(training_data)
        
        assert result is True
        assert prediction_model.trained is True
        assert prediction_model.accuracy > 0
        assert prediction_model.last_training is not None
        
    @pytest.mark.asyncio
    async def test_model_prediction(self, prediction_model):
        """Test making predictions with trained model"""
        # Train model first
        training_data = [{'cpu_utilization': 80, 'memory_usage': 70, 'failed': 0}]
        await prediction_model.train(training_data)
        
        # Make prediction
        features = {'cpu_utilization': 90, 'memory_usage': 85, 'error_rate': 0.05}
        probability, confidence = await prediction_model.predict(features)
        
        assert 0.0 <= probability <= 1.0
        assert 0.0 <= confidence <= 1.0
        
    @pytest.mark.asyncio
    async def test_untrained_model_prediction(self, prediction_model):
        """Test prediction with untrained model"""
        features = {'cpu_utilization': 90, 'memory_usage': 85}
        probability, confidence = await prediction_model.predict(features)
        
        assert probability == 0.0
        assert confidence == 0.0


class TestPredictiveMaintenanceEngine:
    """Test PredictiveMaintenanceEngine class"""
    
    @pytest.fixture
    def maintenance_engine(self):
        """Create PredictiveMaintenanceEngine instance"""
        return PredictiveMaintenanceEngine()
        
    @pytest.mark.asyncio
    async def test_start_stop_monitoring(self, maintenance_engine):
        """Test starting and stopping monitoring"""
        await maintenance_engine.start_monitoring()
        assert maintenance_engine.monitoring_active is True
        
        await maintenance_engine.stop_monitoring()
        assert maintenance_engine.monitoring_active is False
        
    @pytest.mark.asyncio
    async def test_assess_infrastructure_health(self, maintenance_engine):
        """Test assessing infrastructure health"""
        metrics = {
            'cpu_utilization': 75.0,
            'memory_usage': 60.0,
            'disk_usage': 45.0,
            'error_rate': 0.01,
            'response_time': 120.0
        }
        
        health = await maintenance_engine.assess_infrastructure_health(
            'web-server-1', 'compute_instance', metrics
        )
        
        assert health.resource_id == 'web-server-1'
        assert health.resource_type == 'compute_instance'
        assert isinstance(health.health_score, float)
        assert 0.0 <= health.health_score <= 100.0
        assert health.health_status in [HealthStatus.HEALTHY, HealthStatus.WARNING, HealthStatus.CRITICAL, HealthStatus.FAILING]
        
    @pytest.mark.asyncio
    async def test_predict_failures(self, maintenance_engine):
        """Test predicting failures"""
        # Use high utilization metrics to trigger prediction
        metrics = {
            'cpu_utilization': 95.0,
            'memory_usage': 90.0,
            'disk_usage': 85.0,
            'error_rate': 0.08,
            'response_time': 800.0
        }
        
        prediction = await maintenance_engine.predict_failures(
            'web-server-1', 'compute_instance', metrics
        )
        
        # Prediction might be None if probability is below threshold
        if prediction:
            assert prediction.resource_id == 'web-server-1'
            assert isinstance(prediction.probability, float)
            assert 0.0 <= prediction.probability <= 1.0
            assert isinstance(prediction.time_to_failure, timedelta)
            
    @pytest.mark.asyncio
    async def test_create_maintenance_action(self, maintenance_engine):
        """Test creating maintenance action"""
        # Create a prediction first
        prediction = FailurePrediction(
            prediction_id='test-pred-001',
            resource_id='web-server-1',
            resource_type='compute_instance',
            failure_type=FailureType.PERFORMANCE_DEGRADATION,
            probability=0.85,
            time_to_failure=timedelta(hours=6),
            confidence=0.92,
            impact_severity='high'
        )
        
        action = await maintenance_engine.create_maintenance_action(prediction)
        
        assert action.prediction_id == 'test-pred-001'
        assert action.resource_id == 'web-server-1'
        assert isinstance(action.action_type, MaintenanceType)
        assert action.priority >= 1
        assert isinstance(action.estimated_duration, timedelta)
        
    @pytest.mark.asyncio
    async def test_get_maintenance_dashboard(self, maintenance_engine):
        """Test getting maintenance dashboard"""
        dashboard = await maintenance_engine.get_maintenance_dashboard()
        
        assert 'overview' in dashboard
        assert 'health_summary' in dashboard
        assert 'predictions' in dashboard
        assert 'maintenance_actions' in dashboard
        assert 'maintenance_metrics' in dashboard
        
        overview = dashboard['overview']
        assert 'total_predictions' in overview
        assert 'monitoring_status' in overview


class TestOptimizationStrategy:
    """Test OptimizationStrategy class"""
    
    def test_optimization_strategy_creation(self):
        """Test creating optimization strategy"""
        strategy = OptimizationStrategy(
            strategy_id='opt-001',
            name='CPU Performance Optimization',
            optimization_type=OptimizationType.PERFORMANCE,
            scope=OptimizationScope.INFRASTRUCTURE,
            target_metrics={'cpu_utilization': 70.0},
            expected_improvement={'cpu_utilization': -20.0, 'response_time': -30.0},
            implementation_complexity='medium',
            estimated_duration=timedelta(hours=4),
            estimated_cost=2000.0,
            risk_level='low'
        )
        
        assert strategy.strategy_id == 'opt-001'
        assert strategy.optimization_type == OptimizationType.PERFORMANCE
        assert strategy.scope == OptimizationScope.INFRASTRUCTURE
        assert strategy.implementation_complexity == 'medium'
        assert strategy.risk_level == 'low'
        
    def test_optimization_strategy_to_dict(self):
        """Test converting optimization strategy to dictionary"""
        strategy = OptimizationStrategy(
            strategy_id='opt-002',
            name='Database Optimization',
            optimization_type=OptimizationType.PERFORMANCE,
            scope=OptimizationScope.DATABASE,
            target_metrics={'db_response_time': 200.0},
            expected_improvement={'db_response_time': -60.0},
            implementation_complexity='high',
            estimated_duration=timedelta(hours=8),
            estimated_cost=5000.0,
            risk_level='medium'
        )
        
        strategy_dict = strategy.to_dict()
        assert strategy_dict['strategy_id'] == 'opt-002'
        assert strategy_dict['optimization_type'] == 'performance'
        assert strategy_dict['scope'] == 'database'
        assert strategy_dict['implementation_complexity'] == 'high'


class TestArchitectureRefactor:
    """Test ArchitectureRefactor class"""
    
    def test_architecture_refactor_creation(self):
        """Test creating architecture refactor"""
        refactor = ArchitectureRefactor(
            refactor_id='refactor-001',
            strategy_id='opt-001',
            refactor_type=RefactorType.RESOURCE_RIGHTSIZING,
            target_components=['web-server-1', 'web-server-2'],
            description='Rightsize web servers based on utilization',
            status='planned',
            progress=0.0
        )
        
        assert refactor.refactor_id == 'refactor-001'
        assert refactor.refactor_type == RefactorType.RESOURCE_RIGHTSIZING
        assert len(refactor.target_components) == 2
        assert refactor.status == 'planned'
        assert refactor.progress == 0.0
        
    def test_architecture_refactor_to_dict(self):
        """Test converting architecture refactor to dictionary"""
        refactor = ArchitectureRefactor(
            refactor_id='refactor-002',
            strategy_id='opt-002',
            refactor_type=RefactorType.DATABASE_OPTIMIZATION,
            target_components=['db-primary'],
            description='Optimize database performance',
            status='running',
            progress=45.0
        )
        
        refactor_dict = refactor.to_dict()
        assert refactor_dict['refactor_id'] == 'refactor-002'
        assert refactor_dict['refactor_type'] == 'database_optimization'
        assert refactor_dict['status'] == 'running'
        assert refactor_dict['progress'] == 45.0


class TestPerformanceOptimizer:
    """Test PerformanceOptimizer class"""
    
    @pytest.fixture
    def performance_optimizer(self):
        """Create PerformanceOptimizer instance"""
        return PerformanceOptimizer()
        
    @pytest.mark.asyncio
    async def test_analyze_performance_bottlenecks(self, performance_optimizer):
        """Test analyzing performance bottlenecks"""
        metrics = {
            'cpu_utilization': 85.0,
            'memory_utilization': 90.0,
            'db_response_time': 600.0,
            'network_latency': 120.0
        }
        
        bottlenecks = await performance_optimizer.analyze_performance_bottlenecks(metrics)
        
        assert isinstance(bottlenecks, list)
        assert len(bottlenecks) > 0
        
        # Check bottleneck structure
        for bottleneck in bottlenecks:
            assert 'type' in bottleneck
            assert 'severity' in bottleneck
            assert 'description' in bottleneck
            assert 'recommendations' in bottleneck
            
    @pytest.mark.asyncio
    async def test_generate_performance_optimizations(self, performance_optimizer):
        """Test generating performance optimizations"""
        bottlenecks = [
            {
                'type': 'cpu',
                'severity': 'high',
                'description': 'High CPU utilization: 90.0%',
                'recommendations': ['Scale up compute resources']
            },
            {
                'type': 'database',
                'severity': 'medium',
                'description': 'Slow database response: 600.0ms',
                'recommendations': ['Optimize database queries']
            }
        ]
        
        strategies = await performance_optimizer.generate_performance_optimizations(bottlenecks)
        
        assert isinstance(strategies, list)
        assert len(strategies) > 0
        
        for strategy in strategies:
            assert isinstance(strategy, OptimizationStrategy)
            assert strategy.optimization_type == OptimizationType.PERFORMANCE


class TestResourceOptimizer:
    """Test ResourceOptimizer class"""
    
    @pytest.fixture
    def resource_optimizer(self):
        """Create ResourceOptimizer instance"""
        return ResourceOptimizer()
        
    @pytest.mark.asyncio
    async def test_analyze_resource_utilization(self, resource_optimizer):
        """Test analyzing resource utilization"""
        resources = {
            'web-server-1': {
                'cpu_utilization': 15.0,
                'memory_utilization': 25.0,
                'cost_per_hour': 0.50
            },
            'web-server-2': {
                'cpu_utilization': 85.0,
                'memory_utilization': 90.0,
                'cost_per_hour': 1.00
            }
        }
        
        analysis = await resource_optimizer.analyze_resource_utilization(resources)
        
        assert 'underutilized_resources' in analysis
        assert 'overutilized_resources' in analysis
        assert 'rightsizing_opportunities' in analysis
        assert 'cost_optimization_potential' in analysis
        
        assert len(analysis['underutilized_resources']) > 0
        assert len(analysis['overutilized_resources']) > 0
        
    @pytest.mark.asyncio
    async def test_generate_rightsizing_recommendations(self, resource_optimizer):
        """Test generating rightsizing recommendations"""
        analysis = {
            'underutilized_resources': [
                {
                    'resource_id': 'web-server-1',
                    'cpu_utilization': 15.0,
                    'memory_utilization': 25.0,
                    'recommendation': 'downsize',
                    'potential_savings': 0.25
                }
            ],
            'overutilized_resources': [
                {
                    'resource_id': 'web-server-2',
                    'cpu_utilization': 85.0,
                    'memory_utilization': 90.0,
                    'recommendation': 'upsize',
                    'urgency': 'high'
                }
            ],
            'cost_optimization_potential': 180.0
        }
        
        strategies = await resource_optimizer.generate_rightsizing_recommendations(analysis)
        
        assert isinstance(strategies, list)
        assert len(strategies) > 0
        
        for strategy in strategies:
            assert isinstance(strategy, OptimizationStrategy)


class TestSelfOptimizer:
    """Test SelfOptimizer class"""
    
    @pytest.fixture
    def self_optimizer(self):
        """Create SelfOptimizer instance"""
        return SelfOptimizer()
        
    @pytest.mark.asyncio
    async def test_start_stop_optimization(self, self_optimizer):
        """Test starting and stopping optimization"""
        await self_optimizer.start_optimization()
        assert self_optimizer.optimization_active is True
        
        await self_optimizer.stop_optimization()
        assert self_optimizer.optimization_active is False
        
    @pytest.mark.asyncio
    async def test_analyze_system_performance(self, self_optimizer):
        """Test analyzing system performance"""
        system_metrics = {
            'cpu_utilization': 75.0,
            'memory_utilization': 65.0,
            'response_time': 200.0,
            'throughput': 500.0,
            'error_rate': 0.02,
            'db_response_time': 300.0,
            'resources': {
                'web-server-1': {
                    'cpu_utilization': 15.0,
                    'memory_utilization': 25.0,
                    'cost_per_hour': 0.50
                }
            }
        }
        
        analysis = await self_optimizer.analyze_system_performance(system_metrics)
        
        assert 'performance_score' in analysis
        assert 'bottlenecks' in analysis
        assert 'resource_analysis' in analysis
        assert 'optimization_opportunities' in analysis
        assert 'estimated_improvements' in analysis
        assert 'recommended_actions' in analysis
        
        assert isinstance(analysis['performance_score'], float)
        assert 0.0 <= analysis['performance_score'] <= 100.0
        
    @pytest.mark.asyncio
    async def test_get_optimization_dashboard(self, self_optimizer):
        """Test getting optimization dashboard"""
        dashboard = await self_optimizer.get_optimization_dashboard()
        
        assert 'overview' in dashboard
        assert 'recent_optimizations' in dashboard
        assert 'optimization_metrics' in dashboard
        assert 'upcoming_optimizations' in dashboard
        
        overview = dashboard['overview']
        assert 'optimization_status' in overview
        assert 'total_strategies' in overview
        assert 'active_refactors' in overview


class TestAutonomousIntegration:
    """Integration tests for autonomous infrastructure functionality"""
    
    @pytest.mark.asyncio
    async def test_full_autonomous_workflow(self):
        """Test complete autonomous infrastructure workflow"""
        # Create components
        maintenance_engine = PredictiveMaintenanceEngine()
        self_optimizer = SelfOptimizer()
        
        # Start monitoring and optimization
        await maintenance_engine.start_monitoring()
        await self_optimizer.start_optimization()
        
        # Simulate system with issues
        problematic_metrics = {
            'cpu_utilization': 95.0,
            'memory_utilization': 90.0,
            'disk_usage': 85.0,
            'error_rate': 0.08,
            'response_time': 800.0,
            'db_response_time': 1200.0,
            'resources': {
                'web-server-1': {
                    'cpu_utilization': 15.0,  # Underutilized
                    'memory_utilization': 20.0,
                    'cost_per_hour': 2.00
                },
                'web-server-2': {
                    'cpu_utilization': 95.0,  # Overutilized
                    'memory_utilization': 92.0,
                    'cost_per_hour': 1.00
                }
            }
        }
        
        # Test predictive maintenance
        health = await maintenance_engine.assess_infrastructure_health(
            'web-server-2', 'compute_instance', {
                'cpu_utilization': 95.0,
                'memory_utilization': 90.0,
                'error_rate': 0.08
            }
        )
        
        prediction = await maintenance_engine.predict_failures(
            'web-server-2', 'compute_instance', {
                'cpu_utilization': 95.0,
                'memory_utilization': 90.0,
                'error_rate': 0.08
            }
        )
        
        # Test self-optimization
        optimization_analysis = await self_optimizer.analyze_system_performance(problematic_metrics)
        
        # Verify results
        assert health.health_status in [HealthStatus.WARNING, HealthStatus.CRITICAL, HealthStatus.FAILING]
        
        if prediction:
            assert prediction.probability > 0
            assert prediction.impact_severity in ['medium', 'high', 'critical']
            
            # Create and potentially execute maintenance action
            action = await maintenance_engine.create_maintenance_action(prediction)
            assert action.resource_id == 'web-server-2'
            
        assert optimization_analysis['performance_score'] < 80  # Should be low due to high utilization
        assert len(optimization_analysis['bottlenecks']) > 0
        assert len(optimization_analysis['optimization_opportunities']) > 0
        
        # Get dashboards
        maintenance_dashboard = await maintenance_engine.get_maintenance_dashboard()
        optimization_dashboard = await self_optimizer.get_optimization_dashboard()
        
        assert maintenance_dashboard['overview']['monitoring_status'] == 'active'
        assert optimization_dashboard['overview']['optimization_status'] == 'active'
        
        # Stop monitoring and optimization
        await maintenance_engine.stop_monitoring()
        await self_optimizer.stop_optimization()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

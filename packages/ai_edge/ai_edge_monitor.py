"""
AI/ML Edge Monitor

This module provides comprehensive monitoring and analytics for AI/ML workloads at the edge,
including performance tracking, anomaly detection, and real-time optimization.
"""

import asyncio
import json
import numpy as np
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union, Set, Tuple
from dataclasses import dataclass, field
from uuid import UUID, uuid4
import logging
from collections import deque

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of AI metrics"""
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    ACCURACY = "accuracy"
    ERROR_RATE = "error_rate"
    RESOURCE_UTILIZATION = "resource_utilization"
    COST = "cost"
    AVAILABILITY = "availability"
    DRIFT = "drift"


class AnomalyType(Enum):
    """Types of anomalies"""
    PERFORMANCE_DEGRADATION = "performance_degradation"
    ACCURACY_DROP = "accuracy_drop"
    RESOURCE_SPIKE = "resource_spike"
    ERROR_SPIKE = "error_spike"
    DRIFT_DETECTED = "drift_detected"
    AVAILABILITY_DROP = "availability_drop"


@dataclass
class InferenceMetrics:
    """Metrics for AI inference operations"""
    timestamp: datetime
    model_id: str
    deployment_id: str
    edge_location_id: str
    latency_ms: float
    throughput_rps: float
    accuracy: Optional[float] = None
    error_rate: float = 0.0
    cpu_utilization: float = 0.0
    memory_utilization: float = 0.0
    gpu_utilization: float = 0.0
    request_count: int = 0
    batch_size: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'model_id': self.model_id,
            'deployment_id': self.deployment_id,
            'edge_location_id': self.edge_location_id,
            'latency_ms': self.latency_ms,
            'throughput_rps': self.throughput_rps,
            'accuracy': self.accuracy,
            'error_rate': self.error_rate,
            'cpu_utilization': self.cpu_utilization,
            'memory_utilization': self.memory_utilization,
            'gpu_utilization': self.gpu_utilization,
            'request_count': self.request_count,
            'batch_size': self.batch_size
        }


@dataclass
class AIAnomaly:
    """Represents an AI-related anomaly"""
    anomaly_id: str
    anomaly_type: AnomalyType
    model_id: str
    deployment_id: str
    edge_location_id: str
    severity: str  # low, medium, high, critical
    description: str
    metrics: Dict[str, float]
    threshold_values: Dict[str, float]
    detected_at: datetime
    resolved_at: Optional[datetime] = None
    resolution_action: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'anomaly_id': self.anomaly_id,
            'anomaly_type': self.anomaly_type.value,
            'model_id': self.model_id,
            'deployment_id': self.deployment_id,
            'edge_location_id': self.edge_location_id,
            'severity': self.severity,
            'description': self.description,
            'metrics': self.metrics,
            'threshold_values': self.threshold_values,
            'detected_at': self.detected_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'resolution_action': self.resolution_action
        }


class ModelPerformanceTracker:
    """Tracks performance metrics for AI models"""
    
    def __init__(self, model_id: str, window_size: int = 1000):
        self.model_id = model_id
        self.window_size = window_size
        self.metrics_history = deque(maxlen=window_size)
        self.baseline_metrics = {}
        self.performance_trends = {}
        
    def add_metrics(self, metrics: InferenceMetrics):
        """Add new metrics to tracker"""
        self.metrics_history.append(metrics)
        self._update_trends()
        
    def _update_trends(self):
        """Update performance trends"""
        if len(self.metrics_history) < 10:
            return
            
        recent_metrics = list(self.metrics_history)[-10:]
        older_metrics = list(self.metrics_history)[-20:-10] if len(self.metrics_history) >= 20 else []
        
        if not older_metrics:
            return
            
        # Calculate trends
        recent_latency = np.mean([m.latency_ms for m in recent_metrics])
        older_latency = np.mean([m.latency_ms for m in older_metrics])
        
        recent_throughput = np.mean([m.throughput_rps for m in recent_metrics])
        older_throughput = np.mean([m.throughput_rps for m in older_metrics])
        
        recent_error_rate = np.mean([m.error_rate for m in recent_metrics])
        older_error_rate = np.mean([m.error_rate for m in older_metrics])
        
        self.performance_trends = {
            'latency_trend': (recent_latency - older_latency) / older_latency * 100 if older_latency > 0 else 0,
            'throughput_trend': (recent_throughput - older_throughput) / older_throughput * 100 if older_throughput > 0 else 0,
            'error_rate_trend': (recent_error_rate - older_error_rate) / older_error_rate * 100 if older_error_rate > 0 else 0
        }
        
    def get_current_performance(self) -> Dict[str, float]:
        """Get current performance metrics"""
        if not self.metrics_history:
            return {}
            
        recent_metrics = list(self.metrics_history)[-10:]
        
        return {
            'average_latency_ms': np.mean([m.latency_ms for m in recent_metrics]),
            'average_throughput_rps': np.mean([m.throughput_rps for m in recent_metrics]),
            'average_error_rate': np.mean([m.error_rate for m in recent_metrics]),
            'average_cpu_utilization': np.mean([m.cpu_utilization for m in recent_metrics]),
            'average_memory_utilization': np.mean([m.memory_utilization for m in recent_metrics]),
            'total_requests': sum([m.request_count for m in recent_metrics])
        }
        
    def detect_performance_anomalies(self, thresholds: Dict[str, float]) -> List[Dict[str, Any]]:
        """Detect performance anomalies"""
        anomalies = []
        current_perf = self.get_current_performance()
        
        # Check latency anomaly
        if current_perf.get('average_latency_ms', 0) > thresholds.get('max_latency_ms', 1000):
            anomalies.append({
                'type': 'high_latency',
                'current_value': current_perf['average_latency_ms'],
                'threshold': thresholds['max_latency_ms'],
                'severity': 'high' if current_perf['average_latency_ms'] > thresholds['max_latency_ms'] * 2 else 'medium'
            })
            
        # Check error rate anomaly
        if current_perf.get('average_error_rate', 0) > thresholds.get('max_error_rate', 0.05):
            anomalies.append({
                'type': 'high_error_rate',
                'current_value': current_perf['average_error_rate'],
                'threshold': thresholds['max_error_rate'],
                'severity': 'critical' if current_perf['average_error_rate'] > 0.1 else 'high'
            })
            
        # Check resource utilization
        if current_perf.get('average_cpu_utilization', 0) > thresholds.get('max_cpu_utilization', 80):
            anomalies.append({
                'type': 'high_cpu_utilization',
                'current_value': current_perf['average_cpu_utilization'],
                'threshold': thresholds['max_cpu_utilization'],
                'severity': 'medium'
            })
            
        return anomalies


class AIAnomalyDetector:
    """Advanced anomaly detector for AI workloads"""
    
    def __init__(self):
        self.detection_models = {}
        self.anomaly_history = {}
        self.thresholds = {
            'latency_percentile_95': 500,  # ms
            'error_rate_threshold': 0.05,  # 5%
            'accuracy_drop_threshold': 0.1,  # 10%
            'resource_spike_threshold': 0.8,  # 80%
            'drift_threshold': 0.2  # 20%
        }
        
    async def detect_anomalies(self, metrics: InferenceMetrics) -> List[AIAnomaly]:
        """Detect anomalies in AI metrics"""
        anomalies = []
        
        try:
            # Performance degradation detection
            perf_anomalies = await self._detect_performance_anomalies(metrics)
            anomalies.extend(perf_anomalies)
            
            # Accuracy drop detection
            accuracy_anomalies = await self._detect_accuracy_anomalies(metrics)
            anomalies.extend(accuracy_anomalies)
            
            # Resource spike detection
            resource_anomalies = await self._detect_resource_anomalies(metrics)
            anomalies.extend(resource_anomalies)
            
            # Error spike detection
            error_anomalies = await self._detect_error_anomalies(metrics)
            anomalies.extend(error_anomalies)
            
        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            
        return anomalies
        
    async def _detect_performance_anomalies(self, metrics: InferenceMetrics) -> List[AIAnomaly]:
        """Detect performance-related anomalies"""
        anomalies = []
        
        # High latency detection
        if metrics.latency_ms > self.thresholds['latency_percentile_95']:
            severity = 'critical' if metrics.latency_ms > self.thresholds['latency_percentile_95'] * 2 else 'high'
            
            anomaly = AIAnomaly(
                anomaly_id=f"perf-{metrics.deployment_id}-{str(uuid4())[:8]}",
                anomaly_type=AnomalyType.PERFORMANCE_DEGRADATION,
                model_id=metrics.model_id,
                deployment_id=metrics.deployment_id,
                edge_location_id=metrics.edge_location_id,
                severity=severity,
                description=f"High inference latency detected: {metrics.latency_ms:.2f}ms",
                metrics={'latency_ms': metrics.latency_ms},
                threshold_values={'max_latency_ms': self.thresholds['latency_percentile_95']},
                detected_at=datetime.utcnow()
            )
            
            anomalies.append(anomaly)
            
        return anomalies
        
    async def _detect_accuracy_anomalies(self, metrics: InferenceMetrics) -> List[AIAnomaly]:
        """Detect accuracy-related anomalies"""
        anomalies = []
        
        if metrics.accuracy is not None:
            # Get baseline accuracy for comparison
            baseline_accuracy = await self._get_baseline_accuracy(metrics.model_id)
            
            if baseline_accuracy and metrics.accuracy < baseline_accuracy * (1 - self.thresholds['accuracy_drop_threshold']):
                anomaly = AIAnomaly(
                    anomaly_id=f"acc-{metrics.deployment_id}-{str(uuid4())[:8]}",
                    anomaly_type=AnomalyType.ACCURACY_DROP,
                    model_id=metrics.model_id,
                    deployment_id=metrics.deployment_id,
                    edge_location_id=metrics.edge_location_id,
                    severity='high',
                    description=f"Model accuracy drop detected: {metrics.accuracy:.3f} vs baseline {baseline_accuracy:.3f}",
                    metrics={'accuracy': metrics.accuracy, 'baseline_accuracy': baseline_accuracy},
                    threshold_values={'min_accuracy': baseline_accuracy * (1 - self.thresholds['accuracy_drop_threshold'])},
                    detected_at=datetime.utcnow()
                )
                
                anomalies.append(anomaly)
                
        return anomalies
        
    async def _detect_resource_anomalies(self, metrics: InferenceMetrics) -> List[AIAnomaly]:
        """Detect resource utilization anomalies"""
        anomalies = []
        
        # CPU spike detection
        if metrics.cpu_utilization > self.thresholds['resource_spike_threshold'] * 100:
            anomaly = AIAnomaly(
                anomaly_id=f"cpu-{metrics.deployment_id}-{str(uuid4())[:8]}",
                anomaly_type=AnomalyType.RESOURCE_SPIKE,
                model_id=metrics.model_id,
                deployment_id=metrics.deployment_id,
                edge_location_id=metrics.edge_location_id,
                severity='medium',
                description=f"High CPU utilization: {metrics.cpu_utilization:.1f}%",
                metrics={'cpu_utilization': metrics.cpu_utilization},
                threshold_values={'max_cpu_utilization': self.thresholds['resource_spike_threshold'] * 100},
                detected_at=datetime.utcnow()
            )
            
            anomalies.append(anomaly)
            
        # Memory spike detection
        if metrics.memory_utilization > self.thresholds['resource_spike_threshold'] * 100:
            anomaly = AIAnomaly(
                anomaly_id=f"mem-{metrics.deployment_id}-{str(uuid4())[:8]}",
                anomaly_type=AnomalyType.RESOURCE_SPIKE,
                model_id=metrics.model_id,
                deployment_id=metrics.deployment_id,
                edge_location_id=metrics.edge_location_id,
                severity='medium',
                description=f"High memory utilization: {metrics.memory_utilization:.1f}%",
                metrics={'memory_utilization': metrics.memory_utilization},
                threshold_values={'max_memory_utilization': self.thresholds['resource_spike_threshold'] * 100},
                detected_at=datetime.utcnow()
            )
            
            anomalies.append(anomaly)
            
        return anomalies
        
    async def _detect_error_anomalies(self, metrics: InferenceMetrics) -> List[AIAnomaly]:
        """Detect error rate anomalies"""
        anomalies = []
        
        if metrics.error_rate > self.thresholds['error_rate_threshold']:
            severity = 'critical' if metrics.error_rate > 0.1 else 'high'
            
            anomaly = AIAnomaly(
                anomaly_id=f"err-{metrics.deployment_id}-{str(uuid4())[:8]}",
                anomaly_type=AnomalyType.ERROR_SPIKE,
                model_id=metrics.model_id,
                deployment_id=metrics.deployment_id,
                edge_location_id=metrics.edge_location_id,
                severity=severity,
                description=f"High error rate: {metrics.error_rate:.3f}",
                metrics={'error_rate': metrics.error_rate},
                threshold_values={'max_error_rate': self.thresholds['error_rate_threshold']},
                detected_at=datetime.utcnow()
            )
            
            anomalies.append(anomaly)
            
        return anomalies
        
    async def _get_baseline_accuracy(self, model_id: str) -> Optional[float]:
        """Get baseline accuracy for model"""
        # In production, this would query historical data
        # For now, return a mock baseline
        baseline_accuracies = {
            'resnet50-v1': 0.76,
            'mobilenet-v2': 0.72,
            'bert-base': 0.85,
            'gpt-3.5': 0.90
        }
        
        return baseline_accuracies.get(model_id, 0.80)


class AIEdgeMonitor:
    """
    Comprehensive AI/ML edge monitoring system
    """
    
    def __init__(self, ai_edge_manager=None):
        self.ai_edge_manager = ai_edge_manager
        self.performance_trackers: Dict[str, ModelPerformanceTracker] = {}
        self.anomaly_detector = AIAnomalyDetector()
        self.metrics_buffer = deque(maxlen=10000)
        self.active_anomalies: Dict[str, AIAnomaly] = {}
        self.monitoring_active = False
        
    async def start_monitoring(self):
        """Start AI edge monitoring"""
        self.monitoring_active = True
        
        # Start background monitoring tasks
        asyncio.create_task(self._metrics_collection_loop())
        asyncio.create_task(self._anomaly_detection_loop())
        asyncio.create_task(self._performance_analysis_loop())
        
        logger.info("AI edge monitoring started")
        
    async def stop_monitoring(self):
        """Stop AI edge monitoring"""
        self.monitoring_active = False
        logger.info("AI edge monitoring stopped")
        
    async def collect_metrics(self, metrics: InferenceMetrics):
        """Collect AI inference metrics"""
        try:
            # Add to buffer
            self.metrics_buffer.append(metrics)
            
            # Update performance tracker
            if metrics.model_id not in self.performance_trackers:
                self.performance_trackers[metrics.model_id] = ModelPerformanceTracker(metrics.model_id)
                
            self.performance_trackers[metrics.model_id].add_metrics(metrics)
            
            # Detect anomalies
            anomalies = await self.anomaly_detector.detect_anomalies(metrics)
            
            # Store active anomalies
            for anomaly in anomalies:
                self.active_anomalies[anomaly.anomaly_id] = anomaly
                logger.warning(f"AI anomaly detected: {anomaly.description}")
                
        except Exception as e:
            logger.error(f"Error collecting AI metrics: {e}")
            
    async def get_model_performance_summary(self, model_id: str) -> Dict[str, Any]:
        """Get performance summary for specific model"""
        try:
            if model_id not in self.performance_trackers:
                return {}
                
            tracker = self.performance_trackers[model_id]
            current_perf = tracker.get_current_performance()
            
            # Get recent anomalies
            recent_anomalies = [
                anomaly for anomaly in self.active_anomalies.values()
                if anomaly.model_id == model_id and 
                (datetime.utcnow() - anomaly.detected_at).total_seconds() < 3600  # Last hour
            ]
            
            summary = {
                'model_id': model_id,
                'current_performance': current_perf,
                'performance_trends': tracker.performance_trends,
                'recent_anomalies': len(recent_anomalies),
                'anomaly_details': [anomaly.to_dict() for anomaly in recent_anomalies],
                'health_score': await self._calculate_health_score(model_id),
                'recommendations': await self._get_performance_recommendations(model_id)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting performance summary: {e}")
            return {}
            
    async def _calculate_health_score(self, model_id: str) -> float:
        """Calculate health score for model (0-100)"""
        try:
            if model_id not in self.performance_trackers:
                return 0.0
                
            tracker = self.performance_trackers[model_id]
            current_perf = tracker.get_current_performance()
            
            # Base score
            score = 100.0
            
            # Deduct for high latency
            avg_latency = current_perf.get('average_latency_ms', 0)
            if avg_latency > 500:
                score -= min(30, (avg_latency - 500) / 10)
                
            # Deduct for high error rate
            error_rate = current_perf.get('average_error_rate', 0)
            if error_rate > 0.01:
                score -= min(40, error_rate * 1000)
                
            # Deduct for resource issues
            cpu_util = current_perf.get('average_cpu_utilization', 0)
            if cpu_util > 80:
                score -= min(20, (cpu_util - 80) / 2)
                
            # Deduct for active anomalies
            active_anomalies = len([
                a for a in self.active_anomalies.values()
                if a.model_id == model_id and not a.resolved_at
            ])
            score -= min(30, active_anomalies * 10)
            
            return max(0.0, score)
            
        except Exception as e:
            logger.error(f"Error calculating health score: {e}")
            return 0.0
            
    async def _get_performance_recommendations(self, model_id: str) -> List[Dict[str, Any]]:
        """Get performance recommendations for model"""
        recommendations = []
        
        try:
            if model_id not in self.performance_trackers:
                return recommendations
                
            tracker = self.performance_trackers[model_id]
            current_perf = tracker.get_current_performance()
            
            # High latency recommendations
            if current_perf.get('average_latency_ms', 0) > 200:
                recommendations.append({
                    'type': 'optimization',
                    'priority': 'high',
                    'title': 'Reduce inference latency',
                    'description': 'Consider model quantization or pruning to reduce inference time',
                    'expected_impact': '20-40% latency reduction'
                })
                
            # High error rate recommendations
            if current_perf.get('average_error_rate', 0) > 0.02:
                recommendations.append({
                    'type': 'investigation',
                    'priority': 'critical',
                    'title': 'Investigate error rate spike',
                    'description': 'High error rate detected, check input data quality and model health',
                    'expected_impact': 'Improved reliability'
                })
                
            # Resource utilization recommendations
            if current_perf.get('average_cpu_utilization', 0) > 75:
                recommendations.append({
                    'type': 'scaling',
                    'priority': 'medium',
                    'title': 'Scale deployment resources',
                    'description': 'High CPU utilization detected, consider scaling up or out',
                    'expected_impact': 'Better performance and reliability'
                })
                
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            
        return recommendations
        
    async def get_monitoring_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive monitoring dashboard data"""
        try:
            dashboard = {
                'overview': {
                    'total_models_monitored': len(self.performance_trackers),
                    'active_anomalies': len([a for a in self.active_anomalies.values() if not a.resolved_at]),
                    'total_metrics_collected': len(self.metrics_buffer),
                    'monitoring_status': 'active' if self.monitoring_active else 'inactive'
                },
                'model_health': {},
                'recent_anomalies': [],
                'performance_trends': {},
                'system_alerts': []
            }
            
            # Model health scores
            for model_id in self.performance_trackers.keys():
                health_score = await self._calculate_health_score(model_id)
                dashboard['model_health'][model_id] = {
                    'health_score': health_score,
                    'status': 'healthy' if health_score > 80 else 'degraded' if health_score > 50 else 'critical'
                }
                
            # Recent anomalies (last 24 hours)
            recent_anomalies = [
                anomaly.to_dict() for anomaly in self.active_anomalies.values()
                if (datetime.utcnow() - anomaly.detected_at).total_seconds() < 86400
            ]
            dashboard['recent_anomalies'] = sorted(recent_anomalies, 
                                                 key=lambda x: x['detected_at'], reverse=True)[:10]
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Error getting monitoring dashboard: {e}")
            return {}
            
    async def _metrics_collection_loop(self):
        """Background loop for metrics collection"""
        while self.monitoring_active:
            try:
                await asyncio.sleep(30)  # Collect every 30 seconds
                
                # Simulate metrics collection from deployments
                if self.ai_edge_manager:
                    for deployment_id, deployment in self.ai_edge_manager.deployments.items():
                        if deployment.status.value == 'running':
                            # Generate mock metrics
                            metrics = await self._generate_mock_metrics(deployment)
                            await self.collect_metrics(metrics)
                            
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in metrics collection loop: {e}")
                
    async def _generate_mock_metrics(self, deployment) -> InferenceMetrics:
        """Generate mock metrics for testing"""
        import random
        
        base_latency = 50 + random.uniform(-20, 30)
        base_throughput = 100 + random.uniform(-30, 50)
        
        return InferenceMetrics(
            timestamp=datetime.utcnow(),
            model_id=deployment.model_id,
            deployment_id=deployment.deployment_id,
            edge_location_id=deployment.edge_location_id,
            latency_ms=max(10, base_latency),
            throughput_rps=max(1, base_throughput),
            accuracy=0.85 + random.uniform(-0.05, 0.05),
            error_rate=max(0, random.uniform(0, 0.02)),
            cpu_utilization=random.uniform(30, 80),
            memory_utilization=random.uniform(40, 70),
            gpu_utilization=random.uniform(20, 60),
            request_count=random.randint(50, 200),
            batch_size=random.randint(1, 8)
        )
        
    async def _anomaly_detection_loop(self):
        """Background loop for anomaly detection"""
        while self.monitoring_active:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                # Clean up resolved anomalies older than 24 hours
                cutoff_time = datetime.utcnow() - timedelta(hours=24)
                anomalies_to_remove = [
                    anomaly_id for anomaly_id, anomaly in self.active_anomalies.items()
                    if anomaly.resolved_at and anomaly.resolved_at < cutoff_time
                ]
                
                for anomaly_id in anomalies_to_remove:
                    del self.active_anomalies[anomaly_id]
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in anomaly detection loop: {e}")
                
    async def _performance_analysis_loop(self):
        """Background loop for performance analysis"""
        while self.monitoring_active:
            try:
                await asyncio.sleep(300)  # Analyze every 5 minutes
                
                # Perform trend analysis and generate insights
                for model_id, tracker in self.performance_trackers.items():
                    if len(tracker.metrics_history) > 50:
                        # Analyze trends and generate recommendations
                        pass
                        
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in performance analysis loop: {e}")


# Example usage
async def example_ai_edge_monitor():
    """Example of using the AI edge monitor"""
    
    # Create monitor
    monitor = AIEdgeMonitor()
    
    # Start monitoring
    await monitor.start_monitoring()
    
    # Simulate metrics collection
    metrics = InferenceMetrics(
        timestamp=datetime.utcnow(),
        model_id='resnet50-v1',
        deployment_id='deploy-001',
        edge_location_id='edge-us-east-1',
        latency_ms=45.5,
        throughput_rps=120.0,
        accuracy=0.76,
        error_rate=0.01,
        cpu_utilization=65.0,
        memory_utilization=55.0,
        gpu_utilization=40.0,
        request_count=150,
        batch_size=4
    )
    
    await monitor.collect_metrics(metrics)
    
    # Get performance summary
    summary = await monitor.get_model_performance_summary('resnet50-v1')
    print(f"Performance summary: {summary}")
    
    # Get monitoring dashboard
    dashboard = await monitor.get_monitoring_dashboard()
    print(f"Monitoring dashboard: {dashboard}")
    
    # Stop monitoring
    await monitor.stop_monitoring()


if __name__ == "__main__":
    asyncio.run(example_ai_edge_monitor())

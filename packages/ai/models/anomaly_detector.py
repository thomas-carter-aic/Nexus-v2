"""
Anomaly Detection Model for AI-Native PaaS Platform.

This module implements machine learning models for detecting anomalies in
application behavior, performance metrics, and system health.

Features:
- Real-time anomaly detection
- Multi-metric anomaly analysis
- Severity classification
- Root cause analysis
- Automated alerting
- Historical anomaly tracking
"""

import asyncio
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import json
import boto3
from botocore.exceptions import ClientError
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Configure logging
logger = logging.getLogger(__name__)


class AnomalySeverity(str, Enum):
    """Anomaly severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AnomalyType(str, Enum):
    """Types of anomalies that can be detected."""
    PERFORMANCE = "performance"
    RESOURCE_USAGE = "resource_usage"
    ERROR_RATE = "error_rate"
    TRAFFIC_PATTERN = "traffic_pattern"
    RESPONSE_TIME = "response_time"
    SECURITY = "security"
    AVAILABILITY = "availability"


@dataclass
class AnomalyAlert:
    """Anomaly detection alert."""
    application_id: str
    anomaly_type: AnomalyType
    severity: AnomalySeverity
    confidence: float
    description: str
    affected_metrics: List[str]
    timestamp: datetime
    duration: Optional[timedelta]
    root_cause_analysis: Dict[str, Any]
    recommended_actions: List[str]
    metadata: Dict[str, Any]


@dataclass
class MetricPoint:
    """Single metric data point for anomaly detection."""
    timestamp: datetime
    metric_name: str
    value: float
    application_id: str
    tags: Dict[str, str] = None


class AnomalyDetector:
    """
    AI-powered anomaly detection engine.
    
    Uses multiple algorithms to detect anomalies in application metrics
    and system behavior patterns.
    """
    
    def __init__(self, sagemaker_endpoint: Optional[str] = None):
        """
        Initialize the anomaly detector.
        
        Args:
            sagemaker_endpoint: Optional SageMaker endpoint for advanced anomaly detection
        """
        self.sagemaker_endpoint = sagemaker_endpoint
        self.sagemaker_client = None
        self.cloudwatch_client = None
        
        # Initialize AWS clients
        try:
            self.sagemaker_client = boto3.client('sagemaker-runtime')
            self.cloudwatch_client = boto3.client('cloudwatch')
            logger.info("AWS clients initialized for anomaly detection")
        except Exception as e:
            logger.warning(f"AWS clients initialization failed: {e}")
        
        # Detection parameters
        self.detection_window = 60  # minutes
        self.sensitivity = 0.8  # 0-1, higher = more sensitive
        self.min_data_points = 10
        
        # Statistical thresholds
        self.z_score_threshold = 2.5
        self.iqr_multiplier = 1.5
        
        # ML models
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        
        # Data storage (in production, use proper database)
        self.metrics_buffer: Dict[str, List[MetricPoint]] = {}
        self.anomaly_history: Dict[str, List[AnomalyAlert]] = {}
        self.baseline_models: Dict[str, Dict[str, Any]] = {}
    
    async def collect_metrics(self, application_id: str) -> List[MetricPoint]:
        """
        Collect metrics for anomaly detection.
        
        Args:
            application_id: Application identifier
            
        Returns:
            List of metric data points
        """
        try:
            current_time = datetime.utcnow()
            metrics = []
            
            # Simulate realistic metrics with occasional anomalies
            for i in range(60):  # Last 60 minutes
                timestamp = current_time - timedelta(minutes=i)
                
                # Base patterns
                hour = timestamp.hour
                minute = timestamp.minute
                
                # CPU utilization with daily pattern
                base_cpu = 40 + 20 * np.sin(2 * np.pi * hour / 24)
                cpu_noise = np.random.normal(0, 3)
                
                # Inject anomalies occasionally
                if np.random.random() < 0.05:  # 5% chance of CPU anomaly
                    cpu_anomaly = np.random.choice([50, -20])  # Spike or drop
                    base_cpu += cpu_anomaly
                
                cpu_value = max(0, min(100, base_cpu + cpu_noise))
                
                # Memory utilization
                base_memory = 50 + 10 * np.sin(2 * np.pi * hour / 24)
                memory_noise = np.random.normal(0, 2)
                
                if np.random.random() < 0.03:  # 3% chance of memory anomaly
                    memory_anomaly = np.random.uniform(30, 40)
                    base_memory += memory_anomaly
                
                memory_value = max(0, min(100, base_memory + memory_noise))
                
                # Response time
                base_response_time = 100 + 50 * np.sin(2 * np.pi * hour / 24)
                response_noise = np.random.normal(0, 10)
                
                if np.random.random() < 0.04:  # 4% chance of response time anomaly
                    response_anomaly = np.random.uniform(200, 500)
                    base_response_time += response_anomaly
                
                response_time = max(10, base_response_time + response_noise)
                
                # Error rate
                base_error_rate = 0.5
                error_noise = np.random.normal(0, 0.1)
                
                if np.random.random() < 0.02:  # 2% chance of error rate anomaly
                    error_anomaly = np.random.uniform(5, 15)
                    base_error_rate += error_anomaly
                
                error_rate = max(0, base_error_rate + error_noise)
                
                # Request count
                base_requests = 200 + 100 * np.sin(2 * np.pi * hour / 24)
                request_noise = np.random.normal(0, 20)
                
                if np.random.random() < 0.03:  # 3% chance of traffic anomaly
                    traffic_anomaly = np.random.choice([300, -150])
                    base_requests += traffic_anomaly
                
                request_count = max(0, base_requests + request_noise)
                
                # Create metric points
                metrics.extend([
                    MetricPoint(timestamp, "cpu_utilization", cpu_value, application_id),
                    MetricPoint(timestamp, "memory_utilization", memory_value, application_id),
                    MetricPoint(timestamp, "response_time", response_time, application_id),
                    MetricPoint(timestamp, "error_rate", error_rate, application_id),
                    MetricPoint(timestamp, "request_count", request_count, application_id)
                ])
            
            # Store in buffer
            if application_id not in self.metrics_buffer:
                self.metrics_buffer[application_id] = []
            
            self.metrics_buffer[application_id].extend(metrics)
            
            # Keep only recent data
            cutoff_time = current_time - timedelta(hours=24)
            self.metrics_buffer[application_id] = [
                m for m in self.metrics_buffer[application_id] 
                if m.timestamp > cutoff_time
            ]
            
            logger.info(f"Collected {len(metrics)} metric points for anomaly detection")
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect metrics for anomaly detection: {e}")
            return []
    
    def build_baseline_model(self, application_id: str, metrics: List[MetricPoint]) -> Dict[str, Any]:
        """
        Build baseline model for normal behavior.
        
        Args:
            application_id: Application identifier
            metrics: Historical metrics data
            
        Returns:
            Baseline model parameters
        """
        try:
            if len(metrics) < self.min_data_points:
                logger.warning(f"Insufficient data for baseline model: {len(metrics)} points")
                return {}
            
            # Group metrics by type
            metric_groups = {}
            for metric in metrics:
                if metric.metric_name not in metric_groups:
                    metric_groups[metric.metric_name] = []
                metric_groups[metric.metric_name].append(metric.value)
            
            baseline = {}
            
            for metric_name, values in metric_groups.items():
                values_array = np.array(values)
                
                # Statistical parameters
                baseline[metric_name] = {
                    'mean': np.mean(values_array),
                    'std': np.std(values_array),
                    'median': np.median(values_array),
                    'q1': np.percentile(values_array, 25),
                    'q3': np.percentile(values_array, 75),
                    'min': np.min(values_array),
                    'max': np.max(values_array),
                    'iqr': np.percentile(values_array, 75) - np.percentile(values_array, 25)
                }
                
                # Time-based patterns (hourly averages)
                df = pd.DataFrame([
                    {'hour': m.timestamp.hour, 'value': m.value}
                    for m in metrics if m.metric_name == metric_name
                ])
                
                if not df.empty:
                    hourly_pattern = df.groupby('hour')['value'].mean().to_dict()
                    baseline[metric_name]['hourly_pattern'] = hourly_pattern
            
            # Store baseline model
            self.baseline_models[application_id] = {
                'created_at': datetime.utcnow(),
                'data_points': len(metrics),
                'metrics': baseline
            }
            
            logger.info(f"Built baseline model for {application_id} with {len(baseline)} metrics")
            return baseline
            
        except Exception as e:
            logger.error(f"Failed to build baseline model: {e}")
            return {}
    
    def detect_statistical_anomalies(
        self, 
        application_id: str, 
        recent_metrics: List[MetricPoint],
        baseline: Dict[str, Any]
    ) -> List[AnomalyAlert]:
        """
        Detect anomalies using statistical methods.
        
        Args:
            application_id: Application identifier
            recent_metrics: Recent metric data points
            baseline: Baseline model parameters
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        try:
            # Group recent metrics by type
            metric_groups = {}
            for metric in recent_metrics:
                if metric.metric_name not in metric_groups:
                    metric_groups[metric.metric_name] = []
                metric_groups[metric.metric_name].append(metric)
            
            for metric_name, metric_points in metric_groups.items():
                if metric_name not in baseline:
                    continue
                
                baseline_stats = baseline[metric_name]
                current_values = [m.value for m in metric_points]
                
                if not current_values:
                    continue
                
                current_mean = np.mean(current_values)
                current_max = np.max(current_values)
                current_min = np.min(current_values)
                
                # Z-score anomaly detection
                z_score = abs(current_mean - baseline_stats['mean']) / (baseline_stats['std'] + 1e-6)
                
                # IQR-based anomaly detection
                q1, q3 = baseline_stats['q1'], baseline_stats['q3']
                iqr = baseline_stats['iqr']
                lower_bound = q1 - self.iqr_multiplier * iqr
                upper_bound = q3 + self.iqr_multiplier * iqr
                
                # Check for anomalies
                anomaly_detected = False
                anomaly_description = ""
                severity = AnomalySeverity.LOW
                confidence = 0.0
                
                if z_score > self.z_score_threshold:
                    anomaly_detected = True
                    confidence = min(0.95, z_score / self.z_score_threshold * 0.7)
                    
                    if current_mean > baseline_stats['mean']:
                        anomaly_description = f"{metric_name} significantly above normal (Z-score: {z_score:.2f})"
                    else:
                        anomaly_description = f"{metric_name} significantly below normal (Z-score: {z_score:.2f})"
                    
                    if z_score > 4:
                        severity = AnomalySeverity.CRITICAL
                    elif z_score > 3:
                        severity = AnomalySeverity.HIGH
                    else:
                        severity = AnomalySeverity.MEDIUM
                
                elif current_max > upper_bound or current_min < lower_bound:
                    anomaly_detected = True
                    confidence = 0.6
                    severity = AnomalySeverity.MEDIUM
                    
                    if current_max > upper_bound:
                        anomaly_description = f"{metric_name} spike detected (max: {current_max:.2f}, threshold: {upper_bound:.2f})"
                    else:
                        anomaly_description = f"{metric_name} drop detected (min: {current_min:.2f}, threshold: {lower_bound:.2f})"
                
                if anomaly_detected:
                    # Determine anomaly type
                    anomaly_type = self._classify_anomaly_type(metric_name)
                    
                    # Root cause analysis
                    root_cause = self._analyze_root_cause(metric_name, current_values, baseline_stats)
                    
                    # Recommended actions
                    actions = self._get_recommended_actions(metric_name, anomaly_type, severity)
                    
                    anomaly = AnomalyAlert(
                        application_id=application_id,
                        anomaly_type=anomaly_type,
                        severity=severity,
                        confidence=confidence,
                        description=anomaly_description,
                        affected_metrics=[metric_name],
                        timestamp=datetime.utcnow(),
                        duration=None,  # Will be calculated for persistent anomalies
                        root_cause_analysis=root_cause,
                        recommended_actions=actions,
                        metadata={
                            'z_score': z_score,
                            'current_mean': current_mean,
                            'baseline_mean': baseline_stats['mean'],
                            'current_max': current_max,
                            'current_min': current_min,
                            'detection_method': 'statistical'
                        }
                    )
                    
                    anomalies.append(anomaly)
            
            logger.info(f"Statistical anomaly detection found {len(anomalies)} anomalies")
            return anomalies
            
        except Exception as e:
            logger.error(f"Statistical anomaly detection failed: {e}")
            return []
    
    def detect_ml_anomalies(
        self, 
        application_id: str, 
        metrics: List[MetricPoint]
    ) -> List[AnomalyAlert]:
        """
        Detect anomalies using machine learning models.
        
        Args:
            application_id: Application identifier
            metrics: Metric data points
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        try:
            if len(metrics) < self.min_data_points:
                return []
            
            # Prepare data for ML model
            df = pd.DataFrame([
                {
                    'timestamp': m.timestamp,
                    'metric_name': m.metric_name,
                    'value': m.value,
                    'hour': m.timestamp.hour,
                    'minute': m.timestamp.minute,
                    'day_of_week': m.timestamp.weekday()
                }
                for m in metrics
            ])
            
            # Pivot to get features for each timestamp
            pivot_df = df.pivot_table(
                index=['timestamp', 'hour', 'minute', 'day_of_week'],
                columns='metric_name',
                values='value',
                fill_value=0
            ).reset_index()
            
            if pivot_df.empty or len(pivot_df) < self.min_data_points:
                return []
            
            # Select numeric columns for ML
            feature_columns = [col for col in pivot_df.columns 
                             if col not in ['timestamp'] and pivot_df[col].dtype in ['float64', 'int64']]
            
            if not feature_columns:
                return []
            
            X = pivot_df[feature_columns].fillna(0)
            
            # Fit and predict with Isolation Forest
            try:
                # Scale features
                X_scaled = self.scaler.fit_transform(X)
                
                # Fit model and predict
                predictions = self.isolation_forest.fit_predict(X_scaled)
                anomaly_scores = self.isolation_forest.decision_function(X_scaled)
                
                # Find anomalies (predictions == -1)
                anomaly_indices = np.where(predictions == -1)[0]
                
                for idx in anomaly_indices:
                    timestamp = pivot_df.iloc[idx]['timestamp']
                    score = anomaly_scores[idx]
                    
                    # Determine severity based on anomaly score
                    if score < -0.5:
                        severity = AnomalySeverity.CRITICAL
                        confidence = 0.9
                    elif score < -0.3:
                        severity = AnomalySeverity.HIGH
                        confidence = 0.8
                    elif score < -0.1:
                        severity = AnomalySeverity.MEDIUM
                        confidence = 0.7
                    else:
                        severity = AnomalySeverity.LOW
                        confidence = 0.6
                    
                    # Find which metrics contributed to the anomaly
                    row_data = pivot_df.iloc[idx]
                    affected_metrics = []
                    
                    for col in feature_columns:
                        if col in ['hour', 'minute', 'day_of_week']:
                            continue
                        value = row_data[col]
                        if abs(value) > 0:  # Non-zero values might be anomalous
                            affected_metrics.append(col)
                    
                    if not affected_metrics:
                        affected_metrics = ['multiple_metrics']
                    
                    anomaly = AnomalyAlert(
                        application_id=application_id,
                        anomaly_type=AnomalyType.PERFORMANCE,
                        severity=severity,
                        confidence=confidence,
                        description=f"ML-detected anomaly at {timestamp} (score: {score:.3f})",
                        affected_metrics=affected_metrics,
                        timestamp=timestamp,
                        duration=None,
                        root_cause_analysis={
                            'anomaly_score': score,
                            'detection_method': 'isolation_forest',
                            'feature_contributions': {
                                col: float(row_data[col]) for col in affected_metrics
                            }
                        },
                        recommended_actions=self._get_recommended_actions(
                            'multiple_metrics', AnomalyType.PERFORMANCE, severity
                        ),
                        metadata={
                            'ml_model': 'isolation_forest',
                            'anomaly_score': score,
                            'feature_count': len(feature_columns)
                        }
                    )
                    
                    anomalies.append(anomaly)
                
                logger.info(f"ML anomaly detection found {len(anomalies)} anomalies")
                
            except Exception as e:
                logger.error(f"ML model prediction failed: {e}")
            
            return anomalies
            
        except Exception as e:
            logger.error(f"ML anomaly detection failed: {e}")
            return []
    
    def _classify_anomaly_type(self, metric_name: str) -> AnomalyType:
        """Classify anomaly type based on metric name."""
        metric_name_lower = metric_name.lower()
        
        if 'cpu' in metric_name_lower or 'memory' in metric_name_lower:
            return AnomalyType.RESOURCE_USAGE
        elif 'error' in metric_name_lower:
            return AnomalyType.ERROR_RATE
        elif 'response_time' in metric_name_lower or 'latency' in metric_name_lower:
            return AnomalyType.RESPONSE_TIME
        elif 'request' in metric_name_lower or 'traffic' in metric_name_lower:
            return AnomalyType.TRAFFIC_PATTERN
        else:
            return AnomalyType.PERFORMANCE
    
    def _analyze_root_cause(
        self, 
        metric_name: str, 
        current_values: List[float], 
        baseline_stats: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze potential root causes of the anomaly."""
        analysis = {
            'metric': metric_name,
            'current_avg': np.mean(current_values),
            'baseline_avg': baseline_stats['mean'],
            'deviation_percentage': ((np.mean(current_values) - baseline_stats['mean']) / baseline_stats['mean']) * 100,
            'potential_causes': []
        }
        
        deviation = analysis['deviation_percentage']
        
        if metric_name == 'cpu_utilization':
            if deviation > 50:
                analysis['potential_causes'] = [
                    'High computational load',
                    'Inefficient algorithms',
                    'Resource contention',
                    'Memory leaks causing CPU overhead'
                ]
            elif deviation < -30:
                analysis['potential_causes'] = [
                    'Application not receiving traffic',
                    'Process crashed or suspended',
                    'Load balancer issues'
                ]
        
        elif metric_name == 'memory_utilization':
            if deviation > 40:
                analysis['potential_causes'] = [
                    'Memory leak',
                    'Large data processing',
                    'Caching issues',
                    'Insufficient memory allocation'
                ]
        
        elif metric_name == 'response_time':
            if deviation > 100:
                analysis['potential_causes'] = [
                    'Database performance issues',
                    'Network latency',
                    'External service delays',
                    'Resource exhaustion'
                ]
        
        elif metric_name == 'error_rate':
            if deviation > 200:
                analysis['potential_causes'] = [
                    'Application bugs',
                    'Configuration errors',
                    'External service failures',
                    'Resource exhaustion'
                ]
        
        return analysis
    
    def _get_recommended_actions(
        self, 
        metric_name: str, 
        anomaly_type: AnomalyType, 
        severity: AnomalySeverity
    ) -> List[str]:
        """Get recommended actions based on anomaly type and severity."""
        actions = []
        
        if severity in [AnomalySeverity.CRITICAL, AnomalySeverity.HIGH]:
            actions.append("Immediate investigation required")
            actions.append("Consider scaling resources")
            actions.append("Check application logs")
        
        if anomaly_type == AnomalyType.RESOURCE_USAGE:
            actions.extend([
                "Monitor resource utilization trends",
                "Consider vertical or horizontal scaling",
                "Review resource allocation policies"
            ])
        
        elif anomaly_type == AnomalyType.ERROR_RATE:
            actions.extend([
                "Check application error logs",
                "Review recent deployments",
                "Validate external service dependencies"
            ])
        
        elif anomaly_type == AnomalyType.RESPONSE_TIME:
            actions.extend([
                "Check database performance",
                "Review network connectivity",
                "Analyze slow query logs"
            ])
        
        elif anomaly_type == AnomalyType.TRAFFIC_PATTERN:
            actions.extend([
                "Verify load balancer configuration",
                "Check for DDoS attacks",
                "Review traffic routing rules"
            ])
        
        actions.append("Set up additional monitoring")
        actions.append("Document incident for future reference")
        
        return actions
    
    async def detect_anomalies(self, application_id: str) -> List[AnomalyAlert]:
        """
        Main anomaly detection method.
        
        Args:
            application_id: Application identifier
            
        Returns:
            List of detected anomalies
        """
        try:
            # Collect recent metrics
            metrics = await self.collect_metrics(application_id)
            if not metrics:
                logger.warning(f"No metrics available for anomaly detection: {application_id}")
                return []
            
            # Build or update baseline model
            baseline = self.build_baseline_model(application_id, metrics)
            if not baseline:
                logger.warning(f"Could not build baseline model for {application_id}")
                return []
            
            # Get recent metrics for anomaly detection (last 10 minutes)
            cutoff_time = datetime.utcnow() - timedelta(minutes=10)
            recent_metrics = [m for m in metrics if m.timestamp > cutoff_time]
            
            if not recent_metrics:
                return []
            
            # Detect anomalies using multiple methods
            statistical_anomalies = self.detect_statistical_anomalies(
                application_id, recent_metrics, baseline
            )
            
            ml_anomalies = self.detect_ml_anomalies(application_id, metrics)
            
            # Combine and deduplicate anomalies
            all_anomalies = statistical_anomalies + ml_anomalies
            
            # Store in history
            if application_id not in self.anomaly_history:
                self.anomaly_history[application_id] = []
            
            self.anomaly_history[application_id].extend(all_anomalies)
            
            # Keep only recent history (last 24 hours)
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            self.anomaly_history[application_id] = [
                a for a in self.anomaly_history[application_id]
                if a.timestamp > cutoff_time
            ]
            
            logger.info(f"Anomaly detection completed for {application_id}: {len(all_anomalies)} anomalies found")
            return all_anomalies
            
        except Exception as e:
            logger.error(f"Anomaly detection failed for {application_id}: {e}")
            return []
    
    async def get_anomaly_history(self, application_id: str, limit: int = 50) -> List[AnomalyAlert]:
        """Get anomaly history for an application."""
        history = self.anomaly_history.get(application_id, [])
        return sorted(history, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    async def update_sensitivity(self, sensitivity: float) -> bool:
        """Update anomaly detection sensitivity."""
        try:
            self.sensitivity = max(0.1, min(1.0, sensitivity))
            self.z_score_threshold = 2.0 + (1.0 - self.sensitivity) * 2.0
            logger.info(f"Anomaly detection sensitivity updated to {self.sensitivity}")
            return True
        except Exception as e:
            logger.error(f"Failed to update sensitivity: {e}")
            return False

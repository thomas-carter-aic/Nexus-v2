"""
Predictive Auto-Scaling Model for AI-Native PaaS Platform.

This module implements machine learning models for intelligent application scaling
based on historical usage patterns, traffic predictions, and resource utilization.

Features:
- Time series forecasting for traffic prediction
- Resource utilization pattern analysis
- Proactive scaling recommendations
- Cost-aware scaling decisions
- Multi-metric scaling optimization
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

# Configure logging
logger = logging.getLogger(__name__)


class ScalingAction(str, Enum):
    """Scaling action recommendations."""
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    MAINTAIN = "maintain"
    PREEMPTIVE_SCALE = "preemptive_scale"


class ScalingReason(str, Enum):
    """Reasons for scaling decisions."""
    HIGH_CPU = "high_cpu_utilization"
    HIGH_MEMORY = "high_memory_utilization"
    HIGH_TRAFFIC = "high_traffic_volume"
    PREDICTED_SPIKE = "predicted_traffic_spike"
    COST_OPTIMIZATION = "cost_optimization"
    SCHEDULED_EVENT = "scheduled_event"
    ANOMALY_DETECTED = "anomaly_detected"


@dataclass
class MetricData:
    """Container for application metrics."""
    timestamp: datetime
    cpu_utilization: float
    memory_utilization: float
    request_count: int
    response_time: float
    error_rate: float
    active_connections: int


@dataclass
class ScalingRecommendation:
    """Scaling recommendation with confidence and reasoning."""
    application_id: str
    action: ScalingAction
    target_instances: int
    current_instances: int
    confidence: float
    reason: ScalingReason
    cost_impact: float
    performance_impact: str
    urgency: str
    metadata: Dict[str, Any]


class ScalingPredictor:
    """
    AI-powered predictive scaling engine.
    
    Uses machine learning to predict application load and recommend
    optimal scaling actions based on historical patterns and real-time metrics.
    """
    
    def __init__(self, sagemaker_endpoint: Optional[str] = None):
        """
        Initialize the scaling predictor.
        
        Args:
            sagemaker_endpoint: Optional SageMaker endpoint for advanced ML predictions
        """
        self.sagemaker_endpoint = sagemaker_endpoint
        self.sagemaker_client = None
        self.cloudwatch_client = None
        
        # Initialize AWS clients
        try:
            self.sagemaker_client = boto3.client('sagemaker-runtime')
            self.cloudwatch_client = boto3.client('cloudwatch')
            logger.info("AWS clients initialized successfully")
        except Exception as e:
            logger.warning(f"AWS clients initialization failed: {e}")
        
        # Model parameters
        self.prediction_window = 30  # minutes
        self.confidence_threshold = 0.7
        self.scaling_cooldown = 300  # seconds
        
        # Historical data storage (in production, use proper database)
        self.metrics_history: Dict[str, List[MetricData]] = {}
        self.scaling_history: Dict[str, List[ScalingRecommendation]] = {}
    
    async def collect_metrics(self, application_id: str) -> List[MetricData]:
        """
        Collect current and historical metrics for an application.
        
        Args:
            application_id: Application identifier
            
        Returns:
            List of metric data points
        """
        try:
            # In production, this would query CloudWatch, Prometheus, or other monitoring systems
            # For now, we'll simulate realistic metrics
            
            current_time = datetime.utcnow()
            metrics = []
            
            # Generate last 24 hours of metrics (hourly data points)
            for i in range(24):
                timestamp = current_time - timedelta(hours=i)
                
                # Simulate realistic patterns with some randomness
                hour = timestamp.hour
                base_cpu = 30 + 20 * np.sin(2 * np.pi * hour / 24)  # Daily pattern
                base_memory = 40 + 15 * np.sin(2 * np.pi * hour / 24)
                base_requests = 100 + 80 * np.sin(2 * np.pi * hour / 24)
                
                # Add some noise and spikes
                cpu_noise = np.random.normal(0, 5)
                memory_noise = np.random.normal(0, 3)
                request_noise = np.random.normal(0, 20)
                
                # Simulate occasional traffic spikes
                if np.random.random() < 0.1:  # 10% chance of spike
                    spike_multiplier = np.random.uniform(1.5, 3.0)
                    base_requests *= spike_multiplier
                    base_cpu *= 1.2
                    base_memory *= 1.1
                
                metrics.append(MetricData(
                    timestamp=timestamp,
                    cpu_utilization=max(0, min(100, base_cpu + cpu_noise)),
                    memory_utilization=max(0, min(100, base_memory + memory_noise)),
                    request_count=max(0, int(base_requests + request_noise)),
                    response_time=np.random.uniform(50, 200),
                    error_rate=np.random.uniform(0, 2),
                    active_connections=max(0, int(base_requests * 0.1))
                ))
            
            # Store in history
            self.metrics_history[application_id] = metrics
            
            logger.info(f"Collected {len(metrics)} metric data points for {application_id}")
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect metrics for {application_id}: {e}")
            return []
    
    def analyze_patterns(self, metrics: List[MetricData]) -> Dict[str, Any]:
        """
        Analyze historical patterns in metrics data.
        
        Args:
            metrics: List of metric data points
            
        Returns:
            Pattern analysis results
        """
        if not metrics:
            return {}
        
        try:
            # Convert to pandas DataFrame for analysis
            df = pd.DataFrame([
                {
                    'timestamp': m.timestamp,
                    'cpu': m.cpu_utilization,
                    'memory': m.memory_utilization,
                    'requests': m.request_count,
                    'response_time': m.response_time,
                    'error_rate': m.error_rate
                }
                for m in metrics
            ])
            
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek
            
            # Calculate patterns
            patterns = {
                'avg_cpu': df['cpu'].mean(),
                'max_cpu': df['cpu'].max(),
                'cpu_trend': self._calculate_trend(df['cpu'].values),
                'avg_memory': df['memory'].mean(),
                'max_memory': df['memory'].max(),
                'memory_trend': self._calculate_trend(df['memory'].values),
                'avg_requests': df['requests'].mean(),
                'max_requests': df['requests'].max(),
                'request_trend': self._calculate_trend(df['requests'].values),
                'peak_hours': df.groupby('hour')['requests'].mean().nlargest(3).index.tolist(),
                'low_hours': df.groupby('hour')['requests'].mean().nsmallest(3).index.tolist(),
                'daily_pattern_strength': self._calculate_daily_pattern_strength(df),
                'volatility': {
                    'cpu': df['cpu'].std(),
                    'memory': df['memory'].std(),
                    'requests': df['requests'].std()
                }
            }
            
            logger.debug(f"Pattern analysis completed: {patterns}")
            return patterns
            
        except Exception as e:
            logger.error(f"Pattern analysis failed: {e}")
            return {}
    
    def _calculate_trend(self, values: np.ndarray) -> str:
        """Calculate trend direction from time series data."""
        if len(values) < 2:
            return "stable"
        
        # Simple linear regression slope
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 1:
            return "increasing"
        elif slope < -1:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_daily_pattern_strength(self, df: pd.DataFrame) -> float:
        """Calculate how strong the daily pattern is (0-1)."""
        try:
            hourly_avg = df.groupby('hour')['requests'].mean()
            pattern_strength = (hourly_avg.max() - hourly_avg.min()) / hourly_avg.mean()
            return min(1.0, pattern_strength / 2.0)  # Normalize to 0-1
        except:
            return 0.0
    
    async def predict_future_load(self, application_id: str, metrics: List[MetricData]) -> Dict[str, Any]:
        """
        Predict future load using time series forecasting.
        
        Args:
            application_id: Application identifier
            metrics: Historical metrics data
            
        Returns:
            Load predictions for the next prediction window
        """
        try:
            if self.sagemaker_endpoint and self.sagemaker_client:
                # Use SageMaker for advanced predictions
                return await self._predict_with_sagemaker(application_id, metrics)
            else:
                # Use local prediction algorithm
                return self._predict_locally(metrics)
                
        except Exception as e:
            logger.error(f"Load prediction failed for {application_id}: {e}")
            return self._get_default_prediction()
    
    async def _predict_with_sagemaker(self, application_id: str, metrics: List[MetricData]) -> Dict[str, Any]:
        """Use SageMaker endpoint for predictions."""
        try:
            # Prepare input data for SageMaker
            input_data = {
                'application_id': application_id,
                'metrics': [
                    {
                        'timestamp': m.timestamp.isoformat(),
                        'cpu': m.cpu_utilization,
                        'memory': m.memory_utilization,
                        'requests': m.request_count,
                        'response_time': m.response_time
                    }
                    for m in metrics[-24:]  # Last 24 data points
                ],
                'prediction_horizon': self.prediction_window
            }
            
            # Call SageMaker endpoint
            response = self.sagemaker_client.invoke_endpoint(
                EndpointName=self.sagemaker_endpoint,
                ContentType='application/json',
                Body=json.dumps(input_data)
            )
            
            result = json.loads(response['Body'].read().decode())
            
            logger.info(f"SageMaker prediction completed for {application_id}")
            return result
            
        except ClientError as e:
            logger.error(f"SageMaker prediction failed: {e}")
            return self._predict_locally(metrics)
    
    def _predict_locally(self, metrics: List[MetricData]) -> Dict[str, Any]:
        """Local prediction using simple algorithms."""
        if not metrics:
            return self._get_default_prediction()
        
        try:
            # Simple moving average with trend analysis
            recent_metrics = metrics[-6:]  # Last 6 data points
            
            # Calculate averages
            avg_cpu = np.mean([m.cpu_utilization for m in recent_metrics])
            avg_memory = np.mean([m.memory_utilization for m in recent_metrics])
            avg_requests = np.mean([m.request_count for m in recent_metrics])
            
            # Calculate trends
            cpu_values = [m.cpu_utilization for m in recent_metrics]
            memory_values = [m.memory_utilization for m in recent_metrics]
            request_values = [m.request_count for m in recent_metrics]
            
            cpu_trend = self._calculate_trend(np.array(cpu_values))
            memory_trend = self._calculate_trend(np.array(memory_values))
            request_trend = self._calculate_trend(np.array(request_values))
            
            # Apply trend multipliers for prediction
            trend_multipliers = {
                "increasing": 1.2,
                "stable": 1.0,
                "decreasing": 0.8
            }
            
            predicted_cpu = avg_cpu * trend_multipliers[cpu_trend]
            predicted_memory = avg_memory * trend_multipliers[memory_trend]
            predicted_requests = avg_requests * trend_multipliers[request_trend]
            
            # Add some seasonality (simple daily pattern)
            current_hour = datetime.utcnow().hour
            future_hour = (current_hour + 1) % 24
            
            # Peak hours adjustment (assuming 9-17 are peak hours)
            if 9 <= future_hour <= 17:
                seasonality_multiplier = 1.3
            elif 22 <= future_hour or future_hour <= 6:
                seasonality_multiplier = 0.7
            else:
                seasonality_multiplier = 1.0
            
            predicted_requests *= seasonality_multiplier
            predicted_cpu *= (seasonality_multiplier * 0.5 + 0.5)  # Less impact on CPU
            
            return {
                'predicted_cpu': min(100, max(0, predicted_cpu)),
                'predicted_memory': min(100, max(0, predicted_memory)),
                'predicted_requests': max(0, int(predicted_requests)),
                'confidence': 0.75,  # Local prediction confidence
                'prediction_horizon': self.prediction_window,
                'method': 'local_trend_analysis'
            }
            
        except Exception as e:
            logger.error(f"Local prediction failed: {e}")
            return self._get_default_prediction()
    
    def _get_default_prediction(self) -> Dict[str, Any]:
        """Return default prediction when other methods fail."""
        return {
            'predicted_cpu': 50.0,
            'predicted_memory': 50.0,
            'predicted_requests': 100,
            'confidence': 0.3,
            'prediction_horizon': self.prediction_window,
            'method': 'default_fallback'
        }
    
    async def generate_scaling_recommendation(
        self, 
        application_id: str, 
        current_instances: int,
        target_cpu_threshold: float = 70.0,
        target_memory_threshold: float = 80.0
    ) -> ScalingRecommendation:
        """
        Generate intelligent scaling recommendation.
        
        Args:
            application_id: Application identifier
            current_instances: Current number of instances
            target_cpu_threshold: Target CPU utilization threshold
            target_memory_threshold: Target memory utilization threshold
            
        Returns:
            Scaling recommendation with confidence and reasoning
        """
        try:
            # Collect current metrics
            metrics = await self.collect_metrics(application_id)
            if not metrics:
                return self._get_default_recommendation(application_id, current_instances)
            
            # Analyze patterns
            patterns = self.analyze_patterns(metrics)
            
            # Predict future load
            predictions = await self.predict_future_load(application_id, metrics)
            
            # Get current metrics (most recent)
            current_metrics = metrics[0]  # Most recent first
            
            # Decision logic
            recommendation = self._make_scaling_decision(
                application_id=application_id,
                current_instances=current_instances,
                current_metrics=current_metrics,
                patterns=patterns,
                predictions=predictions,
                target_cpu_threshold=target_cpu_threshold,
                target_memory_threshold=target_memory_threshold
            )
            
            # Store recommendation in history
            if application_id not in self.scaling_history:
                self.scaling_history[application_id] = []
            self.scaling_history[application_id].append(recommendation)
            
            logger.info(f"Generated scaling recommendation for {application_id}: {recommendation.action}")
            return recommendation
            
        except Exception as e:
            logger.error(f"Failed to generate scaling recommendation for {application_id}: {e}")
            return self._get_default_recommendation(application_id, current_instances)
    
    def _make_scaling_decision(
        self,
        application_id: str,
        current_instances: int,
        current_metrics: MetricData,
        patterns: Dict[str, Any],
        predictions: Dict[str, Any],
        target_cpu_threshold: float,
        target_memory_threshold: float
    ) -> ScalingRecommendation:
        """Make intelligent scaling decision based on all available data."""
        
        # Current utilization
        current_cpu = current_metrics.cpu_utilization
        current_memory = current_metrics.memory_utilization
        
        # Predicted utilization
        predicted_cpu = predictions.get('predicted_cpu', current_cpu)
        predicted_memory = predictions.get('predicted_memory', current_memory)
        
        # Decision variables
        action = ScalingAction.MAINTAIN
        target_instances = current_instances
        confidence = 0.5
        reason = ScalingReason.COST_OPTIMIZATION
        urgency = "low"
        
        # High confidence scaling decisions
        if current_cpu > 90 or current_memory > 95:
            action = ScalingAction.SCALE_UP
            target_instances = min(current_instances * 2, 20)  # Cap at 20 instances
            confidence = 0.95
            reason = ScalingReason.HIGH_CPU if current_cpu > current_memory else ScalingReason.HIGH_MEMORY
            urgency = "critical"
            
        elif predicted_cpu > target_cpu_threshold or predicted_memory > target_memory_threshold:
            if predictions.get('confidence', 0) > self.confidence_threshold:
                action = ScalingAction.PREEMPTIVE_SCALE
                scale_factor = max(predicted_cpu / target_cpu_threshold, predicted_memory / target_memory_threshold)
                target_instances = min(int(current_instances * scale_factor), 15)
                confidence = predictions.get('confidence', 0.7)
                reason = ScalingReason.PREDICTED_SPIKE
                urgency = "medium"
        
        elif current_cpu > target_cpu_threshold or current_memory > target_memory_threshold:
            action = ScalingAction.SCALE_UP
            scale_factor = max(current_cpu / target_cpu_threshold, current_memory / target_memory_threshold)
            target_instances = min(int(current_instances * scale_factor), 10)
            confidence = 0.8
            reason = ScalingReason.HIGH_CPU if current_cpu > current_memory else ScalingReason.HIGH_MEMORY
            urgency = "high"
            
        elif current_cpu < 20 and current_memory < 30 and current_instances > 1:
            # Scale down opportunity
            if patterns.get('cpu_trend') == 'decreasing' and patterns.get('request_trend') == 'decreasing':
                action = ScalingAction.SCALE_DOWN
                target_instances = max(1, current_instances - 1)
                confidence = 0.7
                reason = ScalingReason.COST_OPTIMIZATION
                urgency = "low"
        
        # Calculate cost impact (simplified)
        instance_cost_per_hour = 0.05  # $0.05 per instance per hour
        cost_change = (target_instances - current_instances) * instance_cost_per_hour
        
        # Performance impact assessment
        if action == ScalingAction.SCALE_UP:
            performance_impact = "improved"
        elif action == ScalingAction.SCALE_DOWN:
            performance_impact = "minimal_impact" if confidence > 0.7 else "potential_degradation"
        else:
            performance_impact = "no_change"
        
        return ScalingRecommendation(
            application_id=application_id,
            action=action,
            target_instances=target_instances,
            current_instances=current_instances,
            confidence=confidence,
            reason=reason,
            cost_impact=cost_change,
            performance_impact=performance_impact,
            urgency=urgency,
            metadata={
                'current_cpu': current_cpu,
                'current_memory': current_memory,
                'predicted_cpu': predicted_cpu,
                'predicted_memory': predicted_memory,
                'patterns': patterns,
                'prediction_confidence': predictions.get('confidence', 0),
                'timestamp': datetime.utcnow().isoformat()
            }
        )
    
    def _get_default_recommendation(self, application_id: str, current_instances: int) -> ScalingRecommendation:
        """Return default recommendation when analysis fails."""
        return ScalingRecommendation(
            application_id=application_id,
            action=ScalingAction.MAINTAIN,
            target_instances=current_instances,
            current_instances=current_instances,
            confidence=0.3,
            reason=ScalingReason.COST_OPTIMIZATION,
            cost_impact=0.0,
            performance_impact="no_change",
            urgency="low",
            metadata={
                'error': 'insufficient_data',
                'timestamp': datetime.utcnow().isoformat()
            }
        )
    
    async def get_scaling_history(self, application_id: str, limit: int = 10) -> List[ScalingRecommendation]:
        """Get scaling recommendation history for an application."""
        history = self.scaling_history.get(application_id, [])
        return history[-limit:] if history else []
    
    async def update_model_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Update model parameters for fine-tuning."""
        try:
            if 'prediction_window' in parameters:
                self.prediction_window = parameters['prediction_window']
            if 'confidence_threshold' in parameters:
                self.confidence_threshold = parameters['confidence_threshold']
            if 'scaling_cooldown' in parameters:
                self.scaling_cooldown = parameters['scaling_cooldown']
            
            logger.info(f"Model parameters updated: {parameters}")
            return True
        except Exception as e:
            logger.error(f"Failed to update model parameters: {e}")
            return False

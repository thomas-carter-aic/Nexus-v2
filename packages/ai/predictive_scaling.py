"""
AI-Powered Predictive Scaling Service

This module implements intelligent scaling decisions using AWS SageMaker and
machine learning models to predict optimal resource allocation based on
historical patterns, current metrics, and business context.

Key Features:
- Predictive scaling based on time series analysis
- Multi-dimensional metric analysis (CPU, memory, network, custom metrics)
- Cost-aware scaling decisions
- Anomaly detection for unusual traffic patterns
- Self-learning and model improvement over time
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import boto3
from botocore.exceptions import ClientError

from ..core.domain.models import Application, ResourceRequirements, ScalingStrategy
from ..core.application.services import AIScalingService


# Configure logging for AI services
logger = logging.getLogger(__name__)


class PredictiveScalingService(AIScalingService):
    """
    Advanced AI-powered scaling service that uses machine learning models
    to make intelligent scaling decisions based on multiple factors including
    historical patterns, current metrics, cost implications, and business context.
    """
    
    def __init__(self, 
                 sagemaker_client: Optional[boto3.client] = None,
                 cloudwatch_client: Optional[boto3.client] = None,
                 region_name: str = 'us-east-1'):
        """
        Initialize the predictive scaling service with AWS clients.
        
        Args:
            sagemaker_client: AWS SageMaker client for ML operations
            cloudwatch_client: AWS CloudWatch client for metrics
            region_name: AWS region name for service initialization
        """
        self._sagemaker_client = sagemaker_client or boto3.client('sagemaker', region_name=region_name)
        self._cloudwatch_client = cloudwatch_client or boto3.client('cloudwatch', region_name=region_name)
        self._region_name = region_name
        
        # Model configuration
        self._scaling_model_name = 'paas-scaling-predictor'
        self._anomaly_model_name = 'paas-anomaly-detector'
        self._cost_model_name = 'paas-cost-optimizer'
        
        # Scaling parameters
        self._prediction_horizon_minutes = 60  # Predict 1 hour ahead
        self._confidence_threshold = 0.7       # Minimum confidence for scaling decisions
        self._cost_weight = 0.3               # Weight for cost considerations in scaling decisions
        self._performance_weight = 0.7        # Weight for performance considerations
        
        # Cache for model predictions to avoid redundant calls
        self._prediction_cache: Dict[str, Dict[str, Any]] = {}
        self._cache_ttl_seconds = 300  # 5 minutes cache TTL
    
    async def predict_scaling_need(self, 
                                 application: Application, 
                                 current_metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Predict if scaling is needed based on current metrics and historical patterns.
        
        This method uses multiple ML models to analyze:
        1. Time series patterns for predictive scaling
        2. Anomaly detection for unusual behavior
        3. Cost optimization for efficient resource usage
        4. Business context for intelligent decision making
        
        Args:
            application: The application to analyze for scaling needs
            current_metrics: Current performance metrics (CPU, memory, requests, etc.)
            
        Returns:
            Dictionary containing scaling prediction with detailed analysis:
            {
                'should_scale': bool,
                'recommended_instances': int,
                'confidence': float,
                'reason': str,
                'cost_impact': float,
                'predicted_metrics': dict,
                'anomaly_score': float,
                'scaling_urgency': str  # 'low', 'medium', 'high', 'critical'
            }
        """
        logger.info(f"Predicting scaling need for application {application.id.value}")
        
        try:
            # Check cache first to avoid redundant predictions
            cache_key = f"{application.id.value}_{hash(str(current_metrics))}"
            cached_prediction = self._get_cached_prediction(cache_key)
            if cached_prediction:
                logger.debug(f"Using cached prediction for application {application.id.value}")
                return cached_prediction
            
            # Gather historical metrics for pattern analysis
            historical_metrics = await self._get_historical_metrics(
                application.id.value, 
                hours_back=24  # Analyze last 24 hours of data
            )
            
            # Prepare feature vector for ML models
            feature_vector = self._prepare_feature_vector(
                application=application,
                current_metrics=current_metrics,
                historical_metrics=historical_metrics
            )
            
            # Run parallel predictions using multiple models
            scaling_prediction, anomaly_score, cost_analysis = await asyncio.gather(
                self._predict_scaling_requirements(feature_vector),
                self._detect_anomalies(feature_vector),
                self._analyze_cost_implications(application, feature_vector)
            )
            
            # Combine predictions into final scaling decision
            final_prediction = self._combine_predictions(
                application=application,
                current_metrics=current_metrics,
                scaling_prediction=scaling_prediction,
                anomaly_score=anomaly_score,
                cost_analysis=cost_analysis
            )
            
            # Cache the prediction for future use
            self._cache_prediction(cache_key, final_prediction)
            
            logger.info(f"Scaling prediction completed for application {application.id.value}: "
                       f"should_scale={final_prediction['should_scale']}, "
                       f"confidence={final_prediction['confidence']:.2f}")
            
            return final_prediction
            
        except Exception as e:
            logger.error(f"Error predicting scaling need for application {application.id.value}: {str(e)}")
            # Return safe fallback prediction
            return self._get_fallback_prediction(application, current_metrics)
    
    async def optimize_resource_allocation(self, application: Application) -> ResourceRequirements:
        """
        Optimize resource allocation based on usage patterns and cost efficiency.
        
        This method analyzes historical resource utilization patterns to recommend
        optimal resource allocation that balances performance and cost.
        
        Args:
            application: The application to optimize resource allocation for
            
        Returns:
            Optimized resource requirements based on ML analysis
        """
        logger.info(f"Optimizing resource allocation for application {application.id.value}")
        
        try:
            # Gather extended historical data for resource optimization
            historical_data = await self._get_historical_resource_usage(
                application.id.value,
                days_back=7  # Analyze last week of resource usage
            )
            
            # Prepare optimization feature vector
            optimization_features = self._prepare_optimization_features(
                application=application,
                historical_data=historical_data
            )
            
            # Use ML model to predict optimal resource allocation
            optimization_result = await self._predict_optimal_resources(optimization_features)
            
            # Create optimized resource requirements
            optimized_requirements = ResourceRequirements(
                cpu_cores=max(0.1, optimization_result['cpu_cores']),  # Minimum 0.1 CPU
                memory_mb=max(128, int(optimization_result['memory_mb'])),  # Minimum 128MB
                storage_gb=max(1, int(optimization_result['storage_gb'])),  # Minimum 1GB
                network_bandwidth_mbps=optimization_result.get('network_bandwidth_mbps'),
                gpu_count=optimization_result.get('gpu_count')
            )
            
            logger.info(f"Resource optimization completed for application {application.id.value}: "
                       f"CPU={optimized_requirements.cpu_cores}, "
                       f"Memory={optimized_requirements.memory_mb}MB")
            
            return optimized_requirements
            
        except Exception as e:
            logger.error(f"Error optimizing resources for application {application.id.value}: {str(e)}")
            # Return current requirements as fallback
            return application.resource_requirements
    
    async def _predict_scaling_requirements(self, feature_vector: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use SageMaker model to predict scaling requirements.
        
        Args:
            feature_vector: Prepared features for ML model input
            
        Returns:
            Scaling prediction from ML model
        """
        try:
            # Prepare input data for SageMaker endpoint
            input_data = json.dumps({
                'instances': [feature_vector]
            })
            
            # Invoke SageMaker endpoint for scaling prediction
            response = self._sagemaker_client.invoke_endpoint(
                EndpointName=self._scaling_model_name,
                ContentType='application/json',
                Body=input_data
            )
            
            # Parse prediction results
            result = json.loads(response['Body'].read().decode())
            
            return {
                'recommended_instances': int(result.get('predicted_instances', 1)),
                'confidence': float(result.get('confidence', 0.5)),
                'predicted_cpu_usage': float(result.get('predicted_cpu', 0.0)),
                'predicted_memory_usage': float(result.get('predicted_memory', 0.0)),
                'scaling_direction': result.get('scaling_direction', 'maintain')  # 'up', 'down', 'maintain'
            }
            
        except ClientError as e:
            logger.warning(f"SageMaker scaling prediction failed: {str(e)}")
            # Return conservative prediction as fallback
            return {
                'recommended_instances': feature_vector.get('current_instances', 1),
                'confidence': 0.3,
                'predicted_cpu_usage': feature_vector.get('current_cpu_usage', 50.0),
                'predicted_memory_usage': feature_vector.get('current_memory_usage', 50.0),
                'scaling_direction': 'maintain'
            }
    
    async def _detect_anomalies(self, feature_vector: Dict[str, Any]) -> float:
        """
        Detect anomalies in current metrics using ML model.
        
        Args:
            feature_vector: Prepared features for anomaly detection
            
        Returns:
            Anomaly score (0.0 = normal, 1.0 = highly anomalous)
        """
        try:
            # Prepare input for anomaly detection model
            input_data = json.dumps({
                'instances': [feature_vector]
            })
            
            # Invoke anomaly detection endpoint
            response = self._sagemaker_client.invoke_endpoint(
                EndpointName=self._anomaly_model_name,
                ContentType='application/json',
                Body=input_data
            )
            
            # Parse anomaly score
            result = json.loads(response['Body'].read().decode())
            anomaly_score = float(result.get('anomaly_score', 0.0))
            
            return min(1.0, max(0.0, anomaly_score))  # Ensure score is between 0 and 1
            
        except ClientError as e:
            logger.warning(f"Anomaly detection failed: {str(e)}")
            return 0.0  # Assume normal behavior if detection fails
    
    async def _analyze_cost_implications(self, 
                                       application: Application, 
                                       feature_vector: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze cost implications of different scaling decisions.
        
        Args:
            application: The application being analyzed
            feature_vector: Prepared features for cost analysis
            
        Returns:
            Cost analysis results with recommendations
        """
        try:
            # Add cost-specific features
            cost_features = {
                **feature_vector,
                'current_cost_per_hour': self._calculate_current_cost(application),
                'instance_type': 'standard',  # Could be determined dynamically
                'region': self._region_name,
                'reserved_instance_coverage': 0.0  # Could be retrieved from AWS
            }
            
            # Prepare input for cost optimization model
            input_data = json.dumps({
                'instances': [cost_features]
            })
            
            # Invoke cost optimization endpoint
            response = self._sagemaker_client.invoke_endpoint(
                EndpointName=self._cost_model_name,
                ContentType='application/json',
                Body=input_data
            )
            
            # Parse cost analysis results
            result = json.loads(response['Body'].read().decode())
            
            return {
                'cost_efficiency_score': float(result.get('efficiency_score', 0.5)),
                'estimated_hourly_cost': float(result.get('estimated_cost', 0.0)),
                'cost_optimization_potential': float(result.get('optimization_potential', 0.0)),
                'recommended_instance_type': result.get('recommended_type', 'current')
            }
            
        except ClientError as e:
            logger.warning(f"Cost analysis failed: {str(e)}")
            return {
                'cost_efficiency_score': 0.5,
                'estimated_hourly_cost': self._calculate_current_cost(application),
                'cost_optimization_potential': 0.0,
                'recommended_instance_type': 'current'
            }
    
    def _prepare_feature_vector(self, 
                              application: Application,
                              current_metrics: Dict[str, float],
                              historical_metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Prepare feature vector for ML models from application data and metrics.
        
        Args:
            application: The application being analyzed
            current_metrics: Current performance metrics
            historical_metrics: Historical metrics data
            
        Returns:
            Feature vector suitable for ML model input
        """
        # Calculate statistical features from historical data
        historical_stats = self._calculate_historical_statistics(historical_metrics)
        
        # Time-based features
        now = datetime.utcnow()
        time_features = {
            'hour_of_day': now.hour,
            'day_of_week': now.weekday(),
            'is_weekend': now.weekday() >= 5,
            'is_business_hours': 9 <= now.hour <= 17
        }
        
        # Application-specific features
        app_features = {
            'current_instances': application.current_instance_count,
            'min_instances': application.scaling_config.min_instances,
            'max_instances': application.scaling_config.max_instances,
            'cpu_cores': application.resource_requirements.cpu_cores,
            'memory_mb': application.resource_requirements.memory_mb,
            'scaling_strategy': application.scaling_config.strategy.value
        }
        
        # Current metrics features
        metrics_features = {
            'current_cpu_usage': current_metrics.get('cpu_utilization', 0.0),
            'current_memory_usage': current_metrics.get('memory_utilization', 0.0),
            'current_request_rate': current_metrics.get('request_rate', 0.0),
            'current_response_time': current_metrics.get('response_time', 0.0),
            'current_error_rate': current_metrics.get('error_rate', 0.0)
        }
        
        # Combine all features
        feature_vector = {
            **time_features,
            **app_features,
            **metrics_features,
            **historical_stats
        }
        
        return feature_vector
    
    def _calculate_historical_statistics(self, historical_metrics: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate statistical features from historical metrics data.
        
        Args:
            historical_metrics: List of historical metric data points
            
        Returns:
            Dictionary of statistical features
        """
        if not historical_metrics:
            return {
                'avg_cpu_usage': 0.0,
                'max_cpu_usage': 0.0,
                'cpu_usage_trend': 0.0,
                'avg_memory_usage': 0.0,
                'max_memory_usage': 0.0,
                'memory_usage_trend': 0.0,
                'avg_request_rate': 0.0,
                'max_request_rate': 0.0,
                'request_rate_volatility': 0.0
            }
        
        # Extract metric arrays
        cpu_values = [m.get('cpu_utilization', 0.0) for m in historical_metrics]
        memory_values = [m.get('memory_utilization', 0.0) for m in historical_metrics]
        request_values = [m.get('request_rate', 0.0) for m in historical_metrics]
        
        # Calculate statistics
        stats = {
            'avg_cpu_usage': np.mean(cpu_values),
            'max_cpu_usage': np.max(cpu_values),
            'cpu_usage_trend': self._calculate_trend(cpu_values),
            'avg_memory_usage': np.mean(memory_values),
            'max_memory_usage': np.max(memory_values),
            'memory_usage_trend': self._calculate_trend(memory_values),
            'avg_request_rate': np.mean(request_values),
            'max_request_rate': np.max(request_values),
            'request_rate_volatility': np.std(request_values) if len(request_values) > 1 else 0.0
        }
        
        return stats
    
    def _calculate_trend(self, values: List[float]) -> float:
        """
        Calculate trend direction for a series of values.
        
        Args:
            values: List of numeric values
            
        Returns:
            Trend value (-1.0 to 1.0, negative = decreasing, positive = increasing)
        """
        if len(values) < 2:
            return 0.0
        
        # Simple linear regression slope calculation
        n = len(values)
        x = np.arange(n)
        y = np.array(values)
        
        slope = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x**2) - np.sum(x)**2)
        
        # Normalize slope to [-1, 1] range
        max_value = max(values) if max(values) > 0 else 1.0
        normalized_slope = slope / max_value
        
        return max(-1.0, min(1.0, normalized_slope))
    
    def _combine_predictions(self,
                           application: Application,
                           current_metrics: Dict[str, float],
                           scaling_prediction: Dict[str, Any],
                           anomaly_score: float,
                           cost_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Combine multiple ML predictions into final scaling decision.
        
        Args:
            application: The application being analyzed
            current_metrics: Current performance metrics
            scaling_prediction: Results from scaling prediction model
            anomaly_score: Anomaly detection score
            cost_analysis: Cost analysis results
            
        Returns:
            Final scaling decision with comprehensive analysis
        """
        # Base scaling recommendation from ML model
        recommended_instances = scaling_prediction['recommended_instances']
        base_confidence = scaling_prediction['confidence']
        
        # Adjust confidence based on anomaly score
        # High anomaly score reduces confidence in normal scaling patterns
        anomaly_adjusted_confidence = base_confidence * (1.0 - anomaly_score * 0.5)
        
        # Determine if scaling is needed
        current_instances = application.current_instance_count
        should_scale = (
            recommended_instances != current_instances and
            anomaly_adjusted_confidence >= self._confidence_threshold
        )
        
        # Calculate scaling urgency based on current metrics and predictions
        urgency = self._calculate_scaling_urgency(
            current_metrics=current_metrics,
            predicted_metrics=scaling_prediction,
            anomaly_score=anomaly_score
        )
        
        # Generate human-readable reason for scaling decision
        reason = self._generate_scaling_reason(
            current_instances=current_instances,
            recommended_instances=recommended_instances,
            scaling_prediction=scaling_prediction,
            anomaly_score=anomaly_score,
            urgency=urgency
        )
        
        # Calculate cost impact of scaling decision
        cost_impact = self._calculate_cost_impact(
            current_instances=current_instances,
            recommended_instances=recommended_instances,
            cost_analysis=cost_analysis
        )
        
        return {
            'should_scale': should_scale,
            'recommended_instances': recommended_instances,
            'confidence': anomaly_adjusted_confidence,
            'reason': reason,
            'cost_impact': cost_impact,
            'predicted_metrics': {
                'cpu_usage': scaling_prediction.get('predicted_cpu_usage', 0.0),
                'memory_usage': scaling_prediction.get('predicted_memory_usage', 0.0)
            },
            'anomaly_score': anomaly_score,
            'scaling_urgency': urgency,
            'cost_efficiency_score': cost_analysis.get('cost_efficiency_score', 0.5),
            'scaling_direction': scaling_prediction.get('scaling_direction', 'maintain')
        }
    
    def _calculate_scaling_urgency(self,
                                 current_metrics: Dict[str, float],
                                 predicted_metrics: Dict[str, Any],
                                 anomaly_score: float) -> str:
        """
        Calculate the urgency of scaling based on current and predicted metrics.
        
        Returns:
            Urgency level: 'low', 'medium', 'high', or 'critical'
        """
        cpu_usage = current_metrics.get('cpu_utilization', 0.0)
        memory_usage = current_metrics.get('memory_utilization', 0.0)
        error_rate = current_metrics.get('error_rate', 0.0)
        
        # Critical conditions
        if cpu_usage > 90 or memory_usage > 95 or error_rate > 5.0:
            return 'critical'
        
        # High urgency conditions
        if cpu_usage > 80 or memory_usage > 85 or anomaly_score > 0.8:
            return 'high'
        
        # Medium urgency conditions
        if cpu_usage > 70 or memory_usage > 75 or anomaly_score > 0.5:
            return 'medium'
        
        return 'low'
    
    def _generate_scaling_reason(self,
                               current_instances: int,
                               recommended_instances: int,
                               scaling_prediction: Dict[str, Any],
                               anomaly_score: float,
                               urgency: str) -> str:
        """Generate human-readable reason for scaling decision"""
        if recommended_instances > current_instances:
            direction = "scale up"
            change = recommended_instances - current_instances
        elif recommended_instances < current_instances:
            direction = "scale down"
            change = current_instances - recommended_instances
        else:
            return "No scaling needed - current capacity is optimal"
        
        reason_parts = [
            f"AI recommends {direction} by {change} instance(s)",
            f"based on predicted resource usage"
        ]
        
        if anomaly_score > 0.5:
            reason_parts.append(f"(anomaly detected: {anomaly_score:.2f})")
        
        if urgency in ['high', 'critical']:
            reason_parts.append(f"- {urgency} priority")
        
        return " ".join(reason_parts)
    
    def _calculate_cost_impact(self,
                             current_instances: int,
                             recommended_instances: int,
                             cost_analysis: Dict[str, Any]) -> float:
        """
        Calculate the cost impact of scaling decision.
        
        Returns:
            Cost impact as percentage change (positive = increase, negative = decrease)
        """
        if current_instances == 0:
            return 0.0
        
        instance_change_ratio = recommended_instances / current_instances
        cost_change_percentage = (instance_change_ratio - 1.0) * 100.0
        
        return cost_change_percentage
    
    async def _get_historical_metrics(self, application_id: str, hours_back: int = 24) -> List[Dict[str, Any]]:
        """
        Retrieve historical metrics from CloudWatch.
        
        This is a placeholder implementation that would integrate with
        actual CloudWatch APIs to retrieve historical performance data.
        """
        # TODO: Implement actual CloudWatch integration
        # For now, return mock historical data
        mock_data = []
        for i in range(hours_back):
            timestamp = datetime.utcnow() - timedelta(hours=i)
            mock_data.append({
                'timestamp': timestamp.isoformat(),
                'cpu_utilization': 50.0 + np.random.normal(0, 10),
                'memory_utilization': 60.0 + np.random.normal(0, 15),
                'request_rate': 100.0 + np.random.normal(0, 20),
                'response_time': 200.0 + np.random.normal(0, 50),
                'error_rate': 0.5 + max(0, np.random.normal(0, 0.2))
            })
        
        return mock_data
    
    def _calculate_current_cost(self, application: Application) -> float:
        """
        Calculate current hourly cost for the application.
        
        This is a simplified cost calculation that would integrate with
        AWS pricing APIs for accurate cost estimation.
        """
        # Simplified cost calculation based on resource requirements
        base_cost_per_core_hour = 0.05  # $0.05 per CPU core per hour
        base_cost_per_gb_memory_hour = 0.01  # $0.01 per GB memory per hour
        
        cpu_cost = application.resource_requirements.cpu_cores * base_cost_per_core_hour
        memory_cost = (application.resource_requirements.memory_mb / 1024) * base_cost_per_gb_memory_hour
        
        return (cpu_cost + memory_cost) * application.current_instance_count
    
    def _get_cached_prediction(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached prediction if still valid"""
        if cache_key in self._prediction_cache:
            cached_data = self._prediction_cache[cache_key]
            if datetime.utcnow().timestamp() - cached_data['timestamp'] < self._cache_ttl_seconds:
                return cached_data['prediction']
        return None
    
    def _cache_prediction(self, cache_key: str, prediction: Dict[str, Any]) -> None:
        """Cache prediction with timestamp"""
        self._prediction_cache[cache_key] = {
            'prediction': prediction,
            'timestamp': datetime.utcnow().timestamp()
        }
    
    def _get_fallback_prediction(self, application: Application, current_metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Generate safe fallback prediction when ML models are unavailable.
        
        This uses simple rule-based logic as a backup when AI services fail.
        """
        cpu_usage = current_metrics.get('cpu_utilization', 0.0)
        memory_usage = current_metrics.get('memory_utilization', 0.0)
        
        current_instances = application.current_instance_count
        recommended_instances = current_instances
        
        # Simple rule-based scaling logic
        if cpu_usage > 80 or memory_usage > 85:
            recommended_instances = min(
                current_instances + 1,
                application.scaling_config.max_instances
            )
            reason = f"Rule-based scale up due to high resource usage (CPU: {cpu_usage:.1f}%, Memory: {memory_usage:.1f}%)"
        elif cpu_usage < 30 and memory_usage < 40 and current_instances > application.scaling_config.min_instances:
            recommended_instances = max(
                current_instances - 1,
                application.scaling_config.min_instances
            )
            reason = f"Rule-based scale down due to low resource usage (CPU: {cpu_usage:.1f}%, Memory: {memory_usage:.1f}%)"
        else:
            reason = "No scaling needed based on rule-based analysis"
        
        return {
            'should_scale': recommended_instances != current_instances,
            'recommended_instances': recommended_instances,
            'confidence': 0.5,  # Lower confidence for rule-based decisions
            'reason': reason,
            'cost_impact': 0.0,
            'predicted_metrics': {
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage
            },
            'anomaly_score': 0.0,
            'scaling_urgency': 'medium' if recommended_instances != current_instances else 'low',
            'cost_efficiency_score': 0.5,
            'scaling_direction': 'up' if recommended_instances > current_instances else 'down' if recommended_instances < current_instances else 'maintain'
        }

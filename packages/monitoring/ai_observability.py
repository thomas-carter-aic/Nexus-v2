"""
AI-Driven Observability and Monitoring System

This module implements comprehensive monitoring and observability for the
AI-native PaaS platform with intelligent anomaly detection, predictive
analytics, and self-improving monitoring capabilities.

Key Features:
- Real-time metrics collection and analysis
- AI-powered anomaly detection using SageMaker
- Predictive analytics for proactive issue prevention
- User behavior analysis and business impact correlation
- Self-improving monitoring based on learned patterns
- Custom dashboards with AI-driven insights
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np
import boto3
from botocore.exceptions import ClientError

from ..core.domain.models import ApplicationId, UserId


# Configure logging
logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MetricType(Enum):
    """Types of metrics collected"""
    PERFORMANCE = "performance"
    BUSINESS = "business"
    INFRASTRUCTURE = "infrastructure"
    SECURITY = "security"
    USER_EXPERIENCE = "user_experience"


@dataclass
class MetricData:
    """Data structure for metric information"""
    name: str
    value: float
    timestamp: datetime
    metric_type: MetricType
    dimensions: Dict[str, str]
    unit: str = "Count"
    
    def to_cloudwatch_format(self) -> Dict[str, Any]:
        """Convert to CloudWatch metric format"""
        return {
            'MetricName': self.name,
            'Value': self.value,
            'Timestamp': self.timestamp,
            'Unit': self.unit,
            'Dimensions': [
                {'Name': k, 'Value': v} for k, v in self.dimensions.items()
            ]
        }


@dataclass
class AnomalyDetection:
    """Anomaly detection result"""
    metric_name: str
    anomaly_score: float
    is_anomaly: bool
    confidence: float
    expected_value: float
    actual_value: float
    timestamp: datetime
    context: Dict[str, Any]


@dataclass
class Alert:
    """Alert information"""
    alert_id: str
    severity: AlertSeverity
    title: str
    description: str
    metric_name: str
    current_value: float
    threshold: float
    timestamp: datetime
    application_id: Optional[ApplicationId] = None
    user_id: Optional[UserId] = None
    tags: Dict[str, str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = {}


class AIObservabilityService:
    """
    Comprehensive AI-driven observability service for the PaaS platform.
    
    This service provides intelligent monitoring, anomaly detection, predictive
    analytics, and automated alerting with continuous learning capabilities.
    """
    
    def __init__(self,
                 cloudwatch_client: Optional[boto3.client] = None,
                 sagemaker_client: Optional[boto3.client] = None,
                 comprehend_client: Optional[boto3.client] = None,
                 region_name: str = 'us-east-1'):
        """
        Initialize the AI observability service.
        
        Args:
            cloudwatch_client: AWS CloudWatch client
            sagemaker_client: AWS SageMaker client for AI models
            comprehend_client: AWS Comprehend client for text analysis
            region_name: AWS region name
        """
        self._cloudwatch = cloudwatch_client or boto3.client('cloudwatch', region_name=region_name)
        self._sagemaker = sagemaker_client or boto3.client('sagemaker', region_name=region_name)
        self._comprehend = comprehend_client or boto3.client('comprehend', region_name=region_name)
        self._region_name = region_name
        
        # Configuration
        self._metrics_namespace = 'PaaS/Platform'
        self._anomaly_threshold = 0.7
        self._prediction_horizon_minutes = 60
        self._metric_retention_days = 30
        
        # AI model endpoints
        self._anomaly_detection_endpoint = 'paas-anomaly-detector'
        self._performance_prediction_endpoint = 'paas-performance-predictor'
        self._user_behavior_endpoint = 'paas-user-behavior-analyzer'
        
        # In-memory caches for performance
        self._metric_cache: Dict[str, List[MetricData]] = {}
        self._anomaly_cache: Dict[str, List[AnomalyDetection]] = {}
        self._alert_cache: Dict[str, Alert] = {}
        
        # Learning and adaptation
        self._learning_enabled = True
        self._adaptation_threshold = 0.8
    
    async def collect_metrics(self, 
                            application_id: ApplicationId,
                            metric_types: Optional[List[MetricType]] = None) -> List[MetricData]:
        """
        Collect comprehensive metrics for an application.
        
        Args:
            application_id: Application to collect metrics for
            metric_types: Optional list of metric types to collect
            
        Returns:
            List of collected metrics
        """
        logger.info(f"Collecting metrics for application {application_id.value}")
        
        if metric_types is None:
            metric_types = list(MetricType)
        
        collected_metrics = []
        
        # Collect different types of metrics in parallel
        metric_tasks = []
        
        if MetricType.PERFORMANCE in metric_types:
            metric_tasks.append(self._collect_performance_metrics(application_id))
        
        if MetricType.BUSINESS in metric_types:
            metric_tasks.append(self._collect_business_metrics(application_id))
        
        if MetricType.INFRASTRUCTURE in metric_types:
            metric_tasks.append(self._collect_infrastructure_metrics(application_id))
        
        if MetricType.SECURITY in metric_types:
            metric_tasks.append(self._collect_security_metrics(application_id))
        
        if MetricType.USER_EXPERIENCE in metric_types:
            metric_tasks.append(self._collect_user_experience_metrics(application_id))
        
        # Execute metric collection tasks
        metric_results = await asyncio.gather(*metric_tasks, return_exceptions=True)
        
        # Aggregate results
        for result in metric_results:
            if isinstance(result, Exception):
                logger.warning(f"Metric collection failed: {str(result)}")
                continue
            collected_metrics.extend(result)
        
        # Cache metrics for future analysis
        self._cache_metrics(application_id, collected_metrics)
        
        # Publish metrics to CloudWatch
        await self._publish_metrics_to_cloudwatch(collected_metrics)
        
        logger.info(f"Collected {len(collected_metrics)} metrics for application {application_id.value}")
        
        return collected_metrics
    
    async def detect_anomalies(self,
                             application_id: ApplicationId,
                             metrics: Optional[List[MetricData]] = None) -> List[AnomalyDetection]:
        """
        Detect anomalies in application metrics using AI models.
        
        Args:
            application_id: Application to analyze
            metrics: Optional metrics to analyze (if not provided, will collect current metrics)
            
        Returns:
            List of detected anomalies
        """
        logger.info(f"Detecting anomalies for application {application_id.value}")
        
        if metrics is None:
            metrics = await self.collect_metrics(application_id)
        
        anomalies = []
        
        # Group metrics by type for analysis
        metrics_by_type = self._group_metrics_by_type(metrics)
        
        # Detect anomalies for each metric type
        for metric_type, type_metrics in metrics_by_type.items():
            try:
                type_anomalies = await self._detect_anomalies_for_type(
                    application_id, metric_type, type_metrics
                )
                anomalies.extend(type_anomalies)
            except Exception as e:
                logger.warning(f"Anomaly detection failed for {metric_type}: {str(e)}")
        
        # Cache anomalies
        self._cache_anomalies(application_id, anomalies)
        
        # Generate alerts for significant anomalies
        await self._generate_anomaly_alerts(application_id, anomalies)
        
        logger.info(f"Detected {len(anomalies)} anomalies for application {application_id.value}")
        
        return anomalies
    
    async def predict_performance(self,
                                application_id: ApplicationId,
                                prediction_horizon_minutes: Optional[int] = None) -> Dict[str, Any]:
        """
        Predict future performance metrics using AI models.
        
        Args:
            application_id: Application to predict performance for
            prediction_horizon_minutes: How far ahead to predict (default: 60 minutes)
            
        Returns:
            Performance predictions with confidence intervals
        """
        logger.info(f"Predicting performance for application {application_id.value}")
        
        horizon = prediction_horizon_minutes or self._prediction_horizon_minutes
        
        # Get historical metrics for prediction
        historical_metrics = await self._get_historical_metrics(
            application_id, 
            hours_back=24  # Use 24 hours of history for prediction
        )
        
        # Prepare features for prediction model
        prediction_features = self._prepare_prediction_features(
            application_id, historical_metrics
        )
        
        # Invoke AI model for performance prediction
        prediction_result = await self._invoke_performance_prediction_model(
            prediction_features, horizon
        )
        
        # Analyze prediction for potential issues
        issue_analysis = self._analyze_prediction_for_issues(prediction_result)
        
        # Generate proactive recommendations
        recommendations = self._generate_proactive_recommendations(
            application_id, prediction_result, issue_analysis
        )
        
        result = {
            'application_id': str(application_id.value),
            'prediction_horizon_minutes': horizon,
            'predicted_metrics': prediction_result['predictions'],
            'confidence_intervals': prediction_result['confidence_intervals'],
            'potential_issues': issue_analysis,
            'recommendations': recommendations,
            'model_accuracy': prediction_result.get('model_accuracy', 0.0),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Performance prediction completed for application {application_id.value}")
        
        return result
    
    async def analyze_user_behavior(self,
                                  application_id: ApplicationId,
                                  analysis_period_hours: int = 24) -> Dict[str, Any]:
        """
        Analyze user behavior patterns and their impact on application performance.
        
        Args:
            application_id: Application to analyze
            analysis_period_hours: Period to analyze (default: 24 hours)
            
        Returns:
            User behavior analysis with insights and recommendations
        """
        logger.info(f"Analyzing user behavior for application {application_id.value}")
        
        # Collect user interaction data
        user_data = await self._collect_user_interaction_data(
            application_id, analysis_period_hours
        )
        
        # Analyze user journey patterns
        journey_analysis = await self._analyze_user_journeys(user_data)
        
        # Correlate user behavior with performance metrics
        performance_correlation = await self._correlate_behavior_with_performance(
            application_id, user_data, analysis_period_hours
        )
        
        # Identify optimization opportunities
        optimization_opportunities = self._identify_optimization_opportunities(
            journey_analysis, performance_correlation
        )
        
        # Generate business impact insights
        business_insights = await self._generate_business_insights(
            application_id, user_data, performance_correlation
        )
        
        result = {
            'application_id': str(application_id.value),
            'analysis_period_hours': analysis_period_hours,
            'user_journey_patterns': journey_analysis,
            'performance_correlation': performance_correlation,
            'optimization_opportunities': optimization_opportunities,
            'business_insights': business_insights,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"User behavior analysis completed for application {application_id.value}")
        
        return result
    
    async def create_custom_dashboard(self,
                                    application_id: ApplicationId,
                                    dashboard_config: Dict[str, Any]) -> str:
        """
        Create a custom CloudWatch dashboard with AI-driven insights.
        
        Args:
            application_id: Application to create dashboard for
            dashboard_config: Dashboard configuration and preferences
            
        Returns:
            Dashboard URL or identifier
        """
        logger.info(f"Creating custom dashboard for application {application_id.value}")
        
        # Generate AI-optimized dashboard layout
        optimized_layout = await self._optimize_dashboard_layout(
            application_id, dashboard_config
        )
        
        # Create dashboard widgets with AI insights
        dashboard_widgets = await self._create_ai_enhanced_widgets(
            application_id, optimized_layout
        )
        
        # Build CloudWatch dashboard
        dashboard_body = self._build_dashboard_body(dashboard_widgets)
        
        dashboard_name = f"PaaS-{application_id.value}-AI-Dashboard"
        
        try:
            response = self._cloudwatch.put_dashboard(
                DashboardName=dashboard_name,
                DashboardBody=json.dumps(dashboard_body)
            )
            
            dashboard_url = f"https://console.aws.amazon.com/cloudwatch/home?region={self._region_name}#dashboards:name={dashboard_name}"
            
            logger.info(f"Custom dashboard created: {dashboard_name}")
            
            return dashboard_url
            
        except ClientError as e:
            logger.error(f"Failed to create dashboard: {str(e)}")
            raise
    
    async def generate_insights_report(self,
                                     application_id: ApplicationId,
                                     report_period_days: int = 7) -> Dict[str, Any]:
        """
        Generate comprehensive insights report with AI-driven analysis.
        
        Args:
            application_id: Application to generate report for
            report_period_days: Period to analyze (default: 7 days)
            
        Returns:
            Comprehensive insights report
        """
        logger.info(f"Generating insights report for application {application_id.value}")
        
        # Collect comprehensive data for the report period
        report_data = await self._collect_report_data(application_id, report_period_days)
        
        # Generate AI-driven insights
        ai_insights = await self._generate_ai_insights(application_id, report_data)
        
        # Analyze trends and patterns
        trend_analysis = self._analyze_trends(report_data)
        
        # Generate recommendations
        recommendations = await self._generate_comprehensive_recommendations(
            application_id, report_data, ai_insights, trend_analysis
        )
        
        # Calculate business impact metrics
        business_impact = self._calculate_business_impact(report_data)
        
        # Create executive summary
        executive_summary = self._create_executive_summary(
            ai_insights, trend_analysis, business_impact
        )
        
        report = {
            'application_id': str(application_id.value),
            'report_period_days': report_period_days,
            'generated_at': datetime.utcnow().isoformat(),
            'executive_summary': executive_summary,
            'ai_insights': ai_insights,
            'trend_analysis': trend_analysis,
            'recommendations': recommendations,
            'business_impact': business_impact,
            'raw_data_summary': {
                'total_metrics_analyzed': len(report_data.get('metrics', [])),
                'anomalies_detected': len(report_data.get('anomalies', [])),
                'alerts_generated': len(report_data.get('alerts', []))
            }
        }
        
        logger.info(f"Insights report generated for application {application_id.value}")
        
        return report
    
    # Private helper methods
    
    async def _collect_performance_metrics(self, application_id: ApplicationId) -> List[MetricData]:
        """Collect performance-related metrics"""
        metrics = []
        current_time = datetime.utcnow()
        
        # Mock performance metrics (in real implementation, would query actual services)
        performance_data = {
            'ResponseTime': 250.5,
            'Throughput': 1500.0,
            'ErrorRate': 0.5,
            'CPUUtilization': 65.2,
            'MemoryUtilization': 72.8,
            'DiskIOPS': 850.0,
            'NetworkBytesIn': 1024000.0,
            'NetworkBytesOut': 2048000.0
        }
        
        for metric_name, value in performance_data.items():
            metrics.append(MetricData(
                name=metric_name,
                value=value,
                timestamp=current_time,
                metric_type=MetricType.PERFORMANCE,
                dimensions={'ApplicationId': str(application_id.value)},
                unit='Milliseconds' if 'Time' in metric_name else 'Count'
            ))
        
        return metrics
    
    async def _collect_business_metrics(self, application_id: ApplicationId) -> List[MetricData]:
        """Collect business-related metrics"""
        metrics = []
        current_time = datetime.utcnow()
        
        # Mock business metrics
        business_data = {
            'ActiveUsers': 1250.0,
            'SessionDuration': 420.0,
            'ConversionRate': 3.2,
            'Revenue': 15750.0,
            'CustomerSatisfactionScore': 4.2,
            'FeatureAdoptionRate': 68.5
        }
        
        for metric_name, value in business_data.items():
            metrics.append(MetricData(
                name=metric_name,
                value=value,
                timestamp=current_time,
                metric_type=MetricType.BUSINESS,
                dimensions={'ApplicationId': str(application_id.value)},
                unit='Count'
            ))
        
        return metrics
    
    async def _collect_infrastructure_metrics(self, application_id: ApplicationId) -> List[MetricData]:
        """Collect infrastructure-related metrics"""
        metrics = []
        current_time = datetime.utcnow()
        
        # Mock infrastructure metrics
        infra_data = {
            'InstanceCount': 3.0,
            'LoadBalancerLatency': 15.2,
            'DatabaseConnections': 45.0,
            'CacheHitRate': 92.5,
            'StorageUtilization': 68.3,
            'NetworkLatency': 25.8
        }
        
        for metric_name, value in infra_data.items():
            metrics.append(MetricData(
                name=metric_name,
                value=value,
                timestamp=current_time,
                metric_type=MetricType.INFRASTRUCTURE,
                dimensions={'ApplicationId': str(application_id.value)},
                unit='Count'
            ))
        
        return metrics
    
    async def _collect_security_metrics(self, application_id: ApplicationId) -> List[MetricData]:
        """Collect security-related metrics"""
        metrics = []
        current_time = datetime.utcnow()
        
        # Mock security metrics
        security_data = {
            'FailedLoginAttempts': 12.0,
            'SecurityViolations': 2.0,
            'SuspiciousActivities': 5.0,
            'AuthenticationSuccessRate': 98.5,
            'DataEncryptionCompliance': 100.0
        }
        
        for metric_name, value in security_data.items():
            metrics.append(MetricData(
                name=metric_name,
                value=value,
                timestamp=current_time,
                metric_type=MetricType.SECURITY,
                dimensions={'ApplicationId': str(application_id.value)},
                unit='Count'
            ))
        
        return metrics
    
    async def _collect_user_experience_metrics(self, application_id: ApplicationId) -> List[MetricData]:
        """Collect user experience metrics"""
        metrics = []
        current_time = datetime.utcnow()
        
        # Mock user experience metrics
        ux_data = {
            'PageLoadTime': 1.8,
            'TimeToInteractive': 2.3,
            'BounceRate': 15.2,
            'UserEngagementScore': 7.8,
            'AccessibilityScore': 95.0,
            'MobileUsabilityScore': 88.5
        }
        
        for metric_name, value in ux_data.items():
            metrics.append(MetricData(
                name=metric_name,
                value=value,
                timestamp=current_time,
                metric_type=MetricType.USER_EXPERIENCE,
                dimensions={'ApplicationId': str(application_id.value)},
                unit='Seconds' if 'Time' in metric_name else 'Count'
            ))
        
        return metrics
    
    def _cache_metrics(self, application_id: ApplicationId, metrics: List[MetricData]) -> None:
        """Cache metrics for future analysis"""
        cache_key = str(application_id.value)
        if cache_key not in self._metric_cache:
            self._metric_cache[cache_key] = []
        
        self._metric_cache[cache_key].extend(metrics)
        
        # Keep only recent metrics (last 24 hours)
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        self._metric_cache[cache_key] = [
            m for m in self._metric_cache[cache_key] 
            if m.timestamp > cutoff_time
        ]
    
    async def _publish_metrics_to_cloudwatch(self, metrics: List[MetricData]) -> None:
        """Publish metrics to CloudWatch"""
        if not metrics:
            return
        
        # Group metrics by namespace for batch publishing
        metric_batches = []
        current_batch = []
        
        for metric in metrics:
            current_batch.append(metric.to_cloudwatch_format())
            
            # CloudWatch has a limit of 20 metrics per batch
            if len(current_batch) >= 20:
                metric_batches.append(current_batch)
                current_batch = []
        
        if current_batch:
            metric_batches.append(current_batch)
        
        # Publish batches
        for batch in metric_batches:
            try:
                self._cloudwatch.put_metric_data(
                    Namespace=self._metrics_namespace,
                    MetricData=batch
                )
            except ClientError as e:
                logger.warning(f"Failed to publish metrics batch: {str(e)}")
    
    def _group_metrics_by_type(self, metrics: List[MetricData]) -> Dict[MetricType, List[MetricData]]:
        """Group metrics by their type"""
        grouped = {}
        for metric in metrics:
            if metric.metric_type not in grouped:
                grouped[metric.metric_type] = []
            grouped[metric.metric_type].append(metric)
        return grouped
    
    async def _detect_anomalies_for_type(self,
                                       application_id: ApplicationId,
                                       metric_type: MetricType,
                                       metrics: List[MetricData]) -> List[AnomalyDetection]:
        """Detect anomalies for a specific metric type"""
        anomalies = []
        
        try:
            # Prepare features for anomaly detection model
            features = self._prepare_anomaly_features(metrics)
            
            # Invoke SageMaker anomaly detection model
            response = self._sagemaker.invoke_endpoint(
                EndpointName=self._anomaly_detection_endpoint,
                ContentType='application/json',
                Body=json.dumps({'instances': [features]})
            )
            
            result = json.loads(response['Body'].read().decode())
            
            # Process anomaly detection results
            for i, metric in enumerate(metrics):
                anomaly_score = result.get('anomaly_scores', [0.0])[i] if i < len(result.get('anomaly_scores', [])) else 0.0
                is_anomaly = anomaly_score > self._anomaly_threshold
                
                if is_anomaly or anomaly_score > 0.5:  # Include potential anomalies
                    anomalies.append(AnomalyDetection(
                        metric_name=metric.name,
                        anomaly_score=anomaly_score,
                        is_anomaly=is_anomaly,
                        confidence=result.get('confidence', 0.5),
                        expected_value=result.get('expected_values', [metric.value])[i] if i < len(result.get('expected_values', [])) else metric.value,
                        actual_value=metric.value,
                        timestamp=metric.timestamp,
                        context={
                            'metric_type': metric_type.value,
                            'application_id': str(application_id.value)
                        }
                    ))
            
        except Exception as e:
            logger.warning(f"Anomaly detection failed for {metric_type}: {str(e)}")
            # Fallback to simple statistical anomaly detection
            anomalies.extend(self._simple_anomaly_detection(metrics))
        
        return anomalies
    
    def _prepare_anomaly_features(self, metrics: List[MetricData]) -> Dict[str, Any]:
        """Prepare features for anomaly detection model"""
        if not metrics:
            return {}
        
        # Extract values and timestamps
        values = [m.value for m in metrics]
        timestamps = [m.timestamp.timestamp() for m in metrics]
        
        # Calculate statistical features
        features = {
            'values': values,
            'timestamps': timestamps,
            'mean': np.mean(values),
            'std': np.std(values),
            'min': np.min(values),
            'max': np.max(values),
            'trend': self._calculate_trend(values),
            'seasonality': self._detect_seasonality(values, timestamps)
        }
        
        return features
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend in values"""
        if len(values) < 2:
            return 0.0
        
        x = np.arange(len(values))
        y = np.array(values)
        
        # Simple linear regression
        slope = np.polyfit(x, y, 1)[0]
        return float(slope)
    
    def _detect_seasonality(self, values: List[float], timestamps: List[float]) -> Dict[str, float]:
        """Detect seasonality patterns in values"""
        # Simplified seasonality detection
        # In a real implementation, would use more sophisticated methods
        return {
            'hourly_pattern': 0.0,
            'daily_pattern': 0.0,
            'weekly_pattern': 0.0
        }
    
    def _simple_anomaly_detection(self, metrics: List[MetricData]) -> List[AnomalyDetection]:
        """Simple statistical anomaly detection as fallback"""
        anomalies = []
        
        if len(metrics) < 3:
            return anomalies
        
        values = [m.value for m in metrics]
        mean = np.mean(values)
        std = np.std(values)
        
        # Use 2-sigma rule for anomaly detection
        threshold = 2 * std
        
        for metric in metrics:
            deviation = abs(metric.value - mean)
            if deviation > threshold:
                anomaly_score = min(1.0, deviation / (3 * std))  # Normalize to 0-1
                
                anomalies.append(AnomalyDetection(
                    metric_name=metric.name,
                    anomaly_score=anomaly_score,
                    is_anomaly=True,
                    confidence=0.6,  # Lower confidence for statistical method
                    expected_value=mean,
                    actual_value=metric.value,
                    timestamp=metric.timestamp,
                    context={'method': 'statistical_fallback'}
                ))
        
        return anomalies

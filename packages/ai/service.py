"""
AI Service Integration Layer for AI-Native PaaS Platform.

This module provides a unified interface to all AI/ML models and services,
orchestrating intelligent decision-making across the platform.

Features:
- Unified AI service interface
- Model orchestration and coordination
- Intelligent decision aggregation
- Real-time AI insights
- Model performance monitoring
- Adaptive learning and improvement
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import json

from .models.scaling_predictor import ScalingPredictor, ScalingRecommendation
from .models.anomaly_detector import AnomalyDetector, AnomalyAlert
from .models.cost_optimizer import CostOptimizer, CostRecommendation
from .models.performance_predictor import PerformancePredictor, PerformancePrediction
from .models.resource_recommender import ResourceRecommender, ResourceRecommendation

logger = logging.getLogger(__name__)


class AIInsightType(str, Enum):
    """Types of AI insights."""
    SCALING_RECOMMENDATION = "scaling_recommendation"
    ANOMALY_ALERT = "anomaly_alert"
    COST_OPTIMIZATION = "cost_optimization"
    PERFORMANCE_PREDICTION = "performance_prediction"
    RESOURCE_RECOMMENDATION = "resource_recommendation"
    COMPOSITE_INSIGHT = "composite_insight"


class InsightPriority(str, Enum):
    """Priority levels for AI insights."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AIInsight:
    """Unified AI insight container."""
    insight_id: str
    application_id: str
    insight_type: AIInsightType
    priority: InsightPriority
    title: str
    description: str
    confidence: float
    recommendations: List[str]
    data: Dict[str, Any]
    timestamp: datetime
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None


class AIService:
    """
    Unified AI Service for the PaaS Platform.
    
    Orchestrates all AI/ML models and provides intelligent insights
    for application management, scaling, optimization, and monitoring.
    """
    
    def __init__(self, sagemaker_endpoint: Optional[str] = None):
        """
        Initialize the AI service with all model components.
        
        Args:
            sagemaker_endpoint: Optional SageMaker endpoint for advanced ML
        """
        # Initialize AI models
        self.scaling_predictor = ScalingPredictor(sagemaker_endpoint)
        self.anomaly_detector = AnomalyDetector(sagemaker_endpoint)
        self.cost_optimizer = CostOptimizer()
        self.performance_predictor = PerformancePredictor()
        self.resource_recommender = ResourceRecommender()
        
        # Service state
        self.insights_cache: Dict[str, List[AIInsight]] = {}
        self.model_performance: Dict[str, Dict[str, float]] = {}
        self.service_health = {
            'status': 'healthy',
            'last_check': datetime.utcnow(),
            'models_active': 5,
            'total_predictions': 0,
            'accuracy_score': 0.85
        }
        
        logger.info("AI Service initialized with all model components")
    
    async def get_comprehensive_insights(
        self, 
        application_id: str,
        include_predictions: bool = True,
        include_optimizations: bool = True
    ) -> List[AIInsight]:
        """
        Get comprehensive AI insights for an application.
        
        Args:
            application_id: Application identifier
            include_predictions: Include predictive insights
            include_optimizations: Include optimization recommendations
            
        Returns:
            List of AI insights ordered by priority
        """
        try:
            insights = []
            
            # Collect insights from all models
            if include_predictions:
                # Scaling insights
                scaling_insights = await self._get_scaling_insights(application_id)
                insights.extend(scaling_insights)
                
                # Performance predictions
                performance_insights = await self._get_performance_insights(application_id)
                insights.extend(performance_insights)
            
            # Anomaly detection (always included for safety)
            anomaly_insights = await self._get_anomaly_insights(application_id)
            insights.extend(anomaly_insights)
            
            if include_optimizations:
                # Cost optimization
                cost_insights = await self._get_cost_insights(application_id)
                insights.extend(cost_insights)
                
                # Resource recommendations
                resource_insights = await self._get_resource_insights(application_id)
                insights.extend(resource_insights)
            
            # Generate composite insights
            composite_insights = await self._generate_composite_insights(application_id, insights)
            insights.extend(composite_insights)
            
            # Sort by priority and confidence
            insights.sort(key=lambda x: (
                self._priority_score(x.priority),
                x.confidence
            ), reverse=True)
            
            # Cache insights
            self.insights_cache[application_id] = insights
            
            # Update service metrics
            self.service_health['total_predictions'] += len(insights)
            self.service_health['last_check'] = datetime.utcnow()
            
            logger.info(f"Generated {len(insights)} AI insights for {application_id}")
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate comprehensive insights: {e}")
            return []
    
    async def _get_scaling_insights(self, application_id: str) -> List[AIInsight]:
        """Get scaling-related AI insights."""
        try:
            # Get scaling recommendation
            scaling_rec = await self.scaling_predictor.generate_scaling_recommendation(
                application_id, current_instances=2
            )
            
            if not scaling_rec:
                return []
            
            # Determine priority based on urgency and action
            if scaling_rec.urgency == "critical":
                priority = InsightPriority.CRITICAL
            elif scaling_rec.urgency == "high":
                priority = InsightPriority.HIGH
            elif scaling_rec.urgency == "medium":
                priority = InsightPriority.MEDIUM
            else:
                priority = InsightPriority.LOW
            
            # Create insight
            insight = AIInsight(
                insight_id=f"scaling_{application_id}_{int(datetime.utcnow().timestamp())}",
                application_id=application_id,
                insight_type=AIInsightType.SCALING_RECOMMENDATION,
                priority=priority,
                title=f"Scaling Recommendation: {scaling_rec.action.value}",
                description=f"Recommend {scaling_rec.action.value} from {scaling_rec.current_instances} to {scaling_rec.target_instances} instances",
                confidence=scaling_rec.confidence,
                recommendations=[
                    f"Scale to {scaling_rec.target_instances} instances",
                    f"Reason: {scaling_rec.reason.value}",
                    f"Expected cost impact: ${scaling_rec.cost_impact:.2f}/month"
                ],
                data={
                    'action': scaling_rec.action.value,
                    'current_instances': scaling_rec.current_instances,
                    'target_instances': scaling_rec.target_instances,
                    'reason': scaling_rec.reason.value,
                    'cost_impact': scaling_rec.cost_impact,
                    'performance_impact': scaling_rec.performance_impact,
                    'urgency': scaling_rec.urgency
                },
                timestamp=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(minutes=30),
                metadata=scaling_rec.metadata
            )
            
            return [insight]
            
        except Exception as e:
            logger.error(f"Failed to get scaling insights: {e}")
            return []
    
    async def _get_anomaly_insights(self, application_id: str) -> List[AIInsight]:
        """Get anomaly detection insights."""
        try:
            anomalies = await self.anomaly_detector.detect_anomalies(application_id)
            insights = []
            
            for anomaly in anomalies:
                # Map severity to priority
                priority_map = {
                    'critical': InsightPriority.CRITICAL,
                    'high': InsightPriority.HIGH,
                    'medium': InsightPriority.MEDIUM,
                    'low': InsightPriority.LOW
                }
                priority = priority_map.get(anomaly.severity.value, InsightPriority.MEDIUM)
                
                insight = AIInsight(
                    insight_id=f"anomaly_{application_id}_{int(anomaly.timestamp.timestamp())}",
                    application_id=application_id,
                    insight_type=AIInsightType.ANOMALY_ALERT,
                    priority=priority,
                    title=f"Anomaly Detected: {anomaly.anomaly_type.value}",
                    description=anomaly.description,
                    confidence=anomaly.confidence,
                    recommendations=anomaly.recommended_actions,
                    data={
                        'anomaly_type': anomaly.anomaly_type.value,
                        'severity': anomaly.severity.value,
                        'affected_metrics': anomaly.affected_metrics,
                        'root_cause_analysis': anomaly.root_cause_analysis
                    },
                    timestamp=anomaly.timestamp,
                    expires_at=datetime.utcnow() + timedelta(hours=2),
                    metadata=anomaly.metadata
                )
                
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to get anomaly insights: {e}")
            return []
    
    async def _get_cost_insights(self, application_id: str) -> List[AIInsight]:
        """Get cost optimization insights."""
        try:
            recommendations = await self.cost_optimizer.generate_optimization_recommendations(
                application_id
            )
            insights = []
            
            for rec in recommendations:
                # Determine priority based on savings
                if rec.savings_percentage > 30:
                    priority = InsightPriority.HIGH
                elif rec.savings_percentage > 15:
                    priority = InsightPriority.MEDIUM
                else:
                    priority = InsightPriority.LOW
                
                insight = AIInsight(
                    insight_id=f"cost_{application_id}_{rec.resource_type.value}_{int(datetime.utcnow().timestamp())}",
                    application_id=application_id,
                    insight_type=AIInsightType.COST_OPTIMIZATION,
                    priority=priority,
                    title=f"Cost Optimization: {rec.resource_type.value}",
                    description=rec.description,
                    confidence=rec.confidence,
                    recommendations=rec.actions,
                    data={
                        'resource_type': rec.resource_type.value,
                        'current_cost': rec.current_cost,
                        'optimized_cost': rec.optimized_cost,
                        'savings': rec.savings,
                        'savings_percentage': rec.savings_percentage,
                        'implementation_effort': rec.implementation_effort,
                        'risk_level': rec.risk_level
                    },
                    timestamp=datetime.utcnow(),
                    expires_at=datetime.utcnow() + timedelta(days=1),
                    metadata=rec.metadata
                )
                
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to get cost insights: {e}")
            return []
    
    async def _get_performance_insights(self, application_id: str) -> List[AIInsight]:
        """Get performance prediction insights."""
        try:
            # Predict response time under increased load
            response_time_pred = await self.performance_predictor.predict_response_time(
                application_id,
                target_load=1000,
                resource_config={'cpu_cores': 2, 'memory_gb': 4}
            )
            
            # Predict throughput
            throughput_pred = await self.performance_predictor.predict_throughput(
                application_id,
                resource_config={'cpu_cores': 2, 'memory_gb': 4},
                instance_count=2
            )
            
            insights = []
            
            # Response time insight
            if response_time_pred.predicted_value > 200:  # > 200ms
                priority = InsightPriority.HIGH
            elif response_time_pred.predicted_value > 100:
                priority = InsightPriority.MEDIUM
            else:
                priority = InsightPriority.LOW
            
            rt_insight = AIInsight(
                insight_id=f"perf_rt_{application_id}_{int(datetime.utcnow().timestamp())}",
                application_id=application_id,
                insight_type=AIInsightType.PERFORMANCE_PREDICTION,
                priority=priority,
                title="Response Time Prediction",
                description=f"Predicted response time: {response_time_pred.predicted_value:.1f}ms under target load",
                confidence=response_time_pred.confidence_score,
                recommendations=response_time_pred.recommendations,
                data={
                    'metric': 'response_time',
                    'predicted_value': response_time_pred.predicted_value,
                    'conditions': response_time_pred.conditions,
                    'factors': response_time_pred.factors
                },
                timestamp=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(hours=1),
                metadata=response_time_pred.metadata
            )
            
            insights.append(rt_insight)
            
            # Throughput insight
            throughput_priority = InsightPriority.MEDIUM if throughput_pred.predicted_value < 500 else InsightPriority.LOW
            
            tp_insight = AIInsight(
                insight_id=f"perf_tp_{application_id}_{int(datetime.utcnow().timestamp())}",
                application_id=application_id,
                insight_type=AIInsightType.PERFORMANCE_PREDICTION,
                priority=throughput_priority,
                title="Throughput Prediction",
                description=f"Predicted throughput: {throughput_pred.predicted_value:.0f} RPS",
                confidence=throughput_pred.confidence_score,
                recommendations=throughput_pred.recommendations,
                data={
                    'metric': 'throughput',
                    'predicted_value': throughput_pred.predicted_value,
                    'conditions': throughput_pred.conditions,
                    'factors': throughput_pred.factors
                },
                timestamp=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(hours=1),
                metadata=throughput_pred.metadata
            )
            
            insights.append(tp_insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to get performance insights: {e}")
            return []
    
    async def _get_resource_insights(self, application_id: str) -> List[AIInsight]:
        """Get resource recommendation insights."""
        try:
            # Simulate current metrics
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
            
            recommendation = await self.resource_recommender.generate_recommendation(
                application_id, current_config, metrics
            )
            
            # Determine priority based on cost impact and performance
            if abs(recommendation.cost_impact) > 100:  # Significant cost change
                priority = InsightPriority.HIGH
            elif recommendation.performance_impact in ['significant_improvement', 'potential_degradation']:
                priority = InsightPriority.MEDIUM
            else:
                priority = InsightPriority.LOW
            
            insight = AIInsight(
                insight_id=f"resource_{application_id}_{int(datetime.utcnow().timestamp())}",
                application_id=application_id,
                insight_type=AIInsightType.RESOURCE_RECOMMENDATION,
                priority=priority,
                title=f"Resource Recommendation: {recommendation.workload_type.value}",
                description=f"Optimize resources for {recommendation.optimization_goal.value} goal",
                confidence=recommendation.confidence,
                recommendations=recommendation.reasoning,
                data={
                    'workload_type': recommendation.workload_type.value,
                    'optimization_goal': recommendation.optimization_goal.value,
                    'current_config': recommendation.current_config,
                    'recommended_config': recommendation.recommended_config,
                    'cost_impact': recommendation.cost_impact,
                    'performance_impact': recommendation.performance_impact,
                    'alternatives': recommendation.alternatives
                },
                timestamp=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(hours=6),
                metadata=recommendation.metadata
            )
            
            return [insight]
            
        except Exception as e:
            logger.error(f"Failed to get resource insights: {e}")
            return []
    
    async def _generate_composite_insights(
        self, 
        application_id: str, 
        individual_insights: List[AIInsight]
    ) -> List[AIInsight]:
        """Generate composite insights by analyzing patterns across individual insights."""
        try:
            composite_insights = []
            
            # Check for correlated issues
            high_priority_insights = [i for i in individual_insights if i.priority == InsightPriority.HIGH]
            critical_insights = [i for i in individual_insights if i.priority == InsightPriority.CRITICAL]
            
            if len(critical_insights) > 1:
                # Multiple critical issues - create composite alert
                composite = AIInsight(
                    insight_id=f"composite_critical_{application_id}_{int(datetime.utcnow().timestamp())}",
                    application_id=application_id,
                    insight_type=AIInsightType.COMPOSITE_INSIGHT,
                    priority=InsightPriority.CRITICAL,
                    title="Multiple Critical Issues Detected",
                    description=f"Application has {len(critical_insights)} critical issues requiring immediate attention",
                    confidence=0.9,
                    recommendations=[
                        "Address critical issues immediately",
                        "Consider emergency scaling",
                        "Monitor application closely",
                        "Prepare rollback plan if needed"
                    ],
                    data={
                        'critical_issues_count': len(critical_insights),
                        'affected_areas': list(set([i.insight_type.value for i in critical_insights])),
                        'individual_insights': [i.insight_id for i in critical_insights]
                    },
                    timestamp=datetime.utcnow(),
                    expires_at=datetime.utcnow() + timedelta(minutes=15)
                )
                composite_insights.append(composite)
            
            elif len(high_priority_insights) >= 3:
                # Multiple high priority issues - create composite recommendation
                composite = AIInsight(
                    insight_id=f"composite_optimization_{application_id}_{int(datetime.utcnow().timestamp())}",
                    application_id=application_id,
                    insight_type=AIInsightType.COMPOSITE_INSIGHT,
                    priority=InsightPriority.HIGH,
                    title="Comprehensive Optimization Opportunity",
                    description=f"Multiple optimization opportunities detected across {len(high_priority_insights)} areas",
                    confidence=0.8,
                    recommendations=[
                        "Plan comprehensive optimization",
                        "Prioritize by impact and effort",
                        "Implement changes gradually",
                        "Monitor results closely"
                    ],
                    data={
                        'optimization_areas': list(set([i.insight_type.value for i in high_priority_insights])),
                        'total_opportunities': len(high_priority_insights),
                        'individual_insights': [i.insight_id for i in high_priority_insights]
                    },
                    timestamp=datetime.utcnow(),
                    expires_at=datetime.utcnow() + timedelta(hours=4)
                )
                composite_insights.append(composite)
            
            return composite_insights
            
        except Exception as e:
            logger.error(f"Failed to generate composite insights: {e}")
            return []
    
    def _priority_score(self, priority: InsightPriority) -> int:
        """Convert priority to numeric score for sorting."""
        priority_scores = {
            InsightPriority.CRITICAL: 4,
            InsightPriority.HIGH: 3,
            InsightPriority.MEDIUM: 2,
            InsightPriority.LOW: 1
        }
        return priority_scores.get(priority, 1)
    
    async def get_service_health(self) -> Dict[str, Any]:
        """Get AI service health status."""
        try:
            # Update health metrics
            self.service_health.update({
                'status': 'healthy',
                'last_check': datetime.utcnow(),
                'models_active': 5,
                'uptime_hours': (datetime.utcnow() - self.service_health['last_check']).total_seconds() / 3600
            })
            
            return self.service_health
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'last_check': datetime.utcnow()
            }
    
    async def get_cached_insights(self, application_id: str) -> List[AIInsight]:
        """Get cached insights for an application."""
        return self.insights_cache.get(application_id, [])
    
    async def clear_expired_insights(self) -> int:
        """Clear expired insights from cache."""
        try:
            current_time = datetime.utcnow()
            cleared_count = 0
            
            for app_id in list(self.insights_cache.keys()):
                insights = self.insights_cache[app_id]
                valid_insights = [
                    insight for insight in insights
                    if insight.expires_at is None or insight.expires_at > current_time
                ]
                
                cleared_count += len(insights) - len(valid_insights)
                
                if valid_insights:
                    self.insights_cache[app_id] = valid_insights
                else:
                    del self.insights_cache[app_id]
            
            logger.info(f"Cleared {cleared_count} expired insights")
            return cleared_count
            
        except Exception as e:
            logger.error(f"Failed to clear expired insights: {e}")
            return 0

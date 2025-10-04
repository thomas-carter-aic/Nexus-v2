"""
Resource Recommendation Model for AI-Native PaaS Platform.

This module implements AI-driven resource recommendation algorithms for
optimal resource allocation and configuration.

Features:
- Intelligent resource sizing
- Multi-dimensional optimization
- Cost-performance trade-offs
- Workload-specific recommendations
- Auto-scaling configuration
- Resource efficiency analysis
"""

import asyncio
import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class WorkloadType(str, Enum):
    """Types of application workloads."""
    WEB_APPLICATION = "web_application"
    API_SERVICE = "api_service"
    BATCH_PROCESSING = "batch_processing"
    DATABASE = "database"
    CACHE = "cache"
    MACHINE_LEARNING = "machine_learning"
    MICROSERVICE = "microservice"


class OptimizationGoal(str, Enum):
    """Resource optimization goals."""
    COST_OPTIMIZED = "cost_optimized"
    PERFORMANCE_OPTIMIZED = "performance_optimized"
    BALANCED = "balanced"
    HIGH_AVAILABILITY = "high_availability"


@dataclass
class ResourceRecommendation:
    """Resource allocation recommendation."""
    application_id: str
    workload_type: WorkloadType
    optimization_goal: OptimizationGoal
    recommended_config: Dict[str, Any]
    current_config: Dict[str, Any]
    cost_impact: float
    performance_impact: str
    confidence: float
    reasoning: List[str]
    alternatives: List[Dict[str, Any]]
    metadata: Dict[str, Any]


class ResourceRecommender:
    """AI-powered resource recommendation engine."""
    
    def __init__(self):
        """Initialize the resource recommender."""
        self.workload_profiles = self._initialize_workload_profiles()
        self.instance_types = self._initialize_instance_types()
        self.recommendation_history: Dict[str, List[ResourceRecommendation]] = {}
    
    def _initialize_workload_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Initialize workload-specific resource profiles."""
        return {
            WorkloadType.WEB_APPLICATION: {
                'cpu_weight': 0.6,
                'memory_weight': 0.4,
                'storage_weight': 0.2,
                'network_weight': 0.3,
                'typical_cpu_util': 40,
                'typical_memory_util': 60,
                'scaling_pattern': 'horizontal',
                'instance_types': ['t3.small', 't3.medium', 't3.large']
            },
            WorkloadType.API_SERVICE: {
                'cpu_weight': 0.7,
                'memory_weight': 0.3,
                'storage_weight': 0.1,
                'network_weight': 0.4,
                'typical_cpu_util': 50,
                'typical_memory_util': 45,
                'scaling_pattern': 'horizontal',
                'instance_types': ['t3.medium', 't3.large', 'c5.large']
            },
            WorkloadType.BATCH_PROCESSING: {
                'cpu_weight': 0.8,
                'memory_weight': 0.6,
                'storage_weight': 0.4,
                'network_weight': 0.1,
                'typical_cpu_util': 80,
                'typical_memory_util': 70,
                'scaling_pattern': 'vertical',
                'instance_types': ['c5.large', 'c5.xlarge', 'm5.large']
            },
            WorkloadType.DATABASE: {
                'cpu_weight': 0.5,
                'memory_weight': 0.8,
                'storage_weight': 0.9,
                'network_weight': 0.3,
                'typical_cpu_util': 35,
                'typical_memory_util': 75,
                'scaling_pattern': 'vertical',
                'instance_types': ['r5.large', 'r5.xlarge', 'm5.large']
            },
            WorkloadType.CACHE: {
                'cpu_weight': 0.3,
                'memory_weight': 0.9,
                'storage_weight': 0.2,
                'network_weight': 0.5,
                'typical_cpu_util': 25,
                'typical_memory_util': 85,
                'scaling_pattern': 'horizontal',
                'instance_types': ['r5.large', 'r5.xlarge', 'r5.2xlarge']
            },
            WorkloadType.MACHINE_LEARNING: {
                'cpu_weight': 0.9,
                'memory_weight': 0.7,
                'storage_weight': 0.3,
                'network_weight': 0.2,
                'typical_cpu_util': 85,
                'typical_memory_util': 80,
                'scaling_pattern': 'vertical',
                'instance_types': ['c5.xlarge', 'c5.2xlarge', 'p3.large']
            },
            WorkloadType.MICROSERVICE: {
                'cpu_weight': 0.5,
                'memory_weight': 0.4,
                'storage_weight': 0.1,
                'network_weight': 0.4,
                'typical_cpu_util': 35,
                'typical_memory_util': 50,
                'scaling_pattern': 'horizontal',
                'instance_types': ['t3.micro', 't3.small', 't3.medium']
            }
        }
    
    def _initialize_instance_types(self) -> Dict[str, Dict[str, Any]]:
        """Initialize AWS instance type specifications."""
        return {
            't3.micro': {'cpu': 2, 'memory': 1, 'cost_hour': 0.0104, 'network': 'low'},
            't3.small': {'cpu': 2, 'memory': 2, 'cost_hour': 0.0208, 'network': 'low'},
            't3.medium': {'cpu': 2, 'memory': 4, 'cost_hour': 0.0416, 'network': 'moderate'},
            't3.large': {'cpu': 2, 'memory': 8, 'cost_hour': 0.0832, 'network': 'moderate'},
            't3.xlarge': {'cpu': 4, 'memory': 16, 'cost_hour': 0.1664, 'network': 'moderate'},
            'c5.large': {'cpu': 2, 'memory': 4, 'cost_hour': 0.085, 'network': 'moderate'},
            'c5.xlarge': {'cpu': 4, 'memory': 8, 'cost_hour': 0.17, 'network': 'high'},
            'c5.2xlarge': {'cpu': 8, 'memory': 16, 'cost_hour': 0.34, 'network': 'high'},
            'm5.large': {'cpu': 2, 'memory': 8, 'cost_hour': 0.096, 'network': 'moderate'},
            'm5.xlarge': {'cpu': 4, 'memory': 16, 'cost_hour': 0.192, 'network': 'high'},
            'r5.large': {'cpu': 2, 'memory': 16, 'cost_hour': 0.126, 'network': 'moderate'},
            'r5.xlarge': {'cpu': 4, 'memory': 32, 'cost_hour': 0.252, 'network': 'high'},
            'r5.2xlarge': {'cpu': 8, 'memory': 64, 'cost_hour': 0.504, 'network': 'high'},
            'p3.large': {'cpu': 4, 'memory': 61, 'cost_hour': 3.06, 'network': 'high', 'gpu': 1}
        }
    
    async def analyze_workload(self, application_id: str, metrics: Dict[str, Any]) -> WorkloadType:
        """Analyze application metrics to determine workload type."""
        try:
            # Extract key metrics
            cpu_util = metrics.get('avg_cpu_utilization', 50)
            memory_util = metrics.get('avg_memory_utilization', 50)
            request_rate = metrics.get('avg_request_rate', 100)
            response_time = metrics.get('avg_response_time', 100)
            error_rate = metrics.get('avg_error_rate', 1)
            
            # Scoring system for workload classification
            scores = {}
            
            # Web Application characteristics
            if 20 <= cpu_util <= 60 and 30 <= memory_util <= 70 and request_rate > 50:
                scores[WorkloadType.WEB_APPLICATION] = 0.8
            
            # API Service characteristics
            if 30 <= cpu_util <= 70 and 20 <= memory_util <= 60 and request_rate > 100:
                scores[WorkloadType.API_SERVICE] = 0.9
            
            # Batch Processing characteristics
            if cpu_util > 70 and memory_util > 60 and request_rate < 50:
                scores[WorkloadType.BATCH_PROCESSING] = 0.85
            
            # Database characteristics
            if cpu_util < 50 and memory_util > 60 and response_time > 50:
                scores[WorkloadType.DATABASE] = 0.7
            
            # Cache characteristics
            if cpu_util < 40 and memory_util > 70 and response_time < 50:
                scores[WorkloadType.CACHE] = 0.8
            
            # Machine Learning characteristics
            if cpu_util > 80 and memory_util > 70:
                scores[WorkloadType.MACHINE_LEARNING] = 0.9
            
            # Microservice characteristics (default for small workloads)
            if cpu_util < 50 and memory_util < 60 and request_rate < 200:
                scores[WorkloadType.MICROSERVICE] = 0.6
            
            # Return the highest scoring workload type
            if scores:
                best_workload = max(scores.items(), key=lambda x: x[1])[0]
                logger.info(f"Classified {application_id} as {best_workload}")
                return best_workload
            else:
                # Default to web application
                return WorkloadType.WEB_APPLICATION
                
        except Exception as e:
            logger.error(f"Workload analysis failed: {e}")
            return WorkloadType.WEB_APPLICATION
    
    def calculate_resource_requirements(
        self, 
        workload_type: WorkloadType,
        current_metrics: Dict[str, Any],
        optimization_goal: OptimizationGoal
    ) -> Dict[str, Any]:
        """Calculate optimal resource requirements."""
        try:
            profile = self.workload_profiles[workload_type]
            
            # Current utilization
            current_cpu = current_metrics.get('avg_cpu_utilization', 50)
            current_memory = current_metrics.get('avg_memory_utilization', 50)
            current_load = current_metrics.get('avg_request_rate', 100)
            
            # Target utilization based on optimization goal
            if optimization_goal == OptimizationGoal.COST_OPTIMIZED:
                target_cpu_util = 75
                target_memory_util = 80
                safety_margin = 1.1
            elif optimization_goal == OptimizationGoal.PERFORMANCE_OPTIMIZED:
                target_cpu_util = 50
                target_memory_util = 60
                safety_margin = 1.5
            elif optimization_goal == OptimizationGoal.HIGH_AVAILABILITY:
                target_cpu_util = 40
                target_memory_util = 50
                safety_margin = 2.0
            else:  # BALANCED
                target_cpu_util = 60
                target_memory_util = 70
                safety_margin = 1.3
            
            # Calculate required resources
            cpu_scaling_factor = (current_cpu / target_cpu_util) * safety_margin
            memory_scaling_factor = (current_memory / target_memory_util) * safety_margin
            
            # Find suitable instance types
            suitable_instances = []
            for instance_type in profile['instance_types']:
                if instance_type in self.instance_types:
                    spec = self.instance_types[instance_type]
                    
                    # Check if instance can handle the load
                    cpu_capacity = spec['cpu'] / cpu_scaling_factor
                    memory_capacity = spec['memory'] / memory_scaling_factor
                    
                    if cpu_capacity >= 1 and memory_capacity >= 1:
                        suitable_instances.append({
                            'instance_type': instance_type,
                            'cpu': spec['cpu'],
                            'memory': spec['memory'],
                            'cost_hour': spec['cost_hour'],
                            'cpu_capacity': cpu_capacity,
                            'memory_capacity': memory_capacity,
                            'efficiency_score': (cpu_capacity + memory_capacity) / (2 * spec['cost_hour'])
                        })
            
            # Sort by efficiency score
            suitable_instances.sort(key=lambda x: x['efficiency_score'], reverse=True)
            
            # Calculate instance count for horizontal scaling
            if profile['scaling_pattern'] == 'horizontal':
                base_instance_count = max(1, int(np.ceil(max(cpu_scaling_factor, memory_scaling_factor))))
                if optimization_goal == OptimizationGoal.HIGH_AVAILABILITY:
                    base_instance_count = max(2, base_instance_count)
            else:
                base_instance_count = 1
            
            return {
                'workload_type': workload_type,
                'optimization_goal': optimization_goal,
                'target_utilization': {
                    'cpu': target_cpu_util,
                    'memory': target_memory_util
                },
                'scaling_factors': {
                    'cpu': cpu_scaling_factor,
                    'memory': memory_scaling_factor
                },
                'suitable_instances': suitable_instances[:5],  # Top 5 options
                'recommended_instance_count': base_instance_count,
                'scaling_pattern': profile['scaling_pattern']
            }
            
        except Exception as e:
            logger.error(f"Resource requirement calculation failed: {e}")
            return {}
    
    async def generate_recommendation(
        self, 
        application_id: str,
        current_config: Dict[str, Any],
        metrics: Dict[str, Any],
        optimization_goal: OptimizationGoal = OptimizationGoal.BALANCED
    ) -> ResourceRecommendation:
        """Generate comprehensive resource recommendation."""
        try:
            # Analyze workload type
            workload_type = await self.analyze_workload(application_id, metrics)
            
            # Calculate resource requirements
            requirements = self.calculate_resource_requirements(
                workload_type, metrics, optimization_goal
            )
            
            if not requirements or not requirements.get('suitable_instances'):
                return self._get_default_recommendation(application_id, current_config)
            
            # Select best instance configuration
            best_instance = requirements['suitable_instances'][0]
            recommended_count = requirements['recommended_instance_count']
            
            recommended_config = {
                'instance_type': best_instance['instance_type'],
                'instance_count': recommended_count,
                'cpu_cores': best_instance['cpu'],
                'memory_gb': best_instance['memory'],
                'scaling_pattern': requirements['scaling_pattern'],
                'auto_scaling': {
                    'enabled': True,
                    'min_instances': max(1, recommended_count - 1),
                    'max_instances': recommended_count + 3,
                    'target_cpu_utilization': requirements['target_utilization']['cpu'],
                    'target_memory_utilization': requirements['target_utilization']['memory']
                }
            }
            
            # Calculate cost impact
            current_cost = self._calculate_cost(current_config)
            recommended_cost = self._calculate_cost(recommended_config)
            cost_impact = recommended_cost - current_cost
            
            # Determine performance impact
            performance_impact = self._assess_performance_impact(
                current_config, recommended_config, workload_type
            )
            
            # Calculate confidence
            confidence = self._calculate_recommendation_confidence(
                workload_type, requirements, metrics
            )
            
            # Generate reasoning
            reasoning = self._generate_reasoning(
                workload_type, current_config, recommended_config, 
                optimization_goal, requirements
            )
            
            # Generate alternatives
            alternatives = self._generate_alternatives(requirements['suitable_instances'][1:3])
            
            recommendation = ResourceRecommendation(
                application_id=application_id,
                workload_type=workload_type,
                optimization_goal=optimization_goal,
                recommended_config=recommended_config,
                current_config=current_config,
                cost_impact=cost_impact,
                performance_impact=performance_impact,
                confidence=confidence,
                reasoning=reasoning,
                alternatives=alternatives,
                metadata={
                    'analysis_timestamp': datetime.utcnow().isoformat(),
                    'metrics_analyzed': metrics,
                    'requirements': requirements
                }
            )
            
            # Store recommendation
            if application_id not in self.recommendation_history:
                self.recommendation_history[application_id] = []
            self.recommendation_history[application_id].append(recommendation)
            
            logger.info(f"Generated resource recommendation for {application_id}")
            return recommendation
            
        except Exception as e:
            logger.error(f"Resource recommendation generation failed: {e}")
            return self._get_default_recommendation(application_id, current_config)
    
    def _calculate_cost(self, config: Dict[str, Any]) -> float:
        """Calculate monthly cost for a configuration."""
        try:
            instance_type = config.get('instance_type', 't3.medium')
            instance_count = config.get('instance_count', 1)
            
            if instance_type in self.instance_types:
                hourly_cost = self.instance_types[instance_type]['cost_hour']
                monthly_cost = hourly_cost * 24 * 30 * instance_count
                return monthly_cost
            else:
                return 100.0  # Default estimate
                
        except:
            return 100.0
    
    def _assess_performance_impact(
        self, 
        current_config: Dict[str, Any], 
        recommended_config: Dict[str, Any],
        workload_type: WorkloadType
    ) -> str:
        """Assess performance impact of the recommendation."""
        try:
            current_cpu = current_config.get('cpu_cores', 2)
            current_memory = current_config.get('memory_gb', 4)
            current_instances = current_config.get('instance_count', 1)
            
            rec_cpu = recommended_config.get('cpu_cores', 2)
            rec_memory = recommended_config.get('memory_gb', 4)
            rec_instances = recommended_config.get('instance_count', 1)
            
            # Calculate total capacity
            current_total_cpu = current_cpu * current_instances
            current_total_memory = current_memory * current_instances
            
            rec_total_cpu = rec_cpu * rec_instances
            rec_total_memory = rec_memory * rec_instances
            
            cpu_change = (rec_total_cpu - current_total_cpu) / current_total_cpu
            memory_change = (rec_total_memory - current_total_memory) / current_total_memory
            
            if cpu_change > 0.2 or memory_change > 0.2:
                return "significant_improvement"
            elif cpu_change > 0.05 or memory_change > 0.05:
                return "moderate_improvement"
            elif cpu_change < -0.2 or memory_change < -0.2:
                return "potential_degradation"
            elif cpu_change < -0.05 or memory_change < -0.05:
                return "slight_degradation"
            else:
                return "minimal_change"
                
        except:
            return "unknown"
    
    def _calculate_recommendation_confidence(
        self, 
        workload_type: WorkloadType, 
        requirements: Dict[str, Any], 
        metrics: Dict[str, Any]
    ) -> float:
        """Calculate confidence score for the recommendation."""
        try:
            confidence = 0.7  # Base confidence
            
            # Adjust based on data quality
            if len(metrics) >= 5:
                confidence += 0.1
            
            # Adjust based on workload classification certainty
            if workload_type in [WorkloadType.WEB_APPLICATION, WorkloadType.API_SERVICE]:
                confidence += 0.1
            
            # Adjust based on suitable instances availability
            suitable_count = len(requirements.get('suitable_instances', []))
            if suitable_count >= 3:
                confidence += 0.1
            
            return max(0.3, min(0.95, confidence))
            
        except:
            return 0.5
    
    def _generate_reasoning(
        self, 
        workload_type: WorkloadType,
        current_config: Dict[str, Any],
        recommended_config: Dict[str, Any],
        optimization_goal: OptimizationGoal,
        requirements: Dict[str, Any]
    ) -> List[str]:
        """Generate human-readable reasoning for the recommendation."""
        reasoning = []
        
        reasoning.append(f"Workload classified as {workload_type.value}")
        reasoning.append(f"Optimization goal: {optimization_goal.value}")
        
        current_type = current_config.get('instance_type', 'unknown')
        rec_type = recommended_config.get('instance_type')
        
        if current_type != rec_type:
            reasoning.append(f"Recommended instance type change: {current_type} → {rec_type}")
        
        current_count = current_config.get('instance_count', 1)
        rec_count = recommended_config.get('instance_count', 1)
        
        if current_count != rec_count:
            reasoning.append(f"Recommended instance count: {current_count} → {rec_count}")
        
        scaling_pattern = requirements.get('scaling_pattern')
        if scaling_pattern:
            reasoning.append(f"Scaling pattern: {scaling_pattern}")
        
        return reasoning
    
    def _generate_alternatives(self, alternative_instances: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate alternative configurations."""
        alternatives = []
        
        for instance in alternative_instances:
            alternatives.append({
                'instance_type': instance['instance_type'],
                'cpu_cores': instance['cpu'],
                'memory_gb': instance['memory'],
                'cost_hour': instance['cost_hour'],
                'efficiency_score': instance['efficiency_score']
            })
        
        return alternatives
    
    def _get_default_recommendation(
        self, 
        application_id: str, 
        current_config: Dict[str, Any]
    ) -> ResourceRecommendation:
        """Return default recommendation when analysis fails."""
        return ResourceRecommendation(
            application_id=application_id,
            workload_type=WorkloadType.WEB_APPLICATION,
            optimization_goal=OptimizationGoal.BALANCED,
            recommended_config=current_config,
            current_config=current_config,
            cost_impact=0.0,
            performance_impact="no_change",
            confidence=0.3,
            reasoning=["Insufficient data for detailed analysis"],
            alternatives=[],
            metadata={'error': 'analysis_failed'}
        )
    
    async def get_recommendation_history(self, application_id: str) -> List[ResourceRecommendation]:
        """Get resource recommendation history for an application."""
        return self.recommendation_history.get(application_id, [])

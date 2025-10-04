"""
Edge Orchestrator

This module provides advanced orchestration capabilities for edge computing including
intelligent workload placement, auto-scaling, load balancing, and traffic routing.
"""

import asyncio
import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from uuid import UUID, uuid4
import logging
import math

from .edge_manager import EdgeLocation, EdgeWorkload, EdgeDeployment, DeploymentStatus, WorkloadType

logger = logging.getLogger(__name__)


class PlacementStrategy(Enum):
    """Workload placement strategies"""
    LATENCY_OPTIMIZED = "latency_optimized"
    COST_OPTIMIZED = "cost_optimized"
    BALANCED = "balanced"
    AVAILABILITY_FOCUSED = "availability_focused"
    PERFORMANCE_FOCUSED = "performance_focused"


class ScalingTrigger(Enum):
    """Auto-scaling trigger types"""
    CPU_UTILIZATION = "cpu_utilization"
    MEMORY_UTILIZATION = "memory_utilization"
    REQUEST_RATE = "request_rate"
    RESPONSE_TIME = "response_time"
    ERROR_RATE = "error_rate"
    CUSTOM_METRIC = "custom_metric"


class LoadBalancingAlgorithm(Enum):
    """Load balancing algorithms"""
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_CONNECTIONS = "least_connections"
    LEAST_RESPONSE_TIME = "least_response_time"
    GEOGRAPHIC = "geographic"
    HASH_BASED = "hash_based"


@dataclass
class WorkloadPlacement:
    """Represents a workload placement decision"""
    placement_id: str
    workload_id: str
    strategy: PlacementStrategy
    selected_locations: List[str]
    placement_score: float
    reasoning: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'placement_id': self.placement_id,
            'workload_id': self.workload_id,
            'strategy': self.strategy.value,
            'selected_locations': self.selected_locations,
            'placement_score': self.placement_score,
            'reasoning': self.reasoning,
            'constraints': self.constraints,
            'created_at': self.created_at.isoformat()
        }


@dataclass
class EdgeScalingPolicy:
    """Auto-scaling policy for edge deployments"""
    policy_id: str
    workload_id: str
    trigger: ScalingTrigger
    threshold_up: float
    threshold_down: float
    min_instances: int = 1
    max_instances: int = 10
    scale_up_cooldown: int = 300  # seconds
    scale_down_cooldown: int = 600  # seconds
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class EdgeLoadBalancer:
    """Edge load balancer configuration"""
    lb_id: str
    name: str
    workload_id: str
    algorithm: LoadBalancingAlgorithm
    target_deployments: List[str] = field(default_factory=list)
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)


class EdgeOrchestrator:
    """
    Advanced edge orchestrator for intelligent workload placement and management
    """
    
    def __init__(self, edge_manager):
        self.edge_manager = edge_manager
        self.placements: Dict[str, WorkloadPlacement] = {}
        self.scaling_policies: Dict[str, EdgeScalingPolicy] = {}
        self.load_balancers: Dict[str, EdgeLoadBalancer] = {}
        self.scaling_history: Dict[str, List[Dict[str, Any]]] = {}
        self.traffic_patterns: Dict[str, List[Dict[str, Any]]] = {}
        
    async def create_intelligent_placement(self, workload_id: str,
                                         strategy: PlacementStrategy,
                                         user_locations: List[Dict[str, float]] = None,
                                         constraints: Dict[str, Any] = None) -> WorkloadPlacement:
        """Create intelligent workload placement"""
        try:
            if workload_id not in self.edge_manager.workloads:
                raise ValueError(f"Workload {workload_id} not found")
                
            workload = self.edge_manager.workloads[workload_id]
            user_locations = user_locations or []
            constraints = constraints or {}
            
            # Get available edge locations
            available_locations = await self.edge_manager.get_edge_locations()
            
            # Select optimal locations based on strategy
            selected_locations, score, reasoning = await self._select_locations(
                workload, available_locations, strategy, user_locations, constraints
            )
            
            placement = WorkloadPlacement(
                placement_id=f"placement-{workload_id}-{str(uuid4())[:8]}",
                workload_id=workload_id,
                strategy=strategy,
                selected_locations=selected_locations,
                placement_score=score,
                reasoning=reasoning,
                constraints=constraints
            )
            
            self.placements[placement.placement_id] = placement
            logger.info(f"Created placement {placement.placement_id} for workload {workload_id}")
            
            return placement
            
        except Exception as e:
            logger.error(f"Failed to create placement for workload {workload_id}: {e}")
            raise
            
    async def _select_locations(self, workload: EdgeWorkload,
                              locations: List[EdgeLocation],
                              strategy: PlacementStrategy,
                              user_locations: List[Dict[str, float]],
                              constraints: Dict[str, Any]) -> Tuple[List[str], float, Dict[str, Any]]:
        """Select optimal locations based on strategy"""
        
        max_locations = constraints.get('max_locations', 3)
        
        if strategy == PlacementStrategy.LATENCY_OPTIMIZED:
            return await self._latency_optimized_placement(
                workload, locations, user_locations, max_locations
            )
        elif strategy == PlacementStrategy.COST_OPTIMIZED:
            return await self._cost_optimized_placement(
                workload, locations, max_locations
            )
        else:  # Default to balanced
            return await self._balanced_placement(
                workload, locations, user_locations, max_locations
            )
            
    async def _latency_optimized_placement(self, workload: EdgeWorkload,
                                         locations: List[EdgeLocation],
                                         user_locations: List[Dict[str, float]],
                                         max_locations: int) -> Tuple[List[str], float, Dict[str, Any]]:
        """Select locations optimized for lowest latency"""
        
        location_scores = []
        
        for location in locations:
            # Calculate average latency to user locations
            if user_locations:
                total_latency = 0
                for user_loc in user_locations:
                    lat_diff = abs(location.latitude - user_loc.get('latitude', 0))
                    lon_diff = abs(location.longitude - user_loc.get('longitude', 0))
                    distance = math.sqrt(lat_diff**2 + lon_diff**2) * 111  # Rough km
                    latency = min(distance * 0.1, 200)  # Max 200ms
                    total_latency += latency
                avg_latency = total_latency / len(user_locations)
            else:
                avg_latency = 50  # Default latency
                
            # Score based on latency (lower is better)
            score = max(0, 200 - avg_latency)
            location_scores.append((location.location_id, score, avg_latency))
            
        # Sort by score and select top locations
        location_scores.sort(key=lambda x: x[1], reverse=True)
        selected = location_scores[:max_locations]
        
        selected_ids = [loc_id for loc_id, _, _ in selected]
        avg_score = sum(score for _, score, _ in selected) / len(selected)
        
        reasoning = {
            'strategy': 'latency_optimized',
            'average_latency_ms': sum(latency for _, _, latency in selected) / len(selected),
            'location_scores': {loc_id: score for loc_id, score, _ in selected}
        }
        
        return selected_ids, avg_score, reasoning
        
    async def _cost_optimized_placement(self, workload: EdgeWorkload,
                                      locations: List[EdgeLocation],
                                      max_locations: int) -> Tuple[List[str], float, Dict[str, Any]]:
        """Select locations optimized for lowest cost"""
        
        location_scores = []
        
        for location in locations:
            # Calculate average cost for required capabilities
            required_caps = self.edge_manager._get_required_capabilities(workload.workload_type)
            total_cost = sum(location.cost_per_hour.get(cap, 0.1) for cap in required_caps)
            avg_cost = total_cost / len(required_caps) if required_caps else 0.1
            
            # Score based on cost (lower is better)
            score = max(0, 100 - (avg_cost * 500))  # $0.20/hour = 0 score
            location_scores.append((location.location_id, score, avg_cost))
            
        # Sort by score and select top locations
        location_scores.sort(key=lambda x: x[1], reverse=True)
        selected = location_scores[:max_locations]
        
        selected_ids = [loc_id for loc_id, _, _ in selected]
        avg_score = sum(score for _, score, _ in selected) / len(selected)
        
        reasoning = {
            'strategy': 'cost_optimized',
            'average_cost_per_hour': sum(cost for _, _, cost in selected) / len(selected),
            'location_costs': {loc_id: cost for loc_id, _, cost in selected}
        }
        
        return selected_ids, avg_score, reasoning
        
    async def _balanced_placement(self, workload: EdgeWorkload,
                                locations: List[EdgeLocation],
                                user_locations: List[Dict[str, float]],
                                max_locations: int) -> Tuple[List[str], float, Dict[str, Any]]:
        """Select locations with balanced cost and performance"""
        
        location_scores = []
        
        for location in locations:
            # Latency score
            if user_locations:
                total_latency = 0
                for user_loc in user_locations:
                    lat_diff = abs(location.latitude - user_loc.get('latitude', 0))
                    lon_diff = abs(location.longitude - user_loc.get('longitude', 0))
                    distance = math.sqrt(lat_diff**2 + lon_diff**2) * 111
                    latency = min(distance * 0.1, 200)
                    total_latency += latency
                avg_latency = total_latency / len(user_locations)
            else:
                avg_latency = 50
                
            latency_score = max(0, 200 - avg_latency)
            
            # Cost score
            required_caps = self.edge_manager._get_required_capabilities(workload.workload_type)
            total_cost = sum(location.cost_per_hour.get(cap, 0.1) for cap in required_caps)
            avg_cost = total_cost / len(required_caps) if required_caps else 0.1
            cost_score = max(0, 100 - (avg_cost * 500))
            
            # Capacity score
            cpu_utilization = location.current_load.get('cpu', 0)
            capacity_score = max(0, 100 - cpu_utilization)
            
            # Balanced score (equal weights)
            balanced_score = (latency_score * 0.4 + cost_score * 0.3 + capacity_score * 0.3)
            
            location_scores.append((location.location_id, balanced_score, {
                'latency_ms': avg_latency,
                'cost_per_hour': avg_cost,
                'cpu_utilization': cpu_utilization
            }))
            
        # Sort by score and select top locations
        location_scores.sort(key=lambda x: x[1], reverse=True)
        selected = location_scores[:max_locations]
        
        selected_ids = [loc_id for loc_id, _, _ in selected]
        avg_score = sum(score for _, score, _ in selected) / len(selected)
        
        reasoning = {
            'strategy': 'balanced',
            'location_details': {loc_id: details for loc_id, _, details in selected}
        }
        
        return selected_ids, avg_score, reasoning
        
    async def create_scaling_policy(self, policy: EdgeScalingPolicy) -> bool:
        """Create auto-scaling policy"""
        try:
            self.scaling_policies[policy.policy_id] = policy
            logger.info(f"Created scaling policy {policy.policy_id} for workload {policy.workload_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create scaling policy: {e}")
            return False
            
    async def create_load_balancer(self, load_balancer: EdgeLoadBalancer) -> bool:
        """Create edge load balancer"""
        try:
            self.load_balancers[load_balancer.lb_id] = load_balancer
            logger.info(f"Created load balancer {load_balancer.lb_id} for workload {load_balancer.workload_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create load balancer: {e}")
            return False
            
    async def get_workload_insights(self, workload_id: str) -> Dict[str, Any]:
        """Get performance insights for workload"""
        try:
            insights = {
                'workload_id': workload_id,
                'placement_info': {},
                'scaling_history': [],
                'traffic_patterns': [],
                'recommendations': []
            }
            
            # Get placement information
            placement = None
            for p in self.placements.values():
                if p.workload_id == workload_id:
                    placement = p
                    break
                    
            if placement:
                insights['placement_info'] = placement.to_dict()
                
            return insights
            
        except Exception as e:
            logger.error(f"Failed to get workload insights: {e}")
            return {}
            
    async def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get orchestrator status and statistics"""
        try:
            status = {
                'placements': {
                    'total': len(self.placements),
                    'strategies': {}
                },
                'scaling_policies': {
                    'total': len(self.scaling_policies),
                    'enabled': len([p for p in self.scaling_policies.values() if p.enabled])
                },
                'load_balancers': {
                    'total': len(self.load_balancers),
                    'enabled': len([lb for lb in self.load_balancers.values() if lb.enabled])
                }
            }
            
            # Strategy breakdown
            for placement in self.placements.values():
                strategy = placement.strategy.value
                status['placements']['strategies'][strategy] = \
                    status['placements']['strategies'].get(strategy, 0) + 1
                    
            return status
            
        except Exception as e:
            logger.error(f"Failed to get orchestrator status: {e}")
            return {}


# Example usage
async def example_edge_orchestrator():
    """Example of using the edge orchestrator"""
    
    from .edge_manager import EdgeManager, EdgeWorkload, WorkloadType
    
    # Create edge manager and orchestrator
    edge_manager = EdgeManager()
    orchestrator = EdgeOrchestrator(edge_manager)
    
    # Create a workload
    workload = EdgeWorkload(
        workload_id='api-service-001',
        name='API Gateway Service',
        workload_type=WorkloadType.API_GATEWAY,
        application_id='api-gateway',
        image='nginx:latest',
        resource_requirements={
            'cpu_cores': 1,
            'memory_gb': 2
        }
    )
    
    await edge_manager.create_workload(workload)
    
    # Create intelligent placement
    user_locations = [
        {'latitude': 40.7128, 'longitude': -74.0060},  # New York
        {'latitude': 34.0522, 'longitude': -118.2437}  # Los Angeles
    ]
    
    placement = await orchestrator.create_intelligent_placement(
        'api-service-001',
        PlacementStrategy.BALANCED,
        user_locations,
        {'max_locations': 2}
    )
    
    print(f"Created placement: {placement.placement_id}")
    print(f"Selected locations: {placement.selected_locations}")
    print(f"Placement score: {placement.placement_score}")
    
    # Deploy workload to selected locations
    deployment_ids = await edge_manager.deploy_workload(
        'api-service-001',
        placement.selected_locations
    )
    
    # Create scaling policy
    scaling_policy = EdgeScalingPolicy(
        policy_id='policy-api-001',
        workload_id='api-service-001',
        trigger=ScalingTrigger.CPU_UTILIZATION,
        threshold_up=70.0,
        threshold_down=30.0,
        min_instances=1,
        max_instances=5
    )
    
    await orchestrator.create_scaling_policy(scaling_policy)
    
    # Create load balancer
    load_balancer = EdgeLoadBalancer(
        lb_id='lb-api-001',
        name='API Gateway Load Balancer',
        workload_id='api-service-001',
        algorithm=LoadBalancingAlgorithm.LEAST_RESPONSE_TIME,
        target_deployments=deployment_ids
    )
    
    await orchestrator.create_load_balancer(load_balancer)
    
    # Get orchestrator status
    status = await orchestrator.get_orchestrator_status()
    print(f"Orchestrator status: {status}")


if __name__ == "__main__":
    asyncio.run(example_edge_orchestrator())

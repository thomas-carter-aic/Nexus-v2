"""
AI/ML Edge Optimization Module

This module provides specialized AI/ML workload optimization for edge computing,
including intelligent model placement, inference optimization, federated learning
coordination, and AI-specific resource management.

Key Features:
- AI model placement optimization across edge locations
- Inference latency and throughput optimization
- Federated learning coordination and management
- AI-specific resource allocation and scaling
- Model versioning and A/B testing at the edge
- Real-time AI performance monitoring and optimization
"""

from .ai_edge_manager import (
    AIEdgeManager,
    AIModel,
    ModelDeployment,
    InferenceEndpoint,
    FederatedLearningJob,
    AIWorkloadType,
    ModelFormat,
    OptimizationTarget
)

from .ai_edge_optimizer import (
    AIEdgeOptimizer,
    ModelPlacementStrategy,
    InferenceOptimizationType
)

from .ai_edge_monitor import (
    AIEdgeMonitor,
    InferenceMetrics,
    ModelPerformanceTracker,
    AIAnomalyDetector
)

__all__ = [
    'AIEdgeManager',
    'AIModel',
    'ModelDeployment', 
    'InferenceEndpoint',
    'FederatedLearningJob',
    'AIWorkloadType',
    'ModelFormat',
    'OptimizationTarget',
    'AIEdgeOptimizer',
    'ModelPlacementStrategy',
    'InferenceOptimizationType',
    'AIEdgeMonitor',
    'InferenceMetrics',
    'ModelPerformanceTracker',
    'AIAnomalyDetector'
]

__version__ = "1.0.0"

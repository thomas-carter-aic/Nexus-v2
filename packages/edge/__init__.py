"""
Edge Computing Integration Module

This module provides comprehensive edge computing capabilities for the AI-Native PaaS Platform,
enabling distributed application deployment across edge locations, CDN integration, and
intelligent workload placement for optimal performance and latency reduction.

Key Features:
- Edge location management and orchestration
- Intelligent workload placement and routing
- CDN integration and content optimization
- Real-time performance monitoring and optimization
- Edge-to-cloud data synchronization
- IoT device management and edge analytics
"""

from .edge_manager import (
    EdgeLocation,
    EdgeProvider,
    EdgeCapability,
    EdgeWorkload,
    EdgeDeployment,
    EdgeManager,
    CDNIntegration,
    IoTDeviceManager
)

from .edge_orchestrator import (
    EdgeOrchestrator,
    WorkloadPlacement,
    EdgeScalingPolicy,
    EdgeLoadBalancer
)

__all__ = [
    'EdgeLocation',
    'EdgeProvider', 
    'EdgeCapability',
    'EdgeWorkload',
    'EdgeDeployment',
    'EdgeManager',
    'CDNIntegration',
    'IoTDeviceManager',
    'EdgeOrchestrator',
    'WorkloadPlacement',
    'EdgeScalingPolicy',
    'EdgeLoadBalancer'
]

__version__ = "1.0.0"

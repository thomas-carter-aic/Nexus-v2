"""
Multi-Cloud Management Module

This module provides comprehensive multi-cloud management capabilities for the AI-Native PaaS Platform.
It enables unified management across AWS, Azure, GCP, and other cloud providers with intelligent
orchestration, cost optimization, and seamless resource migration.

Key Features:
- Unified API across multiple cloud providers
- Intelligent provider selection based on cost and performance
- Automated resource migration and disaster recovery
- Real-time cost comparison and optimization
- Multi-cloud compliance and security management
"""

from .cloud_provider_manager import (
    CloudProvider,
    ServiceType,
    ResourceStatus,
    ProviderConfig,
    CloudResource,
    CloudProviderInterface,
    CloudProviderManager,
    AWSProvider,
    AzureProvider,
    GCPProvider
)

__all__ = [
    'CloudProvider',
    'ServiceType', 
    'ResourceStatus',
    'ProviderConfig',
    'CloudResource',
    'CloudProviderInterface',
    'CloudProviderManager',
    'AWSProvider',
    'AzureProvider',
    'GCPProvider'
]

__version__ = "1.0.0"

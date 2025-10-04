"""
Plugin system for the AI-Native PaaS Platform.

This module provides a secure, extensible plugin architecture that allows
third-party developers to extend platform functionality while maintaining
security and isolation.
"""

from .base import PluginBase, PluginMetadata, PluginContext
from .manager import PluginManager
from .registry import PluginRegistry
from .sandbox import PluginSandbox

__all__ = [
    'PluginBase',
    'PluginMetadata', 
    'PluginContext',
    'PluginManager',
    'PluginRegistry',
    'PluginSandbox'
]

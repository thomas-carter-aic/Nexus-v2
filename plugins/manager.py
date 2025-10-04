"""
Plugin manager for loading, executing, and managing plugins.
"""

import asyncio
import importlib
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta

from .base import PluginBase, PluginMetadata, PluginContext, PluginStatus, PluginType
from .registry import PluginRegistry
from .sandbox import PluginSandbox


class PluginManager:
    """Manages plugin lifecycle and execution."""
    
    def __init__(self, registry: PluginRegistry, sandbox: PluginSandbox):
        self.registry = registry
        self.sandbox = sandbox
        self.loaded_plugins: Dict[str, PluginBase] = {}
        self.plugin_contexts: Dict[str, PluginContext] = {}
        self.logger = logging.getLogger(__name__)
        self.execution_stats: Dict[str, Dict[str, Any]] = {}
        
    async def load_plugin(self, plugin_path: str, config: Dict[str, Any] = None) -> bool:
        """
        Load a plugin from the specified path.
        
        Args:
            plugin_path: Path to the plugin directory or file
            config: Plugin configuration
            
        Returns:
            True if plugin loaded successfully
        """
        try:
            # Validate plugin structure
            if not await self._validate_plugin_structure(plugin_path):
                self.logger.error(f"Invalid plugin structure: {plugin_path}")
                return False
            
            # Load plugin metadata
            metadata = await self._load_plugin_metadata(plugin_path)
            if not metadata:
                self.logger.error(f"Failed to load plugin metadata: {plugin_path}")
                return False
            
            # Check if plugin already loaded
            if metadata.name in self.loaded_plugins:
                self.logger.warning(f"Plugin already loaded: {metadata.name}")
                return True
            
            # Validate dependencies
            if not await self._validate_dependencies(metadata):
                self.logger.error(f"Plugin dependencies not met: {metadata.name}")
                return False
            
            # Load plugin in sandbox
            plugin_instance = await self.sandbox.load_plugin(plugin_path, metadata)
            if not plugin_instance:
                self.logger.error(f"Failed to load plugin in sandbox: {metadata.name}")
                return False
            
            # Register plugin
            await self.registry.register_plugin(metadata, plugin_path)
            
            # Store loaded plugin
            self.loaded_plugins[metadata.name] = plugin_instance
            
            # Initialize execution stats
            self.execution_stats[metadata.name] = {
                "total_executions": 0,
                "successful_executions": 0,
                "failed_executions": 0,
                "average_execution_time": 0.0,
                "last_execution": None
            }
            
            self.logger.info(f"Plugin loaded successfully: {metadata.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading plugin {plugin_path}: {str(e)}")
            return False
    
    async def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload a plugin.
        
        Args:
            plugin_name: Name of the plugin to unload
            
        Returns:
            True if plugin unloaded successfully
        """
        try:
            if plugin_name not in self.loaded_plugins:
                self.logger.warning(f"Plugin not loaded: {plugin_name}")
                return True
            
            plugin = self.loaded_plugins[plugin_name]
            
            # Cleanup plugin resources
            if plugin_name in self.plugin_contexts:
                await plugin.cleanup(self.plugin_contexts[plugin_name])
            
            # Unload from sandbox
            await self.sandbox.unload_plugin(plugin_name)
            
            # Unregister plugin
            await self.registry.unregister_plugin(plugin_name)
            
            # Remove from loaded plugins
            del self.loaded_plugins[plugin_name]
            if plugin_name in self.plugin_contexts:
                del self.plugin_contexts[plugin_name]
            if plugin_name in self.execution_stats:
                del self.execution_stats[plugin_name]
            
            self.logger.info(f"Plugin unloaded successfully: {plugin_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error unloading plugin {plugin_name}: {str(e)}")
            return False
    
    async def execute_plugin(self, plugin_name: str, context: PluginContext, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Execute a plugin with the provided context.
        
        Args:
            plugin_name: Name of the plugin to execute
            context: Plugin execution context
            **kwargs: Additional execution parameters
            
        Returns:
            Plugin execution result or None if failed
        """
        if plugin_name not in self.loaded_plugins:
            self.logger.error(f"Plugin not loaded: {plugin_name}")
            return None
        
        plugin = self.loaded_plugins[plugin_name]
        
        # Check plugin status
        if plugin.status == PluginStatus.SUSPENDED:
            self.logger.warning(f"Plugin suspended due to errors: {plugin_name}")
            return None
        
        start_time = datetime.now()
        
        try:
            # Initialize plugin if not active
            if plugin.status == PluginStatus.INACTIVE:
                if not await plugin.initialize(context):
                    self.logger.error(f"Plugin initialization failed: {plugin_name}")
                    plugin.increment_error_count()
                    return None
                plugin.status = PluginStatus.ACTIVE
                self.plugin_contexts[plugin_name] = context
            
            # Execute plugin in sandbox
            result = await self.sandbox.execute_plugin(plugin_name, context, **kwargs)
            
            # Update execution stats
            execution_time = (datetime.now() - start_time).total_seconds()
            self._update_execution_stats(plugin_name, True, execution_time)
            
            # Reset error count on successful execution
            plugin.reset_error_count()
            plugin.last_execution = datetime.now()
            
            return result
            
        except Exception as e:
            self.logger.error(f"Plugin execution failed {plugin_name}: {str(e)}")
            
            # Update execution stats
            execution_time = (datetime.now() - start_time).total_seconds()
            self._update_execution_stats(plugin_name, False, execution_time)
            
            # Increment error count
            plugin.increment_error_count()
            
            return None
    
    async def execute_plugins_by_type(self, plugin_type: PluginType, context: PluginContext, **kwargs) -> Dict[str, Any]:
        """
        Execute all plugins of a specific type.
        
        Args:
            plugin_type: Type of plugins to execute
            context: Plugin execution context
            **kwargs: Additional execution parameters
            
        Returns:
            Dictionary of plugin results
        """
        results = {}
        
        # Get plugins by type
        plugins_by_type = await self.registry.get_plugins_by_type(plugin_type)
        
        # Execute plugins concurrently
        tasks = []
        for plugin_name in plugins_by_type:
            if plugin_name in self.loaded_plugins:
                task = self.execute_plugin(plugin_name, context, **kwargs)
                tasks.append((plugin_name, task))
        
        # Wait for all executions to complete
        for plugin_name, task in tasks:
            try:
                result = await task
                results[plugin_name] = result
            except Exception as e:
                self.logger.error(f"Error executing plugin {plugin_name}: {str(e)}")
                results[plugin_name] = None
        
        return results
    
    async def get_plugin_health(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """
        Get health status of a plugin.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Plugin health information
        """
        if plugin_name not in self.loaded_plugins:
            return None
        
        plugin = self.loaded_plugins[plugin_name]
        context = self.plugin_contexts.get(plugin_name)
        
        if context:
            health_info = await plugin.health_check(context)
        else:
            health_info = {
                "status": plugin.status.value,
                "last_execution": plugin.last_execution,
                "error_count": plugin.error_count,
                "healthy": plugin.error_count < plugin.max_errors
            }
        
        # Add execution stats
        if plugin_name in self.execution_stats:
            health_info["execution_stats"] = self.execution_stats[plugin_name]
        
        return health_info
    
    async def list_loaded_plugins(self) -> List[Dict[str, Any]]:
        """
        List all loaded plugins with their status.
        
        Returns:
            List of plugin information
        """
        plugins_info = []
        
        for plugin_name, plugin in self.loaded_plugins.items():
            health = await self.get_plugin_health(plugin_name)
            
            plugin_info = {
                "name": plugin.metadata.name,
                "version": plugin.metadata.version,
                "type": plugin.metadata.plugin_type.value,
                "status": plugin.status.value,
                "author": plugin.metadata.author,
                "description": plugin.metadata.description,
                "health": health
            }
            
            plugins_info.append(plugin_info)
        
        return plugins_info
    
    async def reload_plugin(self, plugin_name: str) -> bool:
        """
        Reload a plugin.
        
        Args:
            plugin_name: Name of the plugin to reload
            
        Returns:
            True if plugin reloaded successfully
        """
        # Get plugin path from registry
        plugin_info = await self.registry.get_plugin_info(plugin_name)
        if not plugin_info:
            self.logger.error(f"Plugin not found in registry: {plugin_name}")
            return False
        
        plugin_path = plugin_info.get("path")
        if not plugin_path:
            self.logger.error(f"Plugin path not found: {plugin_name}")
            return False
        
        # Unload and reload plugin
        await self.unload_plugin(plugin_name)
        return await self.load_plugin(plugin_path)
    
    async def _validate_plugin_structure(self, plugin_path: str) -> bool:
        """Validate plugin directory structure."""
        path = Path(plugin_path)
        
        if path.is_file() and path.suffix == '.py':
            return True
        
        if path.is_dir():
            # Check for required files
            required_files = ['__init__.py', 'plugin.py', 'metadata.json']
            for required_file in required_files:
                if not (path / required_file).exists():
                    return False
            return True
        
        return False
    
    async def _load_plugin_metadata(self, plugin_path: str) -> Optional[PluginMetadata]:
        """Load plugin metadata from metadata.json or plugin module."""
        try:
            path = Path(plugin_path)
            
            if path.is_file():
                # Load metadata from module docstring or attributes
                spec = importlib.util.spec_from_file_location("plugin_module", path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Try to get metadata from module
                if hasattr(module, 'PLUGIN_METADATA'):
                    metadata_dict = module.PLUGIN_METADATA
                    return PluginMetadata(**metadata_dict)
            
            elif path.is_dir():
                # Load metadata from metadata.json
                metadata_file = path / 'metadata.json'
                if metadata_file.exists():
                    import json
                    with open(metadata_file, 'r') as f:
                        metadata_dict = json.load(f)
                    
                    # Convert plugin_type string to enum
                    if 'plugin_type' in metadata_dict:
                        metadata_dict['plugin_type'] = PluginType(metadata_dict['plugin_type'])
                    
                    return PluginMetadata(**metadata_dict)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error loading plugin metadata: {str(e)}")
            return None
    
    async def _validate_dependencies(self, metadata: PluginMetadata) -> bool:
        """Validate plugin dependencies."""
        for dependency in metadata.dependencies:
            try:
                importlib.import_module(dependency)
            except ImportError:
                self.logger.error(f"Missing dependency: {dependency}")
                return False
        return True
    
    def _update_execution_stats(self, plugin_name: str, success: bool, execution_time: float):
        """Update plugin execution statistics."""
        if plugin_name not in self.execution_stats:
            return
        
        stats = self.execution_stats[plugin_name]
        stats["total_executions"] += 1
        stats["last_execution"] = datetime.now()
        
        if success:
            stats["successful_executions"] += 1
        else:
            stats["failed_executions"] += 1
        
        # Update average execution time
        total_time = stats["average_execution_time"] * (stats["total_executions"] - 1)
        stats["average_execution_time"] = (total_time + execution_time) / stats["total_executions"]

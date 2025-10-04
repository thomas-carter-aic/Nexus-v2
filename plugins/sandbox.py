"""
Plugin sandbox for secure plugin execution with resource isolation.
"""

import asyncio
import sys
import os
import resource
import signal
import multiprocessing
from typing import Dict, Any, Optional
from pathlib import Path
import logging
import importlib.util
from contextlib import contextmanager
import tempfile
import shutil

from .base import PluginBase, PluginMetadata, PluginContext


class ResourceLimits:
    """Resource limits for plugin execution."""
    
    def __init__(self):
        self.max_memory_mb = 512  # 512MB memory limit
        self.max_cpu_time_seconds = 30  # 30 seconds CPU time
        self.max_file_descriptors = 100
        self.max_processes = 5
        self.max_file_size_mb = 100  # 100MB file size limit
        self.allowed_network_hosts = []  # Restricted network access
        self.allowed_file_paths = []  # Restricted file system access


class PluginSandbox:
    """Secure sandbox for plugin execution."""
    
    def __init__(self, sandbox_dir: str = "/tmp/plugin_sandbox"):
        self.sandbox_dir = Path(sandbox_dir)
        self.sandbox_dir.mkdir(exist_ok=True)
        self.resource_limits = ResourceLimits()
        self.logger = logging.getLogger(__name__)
        self.active_plugins: Dict[str, Dict[str, Any]] = {}
        
    async def load_plugin(self, plugin_path: str, metadata: PluginMetadata) -> Optional[PluginBase]:
        """
        Load a plugin in the sandbox environment.
        
        Args:
            plugin_path: Path to the plugin
            metadata: Plugin metadata
            
        Returns:
            Plugin instance or None if loading failed
        """
        try:
            # Create isolated directory for plugin
            plugin_sandbox_dir = self.sandbox_dir / metadata.name
            plugin_sandbox_dir.mkdir(exist_ok=True)
            
            # Copy plugin files to sandbox
            await self._copy_plugin_to_sandbox(plugin_path, plugin_sandbox_dir)
            
            # Load plugin module in restricted environment
            plugin_instance = await self._load_plugin_module(plugin_sandbox_dir, metadata)
            
            if plugin_instance:
                self.active_plugins[metadata.name] = {
                    "instance": plugin_instance,
                    "sandbox_dir": plugin_sandbox_dir,
                    "metadata": metadata,
                    "resource_usage": {
                        "memory_usage": 0,
                        "cpu_time": 0,
                        "file_operations": 0,
                        "network_requests": 0
                    }
                }
                
                self.logger.info(f"Plugin loaded in sandbox: {metadata.name}")
                return plugin_instance
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error loading plugin in sandbox {metadata.name}: {str(e)}")
            return None
    
    async def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload a plugin from the sandbox.
        
        Args:
            plugin_name: Name of the plugin to unload
            
        Returns:
            True if unloading successful
        """
        try:
            if plugin_name not in self.active_plugins:
                return True
            
            plugin_info = self.active_plugins[plugin_name]
            
            # Clean up sandbox directory
            sandbox_dir = plugin_info["sandbox_dir"]
            if sandbox_dir.exists():
                shutil.rmtree(sandbox_dir)
            
            # Remove from active plugins
            del self.active_plugins[plugin_name]
            
            self.logger.info(f"Plugin unloaded from sandbox: {plugin_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error unloading plugin from sandbox {plugin_name}: {str(e)}")
            return False
    
    async def execute_plugin(self, plugin_name: str, context: PluginContext, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Execute a plugin in the sandbox with resource limits.
        
        Args:
            plugin_name: Name of the plugin to execute
            context: Plugin execution context
            **kwargs: Additional execution parameters
            
        Returns:
            Plugin execution result or None if failed
        """
        if plugin_name not in self.active_plugins:
            self.logger.error(f"Plugin not loaded in sandbox: {plugin_name}")
            return None
        
        plugin_info = self.active_plugins[plugin_name]
        plugin_instance = plugin_info["instance"]
        
        try:
            # Execute plugin with resource limits
            result = await self._execute_with_limits(plugin_instance, context, **kwargs)
            
            # Update resource usage tracking
            await self._update_resource_usage(plugin_name)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error executing plugin in sandbox {plugin_name}: {str(e)}")
            return None
    
    async def get_resource_usage(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """
        Get resource usage statistics for a plugin.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Resource usage information
        """
        if plugin_name not in self.active_plugins:
            return None
        
        return self.active_plugins[plugin_name]["resource_usage"].copy()
    
    async def set_resource_limits(self, limits: ResourceLimits):
        """
        Set resource limits for plugin execution.
        
        Args:
            limits: Resource limits configuration
        """
        self.resource_limits = limits
        self.logger.info("Updated plugin resource limits")
    
    async def _copy_plugin_to_sandbox(self, plugin_path: str, sandbox_dir: Path):
        """Copy plugin files to sandbox directory."""
        source_path = Path(plugin_path)
        
        if source_path.is_file():
            # Copy single file
            shutil.copy2(source_path, sandbox_dir / source_path.name)
        elif source_path.is_dir():
            # Copy directory contents
            for item in source_path.iterdir():
                if item.is_file():
                    shutil.copy2(item, sandbox_dir / item.name)
                elif item.is_dir() and item.name != "__pycache__":
                    shutil.copytree(item, sandbox_dir / item.name, dirs_exist_ok=True)
    
    async def _load_plugin_module(self, sandbox_dir: Path, metadata: PluginMetadata) -> Optional[PluginBase]:
        """Load plugin module from sandbox directory."""
        try:
            # Add sandbox directory to Python path temporarily
            sys.path.insert(0, str(sandbox_dir))
            
            try:
                # Try to load from plugin.py
                plugin_file = sandbox_dir / "plugin.py"
                if plugin_file.exists():
                    spec = importlib.util.spec_from_file_location("plugin_module", plugin_file)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                else:
                    # Try to load from __init__.py
                    module = importlib.import_module(metadata.name)
                
                # Find plugin class
                plugin_class = None
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, PluginBase) and 
                        attr != PluginBase):
                        plugin_class = attr
                        break
                
                if plugin_class:
                    return plugin_class(metadata)
                else:
                    self.logger.error(f"No plugin class found in module: {metadata.name}")
                    return None
                    
            finally:
                # Remove sandbox directory from Python path
                sys.path.remove(str(sandbox_dir))
                
        except Exception as e:
            self.logger.error(f"Error loading plugin module {metadata.name}: {str(e)}")
            return None
    
    async def _execute_with_limits(self, plugin_instance: PluginBase, context: PluginContext, **kwargs) -> Dict[str, Any]:
        """Execute plugin with resource limits applied."""
        
        # Create a restricted execution environment
        with self._apply_resource_limits():
            # Execute plugin in a separate process for better isolation
            if self.resource_limits.max_processes > 1:
                return await self._execute_in_process(plugin_instance, context, **kwargs)
            else:
                return await plugin_instance.execute(context, **kwargs)
    
    async def _execute_in_process(self, plugin_instance: PluginBase, context: PluginContext, **kwargs) -> Dict[str, Any]:
        """Execute plugin in a separate process."""
        
        def target_function(result_queue, error_queue):
            try:
                # Apply resource limits in the child process
                self._apply_process_limits()
                
                # Execute plugin
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(plugin_instance.execute(context, **kwargs))
                result_queue.put(result)
                
            except Exception as e:
                error_queue.put(str(e))
        
        # Create queues for communication
        result_queue = multiprocessing.Queue()
        error_queue = multiprocessing.Queue()
        
        # Start process
        process = multiprocessing.Process(
            target=target_function,
            args=(result_queue, error_queue)
        )
        process.start()
        
        # Wait for completion with timeout
        process.join(timeout=self.resource_limits.max_cpu_time_seconds)
        
        if process.is_alive():
            # Kill process if it's still running
            process.terminate()
            process.join()
            raise TimeoutError("Plugin execution timed out")
        
        # Check for errors
        if not error_queue.empty():
            error = error_queue.get()
            raise Exception(f"Plugin execution error: {error}")
        
        # Get result
        if not result_queue.empty():
            return result_queue.get()
        else:
            raise Exception("No result returned from plugin execution")
    
    @contextmanager
    def _apply_resource_limits(self):
        """Apply resource limits to the current process."""
        
        # Save original limits
        original_limits = {}
        
        try:
            # Set memory limit
            if self.resource_limits.max_memory_mb > 0:
                memory_limit = self.resource_limits.max_memory_mb * 1024 * 1024
                original_limits['memory'] = resource.getrlimit(resource.RLIMIT_AS)
                resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
            
            # Set CPU time limit
            if self.resource_limits.max_cpu_time_seconds > 0:
                original_limits['cpu'] = resource.getrlimit(resource.RLIMIT_CPU)
                resource.setrlimit(resource.RLIMIT_CPU, 
                                 (self.resource_limits.max_cpu_time_seconds,
                                  self.resource_limits.max_cpu_time_seconds))
            
            # Set file descriptor limit
            if self.resource_limits.max_file_descriptors > 0:
                original_limits['nofile'] = resource.getrlimit(resource.RLIMIT_NOFILE)
                resource.setrlimit(resource.RLIMIT_NOFILE,
                                 (self.resource_limits.max_file_descriptors,
                                  self.resource_limits.max_file_descriptors))
            
            # Set file size limit
            if self.resource_limits.max_file_size_mb > 0:
                file_size_limit = self.resource_limits.max_file_size_mb * 1024 * 1024
                original_limits['fsize'] = resource.getrlimit(resource.RLIMIT_FSIZE)
                resource.setrlimit(resource.RLIMIT_FSIZE, (file_size_limit, file_size_limit))
            
            yield
            
        finally:
            # Restore original limits
            try:
                if 'memory' in original_limits:
                    resource.setrlimit(resource.RLIMIT_AS, original_limits['memory'])
                if 'cpu' in original_limits:
                    resource.setrlimit(resource.RLIMIT_CPU, original_limits['cpu'])
                if 'nofile' in original_limits:
                    resource.setrlimit(resource.RLIMIT_NOFILE, original_limits['nofile'])
                if 'fsize' in original_limits:
                    resource.setrlimit(resource.RLIMIT_FSIZE, original_limits['fsize'])
            except Exception as e:
                self.logger.warning(f"Error restoring resource limits: {str(e)}")
    
    def _apply_process_limits(self):
        """Apply resource limits in a child process."""
        
        # Set memory limit
        if self.resource_limits.max_memory_mb > 0:
            memory_limit = self.resource_limits.max_memory_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
        
        # Set CPU time limit
        if self.resource_limits.max_cpu_time_seconds > 0:
            resource.setrlimit(resource.RLIMIT_CPU, 
                             (self.resource_limits.max_cpu_time_seconds,
                              self.resource_limits.max_cpu_time_seconds))
        
        # Set file descriptor limit
        if self.resource_limits.max_file_descriptors > 0:
            resource.setrlimit(resource.RLIMIT_NOFILE,
                             (self.resource_limits.max_file_descriptors,
                              self.resource_limits.max_file_descriptors))
    
    async def _update_resource_usage(self, plugin_name: str):
        """Update resource usage statistics for a plugin."""
        if plugin_name not in self.active_plugins:
            return
        
        try:
            # Get current resource usage
            usage = resource.getrusage(resource.RUSAGE_SELF)
            
            # Update plugin resource usage
            plugin_usage = self.active_plugins[plugin_name]["resource_usage"]
            plugin_usage["memory_usage"] = usage.ru_maxrss  # Peak memory usage
            plugin_usage["cpu_time"] = usage.ru_utime + usage.ru_stime  # Total CPU time
            
        except Exception as e:
            self.logger.warning(f"Error updating resource usage for {plugin_name}: {str(e)}")

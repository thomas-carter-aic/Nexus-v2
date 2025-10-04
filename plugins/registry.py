"""
Plugin registry for managing plugin metadata and discovery.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import logging

from .base import PluginMetadata, PluginType, PluginStatus


class PluginRegistry:
    """Registry for managing plugin metadata and discovery."""
    
    def __init__(self, registry_path: str = "plugins_registry.json"):
        self.registry_path = Path(registry_path)
        self.plugins: Dict[str, Dict[str, Any]] = {}
        self.logger = logging.getLogger(__name__)
        self._lock = asyncio.Lock()
        
    async def initialize(self):
        """Initialize the plugin registry."""
        await self._load_registry()
    
    async def register_plugin(self, metadata: PluginMetadata, plugin_path: str) -> bool:
        """
        Register a plugin in the registry.
        
        Args:
            metadata: Plugin metadata
            plugin_path: Path to the plugin
            
        Returns:
            True if registration successful
        """
        async with self._lock:
            try:
                plugin_info = {
                    "name": metadata.name,
                    "version": metadata.version,
                    "description": metadata.description,
                    "author": metadata.author,
                    "plugin_type": metadata.plugin_type.value,
                    "dependencies": metadata.dependencies,
                    "permissions": metadata.permissions,
                    "config_schema": metadata.config_schema,
                    "min_platform_version": metadata.min_platform_version,
                    "max_platform_version": metadata.max_platform_version,
                    "tags": metadata.tags,
                    "path": str(plugin_path),
                    "registered_at": datetime.now().isoformat(),
                    "status": PluginStatus.INACTIVE.value,
                    "install_count": 0,
                    "rating": 0.0,
                    "reviews": []
                }
                
                self.plugins[metadata.name] = plugin_info
                await self._save_registry()
                
                self.logger.info(f"Plugin registered: {metadata.name}")
                return True
                
            except Exception as e:
                self.logger.error(f"Error registering plugin {metadata.name}: {str(e)}")
                return False
    
    async def unregister_plugin(self, plugin_name: str) -> bool:
        """
        Unregister a plugin from the registry.
        
        Args:
            plugin_name: Name of the plugin to unregister
            
        Returns:
            True if unregistration successful
        """
        async with self._lock:
            try:
                if plugin_name in self.plugins:
                    del self.plugins[plugin_name]
                    await self._save_registry()
                    self.logger.info(f"Plugin unregistered: {plugin_name}")
                
                return True
                
            except Exception as e:
                self.logger.error(f"Error unregistering plugin {plugin_name}: {str(e)}")
                return False
    
    async def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """
        Get plugin information.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Plugin information or None if not found
        """
        return self.plugins.get(plugin_name)
    
    async def list_plugins(self, plugin_type: Optional[PluginType] = None, 
                          status: Optional[PluginStatus] = None,
                          tags: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        List plugins with optional filtering.
        
        Args:
            plugin_type: Filter by plugin type
            status: Filter by plugin status
            tags: Filter by tags
            
        Returns:
            List of plugin information
        """
        plugins = list(self.plugins.values())
        
        # Filter by type
        if plugin_type:
            plugins = [p for p in plugins if p["plugin_type"] == plugin_type.value]
        
        # Filter by status
        if status:
            plugins = [p for p in plugins if p["status"] == status.value]
        
        # Filter by tags
        if tags:
            plugins = [p for p in plugins if any(tag in p.get("tags", []) for tag in tags)]
        
        return plugins
    
    async def get_plugins_by_type(self, plugin_type: PluginType) -> List[str]:
        """
        Get plugin names by type.
        
        Args:
            plugin_type: Plugin type to filter by
            
        Returns:
            List of plugin names
        """
        return [
            name for name, info in self.plugins.items()
            if info["plugin_type"] == plugin_type.value
        ]
    
    async def search_plugins(self, query: str) -> List[Dict[str, Any]]:
        """
        Search plugins by name, description, or tags.
        
        Args:
            query: Search query
            
        Returns:
            List of matching plugins
        """
        query_lower = query.lower()
        matching_plugins = []
        
        for plugin_info in self.plugins.values():
            # Search in name
            if query_lower in plugin_info["name"].lower():
                matching_plugins.append(plugin_info)
                continue
            
            # Search in description
            if query_lower in plugin_info["description"].lower():
                matching_plugins.append(plugin_info)
                continue
            
            # Search in tags
            if any(query_lower in tag.lower() for tag in plugin_info.get("tags", [])):
                matching_plugins.append(plugin_info)
                continue
        
        return matching_plugins
    
    async def update_plugin_status(self, plugin_name: str, status: PluginStatus) -> bool:
        """
        Update plugin status.
        
        Args:
            plugin_name: Name of the plugin
            status: New status
            
        Returns:
            True if update successful
        """
        async with self._lock:
            try:
                if plugin_name in self.plugins:
                    self.plugins[plugin_name]["status"] = status.value
                    await self._save_registry()
                    return True
                return False
                
            except Exception as e:
                self.logger.error(f"Error updating plugin status {plugin_name}: {str(e)}")
                return False
    
    async def increment_install_count(self, plugin_name: str) -> bool:
        """
        Increment plugin install count.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            True if update successful
        """
        async with self._lock:
            try:
                if plugin_name in self.plugins:
                    self.plugins[plugin_name]["install_count"] += 1
                    await self._save_registry()
                    return True
                return False
                
            except Exception as e:
                self.logger.error(f"Error incrementing install count {plugin_name}: {str(e)}")
                return False
    
    async def add_plugin_review(self, plugin_name: str, rating: float, 
                               review: str, reviewer: str) -> bool:
        """
        Add a review for a plugin.
        
        Args:
            plugin_name: Name of the plugin
            rating: Rating (1-5)
            review: Review text
            reviewer: Reviewer identifier
            
        Returns:
            True if review added successfully
        """
        async with self._lock:
            try:
                if plugin_name not in self.plugins:
                    return False
                
                # Validate rating
                if not 1 <= rating <= 5:
                    return False
                
                # Add review
                review_data = {
                    "rating": rating,
                    "review": review,
                    "reviewer": reviewer,
                    "timestamp": datetime.now().isoformat()
                }
                
                self.plugins[plugin_name]["reviews"].append(review_data)
                
                # Update average rating
                reviews = self.plugins[plugin_name]["reviews"]
                avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
                self.plugins[plugin_name]["rating"] = round(avg_rating, 2)
                
                await self._save_registry()
                return True
                
            except Exception as e:
                self.logger.error(f"Error adding review for {plugin_name}: {str(e)}")
                return False
    
    async def get_plugin_dependencies(self, plugin_name: str) -> List[str]:
        """
        Get plugin dependencies.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            List of dependencies
        """
        plugin_info = await self.get_plugin_info(plugin_name)
        if plugin_info:
            return plugin_info.get("dependencies", [])
        return []
    
    async def validate_plugin_compatibility(self, plugin_name: str, 
                                          platform_version: str) -> bool:
        """
        Validate plugin compatibility with platform version.
        
        Args:
            plugin_name: Name of the plugin
            platform_version: Platform version to check against
            
        Returns:
            True if compatible
        """
        plugin_info = await self.get_plugin_info(plugin_name)
        if not plugin_info:
            return False
        
        min_version = plugin_info.get("min_platform_version")
        max_version = plugin_info.get("max_platform_version")
        
        # Simple version comparison (assumes semantic versioning)
        if min_version and self._compare_versions(platform_version, min_version) < 0:
            return False
        
        if max_version and self._compare_versions(platform_version, max_version) > 0:
            return False
        
        return True
    
    async def get_popular_plugins(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get most popular plugins by install count.
        
        Args:
            limit: Maximum number of plugins to return
            
        Returns:
            List of popular plugins
        """
        plugins = list(self.plugins.values())
        plugins.sort(key=lambda p: p.get("install_count", 0), reverse=True)
        return plugins[:limit]
    
    async def get_top_rated_plugins(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top-rated plugins.
        
        Args:
            limit: Maximum number of plugins to return
            
        Returns:
            List of top-rated plugins
        """
        plugins = list(self.plugins.values())
        # Filter plugins with at least one review
        plugins = [p for p in plugins if p.get("rating", 0) > 0]
        plugins.sort(key=lambda p: p.get("rating", 0), reverse=True)
        return plugins[:limit]
    
    async def _load_registry(self):
        """Load registry from file."""
        try:
            if self.registry_path.exists():
                with open(self.registry_path, 'r') as f:
                    self.plugins = json.load(f)
                self.logger.info(f"Loaded {len(self.plugins)} plugins from registry")
            else:
                self.plugins = {}
                self.logger.info("Created new plugin registry")
                
        except Exception as e:
            self.logger.error(f"Error loading plugin registry: {str(e)}")
            self.plugins = {}
    
    async def _save_registry(self):
        """Save registry to file."""
        try:
            with open(self.registry_path, 'w') as f:
                json.dump(self.plugins, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving plugin registry: {str(e)}")
    
    def _compare_versions(self, version1: str, version2: str) -> int:
        """
        Compare two version strings.
        
        Returns:
            -1 if version1 < version2
             0 if version1 == version2
             1 if version1 > version2
        """
        def version_tuple(v):
            return tuple(map(int, (v.split("."))))
        
        v1_tuple = version_tuple(version1)
        v2_tuple = version_tuple(version2)
        
        if v1_tuple < v2_tuple:
            return -1
        elif v1_tuple > v2_tuple:
            return 1
        else:
            return 0

"""
Advanced Metrics Collection System

This module provides comprehensive metrics collection capabilities for the AI-Native PaaS Platform,
including real-time data aggregation, custom metrics, and intelligent data processing.
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from uuid import UUID, uuid4
import logging

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of metrics that can be collected"""
    PERFORMANCE = "performance"
    RESOURCE_USAGE = "resource_usage"
    APPLICATION = "application"
    INFRASTRUCTURE = "infrastructure"
    BUSINESS = "business"
    SECURITY = "security"
    COST = "cost"
    USER_BEHAVIOR = "user_behavior"
    AI_MODEL = "ai_model"
    DEPLOYMENT = "deployment"


class MetricUnit(Enum):
    """Units for metric measurements"""
    COUNT = "count"
    PERCENTAGE = "percentage"
    BYTES = "bytes"
    SECONDS = "seconds"
    MILLISECONDS = "milliseconds"
    REQUESTS_PER_SECOND = "requests_per_second"
    CPU_CORES = "cpu_cores"
    MEMORY_MB = "memory_mb"
    STORAGE_GB = "storage_gb"
    DOLLARS = "dollars"
    SCORE = "score"


@dataclass
class MetricData:
    """Represents a single metric data point"""
    metric_id: str
    metric_type: MetricType
    name: str
    value: Union[int, float]
    unit: MetricUnit
    timestamp: datetime = field(default_factory=datetime.utcnow)
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    source: str = "platform"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metric data to dictionary for serialization"""
        return {
            'metric_id': self.metric_id,
            'metric_type': self.metric_type.value,
            'name': self.name,
            'value': self.value,
            'unit': self.unit.value,
            'timestamp': self.timestamp.isoformat(),
            'tags': self.tags,
            'metadata': self.metadata,
            'source': self.source
        }


@dataclass
class MetricAggregation:
    """Aggregated metric data over a time period"""
    metric_name: str
    metric_type: MetricType
    start_time: datetime
    end_time: datetime
    count: int
    sum_value: float
    avg_value: float
    min_value: float
    max_value: float
    percentiles: Dict[str, float] = field(default_factory=dict)
    tags: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """
    Advanced metrics collection system with real-time aggregation and intelligent processing
    """
    
    def __init__(self, buffer_size: int = 10000, flush_interval: int = 60):
        self.buffer_size = buffer_size
        self.flush_interval = flush_interval
        self.metrics_buffer: List[MetricData] = []
        self.aggregations: Dict[str, List[MetricData]] = {}
        self.custom_collectors: Dict[str, callable] = {}
        self.running = False
        self._flush_task: Optional[asyncio.Task] = None
        
    async def start(self):
        """Start the metrics collection system"""
        if self.running:
            return
            
        self.running = True
        self._flush_task = asyncio.create_task(self._periodic_flush())
        logger.info("Metrics collector started")
        
    async def stop(self):
        """Stop the metrics collection system"""
        if not self.running:
            return
            
        self.running = False
        if self._flush_task:
            self._flush_task.cancel()
            try:
                await self._flush_task
            except asyncio.CancelledError:
                pass
                
        # Flush remaining metrics
        await self._flush_metrics()
        logger.info("Metrics collector stopped")
        
    async def collect_metric(self, metric: MetricData):
        """Collect a single metric data point"""
        if not self.running:
            await self.start()
            
        self.metrics_buffer.append(metric)
        
        # Add to aggregation buckets
        bucket_key = f"{metric.metric_type.value}:{metric.name}"
        if bucket_key not in self.aggregations:
            self.aggregations[bucket_key] = []
        self.aggregations[bucket_key].append(metric)
        
        # Flush if buffer is full
        if len(self.metrics_buffer) >= self.buffer_size:
            await self._flush_metrics()
            
    async def collect_performance_metric(self, name: str, value: float, unit: MetricUnit, 
                                       tags: Optional[Dict[str, str]] = None):
        """Collect a performance metric"""
        metric = MetricData(
            metric_id=str(uuid4()),
            metric_type=MetricType.PERFORMANCE,
            name=name,
            value=value,
            unit=unit,
            tags=tags or {}
        )
        await self.collect_metric(metric)
        
    async def collect_resource_usage(self, resource_type: str, usage_value: float, 
                                   capacity: float, tags: Optional[Dict[str, str]] = None):
        """Collect resource usage metrics"""
        usage_percentage = (usage_value / capacity) * 100 if capacity > 0 else 0
        
        # Collect absolute usage
        await self.collect_metric(MetricData(
            metric_id=str(uuid4()),
            metric_type=MetricType.RESOURCE_USAGE,
            name=f"{resource_type}_usage",
            value=usage_value,
            unit=MetricUnit.COUNT,
            tags=tags or {}
        ))
        
        # Collect usage percentage
        await self.collect_metric(MetricData(
            metric_id=str(uuid4()),
            metric_type=MetricType.RESOURCE_USAGE,
            name=f"{resource_type}_usage_percentage",
            value=usage_percentage,
            unit=MetricUnit.PERCENTAGE,
            tags=tags or {}
        ))
        
    async def collect_application_metric(self, app_id: str, metric_name: str, 
                                       value: float, unit: MetricUnit):
        """Collect application-specific metrics"""
        metric = MetricData(
            metric_id=str(uuid4()),
            metric_type=MetricType.APPLICATION,
            name=metric_name,
            value=value,
            unit=unit,
            tags={'application_id': app_id}
        )
        await self.collect_metric(metric)
        
    async def collect_business_metric(self, metric_name: str, value: float, 
                                    unit: MetricUnit, customer_id: Optional[str] = None):
        """Collect business metrics"""
        tags = {}
        if customer_id:
            tags['customer_id'] = customer_id
            
        metric = MetricData(
            metric_id=str(uuid4()),
            metric_type=MetricType.BUSINESS,
            name=metric_name,
            value=value,
            unit=unit,
            tags=tags
        )
        await self.collect_metric(metric)
        
    async def collect_cost_metric(self, service: str, cost: float, 
                                tags: Optional[Dict[str, str]] = None):
        """Collect cost metrics"""
        metric = MetricData(
            metric_id=str(uuid4()),
            metric_type=MetricType.COST,
            name=f"{service}_cost",
            value=cost,
            unit=MetricUnit.DOLLARS,
            tags=tags or {}
        )
        await self.collect_metric(metric)
        
    async def collect_ai_model_metric(self, model_name: str, metric_name: str, 
                                    value: float, unit: MetricUnit):
        """Collect AI model performance metrics"""
        metric = MetricData(
            metric_id=str(uuid4()),
            metric_type=MetricType.AI_MODEL,
            name=metric_name,
            value=value,
            unit=unit,
            tags={'model_name': model_name}
        )
        await self.collect_metric(metric)
        
    def register_custom_collector(self, name: str, collector_func: callable):
        """Register a custom metric collector function"""
        self.custom_collectors[name] = collector_func
        logger.info(f"Registered custom collector: {name}")
        
    async def run_custom_collectors(self):
        """Execute all registered custom collectors"""
        for name, collector_func in self.custom_collectors.items():
            try:
                if asyncio.iscoroutinefunction(collector_func):
                    await collector_func(self)
                else:
                    collector_func(self)
            except Exception as e:
                logger.error(f"Error running custom collector {name}: {e}")
                
    async def get_aggregated_metrics(self, metric_type: Optional[MetricType] = None,
                                   start_time: Optional[datetime] = None,
                                   end_time: Optional[datetime] = None) -> List[MetricAggregation]:
        """Get aggregated metrics for a time period"""
        aggregations = []
        
        for bucket_key, metrics in self.aggregations.items():
            if not metrics:
                continue
                
            # Filter by metric type
            if metric_type:
                bucket_type = MetricType(bucket_key.split(':')[0])
                if bucket_type != metric_type:
                    continue
                    
            # Filter by time range
            filtered_metrics = metrics
            if start_time or end_time:
                filtered_metrics = [
                    m for m in metrics
                    if (not start_time or m.timestamp >= start_time) and
                       (not end_time or m.timestamp <= end_time)
                ]
                
            if not filtered_metrics:
                continue
                
            # Calculate aggregations
            values = [m.value for m in filtered_metrics]
            aggregation = MetricAggregation(
                metric_name=filtered_metrics[0].name,
                metric_type=filtered_metrics[0].metric_type,
                start_time=min(m.timestamp for m in filtered_metrics),
                end_time=max(m.timestamp for m in filtered_metrics),
                count=len(values),
                sum_value=sum(values),
                avg_value=sum(values) / len(values),
                min_value=min(values),
                max_value=max(values),
                percentiles=self._calculate_percentiles(values)
            )
            aggregations.append(aggregation)
            
        return aggregations
        
    def _calculate_percentiles(self, values: List[float]) -> Dict[str, float]:
        """Calculate percentile values"""
        if not values:
            return {}
            
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        percentiles = {}
        for p in [50, 75, 90, 95, 99]:
            index = int((p / 100) * (n - 1))
            percentiles[f"p{p}"] = sorted_values[index]
            
        return percentiles
        
    async def _periodic_flush(self):
        """Periodically flush metrics to storage"""
        while self.running:
            try:
                await asyncio.sleep(self.flush_interval)
                await self._flush_metrics()
                await self.run_custom_collectors()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in periodic flush: {e}")
                
    async def _flush_metrics(self):
        """Flush metrics buffer to storage"""
        if not self.metrics_buffer:
            return
            
        try:
            # In a real implementation, this would write to a time-series database
            # For now, we'll log the metrics
            logger.info(f"Flushing {len(self.metrics_buffer)} metrics to storage")
            
            # Simulate storage operation
            await asyncio.sleep(0.1)
            
            # Clear buffer
            self.metrics_buffer.clear()
            
            # Clean old aggregation data (keep last hour)
            cutoff_time = datetime.utcnow() - timedelta(hours=1)
            for bucket_key in list(self.aggregations.keys()):
                self.aggregations[bucket_key] = [
                    m for m in self.aggregations[bucket_key]
                    if m.timestamp > cutoff_time
                ]
                
        except Exception as e:
            logger.error(f"Error flushing metrics: {e}")


class SystemMetricsCollector:
    """Collects system-level metrics automatically"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        
    async def collect_system_metrics(self):
        """Collect various system metrics"""
        try:
            # CPU usage (simulated)
            cpu_usage = await self._get_cpu_usage()
            await self.metrics_collector.collect_resource_usage(
                "cpu", cpu_usage, 100.0, {"host": "platform-host"}
            )
            
            # Memory usage (simulated)
            memory_usage, memory_total = await self._get_memory_usage()
            await self.metrics_collector.collect_resource_usage(
                "memory", memory_usage, memory_total, {"host": "platform-host"}
            )
            
            # Disk usage (simulated)
            disk_usage, disk_total = await self._get_disk_usage()
            await self.metrics_collector.collect_resource_usage(
                "disk", disk_usage, disk_total, {"host": "platform-host"}
            )
            
            # Network metrics (simulated)
            network_in, network_out = await self._get_network_metrics()
            await self.metrics_collector.collect_performance_metric(
                "network_bytes_in", network_in, MetricUnit.BYTES
            )
            await self.metrics_collector.collect_performance_metric(
                "network_bytes_out", network_out, MetricUnit.BYTES
            )
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            
    async def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage"""
        # Simulate CPU usage between 10-80%
        import random
        return random.uniform(10.0, 80.0)
        
    async def _get_memory_usage(self) -> tuple[float, float]:
        """Get current memory usage in MB"""
        # Simulate memory usage
        import random
        total_memory = 16384.0  # 16GB
        used_memory = random.uniform(4096.0, 12288.0)  # 4-12GB
        return used_memory, total_memory
        
    async def _get_disk_usage(self) -> tuple[float, float]:
        """Get current disk usage in GB"""
        # Simulate disk usage
        import random
        total_disk = 1000.0  # 1TB
        used_disk = random.uniform(100.0, 800.0)  # 100GB-800GB
        return used_disk, total_disk
        
    async def _get_network_metrics(self) -> tuple[float, float]:
        """Get network I/O metrics in bytes"""
        # Simulate network traffic
        import random
        bytes_in = random.uniform(1000000, 10000000)  # 1-10MB
        bytes_out = random.uniform(500000, 5000000)   # 0.5-5MB
        return bytes_in, bytes_out


# Example usage and testing
async def example_usage():
    """Example of how to use the metrics collector"""
    
    # Create metrics collector
    collector = MetricsCollector(buffer_size=1000, flush_interval=30)
    
    # Start collection
    await collector.start()
    
    # Collect various metrics
    await collector.collect_performance_metric(
        "response_time", 150.5, MetricUnit.MILLISECONDS,
        {"endpoint": "/api/applications", "method": "GET"}
    )
    
    await collector.collect_application_metric(
        "app-123", "request_count", 1500, MetricUnit.COUNT
    )
    
    await collector.collect_business_metric(
        "active_users", 250, MetricUnit.COUNT, "customer-456"
    )
    
    await collector.collect_cost_metric(
        "ec2", 125.50, {"region": "us-east-1", "instance_type": "t3.medium"}
    )
    
    # Set up system metrics collection
    system_collector = SystemMetricsCollector(collector)
    collector.register_custom_collector(
        "system_metrics", system_collector.collect_system_metrics
    )
    
    # Let it run for a bit
    await asyncio.sleep(5)
    
    # Get aggregated metrics
    aggregations = await collector.get_aggregated_metrics(
        metric_type=MetricType.PERFORMANCE
    )
    
    for agg in aggregations:
        print(f"Metric: {agg.metric_name}")
        print(f"  Count: {agg.count}")
        print(f"  Average: {agg.avg_value}")
        print(f"  Min/Max: {agg.min_value}/{agg.max_value}")
        print(f"  P95: {agg.percentiles.get('p95', 'N/A')}")
        print()
    
    # Stop collection
    await collector.stop()


if __name__ == "__main__":
    asyncio.run(example_usage())

"""
Dashboard Service Module

This module provides interactive dashboard creation and management capabilities
for the AI-Native PaaS Platform analytics system.
"""

import asyncio
import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from uuid import UUID, uuid4
import logging

logger = logging.getLogger(__name__)


class WidgetType(Enum):
    """Types of dashboard widgets"""
    METRIC_CARD = "metric_card"
    LINE_CHART = "line_chart"
    BAR_CHART = "bar_chart"
    PIE_CHART = "pie_chart"
    GAUGE = "gauge"
    TABLE = "table"
    HEATMAP = "heatmap"
    SCATTER_PLOT = "scatter_plot"
    HISTOGRAM = "histogram"
    ALERT_LIST = "alert_list"
    LOG_VIEWER = "log_viewer"
    STATUS_INDICATOR = "status_indicator"


class DashboardType(Enum):
    """Types of dashboards"""
    EXECUTIVE = "executive"
    OPERATIONAL = "operational"
    TECHNICAL = "technical"
    BUSINESS = "business"
    SECURITY = "security"
    CUSTOM = "custom"


class RefreshInterval(Enum):
    """Dashboard refresh intervals"""
    REAL_TIME = "real_time"      # 5 seconds
    FAST = "fast"                # 30 seconds
    NORMAL = "normal"            # 5 minutes
    SLOW = "slow"                # 30 minutes
    MANUAL = "manual"            # No auto-refresh


@dataclass
class Widget:
    """Dashboard widget configuration"""
    widget_id: str
    widget_type: WidgetType
    title: str
    description: str
    position: Dict[str, int]  # x, y, width, height
    data_source: str
    query: Dict[str, Any]
    config: Dict[str, Any] = field(default_factory=dict)
    refresh_interval: RefreshInterval = RefreshInterval.NORMAL
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'widget_id': self.widget_id,
            'widget_type': self.widget_type.value,
            'title': self.title,
            'description': self.description,
            'position': self.position,
            'data_source': self.data_source,
            'query': self.query,
            'config': self.config,
            'refresh_interval': self.refresh_interval.value
        }


@dataclass
class Dashboard:
    """Dashboard configuration"""
    dashboard_id: str
    name: str
    description: str
    dashboard_type: DashboardType
    widgets: List[Widget] = field(default_factory=list)
    layout: Dict[str, Any] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = "system"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'dashboard_id': self.dashboard_id,
            'name': self.name,
            'description': self.description,
            'dashboard_type': self.dashboard_type.value,
            'widgets': [w.to_dict() for w in self.widgets],
            'layout': self.layout,
            'permissions': self.permissions,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'created_by': self.created_by
        }


@dataclass
class DashboardTemplate:
    """Pre-built dashboard template"""
    template_id: str
    name: str
    description: str
    dashboard_type: DashboardType
    widget_configs: List[Dict[str, Any]]
    default_layout: Dict[str, Any]


class DashboardService:
    """
    Interactive dashboard service for analytics visualization
    """
    
    def __init__(self):
        self.dashboards: Dict[str, Dashboard] = {}
        self.templates: Dict[str, DashboardTemplate] = {}
        self.widget_data_cache: Dict[str, Any] = {}
        self._initialize_templates()
        
    def _initialize_templates(self):
        """Initialize pre-built dashboard templates"""
        
        # Executive Dashboard Template
        exec_template = DashboardTemplate(
            template_id="executive_template",
            name="Executive Dashboard",
            description="High-level business metrics and KPIs",
            dashboard_type=DashboardType.EXECUTIVE,
            widget_configs=[
                {
                    'widget_type': 'metric_card',
                    'title': 'Total Revenue',
                    'data_source': 'business_metrics',
                    'query': {'metric': 'total_revenue', 'period': '30d'},
                    'position': {'x': 0, 'y': 0, 'width': 3, 'height': 2}
                },
                {
                    'widget_type': 'metric_card',
                    'title': 'Active Users',
                    'data_source': 'user_metrics',
                    'query': {'metric': 'active_users', 'period': '24h'},
                    'position': {'x': 3, 'y': 0, 'width': 3, 'height': 2}
                },
                {
                    'widget_type': 'line_chart',
                    'title': 'Revenue Trend',
                    'data_source': 'business_metrics',
                    'query': {'metric': 'daily_revenue', 'period': '30d'},
                    'position': {'x': 0, 'y': 2, 'width': 6, 'height': 4}
                }
            ],
            default_layout={'columns': 12, 'rows': 8}
        )
        self.templates[exec_template.template_id] = exec_template
        
        # Operational Dashboard Template
        ops_template = DashboardTemplate(
            template_id="operational_template",
            name="Operational Dashboard",
            description="System performance and operational metrics",
            dashboard_type=DashboardType.OPERATIONAL,
            widget_configs=[
                {
                    'widget_type': 'gauge',
                    'title': 'CPU Usage',
                    'data_source': 'system_metrics',
                    'query': {'metric': 'cpu_usage_percentage'},
                    'position': {'x': 0, 'y': 0, 'width': 3, 'height': 3}
                },
                {
                    'widget_type': 'gauge',
                    'title': 'Memory Usage',
                    'data_source': 'system_metrics',
                    'query': {'metric': 'memory_usage_percentage'},
                    'position': {'x': 3, 'y': 0, 'width': 3, 'height': 3}
                },
                {
                    'widget_type': 'line_chart',
                    'title': 'Response Time',
                    'data_source': 'performance_metrics',
                    'query': {'metric': 'api_response_time', 'period': '24h'},
                    'position': {'x': 0, 'y': 3, 'width': 6, 'height': 3}
                }
            ],
            default_layout={'columns': 12, 'rows': 8}
        )
        self.templates[ops_template.template_id] = ops_template
        
    async def create_dashboard(self, name: str, description: str,
                             dashboard_type: DashboardType,
                             template_id: Optional[str] = None,
                             created_by: str = "system") -> Dashboard:
        """Create a new dashboard"""
        
        dashboard_id = str(uuid4())
        
        if template_id and template_id in self.templates:
            # Create from template
            template = self.templates[template_id]
            widgets = []
            
            for widget_config in template.widget_configs:
                widget = Widget(
                    widget_id=str(uuid4()),
                    widget_type=WidgetType(widget_config['widget_type']),
                    title=widget_config['title'],
                    description=widget_config.get('description', ''),
                    position=widget_config['position'],
                    data_source=widget_config['data_source'],
                    query=widget_config['query'],
                    config=widget_config.get('config', {})
                )
                widgets.append(widget)
                
            dashboard = Dashboard(
                dashboard_id=dashboard_id,
                name=name,
                description=description,
                dashboard_type=dashboard_type,
                widgets=widgets,
                layout=template.default_layout,
                created_by=created_by
            )
        else:
            # Create empty dashboard
            dashboard = Dashboard(
                dashboard_id=dashboard_id,
                name=name,
                description=description,
                dashboard_type=dashboard_type,
                created_by=created_by
            )
            
        self.dashboards[dashboard_id] = dashboard
        logger.info(f"Created dashboard: {name} ({dashboard_id})")
        
        return dashboard
        
    async def add_widget(self, dashboard_id: str, widget: Widget) -> bool:
        """Add a widget to a dashboard"""
        
        if dashboard_id not in self.dashboards:
            return False
            
        dashboard = self.dashboards[dashboard_id]
        dashboard.widgets.append(widget)
        dashboard.updated_at = datetime.utcnow()
        
        logger.info(f"Added widget {widget.title} to dashboard {dashboard.name}")
        return True
        
    async def remove_widget(self, dashboard_id: str, widget_id: str) -> bool:
        """Remove a widget from a dashboard"""
        
        if dashboard_id not in self.dashboards:
            return False
            
        dashboard = self.dashboards[dashboard_id]
        dashboard.widgets = [w for w in dashboard.widgets if w.widget_id != widget_id]
        dashboard.updated_at = datetime.utcnow()
        
        return True
        
    async def update_widget(self, dashboard_id: str, widget_id: str,
                          updates: Dict[str, Any]) -> bool:
        """Update a widget configuration"""
        
        if dashboard_id not in self.dashboards:
            return False
            
        dashboard = self.dashboards[dashboard_id]
        
        for widget in dashboard.widgets:
            if widget.widget_id == widget_id:
                for key, value in updates.items():
                    if hasattr(widget, key):
                        setattr(widget, key, value)
                        
                dashboard.updated_at = datetime.utcnow()
                return True
                
        return False
        
    async def get_dashboard(self, dashboard_id: str) -> Optional[Dashboard]:
        """Get a dashboard by ID"""
        return self.dashboards.get(dashboard_id)
        
    async def list_dashboards(self, dashboard_type: Optional[DashboardType] = None,
                            created_by: Optional[str] = None) -> List[Dashboard]:
        """List dashboards with optional filtering"""
        
        dashboards = list(self.dashboards.values())
        
        if dashboard_type:
            dashboards = [d for d in dashboards if d.dashboard_type == dashboard_type]
            
        if created_by:
            dashboards = [d for d in dashboards if d.created_by == created_by]
            
        # Sort by creation date (newest first)
        dashboards.sort(key=lambda x: x.created_at, reverse=True)
        
        return dashboards
        
    async def get_widget_data(self, widget: Widget) -> Dict[str, Any]:
        """Get data for a specific widget"""
        
        # Check cache first
        cache_key = f"{widget.widget_id}_{widget.data_source}_{hash(str(widget.query))}"
        
        if cache_key in self.widget_data_cache:
            cached_data = self.widget_data_cache[cache_key]
            # Check if cache is still valid (5 minutes)
            if datetime.utcnow() - cached_data['timestamp'] < timedelta(minutes=5):
                return cached_data['data']
                
        # Generate mock data based on widget type and data source
        data = await self._generate_widget_data(widget)
        
        # Cache the data
        self.widget_data_cache[cache_key] = {
            'data': data,
            'timestamp': datetime.utcnow()
        }
        
        return data
        
    async def _generate_widget_data(self, widget: Widget) -> Dict[str, Any]:
        """Generate mock data for widgets"""
        
        if widget.widget_type == WidgetType.METRIC_CARD:
            return await self._generate_metric_card_data(widget)
        elif widget.widget_type == WidgetType.LINE_CHART:
            return await self._generate_line_chart_data(widget)
        elif widget.widget_type == WidgetType.BAR_CHART:
            return await self._generate_bar_chart_data(widget)
        elif widget.widget_type == WidgetType.PIE_CHART:
            return await self._generate_pie_chart_data(widget)
        elif widget.widget_type == WidgetType.GAUGE:
            return await self._generate_gauge_data(widget)
        elif widget.widget_type == WidgetType.TABLE:
            return await self._generate_table_data(widget)
        else:
            return {'error': f'Unsupported widget type: {widget.widget_type.value}'}
            
    async def _generate_metric_card_data(self, widget: Widget) -> Dict[str, Any]:
        """Generate data for metric card widgets"""
        
        metric = widget.query.get('metric', 'unknown')
        
        # Mock data based on metric type
        if 'revenue' in metric:
            value = 125000.50
            change = 15.3
            trend = 'up'
        elif 'users' in metric:
            value = 8547
            change = 8.7
            trend = 'up'
        elif 'cpu' in metric:
            value = 68.5
            change = -2.1
            trend = 'down'
        elif 'memory' in metric:
            value = 72.3
            change = 1.8
            trend = 'up'
        else:
            value = 42.0
            change = 0.0
            trend = 'stable'
            
        return {
            'value': value,
            'change': change,
            'trend': trend,
            'unit': widget.config.get('unit', ''),
            'timestamp': datetime.utcnow().isoformat()
        }
        
    async def _generate_line_chart_data(self, widget: Widget) -> Dict[str, Any]:
        """Generate data for line chart widgets"""
        
        # Generate time series data
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)
        
        timestamps = []
        values = []
        
        for i in range(24):
            timestamp = start_time + timedelta(hours=i)
            timestamps.append(timestamp.isoformat())
            
            # Generate mock values with some trend and noise
            base_value = 100
            trend = i * 2
            noise = (i % 3 - 1) * 10
            values.append(max(0, base_value + trend + noise))
            
        return {
            'labels': timestamps,
            'datasets': [{
                'label': widget.title,
                'data': values,
                'borderColor': '#007bff',
                'backgroundColor': 'rgba(0, 123, 255, 0.1)'
            }]
        }
        
    async def _generate_bar_chart_data(self, widget: Widget) -> Dict[str, Any]:
        """Generate data for bar chart widgets"""
        
        categories = ['Service A', 'Service B', 'Service C', 'Service D', 'Service E']
        values = [45, 67, 23, 89, 34]
        
        return {
            'labels': categories,
            'datasets': [{
                'label': widget.title,
                'data': values,
                'backgroundColor': [
                    '#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d'
                ]
            }]
        }
        
    async def _generate_pie_chart_data(self, widget: Widget) -> Dict[str, Any]:
        """Generate data for pie chart widgets"""
        
        labels = ['Compute', 'Storage', 'Network', 'Database', 'Other']
        values = [35, 25, 15, 20, 5]
        
        return {
            'labels': labels,
            'datasets': [{
                'data': values,
                'backgroundColor': [
                    '#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d'
                ]
            }]
        }
        
    async def _generate_gauge_data(self, widget: Widget) -> Dict[str, Any]:
        """Generate data for gauge widgets"""
        
        metric = widget.query.get('metric', 'unknown')
        
        if 'cpu' in metric:
            value = 68.5
            max_value = 100
            thresholds = [50, 80, 95]
        elif 'memory' in metric:
            value = 72.3
            max_value = 100
            thresholds = [60, 85, 95]
        else:
            value = 42.0
            max_value = 100
            thresholds = [50, 75, 90]
            
        return {
            'value': value,
            'max_value': max_value,
            'thresholds': thresholds,
            'unit': widget.config.get('unit', '%')
        }
        
    async def _generate_table_data(self, widget: Widget) -> Dict[str, Any]:
        """Generate data for table widgets"""
        
        headers = ['Application', 'Status', 'CPU %', 'Memory %', 'Requests/min']
        rows = [
            ['app-frontend', 'Running', '45.2', '67.8', '1,250'],
            ['app-backend', 'Running', '72.1', '58.3', '2,100'],
            ['app-worker', 'Running', '23.5', '34.7', '450'],
            ['app-cache', 'Running', '12.8', '89.2', '3,200'],
            ['app-db', 'Running', '56.9', '78.4', '850']
        ]
        
        return {
            'headers': headers,
            'rows': rows,
            'total_rows': len(rows)
        }
        
    async def get_dashboard_data(self, dashboard_id: str) -> Dict[str, Any]:
        """Get complete data for a dashboard"""
        
        dashboard = await self.get_dashboard(dashboard_id)
        if not dashboard:
            return {'error': 'Dashboard not found'}
            
        dashboard_data = dashboard.to_dict()
        
        # Get data for each widget
        widget_data = {}
        for widget in dashboard.widgets:
            widget_data[widget.widget_id] = await self.get_widget_data(widget)
            
        dashboard_data['widget_data'] = widget_data
        dashboard_data['last_updated'] = datetime.utcnow().isoformat()
        
        return dashboard_data
        
    async def export_dashboard(self, dashboard_id: str) -> Dict[str, Any]:
        """Export dashboard configuration"""
        
        dashboard = await self.get_dashboard(dashboard_id)
        if not dashboard:
            return {'error': 'Dashboard not found'}
            
        return {
            'dashboard': dashboard.to_dict(),
            'export_timestamp': datetime.utcnow().isoformat(),
            'version': '1.0'
        }
        
    async def import_dashboard(self, dashboard_config: Dict[str, Any],
                             created_by: str = "system") -> str:
        """Import dashboard from configuration"""
        
        dashboard_data = dashboard_config.get('dashboard', {})
        
        # Create new dashboard ID
        new_dashboard_id = str(uuid4())
        
        # Recreate widgets with new IDs
        widgets = []
        for widget_data in dashboard_data.get('widgets', []):
            widget = Widget(
                widget_id=str(uuid4()),
                widget_type=WidgetType(widget_data['widget_type']),
                title=widget_data['title'],
                description=widget_data['description'],
                position=widget_data['position'],
                data_source=widget_data['data_source'],
                query=widget_data['query'],
                config=widget_data.get('config', {}),
                refresh_interval=RefreshInterval(widget_data.get('refresh_interval', 'normal'))
            )
            widgets.append(widget)
            
        # Create dashboard
        dashboard = Dashboard(
            dashboard_id=new_dashboard_id,
            name=dashboard_data['name'] + ' (Imported)',
            description=dashboard_data['description'],
            dashboard_type=DashboardType(dashboard_data['dashboard_type']),
            widgets=widgets,
            layout=dashboard_data.get('layout', {}),
            created_by=created_by
        )
        
        self.dashboards[new_dashboard_id] = dashboard
        
        return new_dashboard_id


# Example usage
async def example_dashboard_service():
    """Example of using the dashboard service"""
    
    # Create dashboard service
    dashboard_service = DashboardService()
    
    # Create executive dashboard from template
    exec_dashboard = await dashboard_service.create_dashboard(
        name="Executive Overview",
        description="High-level business metrics",
        dashboard_type=DashboardType.EXECUTIVE,
        template_id="executive_template",
        created_by="admin"
    )
    
    print(f"Created dashboard: {exec_dashboard.name}")
    print(f"Widgets: {len(exec_dashboard.widgets)}")
    
    # Add a custom widget
    custom_widget = Widget(
        widget_id=str(uuid4()),
        widget_type=WidgetType.ALERT_LIST,
        title="Recent Alerts",
        description="List of recent system alerts",
        position={'x': 6, 'y': 0, 'width': 6, 'height': 4},
        data_source="alerts",
        query={'severity': 'high', 'limit': 10}
    )
    
    await dashboard_service.add_widget(exec_dashboard.dashboard_id, custom_widget)
    
    # Get dashboard data
    dashboard_data = await dashboard_service.get_dashboard_data(exec_dashboard.dashboard_id)
    print(f"Dashboard data keys: {list(dashboard_data.keys())}")
    
    # List all dashboards
    all_dashboards = await dashboard_service.list_dashboards()
    print(f"Total dashboards: {len(all_dashboards)}")
    
    # Export dashboard
    export_data = await dashboard_service.export_dashboard(exec_dashboard.dashboard_id)
    print(f"Export successful: {'dashboard' in export_data}")


if __name__ == "__main__":
    asyncio.run(example_dashboard_service())

"""
Monitoring Service for AI-Native PaaS Platform.

This module provides comprehensive monitoring and observability with
AI-driven insights, intelligent alerting, and performance analytics.

Features:
- Real-time metrics collection and analysis
- AI-powered anomaly detection integration
- Intelligent alerting with noise reduction
- Performance dashboards with AI insights
- Distributed tracing and logging
- Business intelligence and reporting
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

logger = logging.getLogger(__name__)


class MetricType(str, Enum):
    """Types of metrics collected."""
    SYSTEM = "system"
    APPLICATION = "application"
    BUSINESS = "business"
    CUSTOM = "custom"


class AlertSeverity(str, Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class MetricPoint:
    """Individual metric data point."""
    timestamp: datetime
    metric_name: str
    value: float
    unit: str
    dimensions: Dict[str, str]
    metric_type: MetricType


@dataclass
class Alert:
    """Alert definition and status."""
    alert_id: str
    name: str
    description: str
    severity: AlertSeverity
    metric_name: str
    threshold: float
    comparison: str  # >, <, >=, <=, ==
    duration_minutes: int
    enabled: bool
    ai_enhanced: bool
    notification_channels: List[str]
    created_at: datetime
    last_triggered: Optional[datetime] = None


@dataclass
class Dashboard:
    """Dashboard configuration."""
    dashboard_id: str
    name: str
    description: str
    widgets: List[Dict[str, Any]]
    refresh_interval: int
    ai_insights_enabled: bool
    created_at: datetime
    updated_at: datetime


class MonitoringService:
    """
    Comprehensive monitoring service with AI integration.
    
    Provides real-time monitoring, intelligent alerting, and
    AI-powered insights for the PaaS platform.
    """
    
    def __init__(self, ai_service=None):
        """
        Initialize Monitoring Service.
        
        Args:
            ai_service: AI service for intelligent insights
        """
        self.ai_service = ai_service
        
        # Initialize AWS clients
        try:
            self.cloudwatch_client = boto3.client('cloudwatch')
            self.logs_client = boto3.client('logs')
            self.xray_client = boto3.client('xray')
            
            # Test AWS connectivity
            try:
                self.cloudwatch_client.list_metrics(MaxRecords=1)
                logger.info("Monitoring Service initialized with AWS connectivity")
            except Exception:
                logger.warning("AWS not available - using mock mode")
                self._enable_mock_mode()
                
        except (NoCredentialsError, Exception):
            logger.warning("AWS credentials not configured - using mock mode")
            self._enable_mock_mode()
        
        # Service state
        self.metrics_buffer: Dict[str, List[MetricPoint]] = {}
        self.alerts: Dict[str, Alert] = {}
        self.dashboards: Dict[str, Dashboard] = {}
        self.alert_history: List[Dict[str, Any]] = []
        
        # Configuration
        self.metrics_retention_hours = 24
        self.alert_evaluation_interval = 60  # seconds
        self.ai_insights_enabled = True
        
        # Initialize default alerts and dashboards
        self._initialize_default_alerts()
        self._initialize_default_dashboards()
        
        # Start monitoring tasks
        asyncio.create_task(self._metrics_collection_loop())
        asyncio.create_task(self._alert_evaluation_loop())
        
        logger.info("Monitoring Service initialized")
    
    def _enable_mock_mode(self):
        """Enable mock mode for testing without AWS."""
        self.cloudwatch_client = None
        self.logs_client = None
        self.xray_client = None
    
    def _initialize_default_alerts(self):
        """Initialize default alert configurations."""
        
        # High CPU utilization alert
        cpu_alert = Alert(
            alert_id="high-cpu-utilization",
            name="High CPU Utilization",
            description="CPU utilization is above threshold",
            severity=AlertSeverity.WARNING,
            metric_name="cpu_utilization",
            threshold=80.0,
            comparison=">=",
            duration_minutes=5,
            enabled=True,
            ai_enhanced=True,
            notification_channels=["slack://ops-team"],
            created_at=datetime.utcnow()
        )
        
        # High memory utilization alert
        memory_alert = Alert(
            alert_id="high-memory-utilization",
            name="High Memory Utilization",
            description="Memory utilization is above threshold",
            severity=AlertSeverity.WARNING,
            metric_name="memory_utilization",
            threshold=85.0,
            comparison=">=",
            duration_minutes=5,
            enabled=True,
            ai_enhanced=True,
            notification_channels=["slack://ops-team"],
            created_at=datetime.utcnow()
        )
        
        # High error rate alert
        error_alert = Alert(
            alert_id="high-error-rate",
            name="High Error Rate",
            description="Application error rate is above threshold",
            severity=AlertSeverity.ERROR,
            metric_name="error_rate",
            threshold=5.0,
            comparison=">=",
            duration_minutes=2,
            enabled=True,
            ai_enhanced=True,
            notification_channels=["slack://dev-team", "email://oncall@company.com"],
            created_at=datetime.utcnow()
        )
        
        # Response time alert
        response_time_alert = Alert(
            alert_id="high-response-time",
            name="High Response Time",
            description="Average response time is above threshold",
            severity=AlertSeverity.WARNING,
            metric_name="response_time",
            threshold=500.0,
            comparison=">=",
            duration_minutes=3,
            enabled=True,
            ai_enhanced=True,
            notification_channels=["slack://dev-team"],
            created_at=datetime.utcnow()
        )
        
        self.alerts.update({
            cpu_alert.alert_id: cpu_alert,
            memory_alert.alert_id: memory_alert,
            error_alert.alert_id: error_alert,
            response_time_alert.alert_id: response_time_alert
        })
    
    def _initialize_default_dashboards(self):
        """Initialize default dashboard configurations."""
        
        # System Overview Dashboard
        system_dashboard = Dashboard(
            dashboard_id="system-overview",
            name="System Overview",
            description="High-level system metrics and health",
            widgets=[
                {
                    "type": "metric_chart",
                    "title": "CPU Utilization",
                    "metric": "cpu_utilization",
                    "chart_type": "line",
                    "time_range": "1h"
                },
                {
                    "type": "metric_chart",
                    "title": "Memory Utilization",
                    "metric": "memory_utilization",
                    "chart_type": "line",
                    "time_range": "1h"
                },
                {
                    "type": "metric_chart",
                    "title": "Request Rate",
                    "metric": "request_rate",
                    "chart_type": "area",
                    "time_range": "1h"
                },
                {
                    "type": "ai_insights",
                    "title": "AI Insights",
                    "insight_types": ["anomaly", "prediction", "recommendation"]
                }
            ],
            refresh_interval=30,
            ai_insights_enabled=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Application Performance Dashboard
        app_dashboard = Dashboard(
            dashboard_id="application-performance",
            name="Application Performance",
            description="Application-specific performance metrics",
            widgets=[
                {
                    "type": "metric_chart",
                    "title": "Response Time",
                    "metric": "response_time",
                    "chart_type": "line",
                    "time_range": "4h"
                },
                {
                    "type": "metric_chart",
                    "title": "Error Rate",
                    "metric": "error_rate",
                    "chart_type": "line",
                    "time_range": "4h"
                },
                {
                    "type": "metric_chart",
                    "title": "Throughput",
                    "metric": "throughput",
                    "chart_type": "area",
                    "time_range": "4h"
                },
                {
                    "type": "performance_insights",
                    "title": "Performance Analysis",
                    "ai_powered": True
                }
            ],
            refresh_interval=60,
            ai_insights_enabled=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self.dashboards.update({
            system_dashboard.dashboard_id: system_dashboard,
            app_dashboard.dashboard_id: app_dashboard
        })
    
    async def collect_metric(
        self, 
        metric_name: str,
        value: float,
        unit: str = "Count",
        dimensions: Optional[Dict[str, str]] = None,
        metric_type: MetricType = MetricType.CUSTOM
    ) -> bool:
        """
        Collect a metric data point.
        
        Args:
            metric_name: Name of the metric
            value: Metric value
            unit: Unit of measurement
            dimensions: Metric dimensions/tags
            metric_type: Type of metric
            
        Returns:
            True if successful
        """
        try:
            if dimensions is None:
                dimensions = {}
            
            metric_point = MetricPoint(
                timestamp=datetime.utcnow(),
                metric_name=metric_name,
                value=value,
                unit=unit,
                dimensions=dimensions,
                metric_type=metric_type
            )
            
            # Store in buffer
            if metric_name not in self.metrics_buffer:
                self.metrics_buffer[metric_name] = []
            
            self.metrics_buffer[metric_name].append(metric_point)
            
            # Send to CloudWatch if available
            if self.cloudwatch_client:
                await self._send_to_cloudwatch(metric_point)
            
            # Clean old metrics
            await self._cleanup_old_metrics()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to collect metric: {e}")
            return False
    
    async def _send_to_cloudwatch(self, metric_point: MetricPoint):
        """Send metric to CloudWatch."""
        try:
            dimensions = [
                {'Name': k, 'Value': v} 
                for k, v in metric_point.dimensions.items()
            ]
            
            self.cloudwatch_client.put_metric_data(
                Namespace='AI-Native-PaaS',
                MetricData=[
                    {
                        'MetricName': metric_point.metric_name,
                        'Value': metric_point.value,
                        'Unit': metric_point.unit,
                        'Timestamp': metric_point.timestamp,
                        'Dimensions': dimensions
                    }
                ]
            )
            
        except Exception as e:
            logger.error(f"Failed to send metric to CloudWatch: {e}")
    
    async def _cleanup_old_metrics(self):
        """Clean up old metrics from buffer."""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=self.metrics_retention_hours)
            
            for metric_name in list(self.metrics_buffer.keys()):
                self.metrics_buffer[metric_name] = [
                    point for point in self.metrics_buffer[metric_name]
                    if point.timestamp > cutoff_time
                ]
                
                # Remove empty metric buffers
                if not self.metrics_buffer[metric_name]:
                    del self.metrics_buffer[metric_name]
                    
        except Exception as e:
            logger.error(f"Failed to cleanup old metrics: {e}")
    
    async def _metrics_collection_loop(self):
        """Background task for collecting system metrics."""
        while True:
            try:
                # Collect system metrics
                await self._collect_system_metrics()
                
                # Wait for next collection cycle
                await asyncio.sleep(60)  # Collect every minute
                
            except Exception as e:
                logger.error(f"Metrics collection loop error: {e}")
                await asyncio.sleep(60)
    
    async def _collect_system_metrics(self):
        """Collect system-level metrics."""
        try:
            import random
            
            # Simulate system metrics
            current_time = datetime.utcnow()
            
            # CPU utilization
            cpu_util = 40 + random.uniform(-15, 25)
            await self.collect_metric(
                "cpu_utilization",
                max(0, min(100, cpu_util)),
                "Percent",
                {"source": "system"},
                MetricType.SYSTEM
            )
            
            # Memory utilization
            memory_util = 60 + random.uniform(-20, 20)
            await self.collect_metric(
                "memory_utilization",
                max(0, min(100, memory_util)),
                "Percent",
                {"source": "system"},
                MetricType.SYSTEM
            )
            
            # Request rate
            request_rate = 100 + random.uniform(-30, 50)
            await self.collect_metric(
                "request_rate",
                max(0, request_rate),
                "Count/Second",
                {"source": "application"},
                MetricType.APPLICATION
            )
            
            # Response time
            response_time = 120 + random.uniform(-40, 80)
            await self.collect_metric(
                "response_time",
                max(10, response_time),
                "Milliseconds",
                {"source": "application"},
                MetricType.APPLICATION
            )
            
            # Error rate
            error_rate = 1.0 + random.uniform(-0.8, 2.0)
            await self.collect_metric(
                "error_rate",
                max(0, error_rate),
                "Percent",
                {"source": "application"},
                MetricType.APPLICATION
            )
            
        except Exception as e:
            logger.error(f"System metrics collection failed: {e}")
    
    async def _alert_evaluation_loop(self):
        """Background task for evaluating alerts."""
        while True:
            try:
                # Evaluate all enabled alerts
                for alert in self.alerts.values():
                    if alert.enabled:
                        await self._evaluate_alert(alert)
                
                # Wait for next evaluation cycle
                await asyncio.sleep(self.alert_evaluation_interval)
                
            except Exception as e:
                logger.error(f"Alert evaluation loop error: {e}")
                await asyncio.sleep(self.alert_evaluation_interval)
    
    async def _evaluate_alert(self, alert: Alert):
        """Evaluate individual alert condition."""
        try:
            # Get recent metric values
            if alert.metric_name not in self.metrics_buffer:
                return
            
            recent_metrics = self.metrics_buffer[alert.metric_name]
            if not recent_metrics:
                return
            
            # Get metrics within the alert duration
            duration_cutoff = datetime.utcnow() - timedelta(minutes=alert.duration_minutes)
            relevant_metrics = [
                m for m in recent_metrics
                if m.timestamp > duration_cutoff
            ]
            
            if not relevant_metrics:
                return
            
            # Calculate average value over the duration
            avg_value = sum(m.value for m in relevant_metrics) / len(relevant_metrics)
            
            # Evaluate alert condition
            alert_triggered = False
            
            if alert.comparison == ">=":
                alert_triggered = avg_value >= alert.threshold
            elif alert.comparison == ">":
                alert_triggered = avg_value > alert.threshold
            elif alert.comparison == "<=":
                alert_triggered = avg_value <= alert.threshold
            elif alert.comparison == "<":
                alert_triggered = avg_value < alert.threshold
            elif alert.comparison == "==":
                alert_triggered = abs(avg_value - alert.threshold) < 0.01
            
            # Apply AI enhancement if enabled
            if alert.ai_enhanced and self.ai_service:
                alert_triggered = await self._ai_enhance_alert(alert, avg_value, alert_triggered)
            
            # Trigger alert if condition is met
            if alert_triggered:
                await self._trigger_alert(alert, avg_value)
                
        except Exception as e:
            logger.error(f"Alert evaluation failed for {alert.alert_id}: {e}")
    
    async def _ai_enhance_alert(self, alert: Alert, current_value: float, initial_trigger: bool) -> bool:
        """Apply AI enhancement to alert evaluation."""
        try:
            if not self.ai_service:
                return initial_trigger
            
            # Get AI insights for the metric
            insights = await self.ai_service.get_comprehensive_insights(f"metric-{alert.metric_name}")
            
            # Check for anomaly detection insights
            anomaly_insights = [i for i in insights if i.insight_type.value == 'anomaly_alert']
            
            for insight in anomaly_insights:
                if insight.priority.value in ['critical', 'high']:
                    # AI detected anomaly - enhance alert sensitivity
                    return True
                elif insight.priority.value == 'low' and initial_trigger:
                    # AI suggests this might be normal - reduce false positives
                    if insight.confidence > 0.8:
                        return False
            
            return initial_trigger
            
        except Exception as e:
            logger.error(f"AI alert enhancement failed: {e}")
            return initial_trigger
    
    async def _trigger_alert(self, alert: Alert, current_value: float):
        """Trigger alert and send notifications."""
        try:
            # Check if alert was recently triggered (avoid spam)
            if alert.last_triggered:
                time_since_last = datetime.utcnow() - alert.last_triggered
                if time_since_last < timedelta(minutes=5):  # 5-minute cooldown
                    return
            
            # Update alert status
            alert.last_triggered = datetime.utcnow()
            
            # Create alert event
            alert_event = {
                "alert_id": alert.alert_id,
                "name": alert.name,
                "description": alert.description,
                "severity": alert.severity.value,
                "metric_name": alert.metric_name,
                "current_value": current_value,
                "threshold": alert.threshold,
                "triggered_at": alert.last_triggered.isoformat(),
                "notification_channels": alert.notification_channels
            }
            
            # Store in alert history
            self.alert_history.append(alert_event)
            
            # Send notifications
            await self._send_alert_notifications(alert_event)
            
            logger.warning(f"Alert triggered: {alert.name} - {current_value} {alert.comparison} {alert.threshold}")
            
        except Exception as e:
            logger.error(f"Failed to trigger alert: {e}")
    
    async def _send_alert_notifications(self, alert_event: Dict[str, Any]):
        """Send alert notifications to configured channels."""
        try:
            for channel in alert_event["notification_channels"]:
                if channel.startswith("slack://"):
                    await self._send_slack_notification(channel, alert_event)
                elif channel.startswith("email://"):
                    await self._send_email_notification(channel, alert_event)
                else:
                    logger.warning(f"Unknown notification channel: {channel}")
                    
        except Exception as e:
            logger.error(f"Failed to send alert notifications: {e}")
    
    async def _send_slack_notification(self, channel: str, alert_event: Dict[str, Any]):
        """Send Slack notification (simulated)."""
        # In production, this would integrate with Slack API
        logger.info(f"Slack notification sent to {channel}: {alert_event['name']}")
    
    async def _send_email_notification(self, channel: str, alert_event: Dict[str, Any]):
        """Send email notification (simulated)."""
        # In production, this would integrate with SES or other email service
        logger.info(f"Email notification sent to {channel}: {alert_event['name']}")
    
    async def get_metrics(
        self, 
        metric_name: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[MetricPoint]:
        """Get metric data points for a time range."""
        try:
            if metric_name not in self.metrics_buffer:
                return []
            
            metrics = self.metrics_buffer[metric_name]
            
            if start_time is None:
                start_time = datetime.utcnow() - timedelta(hours=1)
            if end_time is None:
                end_time = datetime.utcnow()
            
            filtered_metrics = [
                m for m in metrics
                if start_time <= m.timestamp <= end_time
            ]
            
            return sorted(filtered_metrics, key=lambda x: x.timestamp)
            
        except Exception as e:
            logger.error(f"Failed to get metrics: {e}")
            return []
    
    async def get_dashboard_data(self, dashboard_id: str) -> Dict[str, Any]:
        """Get dashboard data with AI insights."""
        try:
            if dashboard_id not in self.dashboards:
                return {"error": f"Dashboard not found: {dashboard_id}"}
            
            dashboard = self.dashboards[dashboard_id]
            dashboard_data = {
                "dashboard_id": dashboard_id,
                "name": dashboard.name,
                "description": dashboard.description,
                "widgets": [],
                "ai_insights": [],
                "last_updated": datetime.utcnow().isoformat()
            }
            
            # Generate widget data
            for widget in dashboard.widgets:
                widget_data = await self._generate_widget_data(widget)
                dashboard_data["widgets"].append(widget_data)
            
            # Generate AI insights if enabled
            if dashboard.ai_insights_enabled and self.ai_service:
                ai_insights = await self._generate_dashboard_ai_insights(dashboard_id)
                dashboard_data["ai_insights"] = ai_insights
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Failed to get dashboard data: {e}")
            return {"error": str(e)}
    
    async def _generate_widget_data(self, widget: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data for dashboard widget."""
        try:
            widget_data = widget.copy()
            
            if widget["type"] == "metric_chart":
                # Get metric data
                metric_name = widget["metric"]
                time_range = widget.get("time_range", "1h")
                
                # Parse time range
                if time_range == "1h":
                    start_time = datetime.utcnow() - timedelta(hours=1)
                elif time_range == "4h":
                    start_time = datetime.utcnow() - timedelta(hours=4)
                elif time_range == "24h":
                    start_time = datetime.utcnow() - timedelta(hours=24)
                else:
                    start_time = datetime.utcnow() - timedelta(hours=1)
                
                metrics = await self.get_metrics(metric_name, start_time)
                
                widget_data["data"] = [
                    {
                        "timestamp": m.timestamp.isoformat(),
                        "value": m.value
                    }
                    for m in metrics
                ]
                
            elif widget["type"] == "ai_insights":
                # Generate AI insights
                if self.ai_service:
                    insights = await self.ai_service.get_comprehensive_insights("monitoring-dashboard")
                    widget_data["insights"] = [
                        {
                            "type": insight.insight_type.value,
                            "title": insight.title,
                            "description": insight.description,
                            "priority": insight.priority.value,
                            "confidence": insight.confidence
                        }
                        for insight in insights[:5]  # Top 5 insights
                    ]
                else:
                    widget_data["insights"] = []
            
            return widget_data
            
        except Exception as e:
            logger.error(f"Widget data generation failed: {e}")
            return widget
    
    async def _generate_dashboard_ai_insights(self, dashboard_id: str) -> List[Dict[str, Any]]:
        """Generate AI insights for dashboard."""
        try:
            if not self.ai_service:
                return []
            
            insights = await self.ai_service.get_comprehensive_insights(f"dashboard-{dashboard_id}")
            
            return [
                {
                    "insight_id": f"insight-{i}",
                    "type": insight.insight_type.value,
                    "title": insight.title,
                    "description": insight.description,
                    "priority": insight.priority.value,
                    "confidence": insight.confidence,
                    "recommendations": insight.recommendations,
                    "timestamp": insight.timestamp.isoformat()
                }
                for i, insight in enumerate(insights[:10])  # Top 10 insights
            ]
            
        except Exception as e:
            logger.error(f"Dashboard AI insights generation failed: {e}")
            return []
    
    async def get_alert_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get alert history."""
        return sorted(self.alert_history, key=lambda x: x["triggered_at"], reverse=True)[:limit]
    
    async def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status."""
        try:
            # Get recent metrics
            current_time = datetime.utcnow()
            recent_cutoff = current_time - timedelta(minutes=5)
            
            health_status = {
                "overall_status": "healthy",
                "components": {},
                "metrics_summary": {},
                "active_alerts": 0,
                "last_updated": current_time.isoformat()
            }
            
            # Check component health based on recent metrics
            for metric_name, metrics in self.metrics_buffer.items():
                recent_metrics = [m for m in metrics if m.timestamp > recent_cutoff]
                
                if recent_metrics:
                    avg_value = sum(m.value for m in recent_metrics) / len(recent_metrics)
                    health_status["metrics_summary"][metric_name] = {
                        "current_value": avg_value,
                        "unit": recent_metrics[-1].unit,
                        "status": "normal"
                    }
                    
                    # Determine component status
                    if metric_name == "cpu_utilization" and avg_value > 90:
                        health_status["components"]["cpu"] = "critical"
                        health_status["overall_status"] = "degraded"
                    elif metric_name == "memory_utilization" and avg_value > 95:
                        health_status["components"]["memory"] = "critical"
                        health_status["overall_status"] = "degraded"
                    elif metric_name == "error_rate" and avg_value > 5:
                        health_status["components"]["application"] = "unhealthy"
                        health_status["overall_status"] = "unhealthy"
            
            # Count active alerts
            recent_alerts = [
                alert for alert in self.alert_history
                if datetime.fromisoformat(alert["triggered_at"]) > recent_cutoff
            ]
            health_status["active_alerts"] = len(recent_alerts)
            
            return health_status
            
        except Exception as e:
            logger.error(f"System health check failed: {e}")
            return {"error": str(e)}

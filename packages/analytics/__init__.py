"""
Advanced Analytics and Business Intelligence Module

This module provides comprehensive analytics capabilities for the AI-Native PaaS Platform,
including real-time metrics, predictive analytics, business intelligence, and advanced
reporting features.

Key Components:
- MetricsCollector: Real-time data collection and aggregation
- AnalyticsEngine: Advanced data processing and analysis
- BusinessIntelligence: Strategic insights and reporting
- PredictiveAnalytics: Forecasting and trend analysis
- ReportingService: Automated report generation
- DashboardService: Interactive analytics dashboards
"""

from .metrics_collector import MetricsCollector, MetricType, MetricData
from .analytics_engine import AnalyticsEngine, AnalysisResult, AnalysisType
from .business_intelligence import BusinessIntelligence, BusinessInsight, InsightType
from .predictive_analytics import PredictiveAnalytics, Forecast, TrendAnalysis
from .reporting_service import ReportingService, Report, ReportType
from .dashboard_service import DashboardService, Dashboard, Widget

__all__ = [
    'MetricsCollector',
    'MetricType',
    'MetricData',
    'AnalyticsEngine',
    'AnalysisResult',
    'AnalysisType',
    'BusinessIntelligence',
    'BusinessInsight',
    'InsightType',
    'PredictiveAnalytics',
    'Forecast',
    'TrendAnalysis',
    'ReportingService',
    'Report',
    'ReportType',
    'DashboardService',
    'Dashboard',
    'Widget'
]

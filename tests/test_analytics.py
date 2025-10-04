"""
Comprehensive tests for the Analytics module

This test suite validates all components of the advanced analytics system including
metrics collection, analytics engine, business intelligence, predictive analytics,
reporting, and dashboard services.
"""

import asyncio
import pytest
import numpy as np
from datetime import datetime, timedelta
from uuid import uuid4

# Import analytics modules
from src.analytics.metrics_collector import (
    MetricsCollector, MetricData, MetricType, MetricUnit, SystemMetricsCollector
)
from src.analytics.analytics_engine import (
    AnalyticsEngine, AnalysisType, AnalysisResult, Severity
)
from src.analytics.business_intelligence import (
    BusinessIntelligence, BusinessInsight, InsightType, BusinessMetric
)
from src.analytics.predictive_analytics import (
    PredictiveAnalytics, ForecastModel, ForecastHorizon
)
from src.analytics.reporting_service import (
    ReportingService, ReportType, ReportFormat, ReportFrequency
)
from src.analytics.dashboard_service import (
    DashboardService, DashboardType, WidgetType, Widget
)


class TestMetricsCollector:
    """Test metrics collection functionality"""
    
    @pytest.mark.asyncio
    async def test_metrics_collector_basic(self):
        """Test basic metrics collection"""
        collector = MetricsCollector(buffer_size=100, flush_interval=1)
        
        # Start collector
        await collector.start()
        
        # Collect some metrics
        await collector.collect_performance_metric(
            "api_response_time", 150.5, MetricUnit.MILLISECONDS,
            {"endpoint": "/api/test"}
        )
        
        await collector.collect_resource_usage(
            "cpu", 75.0, 100.0, {"host": "test-host"}
        )
        
        # Wait a bit for processing
        await asyncio.sleep(0.1)
        
        # Check aggregations
        aggregations = await collector.get_aggregated_metrics(MetricType.PERFORMANCE)
        assert len(aggregations) > 0
        
        # Stop collector
        await collector.stop()
        
    @pytest.mark.asyncio
    async def test_system_metrics_collector(self):
        """Test system metrics collection"""
        collector = MetricsCollector()
        system_collector = SystemMetricsCollector(collector)
        
        await collector.start()
        await system_collector.collect_system_metrics()
        
        # Check that metrics were collected
        assert len(collector.metrics_buffer) > 0
        
        await collector.stop()
        
    def test_metric_data_serialization(self):
        """Test metric data serialization"""
        metric = MetricData(
            metric_id="test-123",
            metric_type=MetricType.PERFORMANCE,
            name="test_metric",
            value=42.5,
            unit=MetricUnit.MILLISECONDS,
            tags={"service": "test"}
        )
        
        serialized = metric.to_dict()
        assert serialized['metric_id'] == "test-123"
        assert serialized['metric_type'] == "performance"
        assert serialized['value'] == 42.5


class TestAnalyticsEngine:
    """Test analytics engine functionality"""
    
    def _create_sample_metrics(self, count: int = 50) -> list:
        """Create sample metrics for testing"""
        metrics = []
        base_time = datetime.utcnow() - timedelta(hours=count)
        
        for i in range(count):
            timestamp = base_time + timedelta(hours=i)
            
            # Create response time metric with trend and anomalies
            base_value = 100 + i * 0.5  # Slight upward trend
            if i in [10, 30]:  # Add anomalies
                value = base_value * 3
            else:
                value = base_value + np.random.normal(0, 10)
                
            metrics.append(MetricData(
                metric_id=str(uuid4()),
                metric_type=MetricType.PERFORMANCE,
                name="api_response_time",
                value=max(0, value),
                unit=MetricUnit.MILLISECONDS,
                timestamp=timestamp
            ))
            
        return metrics
        
    @pytest.mark.asyncio
    async def test_statistical_analysis(self):
        """Test statistical analysis"""
        engine = AnalyticsEngine()
        metrics = self._create_sample_metrics(30)
        
        results = await engine.analyze_metrics(metrics, [AnalysisType.STATISTICAL])
        
        assert len(results) > 0
        stat_result = results[0]
        assert stat_result.analysis_type == AnalysisType.STATISTICAL
        assert 'mean' in stat_result.data
        assert 'std' in stat_result.data
        assert stat_result.confidence > 0
        
    @pytest.mark.asyncio
    async def test_trend_analysis(self):
        """Test trend analysis"""
        engine = AnalyticsEngine()
        metrics = self._create_sample_metrics(30)
        
        results = await engine.analyze_metrics(metrics, [AnalysisType.TREND])
        
        assert len(results) > 0
        trend_result = results[0]
        assert trend_result.analysis_type == AnalysisType.TREND
        assert 'trend_direction' in trend_result.data
        assert 'trend_strength' in trend_result.data
        
    @pytest.mark.asyncio
    async def test_anomaly_detection(self):
        """Test anomaly detection"""
        engine = AnalyticsEngine()
        metrics = self._create_sample_metrics(50)  # Includes anomalies
        
        results = await engine.analyze_metrics(metrics, [AnalysisType.ANOMALY])
        
        assert len(results) > 0
        anomaly_result = results[0]
        assert anomaly_result.analysis_type == AnalysisType.ANOMALY
        assert 'anomalous_points' in anomaly_result.data
        
    @pytest.mark.asyncio
    async def test_performance_analysis(self):
        """Test performance analysis"""
        engine = AnalyticsEngine()
        metrics = self._create_sample_metrics(20)
        
        results = await engine.analyze_metrics(metrics, [AnalysisType.PERFORMANCE])
        
        assert len(results) > 0
        perf_result = results[0]
        assert perf_result.analysis_type == AnalysisType.PERFORMANCE
        assert 'p95' in perf_result.data or 'mean' in perf_result.data
        
    @pytest.mark.asyncio
    async def test_analysis_summary(self):
        """Test analysis summary generation"""
        engine = AnalyticsEngine()
        metrics = self._create_sample_metrics(30)
        
        # Run multiple analyses
        await engine.analyze_metrics(metrics, [
            AnalysisType.STATISTICAL,
            AnalysisType.TREND,
            AnalysisType.ANOMALY
        ])
        
        summary = await engine.get_analysis_summary()
        
        assert summary['total_analyses'] > 0
        assert 'by_type' in summary
        assert 'by_severity' in summary


class TestBusinessIntelligence:
    """Test business intelligence functionality"""
    
    def _create_business_metrics(self) -> list:
        """Create sample business metrics"""
        metrics = []
        base_time = datetime.utcnow() - timedelta(days=60)
        
        for i in range(60):
            timestamp = base_time + timedelta(days=i)
            
            # Revenue with significant growth after day 30
            if i < 30:
                revenue = 10000 + i * 50  # Slow growth
            else:
                revenue = 10000 + 30 * 50 + (i - 30) * 200  # Accelerated growth
                
            metrics.append(MetricData(
                metric_id=str(uuid4()),
                metric_type=MetricType.BUSINESS,
                name="daily_revenue",
                value=revenue,
                unit=MetricUnit.DOLLARS,
                timestamp=timestamp
            ))
            
            # Active users with some volatility
            if i < 30:
                users = 1000 + i * 10
            else:
                users = 1000 + 30 * 10 + (i - 30) * 25  # Growth acceleration
                
            metrics.append(MetricData(
                metric_id=str(uuid4()),
                metric_type=MetricType.USER_BEHAVIOR,
                name="active_users",
                value=users,
                unit=MetricUnit.COUNT,
                timestamp=timestamp
            ))
            
            # Add cost metrics for cost optimization insights
            cost = 5000 + i * 20 + (100 if i % 7 == 0 else 0)  # Weekly spikes
            metrics.append(MetricData(
                metric_id=str(uuid4()),
                metric_type=MetricType.COST,
                name="infrastructure_cost",
                value=cost,
                unit=MetricUnit.DOLLARS,
                timestamp=timestamp,
                tags={"service": "compute"}
            ))
            
        return metrics
        
    @pytest.mark.asyncio
    async def test_business_insights_generation(self):
        """Test business insights generation"""
        bi = BusinessIntelligence()
        metrics = self._create_business_metrics()
        
        insights = await bi.generate_insights(metrics, [])
        
        assert len(insights) > 0
        
        # Check for revenue insights
        revenue_insights = [i for i in insights if i.insight_type == InsightType.REVENUE]
        assert len(revenue_insights) > 0
        
        revenue_insight = revenue_insights[0]
        assert revenue_insight.confidence > 0
        assert len(revenue_insight.recommendations) > 0
        
    @pytest.mark.asyncio
    async def test_kpi_calculation(self):
        """Test KPI calculation"""
        bi = BusinessIntelligence()
        metrics = self._create_business_metrics()
        
        kpi_snapshot = await bi.calculate_kpis(metrics)
        
        assert len(kpi_snapshot.metrics) > 0
        assert BusinessMetric.MONTHLY_RECURRING_REVENUE in kpi_snapshot.metrics or \
               BusinessMetric.ACTIVE_USERS in kpi_snapshot.metrics
               
    @pytest.mark.asyncio
    async def test_executive_summary(self):
        """Test executive summary generation"""
        bi = BusinessIntelligence()
        metrics = self._create_business_metrics()
        
        # Generate some insights first
        await bi.generate_insights(metrics, [])
        
        summary = await bi.get_executive_summary()
        
        assert 'total_insights' in summary
        assert 'financial_impact' in summary
        assert 'key_recommendations' in summary


class TestPredictiveAnalytics:
    """Test predictive analytics functionality"""
    
    def _create_time_series_data(self) -> list:
        """Create time series data for forecasting"""
        metrics = []
        base_time = datetime.utcnow() - timedelta(days=7)
        
        for i in range(168):  # 7 days of hourly data
            timestamp = base_time + timedelta(hours=i)
            
            # CPU usage with trend and seasonality
            trend = i * 0.05
            seasonal = 10 * np.sin(2 * np.pi * i / 24)
            noise = np.random.normal(0, 5)
            cpu_usage = max(0, min(100, 50 + trend + seasonal + noise))
            
            metrics.append(MetricData(
                metric_id=str(uuid4()),
                metric_type=MetricType.RESOURCE_USAGE,
                name="cpu_usage_percentage",
                value=cpu_usage,
                unit=MetricUnit.PERCENTAGE,
                timestamp=timestamp
            ))
            
        return metrics
        
    @pytest.mark.asyncio
    async def test_linear_regression_forecast(self):
        """Test linear regression forecasting"""
        predictor = PredictiveAnalytics()
        metrics = self._create_time_series_data()
        
        forecast = await predictor.create_forecast(
            metrics, "cpu_usage_percentage",
            ForecastHorizon.SHORT_TERM,
            ForecastModel.LINEAR_REGRESSION
        )
        
        assert forecast.metric_name == "cpu_usage_percentage"
        assert forecast.model_type == ForecastModel.LINEAR_REGRESSION
        assert len(forecast.forecast_values) > 0
        assert len(forecast.forecast_timestamps) == len(forecast.forecast_values)
        assert 'r_squared' in forecast.accuracy_metrics
        
    @pytest.mark.asyncio
    async def test_trend_analysis(self):
        """Test trend analysis"""
        predictor = PredictiveAnalytics()
        metrics = self._create_time_series_data()
        
        trend_analysis = await predictor.analyze_trends(metrics, "cpu_usage_percentage")
        
        assert trend_analysis.metric_name == "cpu_usage_percentage"
        assert trend_analysis.trend_direction in ["increasing", "decreasing", "stable"]
        assert 0 <= trend_analysis.trend_strength <= 1
        assert trend_analysis.r_squared >= 0
        
    @pytest.mark.asyncio
    async def test_anomaly_prediction(self):
        """Test anomaly prediction"""
        predictor = PredictiveAnalytics()
        metrics = self._create_time_series_data()
        
        anomaly_prediction = await predictor.predict_anomalies(
            metrics, "cpu_usage_percentage"
        )
        
        assert anomaly_prediction.metric_name == "cpu_usage_percentage"
        assert anomaly_prediction.anomaly_threshold > 0
        assert 0 <= anomaly_prediction.model_confidence <= 1
        
    @pytest.mark.asyncio
    async def test_model_comparison(self):
        """Test model comparison"""
        predictor = PredictiveAnalytics()
        metrics = self._create_time_series_data()
        
        comparison = await predictor.compare_models(metrics, "cpu_usage_percentage")
        
        assert len(comparison) > 0
        assert 'linear_regression' in comparison
        
        # Check that at least one model has accuracy metrics
        has_metrics = any(
            'r_squared' in model_data 
            for model_data in comparison.values()
            if isinstance(model_data, dict)
        )
        assert has_metrics


class TestReportingService:
    """Test reporting service functionality"""
    
    @pytest.mark.asyncio
    async def test_executive_summary_report(self):
        """Test executive summary report generation"""
        reporting = ReportingService()
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        report = await reporting.generate_report(
            ReportType.EXECUTIVE_SUMMARY,
            start_date,
            end_date,
            ReportFormat.HTML
        )
        
        assert report.report_type == ReportType.EXECUTIVE_SUMMARY
        assert report.format == ReportFormat.HTML
        assert len(report.sections) > 0
        assert report.period_start == start_date
        assert report.period_end == end_date
        
    @pytest.mark.asyncio
    async def test_performance_report(self):
        """Test performance report generation"""
        reporting = ReportingService()
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)
        
        report = await reporting.generate_report(
            ReportType.PERFORMANCE_REPORT,
            start_date,
            end_date
        )
        
        assert report.report_type == ReportType.PERFORMANCE_REPORT
        assert len(report.sections) > 0
        
        # Check for specific sections
        section_titles = [s.title for s in report.sections]
        assert any("Response Time" in title for title in section_titles)
        
    @pytest.mark.asyncio
    async def test_cost_analysis_report(self):
        """Test cost analysis report generation"""
        reporting = ReportingService()
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        report = await reporting.generate_report(
            ReportType.COST_ANALYSIS,
            start_date,
            end_date
        )
        
        assert report.report_type == ReportType.COST_ANALYSIS
        assert len(report.sections) > 0
        
    @pytest.mark.asyncio
    async def test_report_export(self):
        """Test report export functionality"""
        reporting = ReportingService()
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)
        
        report = await reporting.generate_report(
            ReportType.EXECUTIVE_SUMMARY,
            start_date,
            end_date
        )
        
        # Test HTML export
        html_export = await reporting.export_report(report.report_id, ReportFormat.HTML)
        assert 'content' in html_export
        assert 'text/html' in html_export['content_type']
        
        # Test CSV export
        csv_export = await reporting.export_report(report.report_id, ReportFormat.CSV)
        assert 'content' in csv_export
        assert 'text/csv' in csv_export['content_type']
        
    @pytest.mark.asyncio
    async def test_report_listing(self):
        """Test report listing functionality"""
        reporting = ReportingService()
        
        # Generate a few reports
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)
        
        await reporting.generate_report(ReportType.EXECUTIVE_SUMMARY, start_date, end_date)
        await reporting.generate_report(ReportType.PERFORMANCE_REPORT, start_date, end_date)
        
        # List all reports
        all_reports = await reporting.list_reports()
        assert len(all_reports) >= 2
        
        # List filtered reports
        exec_reports = await reporting.list_reports(ReportType.EXECUTIVE_SUMMARY)
        assert len(exec_reports) >= 1
        assert all(r.report_type == ReportType.EXECUTIVE_SUMMARY for r in exec_reports)


class TestDashboardService:
    """Test dashboard service functionality"""
    
    @pytest.mark.asyncio
    async def test_dashboard_creation(self):
        """Test dashboard creation"""
        dashboard_service = DashboardService()
        
        dashboard = await dashboard_service.create_dashboard(
            name="Test Dashboard",
            description="Test dashboard for unit tests",
            dashboard_type=DashboardType.OPERATIONAL
        )
        
        assert dashboard.name == "Test Dashboard"
        assert dashboard.dashboard_type == DashboardType.OPERATIONAL
        assert len(dashboard.widgets) == 0  # Empty dashboard
        
    @pytest.mark.asyncio
    async def test_dashboard_from_template(self):
        """Test dashboard creation from template"""
        dashboard_service = DashboardService()
        
        dashboard = await dashboard_service.create_dashboard(
            name="Executive Dashboard",
            description="Executive dashboard from template",
            dashboard_type=DashboardType.EXECUTIVE,
            template_id="executive_template"
        )
        
        assert dashboard.dashboard_type == DashboardType.EXECUTIVE
        assert len(dashboard.widgets) > 0  # Should have widgets from template
        
    @pytest.mark.asyncio
    async def test_widget_management(self):
        """Test widget add/remove/update operations"""
        dashboard_service = DashboardService()
        
        # Create dashboard
        dashboard = await dashboard_service.create_dashboard(
            name="Test Dashboard",
            description="Test dashboard",
            dashboard_type=DashboardType.CUSTOM
        )
        
        # Add widget
        widget = Widget(
            widget_id=str(uuid4()),
            widget_type=WidgetType.METRIC_CARD,
            title="Test Metric",
            description="Test metric widget",
            position={'x': 0, 'y': 0, 'width': 3, 'height': 2},
            data_source="test_metrics",
            query={'metric': 'test_value'}
        )
        
        success = await dashboard_service.add_widget(dashboard.dashboard_id, widget)
        assert success
        
        # Check widget was added
        updated_dashboard = await dashboard_service.get_dashboard(dashboard.dashboard_id)
        assert len(updated_dashboard.widgets) == 1
        
        # Update widget
        success = await dashboard_service.update_widget(
            dashboard.dashboard_id,
            widget.widget_id,
            {'title': 'Updated Test Metric'}
        )
        assert success
        
        # Remove widget
        success = await dashboard_service.remove_widget(
            dashboard.dashboard_id,
            widget.widget_id
        )
        assert success
        
        # Check widget was removed
        final_dashboard = await dashboard_service.get_dashboard(dashboard.dashboard_id)
        assert len(final_dashboard.widgets) == 0
        
    @pytest.mark.asyncio
    async def test_widget_data_generation(self):
        """Test widget data generation"""
        dashboard_service = DashboardService()
        
        # Test metric card widget
        metric_widget = Widget(
            widget_id=str(uuid4()),
            widget_type=WidgetType.METRIC_CARD,
            title="CPU Usage",
            description="Current CPU usage",
            position={'x': 0, 'y': 0, 'width': 3, 'height': 2},
            data_source="system_metrics",
            query={'metric': 'cpu_usage_percentage'}
        )
        
        data = await dashboard_service.get_widget_data(metric_widget)
        assert 'value' in data
        assert 'trend' in data
        
        # Test line chart widget
        chart_widget = Widget(
            widget_id=str(uuid4()),
            widget_type=WidgetType.LINE_CHART,
            title="Response Time Trend",
            description="API response time over time",
            position={'x': 0, 'y': 2, 'width': 6, 'height': 4},
            data_source="performance_metrics",
            query={'metric': 'api_response_time', 'period': '24h'}
        )
        
        chart_data = await dashboard_service.get_widget_data(chart_widget)
        assert 'labels' in chart_data
        assert 'datasets' in chart_data
        
    @pytest.mark.asyncio
    async def test_dashboard_data_retrieval(self):
        """Test complete dashboard data retrieval"""
        dashboard_service = DashboardService()
        
        # Create dashboard with template
        dashboard = await dashboard_service.create_dashboard(
            name="Test Dashboard",
            description="Test dashboard",
            dashboard_type=DashboardType.OPERATIONAL,
            template_id="operational_template"
        )
        
        # Get complete dashboard data
        dashboard_data = await dashboard_service.get_dashboard_data(dashboard.dashboard_id)
        
        assert 'dashboard_id' in dashboard_data
        assert 'widgets' in dashboard_data
        assert 'widget_data' in dashboard_data
        assert 'last_updated' in dashboard_data
        
        # Check that widget data is included
        assert len(dashboard_data['widget_data']) == len(dashboard.widgets)
        
    @pytest.mark.asyncio
    async def test_dashboard_export_import(self):
        """Test dashboard export and import"""
        dashboard_service = DashboardService()
        
        # Create dashboard
        original_dashboard = await dashboard_service.create_dashboard(
            name="Export Test Dashboard",
            description="Dashboard for export testing",
            dashboard_type=DashboardType.TECHNICAL,
            template_id="operational_template"
        )
        
        # Export dashboard
        export_data = await dashboard_service.export_dashboard(original_dashboard.dashboard_id)
        assert 'dashboard' in export_data
        assert 'export_timestamp' in export_data
        
        # Import dashboard
        new_dashboard_id = await dashboard_service.import_dashboard(export_data)
        assert new_dashboard_id != original_dashboard.dashboard_id
        
        # Verify imported dashboard
        imported_dashboard = await dashboard_service.get_dashboard(new_dashboard_id)
        assert imported_dashboard is not None
        assert len(imported_dashboard.widgets) == len(original_dashboard.widgets)


class TestAnalyticsIntegration:
    """Test integration between analytics components"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_analytics_workflow(self):
        """Test complete analytics workflow"""
        
        # 1. Collect metrics
        collector = MetricsCollector()
        await collector.start()
        
        # Generate sample metrics
        for i in range(50):
            await collector.collect_performance_metric(
                "api_response_time", 100 + i + np.random.normal(0, 10),
                MetricUnit.MILLISECONDS
            )
            await collector.collect_resource_usage(
                "cpu", 50 + i * 0.5 + np.random.normal(0, 5), 100.0
            )
            
        await asyncio.sleep(0.1)  # Let metrics process
        
        # 2. Analyze metrics
        engine = AnalyticsEngine()
        analysis_results = await engine.analyze_metrics(
            collector.metrics_buffer,
            [AnalysisType.STATISTICAL, AnalysisType.TREND, AnalysisType.PERFORMANCE]
        )
        
        assert len(analysis_results) > 0
        
        # 3. Generate business insights
        bi = BusinessIntelligence()
        insights = await bi.generate_insights(collector.metrics_buffer, analysis_results)
        
        # 4. Create forecasts
        predictor = PredictiveAnalytics()
        if len(collector.metrics_buffer) >= 10:
            perf_metrics = [m for m in collector.metrics_buffer if m.name == "api_response_time"]
            if perf_metrics:
                forecast = await predictor.create_forecast(
                    perf_metrics, "api_response_time"
                )
                assert forecast is not None
                
        # 5. Generate reports
        reporting = ReportingService()
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=1)
        
        report = await reporting.generate_report(
            ReportType.PERFORMANCE_REPORT,
            start_date,
            end_date
        )
        
        assert report is not None
        
        # 6. Create dashboard
        dashboard_service = DashboardService()
        dashboard = await dashboard_service.create_dashboard(
            name="Analytics Test Dashboard",
            description="Dashboard for integration test",
            dashboard_type=DashboardType.OPERATIONAL,
            template_id="operational_template"
        )
        
        dashboard_data = await dashboard_service.get_dashboard_data(dashboard.dashboard_id)
        assert dashboard_data is not None
        
        await collector.stop()
        
        print("✅ End-to-end analytics workflow completed successfully")


# Test runner
async def run_analytics_tests():
    """Run all analytics tests"""
    
    print("🧪 Running Analytics Module Tests...")
    
    # Metrics Collector Tests
    print("Testing Metrics Collector...")
    test_collector = TestMetricsCollector()
    await test_collector.test_metrics_collector_basic()
    await test_collector.test_system_metrics_collector()
    test_collector.test_metric_data_serialization()
    print("✅ Metrics Collector tests passed")
    
    # Analytics Engine Tests
    print("Testing Analytics Engine...")
    test_engine = TestAnalyticsEngine()
    await test_engine.test_statistical_analysis()
    await test_engine.test_trend_analysis()
    await test_engine.test_anomaly_detection()
    await test_engine.test_performance_analysis()
    await test_engine.test_analysis_summary()
    print("✅ Analytics Engine tests passed")
    
    # Business Intelligence Tests
    print("Testing Business Intelligence...")
    test_bi = TestBusinessIntelligence()
    await test_bi.test_business_insights_generation()
    await test_bi.test_kpi_calculation()
    await test_bi.test_executive_summary()
    print("✅ Business Intelligence tests passed")
    
    # Predictive Analytics Tests
    print("Testing Predictive Analytics...")
    test_pred = TestPredictiveAnalytics()
    await test_pred.test_linear_regression_forecast()
    await test_pred.test_trend_analysis()
    await test_pred.test_anomaly_prediction()
    await test_pred.test_model_comparison()
    print("✅ Predictive Analytics tests passed")
    
    # Reporting Service Tests
    print("Testing Reporting Service...")
    test_reporting = TestReportingService()
    await test_reporting.test_executive_summary_report()
    await test_reporting.test_performance_report()
    await test_reporting.test_cost_analysis_report()
    await test_reporting.test_report_export()
    await test_reporting.test_report_listing()
    print("✅ Reporting Service tests passed")
    
    # Dashboard Service Tests
    print("Testing Dashboard Service...")
    test_dashboard = TestDashboardService()
    await test_dashboard.test_dashboard_creation()
    await test_dashboard.test_dashboard_from_template()
    await test_dashboard.test_widget_management()
    await test_dashboard.test_widget_data_generation()
    await test_dashboard.test_dashboard_data_retrieval()
    await test_dashboard.test_dashboard_export_import()
    print("✅ Dashboard Service tests passed")
    
    # Integration Tests
    print("Testing Analytics Integration...")
    test_integration = TestAnalyticsIntegration()
    await test_integration.test_end_to_end_analytics_workflow()
    print("✅ Analytics Integration tests passed")
    
    print("🎉 All Analytics Module tests passed successfully!")


if __name__ == "__main__":
    asyncio.run(run_analytics_tests())

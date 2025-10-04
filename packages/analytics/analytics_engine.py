"""
Advanced Analytics Engine

This module provides sophisticated data analysis capabilities including statistical analysis,
pattern recognition, anomaly detection, and intelligent insights generation.
"""

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from uuid import UUID, uuid4
import logging
import json
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from .metrics_collector import MetricData, MetricType, MetricAggregation

logger = logging.getLogger(__name__)


class AnalysisType(Enum):
    """Types of analysis that can be performed"""
    STATISTICAL = "statistical"
    TREND = "trend"
    ANOMALY = "anomaly"
    CORRELATION = "correlation"
    CLUSTERING = "clustering"
    FORECASTING = "forecasting"
    PATTERN_RECOGNITION = "pattern_recognition"
    PERFORMANCE = "performance"
    CAPACITY_PLANNING = "capacity_planning"
    ROOT_CAUSE = "root_cause"


class Severity(Enum):
    """Severity levels for analysis results"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AnalysisResult:
    """Result of an analytics analysis"""
    analysis_id: str
    analysis_type: AnalysisType
    title: str
    description: str
    severity: Severity
    confidence: float  # 0.0 to 1.0
    timestamp: datetime = field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert analysis result to dictionary"""
        return {
            'analysis_id': self.analysis_id,
            'analysis_type': self.analysis_type.value,
            'title': self.title,
            'description': self.description,
            'severity': self.severity.value,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat(),
            'data': self.data,
            'recommendations': self.recommendations,
            'tags': self.tags
        }


@dataclass
class TrendAnalysis:
    """Trend analysis result"""
    metric_name: str
    trend_direction: str  # "increasing", "decreasing", "stable"
    trend_strength: float  # 0.0 to 1.0
    slope: float
    r_squared: float
    forecast_values: List[float]
    forecast_timestamps: List[datetime]
    confidence_interval: Tuple[List[float], List[float]]


@dataclass
class AnomalyDetection:
    """Anomaly detection result"""
    metric_name: str
    anomalous_points: List[Tuple[datetime, float]]
    anomaly_scores: List[float]
    threshold: float
    detection_method: str


@dataclass
class CorrelationAnalysis:
    """Correlation analysis result"""
    metric_pairs: List[Tuple[str, str]]
    correlation_coefficients: List[float]
    p_values: List[float]
    significant_correlations: List[Tuple[str, str, float]]


class AnalyticsEngine:
    """
    Advanced analytics engine for comprehensive data analysis and insights generation
    """
    
    def __init__(self):
        self.analysis_history: List[AnalysisResult] = []
        self.cached_results: Dict[str, AnalysisResult] = {}
        self.analysis_rules: Dict[str, callable] = {}
        
    async def analyze_metrics(self, metrics: List[MetricData], 
                            analysis_types: List[AnalysisType]) -> List[AnalysisResult]:
        """Perform comprehensive analysis on metrics data"""
        results = []
        
        # Convert metrics to DataFrame for analysis
        df = self._metrics_to_dataframe(metrics)
        
        for analysis_type in analysis_types:
            try:
                if analysis_type == AnalysisType.STATISTICAL:
                    result = await self._statistical_analysis(df, metrics)
                elif analysis_type == AnalysisType.TREND:
                    result = await self._trend_analysis(df, metrics)
                elif analysis_type == AnalysisType.ANOMALY:
                    result = await self._anomaly_analysis(df, metrics)
                elif analysis_type == AnalysisType.CORRELATION:
                    result = await self._correlation_analysis(df, metrics)
                elif analysis_type == AnalysisType.CLUSTERING:
                    result = await self._clustering_analysis(df, metrics)
                elif analysis_type == AnalysisType.PERFORMANCE:
                    result = await self._performance_analysis(df, metrics)
                elif analysis_type == AnalysisType.CAPACITY_PLANNING:
                    result = await self._capacity_planning_analysis(df, metrics)
                else:
                    continue
                    
                if result:
                    results.extend(result if isinstance(result, list) else [result])
                    
            except Exception as e:
                logger.error(f"Error in {analysis_type.value} analysis: {e}")
                
        # Store results
        self.analysis_history.extend(results)
        
        return results
        
    async def _statistical_analysis(self, df: pd.DataFrame, 
                                  metrics: List[MetricData]) -> List[AnalysisResult]:
        """Perform statistical analysis on metrics"""
        results = []
        
        # Group by metric name for analysis
        for metric_name in df['name'].unique():
            metric_data = df[df['name'] == metric_name]['value']
            
            if len(metric_data) < 2:
                continue
                
            # Calculate statistics
            stats_data = {
                'count': len(metric_data),
                'mean': float(metric_data.mean()),
                'median': float(metric_data.median()),
                'std': float(metric_data.std()),
                'min': float(metric_data.min()),
                'max': float(metric_data.max()),
                'skewness': float(stats.skew(metric_data)),
                'kurtosis': float(stats.kurtosis(metric_data))
            }
            
            # Determine severity based on coefficient of variation
            cv = stats_data['std'] / stats_data['mean'] if stats_data['mean'] != 0 else 0
            severity = Severity.LOW
            if cv > 0.5:
                severity = Severity.MEDIUM
            if cv > 1.0:
                severity = Severity.HIGH
                
            # Generate recommendations
            recommendations = []
            if cv > 0.8:
                recommendations.append(f"High variability detected in {metric_name}. Consider investigating root causes.")
            if stats_data['skewness'] > 2:
                recommendations.append(f"Significant positive skew in {metric_name}. May indicate outliers or system issues.")
                
            result = AnalysisResult(
                analysis_id=str(uuid4()),
                analysis_type=AnalysisType.STATISTICAL,
                title=f"Statistical Analysis: {metric_name}",
                description=f"Statistical summary for {metric_name} over {stats_data['count']} data points",
                severity=severity,
                confidence=0.95,
                data=stats_data,
                recommendations=recommendations,
                tags={'metric_name': metric_name}
            )
            results.append(result)
            
        return results
        
    async def _trend_analysis(self, df: pd.DataFrame, 
                            metrics: List[MetricData]) -> List[AnalysisResult]:
        """Perform trend analysis on time series data"""
        results = []
        
        for metric_name in df['name'].unique():
            metric_df = df[df['name'] == metric_name].sort_values('timestamp')
            
            if len(metric_df) < 5:
                continue
                
            # Prepare data for trend analysis
            timestamps = pd.to_datetime(metric_df['timestamp'])
            values = metric_df['value'].values
            x = np.arange(len(values))
            
            # Linear regression for trend
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
            
            # Determine trend direction and strength
            trend_direction = "stable"
            if abs(slope) > std_err * 2:  # Significant trend
                trend_direction = "increasing" if slope > 0 else "decreasing"
                
            trend_strength = min(abs(r_value), 1.0)
            
            # Generate forecast (simple linear extrapolation)
            forecast_points = 10
            future_x = np.arange(len(values), len(values) + forecast_points)
            forecast_values = slope * future_x + intercept
            
            # Create future timestamps
            last_timestamp = timestamps.iloc[-1]
            time_delta = (timestamps.iloc[-1] - timestamps.iloc[-2]) if len(timestamps) > 1 else timedelta(minutes=5)
            forecast_timestamps = [last_timestamp + (i + 1) * time_delta for i in range(forecast_points)]
            
            # Determine severity
            severity = Severity.LOW
            if trend_strength > 0.7 and abs(slope) > values.std():
                severity = Severity.MEDIUM
            if trend_strength > 0.9 and abs(slope) > 2 * values.std():
                severity = Severity.HIGH
                
            # Generate recommendations
            recommendations = []
            if trend_direction == "increasing" and slope > 0:
                recommendations.append(f"Upward trend detected in {metric_name}. Monitor for capacity constraints.")
            elif trend_direction == "decreasing" and slope < 0:
                recommendations.append(f"Downward trend detected in {metric_name}. Investigate potential issues.")
                
            trend_data = TrendAnalysis(
                metric_name=metric_name,
                trend_direction=trend_direction,
                trend_strength=trend_strength,
                slope=slope,
                r_squared=r_value**2,
                forecast_values=forecast_values.tolist(),
                forecast_timestamps=forecast_timestamps,
                confidence_interval=([], [])  # Simplified for now
            )
            
            result = AnalysisResult(
                analysis_id=str(uuid4()),
                analysis_type=AnalysisType.TREND,
                title=f"Trend Analysis: {metric_name}",
                description=f"Trend analysis showing {trend_direction} pattern with {trend_strength:.2f} strength",
                severity=severity,
                confidence=trend_strength,
                data=trend_data.__dict__,
                recommendations=recommendations,
                tags={'metric_name': metric_name, 'trend_direction': trend_direction}
            )
            results.append(result)
            
        return results
        
    async def _anomaly_analysis(self, df: pd.DataFrame, 
                              metrics: List[MetricData]) -> List[AnalysisResult]:
        """Perform anomaly detection on metrics"""
        results = []
        
        for metric_name in df['name'].unique():
            metric_df = df[df['name'] == metric_name].sort_values('timestamp')
            
            if len(metric_df) < 10:
                continue
                
            values = metric_df['value'].values
            timestamps = pd.to_datetime(metric_df['timestamp'])
            
            # Statistical anomaly detection using Z-score
            z_scores = np.abs(stats.zscore(values))
            threshold = 2.5  # Standard threshold for anomalies
            
            anomalous_indices = np.where(z_scores > threshold)[0]
            anomalous_points = [(timestamps.iloc[i], values[i]) for i in anomalous_indices]
            
            if not anomalous_points:
                continue
                
            # Calculate severity based on number and magnitude of anomalies
            anomaly_ratio = len(anomalous_points) / len(values)
            max_z_score = np.max(z_scores[anomalous_indices])
            
            severity = Severity.LOW
            if anomaly_ratio > 0.05 or max_z_score > 3.0:
                severity = Severity.MEDIUM
            if anomaly_ratio > 0.1 or max_z_score > 4.0:
                severity = Severity.HIGH
                
            # Generate recommendations
            recommendations = []
            if len(anomalous_points) > 1:
                recommendations.append(f"Multiple anomalies detected in {metric_name}. Investigate system behavior.")
            if max_z_score > 4.0:
                recommendations.append(f"Extreme anomaly detected in {metric_name}. Immediate investigation recommended.")
                
            anomaly_data = AnomalyDetection(
                metric_name=metric_name,
                anomalous_points=anomalous_points,
                anomaly_scores=z_scores[anomalous_indices].tolist(),
                threshold=threshold,
                detection_method="z_score"
            )
            
            result = AnalysisResult(
                analysis_id=str(uuid4()),
                analysis_type=AnalysisType.ANOMALY,
                title=f"Anomaly Detection: {metric_name}",
                description=f"Detected {len(anomalous_points)} anomalies in {metric_name}",
                severity=severity,
                confidence=0.85,
                data=anomaly_data.__dict__,
                recommendations=recommendations,
                tags={'metric_name': metric_name, 'anomaly_count': str(len(anomalous_points))}
            )
            results.append(result)
            
        return results
        
    async def _correlation_analysis(self, df: pd.DataFrame, 
                                  metrics: List[MetricData]) -> List[AnalysisResult]:
        """Perform correlation analysis between metrics"""
        results = []
        
        # Create pivot table for correlation analysis
        pivot_df = df.pivot_table(
            index='timestamp', 
            columns='name', 
            values='value', 
            aggfunc='mean'
        ).fillna(method='ffill').fillna(method='bfill')
        
        if pivot_df.shape[1] < 2:
            return results
            
        # Calculate correlation matrix
        corr_matrix = pivot_df.corr()
        
        # Find significant correlations
        significant_correlations = []
        metric_pairs = []
        correlation_coefficients = []
        p_values = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                metric1 = corr_matrix.columns[i]
                metric2 = corr_matrix.columns[j]
                corr_coef = corr_matrix.iloc[i, j]
                
                if abs(corr_coef) > 0.5:  # Significant correlation threshold
                    # Calculate p-value
                    _, p_val = stats.pearsonr(pivot_df[metric1].dropna(), pivot_df[metric2].dropna())
                    
                    metric_pairs.append((metric1, metric2))
                    correlation_coefficients.append(corr_coef)
                    p_values.append(p_val)
                    
                    if p_val < 0.05:  # Statistically significant
                        significant_correlations.append((metric1, metric2, corr_coef))
                        
        if not significant_correlations:
            return results
            
        # Determine severity
        max_correlation = max(abs(corr) for _, _, corr in significant_correlations)
        severity = Severity.LOW
        if max_correlation > 0.7:
            severity = Severity.MEDIUM
        if max_correlation > 0.9:
            severity = Severity.HIGH
            
        # Generate recommendations
        recommendations = []
        for metric1, metric2, corr in significant_correlations:
            if corr > 0.8:
                recommendations.append(f"Strong positive correlation between {metric1} and {metric2}. Consider joint optimization.")
            elif corr < -0.8:
                recommendations.append(f"Strong negative correlation between {metric1} and {metric2}. Monitor for trade-offs.")
                
        correlation_data = CorrelationAnalysis(
            metric_pairs=metric_pairs,
            correlation_coefficients=correlation_coefficients,
            p_values=p_values,
            significant_correlations=significant_correlations
        )
        
        result = AnalysisResult(
            analysis_id=str(uuid4()),
            analysis_type=AnalysisType.CORRELATION,
            title="Metric Correlation Analysis",
            description=f"Found {len(significant_correlations)} significant correlations between metrics",
            severity=severity,
            confidence=0.90,
            data=correlation_data.__dict__,
            recommendations=recommendations,
            tags={'correlation_count': str(len(significant_correlations))}
        )
        results.append(result)
        
        return results
        
    async def _clustering_analysis(self, df: pd.DataFrame, 
                                 metrics: List[MetricData]) -> List[AnalysisResult]:
        """Perform clustering analysis to identify patterns"""
        results = []
        
        # Create feature matrix for clustering
        pivot_df = df.pivot_table(
            index='timestamp', 
            columns='name', 
            values='value', 
            aggfunc='mean'
        ).fillna(method='ffill').fillna(method='bfill')
        
        if pivot_df.shape[0] < 10 or pivot_df.shape[1] < 2:
            return results
            
        # Standardize features
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(pivot_df.values)
        
        # Perform K-means clustering
        n_clusters = min(5, len(pivot_df) // 3)  # Reasonable number of clusters
        if n_clusters < 2:
            return results
            
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(scaled_data)
        
        # Analyze clusters
        cluster_info = {}
        for i in range(n_clusters):
            cluster_mask = cluster_labels == i
            cluster_data = pivot_df.values[cluster_mask]
            
            cluster_info[f"cluster_{i}"] = {
                'size': int(np.sum(cluster_mask)),
                'centroid': cluster_data.mean(axis=0).tolist(),
                'std': cluster_data.std(axis=0).tolist(),
                'timestamps': pivot_df.index[cluster_mask].tolist()
            }
            
        # Determine severity based on cluster separation
        inertia = kmeans.inertia_
        severity = Severity.LOW
        if inertia < np.var(scaled_data) * 0.5:
            severity = Severity.MEDIUM
            
        # Generate recommendations
        recommendations = []
        largest_cluster = max(cluster_info.keys(), key=lambda k: cluster_info[k]['size'])
        recommendations.append(f"Identified {n_clusters} distinct operational patterns. Largest pattern represents {cluster_info[largest_cluster]['size']} time periods.")
        
        result = AnalysisResult(
            analysis_id=str(uuid4()),
            analysis_type=AnalysisType.CLUSTERING,
            title="Operational Pattern Clustering",
            description=f"Identified {n_clusters} distinct operational patterns in system behavior",
            severity=severity,
            confidence=0.75,
            data={
                'n_clusters': n_clusters,
                'cluster_info': cluster_info,
                'inertia': inertia
            },
            recommendations=recommendations,
            tags={'n_clusters': str(n_clusters)}
        )
        results.append(result)
        
        return results
        
    async def _performance_analysis(self, df: pd.DataFrame, 
                                  metrics: List[MetricData]) -> List[AnalysisResult]:
        """Analyze performance metrics and identify issues"""
        results = []
        
        # Focus on performance-related metrics
        perf_df = df[df['metric_type'] == MetricType.PERFORMANCE.value]
        
        if perf_df.empty:
            return results
            
        for metric_name in perf_df['name'].unique():
            metric_data = perf_df[perf_df['name'] == metric_name]['value']
            
            if len(metric_data) < 5:
                continue
                
            # Calculate performance statistics
            mean_value = metric_data.mean()
            p95_value = metric_data.quantile(0.95)
            p99_value = metric_data.quantile(0.99)
            
            # Define performance thresholds (example for response time)
            if 'response_time' in metric_name.lower() or 'latency' in metric_name.lower():
                # Response time thresholds in milliseconds
                good_threshold = 100
                acceptable_threshold = 500
                poor_threshold = 1000
                
                severity = Severity.LOW
                if p95_value > acceptable_threshold:
                    severity = Severity.MEDIUM
                if p95_value > poor_threshold:
                    severity = Severity.HIGH
                    
                recommendations = []
                if p95_value > good_threshold:
                    recommendations.append(f"P95 {metric_name} is {p95_value:.1f}ms. Consider performance optimization.")
                if p99_value > poor_threshold:
                    recommendations.append(f"P99 {metric_name} is {p99_value:.1f}ms. Critical performance issue detected.")
                    
                result = AnalysisResult(
                    analysis_id=str(uuid4()),
                    analysis_type=AnalysisType.PERFORMANCE,
                    title=f"Performance Analysis: {metric_name}",
                    description=f"Performance analysis for {metric_name} - P95: {p95_value:.1f}ms",
                    severity=severity,
                    confidence=0.90,
                    data={
                        'mean': mean_value,
                        'p95': p95_value,
                        'p99': p99_value,
                        'sample_count': len(metric_data)
                    },
                    recommendations=recommendations,
                    tags={'metric_name': metric_name, 'metric_type': 'performance'}
                )
                results.append(result)
                
        return results
        
    async def _capacity_planning_analysis(self, df: pd.DataFrame, 
                                        metrics: List[MetricData]) -> List[AnalysisResult]:
        """Perform capacity planning analysis"""
        results = []
        
        # Focus on resource usage metrics
        resource_df = df[df['metric_type'] == MetricType.RESOURCE_USAGE.value]
        
        if resource_df.empty:
            return results
            
        for metric_name in resource_df['name'].unique():
            if 'percentage' not in metric_name:
                continue
                
            metric_data = resource_df[resource_df['name'] == metric_name]['value']
            
            if len(metric_data) < 10:
                continue
                
            # Calculate capacity metrics
            current_usage = metric_data.mean()
            peak_usage = metric_data.max()
            p95_usage = metric_data.quantile(0.95)
            
            # Capacity planning thresholds
            warning_threshold = 70.0
            critical_threshold = 85.0
            
            severity = Severity.LOW
            if p95_usage > warning_threshold:
                severity = Severity.MEDIUM
            if p95_usage > critical_threshold:
                severity = Severity.HIGH
                
            # Generate recommendations
            recommendations = []
            if p95_usage > warning_threshold:
                headroom = 100 - p95_usage
                recommendations.append(f"Resource utilization approaching capacity. Only {headroom:.1f}% headroom remaining.")
            if peak_usage > critical_threshold:
                recommendations.append(f"Peak usage of {peak_usage:.1f}% detected. Consider scaling up resources.")
                
            # Estimate time to capacity based on trend
            if len(metric_data) > 20:
                x = np.arange(len(metric_data))
                slope, _, _, _, _ = stats.linregress(x, metric_data.values)
                
                if slope > 0:
                    # Estimate days until 90% capacity
                    days_to_90_percent = (90 - current_usage) / (slope * 24 * 12)  # Assuming 5-minute intervals
                    if days_to_90_percent > 0 and days_to_90_percent < 90:
                        recommendations.append(f"At current growth rate, 90% capacity will be reached in approximately {days_to_90_percent:.0f} days.")
                        
            result = AnalysisResult(
                analysis_id=str(uuid4()),
                analysis_type=AnalysisType.CAPACITY_PLANNING,
                title=f"Capacity Planning: {metric_name}",
                description=f"Capacity analysis for {metric_name} - Current: {current_usage:.1f}%, P95: {p95_usage:.1f}%",
                severity=severity,
                confidence=0.85,
                data={
                    'current_usage': current_usage,
                    'peak_usage': peak_usage,
                    'p95_usage': p95_usage,
                    'warning_threshold': warning_threshold,
                    'critical_threshold': critical_threshold
                },
                recommendations=recommendations,
                tags={'metric_name': metric_name, 'resource_type': metric_name.replace('_usage_percentage', '')}
            )
            results.append(result)
            
        return results
        
    def _metrics_to_dataframe(self, metrics: List[MetricData]) -> pd.DataFrame:
        """Convert metrics list to pandas DataFrame for analysis"""
        data = []
        for metric in metrics:
            data.append({
                'timestamp': metric.timestamp,
                'name': metric.name,
                'value': metric.value,
                'metric_type': metric.metric_type.value,
                'unit': metric.unit.value,
                'source': metric.source,
                **metric.tags
            })
        return pd.DataFrame(data)
        
    async def get_analysis_summary(self, time_window: Optional[timedelta] = None) -> Dict[str, Any]:
        """Get a summary of recent analysis results"""
        if time_window:
            cutoff_time = datetime.utcnow() - time_window
            recent_results = [r for r in self.analysis_history if r.timestamp > cutoff_time]
        else:
            recent_results = self.analysis_history[-100:]  # Last 100 results
            
        summary = {
            'total_analyses': len(recent_results),
            'by_type': {},
            'by_severity': {},
            'high_confidence_results': [],
            'critical_issues': []
        }
        
        for result in recent_results:
            # Count by type
            analysis_type = result.analysis_type.value
            summary['by_type'][analysis_type] = summary['by_type'].get(analysis_type, 0) + 1
            
            # Count by severity
            severity = result.severity.value
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
            
            # High confidence results
            if result.confidence > 0.9:
                summary['high_confidence_results'].append(result.to_dict())
                
            # Critical issues
            if result.severity == Severity.CRITICAL:
                summary['critical_issues'].append(result.to_dict())
                
        return summary


# Example usage
async def example_analytics():
    """Example of using the analytics engine"""
    from .metrics_collector import MetricsCollector, MetricType, MetricUnit
    
    # Create some sample metrics
    metrics = []
    base_time = datetime.utcnow() - timedelta(hours=1)
    
    for i in range(60):  # 60 data points over 1 hour
        timestamp = base_time + timedelta(minutes=i)
        
        # Simulate response time with trend and anomalies
        base_response_time = 100 + i * 0.5  # Slight upward trend
        if i in [20, 45]:  # Add some anomalies
            response_time = base_response_time * 3
        else:
            response_time = base_response_time + np.random.normal(0, 10)
            
        metrics.append(MetricData(
            metric_id=str(uuid4()),
            metric_type=MetricType.PERFORMANCE,
            name="api_response_time",
            value=max(0, response_time),
            unit=MetricUnit.MILLISECONDS,
            timestamp=timestamp
        ))
        
        # Simulate CPU usage
        cpu_usage = 50 + 20 * np.sin(i * 0.1) + np.random.normal(0, 5)
        metrics.append(MetricData(
            metric_id=str(uuid4()),
            metric_type=MetricType.RESOURCE_USAGE,
            name="cpu_usage_percentage",
            value=max(0, min(100, cpu_usage)),
            unit=MetricUnit.PERCENTAGE,
            timestamp=timestamp
        ))
        
    # Create analytics engine and analyze
    engine = AnalyticsEngine()
    
    analysis_types = [
        AnalysisType.STATISTICAL,
        AnalysisType.TREND,
        AnalysisType.ANOMALY,
        AnalysisType.PERFORMANCE,
        AnalysisType.CAPACITY_PLANNING
    ]
    
    results = await engine.analyze_metrics(metrics, analysis_types)
    
    print(f"Generated {len(results)} analysis results:")
    for result in results:
        print(f"- {result.title} ({result.severity.value}): {result.description}")
        if result.recommendations:
            for rec in result.recommendations:
                print(f"  → {rec}")
        print()
        
    # Get summary
    summary = await engine.get_analysis_summary()
    print("Analysis Summary:")
    print(f"Total analyses: {summary['total_analyses']}")
    print(f"By type: {summary['by_type']}")
    print(f"By severity: {summary['by_severity']}")


if __name__ == "__main__":
    asyncio.run(example_analytics())

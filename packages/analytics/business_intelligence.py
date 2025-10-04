"""
Business Intelligence Module

This module provides strategic business insights, KPI tracking, and executive reporting
capabilities for the AI-Native PaaS Platform.
"""

import asyncio
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from uuid import UUID, uuid4
import logging

from .metrics_collector import MetricData, MetricType
from .analytics_engine import AnalysisResult, AnalysisType

logger = logging.getLogger(__name__)


class InsightType(Enum):
    """Types of business insights"""
    REVENUE = "revenue"
    COST_OPTIMIZATION = "cost_optimization"
    CUSTOMER_BEHAVIOR = "customer_behavior"
    OPERATIONAL_EFFICIENCY = "operational_efficiency"
    GROWTH_OPPORTUNITY = "growth_opportunity"
    RISK_ASSESSMENT = "risk_assessment"
    COMPETITIVE_ADVANTAGE = "competitive_advantage"
    RESOURCE_UTILIZATION = "resource_utilization"


class BusinessMetric(Enum):
    """Key business metrics"""
    MONTHLY_RECURRING_REVENUE = "mrr"
    CUSTOMER_ACQUISITION_COST = "cac"
    CUSTOMER_LIFETIME_VALUE = "clv"
    CHURN_RATE = "churn_rate"
    GROSS_MARGIN = "gross_margin"
    OPERATIONAL_COST = "operational_cost"
    ACTIVE_USERS = "active_users"
    DEPLOYMENT_SUCCESS_RATE = "deployment_success_rate"
    PLATFORM_UPTIME = "platform_uptime"
    COST_PER_DEPLOYMENT = "cost_per_deployment"


@dataclass
class BusinessInsight:
    """Business intelligence insight"""
    insight_id: str
    insight_type: InsightType
    title: str
    description: str
    impact_score: float  # 0.0 to 10.0
    confidence: float    # 0.0 to 1.0
    timestamp: datetime = field(default_factory=datetime.utcnow)
    kpis_affected: List[BusinessMetric] = field(default_factory=list)
    financial_impact: Optional[float] = None  # Dollar amount
    recommendations: List[str] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)
    tags: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert insight to dictionary"""
        return {
            'insight_id': self.insight_id,
            'insight_type': self.insight_type.value,
            'title': self.title,
            'description': self.description,
            'impact_score': self.impact_score,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat(),
            'kpis_affected': [kpi.value for kpi in self.kpis_affected],
            'financial_impact': self.financial_impact,
            'recommendations': self.recommendations,
            'data': self.data,
            'tags': self.tags
        }


@dataclass
class KPISnapshot:
    """Snapshot of key performance indicators"""
    timestamp: datetime
    metrics: Dict[BusinessMetric, float]
    period: str  # "daily", "weekly", "monthly"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'metrics': {k.value: v for k, v in self.metrics.items()},
            'period': self.period
        }


class BusinessIntelligence:
    """
    Business Intelligence engine for strategic insights and KPI tracking
    """
    
    def __init__(self):
        self.insights_history: List[BusinessInsight] = []
        self.kpi_snapshots: List[KPISnapshot] = []
        self.business_rules: Dict[str, callable] = {}
        
    async def generate_insights(self, metrics: List[MetricData], 
                              analysis_results: List[AnalysisResult]) -> List[BusinessInsight]:
        """Generate business insights from metrics and analysis results"""
        insights = []
        
        # Revenue insights
        revenue_insights = await self._analyze_revenue_trends(metrics)
        insights.extend(revenue_insights)
        
        # Cost optimization insights
        cost_insights = await self._analyze_cost_optimization(metrics, analysis_results)
        insights.extend(cost_insights)
        
        # Customer behavior insights
        customer_insights = await self._analyze_customer_behavior(metrics)
        insights.extend(customer_insights)
        
        # Operational efficiency insights
        ops_insights = await self._analyze_operational_efficiency(metrics, analysis_results)
        insights.extend(ops_insights)
        
        # Growth opportunity insights
        growth_insights = await self._identify_growth_opportunities(metrics, analysis_results)
        insights.extend(growth_insights)
        
        # Risk assessment insights
        risk_insights = await self._assess_business_risks(analysis_results)
        insights.extend(risk_insights)
        
        # Store insights
        self.insights_history.extend(insights)
        
        return insights
        
    async def _analyze_revenue_trends(self, metrics: List[MetricData]) -> List[BusinessInsight]:
        """Analyze revenue trends and generate insights"""
        insights = []
        
        # Filter business metrics
        business_metrics = [m for m in metrics if m.metric_type == MetricType.BUSINESS]
        revenue_metrics = [m for m in business_metrics if 'revenue' in m.name.lower()]
        
        if not revenue_metrics:
            return insights
            
        # Calculate revenue growth
        current_period_revenue = sum(m.value for m in revenue_metrics[-30:])  # Last 30 data points
        previous_period_revenue = sum(m.value for m in revenue_metrics[-60:-30])  # Previous 30
        
        if previous_period_revenue > 0:
            growth_rate = ((current_period_revenue - previous_period_revenue) / previous_period_revenue) * 100
            
            if abs(growth_rate) > 5:  # Significant change
                insight_type = InsightType.REVENUE
                impact_score = min(abs(growth_rate) / 10, 10.0)
                
                if growth_rate > 0:
                    title = f"Revenue Growth Acceleration: +{growth_rate:.1f}%"
                    description = f"Revenue has increased by {growth_rate:.1f}% compared to the previous period"
                    recommendations = [
                        "Analyze successful customer segments for expansion opportunities",
                        "Invest in marketing channels driving growth",
                        "Consider scaling infrastructure to support growth"
                    ]
                else:
                    title = f"Revenue Decline Alert: {growth_rate:.1f}%"
                    description = f"Revenue has decreased by {abs(growth_rate):.1f}% compared to the previous period"
                    recommendations = [
                        "Investigate customer churn causes",
                        "Review pricing strategy and competitive positioning",
                        "Implement customer retention programs"
                    ]
                    
                insight = BusinessInsight(
                    insight_id=str(uuid4()),
                    insight_type=insight_type,
                    title=title,
                    description=description,
                    impact_score=impact_score,
                    confidence=0.85,
                    kpis_affected=[BusinessMetric.MONTHLY_RECURRING_REVENUE],
                    financial_impact=current_period_revenue - previous_period_revenue,
                    recommendations=recommendations,
                    data={
                        'current_revenue': current_period_revenue,
                        'previous_revenue': previous_period_revenue,
                        'growth_rate': growth_rate
                    }
                )
                insights.append(insight)
                
        return insights
        
    async def _analyze_cost_optimization(self, metrics: List[MetricData], 
                                       analysis_results: List[AnalysisResult]) -> List[BusinessInsight]:
        """Analyze cost optimization opportunities"""
        insights = []
        
        # Filter cost metrics
        cost_metrics = [m for m in metrics if m.metric_type == MetricType.COST]
        
        if not cost_metrics:
            return insights
            
        # Calculate total costs by service
        service_costs = {}
        for metric in cost_metrics:
            service = metric.tags.get('service', 'unknown')
            service_costs[service] = service_costs.get(service, 0) + metric.value
            
        # Identify highest cost services
        if service_costs:
            total_cost = sum(service_costs.values())
            sorted_services = sorted(service_costs.items(), key=lambda x: x[1], reverse=True)
            
            # Check for cost optimization opportunities
            for service, cost in sorted_services[:3]:  # Top 3 cost centers
                cost_percentage = (cost / total_cost) * 100
                
                if cost_percentage > 30:  # Service consuming >30% of budget
                    # Look for related analysis results
                    related_analyses = [
                        r for r in analysis_results 
                        if r.analysis_type == AnalysisType.CAPACITY_PLANNING and 
                        service in str(r.data)
                    ]
                    
                    recommendations = [
                        f"Review {service} resource allocation for optimization opportunities",
                        f"Consider reserved instances or spot pricing for {service}",
                        f"Implement automated scaling policies for {service}"
                    ]
                    
                    if related_analyses:
                        recommendations.append(f"Capacity analysis suggests potential for {service} optimization")
                        
                    insight = BusinessInsight(
                        insight_id=str(uuid4()),
                        insight_type=InsightType.COST_OPTIMIZATION,
                        title=f"High Cost Center Identified: {service}",
                        description=f"{service} represents {cost_percentage:.1f}% of total infrastructure costs",
                        impact_score=min(cost_percentage / 10, 10.0),
                        confidence=0.90,
                        kpis_affected=[BusinessMetric.OPERATIONAL_COST, BusinessMetric.GROSS_MARGIN],
                        financial_impact=cost * 0.2,  # Potential 20% savings
                        recommendations=recommendations,
                        data={
                            'service': service,
                            'cost': cost,
                            'cost_percentage': cost_percentage,
                            'total_cost': total_cost
                        },
                        tags={'service': service}
                    )
                    insights.append(insight)
                    
        return insights
        
    async def _analyze_customer_behavior(self, metrics: List[MetricData]) -> List[BusinessInsight]:
        """Analyze customer behavior patterns"""
        insights = []
        
        # Filter user behavior metrics
        user_metrics = [m for m in metrics if m.metric_type == MetricType.USER_BEHAVIOR]
        
        if not user_metrics:
            return insights
            
        # Analyze active users trend
        active_user_metrics = [m for m in user_metrics if 'active_users' in m.name]
        
        if len(active_user_metrics) > 10:
            recent_users = sum(m.value for m in active_user_metrics[-7:]) / 7  # Last week average
            previous_users = sum(m.value for m in active_user_metrics[-14:-7]) / 7  # Previous week
            
            if previous_users > 0:
                user_growth = ((recent_users - previous_users) / previous_users) * 100
                
                if abs(user_growth) > 10:  # Significant change
                    if user_growth > 0:
                        title = f"User Engagement Surge: +{user_growth:.1f}%"
                        description = f"Active users increased by {user_growth:.1f}% week-over-week"
                        recommendations = [
                            "Analyze user acquisition channels driving growth",
                            "Ensure platform capacity can handle increased load",
                            "Implement user onboarding optimization"
                        ]
                    else:
                        title = f"User Engagement Decline: {user_growth:.1f}%"
                        description = f"Active users decreased by {abs(user_growth):.1f}% week-over-week"
                        recommendations = [
                            "Investigate user experience issues",
                            "Implement user retention campaigns",
                            "Review recent platform changes for negative impact"
                        ]
                        
                    insight = BusinessInsight(
                        insight_id=str(uuid4()),
                        insight_type=InsightType.CUSTOMER_BEHAVIOR,
                        title=title,
                        description=description,
                        impact_score=min(abs(user_growth) / 5, 10.0),
                        confidence=0.80,
                        kpis_affected=[BusinessMetric.ACTIVE_USERS, BusinessMetric.CHURN_RATE],
                        recommendations=recommendations,
                        data={
                            'recent_users': recent_users,
                            'previous_users': previous_users,
                            'growth_rate': user_growth
                        }
                    )
                    insights.append(insight)
                    
        return insights
        
    async def _analyze_operational_efficiency(self, metrics: List[MetricData], 
                                            analysis_results: List[AnalysisResult]) -> List[BusinessInsight]:
        """Analyze operational efficiency metrics"""
        insights = []
        
        # Analyze deployment success rates
        deployment_metrics = [m for m in metrics if 'deployment' in m.name and 'success' in m.name]
        
        if deployment_metrics:
            success_rate = sum(m.value for m in deployment_metrics[-20:]) / len(deployment_metrics[-20:])
            
            if success_rate < 95:  # Below target
                insight = BusinessInsight(
                    insight_id=str(uuid4()),
                    insight_type=InsightType.OPERATIONAL_EFFICIENCY,
                    title=f"Deployment Success Rate Below Target: {success_rate:.1f}%",
                    description=f"Current deployment success rate is {success_rate:.1f}%, below the 95% target",
                    impact_score=8.0,
                    confidence=0.90,
                    kpis_affected=[BusinessMetric.DEPLOYMENT_SUCCESS_RATE],
                    recommendations=[
                        "Review deployment pipeline for failure points",
                        "Implement additional automated testing",
                        "Enhance rollback mechanisms"
                    ],
                    data={'success_rate': success_rate, 'target': 95.0}
                )
                insights.append(insight)
                
        # Analyze platform uptime
        uptime_metrics = [m for m in metrics if 'uptime' in m.name]
        
        if uptime_metrics:
            avg_uptime = sum(m.value for m in uptime_metrics[-30:]) / len(uptime_metrics[-30:])
            
            if avg_uptime < 99.9:  # Below SLA
                insight = BusinessInsight(
                    insight_id=str(uuid4()),
                    insight_type=InsightType.OPERATIONAL_EFFICIENCY,
                    title=f"Platform Uptime Below SLA: {avg_uptime:.2f}%",
                    description=f"Platform uptime is {avg_uptime:.2f}%, below the 99.9% SLA target",
                    impact_score=9.0,
                    confidence=0.95,
                    kpis_affected=[BusinessMetric.PLATFORM_UPTIME],
                    recommendations=[
                        "Investigate root causes of downtime",
                        "Implement additional redundancy",
                        "Enhance monitoring and alerting"
                    ],
                    data={'uptime': avg_uptime, 'sla_target': 99.9}
                )
                insights.append(insight)
                
        return insights
        
    async def _identify_growth_opportunities(self, metrics: List[MetricData], 
                                           analysis_results: List[AnalysisResult]) -> List[BusinessInsight]:
        """Identify growth opportunities"""
        insights = []
        
        # Look for positive trends that indicate growth opportunities
        trend_analyses = [r for r in analysis_results if r.analysis_type == AnalysisType.TREND]
        
        for analysis in trend_analyses:
            if analysis.data.get('trend_direction') == 'increasing':
                trend_strength = analysis.data.get('trend_strength', 0)
                
                if trend_strength > 0.7:  # Strong upward trend
                    metric_name = analysis.tags.get('metric_name', 'unknown')
                    
                    if 'user' in metric_name or 'request' in metric_name:
                        insight = BusinessInsight(
                            insight_id=str(uuid4()),
                            insight_type=InsightType.GROWTH_OPPORTUNITY,
                            title=f"Growth Opportunity: {metric_name} Trending Up",
                            description=f"Strong upward trend detected in {metric_name} with {trend_strength:.1%} correlation",
                            impact_score=7.0,
                            confidence=trend_strength,
                            kpis_affected=[BusinessMetric.ACTIVE_USERS, BusinessMetric.MONTHLY_RECURRING_REVENUE],
                            recommendations=[
                                f"Capitalize on growing demand in {metric_name}",
                                "Consider expanding capacity proactively",
                                "Investigate market factors driving growth"
                            ],
                            data={
                                'metric_name': metric_name,
                                'trend_strength': trend_strength,
                                'trend_direction': 'increasing'
                            }
                        )
                        insights.append(insight)
                        
        return insights
        
    async def _assess_business_risks(self, analysis_results: List[AnalysisResult]) -> List[BusinessInsight]:
        """Assess business risks from analysis results"""
        insights = []
        
        # Look for high-severity issues that pose business risks
        high_severity_results = [
            r for r in analysis_results 
            if r.severity.value in ['high', 'critical']
        ]
        
        for result in high_severity_results:
            if result.analysis_type == AnalysisType.ANOMALY:
                insight = BusinessInsight(
                    insight_id=str(uuid4()),
                    insight_type=InsightType.RISK_ASSESSMENT,
                    title=f"Business Risk: {result.title}",
                    description=f"Critical anomaly detected that may impact business operations: {result.description}",
                    impact_score=8.0,
                    confidence=result.confidence,
                    kpis_affected=[BusinessMetric.PLATFORM_UPTIME, BusinessMetric.OPERATIONAL_COST],
                    recommendations=[
                        "Immediate investigation required",
                        "Implement additional monitoring",
                        "Prepare contingency plans"
                    ] + result.recommendations,
                    data=result.data
                )
                insights.append(insight)
                
        return insights
        
    async def calculate_kpis(self, metrics: List[MetricData]) -> KPISnapshot:
        """Calculate current KPI values"""
        kpi_values = {}
        
        # Calculate MRR (Monthly Recurring Revenue)
        revenue_metrics = [m for m in metrics if 'revenue' in m.name.lower()]
        if revenue_metrics:
            monthly_revenue = sum(m.value for m in revenue_metrics[-30:])  # Last 30 days
            kpi_values[BusinessMetric.MONTHLY_RECURRING_REVENUE] = monthly_revenue
            
        # Calculate Active Users
        user_metrics = [m for m in metrics if 'active_users' in m.name]
        if user_metrics:
            active_users = user_metrics[-1].value if user_metrics else 0
            kpi_values[BusinessMetric.ACTIVE_USERS] = active_users
            
        # Calculate Platform Uptime
        uptime_metrics = [m for m in metrics if 'uptime' in m.name]
        if uptime_metrics:
            avg_uptime = sum(m.value for m in uptime_metrics[-7:]) / len(uptime_metrics[-7:])
            kpi_values[BusinessMetric.PLATFORM_UPTIME] = avg_uptime
            
        # Calculate Deployment Success Rate
        deployment_metrics = [m for m in metrics if 'deployment' in m.name and 'success' in m.name]
        if deployment_metrics:
            success_rate = sum(m.value for m in deployment_metrics[-20:]) / len(deployment_metrics[-20:])
            kpi_values[BusinessMetric.DEPLOYMENT_SUCCESS_RATE] = success_rate
            
        # Calculate Operational Cost
        cost_metrics = [m for m in metrics if m.metric_type == MetricType.COST]
        if cost_metrics:
            total_cost = sum(m.value for m in cost_metrics[-30:])  # Last 30 days
            kpi_values[BusinessMetric.OPERATIONAL_COST] = total_cost
            
        snapshot = KPISnapshot(
            timestamp=datetime.utcnow(),
            metrics=kpi_values,
            period="daily"
        )
        
        self.kpi_snapshots.append(snapshot)
        return snapshot
        
    async def get_executive_summary(self, time_window: timedelta = timedelta(days=7)) -> Dict[str, Any]:
        """Generate executive summary of business insights"""
        cutoff_time = datetime.utcnow() - time_window
        recent_insights = [i for i in self.insights_history if i.timestamp > cutoff_time]
        
        # Categorize insights
        summary = {
            'period': f"Last {time_window.days} days",
            'total_insights': len(recent_insights),
            'high_impact_insights': [],
            'financial_impact': 0,
            'key_recommendations': [],
            'risk_alerts': [],
            'growth_opportunities': []
        }
        
        for insight in recent_insights:
            if insight.impact_score >= 7.0:
                summary['high_impact_insights'].append(insight.to_dict())
                
            if insight.financial_impact:
                summary['financial_impact'] += insight.financial_impact
                
            if insight.insight_type == InsightType.RISK_ASSESSMENT:
                summary['risk_alerts'].append(insight.to_dict())
                
            if insight.insight_type == InsightType.GROWTH_OPPORTUNITY:
                summary['growth_opportunities'].append(insight.to_dict())
                
            # Collect top recommendations
            for rec in insight.recommendations:
                if rec not in summary['key_recommendations']:
                    summary['key_recommendations'].append(rec)
                    
        # Limit recommendations to top 10
        summary['key_recommendations'] = summary['key_recommendations'][:10]
        
        return summary


# Example usage
async def example_business_intelligence():
    """Example of using business intelligence"""
    from .metrics_collector import MetricData, MetricType, MetricUnit
    
    # Create sample business metrics
    metrics = []
    base_time = datetime.utcnow() - timedelta(days=30)
    
    for i in range(30):  # 30 days of data
        timestamp = base_time + timedelta(days=i)
        
        # Revenue metrics with growth trend
        revenue = 10000 + i * 100 + (i * 50 if i > 15 else 0)  # Acceleration after day 15
        metrics.append(MetricData(
            metric_id=str(uuid4()),
            metric_type=MetricType.BUSINESS,
            name="daily_revenue",
            value=revenue,
            unit=MetricUnit.DOLLARS,
            timestamp=timestamp
        ))
        
        # Active users with some volatility
        users = 1000 + i * 10 + (50 if i > 20 else 0)
        metrics.append(MetricData(
            metric_id=str(uuid4()),
            metric_type=MetricType.USER_BEHAVIOR,
            name="active_users",
            value=users,
            unit=MetricUnit.COUNT,
            timestamp=timestamp
        ))
        
    # Create BI engine and generate insights
    bi = BusinessIntelligence()
    insights = await bi.generate_insights(metrics, [])
    
    print(f"Generated {len(insights)} business insights:")
    for insight in insights:
        print(f"- {insight.title} (Impact: {insight.impact_score}/10)")
        print(f"  {insight.description}")
        if insight.financial_impact:
            print(f"  Financial Impact: ${insight.financial_impact:,.2f}")
        print()
        
    # Calculate KPIs
    kpi_snapshot = await bi.calculate_kpis(metrics)
    print("Current KPIs:")
    for kpi, value in kpi_snapshot.metrics.items():
        print(f"- {kpi.value}: {value:,.2f}")
        
    # Get executive summary
    summary = await bi.get_executive_summary()
    print(f"\nExecutive Summary ({summary['period']}):")
    print(f"Total Insights: {summary['total_insights']}")
    print(f"Financial Impact: ${summary['financial_impact']:,.2f}")
    print(f"High Impact Insights: {len(summary['high_impact_insights'])}")


if __name__ == "__main__":
    asyncio.run(example_business_intelligence())

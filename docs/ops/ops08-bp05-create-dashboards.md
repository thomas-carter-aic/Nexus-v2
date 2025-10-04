[Documentation](/index.html)[Framework](welcome.html)

[Implementation guidance](#implementation-guidance)[Resources](#resources)

# OPS08-BP05 Create dashboards

Dashboards are the human-centric view into the telemetry data of your workloads. While they provide a vital visual interface, they should not replace alerting mechanisms, but complement them. When crafted with care, not only can they offer rapid insights into system health and performance, but they can also present stakeholders with real-time information on business outcomes and the impact of issues.

**Desired outcome:**

Clear, actionable insights into system and business health using visual representations.

**Common anti-patterns:**

* Overcomplicating dashboards with too many metrics.

* Relying on dashboards without alerts for anomaly detection.

* Not updating dashboards as workloads evolve.

**Benefits of this best practice:**

* Immediate visibility into critical system metrics and KPIs.

* Enhanced stakeholder communication and understanding.

* Rapid insight into the impact of operational issues.

**Level of risk if this best practice isn't established:** Medium

## Implementation guidance

**Business-centric dashboards**

Dashboards tailored to business KPIs engage a wider array of stakeholders. While these individuals might not be interested in system metrics, they are keen on understanding the business implications of these numbers. A business-centric dashboard ensures that all technical and operational metrics being monitored and analyzed are in sync with overarching business goals. This alignment provides clarity, ensuring everyone is on the same page regarding what's essential and what's not. Additionally, dashboards that highlight business KPIs tend to be more actionable. Stakeholders can quickly understand the health of operations, areas that need attention, and the potential impact on business outcomes.

With this in mind, when creating your dashboards, ensure that there's a balance between technical metrics and business KPIs. Both are vital, but they cater to different audiences. Ideally, you should have dashboards that provide a holistic view of the system's health and performance while also emphasizing key business outcomes and their implications.

Amazon CloudWatch Dashboards are customizable home pages in the CloudWatch console that you can use to monitor your resources in a single view, even those resources that are spread across different AWS Regions and accounts.

### Implementation steps

1. **Create a basic dashboard:** [Create a new dashboard in CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create_dashboard.html), giving it a descriptive name.

2. **Use Markdown widgets:** Before diving into the metrics, [use Markdown widgets](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/add_remove_text_dashboard.html) to add textual context at the top of your dashboard. This should explain what the dashboard covers, the significance of the represented metrics, and can also contain links to other dashboards and troubleshooting tools.

3. **Create dashboard variables:** [Incorporate dashboard variables](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_dashboard_variables.html) where appropriate to allow for dynamic and flexible dashboard views.

4. **Create metrics widgets:** [Add metric widgets](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create-and-work-with-widgets.html) to visualize various metrics your application emits, tailoring these widgets to effectively represent system health and business outcomes.

5. **Log Insights queries:** Utilize [CloudWatch Log Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_ExportQueryResults.html) to derive actionable metrics from your logs and display these insights on your dashboard.

6. **Set up alarms:** Integrate [CloudWatch Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/add_remove_alarm_dashboard.html) into your dashboard for a quick view of any metrics breaching their thresholds.

7. **Use Contributor Insights:** Incorporate [CloudWatch Contributor Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights-ViewReports.html) to analyze high-cardinality fields and get a clearer understanding of your resource's top contributors.

8. **Design custom widgets:** For specific needs not met by standard widgets, consider creating [custom widgets](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/add_custom_widget_dashboard.html). These can pull from various data sources or represent data in unique ways.

9. **Use AWS Health:** AWS Health is the authoritative source of information about the health of your AWS Cloud resources. Use [AWS Health Dashboard](https://health.aws.amazon.com/health/status) out of the box, or use AWS Health data in your own dashboards and tools so you have the right information available to make informed decisions.

10. **Iterate and refine:** As your application evolves, regularly revisit your dashboard to ensure its relevance.

## Resources

**Related best practices:**

* [OPS04-BP01 Identify key performance indicators](./ops_observability_identify_kpis.html)

* [OPS08-BP01 Analyze workload metrics](./ops_workload_observability_analyze_workload_metrics.html)

* [OPS08-BP02 Analyze workload logs](./ops_workload_observability_analyze_workload_logs.html)

* [OPS08-BP03 Analyze workload traces](./ops_workload_observability_analyze_workload_traces.html)

* [OPS08-BP04 Create actionable alerts](./ops_workload_observability_create_alerts.html)

**Related documents:**

* [Building Dashboards for Operational Visibility](https://aws.amazon.com/builders-library/building-dashboards-for-operational-visibility/)

* [Using Amazon CloudWatch Dashboards](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Dashboards.html)

**Related videos:**

* [Create Cross Account & Cross Region CloudWatch Dashboards](https://www.youtube.com/watch?v=eIUZdaqColg)

* [AWS re:Invent 2021 - Gain enterprise visibility with AWS Cloud operation dashboards)](https://www.youtube.com/watch?v=NfMpYiGwPGo)

**Related examples:**

* [One Observability Workshop](https://catalog.workshops.aws/observability/en-US/intro)

* [Application Monitoring with Amazon CloudWatch](https://aws.amazon.com/solutions/implementations/application-monitoring-with-cloudwatch/)

* [AWS Health Events Intelligence Dashboards and Insights](https://aws.amazon.com/blogs/mt/aws-health-events-intelligence-dashboards-insights/)

* [Visualize AWS Health events using Amazon Managed Grafana](https://aws.amazon.com/blogs/mt/visualize-aws-health-events-using-amazon-managed-grafana/)


[Document Conventions](/general/latest/gr/docconventions.html)

OPS08-BP04 Create actionable alerts

OPS 9. How do you understand the health of your operations?

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.</awsdocs-view></awsui-app-layout>
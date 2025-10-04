[Documentation](/index.html)[Framework](welcome.html)

[Implementation guidance](#implementation-guidance)[Resources](#resources)

# OPS04-BP02 Implement application telemetry

Application telemetry serves as the foundation for observability of your workload. It's crucial to emit telemetry that offers actionable insights into the state of your application and the achievement of both technical and business outcomes. From troubleshooting to measuring the impact of a new feature or ensuring alignment with business key performance indicators (KPIs), application telemetry informs the way you build, operate, and evolve your workload.

Metrics, logs, and traces form the three primary pillars of observability. These serve as diagnostic tools that describe the state of your application. Over time, they assist in creating baselines and identifying anomalies. However, to ensure alignment between monitoring activities and business objectives, it's pivotal to define and monitor KPIs. Business KPIs often make it easier to identify issues compared to technical metrics alone.

Other telemetry types, like real user monitoring (RUM) and synthetic transactions, complement these primary data sources. RUM offers insights into real-time user interactions, whereas synthetic transactions simulate potential user behaviors, helping detect bottlenecks before real users encounter them.

**Desired outcome:** Derive actionable insights into the performance of your workload. These insights allow you to make proactive decisions about performance optimization, achieve increased workload stability, streamline CI/CD processes, and utilize resources effectively.

**Common anti-patterns:**

* **Incomplete observability:** Neglecting to incorporate observability at every layer of the workload, resulting in blind spots that can obscure vital system performance and behavior insights.

* **Fragmented data view:** When data is scattered across multiple tools and systems, it becomes challenging to maintain a holistic view of your workload's health and performance.

* **User-reported issues:** A sign that proactive issue detection through telemetry and business KPI monitoring is lacking.

**Benefits of establishing this best practice:**

* **Informed decision-making:** With insights from telemetry and business KPIs, you can make data-driven decisions.

* **Improved operational efficiency:** Data-driven resource utilization leads to cost-effectiveness.

* **Enhanced workload stability:** Faster detection and resolution of issues leading to improved uptime.

* **Streamlined CI/CD processes:** Insights from telemetry data facilitate refinement of processes and reliable code delivery.

**Level of risk exposed if this best practice is not established:** High

## Implementation guidance

To implement application telemetry for your workload, use AWS services like [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) and [AWS X-Ray](https://aws.amazon.com/xray/). Amazon CloudWatch provides a comprehensive suite of monitoring tools, allowing you to observe your resources and applications in AWS and on-premises environments. It collects, tracks, and analyzes metrics, consolidates and monitors log data, and responds to changes in your resources, enhancing your understanding of how your workload operates. In tandem, AWS X-Ray lets you trace, analyze, and debug your applications, giving you a deep understanding of your workload's behavior. With features like service maps, latency distributions, and trace timelines, AWS X-Ray provides insights into your workload's performance and the bottlenecks affecting it.

### Implementation steps

1. **Identify what data to collect:** Ascertain the essential metrics, logs, and traces that would offer substantial insights into your workload's health, performance, and behavior.

2. **Deploy the [CloudWatch agent](https://aws.amazon.com/cloudwatch/):** The CloudWatch agent is instrumental in procuring system and application metrics and logs from your workload and its underlying infrastructure. The CloudWatch agent can also be used to collect OpenTelemetry or X-Ray traces and send them to X-Ray.

3. **Implement anomaly detection for logs and metrics:** Use [CloudWatch Logs anomaly detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/LogsAnomalyDetection.html) and [CloudWatch Metrics anomaly detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) to automatically identify unusual activities in your application's operations. These tools use machine learning algorithms to detect and alert on anomalies, which enanhces your monitoring capabilities and speeds up response time to potential disruptions or security threats. Set up these features to proactively manage application health and security.

4. **Secure sensitive log data:** Use [Amazon CloudWatch Logs data protection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html) to mask sensitive information within your logs. This feature helps maintain privacy and compliance through automatic detection and masking of sensitive data before it is accessed. Implement data masking to securely handle and protect sensitive details such as personally identifiable information (PII).

5. **Define and monitor business KPIs:** Establish [custom metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html) that align with your [business outcomes](https://aws-observability.github.io/observability-best-practices/guides/operational/business/monitoring-for-business-outcomes/).

6. **Instrument your application with AWS X-Ray:** In addition to deploying the CloudWatch agent, it's crucial to [instrument your application](https://docs.aws.amazon.com/xray/latest/devguide/xray-instrumenting-your-app.html) to emit trace data. This process can provide further insights into your workload's behavior and performance.

7. **Standardize data collection across your application:** Standardize data collection practices across your entire application. Uniformity aids in correlating and analyzing data, providing a comprehensive view of your application's behavior.

8. **Implement cross-account observability:** Enhance monitoring efficiency across multiple AWS accounts with [Amazon CloudWatch cross-account observability](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html). With this feature, you can consolidate metrics, logs, and alarms from different accounts into a single view, which simplifies management and improves response times for identified issues across your organization's AWS environment.

9. **Analyze and act on the data:** Once data collection and normalization are in place, use [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/features/) for metrics and logs analysis, and [AWS X-Ray](https://aws.amazon.com/xray/features/) for trace analysis. Such analysis can yield crucial insights into your workload's health, performance, and behavior, guiding your decision-making process.

**Level of effort for the implementation plan:** High

## Resources

**Related best practices:**

* [OPS04-BP01 Define workload KPIs](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_observability_identify_kpis.html)

* [OPS04-BP03 Implement user activity telemetry](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_observability_customer_telemetry.html)

* [OPS04-BP04 Implement dependency telemetry](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_observability_dependency_telemetry.html)

* [OPS04-BP05 Implement transaction traceability](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_observability_dist_trace.html)

**Related documents:**

* [AWS Observability Best Practices](https://aws-observability.github.io/observability-best-practices/)

* [CloudWatch User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)

* [AWS X-Ray Developer Guide](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html)

* [Instrumenting distributed systems for operational visibility](https://aws.amazon.com/builders-library/instrumenting-distributed-systems-for-operational-visibility)

* [AWS Observability Skill Builder Course](https://explore.skillbuilder.aws/learn/course/external/view/elearning/14688/aws-observability)

* [What's New with Amazon CloudWatch](https://aws.amazon.com/about-aws/whats-new/management-and-governance/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=general-products%23amazon-cloudwatch)

* [What's new with AWS X-Ray](https://aws.amazon.com/about-aws/whats-new/developer-tools/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=general-products%23aws-x-ray)

**Related videos:**

* [AWS re:Invent 2022 - Observability best practices at Amazon](https://youtu.be/zZPzXEBW4P8)

* [AWS re:Invent 2022 - Developing an observability strategy](https://youtu.be/Ub3ATriFapQ)

**Related examples:**

* [One Observability Workshop](https://catalog.workshops.aws/observability)

* [AWS Solutions Library: Application Monitoring with Amazon CloudWatch](https://aws.amazon.com/solutions/implementations/application-monitoring-with-cloudwatch)


[Document Conventions](/general/latest/gr/docconventions.html)

OPS04-BP01 Identify key performance indicators

OPS04-BP03 Implement user experience telemetry

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.</awsdocs-view></awsui-app-layout>
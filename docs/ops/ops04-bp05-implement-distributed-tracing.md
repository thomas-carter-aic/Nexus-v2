[Documentation](/index.html)[Framework](welcome.html)

[Implementation guidance](#implementation-guidance)[Resources](#resources)

# OPS04-BP05 Implement distributed tracing

Distributed tracing offers a way to monitor and visualize requests as they traverse through various components of a distributed system. By capturing trace data from multiple sources and analyzing it in a unified view, teams can better understand how requests flow, where bottlenecks exist, and where optimization efforts should focus.

**Desired outcome:** Achieve a holistic view of requests flowing through your distributed system, allowing for precise debugging, optimized performance, and improved user experiences.

**Common anti-patterns:**

* Inconsistent instrumentation: Not all services in a distributed system are instrumented for tracing.

* Ignoring latency: Only focusing on errors and not considering the latency or gradual performance degradations.

**Benefits of establishing this best practice:**

* Comprehensive system overview: Visualizing the entire path of requests, from entry to exit.

* Enhanced debugging: Quickly identifying where failures or performance issues occur.

* Improved user experience: Monitoring and optimizing based on actual user data, ensuring the system meets real-world demands.

**Level of risk exposed if this best practice is not established:** High

## Implementation guidance

Begin by identifying all of the elements of your workload that require instrumentation. Once all components are accounted for, leverage tools such as AWS X-Ray and OpenTelemetry to gather trace data for analysis with tools like X-Ray and Amazon CloudWatch ServiceLens Map. Engage in regular reviews with developers, and supplement these discussions with tools like Amazon DevOps Guru, X-Ray Analytics and X-Ray Insights to help uncover deeper findings. Establish alerts from trace data to notify when outcomes, as defined in the workload monitoring plan, are at risk.

### Implementation steps

To implement distributed tracing effectively:

1. **Adopt [AWS X-Ray](https://aws.amazon.com/xray/):** Integrate X-Ray into your application to gain insights into its behavior, understand its performance, and pinpoint bottlenecks. Utilize X-Ray Insights for automatic trace analysis.

2. **Instrument your services:** Verify that every service, from an [AWS Lambda](https://aws.amazon.com/lambda/) function to an [EC2 instance](https://aws.amazon.com/ec2/), sends trace data. The more services you instrument, the clearer the end-to-end view.

3. **Incorporate [CloudWatch Real User Monitoring](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-RUM.html) and [synthetic monitoring](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html):** Integrate Real User Monitoring (RUM) and synthetic monitoring with X-Ray. This allows for capturing real-world user experiences and simulating user interactions to identify potential issues.

4. **Use the [CloudWatch agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html):** The agent can send traces from either X-Ray or OpenTelemetry, enhancing the depth of insights obtained.

5. **Use [Amazon DevOps Guru](https://aws.amazon.com/devops-guru/):** DevOps Guru uses data from X-Ray, CloudWatch, AWS Config, and AWS CloudTrail to provide actionable recommendations.

6. **Analyze traces:** Regularly review the trace data to discern patterns, anomalies, or bottlenecks that might impact your application's performance.

7. **Set up alerts:** Configure alarms in [CloudWatch](https://aws.amazon.com/cloudwatch/) for unusual patterns or extended latencies, allowing proactive issue addressing.

8. **Continuous improvement:** Revisit your tracing strategy as services are added or modified to capture all relevant data points.

**Level of effort for the implementation plan:** Medium

## Resources

**Related best practices:**

* [OPS04-BP01 Identify key performance indicators](./ops_observability_identify_kpis.html)

* [OPS04-BP02 Implement application telemetry](./ops_observability_application_telemetry.html)

* [OPS04-BP03 Implement user experience telemetry](./ops_observability_customer_telemetry.html)

* [OPS04-BP04 Implement dependency telemetry](./ops_observability_dependency_telemetry.html)

**Related documents:**

* [AWS X-Ray Developer Guide](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html)

* [Amazon CloudWatch agent User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html)

* [Amazon DevOps Guru User Guide](https://docs.aws.amazon.com/devops-guru/latest/userguide/welcome.html)

**Related videos:**

* [Use AWS X-Ray Insights](https://www.youtube.com/watch?v=tl8OWHl6jxw)

* [AWS on Air ft. Observability: Amazon CloudWatch and AWS X-Ray](https://www.youtube.com/watch?v=qBDBnPkZ-KI)

**Related examples:**

* [Instrumenting your application for AWS X-Ray](https://aws.amazon.com/xray/latest/devguide/xray-instrumenting-your-app.html)


[Document Conventions](/general/latest/gr/docconventions.html)

OPS04-BP04 Implement dependency telemetry

OPS 5. How do you reduce defects, ease remediation, and improve flow into production?

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.</awsdocs-view></awsui-app-layout>
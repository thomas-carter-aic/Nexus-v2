[Documentation](/index.html)[Framework](welcome.html)

[Implementation guidance](#implementation-guidance)[Resources](#resources)

# OPS10-BP07 Automate responses to events

Automating event responses is key for fast, consistent, and error-free operational handling. Create streamlined processes and use tools to automatically manage and respond to events, minimizing manual interventions and enhancing operational effectiveness.

**Desired outcome:**

* Reduced human errors and faster resolution times through automation.

* Consistent and reliable operational event handling.

* Enhanced operational efficiency and system reliability.

**Common anti-patterns:**

* Manual event handling leads to delays and errors.

* Automation is overlooked in repetitive, critical tasks.

* Repetitive, manual tasks lead to alert fatigue and missing critical issues.

**Benefits of establishing this best practice:**

* Accelerated event responses, reducing system downtime.

* Reliable operations with automated and consistent event handling.

**Level of risk exposed if this best practice is not established:** Medium

## Implementation guidance

Incorporate automation to create efficient operational workflows and minimize manual interventions.

### Implementation steps

1. **Identify automation opportunites:** Determine repetitive tasks for automation, such as issue remediation, ticket enrichment, capacity management, scaling, deployments, and testing.

2. **Identify automation prompts:**

   * Assess and define specific conditions or metrics that initiate automated responses using [Amazon CloudWatch alarm actions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarms-and-actions).

   * Use [Amazon EventBridge](https://aws.amazon.com/eventbridge/) to respond to events in AWS services, custom workloads, and SaaS applications.

   * Consider initiation events such as [specific log entries](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/MonitoringLogData.html), [performance metrics thresholds](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html), or [state changes](https://docs.aws.amazon.com/config/latest/developerguide/remediation.html) in AWS resources.

3. **Implement event-driven automation:**

   * Use AWS Systems Manager Automation runbooks to simplify maintenance, deployment, and remediation tasks.

   * [Creating incidents in Incident Manager](https://docs.aws.amazon.com/incident-manager/latest/userguide/incident-creation.html) automatically gathers and adds details about the involved AWS resources to the incident.

   * Proactively monitor quotas using [Quota Monitor for AWS](https://aws.amazon.com/solutions/implementations/quota-monitor/).

   * Automatically adjust capacity with [AWS Auto Scaling](https://aws.amazon.com/autoscaling/) to maintain availability and performance.

   * Automate development pipelines with [Amazon CodeCatalyst](https://codecatalyst.aws/explore).

   * Smoke test or continually monitor endpoints and APIs [using synthetic monitoring](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html).

4. **Perform risk mitigation through automation:**

   * Implement [automated security responses](https://aws.amazon.com/solutions/implementations/automated-security-response-on-aws/) to swiftly address risks.

   * Use [AWS Systems Manager State Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-state.html) to reduce configuration drift.

   * [Remediate noncompliant resources with AWS Config Rules](https://docs.aws.amazon.com/config/latest/developerguide/remediation.html).

**Level of effort for the implementation plan:** High

## Resources

**Related best practices:**

* [OPS08-BP04 Create actionable alerts](./ops_workload_observability_create_alerts.html)

* [OPS10-BP02 Have a process per alert](./ops_event_response_process_per_alert.html)

**Related documents:**

* [Using Systems Manager Automation runbooks with Incident Manager](https://docs.aws.amazon.com/incident-manager/latest/userguide/tutorials-runbooks.html)

* [Creating incidents in Incident Manager](https://docs.aws.amazon.com/incident-manager/latest/userguide/incident-creation.html)

* [AWS service quotas](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html)

* [Monitor resource usage and send notifications when approaching quotas](https://docs.aws.amazon.com/solutions/latest/quota-monitor-for-aws/solution-overview.html)

* [AWS Auto Scaling](https://aws.amazon.com/autoscaling/)

* [What is Amazon CodeCatalyst?](https://docs.aws.amazon.com/codecatalyst/latest/userguide/welcome.html)

* [Using Amazon CloudWatch alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)

* [Using Amazon CloudWatch alarm actions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarms-and-actions)

* [Remediating Noncompliant Resources with AWS Config Rules](https://docs.aws.amazon.com/config/latest/developerguide/remediation.html)

* [Creating metrics from log events using filters](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/MonitoringLogData.html)

* [AWS Systems Manager State Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-state.html)

**Related videos:**

* [Create Automation Runbooks with AWS Systems Manager](https://www.youtube.com/watch?v=fQ_KahCPBeU)

* [How to automate IT Operations on AWS](https://www.youtube.com/watch?v=GuWj_mlyTug)

* [AWS Security Hub automation rules](https://www.youtube.com/watch?v=XaMfO_MERH8)

* [Start your software project fast with Amazon CodeCatalyst blueprints](https://www.youtube.com/watch?v=rp7roaoPzFE)

**Related examples:**

* [Amazon CodeCatalyst Tutorial: Creating a project with the Modern three-tier web application blueprint](https://docs.aws.amazon.com/codecatalyst/latest/userguide/getting-started-template-project.html)

* [One Observability Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/31676d37-bbe9-4992-9cd1-ceae13c5116c/en-US)

* [Respond to incidents using Incident Manager](https://catalog.workshops.aws/getting-started-with-com/en-US/operations-management/incident-manager)


[Document Conventions](/general/latest/gr/docconventions.html)

OPS10-BP06 Communicate status through dashboards

Evolve

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.</awsdocs-view></awsui-app-layout>
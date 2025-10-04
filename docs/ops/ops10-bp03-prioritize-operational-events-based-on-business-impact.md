[Documentation](/index.html)[Framework](welcome.html)

[Implementation guidance](#implementation-guidance)[Resources](#resources)

# OPS10-BP03 Prioritize operational events based on business impact

Responding promptly to operational events is critical, but not all events are equal. When you prioritize based on business impact, you also prioritize addressing events with the potential for significant consequences, such as safety, financial loss, regulatory violations, or damage to reputation.

**Desired outcome:** Responses to operational events are prioritized based on potential impact to business operations and objectives. This makes the responses efficient and effective.

**Common anti-patterns:**

* Every event is treated with the same level of urgency, leading to confusion and delays in addressing critical issues.

* You fail to distinguish between high and low impact events, leading to misallocation of resources.

* Your organization lacks a clear prioritization framework, resulting in inconsistent responses to operational events.

* Events are prioritized based on the order they are reported, rather than their impact on business outcomes.

**Benefits of establishing this best practice:**

* Ensures critical business functions receive attention first, minimizing potential damage.

* Improves resource allocation during multiple concurrent events.

* Enhances the organization's ability to maintain trust and meet regulatory requirements.

**Level of risk exposed if this best practice is not established:** High

## Implementation guidance

When faced with multiple operational events, a structured approach to prioritization based on impact and urgency is essential. This approach helps you make informed decisions, direct efforts where they're needed most, and mitigate the risk to business continuity.

### Implementation steps

1. **Assess impact:** Develop a classification system to evaluate the severity of events in terms of their potential impact on business operations and objectives. The following example shows impact categories:

   |---|---|
   |Impact level|Description|
   |High|Affects many staff or customers, high financial impact, high reputational damage, or injury.|
   |Medium|Affects a groups of staff or customers, moderate financial impact, or moderate reputational damage.|
   |Low|Affects individual staff or customers, low financial impact, or low reputational damage.|

2. **Assess urgency:** Define urgency levels for how quickly an event needs a response, considering factors such as safety, financial implications, and service-level agreements (SLAs). The following example demonstrates urgency categories:

   |---|---|
   |Urgency level|Description|
   |High|Exponentially increasing damage, time-sensitive work impacted, imminent escalation, or VIP users or groups affected.|
   |Medium|Damage increases over time, or single VIP user or group affected.|
   |Low|Marginal damage increase over time, or non-time-sensitive work impacted.|

3. **Create a prioritization matrix:**

   * Use a matrix to cross-reference impact and urgency, assigning priority levels to different combinations.

   * Make the matrix accessible and understood by all team members responsible for operational event responses.

   * The following example matrix displays incident severity according to urgency and impact:

   |---|---|---|---|
   |Urgency and impact|High|Medium|Low|
   |High|Critical|Urgent|High|
   |Medium|Urgent|High|Normal|
   |Low|High|Normal|Low|

4. **Train and communicate:** Train response teams on the prioritization matrix and the importance of following it during an event. Communicate the prioritization process to all stakeholders to set clear expectations.

5. **Integrate with incident response:**

   * Incorporate the prioritization matrix into your incident response plans and tools.

   * Automate the classification and prioritization of events where possible to speed up response times.

   * Enterprise Support customers can leverage [AWS Incident Detection and Response](https://aws.amazon.com/premiumsupport/aws-incident-detection-response/), which provides 24x7 proactive monitoring and incident management for production workloads.

6. **Review and adapt:** Regularly review the effectiveness of the prioritization process and make adjustments based on feedback and changes in the business environment.

## Resources

**Related best practices:**

* [OPS03-BP03 Escalation is encouraged](./ops_org_culture_team_enc_escalation.html)

* [OPS08-BP04 Create actionable alerts](./ops_workload_observability_create_alerts.html)

* [OPS09-BP01 Measure operations goals and KPIs with metrics](./ops_operations_health_measure_ops_goals_kpis.html)

**Related documents:**

* [Atlassian - Understanding incident severity levels](https://www.atlassian.com/incident-management/kpis/severity-levels)

* [IT Process Map - Checklist Incident Priority](https://wiki.en.it-processmaps.com/index.php/Checklist_Incident_Priority)


[Document Conventions](/general/latest/gr/docconventions.html)

OPS10-BP02 Have a process per alert

OPS10-BP04 Define escalation paths

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.</awsdocs-view></awsui-app-layout>
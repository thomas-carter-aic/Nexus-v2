[Documentation](/index.html)[Framework](welcome.html)

[Implementation guidance](#implementation-guidance)[Resources](#resources)

# OPS11-BP08 Document and share lessons learned

Document and share lessons learned from the operations activities so that you can use them internally and across teams. You should share what your teams learn to increase the benefit across your organization. Share information and resources to prevent avoidable errors and ease development efforts, and focus on delivery of desired features.

Use AWS Identity and Access Management (IAM) to define permissions that permit controlled access to the resources you wish to share within and across accounts.

**Desired outcome:**

* You use version-controlled repositories to share application libraries, scripted procedures, procedure documentation, and other system documentation.

* You share your infrastructure standards as version-controlled AWS CloudFormation templates.

* You review lessons learned across teams.

**Common anti-patterns:**

* You suffered an extended outage because your organization commonly uses buggy library. You have since migrated to a reliable library. The other teams in your organization do not know they are at risk. No one documents and shares the experience with this library, and they are not aware of the risk.

* You have identified an edge case in an internally-shared microservice that causes sessions to drop. You have updated your calls to the service to avoid this edge case. The other teams in your organization do not know that they are at risk.

* You have found a way to significantly reduce the CPU utilization requirements for one of your microservices. You do not know if any other teams could take advantage of this technique.

**Benefits of establishing this best practice:** Share lessons learned to support improvement and to maximize the benefits of experience.

**Level of risk exposed if this best practice is not established:** Low

## Implementation guidance

* **Document and share lessons learned:** Have procedures to document the lessons learned from the running of operations activities and retrospective analysis so that they can be used by other teams.

* **Share learnings:** Have procedures to share lessons learned and associated artifacts across teams. For example, share updated procedures, guidance, governance, and best practices through an accessible wiki. Share scripts, code, and libraries through a common repository.

  * Leverage [AWS re:Post Private](https://aws.amazon.com/repost-private/) as a knowledge service to streamline collaboration and knowledge sharing within your organization.

## Resources

**Related best practices:**

* [OPS02-BP06 Responsibilities between teams are predefined or negotiated](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_ops_model_def_neg_team_agreements.html)

* [OPS05-BP01 Use version control](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_dev_integ_version_control.html)

* [OPS05-BP06 Share design standards](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_dev_integ_share_design_stds.html)

* [OPS11-BP03 Implement feedback loops](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_evolve_ops_feedback_loops.html)

* [OPS11-BP07 Perform operations metrics reviews](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_evolve_ops_metrics_review.html)

**Related documents:**

* [Increase collaboration and securely share cloud knowledge with AWS re:Post Private](https://aws.amazon.com/blogs/aws/increase-collaboration-and-securely-share-cloud-knowledge-with-aws-repost-private/)

* [Reduce project delays with a docs-as-code solution](https://aws.amazon.com/blogs/infrastructure-and-automation/reduce-project-delays-with-docs-as-code-solution/)

**Related videos:**

* [AWS re:Invent 2023 - Collaborate within your company and with AWS using AWS re:Post Private](https://www.youtube.com/watch?v=HNq_kU2QJLU)

* [Supports You | Exploring the Incident Management Tabletop Exercise](https://www.youtube.com/watch?v=0m8sGDx-pRM)


[Document Conventions](/general/latest/gr/docconventions.html)

OPS11-BP07 Perform operations metrics reviews

OPS11-BP09 Allocate time to make improvements

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.</awsdocs-view></awsui-app-layout>
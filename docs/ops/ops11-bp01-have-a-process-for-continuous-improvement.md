[Documentation](/index.html)[Framework](welcome.html)

[Implementation guidance](#implementation-guidance)[Resources](#resources)

# OPS11-BP01 Have a process for continuous improvement

Evaluate your workload against internal and external architecture best practices. Conduct frequent, intentional workload reviews. Prioritize improvement opportunities into your software development cadence.

**Desired outcome:**

* You analyze your workload against architecture best practices frequently.

* You give improvement opportunities equal priority to features in your software development process.

**Common anti-patterns:**

* You have not conducted an architecture review on your workload since it was deployed several years ago.

* You give a lower priority to improvement opportunities. Compared to new features, these opportunities stay in the backlog.

* There is no standard for implementing modifications to best practices for the organization.

**Benefits of establishing this best practice:**

* Your workload is kept up-to-date on architecture best practices.

* You evolve your workload in an intentional manner.

* You can leverage organization best practices to improve all workloads.

* You make marginal gains that have a cumulative impact, which drives deeper efficiencies.

**Level of risk exposed if this best practice is not established:** High

## Implementation guidance

Frequently conduct an architectural review of your workload. Use internal and external best practices, evaluate your workload, and identify improvement opportunities. Prioritize improvement opportunities into your software development cadence.

### Implementation steps

1. Conduct periodic architecture reviews of your production workload with an agreed-upon frequency. Use a documented architectural standard that includes AWS-specific best practices.

   1. Use your internally-defined standards for these reviews. If you do not have an internal standard, use the AWS Well-Architected Framework.

   2. Use the AWS Well-Architected Tool to create a custom lens of your internal best practices and conduct your architecture review.

   3. Contact your AWS Solution Architect or Technical Account Manager to conduct a guided Well-Architected Framework Review of your workload.

2. Prioritize improvement opportunities identified during the review into your software development process.

**Level of effort for the implementation plan:** Low. You can use the AWS Well-Architected Framework to conduct your yearly architecture review.

## Resources

**Related best practices:**

* [OPS11-BP02 Perform post-incident analysis](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_evolve_ops_perform_rca_process.html)

* [OPS11-BP08 Document and share lessons learned](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_evolve_ops_share_lessons_learned.html)

* [OPS04 Implement Observability](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_evolve_ops_process_cont_imp.html)

**Related documents:**

* [AWS Well-Architected Tool - Custom lenses](https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses-custom.html)

* [AWS Well-Architected Whitepaper - The review process](https://docs.aws.amazon.com/wellarchitected/latest/framework/the-review-process.html)

* [Customize Well-Architected Reviews using Custom Lenses and the AWS Well-Architected Tool](https://aws.amazon.com/blogs/mt/customize-well-architected-reviews-using-custom-lenses-and-the-aws-well-architected-tool/)

* [Implementing the AWS Well-Architected Custom Lens lifecycle in your organization](https://aws.amazon.com/blogs/architecture/implementing-the-aws-well-architected-custom-lens-lifecycle-in-your-organization/)

**Related videos:**

* [AWS re:Invent 2023 - Scaling AWS Well-Architected best practices across your organization](https://youtu.be/UXtZCoE9qfQ?si=OPATCOY2YAwiF2TS)

**Related examples:**

* [AWS Well-Architected Tool](https://docs.aws.amazon.com/wellarchitected/latest/userguide/intro.html)


[Document Conventions](/general/latest/gr/docconventions.html)

OPS 11. How do you evolve operations?

OPS11-BP02 Perform post-incident analysis

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.</awsdocs-view></awsui-app-layout>
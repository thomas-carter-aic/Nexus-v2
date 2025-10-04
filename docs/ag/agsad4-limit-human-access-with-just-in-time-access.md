[Documentation](/index.html)[AWS Well-Architected](devops-guidance.html)

# [AG.SAD.4] Limit human access with just-in-time access

**Category:** FOUNDATIONAL

As pipelines take on a more prominent role in the software development lifecycle in a DevOps model, the necessity for extensive human access to environments decreases. Human users should be granted minimal access necessary for their role, which is usually read-only access that does not allow any modifications or access to sensitive data. For experimentation which is typically hands-on and exploratory, teams should be granted access to sandbox environments which are isolated from system workloads.

In some cases, where things go wrong or a process cannot yet be automated, elevated permissions might be required. To accommodate these needs without compromising security, implement a just-in-time (JIT) access control strategy where permissions are temporarily escalated for a specific duration and purpose, upon explicit request and approval. This approach maintains the principle of least privilege, allowing necessary operational functions to be performed efficiently when needed, while also ensuring that the access is revoked once the task is complete.

By enforcing limited human permissions and using JIT access, you can improve your organization's security posture and reduce the risk of accidental or deliberate misuse of access rights. This restrictive and controlled model supports modern, secure DevOps practices where pipelines, treating everything as code, and automation should take precedence over manual actions.

**Related information:**

* [Eliminate the need for human access](https://docs.aws.amazon.com/wellarchitected/latest/financial-services-industry-lens/use-immutable-infrastructure-with-no-human-access.html)

* [AWS Samples: AWS IAM Temporary Elevated Access Broker](https://github.com/aws-samples/aws-iam-temporary-elevated-access-broker)

* [Blog: Managing temporary elevated access to your AWS environment](https://aws.amazon.com/blogs/security/managing-temporary-elevated-access-to-your-aws-environment/)


[Document Conventions](/general/latest/gr/docconventions.html)

\[AG.SAD.3] Treat pipelines as production resources

\[AG.SAD.5] Implement break-glass procedures

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.</awsdocs-view></awsui-app-layout>
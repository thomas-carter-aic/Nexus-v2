[Documentation](/index.html)[Framework](welcome.html)

[Implementation guidance](#implementation-guidance)[Resources](#resources)

# OPS05-BP09 Make frequent, small, reversible changes

Frequent, small, and reversible changes reduce the scope and impact of a change. When used in conjunction with change management systems, configuration management systems, and build and delivery systems frequent, small, and reversible changes reduce the scope and impact of a change. This results in more effective troubleshooting and faster remediation with the option to roll back changes.

**Common anti-patterns:**

* You deploy a new version of your application quarterly with a change window that means a core service is turned off.

* You frequently make changes to your database schema without tracking changes in your management systems.

* You perform manual in-place updates, overwriting existing installations and configurations, and have no clear roll-back plan.

**Benefits of establishing this best practice:** Development efforts are faster by deploying small changes frequently. When the changes are small, it is much easier to identify if they have unintended consequences, and they are easier to reverse. When the changes are reversible, there is less risk to implementing the change, as recovery is simplified. The change process has a reduced risk and the impact of a failed change is reduced.

**Level of risk exposed if this best practice is not established:** Low

## Implementation guidance

Use frequent, small, and reversible changes to reduce the scope and impact of a change. This eases troubleshooting, helps with faster remediation, and provides the option to roll back a change. It also increases the rate at which you can deliver value to the business.

## Resources

**Related best practices:**

* [OPS05-BP03 Use configuration management systems](./ops_dev_integ_conf_mgmt_sys.html)

* [OPS05-BP04 Use build and deployment management systems](./ops_dev_integ_build_mgmt_sys.html)

* [OPS06-BP04 Automate testing and rollback](./ops_mit_deploy_risks_auto_testing_and_rollback.html)

**Related documents:**

* [Implementing Microservices on AWS](https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices-on-aws.html)

* [Microservices - Observability](https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/observability.html)


[Document Conventions](/general/latest/gr/docconventions.html)

OPS05-BP08 Use multiple environments

OPS05-BP10 Fully automate integration and deployment

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.</awsdocs-view></awsui-app-layout>
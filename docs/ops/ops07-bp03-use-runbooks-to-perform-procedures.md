[Documentation](/index.html)[Framework](welcome.html)

[Implementation guidance](#implementation-guidance)[Resources](#resources)

# OPS07-BP03 Use runbooks to perform procedures

A *runbook* is a documented process to achieve a specific outcome. Runbooks consist of a series of steps that someone follows to get something done. Runbooks have been used in operations going back to the early days of aviation. In cloud operations, we use runbooks to reduce risk and achieve desired outcomes. At its simplest, a runbook is a checklist to complete a task.

Runbooks are an essential part of operating your workload. From onboarding a new team member to deploying a major release, runbooks are the codified processes that provide consistent outcomes no matter who uses them. Runbooks should be published in a central location and updated as the process evolves, as updating runbooks is a key component of a change management process. They should also include guidance on error handling, tools, permissions, exceptions, and escalations in case a problem occurs.

As your organization matures, begin automating runbooks. Start with runbooks that are short and frequently used. Use scripting languages to automate steps or make steps easier to perform. As you automate the first few runbooks, you'll dedicate time to automating more complex runbooks. Over time, most of your runbooks should be automated in some way.

**Desired outcome:** Your team has a collection of step-by-step guides for performing workload tasks. The runbooks contain the desired outcome, necessary tools and permissions, and instructions for error handling. They are stored in a central location (version control system) and updated frequently. For example, your runbooks provide capabilities for your teams to monitor, communicate, and respond to AWS Health events for critical accounts during application alarms, operational issues, and planned lifecycle events.

**Common anti-patterns:**

* Relying on memory to complete each step of a process.

* Manually deploying changes without a checklist.

* Different team members performing the same process but with different steps or outcomes.

* Letting runbooks drift out of sync with system changes and automation.

**Benefits of establishing this best practice:**

* Reducing error rates for manual tasks.

* Operations are performed in a consistent manner.

* New team members can start performing tasks sooner.

* Runbooks can be automated to reduce toil.

**Level of risk exposed if this best practice is not established:** Medium

## Implementation guidance

Runbooks can take several forms depending on the maturity level of your organization. At a minimum, they should consist of a step-by-step text document. The desired outcome should be clearly indicated. Clearly document necessary special permissions or tools. Provide detailed guidance on error handling and escalations in case something goes wrong. List the runbook owner and publish it in a central location. Once your runbook is documented, validate it by having someone else on your team run it. As procedures evolve, update your runbooks in accordance with your change management process.

Your text runbooks should be automated as your organization matures. Using services like [AWS Systems Manager automations](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-automation.html), you can transform flat text into automations that can be run against your workload. These automations can be run in response to events, reducing the operational burden to maintain your workload. AWS Systems Manager Automation also provides a low-code [visual design experience](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-visual-designer.html) to create automation runbooks more easily.

**Customer example**

AnyCompany Retail must perform database schema updates during software deployments. The Cloud Operations Team worked with the Database Administration Team to build a runbook for manually deploying these changes. The runbook listed each step in the process in checklist form. It included a section on error handling in case something went wrong. They published the runbook on their internal wiki along with their other runbooks. The Cloud Operations Team plans to automate the runbook in a future sprint.

### Implementation steps

If you don't have an existing document repository, a version control repository is a great place to start building your runbook library. You can build your runbooks using Markdown. We have provided an example runbook template that you can use to start building runbooks.

```
# Runbook Title
## Runbook Info
| Runbook ID | Description | Tools Used | Special Permissions | Runbook Author | Last Updated | Escalation POC | 
|-------|-------|-------|-------|-------|-------|-------|
| RUN001 | What is this runbook for? What is the desired outcome? | Tools | Permissions | Your Name | 2022-09-21 | Escalation Name |
## Steps
1. Step one
2. Step two
```

1. If you don't have an existing documentation repository or wiki, create a new version control repository in your version control system.

2. Identify a process that does not have a runbook. An ideal process is one that is conducted semiregularly, short in number of steps, and has low impact failures.

3. In your document repository, create a new draft Markdown document using the template. Fill in Runbook Title and the required fields under Runbook Info.

4. Starting with the first step, fill in the Steps portion of the runbook.

5. Give the runbook to a team member. Have them use the runbook to validate the steps. If something is missing or needs clarity, update the runbook.

6. Publish the runbook to your internal documentation store. Once published, tell your team and other stakeholders.

7. Over time, you'll build a library of runbooks. As that library grows, start working to automate runbooks.

**Level of effort for the implementation plan:** Low. The minimum standard for a runbook is a step-by-step text guide. Automating runbooks can increase the implementation effort.

## Resources

**Related best practices:**

* [OPS02-BP02 Processes and procedures have identified owners](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_ops_model_def_proc_owners.html)

* [OPS07-BP04 Use playbooks to investigate issues](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_ready_to_support_use_playbooks.html)

* [OPS10-BP01 Use a process for event, incident, and problem management](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_event_response_event_incident_problem_process.html)

* [OPS10-BP02 Have a process per alert](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_event_response_process_per_alert.html)

* [OPS11-BP04 Perform knowledge management](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_evolve_ops_knowledge_management.html)

**Related documents:**

* [AWS Well-Architected Framework: Concepts: Runbook development](https://wa.aws.amazon.com/wellarchitected/2020-07-02T19-33-23/wat.concept.runbook.en.html)

* [Achieving Operational Excellence using automated playbook and runbook](https://aws.amazon.com/blogs/mt/achieving-operational-excellence-using-automated-playbook-and-runbook/)

* [AWS Systems Manager: Working with runbooks](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-documents.html)

* [Migration playbook for AWS large migrations - Task 4: Improving your migration runbooks](https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-migration-playbook/task-four-migration-runbooks.html)

* [Use AWS Systems Manager Automation runbooks to resolve operational tasks](https://aws.amazon.com/blogs/mt/use-aws-systems-manager-automation-runbooks-to-resolve-operational-tasks/)

**Related videos:**

* [AWS re:Invent 2019: DIY guide to runbooks, incident reports, and incident response](https://www.youtube.com/watch?v=E1NaYN_fJUo)

* [How to automate IT Operations on AWS | Amazon Web Services](https://www.youtube.com/watch?v=GuWj_mlyTug)

* [Integrate Scripts into AWS Systems Manager](https://www.youtube.com/watch?v=Seh1RbnF-uE)

**Related examples:**

* [Well-Architected Labs: Automating operations with Playbooks and Runbooks](https://wellarchitectedlabs.com/operational-excellence/200_labs/200_automating_operations_with_playbooks_and_runbooks/)

* [AWS Blog Post: Build a Cloud Automation Practice for Operational Excellence: Best Practices from AWS Managed Services](https://aws.amazon.com/blogs/mt/build-a-cloud-automation-practice-for-operational-excellence-best-practices-from-aws-managed-services/)

* [AWS Systems Manager: Automation walkthroughs](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-walk.html)

* [AWS Systems Manager: Restore a root volume from the latest snapshot runbook](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-document-sample-restore.html)

* [Building an AWS incident response runbook using Jupyter notebooks and CloudTrail Lake](https://catalog.us-east-1.prod.workshops.aws/workshops/a5801f0c-7bd6-4282-91ae-4dfeb926a035/en-US)

* [Gitlab - Runbooks](https://gitlab.com/gitlab-com/runbooks)

* [Rubix - A Python library for building runbooks in Jupyter Notebooks](https://github.com/Nurtch/rubix)

* [Using Document Builder to create a custom runbook](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-walk-document-builder.html)

**Related services:**

* [AWS Systems Manager Automation](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-automation.html)


[Document Conventions](/general/latest/gr/docconventions.html)

OPS07-BP02: Ensure a consistent review of operational readiness

OPS07-BP04 Use playbooks to investigate issues

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.</awsdocs-view></awsui-app-layout>
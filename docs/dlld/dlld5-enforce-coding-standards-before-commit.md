[Documentation](/index.html)[AWS Well-Architected](devops-guidance.html)

# [DL.LD.5] Enforce coding standards before commit

**Category:** RECOMMENDED

Identify common style, formatting, and other flaws before they are published to a repository. Use static code scanning tools, such as linters, to improve code quality and consistency before pushing committed code. This process can be automated using pre-commit hooks. Upon discovery, pushing the commit should ideally fail and require immediate correction by the developer. Automatically and consistently enforcing coding standards during the local development process directly improves the code review process by removing common errors before manual review.

Select scanning tools compatible with your chosen programming language and customize them to uphold specific coding standards and styles. It is best to integrate these tools into pre-commit hooks, integrated development environments (IDEs), and continuous integration pipelines so that changes are consistently and continuously checked at all stages of the development lifecycle.

**Related information:**

* [Amazon CodeGuru Reviewer](https://aws.amazon.com/codeguru/)

* [AWS CloudFormation Linter](https://github.com/aws-cloudformation/cfn-lint)

* [Pre-commit](https://pre-commit.com/)

* [Husky](https://typicode.github.io/husky/)

* [Validate your AWS SAM applications with AWS CloudFormation Linter](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/validate-cfn-lint.html)

* [Workshop: AWS CloudFormation Workshop - Linting and-testing](https://catalog.workshops.aws/cfn101/en-US/basics/templates/linting-and-testing)

* [Blog: Use Git pre-commit hooks to avoid AWS CloudFormation errors](https://aws.amazon.com/blogs/infrastructure-and-automation/use-git-pre-commit-hooks-avoid-aws-cloudformation-errors/)

* [Blog: Automate code reviews with Amazon CodeGuru Reviewer](https://aws.amazon.com/blogs/devops/automate-code-reviews-with-amazon-codeguru-reviewer/)


[Document Conventions](/general/latest/gr/docconventions.html)

\[DL.LD.4] Enforce security checks before commit

\[DL.LD.6] Leverage extensible development tools

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.</awsdocs-view></awsui-app-layout>
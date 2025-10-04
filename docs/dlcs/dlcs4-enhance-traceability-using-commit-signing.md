[Documentation](/index.html)[AWS Well-Architected](devops-guidance.html)

# [DL.CS.4] Enhance traceability using commit signing

**Category:** OPTIONAL

Commit signing involves attaching a digital signature to code commits, certifying the integrity of changes and the identity of the committer. While not universally adopted by all organizations, commit signing enhances trust and traceability as developers make code changes, making it easier to track the origin of changes and ensure their authenticity.

Have developers sign their code changes when submitting to version control using personal private keys from tools like [GPG](https://gnupg.org/). Developers should be encouraged to sign both commits and tags with their private keys. This can be particularly valuable for open-source projects or where code originates from diverse sources.

For this approach to be effective in practice, developers require an understanding of certificates and using them for signing. Developers must ensure that their private keys remain confidential, taking measures to store them securely and avoid potential exposure. They also should be trained to recognize signs of key compromise, such as unexpected commits. When compromise is detected, the associated key should be revoked immediately to mitigate potential risks.

**Related information:**

* [Signing Commits](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work#_signing_commits)

* [The GNU Privacy Guard](https://gnupg.org/)


[Document Conventions](/general/latest/gr/docconventions.html)

\[DL.CS.3] Enforce verification before using signed artifacts

Anti-patterns

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.</awsdocs-view></awsui-app-layout>
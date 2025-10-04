ADR 0002: Adoption of ArgoCD for GitOps
Status
Accepted
Context
The monorepo requires a GitOps approach for continuous deployment to Kubernetes, ensuring declarative and automated deployments.
Decision
Use ArgoCD with Rollouts for canary deployments, integrated with Kustomize for multi-environment support.
Consequences

Pros: Declarative deployments, automated rollbacks, environment isolation.
Cons: Learning curve for team unfamiliar with GitOps.
Mitigation: Provide documentation in docs/setup.md and admin frontend for management.

Date
2025-07-18

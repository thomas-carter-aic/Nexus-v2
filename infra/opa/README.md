OPA Gatekeeper:
Install via Helm:
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm install gatekeeper gatekeeper/gatekeeper --create-namespace -n gatekeeper

Example ConstraintTemplate and Constraint are provided to enforce namespace label policies.

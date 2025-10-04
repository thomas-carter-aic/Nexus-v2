# cert-manager <-> Vault Integration (dev sample)

This document explains how to configure cert-manager to use Vault as a signing CA.

1. Install Vault and cert-manager.
2. Create a Vault policy 'cert-manager-pki' allowing cert signing at 'pki/issue/cert-manager-otel'.
3. Create a Kubernetes secret in the cert-manager namespace containing a Vault token with that policy (see infra/cert-manager-vault/vault-token-secret.yaml).
4. Apply the ClusterIssuer infra/cert-manager-vault/cluster-issuer-vault.yaml.

This sample is for development and demonstration. For production, configure Kubernetes auth for Vault and use a secure token management strategy.

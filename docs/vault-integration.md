# Vault Integration

Steps:
1. Install Vault (Bitnami chart included as example) or use HashiCorp official distribution.
2. Configure Kubernetes auth and create policies for External Secrets.
3. Store secrets at paths like secret/data/platform/orchestration/postgres with POSTGRES_URL property.
4. Deploy ExternalSecrets operator and ClusterSecretStore pointing to Vault.
5. Helm charts reference the created secrets via templates/externalsecret.yaml in orchestration chart.

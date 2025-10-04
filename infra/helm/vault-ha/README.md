Vault HA Helm Chart (with AWS auto-unseal & S3 optional)

This chart supports:
- storage.type: raft (default) or s3
- autoUnseal.provider: none or awskms

Operator steps (AWS):
1. If using AWS S3 for storage or AWS KMS for auto-unseal, run Terraform in infra/terraform/vault-aws to create S3 bucket and KMS key.
2. Set the following values in Helm values.yaml or pass via --set:
   - storage.type=s3
   - storage.s3.bucket=<bucket-name>
   - storage.s3.region=<region>
   - autoUnseal.provider=awskms
   - autoUnseal.awskms.kmsKeyId=<kms-key-id>
3. Deploy the chart:
   helm upgrade --install vault infra/helm/vault-ha -n vault --create-namespace -f myvalues.yaml
4. Initialize vault (only once):
   kubectl -n vault exec -it statefulset/vault -- vault operator init -key-shares=1 -key-threshold=1
   Save the unseal keys securely (or configure auto-unseal with KMS to avoid manual unseal).
5. If using auto-unseal with KMS, ensure the Kubernetes nodes (or service account via IRSA) have permission to use the KMS key.
6. Enable kubernetes auth and create roles/policies (scripts provided in templates/k8s-auth-setup.sh).

Notes:
- For production, configure TLS for Vault listener and set appropriate storage and backup policies.
- Consider using Vault Auto Unseal with a cloud KMS and Vault enterprise features for stronger high-availability workflows.

---
### AWS IRSA & Terraform bridge
A sample Terraform module exists at infra/terraform/vault-aws which will create:
- S3 bucket for storage
- KMS key for auto-unseal
- IAM role to use for IRSA (Vault service account)

After terraform apply, run:
- scripts/generate-vault-values-from-tf.sh infra/terraform/vault-aws > myvalues.yaml
- Edit myvalues.yaml as needed, then helm upgrade --install vault infra/helm/vault-ha -n vault -f myvalues.yaml

To enable IRSA for the Vault service account, create the serviceaccount manifest infra/k8s/vault/vault-serviceaccount-irsa.yaml with the role ARN output from Terraform.

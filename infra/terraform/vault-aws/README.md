Terraform module to create AWS resources for Vault HA auto-unseal and IRSA role binding

Usage:
- Provide the EKS cluster name (existing), OIDC thumbprint, and desired S3 bucket name.
- terraform init && terraform apply
- Use outputs to populate Helm values (s3 bucket, kms key id, and IRSA role arn)

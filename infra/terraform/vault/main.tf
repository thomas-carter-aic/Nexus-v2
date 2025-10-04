# Terraform skeleton for Vault provisioning (cloud-specific resources required)
terraform {
  required_version = ">= 1.1.0"
}
provider "kubernetes" {
  # configure provider as needed
}
# This file intentionally minimal: in production, add cloud resources (load balancers, storage) and k8s provider config

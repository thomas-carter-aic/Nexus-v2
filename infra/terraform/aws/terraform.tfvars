# AIC AI Platform Terraform Variables
# Customize these values for your environment

# Basic Configuration
cluster_name = "aic-aipaas-eks-dev"
aws_region   = "us-west-2"
environment  = "dev"

# Kubernetes Configuration
kubernetes_version = "1.28"

# Cost Optimization (set to false for production)
single_nat_gateway         = true
enable_deletion_protection = false

# Logging
log_retention_days = 7

# Node Group Sizing (adjust based on your needs)
# System nodes (for core Kubernetes services)
system_node_min_size     = 1
system_node_max_size     = 3
system_node_desired_size = 2

# Application nodes (for your services)
app_node_min_size     = 2
app_node_max_size     = 10
app_node_desired_size = 3

# GPU nodes (for AI/ML workloads)
gpu_node_min_size     = 0
gpu_node_max_size     = 3
gpu_node_desired_size = 0 # Start with 0 to save costs

# Tags
common_tags = {
  Project     = "AIC-AIPaaS"
  Environment = "dev"
  ManagedBy   = "Terraform"
  Owner       = "Platform-Team"
  CostCenter  = "Engineering"
}

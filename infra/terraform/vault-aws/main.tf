terraform {
  required_version = ">= 1.1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# Data source for existing EKS cluster (assumes cluster created externally)
data "aws_eks_cluster" "cluster" {
  name = var.eks_cluster_name
}

data "aws_eks_cluster_auth" "cluster" {
  name = var.eks_cluster_name
}

# Create S3 bucket for Vault storage (optional)
resource "aws_s3_bucket" "vault_storage" {
  bucket = var.s3_bucket_name
  acl    = "private"
  force_destroy = true
  tags = var.tags
}

# Create a KMS key for auto-unseal
resource "aws_kms_key" "vault_unseal_key" {
  description = "KMS key for Vault auto-unseal"
  deletion_window_in_days = 7
  enable_key_rotation = true
  policy = data.aws_iam_policy_document.vault_kms_policy.json
  tags = var.tags
}

data "aws_iam_policy_document" "vault_kms_policy" {
  statement {
    sid = "AllowUseCrossAccount" 
    actions = [
      "kms:Decrypt",
      "kms:DescribeKey",
      "kms:Encrypt",
      "kms:GenerateDataKey*",
      "kms:ReEncrypt*"
    ]
    resources = ["*"]
    principals {
      type = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

# Create IAM role for Vault service account (IRSA)
resource "aws_iam_openid_connect_provider" "oidc" {
  url = data.aws_eks_cluster.cluster.identity[0].oidc[0].issuer
  client_id_list = ["sts.amazonaws.com"]
  thumbprint_list = [var.oidc_thumbprint]
}

resource "aws_iam_role" "vault_irsa_role" {
  name = "${var.cluster_short_name}-vault-irsa-role"
  assume_role_policy = data.aws_iam_policy_document.vault_assume_role_policy.json
  tags = var.tags
}

data "aws_iam_policy_document" "vault_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"
    principals {
      type = "Federated"
      identifiers = [aws_iam_openid_connect_provider.oidc.arn]
    }
    condition {
      test = "StringEquals"
      values = ["system:serviceaccount:${var.vault_namespace}:${var.vault_sa_name}"]
      variable = "${replace(aws_iam_openid_connect_provider.oidc.url, "https://", "")}:sub"
    }
  }
}

# Attach policy to allow KMS decrypt and S3 access
resource "aws_iam_policy" "vault_kms_s3_policy" {
  name = "${var.cluster_short_name}-vault-kms-s3-policy"
  path = "/"
  policy = data.aws_iam_policy_document.vault_kms_s3_policy.json
}

data "aws_iam_policy_document" "vault_kms_s3_policy" {
  statement {
    actions = [
      "kms:Decrypt",
      "kms:DescribeKey",
      "kms:Encrypt",
      "kms:GenerateDataKey*",
      "kms:ReEncrypt*"
    ]
    resources = [aws_kms_key.vault_unseal_key.arn]
  }
  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
      "s3:ListBucket"
    ]
    resources = [
      aws_s3_bucket.vault_storage.arn,
      "${aws_s3_bucket.vault_storage.arn}/*"
    ]
  }
}

resource "aws_iam_role_policy_attachment" "attach_policy" {
  role       = aws_iam_role.vault_irsa_role.name
  policy_arn = aws_iam_policy.vault_kms_s3_policy.arn
}

# Outputs for Helm values bridging
output "s3_bucket" {
  value = aws_s3_bucket.vault_storage.id
}
output "kms_key_id" {
  value = aws_kms_key.vault_unseal_key.key_id
}
output "vault_irsa_role_arn" {
  value = aws_iam_role.vault_irsa_role.arn
}

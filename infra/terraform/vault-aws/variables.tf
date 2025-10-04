variable "region" { type = string }
variable "eks_cluster_name" { type = string }
variable "cluster_short_name" { type = string default = "eks" }
variable "s3_bucket_name" { type = string }
variable "oidc_thumbprint" { type = string }
variable "vault_namespace" { type = string default = "vault" }
variable "vault_sa_name" { type = string default = "vault" }
variable "tags" { type = map(string) default = {} }

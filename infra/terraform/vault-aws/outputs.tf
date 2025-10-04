output "s3_bucket" { value = aws_s3_bucket.vault_storage.id }
output "kms_key_id" { value = aws_kms_key.vault_unseal_key.key_id }
output "vault_irsa_role_arn" { value = aws_iam_role.vault_irsa_role.arn }

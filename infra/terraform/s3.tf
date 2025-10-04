resource "aws_s3_bucket" "data" {
  bucket = var.s3_bucket
  acl    = "private"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "prevent-delete"
    enabled = true
    abort_incomplete_multipart_upload_days = 7

    noncurrent_version_expiration {
      days = 30
    }
  }

  tags = {
    Name = "ai-poc-s3"
  }
}

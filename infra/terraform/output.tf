output "management_public_ip" {
  description = "Public IP of the management EC2 instance"
  value       = aws_instance.management.public_ip
}

output "s3_bucket" {
  value = aws_s3_bucket.data.bucket
}

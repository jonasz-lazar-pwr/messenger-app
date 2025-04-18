# s3/outputs.tf

output "bucket_name" {
  description = "Name of the created S3 bucket"  # Nazwa utworzonego bucketa S3
  value       = aws_s3_bucket.this.bucket
}

output "bucket_arn" {
  description = "ARN of the created S3 bucket"   # ARN utworzonego bucketa S3
  value       = aws_s3_bucket.this.arn
}
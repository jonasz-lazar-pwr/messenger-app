# s3/variables.tf

# Nazwa tworzonego bucketa S3
variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

# Wspólne tagi przypisane do zasobów S3
variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
}

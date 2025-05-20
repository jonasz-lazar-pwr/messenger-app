# variables.tf (root)

# === Ustawienia globalne ===
variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
}

# === Poświadczenia AWS  ===
variable "aws_access_key_id" {
  description = "AWS access key ID"
  type        = string
  sensitive   = true
}

variable "aws_secret_access_key" {
  description = "AWS secret access key"
  type        = string
  sensitive   = true
}

variable "aws_session_token" {
  description = "AWS session token"
  type        = string
  sensitive   = true
}

# === VPC i sieć ===
variable "vpc_name" {
  description = "Name tag for the VPC"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "subnet_cidrs" {
  description = "Map of subnet names to their CIDR blocks"
  type        = map(string)
}

variable "availability_zones" {
  description = "Map of subnet names to their availability zones"
  type        = map(string)
}

# === S3 ===
variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

# === RDS ===
variable "db_instance_identifier" {
  description = "The DB instance identifier"
  type        = string
}

variable "db_name" {
  description = "The name of the database"
  type        = string
}

variable "db_username" {
  description = "The master username for the database"
  type        = string
}

variable "db_password" {
  description = "The password for the database"
  type        = string
  sensitive   = true
}

variable "db_subnet_group_name" {
  description = "The DB subnet group name"
  type        = string
}

variable "db_port" {
  description = "The port of the database"
  type        = number
}

# === Cognito ===
variable "user_pool_name" {
  description = "Name of the Cognito User Pool"
  type        = string
}

variable "app_client_name" {
  description = "Name of the Cognito User Pool App Client"
  type        = string
}

variable "domain_prefix" {
  description = "Prefix for the Cognito hosted domain"
  type        = string
}

variable "cognito_issuer_url" {
  description = "Cognito Issuer URL"
  type        = string
}

variable "cognito_code" {
  description = "OAuth2 response type (e.g. 'code')"
  type        = string
}

variable "cognito_scope" {
  description = "OAuth2 scopes (e.g. 'email openid profile')"
  type        = string
}

# === Backend ===
variable "backend_name" {
  description = "The name of the Elastic Beanstalk backend application"
  type        = string
}

variable "backend_env_name" {
  description = "The name of the Elastic Beanstalk backend environment"
  type        = string
}

variable "backend_port" {
  description = "The number of backend port"
  type        = number
}

# === Frontend (Elastic Beanstalk SPA) ===
variable "frontend_name" {
  description = "The name of the Elastic Beanstalk frontend application"
  type        = string
}

variable "frontend_env_name" {
  description = "The name of the Elastic Beanstalk frontend environment"
  type        = string
}

variable "frontend_url" {
  description = "The base URL of this frontend environment"
  type        = string
}

# === Inne ustawienia ===
variable "allowed_origins" {
  description = "Allowed origins for CORS"
  type        = string
}

variable "ssl_certificate_arn" {
  description = "ARN certyfikatu SSL z ACM"
  type        = string
}

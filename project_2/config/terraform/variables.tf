# variables.tf (root)

# === AWS region ===
variable "aws_region" {
  description = "The AWS region where all resources will be deployed."
  type        = string
}

# === Global tags for all resources ===
variable "tags" {
  description = "A map of common tags to apply to all created resources."
  type        = map(string)
}

# === VPC configuration ===
variable "vpc_name" {
  description = "A descriptive name for the Virtual Private Cloud (VPC)."
  type        = string
}

variable "vpc_cidr" {
  description = "The primary IPv4 CIDR block for the VPC (e.g., '10.0.0.0/16')."
  type        = string
}

variable "subnet_cidrs" {
  description = "A map of subnet names to their IPv4 CIDR blocks."
  type        = map(string)
}

variable "availability_zones" {
  type        = map(string)
  description = "A map of subnet names to their corresponding Availability Zones."
}

# === RDS configuration ===
variable "chat_service_db_instance_identifier" {
  description = "Unique identifier for the RDS instance dedicated to the chat-service."
  type        = string
}

variable "chat_service_db_subnet_group_name" {
  description = "Name of the DB subnet group for the chat-service RDS instance."
  type        = string
}

variable "chat_service_db_name" {
  description = "The initial database name to be created within the chat-service RDS instance."
  type        = string
}
variable "chat_service_db_username" {
  description = "Master username for accessing the chat-service database."
  type        = string
}
variable "chat_service_db_password" {
  type        = string
  description = "Master password for the chat-service database."
  sensitive   = true
}
variable "chat_service_db_port" {
  type        = number
  description = "Network port for the chat-service PostgreSQL database."
}

# === Cognito configuration ===
variable "cognito_user_pool_name" {
  description = "Name for the Cognito User Pool."
  type        = string
}

variable "cognito_app_client_name" {
  description = "Name for the Cognito User Pool App Client."
  type        = string
}

variable "cognito_domain_prefix" {
  description = "Unique prefix for the Cognito hosted UI domain."
  type        = string
}

variable "cognito_issuer_url" {
  description = "The issuer URL for the Cognito User Pool."
  type        = string
}

variable "cognito_response_type" {
  description = "The OAuth 2.0 response type used in the authorization flow (e.g., 'code')."
  type        = string
}

variable "cognito_allowed_scopes" {
  description = "A space-separated list of OAuth 2.0 scopes allowed for the app client (e.g., 'openid profile email')."
  type        = string
}

# === S3 configuration ===
variable "s3_bucket_name" {
  description = "Globally unique name for the S3 bucket used by the application."
  type        = string
}

# === SNS configuration ===
variable "sns_topic_name" {
  description = "Name for the SNS topic used for application notifications."
  type        = string
}

variable "sns_notification_email" {
  description = "The email address that will be subscribed to the SNS topic to receive notifications."
  type        = string
}

# === DynamoDB configuration ===
variable "dynamodb_media_table_name" {
  description = "Name for the DynamoDB table used to store media metadata."
  type        = string
}

variable "dynamodb_notification_table_name" {
  description = "Name for the DynamoDB table used to store notification history."
  type        = string
}

# === AWS credentials ===
variable "aws_access_key_id" {
  description = "AWS access key ID. Recommended to use IAM roles instead where possible."
  type        = string
  sensitive   = true
}

variable "aws_secret_access_key" {
  description = "AWS secret access key. Recommended to use IAM roles instead where possible."
  type        = string
  sensitive   = true
}

variable "aws_session_token" {
  description = "AWS session token (if using temporary credentials). Recommended to use IAM roles instead."
  type        = string
  sensitive   = true
}

# === ECS/ALB configuration ===
variable "ssl_certificate_arn" {
  description = "ARN of the SSL certificate to be used by public-facing ALBs for HTTPS."
  type        = string
}

variable "ecs_task_execution_role_arn" {
  description = "ARN of the IAM role that grants the ECS agent permissions to make AWS API calls on your behalf (e.g., pull images, send logs)."
  type        = string
}

variable "notification_receiver_email" {
  description = "The primary email address designated to receive notifications from the notification-service."
  type        = string
}

variable "default_container_port" {
  description = "Default port number used by application containers."
  type        = number
}

variable "default_cpu" {
  description = "Default CPU units to allocate for ECS tasks."
  type        = number
}

variable "default_memory" {
  description = "Default memory (in MiB) to allocate for ECS tasks."
  type        = number
}

variable "default_desired_count" {
  description = "Default initial number of tasks to run for ECS services."
  type        = number
}

variable "cors_allow_origins" {
  description = "A comma-separated string or a single origin URL allowed by CORS configuration (e.g. '*')."
  type        = string
}
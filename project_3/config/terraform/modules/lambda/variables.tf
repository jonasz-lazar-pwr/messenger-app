# lambda/variables.tf

variable "psql_host" {
  description = "Hostname of the PostgreSQL database (RDS endpoint)"
  type        = string
}

variable "psql_port" {
  description = "Port number for connecting to the PostgreSQL database"
  type        = number
}

variable "psql_user" {
  description = "Username for authenticating with the PostgreSQL database"
  type        = string
}

variable "psql_password" {
  description = "Password for authenticating with the PostgreSQL database"
  type        = string
}

variable "psql_name" {
  description = "Name of the PostgreSQL database to connect to"
  type        = string
}

variable "cognito_pool_id" {
  description = "Cognito user pool ID used for JWT validation"
  type        = string
}

variable "cognito_client_id" {
  description = "Client ID of the application registered in Cognito"
  type        = string
}

variable "cognito_issuer_url" {
  description = "Issuer URL for validating JWTs using the Cognito pool"
  type        = string
}

variable "media_service_host" {
  description = "Internal DNS host of the media-service registered in Cloud Map"
  type        = string
}

variable "iam_role_arn" {
  description = "IAM role ARN used by the Lambda function"
  type        = string
}

variable "sqs_notification_queue_url" {
  description = "Full URL to SQS queue used for notifications"
  type        = string
}

variable "sns_notification_email" {
  description = "The email address to subscribe to the SNS topic for notifications"
  type        = string
}

# api_gateway/variables.tf

variable "lambda_arns" {
  description = "Map of Lambda function ARNs keyed by route name (e.g. get_messages, post_message)."
  type        = map(string)
}

variable "cognito_pool_id" {
  description = "ID of the Cognito user pool used to validate JWT tokens."
  type        = string
}

variable "cognito_issuer_url" {
  description = "Issuer URL for JWT validation, derived from the Cognito user pool."
  type        = string
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
}

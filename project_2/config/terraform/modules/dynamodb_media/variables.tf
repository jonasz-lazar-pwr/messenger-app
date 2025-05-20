# dynamodb_media/variables.tf

variable "table_name" {
  description = "The name of the DynamoDB table."
  type        = string
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
}

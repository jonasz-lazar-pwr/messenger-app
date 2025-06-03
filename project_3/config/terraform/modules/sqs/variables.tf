# sqs/variables.tf

variable "queue_name" {
  description = "The name of the SQS queue used for notifications."
  type        = string
}

variable "tags" {
  description = "Common tags to apply to all resources."
  type        = map(string)
}

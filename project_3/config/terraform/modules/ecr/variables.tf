# ecr/variables.tf

variable "services" {
  description = "A list of service names for which ECR repositories will be created."
  type        = list(string)
}

variable "tags" {
  description = "Common tags for all resources."
  type        = map(string)
}

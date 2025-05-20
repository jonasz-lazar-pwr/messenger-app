# ecs/variables.tf

variable "cluster_id" {
  type        = string
  description = "The name of the ECS cluster where the service will be deployed."
}

variable "service_name" {
  description = "The name of the ECS service to be created."
  type        = string
}

variable "image" {
  description = "The Docker image URI for the service's container (e.g., from ECR)."
  type        = string
}

variable "container_port" {
  description = "The port on which the container is listening."
  type        = number
}

variable "cpu" {
  description = "The number of CPU units to reserve for the container."
  type        = number
}

variable "memory" {
  description = "The amount of memory (in MiB) to reserve for the container."
  type        = number
}

variable "desired_count" {
  description = "The initial number of tasks to launch for the service."
  type        = number
}

variable "subnet_ids" {
  description = "A list of subnet IDs where the ECS tasks will be placed."
  type        = list(string)
}

variable "security_group_id" {
  description = "The ID of the security group to associate with the ECS tasks."
  type        = string
}

variable "execution_role_arn" {
  description = "The ARN of the IAM role that allows ECS tasks to make calls to AWS services on your behalf (e.g., to pull images from ECR, send logs to CloudWatch)."
  type        = string
}

variable "alb_target_group_arn" {
  description = "The ARN of the ALB target group to associate with the service."
  type        = string
}

variable "aws_region" {
  description = "The AWS region where the ECS service and related resources are deployed."
  type        = string
}

variable "environment" {
  description = "A list of environment variables to pass to the container."
  type        = list(object({
    name  = string
    value = string
  }))
}

# alb/variables.tf

variable "service_name" {
  description = "Name of the service this ALB is fronting (e.g., 'frontend', 'api-gateway'). Used for naming ALB resources."
  type        = string
}

variable "container_port" {
  description = "The port on which the containers in the target group are listening."
  type        = number
}

variable "vpc_id" {
  description = "The ID of the VPC where the ALB and Target Group will be created."
  type        = string
}

variable "subnet_ids" {
  description = "A list of subnet IDs to associate with the ALB. Should be public for public ALBs, private for internal ALBs."
  type        = list(string)
}

variable "security_group_ids" {
  description = "A list of security group IDs to associate with the ALB."
  type        = list(string)
}

variable "is_internal" {
  description = "Specifies if the load balancer is internal (true) or public (false)."
  type        = bool
}

variable "health_check_path" {
  description = "The destination path for the health check request (e.g., '/' or '/healthz/')."
  type        = string
}

variable "health_check_matcher" {
  description = "The HTTP codes to use when checking for a successful response from a target (e.g., '200' or '200-399')."
  type        = string
}

variable "listener_port" {
  description = "The port on which the load balancer listener will listen (e.g., 80, 443)."
  type        = number
}

variable "listener_protocol" {
  description = "The protocol for the load balancer listener (e.g., 'HTTP', 'HTTPS')."
  type        = string
}

variable "ssl_certificate_arn" {
  description = "ARN of the SSL certificate for HTTPS listener. Required if listener_protocol is HTTPS."
  type        = string
  default     = null
}

variable "tags" {
  description = "Common tags for all resources."
  type = map(string)
}

# alb/variables.tf

variable "default_container_port" {
  description = "The port on which the container listens inside the target group."
  type        = number
}

variable "vpc_id" {
  description = "The ID of the VPC where the Application Load Balancer and target groups will be created."
  type        = string
}

variable "subnet_ids" {
  description = "A list of subnet IDs to associate with the ALB. Use public subnets for internet-facing ALBs, private subnets for internal ALBs."
  type        = list(string)
}

variable "security_group_ids" {
  description = "A list of security group IDs to associate with the ALB for traffic control."
  type        = list(string)
}

variable "ssl_certificate_arn" {
  description = "The ARN of the ACM SSL certificate to use with HTTPS listeners. Required if the listener protocol is HTTPS."
  type        = string
}

variable "tags" {
  description = "Common tags for all resources."
  type        = map(string)
}

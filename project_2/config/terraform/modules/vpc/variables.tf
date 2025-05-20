# vpc/variables.tf

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "vpc_name" {
  description = "Name for the VPC and related resources"
  type        = string
}

variable "subnet_cidrs" {
  description = "Map of CIDR blocks for public subnets"
  type        = map(string)
}

variable "availability_zones" {
  description = "Map of availability zones for each public subnet"
  type        = map(string)
}

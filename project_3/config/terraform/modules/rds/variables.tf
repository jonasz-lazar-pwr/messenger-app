# rds/variables.tf

variable "db_instance_identifier" {
  description = "Unique identifier for the RDS database instance."
  type        = string
}

variable "db_name" {
  description = "The name of the initial database to be created in the RDS instance."
  type        = string
}

variable "db_username" {
  description = "The master username for the RDS database instance."
  type        = string
}

variable "db_password" {
  description = "The master password for the RDS database instance."
  type        = string
  sensitive   = true
}

variable "db_port" {
  description = "The port on which the RDS database instance will listen."
  type        = number
}

variable "db_subnet_ids" {
  description = "A list of subnet IDs to associate with the DB subnet group."
  type        = list(string)
}

variable "db_subnet_group_name" {
  description = "The name for the DB subnet group."
  type        = string
}

variable "security_group_ids" {
  description = "A list of VPC security group IDs to associate with the RDS instance."
  type        = list(string)
}

variable "tags" {
  description = "Common tags"
  type        = map(string)
}

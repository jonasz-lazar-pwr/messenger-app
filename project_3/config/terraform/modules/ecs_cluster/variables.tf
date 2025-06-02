# ecs_cluster/variables.tf

variable "cluster_name" {
  description = "The name of the ECS cluster to be created."
  type        = string
}

variable "tags" {
  description = "Common tags for all resources."
  type        = map(string)
}

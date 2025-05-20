# ecs_cluster/main.tf

resource "aws_ecs_cluster" "this" {
  name = var.cluster_name                   # Nazwa klastra ECS
}
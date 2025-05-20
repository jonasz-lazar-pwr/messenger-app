# ecr/outputs.tf

output "ecr_repository_urls" {
  description = "Map of service names to ECR repository URLs."
  value = {
    for name, repo in aws_ecr_repository.services :
    name => repo.repository_url
  }
}

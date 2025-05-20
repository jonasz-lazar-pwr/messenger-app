# outputs.tf (root)

output "ecr_repository_urls" {
  description = "ECR repository URLs from the ecr module"
  value       = module.ecr.ecr_repository_urls
}

# frontend/outputs.tf

# Nazwa domeny (CNAME) przypisana do środowiska frontendowego EB
output "domain_name" {
  description = "Domain name of the frontend Elastic Beanstalk environment"
  value       = aws_elastic_beanstalk_environment.this.cname
}

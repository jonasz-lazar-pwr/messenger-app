# backend/outputs.tf

# Nazwa domeny (CNAME) przypisana do środowiska backendowego EB
output "domain_name" {
  description = "Domain name of the backend Elastic Beanstalk environment"
  value       = aws_elastic_beanstalk_environment.this.cname
}

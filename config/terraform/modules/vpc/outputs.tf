# Zwraca ID utworzonej sieci VPC
output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.this.id
}

# Lista ID podsieci frontendowych (np. dla Elastic Beanstalk frontend)
output "frontend_subnets_ids" {
  description = "List of frontend subnet IDs"
  value       = [aws_subnet.frontend.id, aws_subnet.frontend_alt.id]
}

# Lista ID podsieci backendowych (np. dla Elastic Beanstalk backend)
output "backend_subnets_ids" {
  description = "List of backend subnet IDs"
  value       = [aws_subnet.backend.id, aws_subnet.backend_alt.id]
}

# Lista ID podsieci przeznaczonych dla bazy danych (RDS)
output "database_subnet_ids" {
  description = "List containing the two public database subnet IDs"
  value       = [aws_subnet.database.id, aws_subnet.database_alt.id]
}

# ID grupy zabezpieczeń (Security Group) dla instancji frontendowych
output "frontend_sg_id" {
  description = "Security Group ID used by the frontend application instance"
  value       = aws_security_group.frontend.id
}

# ID grupy zabezpieczeń (Security Group) dla instancji backendowych
output "backend_sg_id" {
  description = "Security Group ID used by the backend application instance"
  value       = aws_security_group.backend.id
}

# ID grupy zabezpieczeń (Security Group) dla bazy danych (zwracane jako lista)
output "database_sg_id" {
  description = "Security Group ID used by the database application instance"
  value       = [aws_security_group.database.id]
}
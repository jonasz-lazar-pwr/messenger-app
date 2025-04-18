# rds/outputs.tf

# Adres (endpoint) instancji bazy danych
output "db_endpoint" {
  description = "The endpoint of the RDS instance"
  value       = aws_db_instance.this.address
}

# rds/variables.tf

# Nazwa bazy danych wewnątrz instancji
variable "db_name" {
  description = "Name of the database"
  type        = string
}

# Hasło do bazy danych (traktowane jako wrażliwe)
variable "db_password" {
  description = "Password for accessing the database"
  type        = string
  sensitive   = true
}

# Port bazy danych
variable "db_port" {
  description = "Port used by the database"
  type        = number
}

# Nazwa użytkownika bazy danych
variable "db_username" {
  description = "Username for accessing the database"
  type        = string
}

# Unikalny identyfikator instancji RDS
variable "db_instance_identifier" {
  description = "The name of the RDS instance"
  type        = string
}

# Nazwa grupy podsieci dla instancji RDS
variable "db_subnet_group_name" {
  description = "The DB subnet group name"
  type        = string
}

# Lista ID podsieci, w których będzie uruchomiona instancja RDS
variable "db_subnet_ids" {
  description = "List of subnet IDs for the RDS instance"
  type        = list(string)
}

# Lista grup zabezpieczeń przypisanych do instancji RDS
variable "security_group_ids" {
  description = "List of security group IDs to associate with the RDS instance"
  type        = list(string)
}

# Tagi wspólne dla wszystkich zasobów
variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
}

# vpc/variables.tf

# CIDR blok dla sieci VPC, np. "10.0.0.0/16"
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

# Nazwa (tag) dla zasobu VPC
variable "vpc_name" {
  description = "Name tag for the VPC"
  type        = string
}

# Mapa nazw podsieci do przypisanych im CIDR bloków, np. { "frontend" = "10.0.1.0/24" }
variable "subnet_cidrs" {
  description = "Map of subnet names to their CIDR blocks"
  type        = map(string)
}

# Mapa nazw podsieci do przypisanych im stref dostępności (AZ), np. { "frontend" = "us-east-1a" }
variable "availability_zones" {
  description = "Map of subnet names to their AZs"
  type        = map(string)
}

# Wspólne tagi przypisane do wszystkich zasobów
variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
}

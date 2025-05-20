# backend/variables.tf

# === Identyfikacja i środowisko ===
variable "backend_name" {                # Nazwa aplikacji Elastic Beanstalk (backend)
  description = "The name of the Elastic Beanstalk backend application"
  type        = string
}

variable "backend_env_name" {            # Nazwa środowiska Elastic Beanstalk (backend)
  description = "The name of the Elastic Beanstalk backend environment"
  type        = string
}

# === Baza danych ===
variable "db_host" {                     # Endpoint bazy danych (RDS)
  description = "The hostname for the database (RDS endpoint)"
  type        = string
}

variable "db_name" {                     # Nazwa bazy danych
  description = "The name of the database"
  type        = string
}

variable "db_port" {                     # Port używany przez bazę danych
  description = "The port number for the database"
  type        = number
}

variable "db_user" {                     # Nazwa użytkownika bazy danych
  description = "The master username for the database"
  type        = string
}

variable "db_password" {                 # Hasło użytkownika bazy danych
  description = "The master password for the database"
  type        = string
  sensitive   = true
}

# === Cognito ===
variable "cognito_client_id" {           # ID klienta Cognito
  description = "The Cognito client ID"
  type        = string
}

variable "cognito_pool_id" {             # ID puli użytkowników Cognito
  description = "The Cognito user pool ID"
  type        = string
}

variable "cognito_issuer_url" {          # Issuer URL do weryfikacji tokenów JWT
  description = "The Cognito issuer URL"
  type        = string
}

# === AWS credentials ===
variable "aws_access_key_id" {           # Klucz dostępowy AWS
  description = "The AWS access key ID for Elastic Beanstalk"
  type        = string
  sensitive   = true
}

variable "aws_secret_access_key" {       # Sekretny klucz AWS
  description = "The AWS secret access key for Elastic Beanstalk"
  type        = string
  sensitive   = true
}

variable "aws_session_token" {           # Token sesji AWS
  description = "The AWS session token for Elastic Beanstalk"
  type        = string
  sensitive   = true
}

variable "aws_region" {                  # Region AWS
  description = "AWS region to deploy resources"
  type        = string
}

# === Sieć ===
variable "vpc_id" {                      # ID sieci VPC
  description = "VPC ID to use for the backend"
  type        = string
}

variable "subnets_ids" {                 # Lista ID podsieci backendowych
  description = "List of public subnet IDs"
  type        = list(string)
}

variable "security_group_id" {           # ID grupy zabezpieczeń backendu
  description = "ID of the Security Group for backend instances"
  type        = string
}

# === Inne ===
variable "ssl_certificate_arn" {
  description = "ARN of SSL certificate "
  type        = string
}

variable "s3_bucket_name" {              # Nazwa bucketa S3
  description = "The name of the S3 bucket"
  type        = string
}

variable "allowed_origins" {             # Dozwolone originy (CORS)
  description = "The allowed origins for CORS"
  type        = string
}

variable "tags" {                        # Wspólne tagi dla wszystkich zasobów
  description = "Common tags for all resources"
  type        = map(string)
}
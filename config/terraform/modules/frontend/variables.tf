# frontend/variables.tf

# === Informacje o regionie i tagowaniu ===

variable "region" {                                 # Region AWS
  description = "AWS region"
  type        = string
}

variable "tags" {                                   # Wspólne tagi dla wszystkich zasobów
  description = "Common tags for all resources"
  type        = map(string)
}

# === Nazwy aplikacji i środowiska ===

variable "frontend_name" {                          # Nazwa aplikacji frontendowej
  description = "The name of the Elastic Beanstalk frontend application"
  type        = string
}

variable "frontend_env_name" {                      # Nazwa środowiska frontendowego EB
  description = "The name of the Elastic Beanstalk frontend environment"
  type        = string
}

# === Infrastruktura sieciowa ===

variable "vpc_id" {                                 # ID sieci VPC
  description = "VPC ID to use for the frontend"
  type        = string
}

variable "subnets_ids" {                            # Lista podsieci publicznych
  description = "List of public subnet IDs"
  type        = list(string)
}

variable "security_group_id" {                      # ID grupy zabezpieczeń dla frontendowych instancji
  description = "ID of the Security Group for frontend instances"
  type        = string
}

# === Backend ===

variable "backend_domain_name" {                    # Publiczny adres backendu
  description = "Domain name of the backend EB environment"
  type        = string
}

variable "backend_port" {                           # Port backendu
  description = "The number of backend port"
  type        = number
}

# === Cognito ===

variable "cognito_client_id" {                      # ID klienta Cognito
  description = "Cognito Client ID"
  type        = string
}

variable "cognito_pool_id" {                        # ID puli użytkowników Cognito
  description = "Cognito Pool ID"
  type        = string
}

variable "cognito_pool_domain" {                    # Domenowy adres hosted UI Cognito
  description = "Cognito Pool Domain"
  type        = string
}

variable "cognito_code" {                           # Typ odpowiedzi OAuth2 (code)
  description = "OAuth2 response type for Cognito (e.g., 'code')"
  type        = string
}

variable "cognito_scope" {                          # Zakres OAuth2 (email openid profile)
  description = "OAuth2 scope used for Cognito authentication"
  type        = string
}

# === Aplikacja frontendowa ===

variable "frontend_url" {                           # Publiczny URL aplikacji frontendowej
  description = "The base URL of this frontend environment"
  type        = string
}

# === SSL ===

variable "ssl_certificate_arn" {                    # ARN certyfikatu SSL z ACM
  description = "ARN of the SSL certificate from ACM"
  type        = string
}
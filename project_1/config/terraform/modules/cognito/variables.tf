# cognito/variables.tf

# Nazwa Cognito User Pool
variable "user_pool_name" {
  type        = string
  description = "Name of the Cognito User Pool"
}

# Nazwa klienta aplikacji (App Client) w Cognito
variable "app_client_name" {
  type        = string
  description = "Name of the Cognito User Pool App Client"
}

# Prefiks dla domeny hostowanej Cognito
variable "domain_prefix" {
  description = "Prefix for the Cognito hosted domain"
  type        = string
}

# Adres URL środowiska frontendowego – używany w redirectach i callbackach
variable "frontend_url" {
  description = "The base URL of this frontend environment"
  type        = string
}

# Tagi wspólne dla wszystkich zasobów Cognito
variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
}

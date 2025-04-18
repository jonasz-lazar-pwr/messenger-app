# cognito/main.tf

# Cognito User Pool
resource "aws_cognito_user_pool" "this" {
  name = var.user_pool_name

  # Użytkownik loguje się za pomocą e-maila
  username_attributes        = ["email"]
  auto_verified_attributes   = ["email"]

  # Atrybuty użytkownika wymagane przy rejestracji
  schema {
    attribute_data_type = "String"
    name                = "email"
    required            = true
    mutable             = true
  }

  schema {
    attribute_data_type = "String"
    name                = "family_name"
    required            = true
    mutable             = true
  }

  schema {
    attribute_data_type = "String"
    name                = "given_name"
    required            = true
    mutable             = true
  }

  # Konfiguracja tworzenia użytkownika
  admin_create_user_config {
    allow_admin_create_user_only = false
  }

  # Wyłączenie MFA
  # mfa_configuration = "OFF"

  # Wymaganie ponownej weryfikacji atrybutu e-mail przy zmianie
  user_attribute_update_settings {
    attributes_require_verification_before_update = ["email"]
  }

  tags = var.tags
}

# Cognito App Client
resource "aws_cognito_user_pool_client" "this" {
  name         = var.app_client_name
  user_pool_id = aws_cognito_user_pool.this.id

  # Adresy do przekierowań po logowaniu/wylogowaniu
  callback_urls = ["${var.frontend_url}/callback/"]         # URL, na który Cognito przekieruje po zalogowaniu
  logout_urls   = ["${var.frontend_url}/"]                  # URL, na który Cognito przekieruje po wylogowaniu

  # Ustawienia OAuth2
  allowed_oauth_flows_user_pool_client = true               # Włączenie obsługi flow OAuth2 w kliencie
  allowed_oauth_flows                  = ["code"]           # Typ flow – Authorization Code Grant
  allowed_oauth_scopes                 = ["email", "openid", "profile"]  # Zakresy uprawnień żądane przez aplikację
  supported_identity_providers         = ["COGNITO"]        # Lista providerów tożsamości (tu tylko Cognito)
  generate_secret                      = false              # Bez tajnego klucza klienta – wymagane w aplikacjach SPA

  # Dozwolone flow'y uwierzytelniania
  explicit_auth_flows = [                                   # Flow'y logowania dozwolone w kliencie
    "ALLOW_USER_PASSWORD_AUTH",                             # Login + hasło
    "ALLOW_REFRESH_TOKEN_AUTH"                              # Odświeżanie tokenów
  ]

  # Zaawansowane ustawienia bezpieczeństwa
  enable_token_revocation       = true                      # Pozwala na unieważnienie tokenów (revoke)
  prevent_user_existence_errors = "ENABLED"                 # Nie ujawniaj, czy użytkownik istnieje przy błędach

  # Uprawnienia do odczytu atrybutów użytkownika
  read_attributes = [
    "email",
    "email_verified",
    "family_name",
    "given_name"
  ]

  # Uprawnienia do zapisu atrybutów użytkownika
  write_attributes = [
    "email",
    "family_name",
    "given_name"
  ]
}

# Cognito Hosted UI Domain
resource "aws_cognito_user_pool_domain" "this" {
  domain       = var.domain_prefix                     # Prefiks subdomeny dla interfejsu logowania Cognito (Hosted UI)
  user_pool_id = aws_cognito_user_pool.this.id         # ID user poola, do którego przypisujemy domenę
}
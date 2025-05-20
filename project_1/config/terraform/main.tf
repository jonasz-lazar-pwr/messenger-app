# main.tf (root)

# Moduł odpowiedzialny za utworzenie infrastruktury sieciowej VPC
module "vpc" {
  source = "./modules/vpc"
  vpc_cidr           = var.vpc_cidr             # CIDR blok dla głównej sieci VPC (np. 10.0.0.0/16)
  vpc_name           = var.vpc_name             # Nazwa (tag) przypisana do zasobu VPC
  subnet_cidrs       = var.subnet_cidrs         # Mapowanie nazw podsieci na ich CIDR-y (np. frontend -> 10.0.1.0/24)
  availability_zones = var.availability_zones   # Mapowanie nazw podsieci na strefy dostępności (AZ)
  tags               = var.tags                 # Wspólne tagi przypisane do wszystkich zasobów związanych z VPC
}

# Moduł odpowiedzialny za utworzenie zasobu S3
module "s3" {
  source      = "./modules/s3"       # Ścieżka do lokalnego modułu odpowiedzialnego za konfigurację S3
  bucket_name = var.bucket_name      # Nazwa bucketa S3
  tags        = var.tags             # Zestaw tagów przypisanych do zasobu
}

module "cognito" {
  source = "./modules/cognito"
  user_pool_name    = var.user_pool_name     # Nazwa puli użytkowników Cognito
  app_client_name   = var.app_client_name    # Nazwa klienta aplikacji (App Client) w ramach Cognito User Pool
  domain_prefix     = var.domain_prefix      # Prefiks domeny Cognito Hosted UI
  frontend_url      = var.frontend_url       # URL frontendu (dla callback/logout URL)
  tags              = var.tags               # Wspólne tagi dla zasobów
}

module "rds" {
  source                 = "./modules/rds"
  db_subnet_group_name   = var.db_subnet_group_name         # nazwa grupy podsieci RDS
  db_subnet_ids          = module.vpc.database_subnet_ids   # lista ID podsieci RDS
  db_instance_identifier = var.db_instance_identifier       # identyfikator instancji RDS
  db_port                = var.db_port                      # port bazy danych
  db_name                = var.db_name                      # nazwa bazy danych
  db_username            = var.db_username                  # nazwa użytkownika DB
  db_password            = var.db_password                  # hasło użytkownika DB
  security_group_ids     = module.vpc.database_sg_id        # lista SG przypisanych do RDS
  tags                   = var.tags                         # wspólne tagi dla zasobów
}

module "backend" {
  source = "./modules/backend"
  # === Nazewnictwo środowiska ===
  backend_name        = var.backend_name         # Nazwa aplikacji backendowej
  backend_env_name    = var.backend_env_name     # Nazwa środowiska EB
  # === Konfiguracja bazy danych ===
  db_host             = module.rds.db_endpoint   # Endpoint RDS (adres hosta)
  db_name             = var.db_name              # Nazwa bazy danych
  db_port             = var.db_port              # Port bazy danych
  db_user             = var.db_username          # Użytkownik bazy danych
  db_password         = var.db_password          # Hasło do bazy danych
  # === Integracja z Cognito ===
  cognito_client_id   = module.cognito.cognito_client_id   # ID klienta Cognito
  cognito_pool_id     = module.cognito.cognito_pool_id     # ID puli użytkowników
  cognito_issuer_url  = var.cognito_issuer_url             # URL issuer'a do weryfikacji tokenów JWT
  # === Konfiguracja AWS ===
  aws_region          = var.aws_region            # Region AWS
  aws_access_key_id   = var.aws_access_key_id     # Klucz dostępowy AWS
  aws_secret_access_key = var.aws_secret_access_key # Sekretny klucz AWS
  aws_session_token   = var.aws_session_token     # Token sesji AWS
  # === Infrastruktura sieciowa ===
  vpc_id              = module.vpc.vpc_id               # ID sieci VPC
  subnets_ids         = module.vpc.backend_subnets_ids  # Lista podsieci backendowych
  security_group_id   = module.vpc.backend_sg_id        # ID grupy zabezpieczeń backendu
  # === Certyfikat SSL ===
  ssl_certificate_arn = var.ssl_certificate_arn    # ARN certyfikatu SSL (ACM) używanego przez Load Balancer
  s3_bucket_name      = module.s3.bucket_name     # Nazwa bucketa S3 do przechowywania plików
  allowed_origins     = var.allowed_origins       # Dozwolone originy (CORS)
  tags                = var.tags                  # Wspólne tagi dla zasobów
}

module "frontend" {
  source = "./modules/frontend"
  # === Nazewnictwo środowiska ===
  frontend_name      = var.frontend_name         # Nazwa aplikacji frontendowej
  frontend_env_name  = var.frontend_env_name     # Nazwa środowiska EB
  # === Konfiguracja AWS i tagowanie ===
  region             = var.aws_region            # Region AWS
  tags               = var.tags                  # Wspólne tagi dla zasobów
  # === Infrastruktura sieciowa ===
  vpc_id             = module.vpc.vpc_id                 # ID sieci VPC
  subnets_ids        = module.vpc.frontend_subnets_ids   # Lista podsieci frontendowych
  security_group_id  = module.vpc.frontend_sg_id         # ID grupy zabezpieczeń frontendowej
  # === Integracja z backendem ===
  backend_domain_name = module.backend.domain_name       # Publiczny adres backendu
  backend_port        = var.backend_port                 # Port używany przez backend
  # === Integracja z Cognito ===
  cognito_client_id   = module.cognito.cognito_client_id   # ID klienta Cognito
  cognito_pool_id     = module.cognito.cognito_pool_id     # ID puli użytkowników
  cognito_pool_domain = module.cognito.cognito_pool_domain # Publiczny hosted domain Cognito
  cognito_code        = var.cognito_code                   # OAuth response type ("code")
  cognito_scope       = var.cognito_scope                  # Zakresy OAuth ("email openid profile")
  # === Konfiguracja URL aplikacji ===
  frontend_url        = var.frontend_url           # Publiczny adres frontendowej aplikacji
  # === Certyfikat SSL ===
  ssl_certificate_arn = var.ssl_certificate_arn    # ARN certyfikatu SSL (ACM) używanego przez Load Balancer
}
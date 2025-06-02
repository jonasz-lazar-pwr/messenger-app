# main.tf (root)

# Moduł odpowiedzialny za utworzenie infrastruktury sieciowej VPC
module "vpc" {
  source = "./modules/vpc"
  vpc_name           = var.vpc_name           # Nazwa głównej sieci VPC
  vpc_cidr           = var.vpc_cidr           # Główny blok CIDR dla sieci VPC
  subnet_cidrs       = var.subnet_cidrs       # Bloki CIDR dla poszczególnych podsieci
  availability_zones = var.availability_zones # Strefy dostępności dla podsieci
}

module "rds" {
  source = "./modules/rds"
  db_instance_identifier = var.db_instance_identifier # Identyfikator instancji bazy danych
  db_name                = var.db_name                # Nazwa bazy danych w instancji
  db_username            = var.db_username            # Nazwa głównego użytkownika bazy danych
  db_password            = var.db_password            # Hasło głównego użytkownika bazy danych
  db_port                = var.db_port                # Port, na którym nasłuchuje baza danych

  db_subnet_ids          = module.vpc.public_subnet_ids            # Lista ID podsieci
  db_subnet_group_name   = var.db_subnet_group_name   # Nazwa grupy podsieci
  security_group_ids     = [module.vpc.security_group_id]          # Lista ID grup bezpieczeństwa
  tags                   = var.tags                                # Wspólne tagi dla zasobów
}

module "cognito" {
  source = "./modules/cognito"
  user_pool_name    = var.cognito_user_pool_name                    # Nazwa puli użytkowników Cognito
  app_client_name   = var.cognito_app_client_name                   # Nazwa klienta aplikacji (App Client) w ramach Cognito User Pool
  domain_prefix     = var.cognito_domain_prefix                     # Prefiks domeny Cognito Hosted UI
  frontend_url      = "https://${module.alb.alb_dns_names["frontend"]}" # URL frontendu (dla callback/logout URL)
  tags              = var.tags                                      # Wspólne tagi dla zasobów
}

module "s3" {
  source      = "./modules/s3"
  bucket_name = var.s3_bucket_name      # Nazwa bucketa S3
  tags        = var.tags                # Wspólne tagi dla zasobów
}

module "sns" {
  source           = "./modules/sns"
  topic_name       = var.sns_topic_name             # Nazwa tematu SNS do wysyłania powiadomień
  subscriber_email = var.sns_notification_email     # Adres email subskrybenta powiadomień z tematu SNS
  tags             = var.tags                       # Wspólne tagi dla zasobów
}

module "dynamodb_media" {
  source      = "./modules/dynamodb_media"
  table_name  = var.dynamodb_media_table_name       # Nazwa tabeli
  tags        = var.tags                            # Wspólne tagi dla zasobów
}

module "dynamodb_notification" {
  source      = "./modules/dynamodb_notification"
  table_name  = var.dynamodb_notification_table_name    # Nazwa tabeli
  tags        = var.tags                                # Wspólne tagi dla zasobów
}

module "sqs_notification_queue" {
  source     = "./modules/sqs"
  queue_name = var.sqs_notification_queue_name          # Nazwa kolejki SQS
  tags       = var.tags                                 # Wspólne tagi dla wszystkich zasobów
}

module "alb" {
  source                 = "./modules/alb"
  vpc_id                 = module.vpc.vpc_id                 # ID utworzonej sieci VPC
  subnet_ids             = module.vpc.public_subnet_ids      # Lista publicznych podsieci w VPC
  security_group_ids     = [module.vpc.security_group_id]    # Lista grup bezpieczeństwa przypisanych do ALB
  default_container_port = var.default_container_port        # Domyślny port kontenera
  ssl_certificate_arn    = var.ssl_certificate_arn           # ARN certyfikatu SSL do listenera HTTPS
  tags                   = var.tags                          # Wspólne tagi dla wszystkich zasobów
}

module "ecs_cluster" {
  source       = "./modules/ecs_cluster"
  cluster_name = var.ecs_cluster_name       # Nazwa klastra ECS
  tags         = var.tags         # Wspólne tagi dla zasobów
}

module "ecr" {
  source   = "./modules/ecr"
  services = var.services     # Lista nazw serwisów w repozytorium ECR
  tags     = var.tags         # Wspólne tagi dla zasobów
}

module "ecs_services" {
  source = "./modules/ecs"

  for_each = local.ecs_services                                   # Pętla po wszystkich serwisach ECS

  service_name          = each.key                                # Nazwa serwisu ECS (np. "frontend", "media-service")
  image                 = each.value.image                        # URL obrazu Docker z ECR
  alb_target_group_arn  = each.value.alb_target_group_arn         # ARN grupy docelowej ALB
  enable_load_balancer  = each.value.enable_load_balancer         # Czy serwis ma być podłączony do ALB
  environment           = each.value.environment                  # Lista zmiennych środowiskowych

  cluster_id            = module.ecs_cluster.ecs_cluster_name     # Nazwa klastra ECS, do którego należy serwis
  aws_region            = var.aws_region                          # Region AWS, w którym tworzony jest serwis
  subnet_ids            = module.vpc.public_subnet_ids            # Lista ID podsieci dla serwisu
  security_group_id     = module.vpc.security_group_id            # ID grupy bezpieczeństwa przypisanej do serwisu
  execution_role_arn    = var.iam_role_arn                        # ARN roli wykonawczej IAM dla zadań ECS

  container_port        = var.default_container_port              # Port, na którym nasłuchuje kontener
  cpu                   = var.default_cpu                         # Ilość CPU przydzielona dla zadania
  memory                = var.default_memory                      # Ilość pamięci RAM przydzielona dla zadania
  desired_count         = var.default_desired_count               # Liczba instancji zadania do uruchomienia
}

module "api_gateway" {
  source = "./modules/api_gateway"

  lambda_arns         = module.chat_service.lambda_function_arns                  # Mapowanie ścieżek HTTP do funkcji Lambda
  cognito_pool_id     = module.cognito.pool_id                                    # ID puli użytkowników Cognito
  cognito_issuer_url  = "https://cognito-idp.${var.aws_region}.amazonaws.com/${module.cognito.pool_id}" # URL issuer'a tokenów JWT Cognito
  tags                = var.tags         # Wspólne tagi dla zasobów
}

module "chat_service" {
  source = "./modules/lambda"

  # Parametry połączenia do bazy danych
  psql_host     = module.rds.db_endpoint           # Adres hosta RDS (endpoint)
  psql_port     = var.db_port                      # Port bazy danych
  psql_user     = var.db_username                  # Nazwa użytkownika bazy danych
  psql_password = var.db_password                  # Hasło użytkownika bazy danych
  psql_name     = var.db_name                      # Nazwa bazy danych

  # Konfiguracja AWS Cognito dla weryfikacji JWT
  cognito_pool_id    = module.cognito.pool_id                                # ID puli użytkowników Cognito
  cognito_client_id  = module.cognito.pool_client_id                         # ID klienta aplikacji w Cognito
  cognito_issuer_url = "https://cognito-idp.${var.aws_region}.amazonaws.com/${module.cognito.pool_id}"  # Issuer URL do walidacji tokenów

   # Rola wykonawcza IAM przypisana funkcjom Lambda
  iam_role_arn = var.iam_role_arn

  # Adres hosta media-service dostępny przez ALB
  media_service_host = module.alb.alb_dns_names["media_service"]

  # Konfiguracja notyfikacji
  sqs_notification_queue_url = module.sqs_notification_queue.queue_url       # URL kolejki SQS do wysyłania zdarzeń
  sns_notification_email     = var.sns_notification_email                    # E-mail do powiadomień SNS
}

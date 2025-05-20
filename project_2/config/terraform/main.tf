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
  db_instance_identifier = var.chat_service_db_instance_identifier # Identyfikator instancji bazy danych
  db_name                = var.chat_service_db_name                # Nazwa bazy danych w instancji
  db_username            = var.chat_service_db_username            # Nazwa głównego użytkownika bazy danych
  db_password            = var.chat_service_db_password            # Hasło głównego użytkownika bazy danych
  db_port                = var.chat_service_db_port                # Port, na którym nasłuchuje baza danych

  db_subnet_ids          = module.vpc.public_subnet_ids            # Lista ID podsieci
  db_subnet_group_name   = var.chat_service_db_subnet_group_name   # Nazwa grupy podsieci
  security_group_ids     = [module.vpc.security_group_id]          # Lista ID grup bezpieczeństwa
  tags                   = var.tags                                # Wspólne tagi dla zasobów
}

module "cognito" {
  source = "./modules/cognito"
  user_pool_name    = var.cognito_user_pool_name                    # Nazwa puli użytkowników Cognito
  app_client_name   = var.cognito_app_client_name                   # Nazwa klienta aplikacji (App Client) w ramach Cognito User Pool
  domain_prefix     = var.cognito_domain_prefix                     # Prefiks domeny Cognito Hosted UI
  frontend_url      = "https://${module.alb_frontend.alb_dns_name}" # URL frontendu (dla callback/logout URL)
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

module "alb_frontend" {
  source             = "./modules/alb"
  service_name       = "frontend"                     # Nazwa serwisu, dla którego tworzony jest ALB
  vpc_id             = module.vpc.vpc_id              # ID VPC, w której zostanie utworzony ALB
  subnet_ids         = module.vpc.public_subnet_ids   # Podsieci publiczne
  security_group_ids = [module.vpc.security_group_id] # Grupa bezpieczeństwa

  container_port     = 80                             # Port kontenera frontendu
  is_internal        = false                          # Typ ALB: publiczny
  listener_protocol  = "HTTPS"                        # Protokół nasłuchiwacza ALB
  listener_port      = 443                            # Port nasłuchiwacza ALB
  ssl_certificate_arn = var.ssl_certificate_arn       # ARN certyfikatu SSL dla HTTPS
  health_check_path    = "/"                          # Ścieżka sprawdzania kondycji kontenera
  health_check_matcher = "200"                        # Oczekiwany kod odpowiedzi z kontenera
  tags                 = var.tags                     # Wspólne tagi dla zasobów
}

module "alb_api_gateway" {
  source             = "./modules/alb"
  service_name       = "api-gateway"                  # Nazwa serwisu, dla którego tworzony jest ALB
  vpc_id             = module.vpc.vpc_id              # ID VPC, w której zostanie utworzony ALB
  subnet_ids         = module.vpc.public_subnet_ids   # Podsieci publiczne
  security_group_ids = [module.vpc.security_group_id] # Grupa bezpieczeństwa

  container_port     = var.default_container_port     # Port kontenera API Gateway
  is_internal        = false                          # Typ ALB: publiczny
  listener_protocol  = "HTTPS"                        # Protokół nasłuchiwacza ALB
  listener_port      = 443                            # Port nasłuchiwacza ALB
  ssl_certificate_arn = var.ssl_certificate_arn       # ARN certyfikatu SSL dla HTTPS
  health_check_path    = "/healthz/"                  # Ścieżka sprawdzania kondycji kontenera
  health_check_matcher = "200-399"                    # Oczekiwane kody odpowiedzi z kontenera
  tags               = var.tags                       # Wspólne tagi dla zasobów
}

module "alb_chat_service" {
  source             = "./modules/alb"
  service_name       = "chat-service"                 # Nazwa serwisu, dla którego tworzony jest ALB
  vpc_id             = module.vpc.vpc_id              # ID VPC, w której zostanie utworzony ALB
  subnet_ids         = module.vpc.public_subnet_ids   # Podsieci publiczne
  security_group_ids = [module.vpc.security_group_id] # Grupa bezpieczeństwa

  container_port     = var.default_container_port     # Port kontenera Chat Service
  is_internal        = true                           # Typ ALB: wewnętrzny
  listener_protocol  = "HTTP"                         # Protokół nasłuchiwacza ALB
  listener_port      = var.default_container_port     # Port nasłuchiwacza ALB
  health_check_path    = "/healthz/"                  # Ścieżka sprawdzania kondycji kontenera
  health_check_matcher = "200-399"                    # Oczekiwane kody odpowiedzi z kontenera
  tags                 = var.tags                     # Wspólne tagi dla zasobów
}

module "alb_notification_service" {
  source             = "./modules/alb"
  service_name       = "notification-service"         # Nazwa serwisu, dla którego tworzony jest ALB
  vpc_id             = module.vpc.vpc_id              # ID VPC, w której zostanie utworzony ALB
  subnet_ids         = module.vpc.public_subnet_ids   # Podsieci publiczne
  security_group_ids = [module.vpc.security_group_id] # Grupa bezpieczeństwa

  container_port     = var.default_container_port     # Port kontenera Notification Service
  is_internal        = true                           # Typ ALB: wewnętrzny
  listener_protocol  = "HTTP"                         # Protokół nasłuchiwacza ALB
  listener_port      = var.default_container_port     # Port nasłuchiwacza ALB
  health_check_path    = "/healthz/"                  # Ścieżka sprawdzania kondycji kontenera
  health_check_matcher = "200-399"                    # Oczekiwane kody odpowiedzi z kontenera
  tags                 = var.tags                     # Wspólne tagi dla zasobów
}

module "alb_media_service" {
  source             = "./modules/alb"
  service_name       = "media-service"                # Nazwa serwisu, dla którego tworzony jest ALB
  vpc_id             = module.vpc.vpc_id              # ID VPC, w której zostanie utworzony ALB
  subnet_ids         = module.vpc.public_subnet_ids   # Podsieci publiczne
  security_group_ids = [module.vpc.security_group_id] # Grupa bezpieczeństwa

  container_port     = var.default_container_port     # Port kontenera Media Service
  is_internal        = true                           # Typ ALB: wewnętrzny
  listener_protocol  = "HTTP"                         # Protokół nasłuchiwacza ALB
  listener_port      = var.default_container_port     # Port nasłuchiwacza ALB
  health_check_path    = "/healthz/"                  # Ścieżka sprawdzania kondycji kontenera
  health_check_matcher = "200-399"                    # Oczekiwane kody odpowiedzi z kontenera
  tags                 = var.tags                     # Wspólne tagi dla zasobów
}

module "ecs_cluster" {
  source       = "./modules/ecs_cluster"
  cluster_name = "messenger-app-cluster"              # Nazwa klastra ECS
}

module "ecr" {
  source        = "./modules/ecr"
  services = [                    # Lista nazw serwisów, dla których zostaną utworzone repozytoria obrazów Docker
  "frontend",
  "api-gateway",
  "chat-service",
  "media-service",
  "notification-service"
  ]
  tags          = var.tags
}

module "ecs_frontend" {
  source = "./modules/ecs"
  service_name        = "frontend"                                  # Nazwa serwisu ECS
  aws_region          = var.aws_region                              # Region AWS, w którym tworzony jest serwis
  cluster_id          = module.ecs_cluster.ecs_cluster_name         # Nazwa klastra ECS, do którego należy serwis
  image               = module.ecr.ecr_repository_urls["frontend"]  # URL obrazu Docker z ECR

  subnet_ids          = module.vpc.public_subnet_ids                # Lista ID podsieci dla serwisu
  security_group_id   = module.vpc.security_group_id                # ID grupy bezpieczeństwa dla serwisu
  execution_role_arn  = var.ecs_task_execution_role_arn             # ARN roli wykonawczej IAM dla zadań ECS
  alb_target_group_arn = module.alb_frontend.alb_target_group_arn   # ARN grupy docelowej ALB

  container_port      = 80                                          # Port, na którym nasłuchuje kontener
  cpu                 = var.default_cpu                             # Domyślna ilość CPU dla zadania
  memory              = var.default_memory                          # Domyślna ilość pamięci dla zadania
  desired_count       = var.default_desired_count                   # Początkowa liczba uruchomionych zadań

  environment = [
    {
      name  = "API_URL"
      value = "https://${module.alb_api_gateway.alb_dns_name}"
    },
    {
      name = "COGNITO_LOGOUT_URL"
      value = "https://${module.cognito.cognito_pool_domain}.auth.${var.aws_region}.amazoncognito.com/logout"
    },
    {
      name = "COGNITO_AUTHORITY"
      value = "https://cognito-idp.${var.aws_region}.amazonaws.com/${module.cognito.cognito_pool_id}"
    },
    {
      name = "COGNITO_REDIRECT_URL"
      value = "https://${module.alb_frontend.alb_dns_name}/callback/"
    },
    {
      name = "COGNITO_POST_LOGOUT_URI",
      value = "https://${module.alb_frontend.alb_dns_name}/"
    },
    {
      name = "COGNITO_CLIENT_ID"
      value = module.cognito.cognito_client_id
    },
    {
      name = "COGNITO_SCOPE"
      value = var.cognito_allowed_scopes
    },
    {
      name = "COGNITO_RESPONSE_TYPE"
      value = var.cognito_response_type
    }
  ]
}

module "ecs_api_gateway" {
  source = "./modules/ecs"
  service_name        = "api-gateway"                                   # Nazwa serwisu ECS
  aws_region          = var.aws_region                                  # Region AWS, w którym tworzony jest serwis
  cluster_id          = module.ecs_cluster.ecs_cluster_name             # Nazwa klastra ECS, do którego należy serwis
  image               = module.ecr.ecr_repository_urls["api-gateway"]   # URL obrazu Docker z ECR

  subnet_ids          = module.vpc.public_subnet_ids                    # Lista ID podsieci dla serwisu
  security_group_id   = module.vpc.security_group_id                    # ID grupy bezpieczeństwa dla serwisu
  execution_role_arn  = var.ecs_task_execution_role_arn                 # ARN roli wykonawczej IAM dla zadań ECS
  alb_target_group_arn = module.alb_api_gateway.alb_target_group_arn    # ARN grupy docelowej ALB

  container_port      = var.default_container_port                      # Port, na którym nasłuchuje kontener
  cpu                 = var.default_cpu                                 # Domyślna ilość CPU dla zadania
  memory              = var.default_memory                              # Domyślna ilość pamięci dla zadania
  desired_count       = var.default_desired_count                       # Początkowa liczba uruchomionych zadań

  environment = [
    {
      name  = "CHAT_SERVICE_HOST"
      value = module.alb_chat_service.alb_dns_name
    },
    {
      name  = "CHAT_SERVICE_PORT"
      value = var.default_container_port
    },
    {
      name  = "COGNITO_ISSUER_URL"
      value = var.cognito_issuer_url
    },
    {
      name  = "COGNITO_POOL_ID"
      value = module.cognito.cognito_pool_id
    },
    {
      name  = "COGNITO_CLIENT_ID"
      value = module.cognito.cognito_client_id
    },
    {
      name  = "CORS_ALLOW_ORIGINS"
      value = var.cors_allow_origins
    }
  ]
}

module "ecs_chat_service" {
  source = "./modules/ecs"
  service_name       = "chat-service"                                   # Nazwa serwisu ECS
  aws_region          = var.aws_region                                  # Region AWS, w którym tworzony jest serwis
  cluster_id          = module.ecs_cluster.ecs_cluster_name             # Nazwa klastra ECS, do którego należy serwis
  image              = module.ecr.ecr_repository_urls["chat-service"]   # URL obrazu Docker z ECR

  subnet_ids         = module.vpc.public_subnet_ids                     # Lista ID podsieci dla serwisu
  security_group_id  = module.vpc.security_group_id                     # ID grupy bezpieczeństwa dla serwisu
  execution_role_arn = var.ecs_task_execution_role_arn                  # ARN roli wykonawczej IAM dla zadań ECS
  alb_target_group_arn = module.alb_chat_service.alb_target_group_arn   # ARN grupy docelowej ALB

  container_port      = var.default_container_port                      # Port, na którym nasłuchuje kontener
  cpu                 = var.default_cpu                                 # Domyślna ilość CPU dla zadania
  memory              = var.default_memory                              # Domyślna ilość pamięci dla zadania
  desired_count       = var.default_desired_count                       # Początkowa liczba uruchomionych zadań

  environment = [
    {
      name  = "PSQL_HOST"
      value = module.rds.db_endpoint
    },
    {
      name  = "PSQL_PORT"
      value = var.chat_service_db_port
    },
    {
      name  = "PSQL_USER"
      value = var.chat_service_db_username
    },
    {
      name  = "PSQL_PASSWORD"
      value = var.chat_service_db_password
    },
    {
      name  = "PSQL_NAME"
      value = var.chat_service_db_name
    },
    {
      name  = "NOTIFICATION_SERVICE_HOST"
      value = module.alb_notification_service.alb_dns_name
    },
    {
      name  = "NOTIFICATION_SERVICE_PORT"
      value = var.default_container_port
    },
    {
      name  = "NOTIFICATION_RECEIVER_EMAIL"
      value = var.notification_receiver_email
    },
    {
      name  = "MEDIA_SERVICE_HOST"
      value = module.alb_media_service.alb_dns_name
    },
    {
      name  = "MEDIA_SERVICE_PORT"
      value = var.default_container_port
    },
    {
      name  = "CORS_ALLOW_ORIGINS"
      value = var.cors_allow_origins
    }
  ]
}

module "ecs_media_service" {
  source = "./modules/ecs"
  service_name        = "media-service"                                   # Nazwa serwisu ECS
  aws_region          = var.aws_region                                    # Region AWS, w którym tworzony jest serwis
  cluster_id          = module.ecs_cluster.ecs_cluster_name               # Nazwa klastra ECS, do którego należy serwis
  image               = module.ecr.ecr_repository_urls["media-service"]   # URL obrazu Docker z ECR

  subnet_ids          = module.vpc.public_subnet_ids                      # Lista ID podsieci dla serwisu
  security_group_id   = module.vpc.security_group_id                      # ID grupy bezpieczeństwa dla serwisu
  execution_role_arn  = var.ecs_task_execution_role_arn                   # ARN roli wykonawczej IAM dla zadań ECS
  alb_target_group_arn = module.alb_media_service.alb_target_group_arn    # ARN grupy docelowej ALB

  container_port      = var.default_container_port                        # Port, na którym nasłuchuje kontener
  cpu                 = var.default_cpu                                   # Domyślna ilość CPU dla zadania
  memory              = var.default_memory                                # Domyślna ilość pamięci dla zadania
  desired_count       = var.default_desired_count                         # Początkowa liczba uruchomionych zadań

  environment = [
    {
      name  = "AWS_REGION"
      value = var.aws_region
    },
    {
      name  = "AWS_S3_BUCKET_NAME"
      value = var.s3_bucket_name
    },
    {
      name  = "AWS_DYNAMODB_MEDIA_TABLE_NAME"
      value = var.dynamodb_media_table_name
    },
    {
      name  = "AWS_ACCESS_KEY_ID"
      value = var.aws_access_key_id
    },
    {
      name  = "AWS_SECRET_ACCESS_KEY"
      value = var.aws_secret_access_key
    },
    {
      name  = "AWS_SESSION_TOKEN"
      value = var.aws_session_token
    },
    {
      name  = "CORS_ALLOW_ORIGINS"
      value = var.cors_allow_origins
    }
  ]
}

module "ecs_notification_service" {
  source = "./modules/ecs"
  service_name        = "notification-service"                                # Nazwa serwisu ECS
  aws_region          = var.aws_region                                        # Region AWS, w którym tworzony jest serwis
  cluster_id          = module.ecs_cluster.ecs_cluster_name                   # Nazwa klastra ECS, do którego należy serwis
  image               = module.ecr.ecr_repository_urls["notification-service"] # URL obrazu Docker z ECR

  subnet_ids          = module.vpc.public_subnet_ids                          # Lista ID podsieci dla serwisu
  security_group_id   = module.vpc.security_group_id                          # ID grupy bezpieczeństwa dla serwisu
  execution_role_arn  = var.ecs_task_execution_role_arn                       # ARN roli wykonawczej IAM dla zadań ECS
  alb_target_group_arn = module.alb_notification_service.alb_target_group_arn # ARN grupy docelowej ALB

  container_port      = var.default_container_port                          # Port, na którym nasłuchuje kontener
  cpu                 = var.default_cpu                                     # Domyślna ilość CPU dla zadania
  memory              = var.default_memory                                  # Domyślna ilość pamięci dla zadania
  desired_count       = var.default_desired_count                           # Początkowa liczba uruchomionych zadań

  environment = [
    {
      name  = "AWS_REGION"
      value = var.aws_region
    },
    {
      name  = "AWS_SNS_TOPIC_ARN"
      value = module.sns.topic_arn
    },
    {
      name  = "AWS_DYNAMODB_NOTIFICATION_TABLE_NAME"
      value = var.dynamodb_notification_table_name
    },
    {
      name  = "AWS_ACCESS_KEY_ID"
      value = var.aws_access_key_id
    },
    {
      name  = "AWS_SECRET_ACCESS_KEY"
      value = var.aws_secret_access_key
    },
    {
      name  = "AWS_SESSION_TOKEN"
      value = var.aws_session_token
    },
    {
      name  = "CORS_ALLOW_ORIGINS"
      value = var.cors_allow_origins
    }
  ]
}

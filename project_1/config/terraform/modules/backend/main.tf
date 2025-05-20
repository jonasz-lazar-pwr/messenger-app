# backend/main.tf

# --- Aplikacja Elastic Beanstalk ---
resource "aws_elastic_beanstalk_application" "this" {
  name = var.backend_name                      # Nazwa aplikacji
  tags = var.tags                              # Tagi wspólne
}

# --- Wersja aplikacji (ZIP z S3) ---
resource "aws_elastic_beanstalk_application_version" "backend_zip" {
  name        = "deploy-v1"                    # Label wersji
  application = aws_elastic_beanstalk_application.this.name
  bucket      = "messenger-app-artifacts"      # Nazwa bucketa z ZIP-em
  key         = "messenger-app-backend.zip"    # Ścieżka do ZIP-a
}

# --- Środowisko Elastic Beanstalk dla backendu ---
resource "aws_elastic_beanstalk_environment" "this" {
  name                = var.backend_env_name                                    # Nazwa środowiska EB
  application         = aws_elastic_beanstalk_application.this.name            # Przypisana aplikacja EB
  solution_stack_name = "64bit Amazon Linux 2 v4.1.0 running Docker"           # Typ środowiska (system operacyjny i platforma)
  version_label       = aws_elastic_beanstalk_application_version.backend_zip.name  # Wersja aplikacji
  tags                = var.tags                                               # Wspólne tagi

  # --- Ustawienia podstawowe (IAM, instancje, VPC) ---
  setting {
    # Blok ustawień
    namespace = "aws:elasticbeanstalk:environment"
    # Przestrzeń nazw
    name      = "ServiceRole"
    # Nazwa ustawienia
    value     = "LabRole"                                                     # Rola serwisowa EB
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "LabInstanceProfile"                                          # IAM Profile dla instancji EC2
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "VPCId"
    value     = var.vpc_id                                                    # ID VPC
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "Subnets"
    value     = join(",", var.subnets_ids)                                    # Lista podsieci
  }

  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MinSize"
    value     = "1"                                                           # Minimalna liczba instancji
  }

  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MaxSize"
    value     = "1"                                                           # Maksymalna liczba instancji
  }

  setting {
    namespace = "aws:ec2:instances"
    name      = "InstanceTypes"
    value     = "t3.micro"                                                   # Typ instancji EC2
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "ELBSubnets"
    value     = join(",", var.subnets_ids)                                    # Podsieci dla ELB
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "SecurityGroups"
    value     = var.security_group_id                                         # ID SG przypisanej do instancji
  }

  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "EnvironmentType"
    value     = "LoadBalanced"                                               # Środowisko z ELB
  }

  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "LoadBalancerType"
    value     = "application"                                                # Typ ELB: Application Load Balancer
  }

  # --- HTTPS Listener (port 443) ---
  setting {
    namespace = "aws:elbv2:listener:443"
    name      = "ListenerEnabled"
    value     = "true"                                                       # Włączony listener
  }

  setting {
    namespace = "aws:elbv2:listener:443"
    name      = "Protocol"
    value     = "HTTPS"                                                      # Protokół
  }

  setting {
    namespace = "aws:elbv2:listener:443"
    name      = "SSLPolicy"
    value     = "ELBSecurityPolicy-2016-08"                                  # Polityka SSL
  }

  setting {
    namespace = "aws:elbv2:listener:443"
    name      = "SSLCertificateArns"
    value     = var.ssl_certificate_arn
  }

  # --- HTTP Listener (port 80) ---
  setting {
    namespace = "aws:elbv2:listener:80"
    name      = "ListenerEnabled"
    value     = "true"                                                       # Włączony listener
  }

  setting {
    namespace = "aws:elbv2:listener:80"
    name      = "Protocol"
    value     = "HTTP"                                                       # Protokół
  }

    # --- Monitorowanie i logowanie w CloudWatch ---

  # Publikowanie logów z instancji EC2 do EB (niezbędne dla streamowania logów do CloudWatch)
  setting {
    namespace = "aws:elasticbeanstalk:hostmanager"
    name      = "LogPublicationControl"
    value     = "true"
  }

  # Włączenie streamowania logów z instancji do CloudWatch Logs
  setting {
    namespace = "aws:elasticbeanstalk:cloudwatch:logs"
    name      = "StreamLogs"
    value     = "true"
  }

  # Określenie ile dni mają być przechowywane logi w CloudWatch Logs
  setting {
    namespace = "aws:elasticbeanstalk:cloudwatch:logs"
    name      = "RetentionInDays"
    value     = "7"
  }

  # Automatyczne usuwanie logów po usunięciu środowiska EB
  setting {
    namespace = "aws:elasticbeanstalk:cloudwatch:logs"
    name      = "DeleteOnTerminate"
    value     = "true"
  }

  # --- Zmienne środowiskowe: baza danych ---
  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DB_NAME"
    value     = var.db_name
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DB_USER"
    value     = var.db_user
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DB_PASSWORD"
    value     = var.db_password
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DB_HOST"
    value     = var.db_host
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DB_PORT"
    value     = var.db_port
  }

  # --- Zmienne środowiskowe: Cognito ---
  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "COGNITO_CLIENT_ID"
    value     = var.cognito_client_id
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "COGNITO_POOL_ID"
    value     = var.cognito_pool_id
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "COGNITO_ISSUER_URL"
    value     = var.cognito_issuer_url
  }

  # --- Zmienne środowiskowe: dostęp AWS ---
  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "AWS_ACCESS_KEY_ID"
    value     = var.aws_access_key_id
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "AWS_SECRET_ACCESS_KEY"
    value     = var.aws_secret_access_key
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "AWS_SESSION_TOKEN"
    value     = var.aws_session_token
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "AWS_REGION"
    value     = var.aws_region
  }

  # --- Zmienne środowiskowe: inne ---
  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "AWS_S3_BUCKET_NAME"
    value     = var.s3_bucket_name
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "ALLOWED_ORIGINS"
    value     = var.allowed_origins
  }
}

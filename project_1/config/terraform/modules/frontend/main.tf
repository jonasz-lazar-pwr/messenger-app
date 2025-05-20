# frontend/main.tf

# === Aplikacja Elastic Beanstalk ===
resource "aws_elastic_beanstalk_application" "this" {
  name = var.frontend_name               # Nazwa aplikacji frontendowej
  tags = var.tags                        # Wspólne tagi
}

# === Wersja aplikacji (ZIP z S3) ===
resource "aws_elastic_beanstalk_application_version" "frontend_zip" {
  name        = "deploy-v1"              # Etykieta wersji
  application = aws_elastic_beanstalk_application.this.name
  bucket      = "messenger-app-artifacts"       # Bucket z paczką ZIP
  key         = "messenger-app-frontend.zip"     # Nazwa pliku ZIP
}

# === Środowisko Elastic Beanstalk dla frontendu ===
resource "aws_elastic_beanstalk_environment" "this" {
  name                = var.frontend_env_name                                    # Nazwa środowiska EB
  application         = aws_elastic_beanstalk_application.this.name             # Przypisana aplikacja
  solution_stack_name = "64bit Amazon Linux 2 v4.1.0 running Docker"            # Stos technologiczny
  version_label       = aws_elastic_beanstalk_application_version.frontend_zip.name  # Wersja aplikacji
  tags                = var.tags                                                 # Wspólne tagi

  # === Konfiguracja EB: IAM, VPC, instancje, autoskalowanie ===
  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "ServiceRole"
    value     = "LabRole"                         # Rola serwisowa EB
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "LabInstanceProfile"              # IAM profile dla instancji EC2
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "VPCId"
    value     = var.vpc_id                        # ID VPC
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "Subnets"
    value     = join(",", var.subnets_ids)        # Lista podsieci
  }

  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MinSize"
    value     = "1"                               # Min liczba instancji
  }

  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MaxSize"
    value     = "1"                               # Max liczba instancji
  }

  setting {
    namespace = "aws:ec2:instances"
    name      = "InstanceTypes"
    value     = "t3.micro"                        # Typ instancji EC2
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "ELBSubnets"
    value     = join(",", var.subnets_ids)        # Podsieci dla ELB
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "SecurityGroups"
    value     = var.security_group_id             # SG przypisana do instancji
  }

  # === Load Balancer (Application Load Balancer) ===
  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "EnvironmentType"
    value     = "LoadBalanced"                    # Środowisko z ELB
  }

  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "LoadBalancerType"
    value     = "application"                     # Typ ELB: ALB
  }

  # === HTTPS Listener (port 443) ===
  setting {
    namespace = "aws:elbv2:listener:443"
    name      = "ListenerEnabled"
    value     = "true"                            # Listener HTTPS aktywny
  }

  setting {
    namespace = "aws:elbv2:listener:443"
    name      = "Protocol"
    value     = "HTTPS"                           # HTTPS
  }

  setting {
    namespace = "aws:elbv2:listener:443"
    name      = "SSLPolicy"
    value     = "ELBSecurityPolicy-2016-08"       # Polityka SSL
  }

  setting {
    namespace = "aws:elbv2:listener:443"
    name      = "SSLCertificateArns"
    value     = var.ssl_certificate_arn           # Certyfikat z ACM
  }

  # === HTTP Listener (port 80) ===
  setting {
    namespace = "aws:elbv2:listener:80"
    name      = "ListenerEnabled"
    value     = "true"                            # Listener HTTP aktywny
  }

  setting {
    namespace = "aws:elbv2:listener:80"
    name      = "Protocol"
    value     = "HTTP"                            # HTTP
  }

  # === Zmienne środowiskowe: Backend i Cognito ===
  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "API_URL"
    value     = "https://${var.backend_domain_name}"  # URL API (backend)
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "BACKEND_HOST"
    value     = var.backend_domain_name           # Host backendu (bez https)
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "BACKEND_PORT"
    value     = var.backend_port                  # Port backendu
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "CLIENT_ID"
    value     = var.cognito_client_id             # ID klienta Cognito
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "COGNITO_AUTHORITY"
    value     = "https://cognito-idp.${var.region}.amazonaws.com/${var.cognito_pool_id}"  # URL issuer
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "COGNITO_LOGOUT_URL"
    value     = "https://${var.cognito_pool_domain}.auth.${var.region}.amazoncognito.com/logout"  # Logout URL
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "RESPONSE_TYPE"
    value     = var.cognito_code                  # Typ odpowiedzi OAuth2 (code)
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "SCOPE"
    value     = var.cognito_scope                 # Zakres OAuth2
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "POST_LOGOUT_URI"
    value     = "${var.frontend_url}/"            # URL po wylogowaniu
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "REDIRECT_URL"
    value     = "${var.frontend_url}/callback/"   # URL po zalogowaniu
  }
}
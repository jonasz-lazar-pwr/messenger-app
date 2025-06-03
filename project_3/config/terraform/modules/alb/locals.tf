# alb/locals.tf

locals {
  alb_configs = {
    # Konfiguracja dla serwisu frontend
    frontend = {
      service_name         = "frontend"                    # Nazwa serwisu
      is_internal          = false                         # ALB publiczny (false) lub wewnętrzny (true)
      listener_protocol    = "HTTPS"                       # Protokół nasłuchiwania
      listener_port        = 443                           # Port, na którym nasłuchuje listener
      ssl_certificate_arn = var.ssl_certificate_arn        # ARN certyfikatu SSL do obsługi HTTPS
      health_check_path    = "/"                           # Ścieżka do sprawdzania kondycji instancji
      health_check_matcher = "200"                         # Oczekiwany kod HTTP dla zdrowej odpowiedzi
    }

    # Konfiguracja dla serwisu media-service
    media_service = {
      service_name         = "media-service"               # Nazwa serwisu
      is_internal          = false                         # ALB publiczny
      listener_protocol    = "HTTP"                        # Protokół nasłuchiwania
      listener_port        = var.default_container_port    # Port, na którym nasłuchuje listener
      ssl_certificate_arn = null                           # Brak certyfikatu – nie używa HTTPS
      health_check_path    = "/healthz"                    # Ścieżka do sprawdzania kondycji instancji
      health_check_matcher = "200-399"                     # Zakres kodów HTTP uznawanych za zdrowe
    }
  }
}

# alb/main.tf

resource "aws_lb" "this" {
  for_each                   = local.alb_configs

  name                       = "${each.value.service_name}-alb"      # Nazwa Load Balancera (na podstawie nazwy serwisu)
  load_balancer_type         = "application"                         # Typ Load Balancera – ALB
  subnets                    = var.subnet_ids                        # Lista ID podsieci, w których działa ALB
  security_groups            = var.security_group_ids                # Lista ID grup bezpieczeństwa przypisanych do ALB
  enable_deletion_protection = false                                 # Wyłączenie ochrony przed usunięciem
  internal                   = each.value.is_internal                # Czy ALB ma być wewnętrzny (true) czy publiczny (false)
  tags                       = var.tags                              # Wspólne tagi przypisane do ALB
}

resource "aws_lb_target_group" "this" {
  for_each    = local.alb_configs

  name        = "${each.value.service_name}-tg"                      # Nazwa grupy docelowej (Target Group)
  port        = var.default_container_port                           # Port, na którym kontenery nasłuchują
  protocol    = "HTTP"                                               # Protokół używany przez grupę docelową
  target_type = "ip"                                                 # Typ celu – adres IP kontenera
  vpc_id      = var.vpc_id                                           # ID sieci VPC

  health_check {
    path                = each.value.health_check_path               # Ścieżka wykorzystywana do sprawdzania kondycji kontenerów
    interval            = 120                                        # Odstęp (w sekundach) między sprawdzeniami
    timeout             = 5                                          # Limit czasu odpowiedzi (w sekundach)
    healthy_threshold   = 2                                          # Liczba poprawnych odpowiedzi potrzebna do uznania za zdrowy
    unhealthy_threshold = 2                                          # Liczba błędnych odpowiedzi potrzebna do uznania za niezdrowy
    matcher             = each.value.health_check_matcher           # Kody HTTP uznawane za oznaki zdrowia
  }
}

resource "aws_lb_listener" "this" {
  for_each = local.alb_configs

  load_balancer_arn = aws_lb.this[each.key].arn                      # ARN Load Balancera przypisanego do listenera
  port              = each.value.listener_port                       # Port, na którym listener nasłuchuje
  protocol          = each.value.listener_protocol                   # Protokół (HTTP lub HTTPS)
  ssl_policy        = each.value.listener_protocol == "HTTPS" ? "ELBSecurityPolicy-2016-08" : null  # Polityka SSL dla HTTPS
  certificate_arn   = each.value.listener_protocol == "HTTPS" ? each.value.ssl_certificate_arn : null # Certyfikat SSL (tylko dla HTTPS)

  default_action {
    type             = "forward"                                     # Domyślna akcja – przekierowanie do target group
    target_group_arn = aws_lb_target_group.this[each.key].arn        # ARN grupy docelowej
  }
}

# resource "aws_lb" "this" {
#   name                       = "${var.service_name}-alb" # Nazwa Load Balancera
#   load_balancer_type         = "application"             # Typ Load Balancera
#   subnets                    = var.subnet_ids            # Lista ID podsieci, w których ALB będzie działać
#   security_groups            = var.security_group_ids    # Lista ID grup bezpieczeństwa dla ALB
#   enable_deletion_protection = false                     # Wyłączenie ochrony przed usunięciem
#   internal                   = var.is_internal           # Określa, czy ALB jest wewnętrzny czy publiczny
#   tags                       = var.tags                  # Wspólne tagi dla zasobów
# }
#
# resource "aws_lb_target_group" "this" {
#   name        = "${var.service_name}-tg"    # Nazwa grupy docelowej
#   port        = var.default_container_port  # Port, na którym kontenery w tej grupie nasłuchują
#   protocol    = "HTTP"                      # Protokół komunikacji ALB z serwisami
#   target_type = "ip"                        # Typ celu: adresy IP
#   vpc_id      = var.vpc_id                  # ID VPC dla grupy docelowej
#
#   health_check {
#     path                = var.health_check_path     # Ścieżka URL używana do sprawdzania kondycji kontenerów
#     interval            = 120                       # Czas między kolejnymi sprawdzeniami kondycji
#     timeout             = 5                         # Czas oczekiwania na odpowiedź od celu
#     healthy_threshold   = 2                         # Liczba udanych sprawdzeń do uznania kontenera za zdrowy
#     unhealthy_threshold = 2                         # Liczba nieudanych sprawdzeń do uznania kontenera za niezdrowy
#     matcher             = var.health_check_matcher  # Oczekiwane kody HTTP odpowiedzi od zdrowego kontenera
#   }
# }
#
# resource "aws_lb_listener" "this" {
#   load_balancer_arn = aws_lb.this.arn                                  # Load Balancer, do którego listener jest przypisany
#   port              = var.listener_port                                # Port, na którym listener nasłuchuje
#   protocol          = var.listener_protocol                            # Protokół listenera (HTTP lub HTTPS)
#   ssl_policy        = var.listener_protocol == "HTTPS" ? "ELBSecurityPolicy-2016-08" : null # Polityka SSL (tylko dla HTTPS)
#   certificate_arn   = var.listener_protocol == "HTTPS" ? var.ssl_certificate_arn : null     # ARN certyfikatu SSL (tylko dla HTTPS)
#
#   default_action {
#     type             = "forward"                                        # Typ akcji: przekierowanie
#     target_group_arn = aws_lb_target_group.this.arn                     # ARN grupy docelowej, do której ruch jest przekierowywany
#   }
# }

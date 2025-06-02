# ecs/main.tf

resource "aws_ecs_task_definition" "this" {
  family                   = "${var.service_name}-task"        # Nazwa rodziny zadań ECS (np. frontend-task)
  requires_compatibilities = ["FARGATE"]                       # Obsługiwany typ uruchomienia — Fargate
  network_mode             = "awsvpc"                          # Wymagany tryb sieciowy dla Fargate
  cpu                      = var.cpu                           # Przydzielona liczba jednostek CPU
  memory                   = var.memory                        # Przydzielona ilość pamięci RAM
  execution_role_arn       = var.execution_role_arn            # Rola IAM do pobierania obrazów i wysyłania logów

  container_definitions = jsonencode([{
    name      = var.service_name                               # Nazwa kontenera
    image     = var.image                                      # URI obrazu Docker (np. z ECR)
    portMappings = [{
      containerPort = var.container_port                       # Port, na którym kontener nasłuchuje
      protocol      = "tcp"                                    # Protokół komunikacji (TCP)
    }]
    environment = var.environment                              # Lista zmiennych środowiskowych

    logConfiguration = {                                       # Konfiguracja logowania do CloudWatch
      logDriver = "awslogs"
      options = {
        awslogs-group         = "/ecs/${var.service_name}"     # Grupa logów w CloudWatch Logs
        awslogs-region        = var.aws_region                 # Region AWS
        awslogs-stream-prefix = var.service_name               # Prefiks strumieni logów
      }
    }
  }])
}

resource "aws_ecs_service" "this" {
  name            = var.service_name                           # Nazwa serwisu ECS
  cluster         = var.cluster_id                             # ID klastra ECS
  task_definition = aws_ecs_task_definition.this.arn           # Używana definicja zadania
  desired_count   = var.desired_count                          # Liczba instancji zadań
  launch_type     = "FARGATE"                                  # Typ uruchomienia Fargate

  network_configuration {                                      # Konfiguracja sieci dla zadań
    subnets         = var.subnet_ids                           # Lista ID podsieci
    assign_public_ip = true                                    # Przydzielanie publicznego IP
    security_groups  = [var.security_group_id]                 # Grupa bezpieczeństwa
  }

  dynamic "load_balancer" {
    for_each = var.enable_load_balancer ? [1] : []             # Tworzenie tylko jeśli ALB ma być podpięty
    content {
      target_group_arn = var.alb_target_group_arn              # ARN grupy docelowej ALB
      container_name   = var.service_name                      # Nazwa kontenera z ruchem z ALB
      container_port   = var.container_port                    # Port, który obsługuje ruch z ALB
    }
  }
}

resource "aws_cloudwatch_log_group" "this" {
  name              = "/ecs/${var.service_name}"               # Grupa logów dla tego serwisu ECS
  retention_in_days = 7                                        # Liczba dni przechowywania logów
}

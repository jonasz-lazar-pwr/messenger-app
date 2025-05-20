# ecs/main.tf

resource "aws_ecs_task_definition" "this" {
  family                   = "${var.service_name}-task"  # Nazwa rodziny definicji zadania, np. "frontend-task"
  requires_compatibilities = ["FARGATE"]                 # Wymagana kompatybilność z typem uruchomienia Fargate
  network_mode             = "awsvpc"                    # Tryb sieciowy awsvpc, wymagany dla Fargate
  cpu                      = var.cpu                     # Ilość jednostek CPU alokowanych dla zadania
  memory                   = var.memory                  # Ilość pamięci alokowanej dla zadania
  execution_role_arn       = var.execution_role_arn      # ARN roli IAM używanej do pobierania obrazów i wysyłania logów

  container_definitions = jsonencode([                   # Definicje kontenerów w ramach zadania
    {
      name      = var.service_name                       # Nazwa kontenera
      image     = var.image                              # URL obrazu Docker z ECR
      portMappings = [{                                  # Mapowania portów kontenera
        containerPort = var.container_port               # Port, na którym aplikacja w kontenerze nasłuchuje
        protocol      = "tcp"                            # Protokół mapowania portu
      }]
      environment = var.environment                      # Lista zmiennych środowiskowych

      logConfiguration = {                               # Konfiguracja logowania dla kontenera
        logDriver = "awslogs"                            # Sterownik logów: awslogs (wysyła do CloudWatch Logs)
        options = {
          awslogs-group         = "/ecs/${var.service_name}" # Nazwa grupy logów w CloudWatch
          awslogs-region        = var.aws_region             # Region AWS
          awslogs-stream-prefix = var.service_name           # Prefiks strumieni logów
        }
      }
    }
  ])
}

resource "aws_ecs_service" "this" {
  name            = var.service_name                     # Nazwa serwisu ECS
  cluster         = var.cluster_id                       # Nazwa klastra ECS, w którym serwis jest uruchamiany
  task_definition = aws_ecs_task_definition.this.arn     # ARN definicji zadania używanej przez ten serwis
  desired_count   = var.desired_count                    # Liczba instancji zadań
  launch_type     = "FARGATE"                            # Typ uruchomienia serwisu

  network_configuration {                                # Ustawienia sieciowe dla zadań Fargate
    subnets         = var.subnet_ids                     # Podsieci dla zadań serwisu
    assign_public_ip = true                              # Automatyczne publiczne IP dla zadań
    security_groups = [var.security_group_id]            # Grupy bezpieczeństwa dla zadań
  }

  load_balancer {                                        # Integracja z Application Load Balancer
    target_group_arn = var.alb_target_group_arn          # Grupa docelowa ALB dla tego serwisu
    container_name   = var.service_name                  # Nazwa kontenera odbierającego ruch
    container_port   = var.container_port                # Port kontenera odbierającego ruch
  }
}

resource "aws_cloudwatch_log_group" "this" {
  name              = "/ecs/${var.service_name}"         # Nazwa grupy logów w CloudWatch
  retention_in_days = 7                                  # Okres przechowywania logów w dniach
}

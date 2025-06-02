# ecr/main.tf

resource "aws_ecr_repository" "services" {
  for_each = toset(var.services)                     # ECR dla każdego serwisu z listy `services`
  name                  = each.key                   # Nazwa repozytorium ECR
  image_tag_mutability  = "MUTABLE"                  # Nadpisywanie istniejących tagów obrazów (np. `latest`)
  force_delete          = true                       # Usuwanie repozytoriów nawet jeśli zawiera obrazy

  image_scanning_configuration {
    scan_on_push = true                              # Automatyczne skanowanie obrazów po ich wgraniu
  }

  tags = var.tags                                     # Wspólne tagi dla repozytoriów
}
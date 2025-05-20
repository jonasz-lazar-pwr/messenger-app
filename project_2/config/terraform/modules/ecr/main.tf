# ecr/main.tf

resource "aws_ecr_repository" "services" {
  for_each = toset(var.services)             # Pętla tworząca repozytorium dla każdej nazwy serwisu w podanej liście
  name = each.key                            # Nazwa repozytorium ECR, taka sama jak nazwa serwisu
  image_tag_mutability = "MUTABLE"             # Umożliwia nadpisywanie tagów obrazów (np. `latest`)
  force_delete         = true                  # Umożliwia usunięcie repozytorium, nawet jeśli zawiera obrazy

  image_scanning_configuration {
    scan_on_push = true                       # Automatyczne skanowanie obrazów pod kątem podatności po każdym pushu
  }
  tags = var.tags
}
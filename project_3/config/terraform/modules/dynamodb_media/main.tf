# dynamodb_media/main.tf

resource "aws_dynamodb_table" "this" {
  name         = var.table_name                   # Nazwa tabeli
  billing_mode = "PAY_PER_REQUEST"                # Tryb rozliczeń: płatność za żądanie
  hash_key     = "id"                             # Główny klucz skrótu tabeli

  attribute {
    name = "id"                                   # Nazwa atrybutu klucza partycji
    type = "S"                                    # Typ atrybutu klucza partycji (S - String)
  }
  tags = var.tags
}

# dynamodb_notification/main.tf

resource "aws_dynamodb_table" "this" {
  name         = var.table_name                       # Nazwa tabeli DynamoDB
  billing_mode = "PAY_PER_REQUEST"                    # Tryb rozliczeń: płatność za żądanie
  hash_key     = "notification_id"                    # Główny klucz skrótu tabeli, unikalny ID powiadomienia

  attribute {
    name = "notification_id"                          # Nazwa atrybutu klucza partycji
    type = "S"                                        # Typ: String
  }

  attribute {
    name = "user_email"                               # Nazwa atrybutu, który będzie używany jako klucz partycji w GSI
    type = "S"                                        # Typ: String
  }

  global_secondary_index {                            # Definicja globalnego indeksu wtórnego
    name            = "UserEmailIndex"                # Nazwa GSI, umożliwia wyszukiwanie powiadomień po emailu użytkownika
    hash_key        = "user_email"                    # Klucz partycji dla tego GSI
    projection_type = "ALL"                           # Typ projekcji: wszystkie atrybuty z elementu bazowego są kopiowane do indeksu
    read_capacity  = 5                                # Fikcyjna pojemność odczytu dla GSI (ignorowana przy PAY_PER_REQUEST tabeli)
    write_capacity = 5                                # Fikcyjna pojemność zapisu dla GSI (ignorowana przy PAY_PER_REQUEST tabeli)
  }

  tags = var.tags
}
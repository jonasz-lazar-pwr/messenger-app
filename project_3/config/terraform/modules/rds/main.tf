# rds/main.tf

resource "aws_db_subnet_group" "main" {
  name       = var.db_subnet_group_name       # Nazwa grupy podsieci dla instancji RDS
  subnet_ids = var.db_subnet_ids              # Lista ID podsieci, w których może być umieszczona instancja RDS

  tags = var.tags
}

resource "aws_db_instance" "this" {
  identifier              = var.db_instance_identifier   # Unikalny identyfikator instancji RDS
  db_name                 = var.db_name                  # Nazwa bazy danych
  engine                  = "postgres"                   # Silnik bazy danych
  engine_version          = "15.12"                      # Wersja silnika bazy danych PostgreSQL
  instance_class          = "db.t3.micro"                # Typ instancji bazy danych
  allocated_storage       = 20                           # Rozmiar alokowanej przestrzeni dyskowej w GB
  storage_type            = "gp2"                        # Typ dysku (General Purpose SSD)
  multi_az                = false                        # Wyłączenie wdrożenia Multi-AZ
  username                = var.db_username              # Nazwa głównego użytkownika
  password                = var.db_password              # Hasło głównego użytkownika
  port                    = var.db_port                  # Port nasłuchu bazy danych

  db_subnet_group_name    = aws_db_subnet_group.main.name # Powiązanie z utworzoną grupą podsieci
  vpc_security_group_ids  = var.security_group_ids       # Grupy bezpieczeństwa dla instancji

  publicly_accessible     = true                         # Dostępność publiczna instancji
  skip_final_snapshot     = true                         # Pominięcie tworzenia snapshotu przy usuwaniu
  backup_retention_period = 0                            # Wyłączenie automatycznych backupów

  storage_encrypted       = false                        # Wyłączenie szyfrowania dysku
  auto_minor_version_upgrade = false                     # Wyłączenie automatycznych aktualizacji pomniejszych wersji silnika
  deletion_protection     = false                        # Wyłączenie ochrony przed przypadkowym usunięciem

  tags = var.tags
}

# rds/main.tf

# --- Grupa podsieci dla instancji RDS ---
resource "aws_db_subnet_group" "this" {
  name       = var.db_subnet_group_name                 # Nazwa grupy subnetów
  subnet_ids = var.db_subnet_ids                        # Lista ID podsieci
  tags       = var.tags                                 # Tagi wspólne
}

# --- Instancja bazy danych PostgreSQL ---
resource "aws_db_instance" "this" {
  identifier              = var.db_instance_identifier   # Unikalny identyfikator instancji
  db_name                 = var.db_name                  # Nazwa bazy danych
  engine                  = "postgres"                   # Silnik bazy danych
  engine_version          = "15.12"                      # Wersja PostgreSQL
  instance_class          = "db.t3.micro"                # Klasa instancj
  allocated_storage       = 20                           # Ilość przydzielonej pamięci (w GB)
  storage_type            = "gp2"                        # Typ pamięci (SSD GP2)
  multi_az                = false                        # Czy instancja ma być wielostrefowa
  username                = var.db_username              # Nazwa użytkownika bazy danych
  password                = var.db_password              # Hasło do bazy danych
  port                    = var.db_port                  # Port bazy danych

  db_subnet_group_name    = aws_db_subnet_group.this.name    # Nazwa grupy subnetów
  vpc_security_group_ids  = var.security_group_ids           # Lista SG do powiązania z RDS

  publicly_accessible     = true                         # Publiczny dostęp
  skip_final_snapshot     = true                         # Usuwaj bez snapshotu
  backup_retention_period = 0                            # Brak backupów

  # --- Monitoring i logowanie ---
  performance_insights_enabled = false                   # Performance Insights – wyłączone
  monitoring_interval          = 0                       # CloudWatch monitoring – wyłączony

  # --- Konfiguracja opcji i bezpieczeństwa ---
  # option_group_name           = "default:postgres-15"    # Domyślna grupa opcji dla wersji 15
  storage_encrypted           = false                    # Brak szyfrowania dysku
  auto_minor_version_upgrade  = false                    # Automatyczna aktualizacja patchy
  deletion_protection         = false                    # Brak ochrony przed usunięciem

  tags = var.tags                                         # Tagi wspólne
}
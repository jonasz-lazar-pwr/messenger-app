# sqs/main.tf

resource "aws_sqs_queue" "this" {
  name                       = var.queue_name
  message_retention_seconds = 86400            # Czas przechowywania wiadomości w kolejce – 1 dzień
  visibility_timeout_seconds = 30              # Czas ukrycia wiadomości po jej pobraniu
  receive_wait_time_seconds  = 10              # Czas oczekiwania na nowe wiadomości (long pooling)

  tags = var.tags                              # Tagi wspólne dla wszystkich zasobów
}
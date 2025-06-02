# lambda/main.tf

# Tworzenie funkcji Lambda
resource "aws_lambda_function" "lambda" {
  for_each = local.lambda_functions                           # Iteracja po każdej funkcji zdefiniowanej w locals.tf

  function_name = "chat_service_${each.key}"                  # Nazwa funkcji Lambda, np. "chat_service_get_chats"
  description   = each.value.description                      # Opis funkcji (np. używany w konsoli AWS)
  handler       = each.value.handler                          # Ścieżka do handlera w kodzie (np. plik/funkcja)
  timeout       = each.value.timeout                          # Maksymalny czas działania funkcji (w sekundach)

  role      = var.iam_role_arn                                # ARN roli IAM przypisanej do funkcji
  runtime   = "python3.11"                                    # Środowisko uruchomieniowe (Python 3.11)
  s3_bucket = "messenger-app-artifacts"                       # Nazwa bucketa S3 z kodem funkcji
  s3_key    = "messenger-app-chat-service.zip"                # Klucz (ścieżka) do archiwum ZIP z kodem

  environment {
    variables = each.value.env                                # Zmienne środowiskowe przypisane do funkcji
  }
}

# Alarm CloudWatch dla każdej funkcji Lambda – monitoruje liczbę błędów
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  for_each = aws_lambda_function.lambda                       # Tworzy alarm dla każdej funkcji Lambda

  alarm_name          = "chat_service_${each.key}_errors"     # Nazwa alarmu (czytelna w CloudWatch)
  comparison_operator = "GreaterThanOrEqualToThreshold"       # Alarmuje, gdy wartość >= threshold
  evaluation_periods  = 1                                     # Liczba okresów oceny (tu: 1 okres = 5 min)
  metric_name         = "Errors"                              # Metryka AWS Lambda – liczba błędów
  namespace           = "AWS/Lambda"                          # Namespace AWS dla metryk Lambdy
  period              = 300                                   # Długość okresu oceny – 300 sek. = 5 minut
  statistic           = "Sum"                                 # Sumuje błędy w danym okresie
  threshold           = 1                                     # Alarm, jeśli >= 1 błąd

  alarm_description   = "Alarm when ${each.key} Lambda fails" # Opis alarmu (dla konsoli)

  dimensions = {
    FunctionName = each.value.function_name                   # Nazwa funkcji, której dotyczy alarm
  }

  treat_missing_data = "notBreaching"                         # Brak danych nie traktowany jako przekroczenie progu
}

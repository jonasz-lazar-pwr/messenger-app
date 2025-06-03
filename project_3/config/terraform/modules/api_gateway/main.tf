# api_gateway/main.tf

# API Gateway w trybie HTTP z podstawową konfiguracją CORS
# (kontener logiczny dla wszystkich endpointów)
resource "aws_apigatewayv2_api" "main" {
  name          = "messenger-app-api"
  protocol_type = "HTTP"
  cors_configuration {
    allow_origins = ["*"]                      # Zezwól na żądania z dowolnego źródła
    allow_methods = ["GET", "POST", "OPTIONS"] # Dozwolone metody HTTP
    allow_headers = ["*"]                      # Dozwolone wszystkie nagłówki
  }
  tags          = var.tags
}

# Autoryzator JWT oparty o Amazon Cognito dla zabezpieczonych endpointów
resource "aws_apigatewayv2_authorizer" "cognito" {
  name                       = "CognitoJWTAuthorizer"
  api_id                     = aws_apigatewayv2_api.main.id
  authorizer_type            = "JWT"                               # Typ autoryzatora: JWT
  identity_sources           = ["$request.header.Authorization"]   # Źródło tokena JWT – nagłówek Authorization
  jwt_configuration {
    audience = [var.cognito_pool_id]                               # Oczekiwany client_id
    issuer   = var.cognito_issuer_url                              # URL dostawcy tokenów (Cognito)
  }
}

# Definicja połączeń API Gateway z funkcjami Lambda
# (mapowanie endpointów na funkcję Lambda)
resource "aws_apigatewayv2_integration" "lambda" {
  for_each = local.routes

  api_id                 = aws_apigatewayv2_api.main.id
  integration_type       = "AWS_PROXY"                         # Typ integracji proxy – bezpośrednie wywołanie Lambdy
  integration_uri        = var.lambda_arns[each.key]           # Adres URI funkcji Lambda
  integration_method     = each.value.method                   # Metoda HTTP (GET, POST itd.)
  payload_format_version = "2.0"                               # Format payloadu w wersji 2.0
}

# Definicja tras (routes) w API Gateway
resource "aws_apigatewayv2_route" "lambda" {
  for_each = local.routes

  api_id    = aws_apigatewayv2_api.main.id                                  # ID API Gateway, do którego należy ta trasa
  route_key = "${each.value.method} ${each.value.path}"                     # Klucz trasy, np. "GET /api/chats"
  target    = "integrations/${aws_apigatewayv2_integration.lambda[each.key].id}" # Powiązana integracja Lambda

  # Jeśli endpoint wymaga autoryzacji, dołącz autoryzator Cognito
  authorizer_id = each.value.authorizer ? aws_apigatewayv2_authorizer.cognito.id : null
}

# Uprawnienia dla API Gateway do wywoływania każdej funkcji Lambda
resource "aws_lambda_permission" "apigw_lambda" {
  for_each = local.routes

  statement_id  = "AllowExecutionFromAPIGateway-${each.key}"          # Unikalny identyfikator oświadczenia IAM
  action        = "lambda:InvokeFunction"                             # Działanie: zezwolenie na wywołanie funkcji Lambda
  function_name = var.lambda_arns[each.key]                           # Nazwa (ARN) funkcji Lambda, do której przydzielane są uprawnienia
  principal     = "apigateway.amazonaws.com"                          # Podmiot wykonujący: API Gateway
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"    # Dozwolone źródło wywołania (dowolna metoda i ścieżka w API Gateway)
}

# Tworzy stage (etap) API Gateway – "$default" – z automatycznym wdrażaniem zmian po każdej aktualizacji
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.main.id  # ID interfejsu API, do którego przypisywany jest stage
  name        = "$default"                    # Nazwa stage – "$default" umożliwia korzystanie z API bez potrzeby definiowania konkretnych stage (np. /dev, /prod)
  auto_deploy = true                          # Automatyczne wdrażanie zmian (każda zmiana w trasach lub integracjach jest od razu aktywna bez ręcznego deploya)
}

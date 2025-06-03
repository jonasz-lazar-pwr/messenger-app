# lambda/locals.tf

# Definicje funkcji Lambda dla chat-service
# Każdy wpis zawiera opis funkcji, nazwę handlera (ścieżka do pliku), timeout (czas maksymalnego wykonania)
# oraz mapę zmiennych środowiskowych potrzebnych do działania funkcji.

locals {
  lambda_functions = {

    health_check = {
      description = "Simple health check endpoint for monitoring"
      handler     = "handlers/health_check.handler"
      timeout     = 5
      env         = {}
    }

    health_check_secure = {
      description = "Secure health check endpoint requiring valid JWT token"
      handler     = "handlers/health_check_secure.handler"
      timeout     = 5
      env = {
        COGNITO_POOL_ID    = var.cognito_pool_id
        COGNITO_CLIENT_ID  = var.cognito_client_id
        COGNITO_ISSUER_URL = var.cognito_issuer_url
      }
    }

    register_user = {
      description = "Handles POST /api/users/register in chat-service"
      handler     = "handlers/users_post_register.handler"
      timeout     = 5
      env = {
        PSQL_HOST          = var.psql_host
        PSQL_PORT          = var.psql_port
        PSQL_USER          = var.psql_user
        PSQL_PASSWORD      = var.psql_password
        PSQL_NAME          = var.psql_name
        COGNITO_POOL_ID    = var.cognito_pool_id
        COGNITO_CLIENT_ID  = var.cognito_client_id
        COGNITO_ISSUER_URL = var.cognito_issuer_url
      }
    }

    get_chats = {
      description = "Handles GET /api/chats in chat-service"
      handler     = "handlers/chats_get.handler"
      timeout     = 5
      env = {
        PSQL_HOST          = var.psql_host
        PSQL_PORT          = var.psql_port
        PSQL_USER          = var.psql_user
        PSQL_PASSWORD      = var.psql_password
        PSQL_NAME          = var.psql_name
        COGNITO_POOL_ID    = var.cognito_pool_id
        COGNITO_CLIENT_ID  = var.cognito_client_id
        COGNITO_ISSUER_URL = var.cognito_issuer_url
      }
    }

    search_users = {
      description = "Handles GET /api/users/search in chat-service"
      handler     = "handlers/users_get_search.handler"
      timeout     = 5
      env = {
        PSQL_HOST          = var.psql_host
        PSQL_PORT          = var.psql_port
        PSQL_USER          = var.psql_user
        PSQL_PASSWORD      = var.psql_password
        PSQL_NAME          = var.psql_name
        COGNITO_POOL_ID    = var.cognito_pool_id
        COGNITO_CLIENT_ID  = var.cognito_client_id
        COGNITO_ISSUER_URL = var.cognito_issuer_url
      }
    }

    create_chat = {
      description = "Handles POST /api/chats in chat-service"
      handler     = "handlers/chats_post.handler"
      timeout     = 5
      env = {
        PSQL_HOST          = var.psql_host
        PSQL_PORT          = var.psql_port
        PSQL_USER          = var.psql_user
        PSQL_PASSWORD      = var.psql_password
        PSQL_NAME          = var.psql_name
        COGNITO_POOL_ID    = var.cognito_pool_id
        COGNITO_CLIENT_ID  = var.cognito_client_id
        COGNITO_ISSUER_URL = var.cognito_issuer_url
      }
    }

    get_messages = {
      description = "Handles GET /api/messages/{chat_id} in chat-service"
      handler     = "handlers/messages_get_by_chat.handler"
      timeout     = 5
      env = {
        PSQL_HOST          = var.psql_host
        PSQL_PORT          = var.psql_port
        PSQL_USER          = var.psql_user
        PSQL_PASSWORD      = var.psql_password
        PSQL_NAME          = var.psql_name
        COGNITO_POOL_ID    = var.cognito_pool_id
        COGNITO_CLIENT_ID  = var.cognito_client_id
        COGNITO_ISSUER_URL = var.cognito_issuer_url
      }
    }

    send_message_text = {
      description = "Handles POST /api/messages/text in chat-service"
      handler     = "handlers/messages_post_text.handler"
      timeout     = 5
      env = {
        PSQL_HOST          = var.psql_host
        PSQL_PORT          = var.psql_port
        PSQL_USER          = var.psql_user
        PSQL_PASSWORD      = var.psql_password
        PSQL_NAME          = var.psql_name
        COGNITO_POOL_ID    = var.cognito_pool_id
        COGNITO_CLIENT_ID  = var.cognito_client_id
        COGNITO_ISSUER_URL = var.cognito_issuer_url
        AWS_SQS_NOTIFICATION_QUEUE_URL = var.sqs_notification_queue_url
        NOTIFICATION_RECEIVER_EMAIL = var.sns_notification_email
      }
    }

    send_message_media = {
      description = "Handles POST /api/messages/media in chat-service"
      handler     = "handlers/messages_post_media.handler"
      timeout     = 5
      env = {
        PSQL_HOST          = var.psql_host
        PSQL_PORT          = var.psql_port
        PSQL_USER          = var.psql_user
        PSQL_PASSWORD      = var.psql_password
        PSQL_NAME          = var.psql_name
        COGNITO_POOL_ID    = var.cognito_pool_id
        COGNITO_CLIENT_ID  = var.cognito_client_id
        COGNITO_ISSUER_URL = var.cognito_issuer_url
        MEDIA_SERVICE_HOST = var.media_service_host
        AWS_SQS_NOTIFICATION_QUEUE_URL = var.sqs_notification_queue_url
        NOTIFICATION_RECEIVER_EMAIL = var.sns_notification_email
      }
    }
  }
}

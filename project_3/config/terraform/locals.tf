# locals.tf (root)

# Definicja konfiguracji trzech usług ECS w postaci mapy:
# Każda usługa zawiera: obraz Docker, flagę czy używa ALB, ewentualny ARN target group oraz zmienne środowiskowe.

locals {
  ecs_services = {
    frontend = {
      image                = module.ecr.ecr_repository_urls["frontend"]
      alb_target_group_arn = module.alb.alb_target_group_arns["frontend"]
      enable_load_balancer = true
      environment = [
        { name = "API_URL", value = module.api_gateway.api_url },
        { name = "COGNITO_LOGOUT_URL", value = "https://${module.cognito.pool_domain_prefix}.auth.${var.aws_region}.amazoncognito.com/logout" },
        { name = "COGNITO_AUTHORITY", value = "https://cognito-idp.${var.aws_region}.amazonaws.com/${module.cognito.pool_id}" },
        { name = "COGNITO_REDIRECT_URL", value = "https://${module.alb.alb_dns_names["frontend"]}/callback/" },
        { name = "COGNITO_POST_LOGOUT_URI", value = "https://${module.alb.alb_dns_names["frontend"]}/" },
        { name = "COGNITO_CLIENT_ID", value = module.cognito.pool_client_id },
        { name = "COGNITO_SCOPE", value = var.cognito_allowed_scopes },
        { name = "COGNITO_RESPONSE_TYPE", value = var.cognito_response_type },
      ]
    }
    media_service = {
      image                = module.ecr.ecr_repository_urls["media-service"]
      alb_target_group_arn = module.alb.alb_target_group_arns["media_service"]
      enable_load_balancer = true
      environment = [
        { name = "AWS_REGION", value = var.aws_region },
        { name = "AWS_S3_BUCKET_NAME", value = var.s3_bucket_name },
        { name = "AWS_DYNAMODB_MEDIA_TABLE_NAME", value = var.dynamodb_media_table_name },
        { name = "AWS_ACCESS_KEY_ID", value = var.aws_access_key_id },
        { name = "AWS_SECRET_ACCESS_KEY", value = var.aws_secret_access_key },
        { name = "AWS_SESSION_TOKEN", value = var.aws_session_token },
        { name = "CORS_ALLOW_ORIGINS", value = var.cors_allow_origins },
      ]
    }
    notification_service = {
      image                = module.ecr.ecr_repository_urls["notification-service"]
      alb_target_group_arn = null
      enable_load_balancer = false
      environment = [
        { name = "AWS_REGION", value = var.aws_region },
        { name = "AWS_SNS_TOPIC_ARN", value = module.sns.topic_arn },
        { name = "AWS_DYNAMODB_NOTIFICATION_TABLE_NAME", value = var.dynamodb_notification_table_name },
        { name = "AWS_SQS_NOTIFICATION_QUEUE_URL", value = module.sqs_notification_queue.queue_url },
        { name = "AWS_ACCESS_KEY_ID", value = var.aws_access_key_id },
        { name = "AWS_SECRET_ACCESS_KEY", value = var.aws_secret_access_key },
        { name = "AWS_SESSION_TOKEN", value = var.aws_session_token },
        { name = "CORS_ALLOW_ORIGINS", value = var.cors_allow_origins },
      ]
    }
  }
}

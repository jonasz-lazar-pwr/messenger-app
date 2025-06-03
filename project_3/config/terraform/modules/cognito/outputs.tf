# cognito/outputs.tf

output "pool_id" {
  description = "The ID of the Cognito User Pool"             # ID puli użytkowników Cognito
  value       = aws_cognito_user_pool.this.id
}

output "pool_client_id" {
  description = "The ID of the Cognito User Pool App Client"  # ID klienta aplikacji Cognito
  value = aws_cognito_user_pool_client.this.id
}

output "pool_domain_prefix" {
  description = "The domain prefix of the Cognito Hosted UI"  # Prefiks domeny hostowanej przez Cognito
  value = aws_cognito_user_pool_domain.this.domain
}
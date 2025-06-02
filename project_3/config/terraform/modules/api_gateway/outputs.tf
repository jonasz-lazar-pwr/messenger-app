# api_gateway/outputs.tf

output "api_url" {
  description = "URL of the deployed API Gateway"
  value       = aws_apigatewayv2_stage.default.invoke_url
}

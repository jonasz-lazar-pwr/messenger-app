# lambda/outputs.tf

output "lambda_function_arns" {
  description = "ARNs of all Lambda functions in chat-service"
  value = {
    for name, lambda in aws_lambda_function.lambda : name => lambda.arn
  }
}

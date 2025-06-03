# sqs/outputs.tf

output "queue_url" {
  description = "The URL of the SQS queue used to send notification events."
  value       = aws_sqs_queue.this.url
}
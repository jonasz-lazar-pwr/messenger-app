# alb/outputs.tf

output "alb_target_group_arn" {
  description = "The ARN of the created ALB Target Group."
  value       = aws_lb_target_group.this.arn
}

output "alb_dns_name" {
  description = "The DNS name of the created ALB."
  value       = aws_lb.this.dns_name
}

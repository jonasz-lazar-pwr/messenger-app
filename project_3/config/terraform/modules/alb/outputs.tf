# alb/outputs.tf

output "alb_target_group_arns" {
  description = "Map of service names to the ARNs of their respective ALB Target Groups."
  value = {
    for key, tg in aws_lb_target_group.this : key => tg.arn
  }
}

output "alb_dns_names" {
  description = "Map of service names to the DNS names of their respective ALBs."
  value = {
    for key, lb in aws_lb.this : key => lb.dns_name
  }
}

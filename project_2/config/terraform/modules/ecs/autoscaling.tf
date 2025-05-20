# ecs/autoscaling.tf

# Ustawienia celu autoskalowania dla serwisu ECS
resource "aws_appautoscaling_target" "this" {
  min_capacity       = 2                               # Minimalna liczba zadań
  max_capacity       = 4                               # Maksymalna liczba zadań
  resource_id        = "service/${var.cluster_id}/${aws_ecs_service.this.name}" # Identyfikator zasobu ECS do skalowania
  scalable_dimension = "ecs:service:DesiredCount"      # Wymiar, który jest skalowany (liczba zadań serwisu)
  service_namespace  = "ecs"                           # Przestrzeń nazw usługi AWS
}

# Ustawienia polityki autoskalowania opartej na średnim użyciu CPU
resource "aws_appautoscaling_policy" "cpu_utilization" {
  name               = "${var.service_name}-cpu-autoscaling" # Nazwa polityki
  policy_type        = "TargetTrackingScaling"               # Typ polityki: śledzenie wartości docelowej dla metryki
  resource_id        = aws_appautoscaling_target.this.resource_id        # Powiązanie z celem autoskalowania
  scalable_dimension = aws_appautoscaling_target.this.scalable_dimension # Skalowalny wymiar
  service_namespace  = aws_appautoscaling_target.this.service_namespace  # Przestrzeń nazw usługi

  target_tracking_scaling_policy_configuration {
    target_value       = 50                                       # Docelowa wartość średniego użycia CPU
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"  # Predefiniowana metryka ECS: średnie użycie CPU
    }
    scale_out_cooldown = 300                                      # Czas oczekiwania po akcji skalowania w górę
    scale_in_cooldown  = 300                                      # Czas oczekiwania po akcji skalowania w dół
  }
}

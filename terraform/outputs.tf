output "redshift_endpoint" {
  value = aws_redshift_cluster.redshift_cluster.endpoint
}

output "redshift_port" {
  value = aws_redshift_cluster.redshift_cluster.port
}

output "iam_role_arn" {
  value = aws_iam_role.redshift_s3_access.arn
}

output "db_name" {
  value = var.db_name
}

output "db_user" {
  value = var.db_user
}

output "db_password" {
  value     = var.db_password
  sensitive = true
}

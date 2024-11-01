data "template_file" "dwh_cfg" {
  template = file("${path.module}/dwh_cfg.tmpl")

  vars = {
    redshift_endpoint = aws_redshift_cluster.redshift_cluster.endpoint
    redshift_port     = aws_redshift_cluster.redshift_cluster.port
    iam_role_arn      = aws_iam_role.redshift_s3_access.arn
    db_name           = var.db_name
    db_user           = var.db_user
    db_password       = var.db_password
  }
}

resource "local_file" "dwh_cfg" {
  content  = data.template_file.dwh_cfg.rendered
  filename = "${path.module}/../dwh.cfg"
}

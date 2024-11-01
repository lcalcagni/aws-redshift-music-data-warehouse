
resource "aws_redshift_cluster" "redshift_cluster" {
  cluster_identifier          = var.cluster_identifier
  database_name               = var.db_name
  master_username             = var.db_user
  master_password             = var.db_password
  node_type                   = var.node_type
  cluster_type                = "single-node"
  publicly_accessible         = true
  iam_roles                   = [aws_iam_role.redshift_s3_access.arn]
  skip_final_snapshot         = true
  port                        = 5439

  vpc_security_group_ids      = [aws_security_group.redshift_sg.id]
  cluster_subnet_group_name   = aws_redshift_subnet_group.redshift_subnet.name
  availability_zone           = "us-west-2a"  # Match the AZ of your subnet
}

resource "aws_redshift_subnet_group" "redshift_subnet" {
  name       = "redshift-subnet-group"
  subnet_ids = [aws_subnet.public_subnet.id]

  tags = {
    Name = "Redshift subnet group"
  }
}

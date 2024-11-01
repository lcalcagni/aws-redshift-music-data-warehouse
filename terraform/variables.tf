# variables.tf

variable "aws_region" {
  description = "AWS region to create resources in"
  default     = "us-west-2"
}

variable "cluster_identifier" {
  description = "Redshift cluster identifier"
  default     = "sparkify-cluster"
}

variable "db_name" {
  description = "The Redshift cluster database name"
  default     = "dev"
}

variable "db_user" {
  description = "The Redshift cluster master username"
  default     = "awsuser"
}

variable "db_password" {
  description = "Master database password"
  type        = string
  sensitive   = true
}

variable "aws_access_key" {
  description = "AWS Access Key ID"
  type        = string
  sensitive   = true
}

variable "aws_secret_key" {
  description = "AWS Secret Access Key"
  type        = string
  sensitive   = true
}

variable "node_type" {
  description = "Redshift cluster node type"
  default     = "dc2.large"
}

variable "number_of_nodes" {
  description = "Number of nodes in the Redshift cluster"
  default     = 1
}

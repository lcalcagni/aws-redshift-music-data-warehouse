# iam.tf

resource "aws_iam_role" "redshift_s3_access" {
  name = "redshift_s3_access_role"

  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Effect": "Allow",
        "Principal": {
          "Service": "redshift.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "attach_s3_readonly_policy" {
  name       = "redshift_s3_readonly_policy"
  roles      = [aws_iam_role.redshift_s3_access.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

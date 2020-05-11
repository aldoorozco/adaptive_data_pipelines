resource "aws_iam_policy" "glue" {
  name        = "glue-policy"
  description = "Glue crawler policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:*",
        "s3:*",
        "glue:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "emr" {
  name        = "emr-policy"
  description = "EMR policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:*",
        "ec2:*",
        "s3:*",
        "glue:*",
        "elasticmapreduce:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "superserver" {
  name        = "ec2-policy"
  description = "EC2 policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:*",
        "glue:*",
        "elasticmapreduce:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

data "aws_iam_policy_document" "glue" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "emr" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["elasticmapreduce.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "superserver" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "glue" {
  name               = "glue_role"
  assume_role_policy = data.aws_iam_policy_document.glue.json
}

resource "aws_iam_role" "emr" {
  name               = "emr_role"
  assume_role_policy = data.aws_iam_policy_document.emr.json
}

resource "aws_iam_role" "superserver_role" {
  name               = "superserver_role"
  assume_role_policy = data.aws_iam_policy_document.superserver.json
}

resource "aws_iam_role_policy_attachment" "glue" {
  role       = aws_iam_role.glue.name
  policy_arn = aws_iam_policy.glue.arn
}

resource "aws_iam_role_policy_attachment" "emr" {
  role       = aws_iam_role.emr.name
  policy_arn = aws_iam_policy.emr.arn
}

resource "aws_iam_role_policy_attachment" "superserver" {
  role       = aws_iam_role.superserver_role.name
  policy_arn = aws_iam_policy.superserver.arn
}

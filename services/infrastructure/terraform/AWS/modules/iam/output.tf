output "glue_role" {
  value = aws_iam_role.glue.arn
}
output "emr_role" {
  value = aws_iam_role.emr.arn
}

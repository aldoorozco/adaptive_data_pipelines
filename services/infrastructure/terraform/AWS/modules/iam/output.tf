output "glue_role" {
  value = aws_iam_role.glue.arn
}
output "emr_role" {
  value = aws_iam_role.emr.arn
}
output "superserver_role" {
  value = aws_iam_role.superserver_role.name
}

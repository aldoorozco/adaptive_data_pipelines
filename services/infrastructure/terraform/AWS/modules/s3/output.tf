output "template_bucket" {
  value = aws_s3_bucket.templates.id
}

output "datalake_bucket" {
  value = aws_s3_bucket.datalake.id
}

output "datamart_bucket" {
  value = aws_s3_bucket.datamart.id
}

output "logs_bucket" {
  value = aws_s3_bucket.logs.id
}

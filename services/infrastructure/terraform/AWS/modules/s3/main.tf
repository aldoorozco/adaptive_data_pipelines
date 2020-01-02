resource "aws_s3_bucket" "templates" {
  bucket = "abdp-templates"
}

resource "aws_s3_bucket" "logs" {
  bucket = "abdp-logs"
  lifecycle_rule {
    enabled = true
    transition {
      days          = 60
      storage_class = "STANDARD_IA"
    }
    transition {
      days          = 120
      storage_class = "GLACIER"
    }
  }
}

resource "aws_s3_bucket" "datalake" {
  bucket = "abdp-datalake"
  lifecycle_rule {
    enabled = true
    transition {
      days          = 60
      storage_class = "STANDARD_IA"
    }
    transition {
      days          = 120
      storage_class = "GLACIER"
    }
  }
}

resource "aws_s3_bucket" "datamart" {
  bucket = "abdp-datamart"
  lifecycle_rule {
    enabled = true
    transition {
      days          = 60
      storage_class = "STANDARD_IA"
    }
    transition {
      days          = 120
      storage_class = "GLACIER"
    }
  }
}

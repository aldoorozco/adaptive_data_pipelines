module "vpc" {
  source   = "./../vpc"
  local_ip = var.local_ip
}

module "s3" {
  source = "./../s3"
}

module "iam" {
  source = "./../iam"
}

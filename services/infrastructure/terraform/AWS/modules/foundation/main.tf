module "vpc" {
  source              = "./../vpc"
  pipeline_builder_ip = var.pipeline_builder_ip
  webserver_ip        = var.webserver_ip
}

module "s3" {
  source = "./../s3"
}

module "iam" {
  source = "./../iam"
}

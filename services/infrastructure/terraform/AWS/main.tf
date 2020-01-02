provider "aws" {
  region  = var.region
  profile = var.profile
}

terraform {
  backend "s3" {
    bucket = var.terraform_bucket
    key    = "state"
    region = var.region
  }
}

module "foundation" {
  source   = "./modules/foundation"
  local_ip = var.local_ip
}

module "superserver" {
  source           = "./modules/superserver"
  public_subnet_id = var.public_subnet_id
  security_group   = var.security_group
}

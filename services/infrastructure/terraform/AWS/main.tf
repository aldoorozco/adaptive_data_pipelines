provider "aws" {
  region  = var.region
  profile = var.profile
}

terraform {
  backend "s3" {
    bucket = "abdp-terraform"
    key    = "state"
    region = "us-east-1"
  }
}

module "foundation" {
  source   = "./modules/foundation"
  local_ip = var.local_ip
}

module "superserver" {
  source              = "./modules/superserver"
  public_subnet_id    = var.public_subnet_id
  security_group      = var.security_group
  superserver_role    = var.superserver_role
  superserver_keypair = var.superserver_keypair
}

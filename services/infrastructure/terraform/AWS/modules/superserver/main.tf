module "ec2" {
  source = "./../ec2"

  public_subnet_id = var.public_subnet_id
  instance_name    = "Super Server"
  instance_type    = var.instance_type
  script_path      = "${path.root}/scripts/bootstrap.sh"
  security_group   = var.security_group
  iam_role         = var.superserver_role
  ec2_keypair      = var.superserver_keypair
}

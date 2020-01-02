module "ec2" {
  source = "./../ec2"

  public_subnet_id = var.public_subnet_id
  instance_name    = "airflow_webserver"
  script_path      = "${path.root}/scripts/bootstrap_airflow.sh"
}

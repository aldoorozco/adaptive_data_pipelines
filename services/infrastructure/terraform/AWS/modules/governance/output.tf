output "airflow_server_ip" {
  value = module.ec2.aws_eip.elastic_ip.public_ip
}

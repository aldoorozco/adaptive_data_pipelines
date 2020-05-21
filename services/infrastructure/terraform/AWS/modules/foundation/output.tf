output "public_subnet_id" {
  value = module.vpc.public_subnet_id
}
output "private_subnet_id" {
  value = module.vpc.private_subnet_id
}
output "glue_role" {
  value = module.iam.glue_role
}
output "emr_role" {
  value = module.iam.emr_role
}
output "superserver_role" {
  value = module.iam.superserver_role
}
output "template_bucket" {
  value = module.s3.template_bucket
}
output "datalake_bucket" {
  value = module.s3.datalake_bucket
}
output "datamart_bucket" {
  value = module.s3.datamart_bucket
}
output "logs_bucket" {
  value = module.s3.logs_bucket
}
output "superserver_security_group" {
  value = module.vpc.superserver_security_group
}
output "master_security_group" {
  value = module.vpc.master_security_group
}
output "slave_security_group" {
  value = module.vpc.slave_security_group
}
output "superserver_keypair" {
  value = module.vpc.superserver_keypair
}
output "emr_service_access_sg" {
  value = module.vpc.emr_service_access_sg
}

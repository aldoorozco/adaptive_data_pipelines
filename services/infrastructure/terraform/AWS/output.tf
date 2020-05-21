output "foundation_public_subnet_id" {
  value = module.foundation.public_subnet_id
}

output "foundation_private_subnet_id" {
  value = module.foundation.private_subnet_id
}

output "foundation_glue_role" {
  value = module.foundation.glue_role
}

output "foundation_emr_role" {
  value = module.foundation.emr_role
}

output "foundation_superserver_role" {
  value = module.foundation.superserver_role
}

output "foundation_superserver_keypair" {
  value = module.foundation.superserver_keypair
}

output "foundation_template_bucket" {
  value = module.foundation.template_bucket
}

output "foundation_datalake_bucket" {
  value = module.foundation.datalake_bucket
}

output "foundation_datamart_bucket" {
  value = module.foundation.datamart_bucket
}

output "foundation_logs_bucket" {
  value = module.foundation.logs_bucket
}

output "foundation_superserver_security_group" {
  value = module.foundation.superserver_security_group
}

output "foundation_master_security_group" {
  value = module.foundation.master_security_group
}

output "foundation_slave_security_group" {
  value = module.foundation.slave_security_group
}

output "foundation_emr_service_access_sg" {
  value = module.foundation.emr_service_access_sg
}

output "superserver_public_ip" {
  value = module.superserver.public_ip
}

variable "vpc_cidr" {
  description = "CIDR for the whole VPC"
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR for the Public Subnet"
  default     = "10.0.0.0/24"
}

variable "public_subnet_id" {
  description = "Public subnet"
  default     = "dummy"
}

variable "security_group" {
  description = "The security group"
  default     = "dummy"
}

variable "pipeline_builder_ip" {
  description = "The public IP of the pipline builder"
  default     = "dummy"
}

variable "webserver_ip" {
  description = "The public IP of the webserver"
  default     = "dummy"
}

variable "profile" {
  description = "AWS user profile name"
  default     = "abdp-infra"
}

variable "region" {
  description = "The AWS region where everything will be hosted"
  default     = "us-east-1"
}

variable "terraform_bucket" {
  description = "The AWS S3 bucket where the terraform remote state will be hosted"
  default     = "abdp-terraform"
}

variable "superserver_role" {
  description = "The superserver iam role"
  default     = "dummy"
}

variable "superserver_keypair" {
  description = "The superserver ec2 instance keypair"
  default     = "dummy"
}

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

variable "local_ip" {
  description = "The local IP"
  default     = "dummy"
}

variable "profile" {
  description = "AWS user profile name"
  default     = "pipeline_admin"
}

variable "region" {
  description = "The AWS region where everything will be hosted"
  default     = "us-east-1"
}

variable "terraform_bucket" {
  description = "The AWS S3 bucket where the terraform remote state will be hosted"
  default     = "abdp-terraform"
}

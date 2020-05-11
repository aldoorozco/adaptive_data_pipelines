variable "instance_type" {
  description = "The instance type to be created"
}

variable "public_subnet_id" {
  description = "The public subnet id where the instance will be allocated"
}

variable "instance_name" {
  description = "The instance name"
}

variable "script_path" {
  description = "Where the script resides"
}

variable "security_group" {
  description = "The security group that restricts port access"
}

variable "iam_role" {
  description = "The IAM role for the instance"
}

variable "ec2_keypair" {
  description = "The keypair to access the instance"
}

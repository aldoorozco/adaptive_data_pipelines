variable "public_subnet_id" {
  description = "The public subnet where the instance will be located"
}

variable "security_group" {
  description = "The security group"
}

variable "instance_type" {
  description = "The instance type"
  default     = "m5.xlarge"
}

variable "superserver_role" {
  description = "The supserserver instance role"
}

variable "superserver_keypair" {
  description = "The supserserver instance keypair"
}

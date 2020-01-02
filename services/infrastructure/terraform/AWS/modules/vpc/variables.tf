variable "local_ip" {
  description = "The local IP"
}
variable "vpc_cidr" {
  description = "The default VPC CIDR"
  default     = "10.0.0.0/16"
}
variable "public_subnet_cidr" {
  description = "The default public subnet CIDR"
  default     = "10.0.0.0/24"
}
variable "private_subnet_cidr" {
  description = "The default private subnet CIDR"
  default     = "10.0.1.0/24"
}

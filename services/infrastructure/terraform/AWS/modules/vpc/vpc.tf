resource "aws_vpc" "tog" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "TOG VPC"
  }
}

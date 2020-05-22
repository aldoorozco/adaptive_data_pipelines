resource "aws_vpc" "tog" {
  cidr_block           = var.vpc_cidr
  enble_dns_support    = true
  enable_dns_hostnames = true
  tags = {
    Name = "TOG VPC"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.tog.id
  cidr_block              = var.public_subnet_cidr
  map_public_ip_on_launch = "true"
  availability_zone       = "us-east-1a"
  tags = {
    Name = "Public"
  }
}

resource "aws_subnet" "private" {
  vpc_id                  = aws_vpc.tog.id
  cidr_block              = var.private_subnet_cidr
  map_public_ip_on_launch = "false"
  availability_zone       = "us-east-1a"
  tags = {
    Name = "Private"
  }
}

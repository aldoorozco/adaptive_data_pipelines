locals {
  public_access = "0.0.0.0/0"
}

resource "aws_key_pair" "deployer" {
  key_name   = "deploy"
  public_key = file("${path.root}/deploy.pub")
}

resource "aws_eip" "nat" {
  vpc      = true
}

resource "aws_nat_gateway" "tog" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public.id
  depends_on    = [aws_internet_gateway.tog]
}

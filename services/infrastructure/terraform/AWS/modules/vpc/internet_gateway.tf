resource "aws_internet_gateway" "tog" {
  vpc_id = aws_vpc.tog.id
  tags = {
    Name = "tog-igw"
  }
}

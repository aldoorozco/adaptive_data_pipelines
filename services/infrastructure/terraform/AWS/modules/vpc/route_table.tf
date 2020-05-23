resource "aws_route_table" "public" {
  vpc_id = aws_vpc.tog.id

  route {
    cidr_block = local.public_access
    gateway_id = aws_internet_gateway.tog.id
  }

  tags = {
    Name = "Public"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.tog.id

  route {
    cidr_block     = local.public_access
    nat_gateway_id = aws_nat_gateway.tog.id
  }

  /*
  route {
    cidr_block           = aws_vpc_endpoint.glue.
    network_interface_id = aws_vpc_endpoint.glue.
  }
  */

  tags = {
    Name = "Private"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

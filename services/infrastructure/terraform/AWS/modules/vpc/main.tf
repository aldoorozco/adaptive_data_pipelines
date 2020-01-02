locals {
  public_access = "0.0.0.0/0"
}

resource "aws_internet_gateway" "tog" {
  vpc_id = aws_vpc.tog.id
  tags = {
    Name = "tog-igw"
  }
}

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

resource "aws_instance" "nat" {
  ami                         = "ami-00a9d4a05375b2763"
  availability_zone           = "us-east-1a"
  instance_type               = "t2.micro"
  key_name                    = "deploy"
  vpc_security_group_ids      = [aws_security_group.nat.id]
  subnet_id                   = aws_subnet.public.id
  associate_public_ip_address = true
  source_dest_check           = false

  tags = {
    Name = "NAT"
  }
}

resource "aws_eip" "nat" {
  instance = aws_instance.nat.id
  vpc      = true
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.tog.id

  route {
    cidr_block  = local.public_access
    instance_id = aws_instance.nat.id
  }

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

resource "aws_security_group" "master" {
  vpc_id                 = aws_vpc.tog.id
  name                   = "EMR Master"
  revoke_rules_on_delete = true

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [local.public_access]
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${var.local_ip}/32"]
  }
}

resource "aws_security_group_rule" "slave_to_master" {
  source_security_group_id = "${aws_security_group.slave.id}"
  security_group_id        = "${aws_security_group.master.id}"
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
  type                     = "ingress"
}

resource "aws_security_group_rule" "master_to_slave" {
  source_security_group_id = "${aws_security_group.master.id}"
  security_group_id        = "${aws_security_group.slave.id}"
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
  type                     = "ingress"
}

resource "aws_security_group_rule" "slave_to_slave" {
  source_security_group_id = "${aws_security_group.slave.id}"
  security_group_id        = "${aws_security_group.slave.id}"
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
  type                     = "ingress"
}

resource "aws_security_group" "slave" {
  vpc_id                 = aws_vpc.tog.id
  name                   = "EMR Slave"
  revoke_rules_on_delete = true

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [local.public_access]
  }
}

resource "aws_security_group" "superserver" {
  vpc_id = aws_vpc.tog.id
  name   = "Superserver"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [local.public_access]
  }
  /* For spline to access Mongo from within the VPC */
  ingress {
    from_port   = 27017
    to_port     = 27017
    protocol    = "tcp"
    cidr_blocks = [local.public_access]
  }
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["${var.local_ip}/32"]
  }
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["${var.local_ip}/32"]
  }
  ingress {
    from_port   = 8081
    to_port     = 8081
    protocol    = "tcp"
    cidr_blocks = ["${var.local_ip}/32"]
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${var.local_ip}/32"]
  }
  tags = {
    Name = "Superserver Security Group"
  }
}

resource "aws_security_group" "nat" {
  name        = "NAT"
  description = "Allow traffic to pass from the private subnet to the internet"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.private_subnet_cidr]
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [var.private_subnet_cidr]
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [local.public_access]
  }
  ingress {
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = [local.public_access]
  }

  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [local.public_access]
  }
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [local.public_access]
  }
  egress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
  egress {
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = [local.public_access]
  }

  vpc_id = aws_vpc.tog.id

  tags = {
    Name = "NAT Security Group"
  }
}

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
    cidr_blocks = ["${var.pipeline_builder_ip}/32"]
  }
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
    cidr_blocks = ["${var.webserver_ip}/32"]
  }
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["${var.pipeline_builder_ip}/32"]
  }
  ingress {
    from_port   = 8081
    to_port     = 8081
    protocol    = "tcp"
    cidr_blocks = ["${var.pipeline_builder_ip}/32"]
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${var.pipeline_builder_ip}/32"]
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${var.webserver_ip}/32"]
  }
  tags = {
    Name = "Superserver Security Group"
  }
}

resource "aws_security_group" "glue_endpoint" {
  vpc_id      = aws_vpc.tog.id
  name        = "Glue Endpoint"
  description = "Allows traffic for glue"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [local.public_access]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [local.public_access]
  }
}

/*
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
*/

resource "aws_security_group" "emr_service_access" {
  vpc_id                 = aws_vpc.tog.id
  name                   = "EMR Service Access"
  revoke_rules_on_delete = true

  egress {
    from_port   = 8443
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = [local.public_access]
  }
}

resource "aws_security_group_rule" "slave_to_master" {
  source_security_group_id = aws_security_group.slave.id
  security_group_id        = aws_security_group.master.id
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
  type                     = "ingress"
}

resource "aws_security_group_rule" "master_to_slave" {
  source_security_group_id = aws_security_group.master.id
  security_group_id        = aws_security_group.slave.id
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
  type                     = "ingress"
}

resource "aws_security_group_rule" "slave_to_slave" {
  source_security_group_id = aws_security_group.slave.id
  security_group_id        = aws_security_group.slave.id
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
  type                     = "ingress"
}

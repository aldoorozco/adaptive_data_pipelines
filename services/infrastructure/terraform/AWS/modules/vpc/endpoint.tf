resource "aws_vpc_endpoint" "glue" {
  vpc_id            = aws_vpc.tog.id
  service_name      = "com.amazonaws.us-east-1.glue"
  vpc_endpoint_type = "Interface"

  subnet_ids         = [aws_subnet.public.id]
  security_group_ids = [aws_security_group.glue_endpoint.id]

  private_dns_enabled = true
}

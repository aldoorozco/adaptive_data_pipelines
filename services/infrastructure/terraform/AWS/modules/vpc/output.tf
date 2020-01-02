output "public_subnet_id" {
  value = aws_subnet.public.id
}

output "private_subnet_id" {
  value = aws_subnet.private.id
}

output "superserver_security_group" {
  value = aws_security_group.superserver.id
}

output "master_security_group" {
  value = aws_security_group.master.id
}

output "slave_security_group" {
  value = aws_security_group.slave.id
}

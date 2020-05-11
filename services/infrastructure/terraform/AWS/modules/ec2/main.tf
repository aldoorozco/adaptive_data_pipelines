resource "aws_iam_instance_profile" "iam_profile" {
  name = "iam_profile"
  role = var.iam_role
}

resource "aws_instance" "instance" {
  ami                  = "ami-0b69ea66ff7391e80"
  instance_type        = var.instance_type
  subnet_id            = var.public_subnet_id
  key_name             = var.ec2_keypair
  iam_instance_profile = aws_iam_instance_profile.iam_profile.id
  tags = {
    Name = var.instance_name
  }
  vpc_security_group_ids = [var.security_group]

  provisioner "remote-exec" {
    script = var.script_path
    connection {
      host        = aws_instance.instance.public_ip
      private_key = file("${path.root}/deploy")
      user        = "ec2-user"
      timeout     = "10m"
    }
  }
}

/*
resource "aws_eip" "elastic_ip" {
  vpc = true
}
resource "aws_eip_association" "eip_assoc" {
  instance_id   = aws_instance.instance.id
  allocation_id = aws_eip.elastic_ip.id
}
*/

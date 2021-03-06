
#---Skript-wide Vars---------------------------------
locals {
  websrv = toset([
    "cac_web_1", 
    "cac_web_2", 
    "cac_web_3"
  ])
  websrv_amount = 3
}

#---SSH Keys-----------------------------------------
resource "aws_key_pair" "cac4tec" {
  key_name   = "ubuntu"
  public_key = file("~/.ssh/id_rsa.pub")
}


#---VPCs and Sub Nets--------------------------------
resource "aws_vpc" "cac4tec" {
  cidr_block       = "192.168.0.0/16"
  instance_tenancy = "default"
  tags = {
    Name = "cac4tec"
  }
}

resource "aws_subnet" "cac4tec_a" {
  vpc_id     = aws_vpc.cac4tec.id
  cidr_block = "192.168.101.0/24"

  tags = {
    Name = "cac4tec_a"
  }
}

resource "aws_network_interface" "nics" {
  #for_each = local.websrv
  count = local.websrv_amount
  subnet_id   = aws_subnet.cac4tec_a.id
  security_groups = [ aws_security_group.cac4tec.id ]
  tags = {
    #Name = each.key
    Name = "web_nic_${count.index}"
  }
}

#---Secutity Groups----------------------------------
resource "aws_security_group" "cac4tec" {
  name        = "cac4tec-security-group"
  description = "Allow HTTP, HTTPS and SSH traffic"
  vpc_id      = aws_vpc.cac4tec.id
  
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "NFS4WEB"
    from_port   = 2049
    to_port     = 2049
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "terraform"
  }
}

#---Instances----------------------------------------
resource "aws_instance" "web" {
  #for_each = local.websrv
  count = local.websrv_amount

  key_name      = aws_key_pair.cac4tec.key_name
  ami           = "ami-0767046d1677be5a0"
  instance_type = "t2.micro"
  tags = {
    #Name = each.key
    Name = "websrv_${count.index}"
  }

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/id_rsa.pub")
    host        = self.public_ip
  }

  ebs_block_device {
    device_name = "/dev/sda1"
    volume_type = "gp2"
    volume_size = 8
  }

  network_interface {
    network_interface_id = aws_network_interface.nics[count.index].id
    device_index         = 0
  }
}

# resource "aws_eip" "web" {
#   for_each = local.websrv
#   vpc      = true
#   instance = aws_instance.web[each.key].id
# }

#---Internet Gateway---------------------------------
resource "aws_internet_gateway" "cac4tec_gw" {
  vpc_id = aws_vpc.cac4tec.id
}

resource "aws_eip" "web" {
  #for_each = local.websrv
  count = local.websrv_amount
  
  vpc = true
  instance                  = aws_instance.web[count.index].id
  associate_with_private_ip = aws_instance.web[count.index].private_ip
  depends_on                = [aws_internet_gateway.cac4tec_gw]
}

resource "aws_default_route_table" "cac4tec_rt" {
  default_route_table_id = aws_vpc.cac4tec.default_route_table_id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.cac4tec_gw.id
  }
  tags = {
    Name = "cac4tec_rt"
  }
}

#---Network Load Balancer and Target Group----------
resource "aws_lb_target_group" "cac4tectgt" {
  name        = "cac4tectgt"
  port        = 80
  protocol    = "TCP"
  target_type = "ip"
  vpc_id      = aws_vpc.cac4tec.id
}
resource "aws_lb_target_group_attachment" "cac4tectgta" {
  count = local.websrv_amount 
  target_group_arn = aws_lb_target_group.cac4tectgt.arn
  target_id        = aws_instance.web[count.index].private_ip
  port             = 80
}
resource "aws_lb" "cac4teclb" {
  name               = "cac4teclb"
  internal           = false
  load_balancer_type = "network"
  subnets            = [aws_subnet.cac4tec_a.id]

  enable_deletion_protection = false

  tags = {
    Environment = "cac4tec"
  }
}
resource "aws_lb_listener" "cac4tec_lb_listener" {
  load_balancer_arn = aws_lb.cac4teclb.arn
  port              = "80"
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.cac4tectgt.arn
  }
}


#---Central Storage----------------------------------
resource "aws_efs_file_system" "efs_web" {
  creation_token = "efs_web"
  performance_mode = "generalPurpose"
  throughput_mode = "bursting"
  encrypted = "false"
  tags = {
    Name = "Efs4Web"
  }
}

resource "aws_efs_mount_target" "efs_mt_web" {
  file_system_id  = aws_efs_file_system.efs_web.id
  subnet_id = aws_subnet.cac4tec_a.id
  security_groups = [aws_security_group.cac4tec.id]
}



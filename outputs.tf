output "instance_ips" {
  value = {
    for instance in aws_instance.web:
    instance.id => { 
      "public_ip": instance.public_ip,
      "private_ip": instance.private_ip,
      "subnet": instance.subnet_id
    }
    #if instance.associate_public_ip_address
  }
  #value = aws_instance.web["cac_web_1"].public_ip
}

output "public_ips" {
  value =  {
    for pip in aws_eip.web:
    pip.id => {
      "public_ip": pip.public_ip,
      "associate_with_private_ip ": pip.associate_with_private_ip,
      "private_ip ": pip.private_ip
    }
  }
}

output "efs_connect_ip" {
  value = [ aws_efs_mount_target.efs_mt_web.ip_address ]
}
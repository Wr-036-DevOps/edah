output "public-ip" {
  value = aws_instance.mtc_node.*.public_ip
}
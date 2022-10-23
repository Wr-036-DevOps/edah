#---root/variables---
variable "region" {
  default = "us-west-2"
}

variable "access_ip" {
  type = string
}

#----database----

variable "dbname" {
  type      = string
  sensitive = true
}

variable "dbuser" {
  type      = string
  sensitive = true
}

variable "dbpass" {
  type      = string
  sensitive = true
}
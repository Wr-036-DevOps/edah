#!/bin/bash
echo "export SQLALCHEMY_DATABASE_URI=postgres://${dbuser}:${dbpass}@${db_endpoint}/${dbname}" >> /etc/profile
sudo apt-get update -y
sudo apt-get install python3-venv -y
python3 -m venv venv
source venv/bin/activate
sudo apt install nginx -y

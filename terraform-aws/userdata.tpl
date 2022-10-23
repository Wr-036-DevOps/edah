#!/bin/bash
echo "export SQLALCHEMY_DATABASE_URI=postgres://${dbuser}:${dbpass}@${db_endpoint}/${dbname}" >> /etc/profile

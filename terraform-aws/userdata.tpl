#!/bin/bash
sudo hostnamectl set-hostname mtc-${nodename} &&
curl -sfL https://get.k3s.io | sh -s - server \
--datasource-endpoint="postgres://${dbuser}:${dbpass}@${db_endpoint}/${dbname}" \
--write-kubeconfig-mode 644
export DATABASE_URI="postgres://${dbuser}:${dbpass}@${db_endpoint}/${dbname}"

#!/bin/bash

WRKDIR=$PWD

cd $WRKDIR/Ansible

if ! python3 --version
then
  echo "Is python3 installed? we need it..."
  exit
fi
if ! ansible --version
then
  sudo apt update
  sudo apt install software-properties-common
  sudo apt-add-repository --yes --update ppa:ansible/ansible
  sudo apt install -y ansible
fi

python3 terraform_output_takeover.py
ansible-playbook -i inventory_generated.yaml --become 01_base-stack-config.yaml
ansible-playbook -i inventory_generated.yaml --become 02_webapp-config.yaml

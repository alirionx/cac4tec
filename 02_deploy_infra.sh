#!/bin/bash

WRKDIR=$PWD

if ! command -v terraform -v &> /dev/null
then
  sudo apt update
  sudo apt install -y unzip
  mkdir tmpdl
  cd tmpdl
  wget https://releases.hashicorp.com/terraform/0.14.7/terraform_0.14.7_linux_amd64.zip
  unzip terraform_0.14.7_linux_amd64.zip
  sudo mv terraform /usr/local/bin/terraform 
  sudo chmod +x /usr/local/bin/terraform
  cd $WRKDIR
  rm -R tmpdl
fi

cd $WRKDIR/Terraform
if [ ! -f "creds.tf" ]; then
  echo "please configure your credentials first (creds.tf)."
  exit
fi

if [ ! -f "~/.ssh/id_rsa.pub" ]; then
  ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa <<<y 2>&1 >/dev/null
fi

if ! terraform init
then
  echo "Failed to init terraform in this directory."
fi

if ! terraform plan
then
  echo "Failed plan terraform config."
fi

terraform apply

cd $WRKDIR



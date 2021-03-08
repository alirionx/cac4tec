#!/bin/bash

TGTDIR=$PWD/webapp/backend/dist

export DEBIAN_FRONTEND=noninteractive


if ! command -v node --version &> /dev/null
then
  apt update
  apt install -y curl
  curl -fsSL https://deb.nodesource.com/setup_15.x | bash -
  apt install -y nodejs
fi

cd webapp/spa
npm install
npm run build
cp -R dist/* $TGTDIR/


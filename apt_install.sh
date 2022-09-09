#!/bin/bash
echo "This script needs root"
echo "install docker, venv, requirements into venv"
sudo apt update && sudo apt upgrade && sudo apt install python3 python3-dev python3-pip ca-certificates curl  gnupg lsb-release postfix supervisor nginx git

#sudo mkdir -p /etc/apt/keyrings
#curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
#echo \
#  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
#  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
#sudo pip3 install docker-compose

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin   build-essential libpq-dev
sudo docker-compose build
sudo docker-compose up -d

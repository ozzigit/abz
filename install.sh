#!/bin/bash
sudo apt update && sudo apt upgrade && sudo apt install python3 python3-dev python3-pip ca-certificates curl  gnupg lsb-release git
git clone git@github.com:ozzigit/abz.git
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
cd abz
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

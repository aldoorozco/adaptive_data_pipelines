#!/bin/bash

sudo rm -f /var/run/yum.pid
sudo yum update -y &>/dev/null
sudo amazon-linux-extras install docker -y &>/dev/null
sudo systemctl start docker
sudo systemctl enable docker
sudo yum install git -y &>/dev/null

repo="adaptive_data_pipelines"
git clone https://github.com/aldoorozco/$repo.git &>/dev/null

compose_repo="https://github.com/docker/compose/releases/download/1.24.0/docker-compose-`uname -s`-`uname -m`"
sudo curl -L $compose_repo | sudo tee /usr/local/bin/docker-compose &> /dev/null
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

echo "Spinning up remote services..."
cd $repo/services && bash ./setup.sh remote up &> /dev/null

if [ $? -ne 0 ]; then
   echo "[ERROR] unable to setup remote services"
   exit 1
fi

echo "Done"

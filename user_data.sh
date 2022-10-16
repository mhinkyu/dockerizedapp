#!/bin/bash

sudo yum update -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
# API_KEY=$(aws ssm get-paramter --query Parameter.Value --name api_key --output text)
sudo amazon-linux-extras install docker -y
sudo systemctl start docker
sudo usermod -a -G docker ec2-user
sudo systemctl enable docker
sudo curl -SL https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
sudo yum install git -y
git clone https://github.com/mhinkyu/dockerizedapp.git
sudo cd ./MoviePoster-web/
sudo docker build . -t app:latest
sudo docker-compose -f Movie_compose.yaml up

#make sure that the ec2 user has IAM ROLE to access the SSM parameter store.
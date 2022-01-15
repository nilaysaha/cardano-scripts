#!/bin/sh

sudo ufw reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
#sudo ufw allow 443
sudo ufw allow 3001
sudo ufw allow 22
#sudo ufw allow 1337
#sudo ufw allow 51820/udp
sudo ufw enable
sudo ufw status verbose

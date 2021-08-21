#!/bin/sh

sudo ufw reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 8302 #for Mina protocol testing
sudo ufw allow 3001
sudo ufw allow 2222
sudo ufw allow 443
sudo ufw allow 80 #for certbot
sudo ufw allow 51820/udp
sudo ufw deny out to 172.16.0.0/12
sudo ufw deny out to 192.168.0.0/16
sudo ufw deny out to 100.64.0.0/10
sudo ufw deny out to 169.254.0.0/16
sudo ufw deny out to 10.0.0.0/8
sudo ufw enable

sudo ufw status verbose

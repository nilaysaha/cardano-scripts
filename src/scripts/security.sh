#!/bin/sh

sudo ufw reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 3001
sudo ufw allow 2222
sudo ufw enable

sudo ufw status verbose

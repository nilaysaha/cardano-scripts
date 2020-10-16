#!/bin/sh

sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 3001
sudo ufw enable

sudo ufw status verbose

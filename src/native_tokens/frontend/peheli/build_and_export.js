#!/bin/sh


npm run build
sudo rm -rf /var/www/html/peheli
sudo mkdir -p /var/www/html/peheli
sudo cp -a dist/. /var/www/html/peheli

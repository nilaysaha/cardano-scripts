#!/bin/sh


npm run build
sudo rm -rf /var/www/html/rcircle
sudo mkdir -p /var/www/html/rcircle
sudo cp -a dist/. /var/www/html/rcircle

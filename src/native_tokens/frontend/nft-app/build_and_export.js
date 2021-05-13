#!/bin/sh

ng build --prod
sudo mkdir -p /var/www/html/nftapp
sudo cp -a dist/. /var/www/html/nftapp

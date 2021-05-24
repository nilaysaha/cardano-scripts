#!/bin/sh

ng build --configuration production
sudo mkdir -p /var/www/html/nftapp
sudo cp -a dist/. /var/www/html/nftapp

#!/bin/sh

ng build --configuration production
sudo rm -rf /var/www/html/nft-app
sudo cp -a dist/. /var/www/html

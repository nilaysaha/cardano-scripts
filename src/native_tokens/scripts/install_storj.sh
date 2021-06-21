#!/bin/sh

curl -L https://github.com/storj/storj/releases/latest/download/uplink_linux_amd64.zip -o uplink_linux_amd64.zip
unzip -o uplink_linux_amd64.zip
chmod 755 uplink
sudo mv uplink /usr/local/bin/uplink

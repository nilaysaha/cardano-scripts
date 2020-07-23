#!/bin/sh

rm -rf state-node-shelly-testnet/
sudo systemctl daemon-reload;sudo systemctl stop shelly-cardano; sudo systemctl start shelly-cardano

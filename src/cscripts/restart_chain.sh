#!/bin/sh

echo "Now sending signal 2 to terminate chain"
kill -2 `pgrep -u nsaha cardano-node`
sudo systemctl daemon-reload

echo "Now sleeping for 60s"
sleep 60s

echo "Now restarting chain"
sudo systemctl start shelly-cardano
systemctl status shelly-cardano

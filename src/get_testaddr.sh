#!/bin/sh

if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

ADDRESS=$1
curl -v -XPOST "https://faucet.ff.dev.cardano.org/send-money/${ADDRESS}"

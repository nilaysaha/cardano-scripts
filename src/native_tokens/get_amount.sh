#!/bin/sh

UUID=$1
PAY_FILE="./sessions/$UUID/pay.addr"
TESTNET_MAGIC=1097911063

if [ $# -ne 1 ]; then
    echo "The number of arguments provided is incorrect. Please provide the UUID where the pay address will be stored"
    echo "Example: ./get_amount.sh <uuid>"
    exit 1
fi

cardano-cli query utxo --address `cat $PAY_FILE` --testnet-magic ${TESTNET_MAGIC}

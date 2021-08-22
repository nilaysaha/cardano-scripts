#!/bin/sh

UUID=$1

if [ $# -ne 1 ]; then
    echo "The number of arguments provided is incorrect. Please provide the UUID where the recipient address will be stored"
    echo "Example: ./create_recv_addr.sh <uuid>"
    exit 1
fi


TESTNET_MAGIC="1097911063"
TARGET_DIR="./sessions/${UUID}/recipient"

if [ ! -d "$TARGET_DIR" ]; then
    # Control will enter ere if $DIRECTORY doesn't exist.
    mkdir -p $TARGET_DIR
fi

VKEY="${TARGET_DIR}/recipientpay.vkey"
SKEY="${TARGET_DIR}/recipientpay.skey"
RADDR="${TARGET_DIR}/recipientpay.addr"

cardano-cli address key-gen \
    --verification-key-file ${VKEY} \
    --signing-key-file ${SKEY}


cardano-cli address build \
	    --payment-verification-key-file ${VKEY} \
	    --out-file ${RADDR} \
	    --testnet-magic ${TESTNET_MAGIC}



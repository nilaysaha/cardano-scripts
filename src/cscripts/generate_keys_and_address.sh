#!/bin/sh

BASE_DIR=$PWD/kaddr_mainnet
TESTNET_MAGIC=42

if [ ! -d "$BASE_DIR" ]; then
    mkdir ${BASE_DIR}
fi


#First generate payment keys
cardano-cli shelley address key-gen \
	    --verification-key-file $BASE_DIR/payment.vkey \
	    --signing-key-file $BASE_DIR/payment.skey;


#generate stake keys
cardano-cli shelley stake-address key-gen \
	    --verification-key-file $BASE_DIR/stake.vkey \
	    --signing-key-file $BASE_DIR/stake.skey;


#generate payment address
cardano-cli shelley address build \
	    --payment-verification-key-file $BASE_DIR/payment.vkey \
	    --stake-verification-key-file $BASE_DIR/stake.vkey \
	    --out-file $BASE_DIR/payment.addr \
	    --testnet-magic $TESTNET_MAGIC;


#generate stake address
cardano-cli shelley stake-address build \
	    --stake-verification-key-file $BASE_DIR/stake.vkey \
	    --out-file $BASE_DIR/stake.addr \
	    --testnet-magic $TESTNET_MAGIC;

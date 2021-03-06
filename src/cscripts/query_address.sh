#!/bin/sh

TESTNET_MAGIC=42
PAYMENT_ADDR=`cat ../backup/kaddr/payment.addr`
cardano-cli query utxo \
	    --mary-era \
	    --address $PAYMENT_ADDR \
	    --mainnet

#!/bin/sh

TESTNET_MAGIC=42
PAYMENT_ADDR=`cat ./kaddr/payment.addr`
cardano-cli shelley query utxo \
	    --address $PAYMENT_ADDR \
	    --testnet-magic ${TESTNET_MAGIC} \
	    --out-file ./kaddr/utx0

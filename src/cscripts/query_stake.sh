#!/bin/sh

TESTNET_MAGIC=42
STAKE_ADDR=`cat ./kaddr/stake.addr`
cardano-cli shelley query utxo --shelley-mode \
	    --address $STAKE_ADDR \
	    --testnet-magic ${TESTNET_MAGIC}


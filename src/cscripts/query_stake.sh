#!/bin/sh

TESTNET_MAGIC=mainnet
STAKE_ADDR=`cat ../backup/kaddr/stake.addr`
echo "stake address is:${STAKE_ADDR}"
cardano-cli query stake-address-info \
	    --allegra-era \
	    --mainnet \
	    --address ${STAKE_ADDR}

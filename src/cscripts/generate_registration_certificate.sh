#!/bin/sh

STAKE_KEY=./kaddr/stake.vkey

cardano-cli shelley stake-address registration-certificate \
     --staking-verification-key-file ${STAKE_KEY} \
     --out-file ./kaddr/stake.cert

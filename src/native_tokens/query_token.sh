#!/bin/sh

cardano-cli query utxo  --address `cat ./kaddr_token/pay.addr` --mainnet --mary-era

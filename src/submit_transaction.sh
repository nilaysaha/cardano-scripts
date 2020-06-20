#!/bin/sh

cardano-cli shelley transaction submit \
--tx-file tx.signed \
--testnet-magic 42

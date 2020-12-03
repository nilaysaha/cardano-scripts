#!/bin/sh


VKEY="./kaddr_node/cold.vkey"
cardano-cli shelley stake-pool id  --cold-verification-key-file ${VKEY}

#!/bin/sh


VKEY="./kaddr_node/cold.vkey"
cardano-cli shelley stake-pool id --verification-key-file $VKEY

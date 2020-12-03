#!/bin/sh

cardano-cli shelley query protocol-parameters \
	    --testnet-magic 42 \
	    --out-file ./kaddr/protocol.json

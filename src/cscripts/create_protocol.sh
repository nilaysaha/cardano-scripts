#!/bin/sh

NETWORK_MAGIC=42

cardano-cli shelley query protocol-parameters \
    --testnet-magic ${NETWORK_MAGIC} \
    --out-file ./kaddr/protocol.json

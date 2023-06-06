#!/bin/bash

SUBMIT_API="$HOME/.cabal/bin/cardano-submit-api"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SUBMIT_API_CONFIG="${SCRIPT_DIR}/../tconfig/preview/submit-api-config.json"

$SUBMIT_API --shelley-mode \
            --socket-path $CARDANO_NODE_SOCKET_PATH \
            --testnet-magic 2 \
            --listen-address 127.0.0.1 \
            --port 9001 \
            --config $SUBMIT_API_CONFIG

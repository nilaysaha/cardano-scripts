#!/bin/bash

SUBMIT_API="$HOME/.cabal/bin/cardano-submit-api"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SUBMIT_API_CONFIG="${SCRIPT_DIR}/../tconfig/preview/submit-api-config.json"
CARDANO_NODE_SOCKET_PATH='/home/nsaha/projects/cardano-scripts/exec/cardano-chain-data-store/./node.socket'

${SUBMIT_API} --config $SUBMIT_API_CONFIG --shelley-mode --socket-path $CARDANO_NODE_SOCKET_PATH --testnet-magic 2 --listen-address 127.0.0.1 --port 9001     

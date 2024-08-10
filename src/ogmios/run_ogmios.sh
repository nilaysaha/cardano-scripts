#!/bin/bash

OGMIOS=/home/nsaha/local/bin/ogmios
CARDANO_NODE_SOCKET=/home/nsaha/projects/cardano-scripts/exec/state-node-shelly-mainnet/node.socket
CARDANO_CONFIG=/home/nsaha/projects/cardano-scripts/src/tconfig/mainnet/config.json
HOST="0.0.0.0"

$OGMIOS --node-socket $CARDANO_NODE_SOCKET --node-config $CARDANO_CONFIG --host $HOST

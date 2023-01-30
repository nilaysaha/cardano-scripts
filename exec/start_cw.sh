#!/bin/bash

cardano-wallet serve \
    --port 8090 \
    --testnet $HOME/project/cardano-scripts/src/tconfig/preview/byron-genesis.json \
    --database ~/pspace/wallets/db \
    --node-socket $CARDANO_NODE_SOCKET_PATH

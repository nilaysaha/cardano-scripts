#!/bin/bash

CARDANO_WALLET="/home/nsaha/.cabal/bin/cardano-wallet"
CONFIG_FILE="$HOME/project/cardano-scripts/src/tconfig/preview/byron-genesis.json"
DB_DIR="$HOME/pspace/wallets/db"
SOCKET="$HOME/project/cardano-scripts/exec/cardano-chain-data-store/node.socket"

$CARDANO_WALLET serve --port 8090 --testnet $CONFIG_FILE --database $DB_DIR --node-socket $SOCKET

#!/bin/bash

CARDANO_WALLET="/home/nsaha/local/bin/cardano-wallet"
CONFIG_FILE="$HOME/projects/cardano-scripts/src/tconfig/mainnet/byron-genesis.json"
DB_DIR="$HOME/wallets/db"
SOCKET="$HOME/projects/cardano-scripts/exec/state-node-shelly-mainnet/node.socket"

$CARDANO_WALLET serve --port 8090 --testnet $CONFIG_FILE --database $DB_DIR --node-socket $SOCKET

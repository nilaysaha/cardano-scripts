#!/bin/bash

CARDANO_WALLET="/home/nsaha/.cabal/bin/cardano-wallet"
CONFIG_FILE="$HOME/projects/cardano-scripts/src/tconfig/preview/byron-genesis.json"
DB_DIR="$HOME/wallets/db"
SOCKET="$HOME/projects/cardano-scripts/exec/cardano-chain-data-store/node.socket"

$CARDANO_WALLET serve --port 8091 --testnet $CONFIG_FILE --database $DB_DIR --node-socket $SOCKET --token-metadata-server https://tokens.cardano.org --trace-wallet-db=debug 

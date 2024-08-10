#!/bin/bash

CARDANO_NODE=$HOME/.bin/cabal/cardano-node

PGPASSFILE=/home/nsaha/.bin/cabal/cardano-node/config/pgpass-mainnet cardano-db-sync-extended \
    +RTS -N -RTS \
    --config /home/cardano/cardano-node/config/mainnet-db-sync-config.json \
    --socket-path /home/cardano/cardano-node/db/node.socket \
    --state-dir /home/cardano/cardano-node/ledger-state/mainnet \
    --schema-dir /home/cardano/cardano-node/schema/

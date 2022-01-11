#!/bin/sh

DB_SYNC_DIR="../../../cardano-db-sync"
cd ${DB_SYNC_DIR}


#nix-build -A cardano-db-sync -o db-sync-node

SOCKET_DIR="../cardano-scripts/exec/state-node-shelly-mainnet/node.socket"  #relative to cardano-db-sync as we are now thre.
LEDGER_STATE_DIR="../cardano-scripts/exec/state-node-shelly-mainnet/db-ff/ledger/"
PGPASSFILE=config/pgpass-mainnet scripts/postgresql-setup.sh --createdb

echo "${PGPASSFILE}"

PGPASSFILE=config/pgpass-mainnet db-sync-node/bin/cardano-db-sync \
    --config ./config/mainnet-config.yaml \
    --socket-path ${SOCKET_DIR} \
    --state-dir ${LEDGER_STATE_DIR} \
    --schema-dir ./schema/

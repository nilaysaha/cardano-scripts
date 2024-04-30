#!/bin/sh

DB_SYNC_DIR="/home/nsaha/projects/cardano-db-sync"
cd ${DB_SYNC_DIR}

# DB_SYNC_TAG=13.1.0.0

# git checkout -b 13.1.0.0 tags/13.1.0.0
# nix-build -A cardano-db-sync -o db-sync-node

CS_DIR="${HOME}/projects/cardano-scripts"
SOCKET_DIR="${CS_DIR}/exec/cardano-chain-data-store/node.socket"  #relative to cardano-db-sync as we are now thre.
LEDGER_STATE_DIR="${CS_DIR}/exec/cardano-chain-data-store//db-ff/ledger/"
DB_SYNC_CONFIG="${DB_SYNC_DIR}/config/testnet-config.yaml"
DB_SYNC_SCHEMA="${DB_SYNC_DIR}/schema/"


# ${DB_SYNC_DIR}/scripts/postgresql-setup.sh --createdb
export PGPASSFILE="/home/nsaha/.pgpass"
echo ${PGPASSFILE}

DB_SYNC_BINARY="/home/nsaha/local/bin/cardano-db-sync"

${DB_SYNC_BINARY} \
    --config ${DB_SYNC_CONFIG} \
    --socket-path ${SOCKET_DIR} \
    --state-dir ${LEDGER_STATE_DIR} \
    --schema-dir ${DB_SYNC_SCHEMA}

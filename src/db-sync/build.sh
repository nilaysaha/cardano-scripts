#!/bin/sh

DB_SYNC_DIR="/home/nsaha/projects/cardano-db-sync"
cd ${DB_SYNC_DIR}

# DB_SYNC_TAG=13.1.0.0

# git checkout  -b ${DB_SYNC_TAG} tag-${DB_SYNC_TAG}
# nix-build -A cardano-db-sync -o db-sync-node

CS_DIR="/home/nsaha/projects/cardano-scripts"
DBSYNC_DIR="${HOME}/projects/cardano-db-sync"

SOCKET_DIR="${CS_DIR}/exec/state-node-shelly-mainnet/node.socket"  #relative to cardano-db-sync as we are now thre.
LEDGER_STATE_DIR="${CS_DIR}/exec/state-node-shelly-mainnet/db-ff/ledger/"
DB_SYNC_CONFIG="${HOME}/projects/cardano-db-sync/config/mainnet-config.yaml"
DB_SYNC_SCHEMA="${HOME}/projects/cardano-db-sync/cardano-db-sync/schema/"


# ${DB_SYNC_DIR}/scripts/postgresql-setup.sh --createdb
export PGPASSFILE="/home/nsaha/.pgpass"
echo ${PGPASSFILE}

DB_SYNC_BINARY="/home/nsaha/local/bin/cardano-db-sync"

${DB_SYNC_BINARY} \
    --config ${DB_SYNC_CONFIG} \
    --socket-path ${SOCKET_DIR} \
    --state-dir ${LEDGER_STATE_DIR} \
    --schema-dir ${DB_SYNC_SCHEMA}

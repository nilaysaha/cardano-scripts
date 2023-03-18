#!/bin/sh

export PGPASSFILE="/home/nsaha/.pgpass"

CS_DIR="/home/nsaha/projects/cardano-scripts"
CARDANO_DB_SYNC_DIR="/home/nsaha/projects/cardano-db-sync"
CARDANO_SNAPSHOT="/home/nsaha/opt/db-sync-snapshot-full.tgz"
LEDGER_STATE_DIR="${CS_DIR}/exec/cardano-chain-data-store/db-ff/ledger/"

${CARDANO_DB_SYNC_DIR}/scripts/postgresql-setup.sh --restore-snapshot ${CARDANO_SNAPSHOT} ${LEDGER_STATE_DIR}

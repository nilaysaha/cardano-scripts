#!/bin/bash

export PGPASSFILE="/home/nsaha/.pgpass"

CS_DIR="/home/nsaha/projects/cardano-scripts"
CARDANO_DB_SYNC_DIR="/home/nsaha/projects/cardano-db-sync"
CARDANO_SNAPSHOT="/tmp/db-sync-snapshot-schema-13.2-block-10251157-x86_64.tgz"
LEDGER_STATE_DIR="${CS_DIR}/exec/ledger_restore/"

${CARDANO_DB_SYNC_DIR}/scripts/postgresql-setup.sh --restore-snapshot ${CARDANO_SNAPSHOT} ${LEDGER_STATE_DIR}

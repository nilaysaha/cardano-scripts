#!/bin/sh


SLOTLEADER_CONFIG="./slotLeaderconfig.json"
LEDGER_FILE="/tmp/ledger.json"
cardano-cli query ledger-state --mainnet --out-file $LEDGER_FILE
EPOCH_NONCE=$(cardano-cli query protocol-state --mainnet | jq -r .csTickn.ticknStateEpochNonce.contents)
node cardanoLeaderLogs.js path/to/slotLeaderLogsConfig.json $EPOCH_NONCE

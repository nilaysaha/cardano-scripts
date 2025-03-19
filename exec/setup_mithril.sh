#!/bin/sh

# Cardano network
export CARDANO_NETWORK=preview

# Aggregator API endpoint URL
export AGGREGATOR_ENDPOINT=https://aggregator.pre-release-preview.api.mithril.network/aggregator

# Genesis verification key
export GENESIS_VERIFICATION_KEY=$(wget -q -O - https://raw.githubusercontent.com/input-output-hk/mithril/main/mithril-infra/configuration/pre-release-preview/genesis.vkey)

# Digest of the latest produced cardano db snapshot for convenience of the demo
export SNAPSHOT_DIGEST=latest


#list snapshots
mithril-client cardano-db snapshot list


#download
mithril-client cardano-db download d51a0019fcb2d22af7dabe147e41e5868dade01dd57c056078305014aae5d509

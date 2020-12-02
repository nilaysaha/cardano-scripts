#!/bin/sh

CARDANO_CLI='/home/nsaha/.cabal/bin/cardano-cli'
MARGIN=0.05

${CARDANO_CLI} shelley stake-pool registration-certificate \
	    --cold-verification-key-file ./kaddr_node/cold.vkey \
	    --vrf-verification-key-file ./kaddr_node/vrf.vkey \
	    --pool-pledge 90000000000 \
	    --pool-cost 50000 \
	    --pool-margin ${MARGIN} \
	    --pool-reward-account-verification-key-file ./kaddr/stake.vkey \
	    --pool-owner-stake-verification-key-file ./kaddr/stake.vkey \
	    --testnet-magic 42 \
	    --pool-relay-port 3001 \
	    --pool-relay-ipv4 116.203.215.60 \
	    --metadata-url https://shorturl.at/adhlW \
	    --metadata-hash 42b631e3cb1b159e291d763c7513ccf9a28d2151ae4131d620504f4ae3569e54 \
	    --out-file ./kaddr_node/pool_registration.cert

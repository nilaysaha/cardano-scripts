#!/bin/sh

cardano-cli shelley stake-pool registration-certificate \
--cold-verification-key-file pool-keys/cold.vkey \
--vrf-verification-key-file pool-keys/vrf.vkey \
--pool-pledge 128000000 \
--pool-cost 0 \
--pool-margin 0.5 \
--pool-reward-account-verification-key-file pool/stake.vkey \
--pool-owner-stake-verification-key-file owner1/stake.vkey \
--pool-owner-stake-verification-key-file owner2/stake.vkey \
--testnet-magic 42 \
--pool-relay-port 3001 \
--pool-relay-ipv4 XXX.XXX.XXX.XXX \
--metadata-url https://crypto2099.io/willo.json \
--metadata-hash 3db1...fe4f2e8f289c475416363768549 \
	    --out-file pool-keys/pool.cert


#and here's the transaction:

cardano-cli shelley transaction build-raw \
--tx-in 953...#0 \
--tx-out $(cat pool/payment.addr)+99498550000 \
--ttl 450000 --fee 250000 --out-file tx.raw \
--certificate-file pool-keys/pool.cert \
--certificate-file pool/delegation.cert \
--certificate-file owner1/delegation.cert \
--certificate-file owner2/delegation.cert


#sign the transaction
cardano-cli shelley transaction sign \
--tx-body-file tx.raw \
--signing-key-file pool/payment.skey \
--signing-key-file pool/stake.skey \
--signing-key-file owner1/stake.skey \
--signing-key-file owner2/stake.skey \
--signing-key-file pool-keys/cold.skey \
--testnet-magic 42 \
--out-file tx.signed

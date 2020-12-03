#!/bin/sh

cardano-cli shelley transaction calculate-min-fee \
     --tx-in-count 1 \
     --tx-out-count 1 \
     --ttl 200000 \
     --testnet-magic 42 \
     --signing-key-file payment.skey \
     --signing-key-file stake.skey \
     --certificate-file stake.cert \
     --protocol-params-file protocol.json

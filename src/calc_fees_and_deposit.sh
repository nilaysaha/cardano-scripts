#!/bin/sh

cardano-cli shelley transaction calculate-min-fee \
--tx-in-count 1 \
--tx-out-count 1 \
--ttl 1115574 \
--testnet-magic 42 \
--signing-key-file kaddr/payment.skey \
--signing-key-file kaddr/stake.skey \
--certificate-file kaddr/stake.cert \
--protocol-params-file kaddr/protocol.json

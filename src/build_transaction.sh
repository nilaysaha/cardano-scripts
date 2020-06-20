#!/bin/sh

cardano-cli shelley transaction build-raw \
--tx-in b64ae44e1195b04663ab863b62337e626c65b0c9855a9fbb9ef4458f81a6f5ee#1 \
--tx-out $(cat payment.addr)+998483580 \
--ttl 1116420 \
--fee 171485 \
--out-file tx.raw \
--certificate-file stake.cert

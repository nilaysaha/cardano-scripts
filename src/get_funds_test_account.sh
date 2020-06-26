#!/bin/sh

PAYMENT_ADDR=`cat ./kaddr/payment.addr`
curl -v -XPOST "https://faucet.shelley-testnet.dev.cardano.org/send-money/$PAYMENT_ADDR"
`

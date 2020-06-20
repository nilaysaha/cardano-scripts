#!/bin/sh

PAYMENT_ADDR=`cat ./kaddr/payment.addr`
curl -v -XPOST "https://faucet.ff.dev.cardano.org/send-money/$PAYMENT_ADDR"

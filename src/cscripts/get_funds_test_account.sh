#!/bin/sh

PAYMENT_ADDR=`cat ./kaddr/payment.addr`
APIKEY=""
curl -v -XPOST "https://faucet.mainnet-candidate-4.dev.cardano.org/send-money/${PAYMENT_ADDR}?apiKey=${APIKEY}"

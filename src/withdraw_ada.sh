#!/bin/sh

SESSION=$1
AMOUNT=$2

if [ "$#" -ne 2 ];then
    echo "Not sufficient parameters. We need SESSION id and the AMOUNT as input"
    exit 0
fi

   
DEST_ADDR="addr_test1vpyk92350x8gajyefdr44lk5jmjn9f8y4udfxw34pka5pvgjqxw4j"
SRC_ADDR=$(cat ./native_tokens/sessions/$SESSION/pay.addr)

python3 transfer_ada.py --outputAddr $DEST_ADDR  --inputAddr $SRC_ADDR --payskey ./native_tokens/sessions/$SESSION/pay.skey --protocol ./native_tokens/sessions/$SESSION/protocol.json --amount $AMOUNT

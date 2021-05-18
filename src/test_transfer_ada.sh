#!/bin/sh

DEST_ADDR=$1
AMOUNT=$2

SOURCE_UUID=e96efe6b-0d79-4200-a610-bf7250502ce0
SOURCE_ADDR="addr_test1vpyk92350x8gajyefdr44lk5jmjn9f8y4udfxw34pka5pvgjqxw4j"


if [ $# -ne 2 ]; then
    echo "Not enough parameters provided. You should provide two parameters for this script"
    echo "./test_transfer_ada.sh DEST_ADDR AMOUNT (in ada)"
    echo "We are using the source of the funds as:$SOURCE_ADDR from UUID:$SOURCE_UUID"
    exit 2
fi
   


python3 transfer_ada.py --inputAddr $SOURCE_ADDR  --outputAddr $DEST_ADDR --amount $2

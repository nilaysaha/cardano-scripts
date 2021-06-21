#!/bin/sh

DEST_ADDR=$1
AMOUNT=$2

SOURCE_UUID=5cbeadba-c0dd-11eb-82c2-31ea057735b4
SOURCE_ADDR="addr_test1vzezxpug0fuehlk4edj0chk4a7ehvkc704z7sr4mggc68uqccxdmq"


if [ $# -ne 2 ]; then
    echo "Not enough parameters provided. You should provide two parameters for this script"
    echo "./test_transfer_ada.sh DEST_ADDR AMOUNT (in ada)"
    echo "We are using the source of the funds as:$SOURCE_ADDR from UUID:$SOURCE_UUID"
    exit 2
fi
   


python3 transfer_ada.py --inputAddr $SOURCE_ADDR  --outputAddr $DEST_ADDR --amount $2

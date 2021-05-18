#!/bin/sh


#Then send a request to the api server to execute a NFT CREATION request using curl
DEFAULTASSET="NFT1"
DEFAULTAMOUNT=10
DEFAULTADDR="addr_test1vpyk92350x8gajyefdr44lk5jmjn9f8y4udfxw34pka5pvgjqxw4j"
DEFAULTCOST=100
DEFAULTURL="/ipfs/testing"
DEFAULTFUNDUUID="598f0f56-6291-4ebc-bbbf-77f111bf8703"

SERVER_URL="https://nft.oef.io/api/nft"


ASSETNAME=${1:-$DEFAULTASSET} 
ASSETAMOUNT=${2:-$DEFAULTAMOUNT}
ASSETRECVADDR=${3:-$DEFAULTADDR}

send_req()
{
    command="curl -k -X POST $SERVER_URL -d assetName=$ASSETNAME -d assetAmount=$ASSETAMOUNT -d mintingCost=$DEFAULTCOST -d recvAddr=$DEFAULTADDR -d url=$DEFAULTURL"
    echo "Running command: ${command}"
    output=$(eval $command)
    echo $output
    return `echo $output|jq ".payment_addr"`
}


send_payment_for_processing()
{
    outputAddr=$1
    amount=$2
    #First transfer keys and protocol to /trans directory. Source of test funds
    cp ../sessions/$DEFAULTFUNDUUID/pay.skey ../../trans/.
    cp ../sessions/$DEFAULTFUNDUUID/protocol.json ../../trans/.

    cd ../..
    python3 transfer_ada.py --inputAddr `cat ./native_tokens/sessions/$DEFAULTFUNDUUID/pay.addr` --outputAddr $outputAddr --amount $amount
    cd native_tokens/server
}


fulfil_request(){
    #Then send a dummy request
    outputAddr=$(send_req)

    #Then send payment for issuing and transferring the token to the owner
    send_payment_for_processing   $outputAddr, $DEFAULTCOST
}

#fulfil_request
send_req
#send_payment_for_processing addr_test1vz3k3rw75v69xaj7xcck36k8avsrw2qh4walrke97ftd4mskjfd9r  100

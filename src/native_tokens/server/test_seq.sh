#!/bin/sh

# To test the entire backend sequence this script can be modified and used


#Then send a request to the api server to execute a NFT CREATION request using curl
DEFAULTASSET="NFT1"
DEFAULTAMOUNT=10
DEFAULTADDR=addr_test1vryumnwqqqqjsc85fewhtse767r64fm5uru0pnfnthuwpscknn4z8
DEFAULTCOST=100
DEFAULTURL="/ipfs/testing"
DEFAULTFUNDUUID="598f0f56-6291-4ebc-bbbf-77f111bf8703"


ASSETNAME=${1:-$DEFAULTASSET} 
ASSETAMOUNT=${2:-$DEFAULTAMOUNT}
ASSETRECVADDR=${3:-$DEFAULTADDR}


help()
{
    echo "Please input the following parameters if you want to modify the defaults: ./test_seq.sh ASSETNAME ASSETAMOUNT ASSETRECVADDR"
}


start_backend_process()
{
    echo "Now starting the monitoring process to pick up the UUID passed onto the redis queue list by the web based request"
    python3 ../monitor_payment.py --run
}


send_req()
{
    command='curl -X post localhost:5000/nft \
	   -d "assetName=${ASSETNAME}&assetAmount=${ASSETAMOUNT}&mintingCost=${DEFAULTCOST}&recvAddr=${DEFAULTADDR}&url=${DEFAULTURL}"'
    echo "Running command: ${command}"
    output=$(eval $command)
    return `echo $output|jq "payment_addr"`
}

start_api_server()
{
    echo "Now starting the API server"
    #First start the API server
    python3 nft_api.py   
}


send_payment_for_processing()
{
    outputAddr=$1
    amount=$2
    #First transfer keys and protocol to /trans directory. Source of test funds
    cp ../sessions/$DEFAULTFUNDUUID/pay.skey ../../trans/.
    cp ../sessions/$DEFAULTFUNDUUID/protocol.json ../../trans/.

    python3 ../../transfer_ada.py --inputAddr `cat ../sessions/$DEFAULTFUNDUUID/pay.addr` --outputAddr $outputAddr --amount $amount
}

main()
{
    #First backend 
    start_backend_process

    #Then start the api server
    start_api_server

    #Then send a dummy request
    outputAddr=$(send_req)

    #Then send payment for issuing and transferring the token to the owner
    send_payment_for_processing   $outputAddr, $DEFAULTCOST
}


main



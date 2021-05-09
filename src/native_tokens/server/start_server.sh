#!/bin/sh

SERVER_OPTION=$1

# To test the entire backend sequence this script can be modified and used

start_backend_process()
{
    echo "Now starting the monitoring process to pick up the UUID passed onto the redis queue list by the web based request"
    python3 ../monitor_payment.py --run &
}


start_api_server()
{
    echo "Now starting the API server"
    #First start the API server
    python3 nft_api.py   &
}


main_server()
{
    echo "First killing python3 processes"
    pkill -9 python3
    
    #First backend
    echo "Now starting backend processes to monitor payments"
    start_backend_process

    #Then start the api server
    echo "Now starting the api server"
    start_api_server
}

echo $SERVER_OPTION

if [ $SERVER_OPTION =  "API" ]
then
    echo "We need to start the NFT API server"
    start_api_server
fi

if [ $SERVER_OPTION =  "MONITOR" ]
then
    echo "We need to start the Payment Monitoring server"
    start_backend_process
fi

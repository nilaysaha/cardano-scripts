#!/bin/sh

# To test the entire backend sequence this script can be modified and used

start_backend_process()
{
    echo "Now starting the monitoring process to pick up the UUID passed onto the redis queue list by the web based request"
    full_path=$(realpath $0)
    echo $full_path
    dir_path=$(dirname $full_path)
    python3 $dir_path/../queue_task.py --run &
}


start_api_server()
{
    echo "Now starting the API server"
    full_path=$(realpath $0)
    echo $full_path
    dir_path=$(dirname $full_path)
    python3 $dir_path/../nft_api.py&
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

if [ "$1" =  "API" ]
then
    echo "We need to start the NFT API server"
    start_api_server
fi

if [ "$1" =  "MONITOR" ]
then
    echo "We need to start the Payment Monitoring server"
    start_backend_process
fi

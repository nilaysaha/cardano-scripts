#!/bin/sh

SCRIPTDIR=`dirname "$BASH_SOURCE"`
echo ${SCRIPTDIR}
NODE_DIR="${SCRIPTDIR}/../state-node-shelly-testnet"

BASE_CONFIG="${SCRIPTDIR}/../../src/tconfig/testnet-config.json"
SOCKET="${NODE_DIR}/node.socket"
HOST_IP="$(wget http://ipecho.net/plain -O - -q ; echo)"

echo "config is $BASE_CONFIG"
echo "socket is $SOCKET"


ogmios \
  --host "127.0.0.1"\
  --node-config $BASE_CONFIG \
  --node-socket $SOCKET

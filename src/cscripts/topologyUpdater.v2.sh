#!/bin/bash

USERNAME="nsaha" # replace nonroot with your username

CNODE_BIN="/home/${USERNAME}/.cabal/bin"
CNODE_HOME="/home/nsaha/projects/cardano/cardano-scripts"
CNODE_LOG_DIR="${CNODE_HOME}/logs"

CNODE_PORT=3001  # must match your relay node port as set in the startup command
CNODE_HOSTNAME="relay-1.lkbh-pools.org"  # optional. must resolve to the IP you are requesting from
CNODE_VALENCY=1   # optional for multi-IP hostnames

TESTNET_MAGIC=RequiresNoMagic


export DISPLAY=":0"
export PATH="${CNODE_BIN}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
export SHELL="/bin/bash"
export CARDANO_NODE_SOCKET_PATH="${CNODE_HOME}/exec/state-node-shelly-mainnet/node.socket"

echo ${CARDANO_NODE_SOCKET_PATH}

blockNo=$(cardano-cli shelley query tip --mainnet | grep 'blockNo' |sed 's/.*://g'|sed 's/,//g'|xargs)

# Note:
# if you run your node in IPv4/IPv6 dual stack network configuration and want announced the
# IPv4 address only please add the -4 parameter to the curl command below  (curl -4 -s ...)

LOGFILE="$CNODE_LOG_DIR/topologyUpdater_lastresult.json"
if ! test -f "$LOGFILE"; then
    echo "\n${LOGFILE} does not exists. Creating...\n"
    touch ${LOGFILE};
fi

URL="https://api.clio.one/htopology/v1/?port=${CNODE_PORT}&blockNo=${blockNo}&valency=${CNODE_VALENCY}&magic=${TESTNET_MAGIC}${CNODE_HOSTNAME}"
echo $URL

curl -4 -s -v  $URL | tee -a $CNODE_LOG_DIR/topologyUpdater_lastresult.json

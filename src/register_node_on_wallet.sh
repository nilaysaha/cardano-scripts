#!/bin/sh

wget https://hydra.iohk.io/build/3315798/download/1/cardano-wallet-shelley-2020.6.5-linux64.tar.gz
tar -zxvf cardano-wallet-shelley-2020.6.5-linux64.tar.gz

2. start cardano wallet, something like this

~/files/wallet/cardano-wallet-shelley-2020.6.5/cardano-wallet-shelley serve --node-socket $CARDANO_NODE_SOCKET_PATH --testnet ~/files/relay2/shelley_testnet-genesis.json > ~/files/wallet/logs/cardanowallet.out 2>&1 &

3. [wait for a little while and then] query your pool keyword

~/files/wallet/cardano-wallet-shelley-2020.6.5/cardano-wallet-shelley stake-pool list --port 8090 --stake 1|jq '[.[]|select(has("metadata"))]' | grep -A 10 ANGEL

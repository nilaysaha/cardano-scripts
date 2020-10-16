#!/bin/sh

CARDANO_NODE_DIR="${HOME}/projects/cardano/cardano-node"

if [ -d ${CARDANO_NODE_DIR} ] 
then
    echo "Directory ${CARDANO_NODE_DIR} exists."
    echo "Now building new version of cardano-node"
    cd ${CARDANO_NODE_DIR}
    #cabal update
    #cabal build all
    mv ${HOME}/.cabal/store/ghc-8.6.5 /tmp/ghc-8.6.5-old
    cp -R ${CARDANO_NODE_DIR}/dist-newstyle/build/x86_64-linux/ghc-8.6.5 ${HOME}/.cabal/store/ghc-8.6.5
else
    echo "Error: Directory ${CARDANO_NODE_DIR} does not exists."
fi

#!/bin/sh

VERSION_ID=$1
STORAGE_DIR="./download_bin/"

if [ $# -ne 1 ]; then
    echo "The number of arguments provided is incorrect. Please provide the version of the binary."
    echo "Example: ./download_binaries.sh 1.25.1"
    exit 1
fi

if [ ! -d "$STORAGE_DIR" ]; then
    # Control will enter ere if $DIRECTORY doesn't exist.
    mkdir -p $STORAGE_DIR
fi

cd $STORAGE_DIR
BINARY_FILENAME=cardano-node-${VERSION_ID}-linux.tar.gz
wget https://github.com/input-output-hk/cardano-node/releases/download/${VERSION_ID}/${BINARY_FILENAME}
tar xvfz $BINARY_FILENAME

# aws s3 cp s3://stake-pool/cardano-cli-${VERSION_ID} $STORAGE_DIR/cardano-cli
# aws s3 cp s3://stake-pool/cardano-node-${VERSION_ID} $STORAGE_DIR/cardano-node
# aws s3 cp s3://stake-pool/cardano-node-chairman-${VERSION_ID} $STORAGE_DIR/cardano-node-chairman

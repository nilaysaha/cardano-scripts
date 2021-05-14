#!/bin/sh

VERSION_ID=$1
STORAGE_DIR="./download_bin/"

if [ $# -ne 1 ]; then
    echo "The number of arguments provided is incorrect. Please provide the version of the binary."
    echo "Example: ./download_and_install_binaries.sh 1.25.1"
    exit 1
fi

BASE_BINARY_DIR="$HOME/.cabal/bin"

#first download the binaries
./download_binaries.sh $VERSION_ID

#Now backup the current .cabal directory
DATE=$(date +%d/%m/%y)
BACKUP_BIN_DIR="$HOME/.cabal/bin_$DATE"


if [ ! -d "$BACKUP_BIN_DIR" ]; then
    # Control will enter here if $DIRECTORY does not exists.
    mkdir -p $BACKUP_BIN_DIR
fi

#now move the current binaries to backup dir
mv $BASE_BINARY_DIR/* $BACKUP_BIN_DIR/.

#And move the latest binary
mv $STORAGE_DIR/* $BASE_BINARY_DIR/.
for i in `ls $BASE_BINARY_DIR`
do
    chmod +x $BASE_BINARY_DIR/$i
done
    

#Now restart the blockchain
sudo systemctl stop shelly-cardano
sudo systemctl start shelly-cardano
systemctl status shelly-cardano

echo "We have downloaded the binaries and restarted the chain"
echo "Now run journalctl -u shelly-cardano -f to view the logs."
echo "Chow ...!"

#!/bin/sh

S3_FILENAME="db-ff-0122.tgz"
DOWNLOAD_DIR="/tmp"

echo "Downloading ${S3_FILENAME}"
aws s3 cp s3://stake-pool-backup/${S3_FILENAME} ${DOWNLOAD_DIR}

echo "Extracting the downloaded file"
tar xvfz "${DOWNLOAD_DIR}/${S3_FILENAME}"  -C ${DOWNLOAD_DIR}

ORIG_DB_DIR="../../exec/state-node-shelly-mainnet/"

echo "Now moving current db to bu"
mv "${ORIG_DB_DIR}/db-ff" "${DOWNLOAD_DIR}/db-ff-bu"

echo "Now restoring the s3 extraction to current db"
mv "${DOWNLOAD_DIR}/db-ff" "${ORIG_DB_DIR}/db-ff"


echo "Remove the current db to save space"
rm -rf "${DOWNLOAD_DIR}/db-ff-bu"
rm -rf "${DOWNLOAD_DIR}/${S3_FILENAME}"


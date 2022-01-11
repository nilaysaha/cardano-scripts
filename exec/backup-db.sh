#!/bin/sh

WEEK=$(date +"%V")
YEAR=$(date +"%Y")

BACKUP_DIR="/tmp/"
BACKUP_FILE="${BACKUP_DIR}/db-ff-$WEEK-$YEAR"

S3_BUCKET="stake-pool-backup"

echo "Now creating ${BACKUP_FILE} for this session"
tar cvfz ${BACKUP_FILE} "${PWD}/state-node-shelly-mainnet/db-ff"

echo "Now backing up the files to s3 bucket:${S3_BUCKET}"
aws s3 cp ${BACKUP_FILE} s3://${S3_BUCKET}/


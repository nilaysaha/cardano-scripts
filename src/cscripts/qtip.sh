#!/bin/sh

blockNo=$(cardano-cli query tip --mainnet | grep 'blockNo' |sed 's/.*://g'|sed 's/,//g')
echo $blockNo

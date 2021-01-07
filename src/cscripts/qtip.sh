#!/bin/sh

blockNo=$(cardano-cli shelley query tip --mainnet | grep 'blockNo' |sed 's/.*://g'|sed 's/,//g')
echo $blockNo

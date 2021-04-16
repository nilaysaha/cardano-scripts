#!/bin/sh

blockNo=$(cardano-cli query tip --mainnet | grep 'block' |sed 's/.*://g'|sed 's/,//g')
echo $blockNo

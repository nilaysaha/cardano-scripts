#!/bin/sh

blockNo=$(cardano-cli query tip --testnet-magic 1097911063 | grep 'block' |sed 's/.*://g'|sed 's/,//g')
echo $blockNo

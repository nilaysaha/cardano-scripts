#!/bin/sh

#assumes that cardano-wallet binary is installed in the path

cardano-wallet serve --blockfrost-token-file ~/config/blockfrost.txt --mainnet --listen-address 0.0.0.0 --light

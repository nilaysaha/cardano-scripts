#!/bin/sh

#Sample script just to encapsulate the commands required.
#As a next steps will be transferred to a python script for automation
#Page for following:https://developers.cardano.org/en/development-environments/native-tokens/working-with-multi-asset-tokens/

#Step 1:Generate a verification key and a signing key

cardano-cli address key-gen \
    --verification-key-file pay_bld.vkey \
    --signing-key-file pay_bld.skey


#Sample output
# $ cat pay.skey 
# {
#     "type": "PaymentSigningKeyShelley_ed25519",
#     "description": "Payment Signing Key",
#     "cborHex": "5820aed07e0b1ddd946da278ffb1f671cc5b24c8453e6b47c24b0a6b15d818444fe8"
# }
# $ cat pay.vkey 
# {
#     "type": "PaymentVerificationKeyShelley_ed25519",
#     "description": "Payment Verification Key",
#     "cborHex": "582031752dd50ffe7ed90ba136ea775dacd5113ff67d13001a25aac953f719aa1f92"
# }


# Step 2:Generate the payment address

./cardano-cli address build \
--payment-verification-key-file pay_bld.vkey \
--out-file pay_bld.addr \
--mainnet


# Step 3:Check the balance of the payment address

./cardano-cli query utxo --address `cat pay_bld.addr`   --mary-era --mainnet


#Step 4: Fund the address and now try query
./cardano-cli query utxo --address `cat pay_bld.addr`   --mary-era --mainnet


#Step 5: Export protocol parameters to a file for later use

cardano-cli  query protocol-parameters \
	     --mainnet \
	     --out-file protocol.json


#Step 6: Start the minting process

mkdir policy

cardano-cli address key-gen \
    --verification-key-file policy/policy.vkey \
    --signing-key-file policy/policy.skey


touch policy/policy.script && echo "" > policy/policy.script 


echo "{" >> policy/policy.script 
echo "  \"keyHash\": \"$(./cardano-cli address key-hash --payment-verification-key-file policy/policy.vkey)\"," >> policy/policy.script 
echo "  \"type\": \"sig\"" >> policy/policy.script 
echo "}" >> policy/policy.script 



#Step 7:Mint the new asset

./cardano-cli transaction policyid --script-file ./policy/policy.script 


#Step 8: Build raw transaction

./cardano-cli transaction build-raw \
	     --mary-era \
             --fee 0 \
             --tx-in b1ddb0347fed2aecc7f00caabaaf2634f8e2d17541f6237bbed78e2092e1c414#0 \
             --tx-out addr_test1vqvlku0ytscqg32rpv660uu4sgxlje25s5xrpz7zjqsva3c8pfckz+1000000000+"1000000000 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \
             --mint="1000000000 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \
             --out-file matx.raw


#step 9: Calculate minm fees

./cardano-cli transaction calculate-min-fee \
--tx-body-file matx.raw \
--tx-in-count 1 \
--tx-out-count 1 \
--witness-count 2 \
--testnet-magic 3 \
--protocol-params-file protocol.json


#Step 10:
./cardano-cli transaction build-raw \
	     --mary-era \
             --fee 180109 \
             --tx-in b1ddb0347fed2aecc7f00caabaaf2634f8e2d17541f6237bbed78e2092e1c414#0 \
             --tx-out addr_test1vqvlku0ytscqg32rpv660uu4sgxlje25s5xrpz7zjqsva3c8pfckz+999819891+"1000000000 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \
             --mint="1000000000 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \
             --out-file matx.raw


#Step 11: Sign transaciton
./cardano-cli transaction sign \
	     --signing-key-file pay.skey \
	     --signing-key-file policy/policy.skey \
	     --script-file policy/policy.script \
	     --testnet-magic 3 \
	     --tx-body-file matx.raw \
             --out-file matx.signed


#Step 12:submit transaction

./cardano-cli transaction submit --tx-file  matx.signed --mainnet




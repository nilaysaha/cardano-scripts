#!/bin/sh
export CARDANO_NODE_SOCKET_PATH='/tmp/node.socket'


if test -d './policy';
then
    echo "Directory ./policy  exists hence not creating"
else
    echo 'Now creating directory'
    mkdir -p './policy'
fi


FILE='./policy/policy.script'
if test -f "$FILE";
then
    echo "$FILE exists hence removing it."
    rm -f $FILE
    echo 'now proceed to create new $FILE'
fi

#generate key pairs
cardano-cli address key-gen \
            --verification-key-file policy/policy.vkey \
            --signing-key-file policy/policy.skey


echo "{" >> $FILE
echo "  \"type\": \"all\"," >> $FILE 
echo "  \"scripts\":" >> $FILE 
echo "  [" >> $FILE 
echo "   {" >> $FILE 
echo "     \"type\": \"before\"," >> $FILE 
echo "     \"slot\": $(expr $(cardano-cli query tip --testnet-magic 1567 | jq .slot?) + 10000)" >> $FILE
echo "   }," >> $FILE 
echo "   {" >> $FILE
echo "     \"type\": \"sig\"," >> $FILE 
echo "     \"keyHash\": \"$(cardano-cli address key-hash --payment-verification-key-file policy/policy.vkey)\"" >> $FILE 
echo "   }" >> $FILE
echo "  ]" >> $FILE 
echo "}" >> $FILE


#Now generate the policy id
echo "Now generating policy id and storing it in file:policy/policyID"
cardano-cli transaction policyid --script-file $FILE > policy/policyID


#Now generate metadata
#Gradually has to be tuned to the housing NFT generation by stiching together:
#<kyc_token_policy_id>.<document_nft_token_policy_id>.<house_metadata_token> => This will be sort of JWT token for the house. 

echo "Generating metadata for this sample NFT"

METADATA='./metadata.json'


echo "{" >> $METADATA
echo "  \"721\": {" >> $METADATA 
echo "    \"$(cat policy/policyID)\": {" >> $METADATA 
echo "      \"$(echo $realtokenname)\": {" >> $METADATA
echo "        \"description\": \"This is my first NFT thanks to the Cardano foundation\"," >> $METADATA
echo "        \"name\": \"Cardano foundation NFT guide token\"," >> $METADATA
echo "        \"id\": \"1\"," >> $METADATA
echo "        \"image\": \"ipfs://$(echo $ipfs_hash)\"" >> $METADATA
echo "      }" >> $METADATA
echo "    }" >> $METADATA 
echo "  }" >> $METADATA 
echo "}" >> $METADATA

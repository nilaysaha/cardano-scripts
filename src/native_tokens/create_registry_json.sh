#!/bin/sh

echo "Generate subject"
policyid="1a49530b152d1e090a0242ecfe79a5b6b7d28e57f0d9d1b64f42eba4"
assetname=$(echo -n "REIT" | xxd -ps)
subject="${policyid}${assetname}"

echo "-------------------------Prepare draft entry---------------------------------"
./token-metadata-creator entry --init ${subject}


echo "-----------------------Add required fields---------------------------------"
NAME="Real estate investment token"
DESCRIPTION="A protocol to unlock value and trade verified real estate assets"
POLICY="./kaddr_new/policy.script"

./token-metadata-creator entry "${subject}" --name "$NAME" --description "$DESCRIPTION" --policy "$POLICY"
	     
echo "Add optional fields"
TICKER="REIT"
URL="https://reitcircles.com"
LOGO="./kaddr_new/logo.png"
DECIMALS=6

./token-metadata-creator entry "${subject}" --ticker "$TICKER" --url "$URL" --logo "$LOGO" --decimals "$DECIMALS"

echo "Sign the data "
POLICYKEY="./kaddr_new/policy.skey"			       
./token-metadata-creator entry "${subject}" -a "${POLICYKEY}"

			       
echo "Finalize the data"
./token-metadata-creator entry "${subject}" --finalize


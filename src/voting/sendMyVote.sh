#!/bin/bash

# Script is brought to you by ATADA_Stakepool, Telegram @atada_stakepool in
# cooperation with @TheRealAdamDean (BUFFY & SPIKE)

###
# Change the following variables to match your configuration
###

CPATH="/home/<user>/cardano-node"
socket="${CPATH}/db/node.socket"
genesisfile="${CPATH}/config/testnet-shelley-genesis.json"
genesisfile_byron="${CPATH}/config/testnet-byron-genesis.json"
cardanocli="/home/<user>/.cabal/bin/cardano-cli"
cardanonode="/home/<user>/.cabal/bin/cardano-node"
byronToShelleyEpochs=208
magicparam="--mainnet"

###
# STOP EDITING!!!
###

if [[ -z $CARDANO_NODE_SOCKET_PATH ]]; then
  export CARDANO_NODE_SOCKET_PATH=${socket}
fi

dummyShelleyAddr="addr1vyde3cg6cccdzxf4szzpswgz53p8m3r4hu76j3zw0tagyvgdy3s4p"

###
# Define utility functions
###
exists() {
  command -v "$1" >/dev/null 2>&1
}

check_address() {
  tmp=$(${cardanocli} shelley address info --address $1 2> /dev/null)
  if [[ $? -ne 0 ]]; then echo -e "\e[35mERROR - Unknown address format for address: $1 !\e[0m"; exit 1; fi
}

#-------------------------------------------------------------
#Subroutine for user interaction
ask() {
    local prompt default reply

    if [ "${2:-}" = "Y" ]; then
        prompt="Y/n"
        default=Y
    elif [ "${2:-}" = "N" ]; then
        prompt="y/N"
        default=N
    else
        prompt="y/n"
        default=
    fi

    while true; do

        # Ask the question (not using "read -p" as it uses stderr not stdout)
        echo -ne "$1 [$prompt] "

        # Read the answer (use /dev/tty in case stdin is redirected from somewhere else)
        read reply </dev/tty

        # Default?
        if [ -z "$reply" ]; then
            reply=$default
        fi

        # Check if the reply is valid
        case "$reply" in
            Y*|y*) return 0 ;;
            N*|n*) return 1 ;;
        esac

    done
}
#-------------------------------------------------------

#-------------------------------------------------------
#Subroutines to calculate current epoch from genesis.json offline
get_currentEpoch() {
  local startTimeGenesis=$(cat ${genesisfile} | jq -r .systemStart)
  local startTimeSec=$(date --date=${startTimeGenesis} +%s)     #in seconds (UTC)
  local currentTimeSec=$(date -u +%s)                           #in seconds (UTC)
  local epochLength=$(cat ${genesisfile} | jq -r .epochLength)
  local currentEPOCH=$(( (${currentTimeSec}-${startTimeSec}) / ${epochLength} ))  #returns a integer number, we like that
  echo ${currentEPOCH}
}
#-------------------------------------------------------

#-------------------------------------------------------
#Subroutines to calculate current slotHeight(tip)
get_currentTip() {
  local currentTip=$(${cardanocli} shelley query tip ${magicparam} | jq -r .slotNo)
  echo ${currentTip}
}
#-------------------------------------------------------

#-------------------------------------------------------
#Subroutines to calculate current TTL
get_currentTTL() {
  echo $(( $(get_currentTip) + 10000 ))
}
#-------------------------------------------------------

#-------------------------------------------------------
#Displays an Errormessage if parameter is not 0
checkError()
{
if [[ $1 -ne 0 ]]; then echo -e "\n\n\e[35mERROR (Code $1) !\e[0m"; exit 1; fi
}
#-------------------------------------------------------

if ! exists jq; then
  echo -e "\nYou need the tool 'jq' !\n"
  echo -e "Install it On Ubuntu/Debian like:\n\e[97msudo apt update && sudo apt -y install jq\e[0m\n"
  echo -e "Thx! :-)\n"
  exit 2
fi

tempDir=$(dirname $(mktemp tmp.XXXX -ut))

#load variables from common.sh
#       socket          Path to the node.socket (also exports socket to CARDANO_NODE_SOCKET_PATH)
#       genesisfile     Path to the genesis.json
#       magicparam      TestnetMagic parameter
#       cardanocli      Path to the cardano-cli executable
# . "$(dirname "$0")"/00_common.sh

case $# in
  2 ) fromAddr="$1";
      metafile="$2.json";;
  * ) cat >&2 <<EOF
Usage:  $(basename $0) <From AddressName> <VoteFileName>
Note: Do not include file suffixes (i.e. .addr or .json)
EOF
  exit 1;; esac

#This is a simplified Version of the sendLovelaces.sh script so, it will always be a SendALLLovelaces transaction + Metafile
toAddr=${fromAddr}
lovelacesToSend="ALL"

#Throw an error if the voting.json file does not exist
if [ ! -f "${metafile}" ]; then
  echo -e "The specified VoteFileName.json (${metafile} file does not exist. Please try again."
  exit 1
fi

function readMetaParam() {
  required="${3:-0}"
  key=$(jq 'keys[0]' $2)
  param=$(jq -r ".$key .$1" $2 2> /dev/null)
  if [[ $? -ne 0 ]]; then echo "ERROR - ${2} is not a valid JSON file" >&2; exit 1;
  elif [[ "${param}" == null && required -eq 1 ]]; then echo "ERROR - Parameter \"$1\" in ${2} does not exist" >&2; exit 1;
  elif [[ "${param}" == "" && !required -eq 1 ]]; then echo "ERROR - Parameter \"$1\" in ${2} is empty" >&2; exit 1;
  fi
  echo "${param}"
}

objectType=$(readMetaParam "ObjectType" "${metafile}" 1); if [[ ! $? == 0 ]]; then exit 1; fi
objectVersion=$(readMetaParam "ObjectVersion" "${metafile}"); if [[ ! $? == 0 ]]; then exit 1; fi

if [[ $objectType == 'VoteBallot' ]]; then
  # Check VoteBallot required fields
  networkId=$(readMetaParam "NetworkId" "${metafile}" 1); if [[ ! $? == 0 ]]; then exit 1; fi
  proposalId=$(readMetaParam "ProposalId" "${metafile}" 1); if [[ ! $? == 0 ]]; then exit 1; fi
  voterId=$(readMetaParam "VoterId" "${metafile}" 1); if [[ ! $? == 0 ]]; then exit 1; fi
  yesnovote=$(readMetaParam "Vote" "${metafile}"); if [[ ! $? == 0 ]]; then exit 1; fi
  choicevote=$(readMetaParam "Choices" "${metafile}"); if [[ ! $? == 0 ]]; then exit 1; fi
  if [[ $yesnovote == null && $choicevote == null ]]; then
    echo "ERROR - No voting preferences found in ballot.";
    exit 1;
  fi
#else
#    echo "ERROR - JSON is not of type VoteBallot.";
#    exit 1;
fi

sendFromAddr=$(cat ${fromAddr}.addr)
sendToAddr=$(cat ${toAddr}.addr)
check_address "${sendFromAddr}"
# check_address "${sendToAddr}"

rxcnt="1"

#Choose between sending ALL funds or a given amount of lovelaces out
# if [[ ${lovelacesToSend^^} == "ALL" ]]; then
   #Sending ALL lovelaces, so only 1 receiver address
#  rxcnt="1"
# else
  #Sending a free amount, so 2 receiver addresses
#  rxcnt="2"  #transmit to two addresses. 1. destination address, 2. change back to the source address
# fi

echo
echo -e "\e[0mUsing lovelaces from Address\e[32m ${fromAddr}.addr\e[0m to send the metafile\e[32m ${metafile}\e[0m:"
echo

#get live values
currentTip=$(get_currentTip)
ttl=$(get_currentTTL)
currentEPOCH=$(get_currentEpoch)

echo -e "\e[0mCurrent Slot-Height:\e[32m ${currentTip} \e[0m(setting TTL to ${ttl})"
echo
echo -e "\e[0mSource/Destination Address ${fromAddr}.addr:\e[32m ${sendFromAddr} \e[90m"
echo -e "\e[0mAttached Metafile:\e[32m ${metafile} \e[90m"
echo

#Get UTXO Data for the sendFromAddr
utx0=$(${cardanocli} shelley query utxo --address ${sendFromAddr} --cardano-mode ${magicparam})
utx0linecnt=$(echo "${utx0}" | wc -l)
txcnt=$((${utx0linecnt}-2))

if [[ ${txcnt} -lt 1 ]]; then echo -e "\e[35mNo funds on the source Addr!\e[0m"; exit; else echo -e "\e[32m${txcnt} UTXOs\e[0m found on the source Addr!"; fi

echo

#Calculating the total amount of lovelaces in all utxos on this address
totalLovelaces=0
txInString=""

while IFS= read -r utx0entry
do
fromHASH=$(echo ${utx0entry} | awk '{print $1}')
fromHASH=${fromHASH//\"/}
fromINDEX=$(echo ${utx0entry} | awk '{print $2}')
sourceLovelaces=$(echo ${utx0entry} | awk '{print $3}')
echo -e "HASH: ${fromHASH}\t INDEX: ${fromINDEX}\t LOVELACES: ${sourceLovelaces}"

totalLovelaces=$((${totalLovelaces}+${sourceLovelaces}))
txInString=$(echo -e "${txInString} --tx-in ${fromHASH}#${fromINDEX}")

done < <(printf "${utx0}\n" | tail -n ${txcnt})

echo -e "Total lovelaces in UTX0:\e[32m  ${totalLovelaces} lovelaces \e[90m"
echo

#Getting protocol parameters from the blockchain, calculating fees
${cardanocli} shelley query protocol-parameters --cardano-mode ${magicparam} > protocol-parameters.json

#Get the current minUTxOvalue
minUTXO=$(jq -r .minUTxOValue protocol-parameters.json 2> /dev/null)

#Generate Dummy-TxBody file for fee calculation
txBodyFile="${tempDir}/dummy.txbody"
rm ${txBodyFile} 2> /dev/null
if [[ ${rxcnt} == 1 ]]; then  #Sending ALL funds  (rxcnt=1)
  ${cardanocli} shelley transaction build-raw ${txInString} --tx-out ${dummyShelleyAddr}+0 --ttl ${ttl} --fee 0 --metadata-json-file ${metafile} --out-file ${txBodyFile}
  checkError "$?"
else  #Sending chosen amount (rxcnt=2)
  ${cardanocli} shelley transaction build-raw ${txInString} --tx-out ${dummyShelleyAddr}+0 --tx-out ${dummyShelleyAddr}+0 --metadata-json-file ${metafile} --ttl ${ttl} --fee 0 --out-file ${txBodyFile}
  checkError "$?"
fi

fee=$(${cardanocli} shelley transaction calculate-min-fee --tx-body-file ${txBodyFile} --protocol-params-file protocol-parameters.json --tx-in-count ${txcnt} --tx-out-count ${rxcnt} ${magicparam} --witness-count 1 --byron-witness-count 0 | awk '{ print $1 }')
checkError "$?"
echo -e "\e[0mMinimum Transaction Fee for ${txcnt}x TxIn & ${rxcnt}x TxOut: \e[32m ${fee} lovelaces \e[90m"

#If sending ALL funds
if [[ ${rxcnt} == 1 ]]; then lovelacesToSend=$(( ${totalLovelaces} - ${fee} )); fi

#calculate new balance for destination address
lovelacesToReturn=$(( ${totalLovelaces} - ${fee} - ${lovelacesToSend} ))

#Checking about minimum funds in the UTXO
if [[ ${lovelacesToReturn} -lt 0 || ${lovelacesToSend} -lt 0 ]]; then echo -e "\e[35mNot enough funds on the source Addr!\e[0m"; exit; fi

#Checking about the minimum UTXO that can be transfered according to the current set parameters
lovelacesMinCheck=$(( ${totalLovelaces} - ${fee} )) #hold the value of the lovelaces that will be transfered out no mather what type of transaction
if [[ ${lovelacesMinCheck} -lt ${minUTXO} ]]; then echo -e "\e[35mAt least ${minUTXO} lovelaces must be transfered (ParameterSetting)!\e[0m"; exit; fi

echo -e "\e[0mLovelaces to return to ${toAddr}.addr: \e[33m ${lovelacesToSend} lovelaces \e[90m"

echo

txBodyFile="${tempDir}/$(basename ${fromAddr}).txbody"
txFile="${tempDir}/$(basename ${fromAddr}).tx"

echo
echo -e "\e[0mBuilding the unsigned transaction body: \e[32m ${txBodyFile} \e[90m"
echo

#Building unsigned transaction body
rm ${txBodyFile} 2> /dev/null
if [[ ${rxcnt} == 1 ]]; then  #Sending ALL funds  (rxcnt=1)
  ${cardanocli} shelley transaction build-raw ${txInString} --tx-out ${sendToAddr}+${lovelacesToSend} --ttl ${ttl} --fee ${fee} --metadata-json-file ${metafile} --out-file ${txBodyFile}
  checkError "$?"
else  #Sending chosen amount (rxcnt=2)
  ${cardanocli} shelley transaction build-raw ${txInString} --tx-out ${sendToAddr}+${lovelacesToSend} --tx-out ${sendFromAddr}+${lovelacesToReturn} --metadata-json-file ${metafile} --ttl ${ttl} --fee ${fee} --out-file ${txBodyFile}
  checkError "$?"
fi

cat ${txBodyFile}
echo

echo -e "\e[0mSign the unsigned transaction body with the \e[32m${fromAddr}.skey\e[0m: \e[32m ${txFile} \e[90m"
echo

#Sign the unsigned transaction body with the SecureKey
rm ${txFile} 2> /dev/null
${cardanocli} shelley transaction sign --tx-body-file ${txBodyFile} --signing-key-file ${fromAddr}.skey ${magicparam} --out-file ${txFile}
checkError "$?"

cat ${txFile}
echo

if ask "\e[33mDoes this look good for you, continue ?" N; then
        echo
        echo -ne "\e[0mSubmitting the transaction via the node..."
        ${cardanocli} shelley transaction submit --tx-file ${txFile} --cardano-mode ${magicparam}
        checkError "$?"
        echo -e "\e[32mDONE\n"
fi


echo -e "\e[0m\n"

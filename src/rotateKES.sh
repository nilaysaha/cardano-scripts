#!/bin/bash
#
tput clear
trap ctrl_c INT

function ctrl_c() {
        echo "**You pressed Ctrl+C...Exiting"
        exit 0;
}

echo -e "##############################################################################"
echo -e "##############################################################################"
echo "   _____          _____  _____          _   _  ____           ";
echo "  / ____|   /\   |  __ \|  __ \   /\   | \ | |/ __ \          ";
echo " | |       /  \  | |__) | |  | | /  \  |  \| | |  | |         ";
echo " | |      / /\ \ |  _  /| |  | |/ /\ \ | . \` | |  | |         ";
echo " | |____ / ____ \| | \ \| |__| / ____ \| |\  | |__| |         ";
echo "  \_____/_/__  \_\_|  \_\_____/_/__ _\_\_|_\_|\____/__ ______ ";
echo " | |/ /  ____|/ ____| |  __ \ / __ \__   __|/\|__   __|  ____|";
echo " | ' /| |__  | (___   | |__) | |  | | | |  /  \  | |  | |__   ";
echo " |  < |  __|  \___ \  |  _  /| |  | | | | / /\ \ | |  |  __|  ";
echo " | . \| |____ ____) | | | \ \| |__| | | |/ ____ \| |  | |____ ";
echo " |_|\_\______|_____/  |_|  \_\\____/  |_/_/    \_\_|  |______|";
echo "                                                              ";
echo
echo "v2.0.0"
echo "by FRADA stake pool"
echo
echo "#################################################################################"
echo "KES rotation companion script for cardano node installation with Coincashew guide"
echo "#################################################################################"
echo
echo "This companion script will help you rotate your KES keys and generate"
echo "a new node certificate. It is designed for a Coincashew installation"
echo 
echo "Tested for Ubuntu 22.04.2 LTS"
echo
echo "#########################################################################"
echo
# MOVE TO CARDANO HOME

export NODE_HOME='/home/nsaha/projects/cardano-scripts/src/kaddr_run'
cd $NODE_HOME

# KES KEYS ROTATION CHECK

echo
echo "---------------------------------------------------------------------"
echo " KES KEYS PERIOD AND COUNTER VALUE"
echo "---------------------------------------------------------------------"
echo
sleep 1
cardano-cli query kes-period-info --mainnet --op-cert-file $NODE_HOME/node.cert
echo
KES_PERIOD_OUTPUT=$(cardano-cli query kes-period-info --mainnet --op-cert-file $NODE_HOME/node.cert)
EXPIRY_DATE=$(echo $KES_PERIOD_OUTPUT | grep -oP '"qKesKesKeyExpiry": "\K[^"]+')
EXPIRY_TIMESTAMP=$(date -d "$EXPIRY_DATE" +%s)
CURRENT_TIMESTAMP=$(date +%s)
SECONDS_REMAINING=$((EXPIRY_TIMESTAMP - CURRENT_TIMESTAMP))
DAYS_REMAINING=$((SECONDS_REMAINING / 86400))
if [[ $DAYS_REMAINING -lt 1 ]]; then
	echo -e " \e[1;31mDANGER : KES key is about to expire in 1 day or has already expired !"
        echo -e " You must rotate your KES keys or your Cardano Node won't be able to validate blocks\e[0m"
elif [[ $DAYS_REMAINING -lt 8 && $DAYS_REMAINING -gt 1 ]]; then
        echo -e " [\e[1;33mWARNING\e[0m] Remaining days before KES key expires : "$DAYS_REMAINING
elif [[ $DAYS_REMAINING -lt 16 ]]; then
        echo -e " [\e[1;33mWARNING\e[0m] Remaining days before KES key expires : "$DAYS_REMAINING
else
        echo -e " [\e[1;32mOK\e[0m] KES Key valid. Remaining days before expiry : "$DAYS_REMAINING
fi
echo
echo
echo -e " \e[0;33m! REMINDER !\e[0m"
echo
echo " - If your pool minted at least 1 block since last KES rotation, qKesNodeState value and qKesOnDisk must be THE SAME"
echo " --> Your node.counter value on your air-gapped machine must be exactly 1 greater than qKesNodeState value"
echo
echo " - If your pool did not mint a block since KES rotation, qKesNodeState value should be 1 less than qKesOnDisk value"
echo " --> In that case, node.counter value on your air-gapped machine needs to be rolled back by exactly 1"
echo
echo " - If your pool never minted a block since its creation, qKesNodeState should be 'null'"
echo " --> In that case, node.counter value on your air-gapped machine must be set to '0'"
echo

# BACKUP

echo
echo "---------------------------------------------------------------------"
echo " BACKUP KES KEYS AND NODE CERT"
echo "---------------------------------------------------------------------"
echo
sleep 1

VALID_ANSWER=false
while [[ $VALID_ANSWER == false ]]; do
	echo " Do you want to Backup your current KES KEYS and NODE CERT files ?"
	echo " (this will replace any previous backups kes.skey.bak, kes.vkey.bak and node.cert.bak)"
	read -p " (YES/NO) : " ANSWER
	ANSWER_LOWER=$(echo "$ANSWER" | tr '[:upper:]' '[:lower:]')
    	if [[ "$ANSWER_LOWER" == "yes" ]]; then
    		echo
    		rm -f kes.skey.bak
    		rm -f kes.vkey.bak
    		rm -f node.cert.bak
    		cp kes.skey kes.skey.bak
		cp kes.vkey kes.vkey.bak
		cp node.cert node.cert.bak

		if [ -f "kes.skey.bak" ]; then
			echo -e " [\e[1;32mOK\e[0m] BACKUP done : kes.skey.bak created"
		else
			echo -e " \e[1;31mCouldn't backup kes.skey. Please check the file and directory\e[0m"
		fi
		if [ -f "kes.vkey.bak" ]; then
			echo -e " [\e[1;32mOK\e[0m] BACKUP done : kes.vkey.bak created"
		else
			echo -e " \e[1;31mCouldn't backup kes.vkey. Please check the file and directory\e[0m"
		fi
		if [ -f "node.cert.bak" ]; then
        		echo -e " [\e[1;32mOK\e[0m] BACKUP done : node.cert.bak created"
		else
			echo -e " \e[1;31mCouldn't backup node.cert. Please check the file and directory\e[0m"
		fi
        	VALID_ANSWER=true
    	elif [[ "$ANSWER_LOWER" == "no" ]]; then
        	echo -e " \e[1;33mNO BACKUP DONE FOR KES KEYS AND NODE CERT\e[0m"
        	VALID_ANSWER=true
    	else
        	echo -e " \e[1;31mInvalid answer. Please enter YES or NO\e[0m"
    	fi
done
echo

# KES PAIR GENERATE
echo
echo "---------------------------------------------------------------------"
echo " KES KEYS GENERATE"
echo "---------------------------------------------------------------------"
echo
sleep 1

VALID_ANSWER=false
while [[ $VALID_ANSWER == false ]]; do
	echo " Do you want to create a new KES KEYS pair ?"
	echo " (this will remove current kes.skey and kes.vkey files, generate new ones, and chmod 400 them)"
	read -p " (YES/NO) : " ANSWER
	ANSWER_LOWER=$(echo "$ANSWER" | tr '[:upper:]' '[:lower:]')
    	if [[ "$ANSWER_LOWER" == "yes" ]]; then
    		echo

    		mv kes.skey kes.skey.old
		mv kes.vkey kes.vkey.old

		cardano-cli node key-gen-KES --verification-key-file kes.vkey --signing-key-file kes.skey

		if [ -f "kes.skey" ]; then
			chmod 400 kes.skey
			echo -e " [\e[1;32mOK\e[0m] GENERATE new kes.skey : done"
			rm -f kes.skey.old
		else
        		echo -e " \e[1;31mCouldn't generate kes.skey\e[0m"
        		mv kes.skey.old kes.skey
		fi
		if [ -f "kes.vkey" ]; then
			chmod 400 kes.vkey
        		echo -e " [\e[1;32mOK\e[0m] GENERATE new kes.vkey : done"
        		rm -f kes.vkey.old
		else
			echo -e " \e[1;31mCouldn't generate kes.vkey\e[0m"
			mv kes.vkey.old kes.vkey
		fi
		VALID_ANSWER=true
	elif [[ "$ANSWER_LOWER" == "no" ]]; then
        	echo -e " \e[1;31mNO NEW KES KEYS CREATED\e[0m"
        	echo " ... exiting script"
        	sleep 1
        	exit 0;
        	VALID_ANSWER=true
	else
        	echo -e " \e[1;31mInvalid answer. Please enter YES or NO\e[0m"
    	fi
done
echo

# STARTING KES PERIOD CALCULATION
echo
echo "---------------------------------------------------------------------"
echo " STARTING KES PERIOD CALCULATION"
echo "---------------------------------------------------------------------"
echo
sleep 2

slotNo=$(cardano-cli query tip --mainnet | jq -r '.slot')
slotsPerKESPeriod=$(cat $NODE_HOME/shelley-genesis.json | jq -r '.slotsPerKESPeriod')
kesPeriod=$((${slotNo} / ${slotsPerKESPeriod}))
StartingKESPeriod=${kesPeriod}

echo " The starting KES period is : " ${StartingKESPeriod}
echo
echo " This is the period that must be used when you generate the new OP Certificate on your air-gapped machine"
echo

echo
echo "---------------------------------------------------------------------"
echo " NEXT-STEPS "
echo "---------------------------------------------------------------------"
echo
sleep 1
echo " 1- Copy your new kes.skey and kes.vkey to your cardano home directory on your AIR-GAPPED MACHINE"
echo " 2- Double check your node.counter on your air-gapped machine and adjust it if necessary (see the Reminder above)"
echo -e " 3- Generate your new OP certificate ON YOUR AIR-GAPPED MACHINE with your new kes.vkey: "
echo
echo -e "\e[0;37mcd \$NODE_HOME"
echo -e "cardano-cli node issue-op-cert \ "
echo -e "   --kes-verification-key-file kes.vkey \ "
echo -e "   --cold-signing-key-file \$HOME/cold-keys/node.skey \ "
echo -e "   --operational-certificate-issue-counter \$HOME/cold-keys/node.counter \ "
echo -e "   --kes-period ${StartingKESPeriod} \ "
echo -e "   --out-file node.cert\e[0m"
echo
echo " 4- Copy your new node.cert to your cardano home directory on your Block Producer and chmod 400 it"
echo " 5- Restart your block producer"
echo " 6- Check if your new OP certificate is OK :"
echo
echo -e "\e[0;37mcardano-cli query kes-period-info --mainnet --op-cert-file \$NODE_HOME/node.cert\e[0m"
echo
echo " 7- Backup your new KES keys and node.cert files on a secured cold storage"
echo
exit 0;

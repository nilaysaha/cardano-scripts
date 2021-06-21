#!/usr/bin/env python3

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import os
import process_certs as pc
import logging
import colorama
import time
from colorama import Fore, Back, Style

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
colorama.init(autoreset=True)


os.environ["CHAIN"] = "testnet"
os.environ["MAGIC"] = "1097911063"
TINTERVAL=10 #in seconds

MAX_WAITING_TIME=360 #in seconds. A single transaction should not last longer that this.

class PayOrMint:
    def __init__(self, amount):
        self.amount = amount
        self.totalTimeSpent = 0
        
    def check_ADA_amount(self,address):
        """
        we need to gather all utxo amount and then compare based on time. What can be done is to use redis for this purpose.
        So when the payment address is created we check the amount present. And then at regular interval check the increment
        based on base value. If we see amount minted has arrived.
        """
        try:
            if (self.totalTimeSpent < MAX_WAITING_TIME):
                print(Fore.GREEN + f"Checking whether amount {self.amount} ADA has arrived at {address}")
                funds = pc.get_total_fund_in_utx0_with_native_tokens(address)
                if funds['lovelace'] > int(self.amount):
                    return True
                else:
                    time.sleep(TINTERVAL)
                    self.totalTimeSpent += TINTERVAL                
                    self.check_ADA_amount(address)
            else:
                print(f"Now quitting because max waiting time:{MAX_WAITING_TIME} has passed.")
                return False
        except:
            logging.exception("Could not check amount in the address")    

    def check_minted_tokens(self,policy_id,coin_name, address):
        try:
            if (self.totalTimeSpent < MAX_WAITING_TIME):
                print(Fore.GREEN + f"Checking whether amount {self.amount} for coin:{policy_id}.{coin_name} has arrived at {address}")
                native_coin_name=f"{policy_id}.{coin_name}"

                funds = pc.get_total_fund_in_utx0_with_native_tokens(address)
                
                if (native_coin_name in funds):
                    coins_minted = funds[native_coin_name]
                    coins_needed = int(self.amount)
                    print(Fore.GREEN + f"Comparing {coins_minted} with {coins_needed}")

                    print(f"type of coints minted: {type(coins_minted)}")
                    print(f"type of coints minted: {type(coins_needed)}")
                    
                    if coins_minted >= coins_needed:
                        print("NOW RETURNING TRUE AFTER MINTED TOKEN ARRIVAL")
                        return True
                else:
                    print(f"Sufficient coin has not yet arrived at the address. Keep on trying....")
                    time.sleep(TINTERVAL)
                    self.totalTimeSpent += TINTERVAL
                    self.check_minted_tokens(policy_id, coin_name, address)                        
            else:                
                print(f"Now quitting because max waiting time:{MAX_WAITING_TIME} has passed.")
                return False
        except:
            logging.exception("Could not check amount in the address")    
            sys.exit(1)

    

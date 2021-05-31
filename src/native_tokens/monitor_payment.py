#!/usr/bin/env python3

"""
This module is meant to monitor a session payment from the customer and then trigger the step 3: Minting of the tokens sign/commit + sending the token to the recv. address
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


import subprocess, json, shlex
import process_certs as pc
import create_nft_token as nft
import transfer_native_asset as tna
import transfer_ada as tada
import check_payment_arrival as cpa
import logging
import colorama
import time
from colorama import Fore, Back, Style

import daemon

HEARTBEAT_INTERVAL = 5 #waiting time in seconds
MINTING_WAITING_PERIOD=50 #waiting time in seconds
ADA2LOVELACE=1000000
TRANSACTION_COST=1000000 #in lovelace. Just keeping some margin. Normally under 1 ADA. 

os.environ["CHAIN"] = "testnet"
os.environ["MAGIC"] = "1097911063"


DEFAULT_TREASURY_ADDRESS="addr_test1vzezxpug0fuehlk4edj0chk4a7ehvkc704z7sr4mggc68uqccxdmq"

class Treasury:
    """
    This is meant to collect all the funds gained via the NFT minting. This for example can be a stake pool pay.addr so that 
    stake pools can later host this, and lead to decentralize the minting process. And later via smart contract we can detect this software and 
    direct decentralized minting.
    """
    def __init__(self, dest_address=DEFAULT_TREASURY_ADDRESS):
        self.dest_address = dest_address

    def transfer(self, amount, source_address, pay_skey_file, protocol_file):
        try:
            a = tada.Transfer(source_address, amount, self.dest_address)
            a.set_payment_and_protocol(pay_skey_file, protocol_file)
            a.main()
        except:
            logging.exception(f"Could not transfer {amount} to {source_address}")


class Monitor:
    def __init__(self, session_uuid):
        self.session = session_uuid
        self.s = nft.Session(session_uuid)
        inputs= self._fetch_buffer(session_uuid)

        print(f"Fetched input params are:{inputs}")
        
        self.dest_addr = inputs["dest_addr"]
        self.payment_amount = int(inputs["payment"])*ADA2LOVELACE
        self.initial_amount = 0 #ASSUMPITON: We start with a fresh payment address per person.
        self.payment_addr = pc.content(self.s.sdir(nft.FILES['payment']['address']))
        self.heartbeat_interval = HEARTBEAT_INTERVAL

    def _fetch_buffer(self,uuid):
        i =nft.Inputs(uuid)
        return i.fetch()

    def _check_if_minting_done(self):
        c = nft.CreateToken(self.session)
        return c.check_status('phase_3')
    
    def check_payment(self):
        """
        returns the funds in the pay.addr for that session uuid.
        """
        try:
            fund = pc.get_total_fund_in_utx0(self.payment_addr)
            print(f"fund in the payment address :{self.payment_addr} is {fund}")        
            status = int(fund) >= int(self.payment_amount)
            print(f"payment status is:{status}")
            return status
        except:
            logging.exception(f"Failed to check payments")
            sys.exit(1)
   

    def check_minted_tokens(self, amount, policy_id, coin_name):
        try:
            funds = pc.get_total_fund_in_utx0_with_native_tokens(self.payment_addr)
            print(f"fund in the payment address :{self.payment_addr} is {funds}")
            native_coin_name=f"{policy_id}.{coin_name}"
            
            if (native_coin_name in funds):
                status = funds[native_coin_name] >= int(amount)
                print(f"payment status is:{status}")
                return status
        except:
            logging.exception(f"Failed to check minted tokens")
            sys.exit(1)


    def check_minted_tokens_transferred(self, policy_id, coin_name):
        """
        we want to check if all the minted coins are transferred out of the minted address
        """
        try:
            funds = pc.get_total_fund_in_utx0_with_native_tokens(self.payment_addr)
            print(f"fund in the payment address :{self.payment_addr} is {funds}")
            native_coin_name=f"{policy_id}.{coin_name}"
            
            if (native_coin_name not in funds):
                return True
            else:
                return False
        except:
            logging.exception(f"Failed to check minted tokens")
            sys.exit(1)
        
                        
    def heartbeat_check_payment(self):
        """
        check the balance every 200ms
        """
        #Check is step_3 has been run. If yes, then payment_status=true
        if self._check_if_minting_done():
            payment_status = True
        else:
            payment_status = False
            
        while not payment_status:            
            payment_status = self.check_payment()
            print(f"Next loop...Continue till the payment of {self.payment_amount} has arrived at {self.payment_addr}")
            time.sleep(HEARTBEAT_INTERVAL)
        print(f"Payment has been recieved. Now proceeding with post payment steps.")
        return True


    def heartbeat_minting(self,amount,policy,name):
        """
        check whether minting is complete and NFT tokens are available at pay.addr
        """
        mint_status = False
        while not mint_status:            
            mint_status = self.check_minted_tokens(amount, policy, name)
            print(f"Next loop...Continue till the minting at {self.payment_addr} of {policy}.{name} ")
            time.sleep(HEARTBEAT_INTERVAL)
        print(f"Minted tokens has arrived. Now proceeding with next  steps.")
        return True


    def heartbeat_minting_transfer(self, policy, name):
        """
        check whether transfer of the NFT minted tokens are complete so that rest of ADA can be transferred
        """
        transfer_status = False
        while not transfer_status:            
            transfer_status = self.check_minted_tokens_transferred(policy, name)
            print(f"Next loop...Continue till the minted coins {policy}.{name} are transferred out of {self.payment_addr}")
            time.sleep(HEARTBEAT_INTERVAL)
        print(f"Minted tokens have been transferred to owner. Now proceeding with next steps.")
        return True
        

    def mint_tokens_init(self):
        try:
            #Step 1: Check if the minted tokens have arrived at payment addr.
            self.heartbeat_check_payment()
            
            #Step 2: Mint tokens since payment has come            
            inputs = self._fetch_buffer(self.session)
            print(f"fetched the inputs for this run:{inputs}")
            
            t = nft.Transaction(self.session, inputs["name"], inputs["amount"], inputs["metadata"])
            policy_id = t.mint_new_asset() #generates the policyid
            nft.main_phase_B(self.session) #uses the policyid for minting 

            return policy_id
        except:
            logging.exception("could not transfer minted tokens even after they have arrived at payment address")
            sys.exit(1)

        
    def transfer_minted_tokens(self, amount, policy, name, addr):
        try:
            #Step 1: Check if the minted tokens have arrived at payment addr.
            self.heartbeat_minting(amount, policy, name)
            
            #Step 2: Transfer of minted tokens to target address.
            a = tna.Transfer(self.session, amount, policy, name, addr)
            a.main()
        except:
            logging.exception("could not transfer minted tokens even after they have arrived at payment address")
            sys.exit(1)
                

    def transfer_NFT_ADA_reward(self, policy, name):
        """
        We transfer the entire amount present in the address to the treasury address after NFT tokens are transferred out.
        """
        try:

            #first check if the last step of transferring minted coins is complete (as it impacts the amount of ADA present)
            self.heartbeat_minting_transfer(policy, name)

            #Then execute this.
            source_address = pc.content(self.s.sdir(nft.FILES['payment']['address']))
            amount_to_transfer = pc.get_total_fund_in_utx0(source_address) - 3*TRANSACTION_COST
            pay_skey_file = self.s.sdir(nft.FILES['payment']['signature'])
            protocol_file = self.s.sdir(nft.FILES['protocol'])
            
            t1 = Treasury()
            t1.transfer(amount_to_transfer, source_address, pay_skey_file, protocol_file)
        except:
            logging.exception("Could not transfer rewards NFT")


    def _print_divider(self, step_name, state):
        print(Fore.GREEN + f"****=================================================={step_name}:{state}=================================================================****\n")


    def publish_status_of_transaction(self, uuid, stage, status):
        """
        From here we publish the status of the transaction to the SQS.
        """
        
        
    def exec_steps(self):
        """
        Now we trigger minting and transfer of the minted tokens.
        step 1: mint the tokens
          Sample command: python3 --fetchInputs --uuid <uuid>
        step 2: transfer the tokens
          Sample command: python3 transfer_native_asset.py --uuid be3f7e33-7147-4dad-9658-158e88819a9e --amount 1 \
                                  --policyid ad9f33675c1bfa3db8a1e3ed943a8e3ce1b077a00fbd9cbe26bf9e15 --coinname a0c3aa67533d405d92e262ece8ed4344 \
                                  --outputAddr addr_test1vzlzqgcvehq56yd3aya69cyz8wsdu3deju8fsw2jwd0rrvgpwkw6x
        """
        try:
            inputs = self._fetch_buffer(self.session)
            
            #Step 1: Mint Tokens after receiving payment        
            policy_id = self.mint_tokens_init()
            self._print_divider("Token Minting", "Initiated")
                        
            #Step 2: Now transfer the minted tokens
            self.transfer_minted_tokens(inputs["amount"], policy_id, inputs["name"], inputs["dest_addr"])
            self._print_divider("Transfer Minted tokens", "Initiated")

            #Step 3: Now transfer the ADA to the treasury.
            self.transfer_NFT_ADA_reward(policy_id, inputs["name"])
            self._print_divider("Transfer ADA FEES to treasury", "Initiated")            
        except:
            logging.exception("Could not complete all the post payment steps")
            
            
    def main(self):
        try:
            self.exec_steps()
            self._print_divider("All steps have been completed", "Continue to scan ...")
        except:
            logging.exception(f"Could not complete all the monitoring steps")
            sys.exit(1)


def main_task(uuid):
    try:
        t = Monitor(uuid)
        t.main()
    except:
        logging.exception(f"Failed to execute task with uuid:{uuid}")            
        sys.exit(1)
                
            
                
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--run', dest='run', action="store_true", help="Start monitoring the queue and take action if needed")
    parser.add_argument('--uuid', dest='uuid', help="This customer uuid being assigned")
    args = parser.parse_args()

    if args.uuid != None:
        main_task(args.uuid)
    elif args.run:
        print("Ok. Now you want to start the daemon mode. Let's go for it.")
        # a = daemon.Daemon()
        # a.schedule()

        #Now we are shifting to use Python RQ wrapper to queue/exec jobs
        a = daemon.Daemon_RQ()
        

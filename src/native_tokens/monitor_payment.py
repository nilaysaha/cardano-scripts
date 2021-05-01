#!/usr/bin/env python3

"""
This module is meant to monitor a session payment from the customer and then trigger the step 3: Minting of the tokens sign/commit + sending the token to the recv. address
"""

import subprocess, json, os, sys, shlex
import process_certs as pc
import create_nft_token as nft
import transfer_native_asset as ta
import logging
import colorama
import time
from colorama import Fore, Back, Style

HEARTBEAT_INTERVAL = 10
ADA2LOVELACE=1000000

os.environ["CHAIN"] = "testnet"
os.environ["MAGIC"] = "1097911063"

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

        
    def heartbeat(self):
        """
        check the balance every 200ms
        """
        payment_status = False
        while not payment_status:            
            payment_status = self.check_payment()
            print(f"Next loop...Continue till the payment of {self.payment_amount} has arrived at {self.payment_addr}")
            time.sleep(HEARTBEAT_INTERVAL)
        print(f"Payment has been recieved. Now proceeding with post payment steps.")
        return True
        
    def check_payment(self):
        """
        returns the funds in the pay.addr for that session uuid.
        """
        fund = pc.get_total_fund_in_utx0(self.payment_addr)
        print(f"fund in the payment address :{self.payment_addr} is {fund}")        
        status = int(fund) >= int(self.payment_amount)
        print(f"payment status is:{status}")
        return status

    def post_payment_steps(self):
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
            #Fetch the run parameters and store back the recv address of the customer
            a = nft.Inputs(self.session)
            inputs = a.fetch()
            print(f"fetched the inputs for this run:{inputs}")
            
            t = nft.Transaction(self.session, inputs["name"], inputs["amount"], inputs["metadata"])
            policy_id = t.mint_new_asset()

            #Step 1: Minting of the tokens
            nft.main_phase_B(self.session)

            #Step 2: Transfer of minted tokens to target address            
            a = ta.Transfer(uuid=self.session, amount=inputs["amount"], policyid=policy_id, coin_name=inputs["name"], output_addr=inputs["dest_addr"])
            a.main()            
        except:
            logging.exception("Could not complete all the post payment steps")
            

def main(uuid):
    a = Monitor(uuid)
    a.heartbeat()
    a.post_payment_steps()



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--uuid', dest='uuid', help="This customer uuid being assigned")

    args = parser.parse_args()

    if args.uuid != None:
        main(args.uuid)
    else:
        print(f"Missed minimum input params. For help: python3 monitory_payment.py --help")

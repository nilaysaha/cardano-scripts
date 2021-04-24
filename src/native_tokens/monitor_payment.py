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
from colorama import Fore, Back, Style


HEARTBEAT_INTERVAL = 200


class Monitor:
    def __init__(self, session_uuid, payment_due, transfer_address):
        self.session = session_uuid
        self.dest_addr = transfer_address
        self.payment_amount = payment_due
        self.initial_amount = self.check_payment() #needs to be verified by a separate function before we start heartbeat.
        self.s = nft.Session(False, session_uuid)
        self.heartbeat_interval = HEARTBEAT_INTERVAL
        
    def heartbeat(self):
        """
        check the balance every 200ms
        """
        while not check_payment():            
            sleep(HEARTBEAT_INTERVAL)
        print(f"Payment has been recieved.")
            
    def check_payment(self):
        """
        returns the funds in the pay.addr for that session uuid.
        """
        payment_addr = pc.content(self.s.sdir(nft.FILES['payment']['address']))
        rfund = pc.get_total_fund_in_utx0(payment_addr)
        status = (rfund - self.initial_amount)>= self.payment_amount
        return status

    def _post_payment_steps(self):
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
            inputs = nft.fetch_inputs(self.session)
            token_metadata = nft.TokenMetadata()
            m = token_metadata.fetch() #This will only work when the payment is done and minting is done.
            if m["721"] != None:
                t = m["721"]
                policy_keys = m['721'].keys()
                for p in policy_keys:
                    
                    a = ta.Transfer(uuid=inputs.uuid, amount=inputs.num_coins, coinname=inputs.coinName, policyid=p, outputAddr=self.dest_addr)
                    a.main()
        except:
            logging.exception("Could not complete all the post payment steps")
            

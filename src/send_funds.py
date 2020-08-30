#!/usr/bin/env python3                                                                                                                                                                                      

import subprocess, json, sys
import process_certs as pc

"""
Creating a transaction is a process that requires various steps:

1. Get the protocol parameters
2. Define the time-to-live (TTL) for the transaction
3. Calculate the fee
4. Build the transaction
5. Sign the transaction
6. Submit the transaction
"""

def get_payment_utx0(t_address):
    """
    should be able to add all the utx0 to the address.
    """
    try:
        final_array = []
                
        command=[CARDANO_CLI, 'shelley' , 'query', 'utxo', '--address', t_address, '--mainnet']
        s = subprocess.check_output(command)
        split_str=s.decode('UTF-8').split("\n")
        result = filter(lambda x: x != '', split_str) 
        farray = list(result)[2:]
        print(farray)        
        for val in farray:
            print(val)
            (txHash, txtx, lovelace) = val.split()
            final_array.append((txHash, txtx, lovelace))
        return final_array
    except:
        print("Oops!", sys.exc_info()[0], "occurred in get payment utx0")


def get_total_fund_in_utx0(t_address):
    t = get_payment_utx0(t_address)
    total_fund = 0
    for val in t:
        total_fund += int(val[2])
    return total_fund

        

class Transfer:
    def __init__(self, from_address, to_address, transfer_amount):
        self.from_address = from_address
        self.to_address = to_address
        self.transfer_amount = transfer_amount 
        self.ttl = None

    
    def _step_1(self):
        """                                                                                                                                                                                                 
        fetch the protocol file from the chain                                                                                                                                                              
        """
        pc.create_protocol()


    def _step_2(self):    
        """
        get the TTL for the transaction
        """
        self.ttl = pc.get_ttl()

        
    def _step_2(self):
        """                                                                                                                                                                                                 
        Build transaction
        """
        tx_array_from_address = get_payment_utx0(self.from_address)
        print(f'collection of utx0 is:{tx_array_from_address}')

        min_fee = calculate_min_fees(tx_array_from_address, self.ttl)
        print(f"minimum fees: {min_fee}")

        remaining_funds = get_total_fund_in_utx0(self.from_address) - min_fee - self.transfer_amount

        

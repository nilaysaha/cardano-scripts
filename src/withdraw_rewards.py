#!/usr/bin/env python3                                                                                                                                                                                      

import subprocess, json, sys
import process_certs as pc
import argparse


"""
Follow the following tutorial:https://cardano-foundation.gitbook.io/stake-pool-course/stake-pool-guide/stake-pool/withdraw-rewards

Creating a transaction is a process that requires various steps:

1. Get the protocol parameters
2. Define the time-to-live (TTL) for the transaction
3. Calculate the fee
4. Build the transaction
5. Sign the transaction
6. Submit the transaction
"""

FILES={
    'stake': './kaddr/stake.addr',
    'payment': {'verify_key': './kaddr/payment.vkey', 'addr': './kaddr/payment.addr', 'sign_key': './kaddr/payment.skey'},
    'transaction': {'draft':'./kaddr_tx/tx_extra.draft','raw': './kaddr_tx/tx_extra.raw', 'signed':'./kaddr_tx/tx_extra.signed'}
}


class CalcFee:
    def __init__(self):
        pass

    def check_balance_stake(self):
        """
        cardano-cli query stake-address-info \
        --mainnet \
        --mary-era \
        --address $(cat stake.addr)
        """
        try:
            stake_addr = pc.content(FILES['stake'])
            command = ["cardano-cli", "query", "stake-address-info", "--mainnet", "--mary-era", "--address", stake_addr]
            s = subprocess.check_output(command)
            print(f"output for command:{command} is {s}")
        except:
            print("Oops!", sys.exc_info(), "occurred in draft transaction")
            
    def create_tx_in(self,tx_in):
        print(f"Inside _create_tx_in")
        tx_in_array = []
        for val in tx_in:
            print(f"inside build_transaction: val:{val}")
            tx_in  = val[0]+"#"+val[1]
            print(f"tx_in:{tx_in}")
            tx_in_array.append('--tx-in')
            tx_in_array.append(tx_in)
            
        print(f"tx_in_array:{tx_in_array}")
        return tx_in_array

    
    def draft_transaction(self, tx_in, tx_out, withdrawl_amount):
        """
        cardano-cli shelley transaction build raw \
        --tx-in a82f8d2a85cde39118a894306ad7a85ba40af221406064a56bdd9b3c61153527#1
        --tx-out $(cat payment.addr)+0
        --withdrawal $(cat stake.addr)+550000000
        --ttl 0
        --fee 0
        --out-file withdraw_rewards.raw
        """
        try:
            ttl = pc.get_ttl()
            print(f"Inside draft transaction")
            stake_addr = pc.content(FILES['stake'])
            tx_in_array= self.create_tx_in(tx_in)
            command = ["cardano-cli",  "transaction", "build-raw",
                       "--tx-out",tx_out,  "--ttl", ttl,  "--fee", '0',
                       "--withdrawl", stake_addr+"+"+withdrawl_amount,
                       '--out-file', FILES['transaction']['draft'] ] + tx_in_array
            print(command)
            s = subprocess.check_output(command)
            print(s)
        except:
            print("Oops!", sys.exc_info(), "occurred in draft transaction")
        

    def calculate_min_fees(self, tx_in, ttl, withdrawl_amount):
        """
        cardano-cli transaction calculate-min-fee \
        --tx-body-file withdraw_rewards.draft  \
        --tx-in-count 1 \
        --tx-out-count 1 \
        --witness-count 2 \
        --byron-witness-count 0 \
        --mainnet \
        --protocol-params-file protocol.json
        """
        
        try:
            fname =  FILES['transaction']['draft']            
            self.draft_transaction(tx_in, tx_out, withdrawal_amount)            
            
            tx_in_count = len(tx_in)
            tx_out = f"{content(FILES['payment']['addr'])}+{0}"            
            witness_count = 2
            byron_wc = 0
            
            command = [CARDANO_CLI, 'transaction', 'calculate-min-fee',
                       "--tx-body-file", fname,
                       "--witness-count", f"{witness_count}",
                       '--tx-in-count',  str(tx_in_count),
                       '--tx-out-count', str(1) ,
                       '--byron-witness-count', str(byron_wc) ,
                       '--mainnet',
                       '--protocol-params-file', FILES['configs']['protocol'] ]
            s = subprocess.check_output(command,stderr=True, universal_newlines=True)
            print(f"output of command:{command} output is:{s}")
            min_fee = s.split(" ")[0]
            return min_fee
        except:
            print("Oops!", sys.exc_info()[0], "occurred in calculate min fees")

    def calc_remaining_funds(self, ttl, from_address=None, transfer_amount=None):
        try:
            if from_address == None:
                from_address = pc.content(FILES['payment']['addr'])
                
            tx_array_from_address = pc.get_payment_utx0(from_address)
            min_fee = self.calculate_min_fees(tx_array_from_address, ttl, transfer_amount)
            print(f"minimum fees: {min_fee}")
            
            #remaining funds needs to be transferred to the owner (from_address)
            remaining_funds = pc.get_total_fund_in_utx0(from_address) - min_fee - transfer_amount
            return remaining_fund
        except:
            print("Oops!", sys.exc_info()[0], "occurred in calculate min fees")


class Transaction:
    def __init__(self):
        pass
    
    def build(self, txArray, remaining_fund, ttl, min_fee, withdrawal_amount):
        """
        reconstruct: 
        cardano-cli transaction build-raw \
        --tx-in a82f8d2a85cde39118a894306ad7a85ba40af221406064a56bdd9b3c61153527#1 \
        --tx-out $(cat payment.addr)+743882981 \
        --withdrawal $(cat stake.addr)+550000000 \
        --invalid-hereafter 12345678 \
        --fee 171089 \
        --out-file withdraw_rewards.raw
        """
        try:
            tx_in_array = []
            for val in txArray:
                print(f"inside build_transaction: val:{val}")
                tx_in  = val[0]+"#"+val[1]
                print(f"tx_in:{tx_in}")
                tx_in_array.append('--tx-in')
                tx_in_array.append(tx_in)
            payment_addr = content(FILES['payment']['addr'])
            stake_addr   = content(FILES['stake'])
            tx_out = "{paddr}+{rfund}".format(paddr=payment_addr, rfund=remaining_fund)
            command = [CARDANO_CLI,  "transaction", "build-raw", "--mary-era",
                       "--tx-out",tx_out,
                       "--withdrawal", stake_addr+"+"+withdrawal_amount,
                       "--fee", min_fee,
                       "--out-file", FILES['transaction']['raw']]+tx_in_array
            s = subprocess.check_output(command)
            split_str=s.decode('UTF-8').split(" ")
            print(f"out of command:{command} is {s}")
        except:
            print("Oops!", sys.exc_info()[0], "occurred in build transaction")

    def sign(self):
        """
        cardano-cli transaction sign \
        --tx-body-file tx.raw \
        --signing-key-file payment.skey \
        --signing-key-file stake.skey \
        --mainnet \
        --out-file tx.signed
        """
        try:
            command = [CARDANO_CLI, "transaction", "sign", "--tx-body-file", FILES['transaction']['raw'],
                       '--signing-key-file', FILES['payment']['sign_key'],
                       '--signing-key-file', FILES['stake']['sign_key'],
                       '--mainnet',
                       '--out-file',FILES['transaction']['signed']]
            s = subprocess.check_output(command)
            print(f"output of command:{command} is {s}")
        except:
            print("Oops!", sys.exc_info()[0], "occurred in sign transaction")


    def submit(self):
        """
        reconstruct:
        cardano-cli transaction submit \
        --tx-file tx.signed \
        --mainnet
        """
        try:
            command = [CARDANO_CLI, "transaction", "submit", "--tx-file", FILES['transaction']['signed'], '--mainnet']
            s = subprocess.check_output(command)
            print("Submitted transaction for stake registration on chain usin: {command}. Result is: {s}")
        except:
            print("Oops!", sys.exc_info()[0], "occurred in submit transaction")

        
class Transfer:
    def __init__(self, payment_address, transfer_amount):
        self.payment_address = payment_address
        self.transfer_amount = transfer_amount 
        self.ttl = None
    
    def _step_1(self):
        """                                                                                                                                                                                                 
        pre-requisites for transactions. Check if the funding requirements are satisfied
        """
        try:
            pc.create_protocol()
            ttl = pc.get_ttl()
        except:
            print("Oops!", sys.exc_info()[0], "occurred in pre-req transaction for send funds. Step 1 for ref.")

    def _step_2(self):
        """                                                                                                                                                                                                 
        Build transaction
        """
        try:
            c = CalcFee()
            remaining_fund = c.calc_remaining_funds(self.ttl, self.payment_address, self.transfer_amount)
            return remaining_fund
        except:
            print("Oops!", sys.exc_info()[0], "occurred in build/sign/exec transaction for send funds. Step 2 for ref.")

    def _step_3(self):        
        t = Transaction()
        t.build()
        t.sign()
        t.submit()
        

    def main():
        try:
            self._step_1()
            rfund = self._step_2()
            if (rfund > 0):
                print(f"Enough funds {rfund} present hence preparing for transfer")
                self._step_3()
        except:
            print("Oops!", sys.exc_info()[0], "overall function to coordinate transfer")
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--pay_address', dest="target",help='Payment address')
    parser.add_argument('--amount', dest="amount",help='Amount in ADA to be transferred')
    args = parser.parse_args()

    if (args.pay_address == None) or (args.amount == None):
        print("Either the pay_address/amount(ADA) is empty. Please put correct values")
    else:
        print(f"Trying to transfer funds {args.amount} to {args.pay_address}")
        t = Transfer(args.pay_address, args.amount)
        t.main()
            

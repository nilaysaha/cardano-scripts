#!/usr/bin/env python3                                                                                                                                                                                      

import subprocess, json, sys, json
import process_certs as pc
import argparse
import logging
import colorama
from colorama import Fore, Back, Style

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
colorama.init(autoreset=True)


"""
Follow the following tutorial:https://cardano-foundation.gitbook.io/stake-pool-course/stake-pool-guide/stake-pool/withdraw-rewards

Creating a transaction is a process that requires various steps:

1. Get the protocol parameters
2. Calculate the fee
3. Build the transaction
4. Sign the transaction
5. Submit the transaction
"""

FILES={
    'configs': {'protocol': './kaddr/protocol.json'},
    'stake': {'addr': './kaddr/stake.addr', 'sign_key':'./kaddr/stake.skey'},
    'payment': {'addr': './kaddr/payment.addr', 'sign_key': './kaddr/payment.skey'},
    'transaction': {'draft':'./kaddr_tx/withdraw_rewards.draft','raw': './kaddr_tx/withdraw_rewards.raw', 'signed':'./kaddr_tx/withdraw_rewards.signed'}
}

TIP_INCREMENT=10000


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
            stake_addr = pc.content(FILES['stake']['addr'])
            command = ["cardano-cli", "query", "stake-address-info", "--mainnet", "--mary-era", "--address", stake_addr]
            s = subprocess.check_output(command)
            print(Fore.RED + f"output for command:{command} is {s}")
            s_package = json.loads(s)
            return s_package[0]["rewardAccountBalance"]
        except:
            logging.exception("Could not check balance of staking address")
            
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

    
    def draft_transaction(self, tx_in, tx_out):
        """
        cardano-cli transaction build-raw \
        --tx-in a82f8d2a85cde39118a894306ad7a85ba40af221406064a56bdd9b3c61153527#1 \
        --tx-out $(cat payment.addr)+0 \
        --withdrawal $(cat stake.addr)+0 \
        --invalid-hereafter 0 \
        --fee 0 \
        --out-file withdraw_rewards.draft
        """
        try:
            print(f"Inside draft transaction")
            stake_addr = pc.content(FILES['stake']['addr'])
            tx_in_array= self.create_tx_in(tx_in)
            command = ["cardano-cli",  "transaction", "build-raw", "--mary-era",
                       "--tx-out",tx_out,
                       "--withdrawal", stake_addr+"+"+'0',
                       "--invalid-hereafter", '0',
                       "--fee", '0',
                       '--out-file', FILES['transaction']['draft'] ] + tx_in_array        
            s = subprocess.check_output(command)
            print(Fore.RED + f"\noutput of command:{command} is:{s}\n\n")
        except:
            logging.exception("Could not draft transactions")
        

    def calculate_min_fees(self, tx_in, withdrawl_amount):
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
        
        print(f"Input to calculate min fees:{tx_in} {withdrawl_amount}")
        try:

            fname =  FILES['transaction']['draft']            
            tx_in_count = len(tx_in)
            tx_out = pc.content(FILES['payment']['addr'])+"+"+"0"            
            witness_count = 2
            byron_wc = 0

            #This is a prerequisite to calculation of min-fee
            self.draft_transaction(tx_in, tx_out)            

            command = ['cardano-cli', 'transaction', 'calculate-min-fee',
                       "--tx-body-file", fname,
                       '--tx-in-count',  str(tx_in_count),
                       '--tx-out-count', str(1) ,
                       "--witness-count", f"{witness_count}",
                       '--byron-witness-count', str(byron_wc) ,
                       '--mainnet',
                       '--protocol-params-file', FILES['configs']['protocol'] ]
            s = subprocess.check_output(command,stderr=True, universal_newlines=True)
            print(Fore.RED + f"\nOutput of command:{command} output is:{s}\n\n")
            min_fee = float(s.split(" ")[0])
            return min_fee
        except:
            logging.exception("Could not calculate minimum fees")


            
    def calc_remaining_funds(self, from_address=None, transfer_amount=None):
        try:
            if from_address == None:
                from_address = pc.content(FILES['payment']['addr'])
                
            tx_array_from_address = pc.get_payment_utx0(from_address)
            min_fee = self.calculate_min_fees(tx_array_from_address, transfer_amount)
            print(f"minimum fees: {min_fee}")
            
            #remaining funds needs to be transferred to the owner (from_address)
            remaining_funds = int(pc.get_total_fund_in_utx0(from_address)) - min_fee +transfer_amount
            print(f"calculated remaining funds is:{remaining_funds}")
            return remaining_funds, min_fee
        except:
            logging.exception("Could not calculate remaining funds")



class Transaction:
    def __init__(self):
        pass
    
    def build(self, txArray, remaining_fund, min_fee, withdrawal_amount):
        """
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
            payment_addr = pc.content(FILES['payment']['addr'])
            stake_addr   = pc.content(FILES['stake']['addr'])
            future_tip = int(pc.get_tip())+TIP_INCREMENT
            
            tx_out = "{paddr}+{rfund}".format(paddr=payment_addr, rfund=remaining_fund)
            command = ['cardano-cli',  "transaction", "build-raw", "--mary-era",                       
                       "--tx-out",tx_out,
                       "--withdrawal", stake_addr+"+"+str(withdrawal_amount),
                       "--invalid-hereafter", str(future_tip),
                       "--fee", str(min_fee),
                       "--out-file", FILES['transaction']['raw']]+tx_in_array

            s = subprocess.check_output(command)
            split_str=s.decode('UTF-8').split(" ")
            print(Fore.RED + f"\nOutput of command:{command} is {s}\n")
        except:
            logging.exception("Could not build transaction")


    def sign(self):
        """
        cardano-cli transaction sign \
        --tx-body-file withdraw_rewards.raw  \
        --signing-key-file payment.skey \
        --signing-key-file stake.skey \
        --mainnet \
        --out-file withdraw_rewards.signed
        """
        try:
            command = ['cardano-cli', "transaction", "sign", "--tx-body-file", FILES['transaction']['raw'],
                       '--signing-key-file', FILES['payment']['sign_key'],
                       '--signing-key-file', FILES['stake']['sign_key'],
                       '--mainnet',
                       '--out-file',FILES['transaction']['signed']]
            s = subprocess.check_output(command)
            print(Fore.RED + f"\nOutput of command:{command} is {s}\n\n")
        except:
            logging.exception("Cold not sign transaction")


    def submit(self):
        """
        reconstruct:
        cardano-cli transaction submit \
        --tx-file tx.signed \
        --mainnet
        """
        try:
            command = ['cardano-cli', "transaction", "submit",
                       "--tx-file", FILES['transaction']['signed'],
                       '--mainnet']
            s = subprocess.check_output(command)
            print(Fore.RED + F"\nSubmitted transaction on chain using: {command}. Result is: {s}\n\n")
        except:
            logging.exception("Could not submit transaction")

        
class Transfer:
    def __init__(self, payment_address, transfer_amount):
        self.payment_address = payment_address
        self.transfer_amount = transfer_amount
        self.tx_in_array = []
        self.remaining_fund = None
        self.min_fees = None
    
    def _step_1(self):
        """                                                                                                                                                                                                 
        pre-requisites for transactions. Check if the funding requirements are satisfied
        """
        try:
            pc.create_protocol()
            self.tx_in_array = pc.get_payment_utx0(self.payment_address)
        except:
            logging.exception("Could not execute step 1 for funds transfer")

    def _step_2(self):
        """                                                                                                                                                                                                 
        Build transaction
        """
        try:
            c = CalcFee()
            self.remaining_fund, self.min_fees = c.calc_remaining_funds(self.payment_address, self.transfer_amount)
            return self.remaining_fund
        except:
            logging.exception("Could not execute step 2 for funds transfer")


    def _step_3(self):        
        t = Transaction()
        t.build(self.tx_in_array, int(self.remaining_fund), int(self.min_fees), int(self.transfer_amount))
        t.sign()
        t.submit()
        

    def main(self):
        try:
            self._step_1()
            rfund = self._step_2()
            if (rfund > 0):
                print(f"Enough funds {rfund} present hence preparing for transfer")
                self._step_3()
        except:
            logging.exception("Overall transfer error in function main of Transfer")


def get_user_input(args):
    print("Either the pay_address/amount(ADA) is empty. Will try to guide you. OK?")

    p = input("We are going to use the default payment.addr. Is that ok (Y/N) ? ")

    if p == "Y" or p == "y":
        args.target = pc.content(FILES['payment']['addr'])
    else:
        c = ("Would you like to continue? Y/N")
        if c == "Y" or c == "y":
            get_user_input()
        else:
            sys.exit("Quitting!")

    a = CalcFee()
    args.amount = a.check_balance_stake()
    print(Fore.BLUE + f"\nWe are going to withdraw amount {args.amount} from stakepool to pledge address\n")
    p = input("Are you ok with transferring the rewards to the payment address (Y/N)?")

    if p == "Y" or p == "y":
        pass;
    else:
        sys.exit("Quitting!")
        
    return args
        
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--pay_address', dest="target",help='Payment address')
    parser.add_argument('--amount', dest="amount",help='Amount in ADA to be transferred')
    args = parser.parse_args()

    print(args)
    
    if (args.target == None) or (args.amount == None):
        args = get_user_input(args)
        print(f"Trying to transfer funds {args.amount} to {args.target}")
        t = Transfer(args.target, args.amount)
        t.main()
            

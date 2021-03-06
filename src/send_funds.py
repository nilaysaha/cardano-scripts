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
    'payment': {'verify_key': './kaddr/payment.vkey', 'addr': './kaddr/payment.addr', 'sign_key': './kaddr/payment.skey'},
    'transaction': {'draft':'./kaddr/tx_extra.draft','raw': './kaddr/tx_extra.raw', 'signed':'./kaddr/tx_extra.signed'}
}

def _get_payment_utx0(t_address):
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


def _get_total_fund_in_utx0(t_address):
    t = _get_payment_utx0(t_address)
    total_fund = 0
    for val in t:
        total_fund += int(val[2])
    return total_fund



class CalcFee:
    def __init__(self):
        pass

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
        cardano-cli shelley transaction build-raw \
        --tx-in 4e3a6e7fdcb0d0efa17bf79c13aed2b4cb9baf37fb1aa2e39553d5bd720c5c99#4 \
        --tx-out $(cat payment2.addr)+0 \
        --tx-out $(cat payment.addr)+0 \
        --ttl 0 \
        --fee 0 \
        --out-file tx.draft
        """
        try:
            ttl = get_ttl()
            print(f"Inside draft transaction")
            tx_in_array= self.create_tx_in(tx_in)
            command = ["cardano-cli", "shelley", "transaction", "build-raw", "--tx-out",tx_out,  "--ttl", ttl,  "--fee", '0', '--out-file', FILES['transaction']['draft'] ] + tx_in_array
            print(command)
            s = subprocess.check_output(command)
            print(s)
        except:
            print("Oops!", sys.exc_info(), "occurred in draft transaction")
        

    def calculate_min_fees(self, tx_in, ttl, options={"raw_transaction":False}):
        try:            
            tx_in_count = len(tx_in)
            tx_out = f"{content(FILES['payment']['addr'])}+{0}"
            
            if (options["raw_transaction"] == False):
                fname =  FILES['transaction']['draft']            
                #generate the tx_raw first, as this is required for 1.18 MC4
                self.draft_transaction(tx_in, tx_out)
                witness_count = 2
            else:
                fname =  FILES['transaction']['raw']
                witness_count = 2
            
            command = [CARDANO_CLI, 'shelley',  'transaction', 'calculate-min-fee',
                       "--tx-body-file", fname,
                       "--witness-count", f"{witness_count}",
                       '--tx-in-count',  str(tx_in_count),
                       '--tx-out-count', str(1) ,
                       '--byron-witness-count', str(witness_count) ,
                       '--mainnet',
                       '--protocol-params-file', FILES['configs']['protocol'] ]
            print(f"{command}")
            s = subprocess.check_output(command,stderr=True, universal_newlines=True)
            print(f"output of command:{command} output is:{s}")
            min_fee = s.split(" ")[0]
            return min_fee
        except:
            print("Oops!", sys.exc_info()[0], "occurred in calculate min fees")

    def calc_remaining_funds(self, ttl, from_address, transfer_amount):
        try:
            min_fee = self.calculate_min_fees(tx_array_from_address, ttl)
            print(f"minimum fees: {min_fee}")
            
            #remaining funds needs to be transferred to the owner (from_address)
            remaining_funds = self.get_total_fund_in_utx0(from_address) - min_fee - transfer_amount
        except:
            print("Oops!", sys.exc_info()[0], "occurred in calculate min fees")


class Transaction:
    def __init__(self):
        pass
    
    def build(self, txArray, remaining_fund, ttl, min_fee):
        """
        reconstruct: 
           cardano-cli shelley transaction build-raw \
            --tx-in b64ae44e1195b04663ab863b62337e626c65b0c9855a9fbb9ef4458f81a6f5ee#1 \ (multiple values allowed)
            --tx-out $(cat payment.addr)+999428515 \
            --ttl 987654 \
            --fee 171485 \
            --out-file tx.raw \
            --certificate-file stake.cert
        """
        try:
            # Commented out "--ttl", ttl
            #Build the tx_in strings because there may be multiple values.
            tx_in_array = []
            for val in txArray:
                print(f"inside build_transaction: val:{val}")
                tx_in  = val[0]+"#"+val[1]
                print(f"tx_in:{tx_in}")
                tx_in_array.append('--tx-in')
                tx_in_array.append(tx_in)
            payment_addr = content(FILES['payment']['addr'])
            tx_out = "{paddr}+{rfund}".format(paddr=payment_addr, rfund=remaining_fund)
            command = [CARDANO_CLI, "shelley", "transaction", "build-raw",
                       "--tx-out",tx_out,
                       "--ttl", ttl,
                       "--fee", min_fee,
                       "--out-file", FILES['transaction']['raw'],
                       '--certificate-file', FILES['stake']['cert']] + tx_in_array
            print(command)
            s = subprocess.check_output(command)
            split_str=s.decode('UTF-8').split(" ")
        except:
            print("Oops!", sys.exc_info()[0], "occurred in build transaction")

    def sign(self):
        """
        reconstruct:
        cardano-cli shelley transaction sign \
        --tx-body-file tx.raw \
        --signing-key-file payment.skey \
        --signing-key-file stake.skey \
        --testnet-magic 42 \
        --out-file tx.signed
        """
        try:
            command = [CARDANO_CLI, "shelley", "transaction", "sign", "--tx-body-file", FILES['transaction']['raw'], '--signing-key-file',
                       FILES['payment']['sign_key'], '--signing-key-file', FILES['stake']['sign_key'], '--mainnet','--out-file',
                       FILES['transaction']['signed']]
            s = subprocess.check_output(command)
            print(s)
        except:
            print("Oops!", sys.exc_info()[0], "occurred in sign transaction")


    def submit(self):
        """
        reconstruct:
        cardano-cli shelley transaction submit \
        --tx-file tx.signed \
        --testnet-magic 42
        """
        try:
            command = [CARDANO_CLI, "shelley", "transaction", "submit", "--tx-file", FILES['transaction']['signed'], '--mainnet']
            s = subprocess.check_output(command)
            print("Submitted transaction for stake registration on chain usin: {command}. Result is: {s}")
        except:
            print("Oops!", sys.exc_info()[0], "occurred in submit transaction")

        
class Transfer:
    def __init__(self, from_address, to_address, transfer_amount):
        self.from_address = from_address
        self.to_address = to_address
        self.transfer_amount = transfer_amount 
        self.ttl = None
        self.remaining_fund = 0


    
    def _step_1(self):
        """                                                                                                                                                                                                 
        pre-requisites for transactions
        """
        try:
            pc.create_protocol()
            self.ttl = pc.get_ttl()
        except:
            print("Oops!", sys.exc_info()[0], "occurred in pre-req transaction for send funds. Step 1 for ref.")

    def _step_2(self):
        """                                                                                                                                                                                                 
        Build transaction
        """
        try:
            c = CalcFee()
            remaining_fund = c.calc_remaining_funds(self.ttl, self.from_address, self.transfer_amount)
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
                print("Enough funds present hence preparing for transfer")
                self._step_3()
        except:
            print("Oops!", sys.exc_info()[0], "overall function to coordinate transfer")
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--from', dest="src",help='Sending address')
    parser.add_argument('--to', dest="target",help='Receiving address')
    parser.add_argument('--amount', dest="amount",help='Amount in ADA to be transferred')
    args = parser.parse_args()

    if (args.src == None) or (args.target == None) or (args.amount == None):
        print("Either the src/destination/amount(ADA) is empty")
        
    else:
        print(f"Trying to transfer funds {args.amount} from:{args.src} to {args.target}")

    
    
    # t = Transfer()
    # t.main()
            

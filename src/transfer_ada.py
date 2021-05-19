#!/usr/bin/python3

"""
precondition to using this script:
  - Add directory 'trans' to this directory.
  - Add pay.skey and protocol.json to the trans directory created above.
  - Run the command.
"""

import subprocess, json, os, sys, shlex
import process_certs as pc
import native_tokens.create_nft_token as nft
import logging
import colorama
from colorama import Fore, Back, Style

MINIMUM_TOKEN_AMOUNT_ACCOMPANYING_TRANSFER=str(10000000)
ADA2LOVELACE=1000000

os.environ["CHAIN"] = "testnet"
os.environ["MAGIC"] = "1097911063"


FILES={
    "transaction": {
        "raw":"./trans/token.raw",
        "signed": "./trans/token.signed"},
    "protocol":"./trans/protocol.json",
    "payment": {
        "signature":"./trans/pay.skey"
    }
}

def run_command(command):
    print(Fore.GREEN + f"Command is:{command}")
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc

class Transfer:
    def __init__(self, input_addr, amount, output_addr):
        self.amount = amount
        self.dest_addr = output_addr
        self.payment_addr = input_addr
        self.utx0   = pc.get_payment_utx0_with_native_tokens(input_addr)
        self.pay_skey = FILES['payment']['signature']
        self.protocol_file = FILES['protocol']
                   
        
    def _generate_tx_in(self):
        try:
            tx_in_array = []
            for val in self.utx0:
                print(f"testing {val}")
                tx_in  = val["hash"]+"#"+val["tx"]
                print(f"tx_in:{tx_in}")
                tx_in_array.append('--tx-in')
                tx_in_array.append(tx_in)
            return tx_in_array                   
        except:
            logging.exception(f"Failed to generate_tx_in")
            sys.exit(1)            

    def set_payment_and_protocol(self, pay_skey=None, protocol_json=None):
        if pay_skey != None:
            self.pay_skey = pay_skey
            
        if protocol_json != None:
            self.protocol_file = protocol_json
            
    
    def remaining_fund_lovelace(self, fees=0, native_token_fees=MINIMUM_TOKEN_AMOUNT_ACCOMPANYING_TRANSFER):
        total_funds = pc.get_total_fund_in_utx0_with_native_tokens(self.payment_addr)
        rfund = total_funds["lovelace"] -int(fees) - int(self.amount)
        return rfund

    def remaining_native_tokens(self):
        rtokens = 0 #to be calculated. Till now no function to extract number available in payment address and substract self.amount
        return rtokens

    
    def raw_trans(self, fees):
        """
        Sample for : sending 1 melcoin to the recipient

        ./cardano-cli transaction build-raw \
	     --mary-era \
             --fee 0 \
             --tx-in fd0790f3984348f65ee22f35480b873b4eb9862065514f3e3a9c0f04d0a6ad63#0 \
             --tx-out addr_test1vp8s8zu6mr73nvlsjf935k0a38n8xvp3fptkyz2vl8pserqkcx5yz+10000000+"1 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \ #recipient address (Daedauls)
             --tx-out addr_test1vqvlku0ytscqg32rpv660uu4sgxlje25s5xrpz7zjqsva3c8pfckz+999821915+"999000000 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \  #payment address
             --out-file rec_matx.raw
        """
        try:
            raw_trans_file = FILES['transaction']['raw']
            remaining_fund = self.remaining_fund_lovelace(fees)
            total_token_counts = pc.get_total_fund_in_utx0_with_native_tokens(self.payment_addr)

            tx_out_recv_addr = f"{self.dest_addr}+{self.amount}"
            
            self_pay_string = f"{self.payment_addr}+{remaining_fund}"
            for key in total_token_counts.keys():
                if key != 'lovelace':
                    self_pay_string += f"+'{total_token_counts[key]} {key}'"
            
            tx_in_array = self._generate_tx_in()

            command=["cardano-cli", "transaction", "build-raw",
                     "--fee", str(fees),
                     "--tx-out", self_pay_string,
                     "--tx-out", tx_out_recv_addr,
                     "--out-file", raw_trans_file]+tx_in_array
            
            command_str = " ".join(command)
            print(Fore.RED + f"Command is:{command_str}")
            s = os.system(command_str)
            #run_command(command)            
        except:
            logging.exception("Unable to create raw transaction for receiving the nft tokens")
            sys.exit(1)

            
    def calculate_min_fees(self):
        """
        ./cardano-cli transaction calculate-min-fee \
        --tx-body-file rec_matx.raw \
        --tx-in-count 1 \
        --tx-out-count 2 \
        --witness-count 1 \
        --testnet-magic 3 \
        --protocol-params-file protocol.json
        """
        try:
            tx_body_file=FILES['transaction']['raw']
            protocol_file=FILES['protocol']
            command=["cardano-cli", "transaction", "calculate-min-fee", "--tx-body-file",tx_body_file, "--tx-in-count", str(1),
                     "--tx-out-count", str(2), "--witness-count", str(1), "--testnet-magic",os.environ["MAGIC"], "--protocol-params-file", protocol_file]
            print(Fore.GREEN + f"Command is:{command}")
            s = subprocess.check_output(command, stderr=True,  universal_newlines=True)
            return s.split()[0]
            print(f"Successful:  Output is:{s}")
        except:
            logging.exception("Failed to calculate the minimum fees for nft recv transaction")
            sys.exit(1)

    def sign_trans(self):
        """
        ./cardano-cli transaction sign \
	     --signing-key-file pay.skey \
	     --testnet-magic 3 \
	     --tx-body-file rec_matx.raw \
         --out-file rec_matx.signed

        """
        try:
            pay_skey = FILES['payment']['signature']
            tx_raw_file=FILES['transaction']['raw']
            tx_raw_signed=FILES['transaction']['signed']
            command=["cardano-cli", "transaction", "sign", "--signing-key-file", pay_skey, "--testnet-magic",os.environ["MAGIC"],
                     "--tx-body-file", tx_raw_file,
                     "--out-file", tx_raw_signed]
            print(Fore.GREEN + f"Command is:{command}")
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful:  Output is:{s}")
        except:
            logging.exception("Failed to sign transaction for nft recv transaction")
            sys.exit(1)
            
    def submit_trans(self):
        """
        ./cardano-cli transaction submit --tx-file  rec_matx.signed --testnet-magic 3

        Note that we must send more than 1000000 Lovelace in the transaction. (mainnet-shelley-genesis.json:    "minUTxOValue": 1000000,)
        """
        try:
            tx_raw_signed=FILES['transaction']['signed']
            command=["cardano-cli", "transaction", "submit", "--tx-file", tx_raw_signed, "--testnet-magic", os.environ["MAGIC"]]
            print(Fore.GREEN + f"Command is:{command}")
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(f"Successful:  Output is:{s}")
        except:
            logging.exception("Failed to submit raw transaction nft recv transaction")
            sys.exit(1)

    def main(self):
        a.raw_trans(0)
        min_fees = a.calculate_min_fees()
        a.raw_trans(min_fees)
        a.sign_trans()
        a.submit_trans()


if __name__ == "__main__":
    import argparse
    # create parser
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--inputAddr', dest='inputAddr', help="Payment address where funds originate from. This can also have other native tokens at the same utxo.  ")
    parser.add_argument('--amount', dest='amount', help="Amount of ADA to be transferred")
    parser.add_argument('--outputAddr', dest='outputAddr', help="Destination address where ADA needs to be transferred to.")
    parser.add_argument('--payskey', dest='pay_skey', help="Payment signature file required to sent a transaction from an address")
    parser.add_argument('--protocol', dest="protocol", help="Protocol.json file also required for sending payment from an address")
    
    args = parser.parse_args()
    
    if (args.inputAddr != None) and (args.amount != None) and (args.outputAddr != None) :
        a = Transfer(args.inputAddr, int(args.amount)*ADA2LOVELACE,args.outputAddr)

        if (args.payskey != None) or (args.protocol != None):
            a.set_payment_and_protocol(args.payskey, args.protocol)
            
        a.main()
    else:
        print("Not sufficient params. To see help: python3 transfer_ada.py --help")
        
        
        

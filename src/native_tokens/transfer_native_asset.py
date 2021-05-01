#!/usr/bin/python3

"""
Steps from:https://developers.cardano.org/en/development-environments/native-tokens/working-with-multi-asset-tokens/
Goal: to withdraw the native tokens to the Daedalus wallet (or backed by hardware wallet)


"""

import subprocess, json, os, sys, shlex
import process_certs as pc
import create_nft_token as nft
import logging
import colorama
from colorama import Fore, Back, Style

MINIMUM_TOKEN_AMOUNT_ACCOMPANYING_TRANSFER=str(10000000)

os.environ["CHAIN"] = "testnet"
os.environ["MAGIC"] = "1097911063"


FILES={
    "recieve":{
        "transaction": {
            "raw":"recv_token.raw",
            "signed": "recv_token.signed"
        }
    } 
}

def fetch_file(fpath, uuid):
    s = nft.Session(uuid)
    return s.sdir(fpath)


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
    def __init__(self, uuid, amount, policyid, coin_name,  output_addr):
        self.amount = amount
        self.uuid   = uuid
        self.pid    = policyid
        self.coin_name = coin_name
        self.dest_addr = output_addr
        self.payment_addr = pc.content(fetch_file(nft.FILES['payment']['address'], uuid))
        self.utx0   = pc.get_payment_utx0_with_native_tokens(self.payment_addr)
        self.s = nft.Session(uuid)
        
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
        
    def _generate_dest_addr_str(self):
        return "testing "+self.dest_addr+"+"+self.amount+'{}'

    def calculate_native_token_count(self):
        try:
            payment_addr = pc.content(self.s.sdir(nft.FILES['payment']['address']))
            utx0 = pc.get_payment_utx0(payment_addr)        
        except:
            logging.exception("Unable to calculate native token count in payment address")
    
    
    def remaining_fund(self, fees=0, native_token_fees=MINIMUM_TOKEN_AMOUNT_ACCOMPANYING_TRANSFER):
        if (int(fees) > 0):
            rfund = pc.get_total_fund_in_utx0(self.payment_addr) - int(fees) -int(native_token_fees)
        else:
            rfund = pc.get_total_fund_in_utx0(self.payment_addr)
            
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
            remaining_fund = str(self.remaining_fund(fees, MINIMUM_TOKEN_AMOUNT_ACCOMPANYING_TRANSFER))                
            raw_trans_file = self.s.sdir(FILES['recieve']['transaction']['raw'])
            remaining_native_tokens = str(self.remaining_native_tokens())
            tx_in_array = self._generate_tx_in()
            tx_out_receiver = f"{self.dest_addr}+{MINIMUM_TOKEN_AMOUNT_ACCOMPANYING_TRANSFER}+'{self.amount}  {self.pid}.{self.coin_name}'"
            tx_out_self_payment_addr = f"{self.payment_addr}+{remaining_fund}"

            command=["cardano-cli", "transaction", "build-raw",
                     "--fee", str(fees),
                     "--tx-out", tx_out_self_payment_addr,
                     "--tx-out", tx_out_receiver,
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
            tx_body_file=self.s.sdir(FILES['recieve']['transaction']['raw'])
            protocol_file=self.s.sdir(nft.FILES['protocol'])
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
            pay_skey = self.s.sdir(nft.FILES['payment']['signature'])
            tx_raw_file=self.s.sdir(FILES['recieve']['transaction']['raw'])
            tx_raw_signed=self.s.sdir(FILES['recieve']['transaction']['signed'])
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
            tx_raw_signed=self.s.sdir(FILES['recieve']['transaction']['signed'])
            command=["cardano-cli", "transaction", "submit", "--tx-file", tx_raw_signed, "--testnet-magic", os.environ["MAGIC"]]
            print(Fore.GREEN + f"Command is:{command}")
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(f"Successful:  Output is:{s}")
        except:
            logging.exception("Failed to submit raw transaction nft recv transaction")
            sys.exit(1)

    def main(self):
        self.raw_trans(0)
        min_fees = self.calculate_min_fees()
        self.raw_trans(min_fees)
        self.sign_trans()
        self.submit_trans()


if __name__ == "__main__":
    import argparse
    # create parser
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--uuid', dest='uuid')
    parser.add_argument('--amount', dest='amount')
    parser.add_argument('--policyid', dest='policyid')
    parser.add_argument('--coinname', dest='coinname')
    parser.add_argument('--outputAddr', dest='outputAddr')
    parser.set_defaults(latest=True)

    args = parser.parse_args()

    a = Transfer(args.uuid, args.amount, args.policyid, args.coinname,  args.outputAddr)
    a.main()
    
        
        
        

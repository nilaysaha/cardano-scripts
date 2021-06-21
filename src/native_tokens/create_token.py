#!/usr/bin/python3

import sys
sys.path.append('..')

import subprocess, json
import process_certs as pc;
import sys, os
import logging
import colorama
from colorama import Fore, Back, Style

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
colorama.init(autoreset=True)

FILES={
    'payment':{
        'verification': './kaddr_token/pay.vkey',
        'signature':'./kaddr_token/pay.skey',
        'address':'./kaddr_token/pay.addr'
    },
    'policy':{
        'verification': './kaddr_token/policy.vkey',
        'signature': './kaddr_token/policy.skey',
        'script': './kaddr_token/policy.script'
    },
    'protocol':'./kaddr_token/protocol.json',
    'transaction': {
        'raw': './kaddr_token/t.raw',
        'signed': "./kaddr_token/t.signed"
    },
    'status':{
        'phase_1':'./kaddr_token/phase_1',
        'phase_2':'./kaddr_token/phase_2',
        'phase_3':'./kaddr_token/phase_3',
    }
}

TOKEN_NAME="LKBH"
TOKEN_MAX_AMOUNT="45000000000"


def mint_new_asset(policy_file=FILES['policy']['script']):
    """
        ./cardano-cli transaction policyid --script-file ./policy/policy.script 
    """
    try:
        command = ["cardano-cli", "transaction", "policyid", "--script-file", policy_file]
        s = subprocess.check_output(command, stderr=True, universal_newlines=True)
        print(f"Successful: Output of command {command} is:{s}")
        return s.split("\n")[0]
    except:
        logging.exception("Could not mint new asset")            



class CreateToken:
    def __init__(self,token_name="REIT"):
        self.name = token_name

    def generate_keys(self):
        """
        cardano-cli address key-gen \
        --verification-key-file pay_bld.vkey \
        --signing-key-file pay_bld.skey
        
        """

        try:
            command = ["cardano-cli", "address", "key-gen", "--verification-key-file", FILES['payment']['verification'],
                       "--signing-key-file", FILES['payment']['signature']]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful:  Output of command {command} is:{s}")
            
        except:
            logging.exception("Could not generateg payment keys for token generation")



    def generate_payment_addr(self):
        """
        ./cardano-cli address build \
        --payment-verification-key-file pay_bld.vkey \
        --out-file pay_bld.addr \
        --mainnet        
        """

        try:
            command = ["cardano-cli", "address", "build", "--payment-verification-key-file", FILES['payment']['verification'],
                       '--out-file', FILES['payment']['address'], '--mainnet']
            print(command)
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful: Output of command {command} is:{s}")
        except:
            logging.exception("Could not generate payment addr for token generation")



    def export_protocol_params(self):
        """
        cardano-cli  query protocol-parameters \
	     --mainnet \
	     --out-file protocol.json
        """

        try:
            command = ["cardano-cli", "query" , "protocol-parameters", "--mainnet", "--mary-era","--out-file", FILES['protocol']]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful:Output of command {command} is:{s}")
        except:
            logging.exception("Could not export protocol params")


    def generate_policy_keys(self):
        """
        cardano-cli address key-gen \
        --verification-key-file policy/policy.vkey \
        --signing-key-file policy/policy.skey        
        """

        try:
            command = ["cardano-cli", "address", "key-gen", "--verification-key-file", FILES['policy']['verification'],
                       "--signing-key-file", FILES['policy']['signature']]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful: Output of command {command} is:{s}")
        except:
            logging.exception("Could not generate policy keys")


    def _generate_keyhash_pkey(self):
        """
        cardano-cli address key-hash --payment-verification-key-file policy/policy.vkey
        """
        try:
            command = ["cardano-cli", "address", "key-hash", "--payment-verification-key-file", FILES['policy']['verification']]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful: Output of command {command} is:{s}")
            return s.split("\n")[0]
        except:
            logging.exception("Could not generate keyhash")
            
        
            
    def generate_default_policy(self):
        """
        touch FILES['policy']['script']
        """
        try:
            fname = FILES['policy']['script']
            f = open(fname, "w+")
            policy_script = {
                "keyHash": self._generate_keyhash_pkey(),
                "type": "sig"
            }

            json_obj = json.dumps(policy_script, indent=4)
            f.write(json_obj)
            f.close()
        except:
            logging.exception("Could not generate default policy")


    def create_status_file(self,phase_id):
        """
        create file
        """
        from pathlib import Path
        Path(FILES['status'][phase_id]).touch()

    def check_status(self,phase_id):
        return  os.path.exists(FILES['status'][phase_id])


    def check_payment(self):
        """
        ./cardano-cli query utxo --address `cat pay_bld.addr`   --mary-era --mainnet
        """
        try:
            payment_addr = pc.content(FILES['payment']['address'])
            total_fund = pc.get_total_fund_in_utx0(payment_addr)
            print(f"Total funds in the address:{total_fund}")
            return {'addr':payment_addr, 'amount':total_fund}
        except:
            logging.exception("Could not check payment")

        
    
    def main_phase1(self):
        try:
            self.generate_keys()
            self.generate_payment_addr()
            self.create_status_file('phase_1')
        except:
            logging.exception("Could not complete phase 1")

            
    def main_phase2(self):
        try:
            t =  self.check_payment()
            print(f'Current amount in {t["addr"]} is {t["amount"]}')
            self.export_protocol_params()
            self.generate_policy_keys()
            self.generate_default_policy()
            self.create_status_file('phase_2') #add status
        except:
            logging.exception("Could not complete phase 2")

            
class Transaction:
    def __init__(self):
        self.payment_addr = pc.content(FILES['payment']['address'])
        self.utx0 = pc.get_payment_utx0(self.payment_addr)        


    def _calculate_utx0_lovelace(self, fees):
        a = CreateToken()
        n = a.check_payment()
        n["remaining_fund"] = n["amount"] -fees
        return n
            
        
    def create_raw_trans(self, fees, num_coins, coin_name, policy_id):
        """
        ./cardano-cli transaction build-raw \
	     --mary-era \
             --fee 0 \
             --tx-in b1ddb0347fed2aecc7f00caabaaf2634f8e2d17541f6237bbed78e2092e1c414#0 \
             --tx-out addr_test1vqvlku0ytscqg32rpv660uu4sgxlje25s5xrpz7zjqsva3c8pfckz+1000000000+"1000000000
                328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \
             --mint="1000000000 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \
             --out-file matx.raw
        """        
        try:
            tx_in_array = []
            for val in self.utx0:
                print(f"inside build_transaction: val:{val}")
                tx_in  = val[0]+"#"+val[1]
                print(f"tx_in:{tx_in}")
                tx_in_array.append('--tx-in')
                tx_in_array.append(tx_in)

            new_coin_mint_str = str(num_coins)+" "+policy_id+"."+coin_name
            utx0_status = self._calculate_utx0_lovelace(fees) 
            command=["cardano-cli", "transaction", "build-raw", "--mary-era",
                     "--fee", str(fees),
                     "--mint", new_coin_mint_str,
                     "--tx-out", self.payment_addr+"+"+str(utx0_status["remaining_fund"])+"+"+new_coin_mint_str,
                     "--out-file", FILES['transaction']['raw']]+tx_in_array
            
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Output of command {command} is:{s}")
        except:
            logging.exception("Could not create raw transaction")


    def calculate_min_fees(self):
        """
        ./cardano-cli transaction calculate-min-fee \
        --tx-body-file matx.raw \
        --tx-in-count 1 \
        --tx-out-count 1 \
        --witness-count 2 \
        --testnet-magic 3 \
        --byron-witness-count 0 \
        --protocol-params-file protocol.json        
        """
        try:
            command=[ "cardano-cli", "transaction", "calculate-min-fee",
                      "--tx-body-file", FILES['transaction']['raw'],
                      "--tx-in-count",str(len(self.utx0)),
                      "--tx-out-count", '1',
                      "--witness-count", '2',
                      "--byron-witness-count", '0',
                      "--mainnet",
                      "--protocol-params-file", FILES['protocol']]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            min_fees = int(s.split(" ")[0])  
            print(Fore.GREEN + f"Output of command {command} is:{min_fees}")
            return min_fees
        except:
            logging.exception("Could not calculate min fees")
        


    def sign_transaction(self):
        """
        ./cardano-cli transaction sign \
	     --signing-key-file pay.skey \
	     --signing-key-file policy/policy.skey \
	     --auxiliary-script-file policy/policy.script \
	     --testnet-magic 3 \
	     --tx-body-file matx.raw \
             --out-file matx.signed
        """
        try:
            command = ["cardano-cli", "transaction", "sign",
                       "--signing-key-file", FILES['policy']['signature'],
                       "--signing-key-file", FILES['payment']['signature'],
                       "--auxiliary-script-file", FILES['policy']['script'],
                       "--mainnet",
                       "--tx-body-file", FILES['transaction']['raw'],
                       '--out-file', FILES['transaction']['signed']]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Output of command {command} is:{s}")
        except:
            logging.exception("Could not sign transaction")

        

    def submit_transaction(self):
        """
        ./cardano-cli transaction submit --tx-file  matx.signed --mainnet
        """
        try:
            command = ["cardano-cli", "transaction", "submit", "--tx-file", FILES['transaction']['signed'] , "--mainnet"]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Output of command {command} is:{s}")
        except:
            logging.exception("Could not submit transaction")



    def main(self, num_coins, coin_name):
        a = CreateToken()
        t =  a.check_payment()
        if t['amount'] == 0:
            print(f"Current amount in {t['addr']} is zero. Please send some ADA to this address")
        else:
            policy_id = mint_new_asset()
            print(f"found policy id:{policy_id}")
            fees = 0
            self.create_raw_trans(fees, num_coins, coin_name, policy_id)
            min_fees = self.calculate_min_fees()
            self.create_raw_trans(min_fees, num_coins, coin_name, policy_id)
            self.sign_transaction()
            self.submit_transaction()


if __name__ == "__main__":
    num_coins = 45000000000
    coin_name = "REIT"
    
    c = CreateToken(coin_name)

    if not c.check_status('phase_1'):
        c.main_phase1()
    else:
        print('step 1 has been already run')        

    if not c.check_status('phase_2') and c.check_status('phase_1'):
            print(Fore.RED + 'Now proceeding to step 2')
            c.main_phase2()
            print("\n\n")
    else:
        print('STEP 2 has been already run')

    if c.check_status('phase_1') and c.check_status('phase_2') and not c.check_status('phase_3'):
        print(Fore.RED + 'Now proceeding to step 3')
        t = Transaction()
        t.main(num_coins, coin_name)
        print("\n\n")
    else:
        print('STEP 3 also has been completed earlier!')
            









        
        

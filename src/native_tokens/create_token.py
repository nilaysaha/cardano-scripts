#!/usr/bin/python3

import sys
sys.path.append('..')

import subprocess, json
import process_certs as pc;
import sys, os
import logging
import colorama
from colorama import Fore, Back, Style

import transfer_native_asset as tna

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
colorama.init(autoreset=True)

FILES={
    'payment':{
        'verification': './kaddr_new/pay.vkey',
        'signature':'./kaddr_new/pay.skey',
        'address':'./kaddr_new/pay.addr'
    },
    'policy':{
        'verification': './kaddr_new/policy.vkey',
        'signature': './kaddr_new/policy.skey',
        'script': './kaddr_new/policy.script'
    },
    'protocol':'./kaddr_new/protocol.json',
    'transaction': {
        'raw': './kaddr_new/t.raw',
        'signed': "./kaddr_new/t.signed"
    },
    'burn': {
        'raw': './kaddr_new/burn.raw',
        'signed': "./kaddr_new/burn.signed"
    },
    'status':{
        'phase_1':'./kaddr_new/phase_1',
        'phase_2':'./kaddr_new/phase_2',
        'phase_3':'./kaddr_new/phase_3',
    }
}

TOKEN_NAME="REIT"
TOKEN_MAX_AMOUNT=str(45*pow(10,15))
SLOT_OFFSET=56216369

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
            command = ["cardano-cli", "query" , "protocol-parameters", "--mainnet", "--out-file", FILES['protocol']]
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
            policy_script ={
                "type": "all",
                "scripts":
                [
                    {
                        "type": "before",
                        "slot": pc.get_tip()+SLOT_OFFSET
                    },
                    {
                        "type": "sig",
                        "keyHash": self._generate_keyhash_pkey()
                    }
                ]
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
        ./cardano-cli query utxo --address `cat pay_bld.addr` --mainnet
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
    def __init__(self, burn=False):
        self.payment_addr = pc.content(FILES['payment']['address'])
        self.utx0 = pc.get_payment_utx0(self.payment_addr)        
        if burn :
            self.traw = FILES["burn"]["raw"]
            self.tsigned = FILES["burn"]["signed"]
        else:
            self.traw = FILES["transaction"]["raw"]
            self.tsigned = FILES["transaction"]["signed"]

    def _calculate_utx0_lovelace(self, fees):
        a = CreateToken()
        n = a.check_payment()
        n["remaining_fund"] = n["amount"] -fees
        return n

    def convert_token_to_hex(self,tokenName):
        import binascii
        Input = tokenName
        Input = str.encode(Input)
        Input = binascii.hexlify(Input)
        return Input.decode()

    def get_slotNumber(self):
        import json
        with open(FILES["policy"]["script"]) as f:
            data = json.load(f)
        print("policy data read is:", data)
        return data["scripts"][0]["slot"]
            
    def create_raw_trans(self, fees, num_coins, coin_name, policy_id):
        """
        ./cardano-cli transaction build-raw \
             --fee 0 \
             --tx-in b1ddb0347fed2aecc7f00caabaaf2634f8e2d17541f6237bbed78e2092e1c414#0 \
             --tx-out addr_test1vqvlku0ytscqg32rpv660uu4sgxlje25s5xrpz7zjqsva3c8pfckz+1000000000+"1000000000
                328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \
             --mint="1000000000 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \
             --out-file matx.raw
        """        
        try:
            coin_name_hex = self.convert_token_to_hex(coin_name)
            tx_in_array = []
            for val in self.utx0:
                print(f"inside build_transaction: val:{val}")
                tx_in  = val[0]+"#"+val[1]
                print(f"tx_in:{tx_in}")
                tx_in_array.append('--tx-in')
                tx_in_array.append(tx_in)

            # last_slot =self.get_slotNumber() 
            new_coin_mint_str = str(num_coins)+" "+policy_id+"."+coin_name_hex
            utx0_status = self._calculate_utx0_lovelace(fees)
            print(utx0_status)
            tfund = utx0_status["remaining_fund"]


            #Now determine the native tokens present  
            t = tna.Transfer("kaddr_new", -num_coins, policy_id, coin_name, self.payment_addr)
            if fees > 0:
                tx_out_str = t.calculate_aggregated_token_out_str(fees)
            else:
                tx_out_str = f'{self.payment_addr}+0'
        
            command=["cardano-cli", "transaction", "build-raw",
                     "--fee", str(fees),
                     "--mint", new_coin_mint_str,
                     "--minting-script-file",FILES["policy"]["script"],
                     "--tx-out", tx_out_str,
                     # "--tx-out", self.payment_addr+"+"+str(tfund)+"+"+new_coin_mint_str,
                     # "--invalid-hereafter", str(last_slot), INTRODUCE THIS FOR TIME LIMITED TRANSACTION
                     "--out-file", self.traw]+tx_in_array
            
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
                      "--tx-body-file", self.traw,
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
                       "--mainnet",
                       "--tx-body-file", self.traw,
                       '--out-file', self.tsigned]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Output of command {command} is:{s}")
        except:
            logging.exception("Could not sign transaction")

        

    def submit_transaction(self):
        """
        ./cardano-cli transaction submit --tx-file  matx.signed --mainnet
        """
        try:
            command = ["cardano-cli", "transaction", "submit", "--tx-file", self.tsigned , "--mainnet"]
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
    num_coins = 45*pow(10,15)
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
            









        
        

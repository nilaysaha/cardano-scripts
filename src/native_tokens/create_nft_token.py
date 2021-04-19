#!/usr/bin/python3

import subprocess, json
import process_certs as pc;
import uuid
from uuid import UUID
import sys, os
import logging
import colorama
from colorama import Fore, Back, Style

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
colorama.init(autoreset=True)

MUUID = str(uuid.uuid4())
TOKEN_NAME=UUID(MUUID).hex
TOKEN_MAX_AMOUNT="1"
MIN_NFT_SLOT_OFFSET=0
MAX_NFT_SLOT_OFFSET=200

DEFAULT_URL="/ipfs/QmYypFZyFUwo4WNKzumg9FJbw836bZTbguqeLaazKmiHjb"

os.environ["CHAIN"] = "testnet"
os.environ["MAGIC"] = "1097911063"

FILES={
    'payment':{
        'verification': 'pay.vkey',
        'signature':'pay.skey',
        'address':'pay.addr'
    },
    'policy':{
        'verification': 'policy.vkey',
        'signature': 'policy.skey',
        'script': 'policy.script'
    },
    'protocol':'protocol.json',
    'transaction': {
        'raw': 't.raw',
        'signed': "t.signed"
    },
    'status':{
        'phase_1':'phase_1',
        'phase_2':'phase_2',
        'phase_3':'phase_3',
    },
    'metadata': {
        'store': 'metadata.json'
    }
}

def fetch_uuid_for_latest():
    try:
        dir_latest = os.path.join(os.getcwd(),'latest')
        dir_path = os.readlink(dir_latest)
        path_array = os.path.split(dir_path)
        print(f"path array is:{path_array}")
        return path_array[1]
    except:
        logging.exception("Could not find the uuid corresponding to the latest")
        sys.exit(1)

        
class Session:
    def __init__(self, latest=True, uuid=MUUID):
        self.latest = latest
        self.uuid = uuid

        if self.latest:
            self.uuid = None #both cannot be valid. We give preference to the latest.

        
    def sdir(self,fpath):
        try:
            dir_latest = os.path.join(os.getcwd(),'latest')
            print(dir_latest)
            
            if (not self.latest):
                print("WE ARE NOT USING THE LATEST")
                
                dir_path = os.path.join(os.getcwd(),'sessions',self.uuid)
                print(f"The directory being created for this session is:{dir_path}")

                if not os.path.exists(dir_path):
                    os.makedirs(dir_path,exist_ok=True)                    
                else:
                    print(f"Directory:{dir_path} exists already")

                if os.path.exists(dir_latest):
                    os.unlink(dir_latest)
                    
                os.symlink(dir_path,dir_latest)
            else:
                dir_path = os.readlink(dir_latest)
                print(f"Using the existing latest path:{dir_path}")
            
            return os.path.join(dir_path, fpath)
        except:
            logging.exception(f"Failed to construct session:{self.uuid} path for {fpath}")
            sys.exit(1)

                
            

class TokenMetadata:
    """
    Right now we are doing for single token. Later this can be adapted for multiple tokens.
    The CIP submitted for this is: https://www.reddit.com/r/CardanoDevelopers/comments/mkhlv8/nft_metadata_standard/
    """
    def __init__(self,uuid, name, policyid,  imgUrl, extra_data={}):
        self.imgUrl      = imgUrl
        self.tokenname   = name
        self.policyid    = policyid
        self.data = extra_data
        self.uuid = uuid

    def form(self):
        t={}
        t["nft"] = {
            "name": self.tokenname,
            "image": self.imgUrl
        }
        t1 = {}
        t1[self.policyid] = t

        t2 = {"721": t1}

        s = Session(True, self.uuid)
        metadata_file = s.sdir(FILES['metadata']['store'])
        f = open(metadata_file, 'w')
        json.dump(t2, f)
        f.close()
        return metadata_file
        
class CreateToken:
    """
    We will try to enforce the following CIP:https://forum.cardano.org/t/cip-nft-metadata-standard/45687
    Thus when minting NFT we will metadata and the above CIP standard.
    """
    def __init__(self, latest=False, uuid=MUUID):
        self.tip  = pc.get_tip() #Gets the current slot number
        self.s = Session(latest, uuid)
        self.uuid = uuid
        
    def generate_keys(self):
        """
        cardano-cli address key-gen \
        --verification-key-file pay_bld.vkey \
        --signing-key-file pay_bld.skey        
        """
        try:
            print(Fore.GREEN + f"Executing generate keys")            
            command = ["cardano-cli", "address", "key-gen", "--verification-key-file", self.s.sdir(FILES['payment']['verification']),
                       "--signing-key-file", self.s.sdir(FILES['payment']['signature'])]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful:  Output of command {command} is:{s}")            
        except:
            logging.exception("Could not generateg payment keys for token generation")
            sys.exit(1)
            
    def generate_payment_addr(self):
        """
        ./cardano-cli address build \
        --payment-verification-key-file pay_bld.vkey \
        --out-file pay_bld.addr \
        --testnet-magic 764824073        
 
        cardano-cli address build --payment-verification-key-file ./sessions/55d03462-cd0e-4fab-b0d6-0ce0be48e8bb/pay_bld.vkey --out-file ./sessions/55d03462-cd0e-4fab-b0d6-0ce0be48e8bb/pay_bld.addr
        """
        try:
            print(Fore.GREEN + f"Executing generate payment addr")            
            command = ["cardano-cli", "address", "build", "--payment-verification-key-file", self.s.sdir(FILES['payment']['verification']),
                       '--out-file', self.s.sdir(FILES['payment']['address']), '--testnet-magic', os.environ["MAGIC"]]
            print(command)
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful: Output of command {command} is:{s}")
        except:
            logging.exception("Could not generate payment addr for token generation")
            sys.exit(1)


    def export_protocol_params(self):
        """
        cardano-cli  query protocol-parameters \
	     --testnet-magic 764824073 \
	     --out-file protocol.json
        """
        try:
            print(Fore.GREEN + f"Executing export protocol params")            
            command = ["cardano-cli", "query" , "protocol-parameters", "--testnet-magic",os.environ["MAGIC"], "--out-file", self.s.sdir(FILES['protocol'])]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful:Output of command {command} is:{s}")
        except:
            logging.exception("Could not export protocol params")
            sys.exit(1)

    def generate_policy_keys(self):
        """
        cardano-cli address key-gen \
        --verification-key-file policy/policy.vkey \
        --signing-key-file policy/policy.skey        
        """

        try:
            print(Fore.GREEN + f"Executing policy keys")            
            command = ["cardano-cli", "address", "key-gen", "--verification-key-file", self.s.sdir(FILES['policy']['verification']),
                       "--signing-key-file", self.s.sdir(FILES['policy']['signature'])]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful: Output of command {command} is:{s}")
        except:
            logging.exception("Could not generate policy keys")
            sys.exit(1)

    def _generate_keyhash_pkey(self):
        """
        cardano-cli address key-hash --payment-verification-key-file policy/policy.vkey
        """
        try:
            print(Fore.GREEN + f"Executing generate keyhash")            
            command = ["cardano-cli", "address", "key-hash", "--payment-verification-key-file", self.s.sdir(FILES['policy']['verification'])]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful: Output of command {command} is:{s}")
            return s.split("\n")[0]
        except:
            logging.exception("Could not generate keyhash")
            sys.exit(1)
        
            
    def generate_default_policy(self):
        """
        generate keyhash and create policy script: FILES['policy']['script']
        """
        try:
            print(Fore.GREEN + f"Executing generate default policy")            
            fname = self.s.sdir(FILES['policy']['script'])
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
            sys.exit(1)

    def create_status_file(self,phase_id):
        """
        create file
        """
        print(Fore.GREEN + f"Executing status file")            
        from pathlib import Path
        Path(self.s.sdir(FILES['status'][phase_id])).touch()

    def check_status(self,phase_id):
        print(Fore.GREEN + f"Executing check status")            
        return  os.path.exists(self.s.sdir(FILES['status'][phase_id]))


    def check_payment(self):
        """
        ./cardano-cli query utxo --address `cat pay_bld.addr` --testnet-magic 764824073
        """
        try:
            print(Fore.GREEN + f"Executing check payments")            
            payment_addr = pc.content(self.s.sdir(FILES['payment']['address']))
            total_fund = pc.get_total_fund_in_utx0(payment_addr)
            print(f"Total funds in the address:{total_fund}")
            return {'addr':payment_addr, 'amount':total_fund}
        except:
            logging.exception("Could not check payment")
            sys.exit(1)
        
    
    def main_phase1(self):
        """
        can be triggered for any new customer. 
        """
        try:
            self.generate_keys()
            self.generate_payment_addr()
            self.create_status_file('phase_1')
        except:
            logging.exception("Could not complete phase 1")
            sys.exit(1)
            
    def main_phase2(self):
        """
        Send the new address to the frontend and ask for payment.
        """
        try:
            t =  self.check_payment()
            print(f'Current amount in {t["addr"]} is {t["amount"]}')
            self.export_protocol_params()
            self.generate_policy_keys()
            self.generate_default_policy()
            self.create_status_file('phase_2') #add status
        except:
            logging.exception("Could not complete phase 2")
            sys.exit(1)
            
                
class Transaction(CreateToken):
    def _calculate_utx0_lovelace(self, fees):
        n = self.check_payment()
        n["remaining_fund"] = n["amount"] -fees
        return n
            
        
    def create_raw_trans(self, fees, num_coins, coin_name, policy_id, metadata_file):
        """
        Pls note: there is redundant data in metadata_info (which also contains coin_name, policy etc.). Can be optimized later.

        ./cardano-cli transaction build-raw \
             --fee 0 \
             --invalid-before SLOT
             --invalid-hereafter SLOT+20
             --metadata-json-file metadata_file
             --tx-in b1ddb0347fed2aecc7f00caabaaf2634f8e2d17541f6237bbed78e2092e1c414#0 \
             --tx-out addr_test1vqvlku0ytscqg32rpv660uu4sgxlje25s5xrpz7zjqsva3c8pfckz+1000000000+"1000000000
                328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \
             --mint="1000000000 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \
             --out-file matx.raw
        """        
        try:
            payment_addr = pc.content(self.s.sdir(FILES['payment']['address']))
            utx0 = pc.get_payment_utx0(payment_addr)
            
            tx_in_array = []
            for val in utx0:
                print(f"inside build_transaction: val:{val}")
                tx_in  = val[0]+"#"+val[1]
                print(f"tx_in:{tx_in}")
                tx_in_array.append('--tx-in')
                tx_in_array.append(tx_in)

            new_coin_mint_str = str(num_coins)+' '+policy_id+'.'+coin_name
            utx0_status = self._calculate_utx0_lovelace(fees)

            ctip = int(pc.get_tip())
            print(Fore.RED + f"Current slotid/tip is:{ctip}")
            
            min_slot_id=ctip+MIN_NFT_SLOT_OFFSET
            max_slot_id=ctip+MAX_NFT_SLOT_OFFSET

            
            
            command=["cardano-cli", "transaction", "build-raw",
                     "--mint", new_coin_mint_str,
                     "--fee", str(fees),
                     "--metadata-json-file", metadata_file,
                     "--invalid-before",str(min_slot_id),
                     "--invalid-hereafter", str(max_slot_id),
                     "--tx-out", payment_addr+"+"+str(utx0_status["remaining_fund"])+"+"+new_coin_mint_str,
                     "--out-file", self.s.sdir(FILES['transaction']['raw'])]+tx_in_array

            
            print(Fore.RED + f"executing command {command}")
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Output is {s}")
        except:
            logging.exception("Could not create raw transaction")
            sys.exit(1)

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
            payment_addr = pc.content(self.s.sdir(FILES['payment']['address']))
            utx0 = pc.get_payment_utx0(payment_addr)        

            command=[ "cardano-cli", "transaction", "calculate-min-fee",
                      "--tx-body-file", self.s.sdir(FILES['transaction']['raw']),
                      "--tx-in-count",str(len(utx0)),
                      "--tx-out-count", '1',
                      "--witness-count", '2',
                      "--byron-witness-count", '0',
                      "--testnet-magic", os.environ["MAGIC"],
                      "--protocol-params-file", self.s.sdir(FILES['protocol'])]

            print(Fore.RED + f"executing command {command}")
            
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            min_fees = int(s.split(" ")[0])  
            print(Fore.GREEN + f"Output is min_fees:{min_fees}")
            return min_fees
        except:
            logging.exception("Could not calculate min fees")
            sys.exit(1)
            
    def sign_transaction(self):
        """
        ./cardano-cli transaction sign \
	     --signing-key-file pay.skey \
	     --signing-key-file policy/policy.skey \
	     --script-file policy/policy.script \
	     --testnet-magic 3 \
	     --tx-body-file matx.raw \
             --out-file matx.signed
        """
        try:
            command = ["cardano-cli", "transaction", "sign",
                       "--signing-key-file", self.s.sdir(FILES['policy']['signature']),
                       "--signing-key-file", self.s.sdir(FILES['payment']['signature']),
                       "--script-file", self.s.sdir(FILES['policy']['script']),
                       "--testnet-magic", os.environ["MAGIC"],
                       "--tx-body-file", self.s.sdir(FILES['transaction']['raw']),
                       '--out-file', self.s.sdir(FILES['transaction']['signed'])]

            print(Fore.RED + f"executing command {command}")
            
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Output is:{s}")
        except:
            logging.exception("Could not sign transaction")
            sys.exit(1)
        

    def submit_transaction(self):
        """
        ./cardano-cli transaction submit --tx-file  matx.signed --testnet-magic 764824073
        """
        try:
            command = ["cardano-cli", "transaction", "submit", "--tx-file", self.s.sdir(FILES['transaction']['signed']) , "--testnet-magic", os.environ["MAGIC"]]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Output of command {command} is:{s}")
        except:
            logging.exception("Could not submit transaction")
            sys.exit(1)

    def mint_new_asset(self):
        """
        ./cardano-cli transaction policyid --script-file ./policy/policy.script 
        """        
        try:
            policy_file=self.s.sdir(FILES['policy']['script'])
            command = ["cardano-cli", "transaction", "policyid", "--script-file", policy_file]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(f"Successful: Output of command {command} is:{s}")
            return s.split("\n")[0]
        except:
            logging.exception("Could not mint new asset")            
            sys.exit(1)

    def main(self, coin_name, num_coins, imgUrl=None, extra_metadata={}):
        try:
            t =  self.check_payment()
            if t['amount'] == 0:
                print(f"Current amount in {t['addr']} is zero. Please send some ADA to this address")
            else:
                policy_id = self.mint_new_asset()
                print(f"found policy id:{policy_id}")

                #Now create the metadata associated with this transaction
                m = TokenMetadata(self.uuid, coin_name,policy_id,imgUrl)
                metadata_file = m.form()
                
                
                fees = 0
                self.create_raw_trans(fees, num_coins, coin_name, policy_id, metadata_file)
                
                min_fees = self.calculate_min_fees()
                self.create_raw_trans(min_fees, num_coins, coin_name, policy_id, metadata_file)

                self.sign_transaction()
                self.submit_transaction()
        except:
            logging.exception("Failed main function")
            sys.exit(1)


if __name__ == "__main__":

    import argparse
    # create parser
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--latest', dest='latest', action='store_true')
    parser.add_argument('--not-latest', dest='latest', action='store_false')
    parser.add_argument('--uuid', dest='uuid')
    parser.set_defaults(latest=True)

    args = parser.parse_args()
    
    num_coins = 1
    coin_name = TOKEN_NAME

    if args.latest:
        args.uuid = fetch_uuid_for_latest()
    elif not args.uuid:
        args.uuid = MUUID
        
    c = CreateToken(args.latest, args.uuid)

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
        t = Transaction(c)
        t.main(coin_name, num_coins,DEFAULT_URL,)
        print("\n\n")
    else:
        print('STEP 3 also has been completed earlier!')

#!/usr/bin/python3

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


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
DEFAULT_DEST_ADDR="addr_test1vpyk92350x8gajyefdr44lk5jmjn9f8y4udfxw34pka5pvgjqxw4j"

DEFAULT_URL="/ipfs/QmYypFZyFUwo4WNKzumg9FJbw836bZTbguqeLaazKmiHjb"

os.environ["CHAIN"] = "testnet"
os.environ["MAGIC"] = "1097911063"

DEFAULT_INPUT={
    "name": "NFT1",
    "amount": "1",
    "payment": "100",
    "tags": "music, sunday",
    "dest_addr": DEFAULT_DEST_ADDR, 
    "metadata": {
	"url":"/ipfs/QmYypFZyFUwo4WNKzumg9FJbw836bZTbguqeLaazKmiHjb?filename=Screenshot%202021-03-18%20at%2007.33.06.png"
    }
}

FILES={
    'payment':{
        'verification':'pay.vkey',
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
    },
    'buffer': {
        'input':'input.json'
    }
}

class Inputs:
    def __init__(self,uuid):
        self.uuid = uuid        
        self.s = Session(uuid)
        
    def buffer(self, input_obj):
        f = open(self.s.sdir(FILES['buffer']['input']), "w")
        json_obj = json.dumps(input_obj, indent=4)
        f.write(json_obj)
        f.close()

        
    def fetch(self):
        s = Session(self.uuid)
        fpath = s.sdir(FILES['buffer']['input'])
        f = open(fpath, 'r')
        return json.load(f)    

    
def fetch_uuid_for_latest():
    try:
        dir_latest = os.path.join(os.getcwd(),'latest')

        if os.path.exists(dir_latest):
            dir_path = os.readlink(dir_latest)        
            path_array = os.path.split(dir_path)
            print(f"path array is:{path_array}")
            return path_array[1]
        else:
            return None
    except:
        logging.exception("Could not find the uuid corresponding to the latest")
        sys.exit(1)

def is_uuid_latest(uuid):
    """
    checks if the 'uuid' is the latest or not.
    if latest does not exist, then return False
    """
    if fetch_uuid_for_latest() == None:
        return False
    else:
        return fetch_uuid_for_latest() == uuid
        
        
class Session:
    """
    Get the session information
    """
    def __init__(self, uuid):
        self.uuid = uuid


    def exists(self):
        dir_path = os.path.join(os.getcwd(),'sessions',self.uuid)
        if os.path.exists(dir_path):
            return dir_path
        else:
            return None
        
    def sdir(self,fpath):
        try:
            dir_path = os.path.join(os.getcwd(),'sessions',self.uuid)
            print(f"The directory being created for this session is:{dir_path}")
            
            if not os.path.exists(dir_path):
                os.makedirs(dir_path,exist_ok=True)                    
            else:
                print(f"Directory:{dir_path} exists already")

            return os.path.join(dir_path, fpath)
        except:
            logging.exception(f"Failed to construct session:{self.uuid} path for {fpath}")
            sys.exit(1)

                
            

class TokenMetadata:
    """
    Right now we are doing for single token. Later this can be adapted for multiple tokens.
    The CIP submitted for this is: https://www.reddit.com/r/CardanoDevelopers/comments/mkhlv8/nft_metadata_standard/
    """
    def __init__(self,uuid, name, policyid,  metadata={}):
        self.tokenname   = name
        self.policyid    = policyid
        self.data = metadata
        self.uuid = uuid
        self.m = {}
        
    def form(self):
        t={}
            
        t["nft"] = {
            "name": self.tokenname,
        }
        t1 = {}
        t1[self.policyid] = t

        t2 = {"721": t1}

        s = Session(self.uuid)
        metadata_file = s.sdir(FILES['metadata']['store'])
        f = open(metadata_file, 'w')
        json.dump(t2, f)
        self.m = t2
        f.close()
        return metadata_file

    def fetch(self):
        metadata_file = s.sdir(FILES['metadata']['store'])
        f = open(metadata_file, 'r')
        return json.load(f)
    
class CreateToken:
    """
    We will try to enforce the following CIP:https://forum.cardano.org/t/cip-nft-metadata-standard/45687
    Thus when minting NFT we will metadata and the above CIP standard.
    """
    def __init__(self, uuid):
        self.tip  = pc.get_tip() #Gets the current slot number
        self.s = Session(uuid)
        self.uuid = uuid
        self.policyId = None
        
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
            return t
        except:
            logging.exception("Could not complete phase 2")
            sys.exit(1)
            
                
class Transaction(CreateToken):
    def __init__(self,uuid, name, amount, metadata={}):
        super().__init__(uuid)
        self.name = name
        self.amount = amount
        self.metadata = metadata
        
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
             --tx-out <recipient_addr>+<MINIMUM_ADA>+"1 <policyid>.<coinname>"
             --mint="1000000000 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \
             --minting-script-file ${policyname}.policy.script
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
            ncms_2 = f"'{new_coin_mint_str}'"
            utx0_status = self._calculate_utx0_lovelace(fees)

            ctip = int(pc.get_tip())
            print(Fore.RED + f"Current slotid/tip is:{ctip}")
            
            min_slot_id=ctip+MIN_NFT_SLOT_OFFSET
            max_slot_id=ctip+MAX_NFT_SLOT_OFFSET

                        
            command=["cardano-cli", "transaction", "build-raw",
                     "--mint", new_coin_mint_str,
                     "--minting-script-file", self.s.sdir(FILES['policy']['script']),
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
	     --auxiliary-script-file policy/policy.script \ REMOVED IN 1.27.0
	     --testnet-magic 3 \
	     --tx-body-file matx.raw \
             --out-file matx.signed
        """
        try:
            command = ["cardano-cli", "transaction", "sign",
                       "--signing-key-file", self.s.sdir(FILES['policy']['signature']),
                       "--signing-key-file", self.s.sdir(FILES['payment']['signature']),
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
        ./cardano-cli transaction policyid --auxiliary-script-file ./policy/policy.script 
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

            
    def main(self):
        """
        This is a fair way to get contents because we are doing this is stepped fashion where only after payments this step can be executed.
        """
        try:
            #In principle we receive payment for a group of  tokens to be minted under a new policyId.
            t =  self.check_payment()            
            if t['amount'] == 0:
                print(f"Current amount in {t['addr']} is zero. Please send some ADA to this address")
                raise Exception(Fore.RED+f"Not sufficient funds in the payment address:{t['addr']}. Without this minting is not possible. Please deposit sufficient ADA into the above address")
            else:
                policy_id = self.mint_new_asset()
                print(f"found policy id:{policy_id}")
                
                #Now create the metadata associated with this transaction
                m = TokenMetadata(self.uuid, self.name, policy_id, self.metadata)                
                metadata_file = m.form()
                

                #--------------------CHALLENGE: HOW TO EXTEND THIS PART TO PRINT FOR MULTIPLE COIN_NAME, COIN_NUM ----------------#
                #-------------------------------- FOR NOW WE HAVE TESTED FOR SINGLE COIN NAME+ NUM_COINS COMBINATION--------------#

                fees = 0
                self.create_raw_trans(fees, self.amount, self.name, policy_id, metadata_file)
                
                min_fees = self.calculate_min_fees()
                self.create_raw_trans(min_fees, self.amount, self.name, policy_id, metadata_file)
                self.sign_transaction()
                self.submit_transaction()                
                #-----------------------------------------END: End creation of tokens --------------------------------------------#
            return (self.uuid, policy_id, self.name, self.amount, self.metadata)
        except:
            logging.exception("Failed main function")
            sys.exit(1)


def main_phase_A(uuid, sample_input_data=DEFAULT_INPUT):
    try:
        c = CreateToken(uuid)
                
        if not c.check_status('phase_1'):
            c.main_phase1()
        else:
            print('step 1 has been already run')        

        if not c.check_status('phase_2') and c.check_status('phase_1'):
            print(Fore.RED + 'Now proceeding to step 2')
            output = c.main_phase2()
            i = Inputs(uuid)
            i.buffer(sample_input_data)
            print("\n\n")
            return output
        else:
            print('STEP 2 has been already run') 
    except:
        logging.exception("Failed to create nft.")
        sys.exit(1)


def main_phase_B(uuid):
    """
    Currently minting only a single native token. TODO: Later should be extended to mint multiple token names corresponding to single policy_id in single transaction
    Fetch the inputs from phase A from input.json. We need :name=TOKEN_NAME, amount=1, metadata={}
    """
    try:
        c = CreateToken(uuid)
        i = Inputs(uuid)
        saved_params = i.fetch()
        
        if c.check_status('phase_1') and c.check_status('phase_2') and not c.check_status('phase_3'):        
            print(Fore.RED + 'Now proceeding to step 3')
            t = Transaction(uuid, saved_params["name"], saved_params["amount"], saved_params["metadata"])
            t.main()            
            c.create_status_file('phase_3')
            print("\n\n")
        else:
            print('STEP 3 also has been completed earlier!')
    except:
        logging.exception(f"Could not mint in phase_B")
        sys.exit(1)
        

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--new', dest='new', action='store_true', help="For a new customer request this is what creates a new session id")
    parser.add_argument('--uuid', dest='uuid', help="This customer uuid being assigned")
    parser.add_argument('--name', dest='name', help="Name of the NFT token. In absense we will assign some uuid based random name")
    parser.add_argument('--amount',dest='amount', help="Number of NFT tokens with the policy.name combination")
    parser.add_argument('--meta', dest='meta', help="Metadata associated with this NFT. Will vary depending on the medium like picture, video, text etc.")

    args = parser.parse_args()

    print(args.new)
    
    if args.new:
        args.uuid = MUUID        
    else:
        args.new = False
        
    #Phase 1 and Phase 2 generally run together. Phase 3 runs after payments gets submitted 
    if (args.new == True) :
        main_phase_A(args.uuid)
        
    #(in Phase 3: only seesion uuid is enough)
    if not args.new and args.uuid :
        main_phase_B(args.uuid)

    if not args.new and (args.uuid == None) :
        print(f"It is seems you need to run an existing uuid but forgot to mention that!")

        

#!/bin/python3

import subprocess, process_certs,os
import requests,shutil
import logging, sys

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')

CWD=os.getcwd()

BASE_URL = 'https://book.world.dev.cardano.org/environments/'
CARDANO_CLI="/home/nsaha/.cabal/bin/cardano-cli"

FILES={
    'configurations': {        
        'mainnet':{
            'config':os.path.join( CWD, 'tconfig/mainnet/config.json'),
            'topology':os.path.join( CWD, 'tconfig/mainnet/topology.json'),
            'shelley-genesis':os.path.join( CWD, 'tconfig/mainnet/shelley-genesis.json'),
            'byron-genesis':os.path.join( CWD, 'tconfig/mainnet/byron-genesis.json'),
            'alonzo-genesis':os.path.join( CWD, 'tconfig/mainnet/alonzo-genesis.json'),
            'submit-api-config':os.path.join( CWD, 'tconfig/mainnet/submit-api-config.json'),
            'db-sync-config':os.path.join( CWD, 'tconfig/mainnet/db-sync-config.json'),
            'conway-genesis':os.path.join( CWD, 'tconfig/mainnet/conway-genesis.json'),                        
        },
        'preview':{
            'config':os.path.join( CWD, 'tconfig/preview/config.json'),
            'topology':os.path.join( CWD, 'tconfig/preview/topology.json'),
            'shelley-genesis':os.path.join( CWD, 'tconfig/preview/shelley-genesis.json'),
            'byron-genesis':os.path.join( CWD, 'tconfig/preview/byron-genesis.json'),
            'alonzo-genesis':os.path.join( CWD, 'tconfig/preview/alonzo-genesis.json'),
            'submit-api-config':os.path.join( CWD, 'tconfig/preview/submit-api-config.json'),
            'db-sync-config':os.path.join( CWD, 'tconfig/preview/db-sync-config.json'),
            'conway-genesis':os.path.join( CWD, 'tconfig/preview/conway-genesis.json'),                        
        }
    }
}

def create_dir(d):
    try:
        print(f"create directory path: {d}")
        os.makedirs(d)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def create_file(content, fpath):
    try:
        dirname = os.path.dirname(fpath)
        if not os.path.isdir(dirname):
            create_dir(dirname)
        f = open(fpath,"w")
        print(f"Opened file:{fpath} for writing" )
        f.write(content)
        f.close()
    except IOError as e:
        print(e)
        
        
def fetch_init_files(network='mainnet'):
    """
        fetch all the configuration files for the chain initialization
    """
    print(f"fetch_init_files")
    try:
        fnames = [f'{network}/config.json', f'{network}/topology.json', f'{network}/shelley-genesis.json',f'{network}/byron-genesis.json',f'{network}/alonzo-genesis.json', f'{network}/conway-genesis.json',  f'{network}/db-sync-config.json', f'{network}/submit-api-config.json'  ]

        for c in fnames:
            turl = BASE_URL+c
            print(f"fetched content url:{turl}")
            r1 = requests.get(url = BASE_URL+c)
            print(f"content is {r1.text}")
            t = c.split('/')
            t.pop(0)
            print(f"value of t:{t}")
            if len(t) >= 1:
                key = t[0].split(".")[0]
            print(f"key is {key}")
            destination =  FILES['configurations'][network][key]
            print(f"destination is: {destination}")
            create_file(r1.text, destination)
            # If the response was successful, no Exception will be raised
            r1.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except:
        e = sys.exc_info()[0]
        print(f'Other error occurred: {e}')  # Python 3.6
    else:
        print('Success!')


class CreateKAddr:
    """
    In this we create the pairs of keys corresponding to the :https://github.com/input-output-hk/cardano-tutorials/blob/master/node-setup/020_keys_and_addresses.md
    Sequence of creation is:
    - payment skey & vkey
    - stake  skey & vkey
    - payment.addr
    - stake.addr
    """
    from subprocess import STDOUT
    
    def __init__(self, files=process_certs.FILES):
        self.files = files
        self.testnet_magic = 42
        print(f"createKaddr init")
        print(f"files is:{self.files}")
                    
    def _generate_payment_key_pair(self):
        """
        cardano-cli  address key-gen \
	    --verification-key-file $BASE_DIR/payment.vkey \
	    --signing-key-file $BASE_DIR/payment.skey;
        """
        try:
            command = [CARDANO_CLI , 'address', 'key-gen', '--verification-key-file', self.files['payment']['verify_key'], '--signing-key-file',  self.files['payment']['sign_key']]
            s = subprocess.check_output(command)
            print(f"generated payment key pair successfully!")
        except:
            e = sys.exc_info()[0]
            print(e)    

    def _generate_stake_key_pair(self):
        try:
            command = [CARDANO_CLI,  'stake-address', 'key-gen',  '--verification-key-file', self.files['stake']['verify_key'], '--signing-key-file',  self.files['stake']['sign_key']]
            s = subprocess.check_output(command)
            print(f"generated stake key pair successfully!")
        except:
            e = sys.exc_info()[0]
            print(e)

    def _generate_payment_addr(self):
        try:
            command = [CARDANO_CLI, 'address', 'build', '--payment-verification-key-file', self.files['payment']['verify_key'], '--stake-verification-key-file',
                       self.files['stake']['verify_key'],'--out-file', self.files['payment']['addr'], '--mainnet']# ,'--testnet-magic', str(self.testnet_magic)]
            print(f"command for payment addr : {command}")
            s = subprocess.check_output(command)
            print(f"generated payment addr successfully!")
        except:
            e = sys.exc_info()[0]
            print(e)
            
    def _generate_stake_addr(self):
        try:
            command = [CARDANO_CLI ,  'stake-address', 'build',
                       '--stake-verification-key-file', self.files['stake']['verify_key'],
                       '--out-file', self.files['stake']['addr'],'--mainnet']
                       # '--testnet-magic', str(self.testnet_magic)]        
            s = subprocess.check_output(command)
            print(f"generated stake address successfully!")
        except:
            e = sys.exc_info()[0]
            print(e)
            
            
    def _create_cert(self):                  
        try:
            command = [CARDANO_CLI,  'stake-address',  'registration-certificate' ,
                       '--stake-verification-key-file', self.files['stake']['verify_key'],
                       '--out-file', self.files['stake']['cert']]
            s = subprocess.check_output(command)
            print()
        except:
            e = sys.exc_info()[0]
            print(e)
            
    def main(self):
        print(f"Main function. Now generating payment and stake key/addr")
        try:
            self._generate_payment_key_pair()
            self._generate_stake_key_pair()
            self._generate_payment_addr()
            self._generate_stake_addr()
            self._create_cert()
        except:
            e = sys.exc_info()[0]
            print(e)    


if __name__ == "__main__":
    import argparse
    descr = """
    Options to download config files or to create keys etc.
    """
    parser = argparse.ArgumentParser(description=descr, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--network", help="The network should be either 'mainnet' or 'preview' or 'preprod'", default="mainnet")
    parser.add_argument("--configs", help="Fetch the configs and store them in proper directory",action="store_true")
    parser.add_argument("--kaddr", help="create the pairs of keys corresponding to the github.com/input-output-hk/cardano-tutorials/blob/master/node-setup/020_keys_and_addresses.md",action="store_true")
    args = parser.parse_args()
    print(args)

    try:
        if args.configs:
            print(args.network)
            fetch_init_files(args.network)

            
        if args.kaddr:
            a = CreateKAddr()
            a.main()
    except:
        e = sys.exc_info()[0]
        print(e)        

#!/bin/python3

import subprocess, process_certs,os
import requests,shutil
    
CWD=os.getcwd()

FILES={
    'configurations':{
        'config':os.path.join( CWD, 'tconfig/shelley_testnet-config.json'),
        'topology':os.path.join( CWD, 'tconfig/shelley_testnet-topology.json'),
        'genesis':os.path.join( CWD, 'tconfig/shelley_testnet-genesis.json')
    }
}

BASE_URL = 'https://hydra.iohk.io/build/3175192/download/1/'
CARDANO_CLI="/home/nsaha/.cabal/bin/cardano-cli"

def create_dir(d):
    try:
        print(f"create directory path: {d}")
        os.makedirs(d)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def create_file(content, fpath):
    try:
        # dirname = os.path.dirname(fpath)
        # create_dir(dirname)
        f = open(fpath,"w")
        f.write(content)
        f.close()
    except IOError as e:
        print(e)
        
        
def fetch_init_files():
    """
        fetch all the configuration files for the chain initialization
    """
    print(f"fetch_init_files")
    try:        
        fnames = ['shelley_testnet-config.json', 'shelley_testnet-topology.json', 'shelley_testnet-genesis.json' ]
        for c in fnames:
            turl = BASE_URL+c
            r1 = requests.get(url = BASE_URL+c)
            print(f"fetched content url:{turl}")
            print(f"content is {r1.text}")
            key = c.split('-')[-1].split('.')[0]
            print(f"key is {key}")
            destination =  FILES['configurations'][key]
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
    
    def __init__(self):
        self.files = process_certs.FILES
        self.testnet_magic = 42
        print(f"createKaddr init")
        print(f"files is:{self.files}")
                    
    def _generate_payment_key_pair(self):
        """
        cardano-cli shelley address key-gen \
	    --verification-key-file $BASE_DIR/payment.vkey \
	    --signing-key-file $BASE_DIR/payment.skey;
        """
        try:
            command = [CARDANO_CLI , 'shelley' ,'address', 'key-gen', '--verification-key-file', self.files['payment']['verify_key'], '--signing-key-file',  self.files['payment']['sign_key']]
            s = subprocess.check_output(command)
            print(f"generated payment key pair successfully!")
        except:
            e = sys.exc_info()[0]
            print(e)    

    def _generate_stake_key_pair(self):
        try:
            command = [CARDANO_CLI,  'shelley',  'stake-address', 'key-gen',  '--verification-key-file', self.files['stake']['verify_key'], '--signing-key-file',  self.files['stake']['sign_key']]
            s = subprocess.check_output(command)
            print(f"generated stake key pair successfully!")
        except:
            e = sys.exc_info()[0]
            print(e)

    def _generate_payment_addr(self):
        try:
            command = [CARDANO_CLI, 'shelley', 'address', 'build', '--payment-verification-key-file', self.files['payment']['verify_key'], '--stake-verification-key-file',
                       self.files['stake']['verify_key'],'--out-file', self.files['payment']['addr'], '--testnet-magic', str(self.testnet_magic)]
            print(f"command for payment addr : {command}")
            s = subprocess.check_output(command)
            print(f"generated payment addr successfully!")
        except:
            e = sys.exc_info()[0]
            print(e)
            
    def _generate_stake_addr(self):
        try:
            command = [CARDANO_CLI , 'shelley' , 'stake-address', 'build', '--stake-verification-key-file', self.files['stake']['verify_key'], '--out-file', self.files['stake']['addr'],
                       '--testnet-magic', str(self.testnet_magic)]        
            s = subprocess.check_output(command)
            print(f"generated stake address successfully!")
        except:
            e = sys.exc_info()[0]
            print(e)
            
            
    def _create_cert(self):                  
        try:
            command = [CARDANO_CLI,  'shelley' , 'stake-address',  'registration-certificate' ,'--stake-verification-key-file', self.files['stake']['verify_key'], '--out-file',
                       self.files['stake']['cert']]
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
    try:        
        a = CreateKAddr()
        a.main()
    except:
        e = sys.exc_info()[0]
        print(e)        

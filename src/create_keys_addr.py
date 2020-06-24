#!/bin/python3

import subprocess, process_certs,os

CWD=os.getcwd()

FILES={
    'configurations':{
        'genesis':os.path.join( CWD, './tconfig/genesis.json'),
        'topoloy':os.path.join( CWD, './tconfig/toplogy.json'),
        'genesis':os.path.join( CWD, './tconfig/genesis.json')
    }
}

BASE_URL = 'https://hydra.iohk.io/build/3175192/download/1/'

def _create_dir(d):
    import os
    try:
        os.makedirs(d)
    except OSError as e:
        if e.errno != errno.EEXIST:
        raise

def fetch_init_files():
    """
        fetch all the configuration files for the chain initialization
    """
    import requests,shutil,os
        
    try:
        fnames = ['shelley_testnet-config.json', 'shelley_testnet-topoloy.json', 'shelley_testnet-genesis.json' ]
        for c in fnames:
            r1 = requests.get(url = BASE_URL+c)
            key = c.split('-')[-1].split('.')[0]
            #create the directory if not exists
            shutil.move(c, FILES['configurations'][key])            
    except Exception as x:
        print(x)
        

class CreatKAddr:
    """
    In this we create the pairs of keys corresponding to the :https://github.com/input-output-hk/cardano-tutorials/blob/master/node-setup/020_keys_and_addresses.md
    Sequence of creation is:
    - payment skey & vkey
    - stake  skey & vkey
    - payment.addr
    - stake.addr
    """
    def __init__(self):
        self.files = process_certs.FILES
        self.testnet_magic = 42
                    
                    
    def _generate_payment_key_pair(self):
        command = ['cardano-cli' , 'shelley' ,'address', 'key-gen', '--verification-key-file', self.files['payment']['verif_key'], '--signing-key-file',  self.files['payment']['sign_key']]
        s = subprocess.check_output(command)
        return s

    def _generate_stake_key_pair(self):
        command = ['cardano-cli',  'shelley',  'stake-address', 'key-gen',  '--verification-key-file', self.files['stake']['verif_key'], '--signing-key-file',  self.files['stake']['sign_key']]
        s = subprocess.check_output(command)
        return s

    def _generate_payment_addr(self):
        command = ['cardano-cli', 'shelley', 'address', 'build', '--payment-verification-key-file', self.files['payment']['verif_key'], '--stake-verification-key-file',
                   self.files['stake']['verif_key'],'--out-file', self.files['payment']['addr'], '--testnet-magic', self.testnet_magic]
        s = subprocess.check_output(command)
        
        
    def _generate_stake_addr(self):
        command = ['cardano-cli' , 'shelley' , 'stake-address', 'build', '--stake-verification-key-file', self.files['stake']['verif_key'], '--out-file', self.files['stake'].['addr'],
                   '--testnet-magic', self.testnet_magic ]        
        s = subprocess.check_output(command)
        
    def _create_cert(self):
        command = ['cardano-cli',  'shelley' , 'stake-address',  'registration-certificate' ,'--stake-verification-key-file', self.files['stake']['verif_key'], 
                   '--out-file', self.files['stake']['cert']]
        s = subprocess.check_output(command)

    def main():
        try:
            self._generate_payment_key_pair()
            self._generate_stake_keys()
            self._generate_payment_addr()
            self._generate_stake_addr()
        except Exception as x:
            print(x)    


if __name__ == "__main__":
    try:        
        a = CreatKAddr()
        a.main()
    except Exception as e:
        print(e)        

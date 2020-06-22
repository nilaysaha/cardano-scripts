#!/bin/python3

import subprocess



class Register:
    def __init__(self):
        self.files = {'stake': {'verif_key': "stake.vkey", 'addr': 'stake.addr', 'sign_key': 'stake.skey', 'cert': 'stake.cert' },
                      'payment': {'verif_key': 'payment.vkey', 'addr': 'payment.addr', 'sign_key': 'payment.skey'},
                      'protocol': 'protocol.json'}
        self.testnet_magic = 42

    def create_payment_keys(self):
        command = ['cardano-cli' , 'shelley' ,'address', 'key-gen', '--verification-key-file', self.files.payment.verif_key, '--signing-key-file',  self.files.payment.sign_key] 


    def generate_stake_keys(self):
        command = ['cardano-cli',  'shelley',  'stake-address', 'key-gen',  '--verification-key-file', self.files.stake.verif_key, '--signing-key-file',  self.files.stake.sign_key]


    def generate_payment_addr(self, payment_vkey, stake_vkey, testnet_magic):
        command = ['cardano-cli', 'shelley', 'address', 'build', '--payment-verification-key-file', self.files.payment.verif_key, '--stake-verification-key-file', self.files.stake.verif_key,
                   '--out-file', self.files.payment.addr, '--testnet-magic', testnet_magic]

    def generate_stake_addr(self, stake_vkey):
        command = ['cardano-cli' , 'shelley' , 'stake-address', 'build', '--stake-verification-key-file', self.files.stake.verif_key, '--out-file', self.files.stake.addr,
                   '--testnet-magic', self.testnet_magic ]        
        
    def create_cert(self):
        command = ['cardano-cli',  'shelley' , 'stake-address',  'registration-certificate' ,'--stake-verification-key-file', self.files.stake.verif_key, 
                   '--out-file', self.files.stake.cert]

    def calculate_minimum_fees(self, ttl, testnet_magic, ):
        command = ['cardano-cli', 'shelley', 'transaction', 'calculate-min-fee', '--tx-in-count', 1, '--tx-out-count', 1,  '--ttl', ttl,
                   '--testnet-magic', 42, '--signing-key-file', self.files.payment.sign_key, '--signing-key-file',  self.files.stake.sign_key,
                   '--certificate-file', self.files.stake.cert, '--protocol-params-file', protocol.json]

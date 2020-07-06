#!/bin/python3

"""
taken from: https://github.com/input-output-hk/cardano-tutorials/blob/master/Shelley-testnet/solutions/Exercise-4-solutions.md
"""
import create_keys_addr as cka
import process_certs_v2 as pc
import register_stake_pool as rsp

BASE_DIR="kaddr_delegate"

FILES={'stake': {'verify_key': f"./{BASE_DIR}/stake.vkey", 'addr': './{BASE_DIR}/stake.addr',
                 'sign_key': './{BASE_DIR}/stake.skey', 'cert': './{BASE_DIR}/stake.cert' },
       'payment': {'verify_key': './{BASE_DIR}/payment.vkey', 'addr': './{BASE_DIR}/payment.addr',
                   'sign_key': './{BASE_DIR}/payment.skey'},
       'configs': {'protocol': './{BASE_DIR}/protocol.json'},
       'transaction': {'raw': './{BASE_DIR}/tx.raw', 'signed':'./{BASE_DIR}/tx.signed'}
       }


class DelegateFunds:
    def __init__(self):
        pass

    def create_keys(self):
        t = cka.CreateKAddr(files=FILES)
        t.main()

    def load_payment_addr(self):
        payment_addr = pc.content(FILES['payment']['addr'])
        print("Now please load some ada/lovelace into payment address created:{payment_addr}")
        

    

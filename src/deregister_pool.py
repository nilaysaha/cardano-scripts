#!/usr/bin/env python3

import process_certs as pc
import subprocess, json, sys, json
import logging
import colorama
from colorama import Fore, Back, Style

"""
Deregister the pools using this manual: https://docs.cardano.org/projects/cardano-node/en/latest/stake-pool-operations/retire_stakepool.html
"""

FILES={
    'protocol':'./kaddr_dereg/protocol.json',
    'payment':'./kaddr_dereg/payment.addr',
    'pool':{
        'verification':'./kaddr_dereg/cold.vkey',
        'deRegCert':'./kaddr_dereg/pool-deregistration.cert'
    },
    'transaction': {
        'draft':'./kaddr_dereg/tx.draft',
        'raw': './kaddr_dereg/tx.raw',
        'sign': './kaddr_dereg/tx.signed'
    },
    'skey':{
        'payment':'./kaddr_dereg/payment.skey',
        "pool":"./kaddr_dereg/cold.skey"
    }
}

def get_epoch():
    """
    curl -s -m 3 -H 'Accept: application/json' http://127.0.0.1:12788/ | jq '.cardano.node.metrics.epoch.int.val'
    """
    try:
        command=["curl", "-s", "-m", "3", "-H", "'Accept: application/json'", "http://127.0.0.1:12788/", "|", "jq", " '.cardano.node.metrics.epoch.int.val'"]
        s = subprocess.check_output(command)
        print(Fore.RED + f"\noutput of command:{command} is:{s}\n\n")
    except:
        logging.exception("Could not get epoch")


def get_emax():
    """
    cardano-cli query protocol-parameters --mary-era --mainnet --out-file /tmp/protocol.json
    cat /tmp/protocol.json |grep eMax
    """
    try:
        command=["cardano-cli", "query", "protocol-parameters", "--mary-era", "--mainnet", "|", "grep", "eMax"]
        s = subprocess.check_output(command)
        r = s.split(":").split(",")[0]
        print(Fore.RED + f"\noutput of command:{command} is:{r}\n\n")
    except:
        logging.exception("Could not get epoch")
    

def build_multiple_tx_in_trans():
    payment_utx0_array = pc.get_payment_utx0(FILES['payment'])
    
    tx_in_array = []
    for val in payment_utx0_array:
        print(f"inside build_transaction: val:{val}")
        tx_in  = val[0]+"#"+val[1]
        print(f"tx_in:{tx_in}")
        tx_in_array.append('--tx-in')
        tx_in_array.append(tx_in)
        
    return tx_in_array
        
        
        

        
class Dregister:
    def __init__(self):
        self.tip = pc.get_tip()
        self.epoch = get_epoch()


    def generate_cert(self):
        """
        cardano-cli stake-pool deregistration-certificate \
        --cold-verification-key-file cold.vkey \
        --epoch 53 \
        --out-file pool-deregistration.cert
        """
        try:
            command=["cardano-cli", "stake-pool", "deregistration-certificate", "--cold-verification-key-file", FILES['pool']['verification'], '--epoch', self.epoch,
                     '--out-file', FILES['pool']['deRegisCert']]
            s = subprocess.check_output(command)
            print(Fore.RED + f"\noutput of command:{command} is:{s}\n\n")
        except:
            logging.exception("Could not generate cert")
                    
    def draft_transaction(self):
        """
        cardano-cli transaction build-raw \
        --tx-in <TxHash>#<TxIx> \
        --tx-out $(cat payment.addr)+0 \
        --invalid-hereafter 0 \
        --fee 0 \
        --out-file tx.draft \
        --certificate-file pool-deregistration.cert
        """
        try:
            tx_in_array = build_multiple_tx_in_trans()
            payment_addr = pc.content(FILES['payment'])
            tx_out=f"{payment_addr}+0"
            command=["cardano-cli", "transaction", "build-raw", "--tx-out",tx_out,
                     "--invalid-herafter",0, "--fee", 0, "--out-file", FILES['transaction']['draft'],'--certificate-file',FILES['pool']['deRegCert'],
                     "--tx-in"]+tx_in_array
            s = subprocess.check_output(command)
            print(Fore.RED + f"\noutput of command:{command} is:{s}\n\n")
       except:
           logging.exception("Could not draft transaction")
                                

    def main(self):
        self.generate_cert()
        self.draft_transaction()
        return self.calculate_min_fees()



class Transaction:
    def __init__(self):
        self.remaining_fund = pc.get_payment_utx0(FILES['payment']) - self._calculate_min_fees()
        self.epoch = get_epoch()

        
    def _calculate_min_fees(self):
        """
        cardano-cli transaction calculate-min-fee \
        --tx-body-file tx.draft \
        --tx-in-count 1 \
        --tx-out-count 1 \
        --witness-count 2 \
        --byron-witness-count 0 \
        --mainnet \
        --protocol-params-file protocol.json
        """
        try:
            command=["cardano-cli", "transaction", "calculate-min-fee", "--tx-body-file", FILES['transaction']['draft'],
                     "--tx-in-count", 1, "--tx-out-count", 1, "--witness-count", 2, "--byron-witness-count", 0, "--mainnet",
                     "--protocol-params-file", FILES['protocol']]
            s = subprocess.check_output(command)
            print(Fore.RED + f"\noutput of command:{command} is:{s}\n\n")
            min_fee = s.split(" ")[0]
            return min_fee
        except:
            logging.exception("Could not calculate min fees")

    
    def build_raw_transaction(self):
        """
        cardano-cli transaction build-raw \
        --tx-in 9db6cf...#0 \
        --tx-out $(cat payment.addr)+999999096457 \
        --invalid-hereafter 860000 \
        --fee 171309 \
        --out-file tx.raw \
        --certificate-file pool-deregistration.cert
        """
        try:
            tx_in_array = build_multiple_tx_in_trans()
            payment_addr = pc.content(FILES['payment'])
            tx_out_param = payment_addr+self.remaining_fund
            command=["cardano-cli", "transaction", "build-raw", "--tx-out",tx_out_param, "--invalid-hereafter",self.epoch, "--fee",self._calculate_min_fees(),
                     "--out-file", FILES['transaction']['raw'],
                     '--certificate-file-pool', FILES['pool']['deRegCert'],
                     "--tx-in"]+tx_in_array
            s = subprocess.check_output(command)
            print(Fore.RED + f"\noutput of command:{command} is:{s}\n\n")
        except:
            logging.exception("Could not build raw transaction")

            
    def sign_transaction(self):
        """
        cardano-cli transaction sign \
        --tx-body-file tx.raw \
        --signing-key-file payment.skey \
        --signing-key-file cold.skey \
        --mainnet \
        --out-file tx.signed
        """
        try:
            command=["cardano-cli", "transaction", "sign", "--tx-body-file", FILES['transaction']['raw'],
                     "--signing-key-file", FILES['skey']['payment'],
                     "--signing-key-file", FILES['skey']['pool'],
                     "--mainnet",
                     "--out-file", FILES['transaction']['sign']]
            s = subprocess.check_output(command)
            print(Fore.RED + f"\noutput of command:{command} is:{s}\n\n")
        except:
            logging.exception("Could not sign transaction")

    def submit_transaction(self):
        """
        cardano-cli transaction submit \
        --tx-file tx.signed \
        --mainnet
        """
        try
            command=["cardano-cli", "transaction", "submit", "--tx-file", FILES['transaction']['sign'], '--mainnet']
            s = subprocess.check_output(command)
            print(Fore.RED + f"\noutput of command:{command} is:{s}\n\n")            
        except:
            logging.exception("Could not submit transaction")
        
    def main(self):
        pass



if __name__=="__main__":
    pass


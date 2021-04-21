#!/bin/python3

import subprocess, sys, json, os
import logging
import colorama
from colorama import Fore, Back, Style


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
colorama.init(autoreset=True)



FILES={'stake': {'verify_key': "./kaddr/stake.vkey", 'addr': './kaddr/stake.addr', 'sign_key': './kaddr/stake.skey', 'cert': './kaddr/stake.cert' },
       'payment': {'verify_key': './kaddr/payment.vkey', 'addr': './kaddr/payment.addr', 'sign_key': './kaddr/payment.skey'},
       'configs': {'protocol': './kaddr/protocol.json'},
       'transaction': {'draft':'./kaddr/tx.draft','raw': './kaddr/tx.raw', 'signed':'./kaddr/tx.signed'}
       }

TTL_BUFFER=1200
WITNESS_COUNT_DEFAULT=4
BASE_ADDRESS_TXHASH="a09ba8bfc4b33961a744e059429b06981bfd689916971803371748917ceecc30"

CARDANO_CLI="/home/nsaha/.cabal/bin/cardano-cli"

def content(fname):
    f = open(fname, "r")
    text = f.read()
    return text


def get_tip():
    try:
        if os.environ["CHAIN"] == "testnet":
            command=[CARDANO_CLI , 'query', 'tip','--testnet-magic', str(os.environ["MAGIC"])]
        else:
            command = [CARDANO_CLI , "query" , "tip" ,"--mainnet"]
        s =  subprocess.check_output(command, stderr=True, universal_newlines=True)
        print(s)
        s_package = json.loads(s)
        return s_package["slot"]
    except:
        print("Oops!", sys.exc_info()[0], "occurred get ttl")

def get_ttl():
    current_tip = get_tip()
    ttl = int(current_tip)+TTL_BUFFER
    print("ttl:{v}".format(v=ttl))
    return str(ttl)

def create_protocol():
    """
        cardano-cli query protocol-parameters \
        --testnet-magic ${NETWORK_MAGIC} \
        --out-file ./kaddr/protocol.json
    """
    try:
        command = [ CARDANO_CLI, "query", "protocol-parameters", "--mainnet", "--out-file",
                    FILES['configs']['protocol']]
        s = subprocess.check_output(command)
    except:
        logging.exception(f"Oops! Error occured during create_protocol")


def _create_tx_in(tx_in):
    print(f"Inside _create_tx_in")
    tx_in_array = []
    for val in tx_in:
        print(f"inside build_transaction: val:{val}")
        tx_in  = val[0]+"#"+val[1]
        print(f"tx_in:{tx_in}")
        tx_in_array.append('--tx-in')
        tx_in_array.append(tx_in)
    print(f"tx_in_array:{tx_in_array}")
    return tx_in_array        
        
def _draft_transaction(tx_in, tx_out):
    """
    cardano-cli transaction build-raw \
    --tx-in 4e3a6e7fdcb0d0efa17bf79c13aed2b4cb9baf37fb1aa2e39553d5bd720c5c99#4 \
    --tx-out $(cat payment2.addr)+0 \
    --tx-out $(cat payment.addr)+0 \
    --ttl 0 \
    --fee 0 \
    --out-file tx.draft
    """
    try:
        ttl = get_ttl()
        print(f"Inside draft transaction")
        tx_in_array=_create_tx_in(tx_in)
        command = ["cardano-cli", "transaction", "build-raw",
                   "--tx-out",tx_out,  "--ttl", ttl,  "--fee", '0', '--out-file', FILES['transaction']['draft'] ] + tx_in_array
        print(command)
        s = subprocess.check_output(command)
        print(s)
    except:
        logging.exception("failed to draft transaction")
        
def calculate_min_fees(tx_in, ttl, options={"raw_transaction":False}):
    try:
        # commented out:  '--ttl',  str(ttl),
        # commented out:  '--signing-key-file', FILES['payment']['sign_key'], '--signing-key-file', FILES['stake']['sign_key']
        # commented out:  '--certificate-file', FILES['stake']['cert'],
        # Added: "--tx-body-file", FILES['transaction']['raw']

        print(f"tx_in:{tx_in} and ttl:{ttl}")
        
        tx_in_count = len(tx_in)
        tx_out = f"{content(FILES['payment']['addr'])}+{0}"

        
        if (options["raw_transaction"] == False):
            fname =  FILES['transaction']['draft']            
            #generate the tx_raw first, as this is required for 1.18 MC4
            _draft_transaction(tx_in, tx_out)
            witness_count = WITNESS_COUNT_DEFAULT
            byron_wc = 0
        else:
            fname =  FILES['transaction']['raw']
            witness_count = WITNESS_COUNT_DEFAULT
            byron_wc = 0
            
        command = [CARDANO_CLI, 'transaction', 'calculate-min-fee',
                   "--tx-body-file", fname,
                   "--witness-count", f"{witness_count}",
                   '--tx-in-count',  str(tx_in_count),
                   '--tx-out-count', str(1) ,
                   '--byron-witness-count', str(byron_wc) ,
                   '--mainnet',
                   '--protocol-params-file', FILES['configs']['protocol'] ]
        print(command)
        s = subprocess.check_output(command,stderr=True, universal_newlines=True)
        print(f"output of command:{command} output is:{s}")
        min_fee = s.split(" ")[0]
        return min_fee
    except:
        logging.exception("Failed to calculate min fees")
        
def get_payment_utx0(payment_addr=None):
    """
    should be able to add all the utx0 to the address. Ugly way that we have to support two networks. 
    """
    try:
        final_array = []
        
        if payment_addr == None:
            payment_addr = content(FILES['payment']['addr'])
            
        if os.environ["CHAIN"] == "testnet":
            command=[CARDANO_CLI , 'query', 'utxo', '--address', payment_addr, '--testnet-magic', str(os.environ["MAGIC"])]
        else:
            command=[CARDANO_CLI , 'query', 'utxo', '--address', payment_addr, '--mainnet']
            
        s = subprocess.check_output(command)
        split_str=s.decode('UTF-8').split("\n")
        result = filter(lambda x: x != '', split_str) 
        farray = list(result)[2:]
        print(f"farray:{farray}")        
        for val in farray:
            print(f"Now trying to split up :{val}\n")

            #Now we have to distinguish the scenario of presence of native tokens as well.
            #Scenario 1:'65fc4a7a2429e90b54848e9ceb24992bdf4a1dbd248259b9e91ff616df74aa22     0        1407406 lovelace + 2 6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7'
            #Scenario 2:'bd46fa89a00ae1ae4629fe85557a1695dfbc760a5227008beb074dda3976e9ea     0        1000000000 lovelace'
            
            (txHash, txtx, lovelace) = val.split('lovelace')[0].split()
            final_array.append((txHash, txtx, lovelace))
        print(f"final array:{final_array}")
        return final_array
    except:
        logging.exception("Failed to get payment utx0")


        
def get_payment_utx0_with_native_tokens(payment_addr=None):
    """
    should be able to add all the utx0 to the address. Ugly way that we have to support two networks. 
    """
    try:
        final_struct = {}
        
        #Final structure has to be like this:
        # [
        #     {
        #         "hash": "1ff5efd94b1e537875477f0dd3ebc630b519f40771d13596270c910bf319ab0a",
        #         "tx": "0",
        #         "tokens": [
        #             {
        #                 "id": "lovelace",
        #                 "count": "999808099"
        #             },
        #             {
        #                 "id": "ad9f33675c1bfa3db8a1e3ed943a8e3ce1b077a00fbd9cbe26bf9e15.a0c3aa67533d405d92e262ece8ed4344",
        #                 "count": "1"
        #             }
        #         ]
        #     }
        # ]

        if payment_addr == None:
            payment_addr = content(FILES['payment']['addr'])
            
        if os.environ["CHAIN"] == "testnet":
            command=[CARDANO_CLI , 'query', 'utxo', '--address', payment_addr, '--testnet-magic', str(os.environ["MAGIC"])]
        else:
            command=[CARDANO_CLI , 'query', 'utxo', '--address', payment_addr, '--mainnet']
            
        s = subprocess.check_output(command)
        split_str=s.decode('UTF-8').split("\n")
        result = filter(lambda x: x != '', split_str) 
        farray = list(result)[2:]
        print(f"farray:{farray}")
        futxo = []

    
        for val in farray:
            
            nt=[]
            print(f"Now trying to split up :{val}\n")

            #Now we have to distinguish the scenario of presence of native tokens as well.
            #Scenario 1:'65fc4a7a2429e90b54848e9ceb24992bdf4a1dbd248259b9e91ff616df74aa22     0        1407406 lovelace + 2 6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7
            #Scenario 2:'bd46fa89a00ae1ae4629fe85557a1695dfbc760a5227008beb074dda3976e9ea     0        1000000000 lovelace'    

            (txHash, txtx, lovelace) = val.split('lovelace')[0].split()
            
            nt.append({"id":"lovelace", "count": lovelace})
            
            native_token_array = val.split("+")[1:]
            
            for t in native_token_array:
                s = t.split()
                nt.append({"id": s[1], "count": s[0]})

            futxo.append(
                {
                    "hash": txHash,
                    "tx": txtx,
                    "tokens": nt
                }
            )

        print(f"final array:{native_token_array}")
        return futxo
    except:
        logging.exception("Failed to get payment utx0")

        
def get_total_fund_in_utx0(payment_addr=None):
    try:
        print(f"Now trying to get total funds in ADA in address:{payment_addr}")
        if payment_addr == None:
            payment_addr = content(FILES['payment']['addr'])
        t = get_payment_utx0(payment_addr)
        total_fund = 0
        for val in t:
            total_fund += int(val[2])
        return total_fund
    except:
        logging.exception(f"Failed to get total fund in the utxo of address:{payment_addr}")
    
    
def get_key_deposit_fee():
    import json
    s = json.loads(content(FILES['configs']['protocol']))    
    return int(s['keyDeposit'])

def get_pool_deposit_fee():
    import json
    s = json.loads(content(FILES['configs']['protocol']))    
    return int(s['poolDeposit'])


def get_git_tag():
    pass

def get_funds_via_faucet():
    """
    implement:
    curl -v -XPOST "https://faucet.mainnet-candidate-4.dev.cardano.org/send-money/$(cat payment.addr)?apiKey=YOURAPIKEY"  Ideally for 1.18 mainnet-candidate-4
    """
    try:        
        import requests        
        paddr = content(FILES['payment']['addr'])
        URL=f"https://faucet.mainnet-candidate-4.dev.cardano.org/send-money/{paddr}"
        r = requests.post(url = URL)
        return r.text #response text.
    except e:
        logging.exception("failed to get funds via faucet")
    

class RegisterStake:
    def __init__(self):
        pass

    def build_transaction(self, txArray, remaining_fund, ttl, min_fee):
        """
        reconstruct: 
           cardano-cli transaction build-raw \
            --tx-in b64ae44e1195b04663ab863b62337e626c65b0c9855a9fbb9ef4458f81a6f5ee#1 \ (multiple values allowed)
            --tx-out $(cat payment.addr)+999428515 \
            --ttl 987654 \
            --fee 171485 \
            --out-file tx.raw \
            --certificate-file stake.cert
        """
        try:
            # Commented out "--ttl", ttl
            #Build the tx_in strings because there may be multiple values.
            tx_in_array = []
            for val in txArray:
                print(f"inside build_transaction: val:{val}")
                tx_in  = val[0]+"#"+val[1]
                print(f"tx_in:{tx_in}")
                tx_in_array.append('--tx-in')
                tx_in_array.append(tx_in)
            payment_addr = content(FILES['payment']['addr'])
            tx_out = "{paddr}+{rfund}".format(paddr=payment_addr, rfund=remaining_fund)
            command = [CARDANO_CLI, "transaction", "build-raw",
                       "--tx-out",tx_out,
                       "--ttl", ttl,
                       "--fee", min_fee,
                       "--out-file", FILES['transaction']['raw'],
                       '--certificate-file', FILES['stake']['cert']] + tx_in_array
            print(command)
            s = subprocess.check_output(command)
            split_str=s.decode('UTF-8').split(" ")
        except:
            logging.exception("Failed to build transaction in registerstake")

    def sign_transaction(self):
        """
        reconstruct:
        cardano-cli transaction sign \
        --tx-body-file tx.raw \
        --signing-key-file payment.skey \
        --signing-key-file stake.skey \
        --testnet-magic 42 \
        --out-file tx.signed
        """
        try:
            command = [CARDANO_CLI, "transaction", "sign",
                       "--tx-body-file", FILES['transaction']['raw'], '--signing-key-file',
                       FILES['payment']['sign_key'], '--signing-key-file', FILES['stake']['sign_key'], '--mainnet','--out-file',
                       FILES['transaction']['signed']]
            s = subprocess.check_output(command)
            print(s)
        except:
            logging.exception("Failure in sign transaction")


    def submit_transaction(self):
        """
        reconstruct:
        cardano-cli  transaction submit \
        --tx-file tx.signed \
        --testnet-magic 42
        """
        try:
            command = [CARDANO_CLI, "transaction", "submit", "--tx-file",
                       FILES['transaction']['signed'], '--mainnet']
            s = subprocess.check_output(command)
            print("Submitted transaction for stake registration on chain usin: {command}. Result is: {s}")
        except:
            logging.exception("Failed to submit transaction")
            
def main():
    try:
        t = get_payment_utx0()
        print(f'collection of utx0 is:{t}')
        ttl = get_ttl()
        print(f"ttl calcuated is: {ttl}")

        create_protocol()        
        min_fee = calculate_min_fees(t, ttl)
        print(f"minimum fees: {min_fee}")
        dfund = get_key_deposit_fee()
        print(f"deposit:{dfund}")
        total_fund=get_total_fund_in_utx0()
        print(f"total fund:{total_fund}")
        rfund = total_fund  - int(min_fee) - dfund
        print(f"remaining fund:{rfund}")
        
        #Now time for transaction to submit the stake
        a = RegisterStake()
        a.build_transaction(t, rfund, ttl, min_fee) #txArray, remaining_fund, ttl, min_fee
        a.sign_transaction()
        a.submit_transaction()       
 
    except:
        logging.exception("Error in main function of process_certs.py")
        
if __name__ == "__main__": 
    main()                       
    

#!/bin/python3

import subprocess, sys, json

FILES={'stake': {'verify_key': "./kaddr/stake.vkey", 'addr': './kaddr/stake.addr', 'sign_key': './kaddr/stake.skey', 'cert': './kaddr/stake.cert' },
       'payment': {'verify_key': './kaddr/payment.vkey', 'addr': './kaddr/payment.addr', 'sign_key': './kaddr/payment.skey'},
       'configs': {'protocol': './kaddr/protocol.json'},
       'transaction': {'raw': './kaddr/tx.raw', 'signed':'./kaddr/tx.signed'}
       }

TTL_BUFFER=1200
TESTNET_MAGIC=42
BASE_ADDRESS_TXHASH="a09ba8bfc4b33961a744e059429b06981bfd689916971803371748917ceecc30"

CARDANO_CLI="/home/nsaha/.cabal/bin/cardano-cli"

def content(fname):
    f = open(fname, "r")
    text = f.read()
    return text


def get_tip():
    try:
        command = [CARDANO_CLI , "shelley" , "query" , "tip"  ,"--testnet-magic", "42"]
        s =  subprocess.check_output(command, stderr=True, universal_newlines=True)
        print(s)
        s_package = json.loads(s)
        return s_package["slotNo"]
    except:
        print("Oops!", sys.exc_info()[0], "occurred get ttl")

def get_ttl():
    current_tip = get_tip()
    ttl = int(current_tip)+TTL_BUFFER
    print("ttl:{v}".format(v=ttl))
    return str(ttl)

def create_protocol():
    """
        cardano-cli shelley query protocol-parameters \
        --testnet-magic ${NETWORK_MAGIC} \
        --out-file ./kaddr/protocol.json
    """
    try:
        command = [ CARDANO_CLI, "shelley", "query", "protocol-parameters", "--testnet-magic", str(TESTNET_MAGIC), "--out-file", FILES['configs']['protocol']]
        s = subprocess.check_output(command)
    except:
        print(f"Oops! Error occured during create_protocol: {sys.exc_info()[0]}")


    
def calculate_min_fees(tx_in_count, ttl):
    try:
        command = [CARDANO_CLI, 'shelley',  'transaction', 'calculate-min-fee',  '--tx-in-count',  str(tx_in_count),  '--tx-out-count', str(1) , '--ttl',  str(ttl),  '--testnet-magic', str(42), 
                   '--signing-key-file', FILES['payment']['sign_key'], '--signing-key-file', FILES['stake']['sign_key'], '--certificate-file', FILES['stake']['cert'],
                   '--protocol-params-file', FILES['configs']['protocol'] ]
        s = subprocess.check_output(command)
        min_fee = s.decode('UTF-8').split(" ")[1].split("\n")[0]
        return min_fee
    except:
        print("Oops!", sys.exc_info()[0], "occurred in calculate min fees")
        
def get_payment_utx0():
    """
    should be able to add all the utx0 to the address.
    """
    try:
        final_array = []
                
        command=[CARDANO_CLI, 'shelley' , 'query', 'utxo', '--address', content(FILES['payment']['addr']), '--testnet-magic', '42']
        s = subprocess.check_output(command)
        split_str=s.decode('UTF-8').split("\n")
        result = filter(lambda x: x != '', split_str) 
        farray = list(result)[2:]
        print(farray)        
        for val in farray:
            print(val)
            (txHash, txtx, lovelace) = val.split()
            final_array.append((txHash, txtx, lovelace))
        return final_array
    except:
        print("Oops!", sys.exc_info()[0], "occurred in get payment utx0")

def get_total_fund_in_utx0():
    t = get_payment_utx0()
    total_fund = 0
    for val in t:
        total_fund += int(val[2])
    return total_fund
        
def get_deposit_fee():
    #for now hacking. Ideally should be read from the protocol.json (which should be generated and then read) "keyDeposit": 400000,
    import json
    s = json.loads(content(FILES['configs']['protocol']))    
    return int(s['keyDeposit'])


def get_git_tag():
    pass

def get_funds_via_faucet():
    """
    implement:
    curl -v -XPOST "https://faucet.shelley-testnet.dev.cardano.org/send-money/$(cat payment.addr)"  Ideally for 1.14 git tag.
    """
    try:
        import requests
        paddr = content(FILES['payment']['addr'])
        URL="https://faucet.shelley-testnet.dev.cardano.org/send-money/%s"%(paddr)
        r = requests.post(url = URL)
        return r.text #response text.
    except e:
        print(e)
    

class RegisterStake:
    def __init__(self):
        pass

    def build_transaction(self, txArray, remaining_fund, ttl, min_fee):
        """
        reconstruct: 
           cardano-cli shelley transaction build-raw \
            --tx-in b64ae44e1195b04663ab863b62337e626c65b0c9855a9fbb9ef4458f81a6f5ee#1 \ (multiple values allowed)
            --tx-out $(cat payment.addr)+999428515 \
            --ttl 987654 \
            --fee 171485 \
            --out-file tx.raw \
            --certificate-file stake.cert
        """
        try:            
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
            command = [CARDANO_CLI, "shelley", "transaction", "build-raw", "--tx-out",tx_out,"--ttl", ttl, "--fee", min_fee,
                       "--out-file", FILES['transaction']['raw'], '--certificate-file', FILES['stake']['cert']] + tx_in_array
            print(command)
            s = subprocess.check_output(command)
            split_str=s.decode('UTF-8').split(" ")
        except:
            print("Oops!", sys.exc_info()[0], "occurred in build transaction")

    def sign_transaction(self):
        """
        reconstruct:
        cardano-cli shelley transaction sign \
        --tx-body-file tx.raw \
        --signing-key-file payment.skey \
        --signing-key-file stake.skey \
        --testnet-magic 42 \
        --out-file tx.signed
        """
        try:
            command = [CARDANO_CLI, "shelley", "transaction", "sign", "--tx-body-file", FILES['transaction']['raw'], '--signing-key-file',
                       FILES['payment']['sign_key'], '--signing-key-file', FILES['stake']['sign_key'], '--testnet-magic', '42','--out-file',
                       FILES['transaction']['signed']]
            s = subprocess.check_output(command)
            print(s)
        except:
            print("Oops!", sys.exc_info()[0], "occurred in sign transaction")


    def submit_transaction(self):
        """
        reconstruct:
        cardano-cli shelley transaction submit \
        --tx-file tx.signed \
        --testnet-magic 42
        """
        try:
            command = [CARDANO_CLI, "shelley", "transaction", "submit", "--tx-file", FILES['transaction']['signed'], '--testnet-magic', "42"]
            s = subprocess.check_output(command)
            print("Submitted transaction for stake registration on chain usin: {command}. Result is: {s}")
        except:
            print("Oops!", sys.exc_info()[0], "occurred in submit transaction")
            
def main():
    try:
        t = get_payment_utx0()
        print(f'collection of utx0 is:{t}')
        ttl = get_ttl()
        print(f"ttl calcuated is: {ttl}")
        create_protocol()        
        min_fee = calculate_min_fees(len(t),ttl)
        print(f"minimum fees: {min_fee}")
        dfund = get_deposit_fee()
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
        print("Oops!", sys.exc_info()[0], "occurred in main")
        
if __name__ == "__main__": 
    main()                       
    

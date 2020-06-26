#!/bin/python3

import subprocess, sys

FILES={'stake': {'verify_key': "./kaddr/stake.vkey", 'addr': './kaddr/stake.addr', 'sign_key': './kaddr/stake.skey', 'cert': './kaddr/stake.cert' },
       'payment': {'verify_key': './kaddr/payment.vkey', 'addr': './kaddr/payment.addr', 'sign_key': './kaddr/payment.skey'},
       'configs': {'protocol': './kaddr/protocol.json'},
       'transaction': {'raw': './kaddr/tx.raw', 'signed':'./kaddr/tx.signed'}
       }

TTL_BUFFER=1200
TESTNET_MAGIC=42

#replace this will the location of the cardabo binaries compiled using cabal
CARDANO_CLI="/home/nsaha/.cabal/bin/cardano-cli"

def content(fname):
    f = open(fname, "r")
    text = f.read()
    return text


def get_tip():
    try:
        command = [CARDANO_CLI , "shelley" , "query" , "tip"  ,"--testnet-magic", "42"]
        s =  subprocess.check_output(command)
        split_str = s.decode('UTF-8').split(" ")
        current_tip= split_str[4].split("}")[0]
        return current_tip
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


    
def calculate_min_fees(ttl):
    try:
        command = [CARDANO_CLI, 'shelley',  'transaction', 'calculate-min-fee',  '--tx-in-count',  str(1),  '--tx-out-count', str(1) , '--ttl',  str(ttl),  '--testnet-magic', str(42), 
                   '--signing-key-file', FILES['payment']['sign_key'], '--signing-key-file', FILES['stake']['sign_key'], '--certificate-file', FILES['stake']['cert'],
                   '--protocol-params-file', FILES['configs']['protocol'] ]
        s = subprocess.check_output(command)
        min_fee = s.decode('UTF-8').split(" ")[1].split("\n")[0]
        return min_fee
    except:
        print("Oops!", sys.exc_info()[0], "occurred in calculate min fees")
        
def get_payment_utx0():
    try:
        command=[CARDANO_CLI, 'shelley' , 'query', 'utxo', '--address', content(FILES['payment']['addr']), '--testnet-magic', '42']
        s = subprocess.check_output(command)
        split_str=s.decode('UTF-8').split(" ")
        result = filter(lambda x: x != '', split_str) 
        result_array = list(result)
        txHash, txtx, lovelace = result_array[-3].split("\n")[-1], result_array[-2], result_array[-1].split("\n")[0]
        return (txHash, txtx, lovelace)
    except:
        print("Oops!", sys.exc_info()[0], "occurred in get payment utx0")

def get_deposit_fee():
    #for now hacking. Ideally should be read from the protocol.json (which should be generated and then read) "keyDeposit": 400000,
    return 400000


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

    def build_transaction(self, txHash, txtx, remaining_fund, ttl, fee):
        """
        reconstruct: 
           cardano-cli shelley transaction build-raw \
            --tx-in b64ae44e1195b04663ab863b62337e626c65b0c9855a9fbb9ef4458f81a6f5ee#1 \
            --tx-out $(cat payment.addr)+999428515 \
            --ttl 987654 \
            --fee 171485 \
            --out-file tx.raw \
            --certificate-file stake.cert
        """
        try:
            payment_addr = content(FILES['payment']['addr'])
            tx_in  = "{txHash}#{txtx}".format(txHash=txHash, txtx=txtx)
            tx_out = "{paddr}+{rfund}".format(paddr=payment_addr, rfund=remaining_fund)
            command = [CARDANO_CLI, "shelley", "transaction", "build-raw", "--tx-in", tx_in, "--tx-out",tx_out,"--ttl", ttl, "--fee", fee,
                       "--out-file", FILES['transaction']['raw'], '--certificate-file', FILES['stake']['cert']]
            print(command)
            s = subprocess.check_output(command)
            print(s)
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
        txHash, txtx, lovelace = get_payment_utx0()
        print(f"txhash:{txHash}, txtx={txtx}, lovelace={lovelace}")
        ttl = get_ttl()
        print(f"ttl calcuated is: {ttl}")
        create_protocol()        
        min_fee = calculate_min_fees(ttl)
        print(f"minimum fees: {min_fee}")
        dfund = get_deposit_fee()
        print("deposit:{dfund}")
        rfund = int(lovelace) - int(min_fee) - dfund
        print("remaining fund:{rfund}")
        
        #Now time for transaction to submit the stake
        a = RegisterStake()
        a.build_transaction(txHash, txtx, rfund, ttl, min_fee)
        a.sign_transaction()
        a.submit_transaction()       
 
    except:
        print("Oops!", sys.exc_info()[0], "occurred in main")
        
if __name__ == "__main__": 
    main()                       
    

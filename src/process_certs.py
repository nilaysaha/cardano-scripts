#!/bin/python3

import subprocess, sys


FILES={'stake': {'verif_key': "./kaddr/stake.vkey", 'addr': './kaddr/stake.addr', 'sign_key': './kaddr/stake.skey', 'cert': './kaddr/stake.cert' },
       'payment': {'verif_key': './kaddr/payment.vkey', 'addr': './kaddr/payment.addr', 'sign_key': './kaddr/payment.skey'},
       'configs': {'protocol': './kaddr/protocol.json'},
       'transaction': {'raw': './kaddr/tx.raw', 'signed':'./kaddr/tx.signed'},
       'pool': {'cold': {'verify_key':"./kaddr/cold.vkey", "sign_key":"./kaddr/cold.skey","counter":"./kaddr/cold.counter"},
                'vrf': {'verify_key': './kaddr/vrf.vkey', 'sign_key': './kaddr/vrf.skey'}
                'kes': {'verify_key': './kaddr/kes.vkey', 'sign_key': "./kaddr/kes.skey"}},       
       'node': {'cert': './kaddr/node.cert'},
       'ff': {'genesis': '../ff-genesis.json', 'config':'../ff-config.json', 'topology': '../ff-topology.json'}
       }

TTL_BUFFER=1200

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
            print(s)
        except:
            print("Oops!", sys.exc_info()[0], "occurred in submit transaction")

class PoolKeys:
    def __init__(self):
        pass

    def generate_cold_kc(self):
        """
        cardano-cli shelley node key-gen \
        --cold-verification-key-file cold.vkey \
        --cold-signing-key-file cold.skey \
        --operational-certificate-issue-counter-file cold.counter
        """
        try:
            command = [ CARDANO_CLI, "shelley", "node", "key-gen", "--cold-verification-key-file", FILES['pool']['cold']['verify_key'],
                        '--cold-signing-key-file', FILES['pool']['cold']['sign_key'], '--operational-certificate-issue-counter-file',
                        FILES['pool']['cold']['counter']]
            s=subprocess.check_output(command)
        except:
            print("Oops!", sys.exc_info()[0], "occurred in generate cold kc")

    def generate_vrf_keys(self):
        """
        cardano-cli shelley node key-gen-VRF \
        --verification-key-file vrf.vkey \
        --signing-key-file vrf.skey
        """
        try:
            command = [ CARDANO_CLI, "shelley", "node", "key-gen-VRF", "--verification-key-file", FILES['pool']['vrf']['verify_key'],
                        '--signing-key-file', FILES['pool']['vrf']['sign_key']]
            s=subprocess.check_output(command)
        except:
            print("Oops!", sys.exc_info()[0], "occurred in generate vrf keys")
            
    def generate_kes_keys(self):
        """
        cardano-cli shelley node key-gen-KES \
        --verification-key-file kes.vkey \
        --signing-key-file kes.skey
        """
        try:
            command=[CARDANO_CLI, "shelley", "node", "key-gen-KES", "--verification-key-file", FILES['pool']['kes']['verify_key'],
                     '--signing-key-file', FILES['pool']['kes']['sign_key']]
            s=subprocess.check_output(command)
        except:
            print("Oops!", sys.exc_info()[0], "occurred in generate kes keys")

    def _calc_kes_period(self):
        import json
        genesis = json.loads(FILES['ff']['genesis'])
        slotsPerKESPeriod = genesis['slotsPerKESPeriod']
        qtip = int(current_tip())
        return qtip/slotsPerKESPeriod

            
    def generate_node_cert(self):
        """
        Ideally kesPeriod should be derived from genesis file. Here we will manually input it.
        cardano-cli shelley node issue-op-cert \
        --kes-verification-key-file kes.vkey \
        --cold-signing-key-file cold.skey \
        --operational-certificate-issue-counter cold.counter \
        --kes-period 120 \
        --out-file node.cert
        """
        try:
            kesPeriod = self._calc_kes_period()
            command = [ CARDANO_CLI, "shelly", "node", "issue-op-cert", "--kes-verification-key-file", FILES['pool']['kes']['verify_key'],
                        '--cold-signing-key-file', FILES['pool']['cold']['sign_key'], '--operational-certificate-issue-counter', FILES['pool']['cold']['counter'],
                        '--kes-period', kesPeriod, '--out-file', FILES['node']['cert']]
            s = subprocess.check_output(command)
            print(s)
        except:
            print("Oops!", sys.exc_info()[0], "occurred in generate node cert")
                    

    def backup_pool_keys(self):
        """
        We need to backup and then delete the pool keys. TO DO
        """
        pass
            
def main():
    try:
        ttl = get_ttl()
        print(ttl)
        min_fee = calculate_min_fees(ttl)
        print(min_fee)
        txHash, txtx, lovelace = get_payment_utx0()
        print(txHash, txtx, lovelace)
        dfund = get_deposit_fee()
        print(dfund)
        rfund = int(lovelace) - int(min_fee) - dfund
        print(rfund)
        
        #Now time for transaction to submit the stake
        a = RegisterStake()
        a.build_transaction(txHash, txtx, rfund, ttl, min_fee)
        a.sign_transaction()
        a.submit_transaction()       
 
    except:
        print("Oops!", sys.exc_info()[0], "occurred in main")
        
if __name__ == "__main__": 
    main()                       
    

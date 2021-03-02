#!/bin/python3

import subprocess, sys, requests
import process_certs as pc
import create_keys_addr as cka
import os, json, shutil

FILES={
    'pool': {'cold': {'verify_key':"./kaddr_node/cold.vkey", "sign_key":"./kaddr_node/cold.skey","counter":"./kaddr_node/cold.counter"},
             'vrf': {'verify_key': './kaddr_node/vrf.vkey', 'sign_key': './kaddr_node/vrf.skey'},
             'kes': {'verify_key': './kaddr_node/kes.vkey', 'sign_key': "./kaddr_node/kes.skey"},
             'cert': {'registration':'./kaddr_node/pool_registration.cert', 'delegation':'./kaddr_node/pool_delegation.cert'},
             'transaction': {'raw': './kaddr_node/pool_trans.raw', 'signed': './kaddr_node/pool_trans.signed'},
             'metadata': './kaddr_node/pool_metadata.json',
             'pledge': 'config/pool_stakeData.json'
    },       
    'node': {'cert': './kaddr_node/node.cert'},    
}

SETUP_CONFIGS = cka.FILES['configurations']
PROTOCOL_CONFIG = pc.FILES['configs']['protocol']
TTL_BUFFER=1200
KES_PORT=12798

CARDANO_CLI="/home/nsaha/.cabal/bin/cardano-cli"


def setup_run_configs():
    """
    Copies the relevant files needed for BP node to run in a proper directory kaddr_run.
    """
    print('inside setup run configs')
    try:
        flist = [FILES['pool']['vrf']['sign_key'], FILES['pool']['kes']['sign_key'], FILES['node']['cert']]
        print(flist)

        for i in flist:
            fname = os.path.basename(i)
            shutil.copyfile(i,'./kaddr_run/'+fname)            
    except Exception as e:
        print(e)

def encrypt_keys_and_addr():
    """
    Encrypt using GPG all the kaddr and kaddr_node files created during setup.
    """
    try:
        dirlist = ["./kaddr" , "./kaddr_node"]
        for i in dirlist:
            tfile = i+".tgz"
            command=["tar", "cvfz",tfile, i, ";", "gpg", "-c", tfile]
            print(command)
            s=subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(s)            
    except Exception as e:
        print(e)
        
            

        
def get_relay_params():
    relay_configs=[]
    #fetch it from topology file
    fname = SETUP_CONFIGS['topology']
    tp_config = json.loads(pc.content(fname))["Producers"]
    for relay in tp_config:
        relay_configs.append({"addr":relay["addr"],"port":relay['port']})
    return relay_configs


def get_pledge_params():
    pledgeFile = os.path.join(os.getcwd() , FILES['pool']['pledge'] )
    pcontent = pc.content(pledgeFile)
    pledgeConfig = json.loads(pcontent)
    return ( pledgeConfig['amount'], pledgeConfig['cost'], pledgeConfig['margin'])


def get_pooldeposit():
    try:
        import json
        print("inside get pooldeposit")
        fcontent = pc.content(SETUP_CONFIGS['shelley-genesis'])
        p=json.loads(fcontent)
        t = p["protocolParams"]["poolDeposit"]
        return t
    except Exception as e:
        print(e)

def _calc_min_fee():
    try:
        t = pc.get_payment_utx0()
        ttl = pc.get_ttl()
        return pc.calculate_min_fees(t, ttl, {"raw_transaction": True})
    except Exception as e:
        print(e)
    

def calc_transaction_amount(pay_pooldeposit):
    """
    calculate the amount: utx0 - minm_fees - pooldeposit
    At this point we assume that we have registered the stake address in the blockchain. Pooldeposit has to be paid only when we for the first time register the pool. 
    For all further transaction when we want to tune the pool params this need not be paid
    """
    try:
        print(f"Pooldeposit to be paid:{pay_pooldeposit}")
        print("calculate transaction amount")
        poolDeposit = 0
        cmin =  _calc_min_fee()
        if pay_pooldeposit:
            poolDeposit = get_pooldeposit()            
        print(f"minimum fee calc: {cmin}")
        print(f"pooldeposit:{poolDeposit}. Do we need to pay pooldeposit:{pay_pooldeposit}")
        
        # (txHash, txtx, lovelace) = pc.get_payment_utx0()[-1] #Assumption: We have all different txHash aggregated into single one(during stake address registration)
        # print(f"Selected txhash:{txHash} txtx:{txtx} lovelace:{lovelace}")
        
        fund_available = pc.get_total_fund_in_utx0()
        fund_required  = int(cmin) + int(poolDeposit)

        print(f"fund available:{fund_available}")
        print(f"fund required:{fund_required}")
        
        if (fund_available > fund_required):
            diff_fund = fund_available - fund_required
            print(f"calc transaction amount returned:{diff_fund}")
            return diff_fund
        else:
            return -1
    except:
        print("Oops!", sys.exc_info(), "error in calc transaction amount")


def remaining_kes_period():
    """
    curl localhost:12798/metrics | grep cardano_node_Forge_metrics_remainingKESPeriods_int
    """
    import re
    try:
        kes_period=0
        print('calculating remaining KES period')
        command=["curl", f"localhost:{KES_PORT}/metrics"]
        s = subprocess.check_output(command, stderr=True)
        rows = s.decode('UTF-8').split("\n")
        pattern="cardano_node_metrics_remainingKESPeriods_int"
        for i in rows:
            if re.search(pattern, i):
                print(f"found match:{pattern} with {i}")
                kes_period = i.split(' ')[-1]
                print(f"remaining kes period calculated is:{kes_period}")        
                break;
            else:
                #print(f"No match for:{pattern} for {i}")
                pass
    except:
        print("Oops!", sys.exc_info()[0], "error in remaining_kes_period")
    finally:
        return int(kes_period)
        
class PoolKeys:
    def __init__(self):
        #create the directory to hold the keys and certs for the nodes
        pass

    def generate_cold_kc(self):
        """
        cardano-cli  node key-gen \
        --cold-verification-key-file cold.vkey \
        --cold-signing-key-file cold.skey \
        --operational-certificate-issue-counter-file cold.counter
        """
        try:
            command = [ CARDANO_CLI, "node", "key-gen",  "--cold-verification-key-file"
                        , FILES['pool']['cold']['verify_key'],
                        '--cold-signing-key-file'
                        , FILES['pool']['cold']['sign_key']
                        , '--operational-certificate-issue-counter-file'
                        ,FILES['pool']['cold']['counter']]
            s=subprocess.check_output(command, stderr=True, universal_newlines=True)
        except:
            print("Oops!", sys.exc_info()[0], "occurred in generate cold kc")

    def generate_vrf_keys(self):
        """
        cardano-cli node key-gen-VRF \
        --verification-key-file vrf.vkey \
        --signing-key-file vrf.skey
        """
        try:
            command = [ CARDANO_CLI, "node", "key-gen-VRF",
                        "--verification-key-file", FILES['pool']['vrf']['verify_key'],
                        '--signing-key-file', FILES['pool']['vrf']['sign_key']]
            s=subprocess.check_output(command, stderr=True, universal_newlines=True)
        except:
            print("Oops!", sys.exc_info()[0], "occurred in generate vrf keys")
            
    def generate_kes_keys(self):
        """
        cardano-cli  node key-gen-KES \
        --verification-key-file kes.vkey \
        --signing-key-file kes.skey
        """
        try:
            command=[CARDANO_CLI, "node", "key-gen-KES",
                     "--verification-key-file", FILES['pool']['kes']['verify_key'],
                     '--signing-key-file', FILES['pool']['kes']['sign_key']]
            print(command)
            s=subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(s)
        except:
            print("Oops!", sys.exc_info()[0], "occurred in generate kes keys")

    def calc_kes_period(self):
        try:
            import json
            fcontent = pc.content(SETUP_CONFIGS['shelley-genesis'])
            genesis = json.loads(fcontent)
            slotsPerKESPeriod = genesis['slotsPerKESPeriod']            
            qtip = int(pc.get_tip())
            print(f"qtip:{qtip} and slotsperkes:{slotsPerKESPeriod}")
            kes_period=int(qtip/slotsPerKESPeriod)
            print(f'kes_period:{kes_period}')
            return kes_period
        except Exception:
            print ("error in level argument",Exception)

            
    def generate_node_cert(self):
        """
        Ideally kesPeriod should be derived from genesis file. Here we will manually input it.
        cardano-cli  node issue-op-cert \
        --kes-verification-key-file kes.vkey \
        --cold-signing-key-file cold.skey \
        --operational-certificate-issue-counter cold.counter \
        --kes-period 120 \
        --out-file node.cert
        """
        try:
            kesPeriod = str(self.calc_kes_period())
            command = [CARDANO_CLI, "node", "issue-op-cert",
                       "--kes-verification-key-file", FILES['pool']['kes']['verify_key'],
                       '--cold-signing-key-file', FILES['pool']['cold']['sign_key'],
                       '--operational-certificate-issue-counter', FILES['pool']['cold']['counter'],
                       '--kes-period', kesPeriod, '--out-file', FILES['node']['cert']]
            print(command)
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(s)
        except Exception:
            print("Oops!", sys.exc_info()[0], "occurred in generate node cert", Exception)
                    

    def backup_pool_keys(self):
        """
        We need to backup and then delete the pool keys. TO DO
        """
        pass


class RegisterStakePool:
    def __init__(self):
        self.POOL_META_URL="https://raw.githubusercontent.com/nilaysaha/cardano-scripts/master/src/config/pool_metadata.json"
        self.SHORT_POOL_META_URL = "https://lkbh-pool.s3.eu-central-1.amazonaws.com/metadata.json"
    
    def _fetch_pool_metadata(self, outfile):
        try:
            command=["curl","-so", outfile, self.SHORT_POOL_META_URL]
            print(f"command is:{command}")
            s=subprocess.check_output(command, stderr=True)
            print(f"pool metadata:{s}")
            return s
        except Exception as e:
            print(e)
            
    def generate_hash_of_pool_metadata(self):
        """
        execute: cardano-cli stake-pool metadata-hash --pool-metadata-file testPool.json
        """
        try:
            #first fetch pool metadata and store in file.(artifact of cardano cli command line)
            self._fetch_pool_metadata(FILES['pool']['metadata'])            
            #next hash content of file created
            command=[CARDANO_CLI ,"stake-pool", "metadata-hash",
                     "--pool-metadata-file", FILES['pool']['metadata']]
            s=subprocess.check_output(command, stderr=True)
            print(f"pool metadata:{s}")
            hash=s.decode('UTF-8').split("\n")[0]
            return hash
        except Exception as e:
            print(e)

    def _generate_relay_array(self, relay_params):
        relay_arr = []
        for i in relay_params:
            relay_arr += ["--single-host-pool-relay", str(i["addr"]),"--pool-relay-port", str(i["port"])]
        return relay_arr
            
            
    def generate_cert_stakepool(self, pledgeAmount, poolCost, poolMargin, relay_params):
        """
        cardano-cli stake-pool registration-certificate \
        --cold-verification-key-file cold.vkey \
        --vrf-verification-key-file vrf.vkey \
        --pool-pledge 100000000000 \
        --pool-cost 10000000000 \
        --pool-margin 0.05 \
        --pool-reward-account-verification-key-file stake.vkey \
        --pool-owner-stake-verification-key-file stake.vkey \
        --testnet-magic 42 \
        --pool-relay-ipv4 123.123.123.123 \
        --pool-relay-port 3001 \
        --metadata-url https://gist.githubusercontent.com/testPool/.../testPool.json \
        --metadata-hash 6bf124f217d0e5a0a8adb1dbd8540e1334280d49ab861127868339f43b3948af \
        --out-file pool.cert
        """
        try:
            print('Inside generate_cert_stakepool')
            pool_metadata_hash = self.generate_hash_of_pool_metadata()
            PFILES = pc.FILES

            relay_arr = self._generate_relay_array(relay_params)
            
            command = [CARDANO_CLI, "stake-pool", "registration-certificate",
                       "--cold-verification-key-file", FILES['pool']['cold']['verify_key'],
                       '--vrf-verification-key-file', FILES['pool']['vrf']['verify_key'],
                       "--pool-pledge", str(pledgeAmount),
                       "--pool-cost", str(poolCost),
                       "--pool-margin", str(poolMargin),
                       "--pool-reward-account-verification-key-file", PFILES['stake']['verify_key'],
                       "--pool-owner-stake-verification-key-file", PFILES['stake']['verify_key'],
                       "--mainnet",
                       "--metadata-url", self.SHORT_POOL_META_URL,
                       "--metadata-hash", str(pool_metadata_hash),
                       "--out-file", FILES['pool']['cert']['registration']] + relay_arr

            print(f"executing cert stakepool generate: {command}")
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(s)
        except Exception as e:
            print(e)

    def generate_delegation_cert(self):
        """
        cardano-cli stake-address delegation-certificate \
        --stake-verification-key-file stake.vkey \
        --cold-verification-key-file cold.vkey \
        --out-file delegation.cert
        """

        PFILES = pc.FILES
        command = [CARDANO_CLI,  "stake-address", "delegation-certificate",
                   "--stake-verification-key-file", PFILES['stake']['verify_key'],
                   "--cold-verification-key-file", FILES['pool']['cold']['verify_key'],
                   '--out-file', FILES['pool']['cert']['delegation'] ]
        s = subprocess.check_output(command, stderr=True, universal_newlines=True)
        print(s)




class SubmitStakePool:
    def __init__(self, createPool=False):
        self.createPool = createPool

    def _build_multiple_tx_in_trans(self):
        PFILES = pc.FILES
        TTL = pc.get_ttl()
        payment_utx0_array = pc.get_payment_utx0()

        tx_in_array = []
        for val in payment_utx0_array:
            print(f"inside build_transaction: val:{val}")
            tx_in  = val[0]+"#"+val[1]
            print(f"tx_in:{tx_in}")
            tx_in_array.append('--tx-in')
            tx_in_array.append(tx_in)

        return tx_in_array
        
    def build_transaction(self):
        """
        reconstruct:
        cardano-cli  transaction build-raw \
        --mary-era \
        --tx-in <UTXO>#<TxIx> \
        --tx-out $(cat payment.addr)+<CHANGE IN LOVELACE> \
        --ttl <TTL> \
        --fee <FEE> \
        --out-file tx.raw \
        --certificate-file pool-registration.cert \
        --certificate-file delegation.cert
        """
        try:
            PFILES = pc.FILES
            TTL = pc.get_ttl()
            tx_in_array = self._build_multiple_tx_in_trans()
            remaining_fund = calc_transaction_amount(self.createPool)
            fee = _calc_min_fee()
            payment_addr = pc.content(PFILES['payment']['addr'])
            tx_out = f"{payment_addr}+{remaining_fund}"
            print(f"remaining_fund:{remaining_fund}")
            command = [CARDANO_CLI,  "transaction", "build-raw",
                       "--mary-era",
                       "--tx-out",tx_out,
                       "--ttl", str(TTL),
                       "--fee", fee,                       
                       "--out-file", FILES['pool']['transaction']['raw'],
                       '--certificate-file', FILES['pool']['cert']['registration'],
                       "--certificate-file", FILES['pool']['cert']['delegation']]+tx_in_array
            print(command)
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(f"output for build transaction:{s}")
        except:
            print("Oops!", sys.exc_info()[0], "occurred in build transaction")

    def sign_transaction(self):
        """
        reconstruct:

        cardano-cli  transaction sign \
        --tx-body-file tx.raw \
        --signing-key-file payment.skey \
        --signing-key-file stake.skey \
        --signing-key-file cold.skey \
        --mainnet \
        --out-file tx.signed
        """
        PFILES=pc.FILES
        try:
            command = [CARDANO_CLI, "transaction", "sign",
                       "--tx-body-file", FILES['pool']['transaction']['raw'],
                       '--signing-key-file', PFILES['payment']['sign_key'],
                       '--signing-key-file', PFILES['stake']['sign_key'],
                       '--signing-key-file', FILES['pool']['cold']['sign_key'],
                       '--mainnet',
                       '--out-file', FILES['pool']['transaction']['signed']]
            print(command)
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(s)
        except:
            print("Oops!", sys.exc_info()[0], "occurred in sign transaction")


    def submit_transaction(self):
        """
        reconstruct:
        cardano-cli  transaction submit \
        --tx-file tx.signed \
        --mainnet
        """
        try:
            command = [CARDANO_CLI,  "transaction", "submit",
                       "--tx-file", FILES['pool']['transaction']['signed'],
                       '--mainnet']
            print(command)
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(s)
        except:
            print("Oops!", sys.exc_info()[0], "occurred in submit transaction")



class ChainProcess:
    """
    This presumes that we have a shelly-cardano.service file in /etc/systemd/system 
    so that systemctl is able to handle the commands below.
    """
    def __init__(self):
        pass

    def reload_chain(self):
        try:
            command = ["sudo", "systemctl", "reload", "shelly-cardano"]
            s = subprocess.check_output(command, stderr=True)
            print(f"reload chain first")
        except:
            print("Oops!", sys.exc_info()[0], "occurred in reload chain")

    def stop_chain(self):
        try:
            command = ["sudo", "systemctl", "stop", "shelly-cardano"]
            s = subprocess.check_output(command, stderr=True)
            print(f"stop chain first")
        except:
            print("Oops!", sys.exc_info()[0], "occurred in stop chain")


    def start_chain(self):
        try:
            command = ["sudo", "systemctl", "start", "shelly-cardano"]
            s = subprocess.check_output(command, stderr=True)
            print(f"start chain ")
        except:
            print("Oops!", sys.exc_info()[0], "occurred in start chain")

            
    
            
def main(options):
    """
    options: {'generate': true, 'register': true, 'submit':true, 'createPool':True, 'renewKES':false}
    """
    #generate the pool keys & cert
    if (options['generate']):
        print(f"Step: Generating the pool keys & certs")
        try:
            p = PoolKeys()
            p.generate_cold_kc()
            p.generate_vrf_keys()
            p.generate_kes_keys()
            p.generate_node_cert()
            print('--------------------Finished generating pool keys & node certs ---------------------------------\n')
        except Exception as e:
            print("Failed to generate pool keys and certs")
            print(e)

    #generate the pool keys & cert
    if (options['renewKES']):
        print(f"Step: Renewing the pool kes & certs")
        try:
            p = PoolKeys()
            p.generate_kes_keys()
            p.generate_node_cert()
            print('--------------------Finished generating kes keys & node certs ---------------------------------\n')
        except Exception as e:
            print("Failed to generate pool keys and certs")
            print(e)

    
    
    #register stake pool certs
    if (options["register"]):
        print(f"Step: Registering the pool certs")
        try:
            relay_params = get_relay_params()
            print(f"relay params are {relay_params}")
            (pledgeAmount, poolCost, poolMargin) = get_pledge_params()
            print(f"pledgeAmount:{pledgeAmount}  poolCost: {poolCost}   poolMargin:{poolMargin}")
            sp = RegisterStakePool()
            sp.generate_cert_stakepool(pledgeAmount, poolCost, poolMargin, relay_params)
            sp.generate_delegation_cert()
            print('--------------------Finished register stake pool certs ---------------------------------\n')
        except Exception as e:
            print("Failed to register stake pool certs")
            print(e)

        
    #submit the transaction
    if(options["submit"]):
        try:
            tr = SubmitStakePool(options['createPool'])
            tr.build_transaction() #only for createPool=True we pay 500ADA pool deposit fee.(refunded when pool deregistered)
            tr.sign_transaction()
            tr.submit_transaction()
        except Exception as e:
            print("Failed to submit the pool registration transaction")
            print(e)


            
if __name__ == "__main__": 
    main()                       

#!/usr/bin/python3

import process_cert as pc;

FILES={
    'payment':{
        'verification': './kaddr_token/pay.vkey',
        'signature':'./kaddr_token/pay.skey',
        'address':'./kaddr_token/pay.addr'
    },
    'policy':{
        'verification': './kaddr_token/policy.vkey',
        'signature': './kaddr_token/policy.skey',
        'script': './kaddr_token/policy.script'
    },
    'protocol':'./kaddr_token/protocol.json',
    'transaction': {
        'raw': './kaddr_token/t.raw',
        'signed': "./kaddr_token/t.signed"
    }
}



class CreateToken:
    def __init__(self,token_name="REIT"):
        self.name = token_name

    def generate_keys(self):
        """
        cardano-cli address key-gen \
        --verification-key-file pay_bld.vkey \
        --signing-key-file pay_bld.skey
        
        """

        try:
            command = ["cardano-cli", "address", "key-gen", "--verification-key-file", FILES['policy']['verification'],
                       "--signing-key-file", FILES['payment']['signature']]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(f"Output of command is:{s}")
        except:
            print("oops!", sys.exc_info()[0], " occured in generating payment keys for token generation")


    def generate_payment_addr(self):
        """
        ./cardano-cli address build \
        --payment-verification-key-file pay_bld.vkey \
        --out-file pay_bld.addr \
        --mainnet        
        """

        try:
            command = ["cardano-cli", "address", "build", "--payment-verification-key-file", FILES['payment']['verification'],
                       '--out-file', FILES['payment']['address'], '--mainnet']
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(f"Output of command {command} is:{s}")
        except:
            print("oops!", sys.exc_info()[0], " occured in generating payment address")            


    def check_payment(self):
        """
        ./cardano-cli query utxo --address `cat pay_bld.addr`   --mary-era --mainnet
        """
        try:
            payment_addr = pc.content(FILES['payment']['address'])
            total_fund = pc.get_total_fund_in_utx0(payment_addr)
            return total_fund
        except:
            print("Oops!", sys.exc_info()[0], " occured in check_payment")



    def export_protocol_params(self):
        """
        cardano-cli  query protocol-parameters \
	     --mainnet \
	     --out-file protocol.json
        """

        try:
            command = ["cardano-cli", "query" , "protocol-parameters", "--mainnet", "--out-file", FILES['protocol']]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(f"Output of command {command} is:{s}")
        except:
            print("Oops!", sys.exc_info()[0], " occured in check_payment")


    def generate_policy_keys(self):
        """
        cardano-cli address key-gen \
        --verification-key-file policy/policy.vkey \
        --signing-key-file policy/policy.skey        
        """

        try:
            command = ["cardano-cli", "address", "key-gen", "--verification-key-file", FILES['policy']['verification'],
                       "--signing-key-file", FILES['policy']['signature']]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(f"Output of command {command} is:{s}")
        except:
            print("Oops!", sys.exc_info()[0], " occured in generate_policy_keys")


    def _generate_keyhash_pkey(self):
        """
        cardano-cli address key-hash --payment-verification-key-file policy/policy.vkey
        """
        try:
            command = ["cardano-cli", "address", "key-hash", "--payment-verification-key-file", FILES['policy']['verification']]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(f"Output of command {command} is:{s}")
        except:
            print("Oops!", sys.exc_info()[0], " occured in generate_keyhash_pkey")
            
        
            
    def generate_default_policy(self):
        """
        touch FILES['policy']['script']
        """
        fname = FILES['policy']['script']

        if os.path.isfile(fname):
            print ("File is exist")
        else:
            print ("File is not exist")
            f = open(fname, "w+")
        if

        policy_script = {
            "keyHash": self._generate_keyhash_pkey(),
            "type": "sig"
        }

        f.write(policy_script)
        f.close()


    def mint_new_asset(self):
        """
        ./cardano-cli transaction policyid --script-file ./policy/policy.script 
        """
        try:
            command = ["cardano-cli", "transaction", "policyid", "--script-file", FILES['policy']['script']]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(f"Output of command {command} is:{s}")
            return s
        except:
            print("Oops!", sys.exc_info()[0], " occured in mint_new_asset")


    def main(self):
        self.generate_keys()
        self.generate_payment_addr()
        amount = self.check_payment()
        if (amount == 0):
            payment_addr = pc.content(FILES['payment']['address'])
            print(f"Please fund your account with payment address:{payment_addr}")
            exit 1
        self.export_protocol_params()
        self.generate_policy_keys()
        self.generate_default_policy()
        policy_id = self.mint_new_asset()
        return policy_id


class Transaction:
    def __init__(self):
        payment_addr = pc.content(FILES['payment']['address'])
        self.utx0 = pc.get_payment_utx0(payment_addr)


    def create_raw_trans(self, fees, num_coins, coin_name, policy_id):
        """
        ./cardano-cli transaction build-raw \
	     --mary-era \
             --fee 0 \
             --tx-in b1ddb0347fed2aecc7f00caabaaf2634f8e2d17541f6237bbed78e2092e1c414#0 \
             --tx-out addr_test1vqvlku0ytscqg32rpv660uu4sgxlje25s5xrpz7zjqsva3c8pfckz+1000000000+"1000000000 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \
             --mint="1000000000 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \
             --out-file matx.raw

        """
        
        try:
            new_coin_mint_str = str(num_coins)+" "+policy_id+"."+coin_name
            command=["cardano-cli", "build-raw", "--mary-era", "--fee", fees, "--tx-in", self.utx0+"#0"+new_coin_mint_str, "--mint", new_coin_mint_str,
                     "--out-file", FILES['transaction']['raw']]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(f"Output of command {command} is:{s}")
        except:
            print("Oops!", sys.exc_info()[0], " occured in mint_new_asset")            

    def calculate_min_fees(self):
        """
        ./cardano-cli transaction calculate-min-fee \
        --tx-body-file matx.raw \
        --tx-in-count 1 \
        --tx-out-count 1 \
        --witness-count 2 \
        --testnet-magic 3 \
        --protocol-params-file protocol.json        
        """
        try:
            command=[ "cardano-cli", "transaction", "calculate-min-fee", "--tx-body-file", FILES['transaction']['raw'],
                      "--tx-in-count", 1, "--tx-out-count", 1, "--witness-count", 2, "--mainnet", "--protocol-params-file", FILES['protocol']]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)            
            print(f"Output of command {command} is:{s}")
            return s
        except:
            print("Oops!", sys.exc_info()[0], " occured in sign_transaction")            
        


    def sign_transaction(self):
        """
        ./cardano-cli transaction sign \
	     --signing-key-file pay.skey \
	     --signing-key-file policy/policy.skey \
	     --script-file policy/policy.script \
	     --testnet-magic 3 \
	     --tx-body-file matx.raw \
             --out-file matx.signed
        """
        try:
            command = ["cardano-cli", "transaction", "sign", "--signing-key-file", FILES['payment']['signature'],
                       "--script-file", FILES['policy']['script'], "--mainnet", "--tx-body-file", FILES['transaction']['raw'], '--out-file', FILES['transaction']['signed']]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(f"Output of command {command} is:{s}")
        except:
            print("Oops!", sys.exc_info()[0], " occured in sign_transaction")            

        

    def submit_transaction(self):
        """
        ./cardano-cli transaction submit --tx-file  matx.signed --mainnet
        """
        try:
            command = ["cardano-cli", "transaction", "submit", "--tx-file", FILES['transaction']['signed'] ]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(f"Output of command {command} is:{s}")
        except:
            print("Oops!", sys.exc_info()[0], " occured in submit transaction")            



    def main(self, num_coins, coin_name, policy_id):
        fees = 0
        self.create_raw_trans(fees, num_coins, coin_name, policy_id)
        min_fees = self.calculate_min_fees()
        self.create_raw_trans(min_fees, num_coins, coin_name, policy_id)
        self.sign_transaction()
        self.submit_transaction()




if __name__ == "__main__":
    num_coins = 45000000000
    coin_name = "REIT"
    
    c = CreateToken(coin_name)
    
    t = Transaction()
    t.main()
            









        
        

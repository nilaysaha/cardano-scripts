#!/usr/bin/python3


"""
Steps from:https://developers.cardano.org/en/development-environments/native-tokens/working-with-multi-asset-tokens/
Goal: to withdraw the native tokens to the Daedalus wallet (or backed by hardware wallet)


"""

import process_certs as pc


FILES={
    'protocol':'./kaddr_token/protocol.json',
    'payment':{
        'addr':"./kaddr_token/pay.addr",
        'skey':"./kaddr_token/pay.skey"
    },
    'transaction':{
        'draft':"./kaddr_token/t.raw",
        'signed':"./kaddr_token/t.signed"        
    }
}


class Transfer:
    def __init__(self, amount, policyid):
        self.amount = amount
        self.pid    = policyid


    def raw_trans(self, fees, payment_addr, recipient_addr):
        """
        ./cardano-cli transaction build-raw \
	     --mary-era \
             --fee 0 \
             --tx-in fd0790f3984348f65ee22f35480b873b4eb9862065514f3e3a9c0f04d0a6ad63#0 \
             --tx-out addr_test1vp8s8zu6mr73nvlsjf935k0a38n8xvp3fptkyz2vl8pserqkcx5yz+10000000+"1 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \ #recipient address (Daedauls)
             --tx-out addr_test1vqvlku0ytscqg32rpv660uu4sgxlje25s5xrpz7zjqsva3c8pfckz+999821915+"999000000 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \  #payment address
             --out-file rec_matx.raw
        """
        pass

    def calculate_min_fees(self):
        """
        ./cardano-cli transaction calculate-min-fee \
        --tx-body-file rec_matx.raw \
        --tx-in-count 1 \
        --tx-out-count 2 \
        --witness-count 1 \
        --testnet-magic 3 \
        --protocol-params-file protocol.json
        """
        pass


    def sign_trans(self):
        """
        ./cardano-cli transaction sign \
	     --signing-key-file pay.skey \
	     --testnet-magic 3 \
	     --tx-body-file rec_matx.raw \
         --out-file rec_matx.signed

        """
        pass

    def submit_trans(self):
        """
        ./cardano-cli transaction submit --tx-file  rec_matx.signed --testnet-magic 3

        Note that we must send more than 1000000 Lovelace in the transaction. (mainnet-shelley-genesis.json:    "minUTxOValue": 1000000,)
        """
        pass


    def main(self):
        


if __name__ == "__main__":
    a = 
    
        
        
        

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
        'raw':"./kaddr_token/t.raw",
        'signed':"./kaddr_token/t.signed"        
    }
}

MINIMUM_TOKEN_AMOUNT_ACCOMPANYING_TRANSFER=1.407406


class Transfer:
    def __init__(self, amount, policyid, coin_name,  output_addr):
        self.amount = amount
        self.pid    = policyid
        self.coin_name = coin_name
        self.dest_addr = output_addr
        self.payment_addr = pc.content(FILES['payment']['addr'])
        self.utx0   = pc.get_payment_utx0(self.payment_addr)
        
    def _generate_tx_in(self):
        tx_in_array = []
        for val in self.utx0:
            print(f"inside build_transaction: val:{val}")
            tx_in  = val[0]+"#"+val[1]
            print(f"tx_in:{tx_in}")
            tx_in_array.append('--tx-in')
            tx_in_array.append(tx_in)
        return tx_in_array


    def _generate_dest_addr_str(self):
        return f"{self.dest_addr}+{self.amount}+'{}'"

    def remaining_fund(self, fees):
        rfund = pc.get_total_fund_in_utx0(self.payment_addr) - fees
        return rfund

    def remaining_native_tokens(self):
        rtokens = 10 #to be calculated. Till now no function to extract number available in payment address and substract self.amount
        return rtokens
    
    def raw_trans(self, fees):
        """
        Sample for : sending 1 melcoin to the recipient

        ./cardano-cli transaction build-raw \
	     --mary-era \
             --fee 0 \
             --tx-in fd0790f3984348f65ee22f35480b873b4eb9862065514f3e3a9c0f04d0a6ad63#0 \
             --tx-out addr_test1vp8s8zu6mr73nvlsjf935k0a38n8xvp3fptkyz2vl8pserqkcx5yz+10000000+"1 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \ #recipient address (Daedauls)
             --tx-out addr_test1vqvlku0ytscqg32rpv660uu4sgxlje25s5xrpz7zjqsva3c8pfckz+999821915+"999000000 328a60495759e0d8e244eca5b85b2467d142c8a755d6cd0592dff47b.melcoin" \  #payment address
             --out-file rec_matx.raw
        """
        remaining_fund = self.remaining_fund(fees)
        remaining_native_tokens = self.remaining_native_tokens()
        tx_in_array = self._generate_tx_in()
        tx_out_receiver = f'{self.dest_addr}+{MINIMUM_TOKEN_AMOUNT_ACCOMPANYING_TRANSFER}+"{self.amount} {self.pid}.{self.coin_name}"'
        tx_out_self_payment_addr = f'{self.payment_addr}+{remaining_fund}+"{remaining_native_tokens} {self.pid}.{self.coin_name}"'
        command=["cardano-cli", "transaction", "build-raw", "--mary-era",
                 "--fee", str(fees),
                 "--tx-out", self.dest_addr,
                 "--tx-out", self.
                 ,"--tx-in"]+tx_in_array

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
        command=["cardano-cli", "transaction", "calculate-min-fee", "--tx-body-file", ]


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
    
        
        
        

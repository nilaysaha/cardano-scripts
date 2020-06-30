#!/usr/bin/python3

import process_certs as pc


class UpdatePool:
    def __init__(self,txhash, txtx, lovelace):
        self.txHash = txhash
        self.txtx       = txtx
        self.lovelace   = lovelace

    def calc_params(self):
        """
        assumption is the protocol.json is present.
        """
        ttl = pc.get_ttl()
        print(f"ttl calcuated is: {ttl}")
        min_fee = pc.calculate_min_fees(ttl)
        print(f"minimum fees: {min_fee}")
        dfund = pc.get_deposit_fee()
        print("deposit:{dfund}")
        rfund = int(self.lovelace) - int(min_fee) - dfund
        print("remaining fund:{rfund}")
        

    def process_trans(self):
        a = pc.RegisterStake()
        a.build_transaction(self.txHash, self.txtx, rfund, ttl, min_fee)
        a.sign_transaction()
        a.submit_transaction()       



        
if __name__=="__main__":
    import argparse

    descr="This script is to update the poolpledge"
    
    parser = argparse.ArgumentParser(description=descr, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--txhash", type=str, required=True,
                        help="Please input the txhash which is the source of the fund")
    parser.add_argument("--txtx", type=str, required=True,
                        help="Please input the txtx which is the id of the hash")
    parser.add_argument("--lovelace", type=str, required=True,
                        help="Please input the lovelace to be deposited to the pool")

    args = parser.parse_args()
    print(f"txhash:{args.txhash} txtx:{args.txtx} lovelace:{args.lovelace}")
    a = UpdatePool(args.txhash, args.txtx, args.lovelace)
    a.calc_params()
    #a.process_trans()

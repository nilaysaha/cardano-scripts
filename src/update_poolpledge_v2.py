#!/usr/bin/python3

"""
Can be used to update the poolpledge. Please note that this uses the last UTX0 for taking the pledge amount. Incase we want to combine multiple utx0 then this needs to be modified.
Sample usage: python3 update_poolpledge_v2.py --lovelace 497430545
In order to change pledge follow the following steps:

 - ensure enough amount present in payment.addr (combined utx0. Updating new version of script to take all utx0)
 - change the pledge amount in: config/pool_stakeData.json
 - run this script
  (Note: NO NEED TO RESTART THE CHAIN, as we are not changing any keys that the chain uses. Just updating the certificate in the chain belonging to this pool)

"""

import process_certs as pc
import register_stake_pool as rsp

class UpdatePledge:
    def __init__(self, lovelace):
        self.lovelace   = int(lovelace)
        self.rfund = 0
        
    def check_funds_in_wallet(self):
        """
        assumption is the protocol.json is present.
        """
        try:
            t = pc.get_payment_utx0()
            self.ttl = pc.get_ttl()
            print(f"ttl calculated is: {self.ttl}")
            self.min_fee = pc.calculate_min_fees(t,self.ttl)
            print(f"minimum fees: {self.min_fee}")
            (pledgeAmount, poolCost, poolMargin) = rsp.get_pledge_params()
            print(f"pledgemount:{pledgeAmount}  poolCost: {poolCost}   poolMargin:{poolMargin}")
            self.rfund = self.lovelace - int(self.min_fee) - pledgeAmount
            print(f"remaining fund:{self.rfund}")
        except Exception as e:
            print(e)        
            
            
    def create_new_pool_cert(self):
        try:
            print("-------------------------Now constructing new pool certificate with new Pledge--------------------------")
            print("-----------------We are taking the pledge from the config file: ./config/pool_stakeData.json------------")

            relay_params = rsp.get_relay_params()
            print(f"relay params are {relay_params}")
            (pledgeAmount, poolCost, poolMargin) = rsp.get_pledge_params()
            print(f"pledgeAmount:{pledgeAmount}  poolCost: {poolCost}   poolMargin:{poolMargin}")
            sp = rsp.RegisterStakePool()
            sp.generate_cert_stakepool(pledgeAmount, poolCost, poolMargin, relay_params)
            #Please note we are not generating the delegation cert as this is already there.

            print("----------------------------------Completed generation of pool certificate------------------------------")
        except Exception as e:
            print("Failed to create new pool certificate")
            print(e)
            
    def submit_new_pool_cert(self):
        try:
            tr = rsp.SubmitStakePool(False) #Note we are not going to submit stake registration fees: 500ADA.
            tr.build_transaction()
            tr.sign_transaction()
            tr.submit_transaction()
        except Exception as e:
            print("Failed to submit the pool registration transaction")
            print(e)
            


def main(lovelace_remaining):
    try:
        a = UpdatePledge(lovelace_remaining)
        a.check_funds_in_wallet()
        
        #First let us do a check of the new pledge amount and check if sufficient funds are present for the transaction.
        #Then we proceed.
        
        if (a.rfund > 0):
            a.create_new_pool_cert()
            a.submit_new_pool_cert()            
        else:
            print("We do not have sufficient fund for the transaction creation. Please ensure that first!")
    except Exception as e:
        print(e)

        
if __name__=="__main__":
    import argparse

    descr="This script is to update the poolpledge"
    
    parser = argparse.ArgumentParser(description=descr, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--lovelace", type=str, required=True,
                        help="Please input current amount of lovelace in the payment.addr. Sample usage: python3 update_poolpledge_v2.py --lovelace 497430545. It uses last utx0 for building transactions")

    args = parser.parse_args()
    print(f"lovelace:{args.lovelace}")

    main(args.lovelace)

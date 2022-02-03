#!/bin/sh

import create_token as ct

class BurnToken:
    def __init__(self, policyid, coin_name, burn_amount):
        self.policyid = policyid
        self.burnamount = burn_amount
        self.coinName = coin_name

    def exec_burn(self):
        t = ct.Transaction(burn=True)
        min_fees = 0 
        t.create_raw_trans(min_fees, -self.burnamount, self.coinName, self.policyid)
        min_fees = t.calculate_min_fees()
        t.create_raw_trans(min_fees, -self.burnamount, self.coinName, self.policyid)
        self.sign_transaction()
        self.submit_transaction()


if __name__ == "__main__":
    policy_id="36296615943a2cba0a971b89f1a59f81928712c13eab3e4943e26086"
    coin_name="REIT"
    burn_amount=45*pow(10,9)        
    
    t = BurnToken(policy_id, coin_name, burn_amount)
    t.exec_burn()

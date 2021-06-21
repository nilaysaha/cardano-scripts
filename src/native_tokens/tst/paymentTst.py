import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
import check_payment_arrival as cpa
import monitor_payment as mp

BASE_ADDR="addr_test1vpyk92350x8gajyefdr44lk5jmjn9f8y4udfxw34pka5pvgjqxw4j"
REFERENCE_POLICY="ee0b053de9262912d43854498bb80c664ae3ea62efaaa6591a25e353"
REFERENCE_TOKEN_NAME="NFT3"

REFERENCE_UUID="3df6dbac-b90b-11eb-82c2-31ea057735b4"

class Testing(unittest.TestCase):
    # def test_payment_arrived(self):
    #     THRESHOLD_AMOUNT=10
    #     t = cpa.PayOrMint(THRESHOLD_AMOUNT)
    #     result = t.check_minted_tokens(REFERENCE_POLICY, REFERENCE_TOKEN_NAME, BASE_ADDR)        
    #     self.assertEqual(result, True)

    # def test_payment_not_arrived(self):
    #     THRESHOLD_AMOUNT=50
    #     t = cpa.PayOrMint(THRESHOLD_AMOUNT)
    #     result = t.check_minted_tokens(REFERENCE_POLICY, REFERENCE_TOKEN_NAME, BASE_ADDR)        
    #     self.assertEqual(result, False)

    def test_monitor_nft_transfer(self):
        amount=1
        policy="06ea4ed6efff368db49ea0c546a01ac12dc7c36ca15c6d6cd6de0744"
        name="NFT1"
        addr=BASE_ADDR
        a=mp.Monitor(REFERENCE_UUID)
        a.transfer_minted_tokens(amount, policy, name, addr)
        

if __name__ == '__main__':
    unittest.main()

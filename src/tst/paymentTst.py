import unittest
import check_payment_arrival as cpa

BASE_ADDR="addr_test1vpyk92350x8gajyefdr44lk5jmjn9f8y4udfxw34pka5pvgjqxw4j"
REFERENCE_POLICY="ee0b053de9262912d43854498bb80c664ae3ea62efaaa6591a25e353"
REFERENCE_TOKEN_NAME="NFT3"

class Testing(unittest.TestCase):
    def test_payment_arrived(self):
        THRESHOLD_AMOUNT=10
        t = cpa.PayOrMint(THRESHOLD_AMOUNT)
        result = t.check_minted_tokens(REFERENCE_POLICY, REFERENCE_TOKEN_NAME, BASE_ADDR)        
        self.assertEqual(result, True)

    def test_payment_not_arrived(self):
        THRESHOLD_AMOUNT=50
        t = cpa.PayOrMint(THRESHOLD_AMOUNT)
        result = t.check_minted_tokens(REFERENCE_POLICY, REFERENCE_TOKEN_NAME, BASE_ADDR)        
        self.assertEqual(result, False)


if __name__ == '__main__':
    unittest.main()

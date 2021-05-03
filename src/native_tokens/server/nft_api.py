from flask import Flask, request
from flask_restful import Resource, Api

import create_nft_token as cnt


app = Flask(__name__)
api = Api(app)

NFTData = {}


class Actions:
    def __init__(self, uuid):
        self.uuid = uuid    
        
    def phase_A(self, name, amount, cost, addr, url):
        """
        output is: {"addr":"", "amount":50}
        """
        sinput = {
            "name": name,
            "amount": amount,
            "payment": cost,
            "dest_addr": addr,
            "metadata":{
                "url": url
            }
        }
        
        output = nft.main_phase_A(self.uuid, sinput)
        return output["addr"]
        

Class NFT(Resource):
    def post(self):
        data = request.get_json()
        assetname = request.form.get('assetName')
        assetamount = request.form.get('assetAmount')
        mintingcost = request.form.get("mintingCost")
        recvaddr    = request.form.get("recvAddr")
        url         = request.form.get("url")
        
        print(f"Asset: {assetname} with amount:{assetamount} costs {mintingcost} ADA with addr:{recvaddr}")
        
        #Now we can call the phase A to create a new entry for this customer
        a = Actions(nft.MUUID)
        payment_addr = a.phase_A(assetname, assetamount, mintingcost, recvaddr, url)
        print("payment address created is:{payment_addr}")
        
        
##
## Actually setup the Api resource routing here
##        
api.add_resource(NFT, '/nft')

if __name__ == '__main__':
    app.run(debug=True)

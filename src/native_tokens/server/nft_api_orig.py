import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from flask import Flask, request, jsonify
from flask_restful import Resource, Api, abort

import uuid 
import create_nft_token as cnt
import queue_task as qt
from waitress import serve



app = Flask(__name__)
api = Api(app)

NFTData = {}

LOCALHOST="127.0.0.1"
PORT=3134

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

        print(f"For phase A we have the input params:{sinput}")
        
        output = cnt.main_phase_A(self.uuid, sinput)
        return output["addr"]
        

class Liveness(Resource):
    def get(self):
        return {"alive": True}
    
class NFT(Resource):    
    def post(self):
        try:
            data = request.get_json()
            print(data)
            assetname = request.form.get('assetName')
            assetamount = request.form.get('assetAmount')
            mintingcost = request.form.get("mintingCost")
            recvaddr    = request.form.get("recvAddr")
            url         = request.form.get("url")
        
            print(f"Asset: {assetname} with amount:{assetamount} costs {mintingcost} ADA with addr:{recvaddr}")
            
            #Now we can call the phase A to create a new entry for this customer
            uuid_str = str(uuid.uuid1())
            a = Actions(uuid_str)
            payment_addr = a.phase_A(assetname, assetamount, mintingcost, recvaddr, url)
            print(f"payment address created is:{payment_addr}")

            #Now push the values to the queue so that it can be picked by the monitoring task
            q = qt.Queue(qt.PLIST)
            q.queue(uuid_str)
            
            return {"payment_addr":payment_addr, "uuid":uuid_str}
        except Exception as e:
            abort(400)
        
##
## Actually setup the Api resource routing here
##
api.add_resource(Liveness, "/")
api.add_resource(NFT, '/nft')

if __name__ == '__main__':
    #app.run(debug=True, host=LOCALHOST, port=PORT)
    serve(app, host=LOCALHOST, port=PORT)

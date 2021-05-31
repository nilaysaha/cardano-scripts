import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from flask import Flask, request, jsonify
from flask_restful import Resource, Api, abort

import uuid 
import create_nft_token as cnt
import queue_task as qt
from waitress import serve

import monitor_payment as mp

app = Flask(__name__)
api = Api(app)

NFTData = {}

LOCALHOST="127.0.0.1"
PORT=3134
MINTING_COST=100

class Actions:
    def __init__(self, uuid):
        self.uuid = uuid    
        
    def phase_A(self, name, amount, cost, addr, url, tags):
        """
        output is: {"addr":"", "amount":50}
        """
        sinput = {
            "name": name,
            "amount": amount,
            "payment": cost,
            "dest_addr": addr,
            "metadata":{
                "url": url,
                "tags": tags
            }
        }

        print(f"For phase A we have the input params:{sinput}")
        
        output = cnt.main_phase_A(self.uuid, sinput)
        return output["addr"]
        

class Liveness(Resource):
    def get(self):
        return {"alive": True}


class NftMonitor(Resource):
    """
    This is to start processing the different steps after payment is done.    
    """
    def post(self):
        try:
            data = request.json
            print(data)

            if "transactionUUID" in data:
                uuid = data["transactionID"]
                print(f"uuid:{uuid}")
            
                a = mp.Monitor(uuid)
                a.main()
            else:
                abort(406, {'message': 'Could not find the uuid to process'})
        except:
            abort(400)

    
class NFT(Resource):    
    def post(self):
        try:
            data = request.json
            print(data)

            if "assetName" in data:
                assetname = data['assetName']
                print(f"assetname:{assetname}")
                
            if "assetAmount" in data:
                assetamount = data['assetAmount']
                print(f"assetamount:{assetamount} " )
                
            if "recvAddr" in data:
                recvaddr    = data["recvAddr"]
                print(f"recvaddr: {recvaddr}" )
            
            if "url" in data:
                url = data["url"]
                print(f"url:{url}" )
            else:
                url = None
            
            if "tags" in data:
                tags = data["tags"]
                print(f"tags:{tags}" )
            else:
                tags = None

            mintingcost = MINTING_COST  #THIS DOES NOT COME FROM THE CLIENT. WE SET THE PRICE !

            print(f"Asset: {assetname} with amount:{assetamount} costs {mintingcost} ADA with addr:{recvaddr}")
            
            #Now we can call the phase A to create a new entry for this customer
            uuid_str = str(uuid.uuid1())
            a = Actions(uuid_str)

            if (assetName != None and  assetAmount != None and recvAddr != None):
                payment_addr = a.phase_A(assetname, assetamount, mintingcost, recvaddr, url, tags)
                print(f"payment address created is:{payment_addr}")
                
                #Now push the values to the queue so that it can be picked by the monitoring task
                # q = qt.Queue(qt.PLIST)
                # q.queue(uuid_str)

                #Now we are shifting to using the RQ wrapper on redis to do stuff.
                q = qt.RQ()
                q.queue(uuid_str)
            
                return {"payment_addr":payment_addr, "uuid":uuid_str, "currency": "ADA", "mintingCost": mintingcost }
            else:
                abort(406) #insufficient params.
        except Exception as e:
            abort(400)
        
##
## Actually setup the Api resource routing here
##
api.add_resource(Liveness, "/")
api.add_resource(NFT, '/nft')
api.add_resource(NftMonitor, '/nft/process')

if __name__ == '__main__':
    #app.run(debug=True, host=LOCALHOST, port=PORT)
    serve(app, host=LOCALHOST, port=PORT)

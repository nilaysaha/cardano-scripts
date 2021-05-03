from flask import Flask, request
from flask_restful import Resource, Api

import nftModel as nftm

app = Flask(__name__)
api = Api(app)

NFTData = {}

class NFT(Resource):
    def post(self):
        data = request.get_json()
        new_nft = nftm.NftModel(data['assetName'],data['assetAmount'],data['mintingCost'], data['recvAddr'])
        db.session.add(new_nft)
        db.session.commit()
        return new_nft.json(),201

        
##
## Actually setup the Api resource routing here
##        
api.add_resource(NFT, '/nft')

if __name__ == '__main__':
    app.run(debug=True)

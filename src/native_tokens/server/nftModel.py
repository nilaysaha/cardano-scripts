from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class NftModel(db.Model):
    __tablename__ = 'nft'

    id = db.Column(db.Integer, primary_key=True)
    assetName   = db.Column(db.String(80))
    assetAmount = db.Column(db.Integer())
    mintingCost = db.Column(db.Integer())
    recvAddr    = db.Column(db.String(80))


    def __init__(self, name, amount, cost, addr):
        self.assetName = name
        self.assetAmount = amount
        self.mintingCost = cost
        self.recvAddr = addr

    def json(self):
        return {
            "assetName": self.assetName,
            "assetAmount": self.assetAmount,
            "mintingCost": self.mintingCost,
            "recvAddr": self.recvAddr
        }

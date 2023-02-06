from ...mongo.connect import ConnectionMongo
import hashlib
# import json
# from bson import json_util, ObjectId

class MongodUser:
    def __init__(self):
        self.connect = ConnectionMongo()

    def userConnect(self, user, pasw):
        db = self.connect.con
        col = db["tbcredenciales"]
        col = col.find_one({"user": user, "pass": pasw, "status": True}, {'_id': False})
        return col
    
    def tbclienteConnect(self, ruc):
        db = self.connect.con
        col = db["tbcliente"]
        col = col.find_one({"ruc": ruc, "status": True}, {'_id': False})
        return col


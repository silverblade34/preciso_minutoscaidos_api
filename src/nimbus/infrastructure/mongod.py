from ...mongo.connect import ConnectionMongo
import hashlib
# import json
import datetime
from bson import json_util, ObjectId

class MongodRutinas:
    def __init__(self):
        self.connect = ConnectionMongo()

    def rutinasConnect(self, fechaIni, fechaFin, ruc, ruta):
        db = self.connect.con
        col = db["report_minutosc"]
        if fechaIni == 0 and fechaFin == 0:
            if ruta != "ALL":
                result = list(col.find({"ruc" : ruc, "ruta" : ruta}))
                return result
            else:
                result = list(col.find({"ruc" : ruc}))
                return result
        elif ruta == "ALL":
            result = list(col.find({"fechaunix": {"$gte": fechaIni, "$lt": fechaFin}, "ruc" : ruc}))
            return result
    
    def consultarRuc(self, token, depot):
        db = self.connect.con
        col = db["tbcliente"]
        result = col.find_one({"token" : str(token), "depot" : str(depot)})
        return result["ruc"]

    def rutinasFilterRuc(self, ruc):
        db = self.connect.con
        col = db["report_minutosc"]
        ahora = datetime.datetime.now()
        fecha_actual = ahora.strftime("%d-%m-%Y")
        result = col.find({"ruc" : ruc, "fecha":fecha_actual},{"_id" : False})
        return result
from src.nimbus.application.response import ResponseNimbus
from ..infrastructure.mongod import MongodRutinas
class NimbusController:
    def __init__(self):
        self.response = ResponseNimbus()
        self.mongodata = MongodRutinas()
    def orderController(self, token, depot):
        dataruc = self.mongodata.consultarRuc(token, depot)
        datamongo = self.mongodata.rutinasFilterRuc(dataruc)
        dataRides = self.response.responseRides(token, depot)
        dataRutina = self.response.parsearRutinaEstatica(datamongo)
        dataOrder = self.response.Order(dataRides, dataRutina)
        return dataOrder
    
    def mostrar_rutinas_mongo(self, fechaIni, fechaFin, ids, ruc):
        datamongo = self.mongodata.rutinasConnect(fechaIni, fechaFin, ids, ruc)
        dataparsed = self.response.responseDataMongo(datamongo)
        return dataparsed
        
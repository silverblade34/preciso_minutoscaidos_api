from src.nimbus.application.response import ResponseNimbus
from ..infrastructure.mongod import MongodRutinas
from src.nimbus.application.request import RequestsData
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
    
    def mostrar_rutinas_mongo(self, fechaIni, fechaFin, ruc, ruta):
        datamongo = self.mongodata.rutinasConnect(fechaIni, fechaFin, ruc, ruta)
        dataparsed = self.response.responseDataMongo(datamongo)
        return dataparsed
    
    def listarRutasEnviar(self, token, depot):
        requests = RequestsData(token, depot)
        data = requests.consumirRutas()
        return data
        
from ..application.request import RequestsData
import json, time
from datetime import datetime
from pymongo import MongoClient
import pymongo

class ResponseNimbus:
    def __init__(self):
        self.indice_color = 0

    def responseRides(self, token, depot):
        # Inicializa las variables en el Request como constructores Header y depot
        requestModule = RequestsData(token, depot)
        print(requestModule)
        [timetables, stops_of_every_routes] = requestModule.get_timetables_per_routes()
        unit_names = requestModule.get_names_of_units()
        stop_names_per_id = requestModule.get_stops_names()
        rides_whole = requestModule.get_rides()
        # * Main data
        whole_rides_result = []
        for ride in rides_whole["rides"]:
            rutina_id = ride["id"]
            unidad_id = ride["u"]
            timetable_id = ride["tid"]
            planned_stops = ride["pt"]
            actual_stops = ride["at"]
            date = ride["d"]
            active = ride["a"]
            flag = ride["f"]
            first_stop = ride["si"]
            status = ride["a"]
            if not (unidad_id is None):
                placa = self.get_name_per_unit(unit_names, unidad_id)
                if len(planned_stops) > 0 and active:
                    if timetable_id in timetables:
                        ride_result = {
                            "id": rutina_id,
                            "plate": self.clean_plate(placa),
                            "route": timetables[timetable_id],
                            "date": date,
                            "range": f"{self.datefromtimestamp(planned_stops[0])} - {self.datefromtimestamp(planned_stops[-1])}",
                            "stops": [],
                            "aditional": {"flag": flag, "first_stop": first_stop, "status": status}
                        }
                        route_stop_ids = stops_of_every_routes[timetables[timetable_id]]
                        for index, stop_id in enumerate(route_stop_ids):
                            parada = {}
                            parada["name"] = f"{index + 1}. {stop_names_per_id[stop_id]}"
                            # parada["status"] = "Hard_Code"
                            parada["differencetime"] = self.get_diff_by_stop(
                                planned_stops[index], actual_stops[index]
                            )
                            # ? Hora:Minuto Planificado
                            if planned_stops[index]:
                                # ? planned time
                                parada["plannedtime"] = self.datefromtimestamp(planned_stops[index])
                            else:
                                parada["plannedtime"] = "--:--"
                            # ? Hora:Minuto Cumplido
                            if actual_stops[index]:
                                # ? actual time
                                parada["actualtime"] = self.datefromtimestamp(actual_stops[index])
                            else:
                                parada["actualtime"] = "--:--"

                            ride_result["stops"].append(parada)
                    whole_rides_result.append(ride_result)
        whole_rides_result = self.order_data(whole_rides_result)
        return whole_rides_result
    
    def get_name_per_unit(self, unit_names, unit_id):
        unit_name = "No se halló"
        for unit in unit_names:
            if unit["id"] == unit_id:
                unit_name = unit["nm"]
                break
        return unit_name
    
    def get_diff_by_stop(self, planned_time, actual_time):
        diff = {"time": "-", "status": 3}
        try:
            pt = int(planned_time)
            at = int(actual_time)
            diff["time"] = "0"
            # diff = 0
            def curr_min(tiemp):
                return int(tiemp - (tiemp % 60))

            if curr_min(pt) > curr_min(at):
                diff["time"] = f"+{int((curr_min(pt) - curr_min(at)) / 60)}"
                diff["status"] = 2
            elif curr_min(pt) < curr_min(at):
                diff["time"] = f"-{int((curr_min(at) - curr_min(pt)) / 60)}"
                diff["status"] = 1
            return diff
        except (TypeError, ValueError):
            return diff

    def clean_plate(self, plate):
        return plate[8:]

    def order_data(self, lista):
        nueva_lista = sorted(lista, key=lambda d: d["range"])
        return nueva_lista

    def datefromtimestamp(self, timestamp):
        date = datetime.utcfromtimestamp(int(timestamp) - 18000).strftime("%H:%M")
        return date
    
    def Order(self, dataRides, dataRutina):
            datas = dataRutina + dataRides
            routes_list = []
            # Con la siguiente iteracion recorre toda las datas, agarra las routes y si no esta almacenada en routes_list, la almacena
            for data in datas:
                if {"route": data["route"]} not in routes_list:
                    routes_list.append({"route": data["route"],})
            # Hasta ahora routes_list tiene la forma: [{"route": RUTA115}, {"route": RUTA15} ...]
            stops_by_route = {}
            for route_list in routes_list:
                stops_by_route[route_list["route"]] = {}
            # Creamos un {"RUTA115" : {}}
            # Recorremos las rutas y agregamos details
            for route_list in routes_list:
                route_list["details"] = [{
                    "plates": [],
                    "datetimes": [],
                    "stops": [],
                    "mins" : []
                }]
                # Ahora tenemos [{"route": RUTA115, "details" : ["plates": [],"datetimes": [],"stops": [],"mins" : []]} ...]
                for data in datas:
                    global indice_color
                    if route_list["route"] == data["route"]:
                        color_capricho = self.change_color_index(self.indice_color)
                        placa = {"color": color_capricho, "plate": data["plate"]}
                        # Se le agrega la placa de la primera rutina "plates": [{"color": 1,"plate": "(07/1746)"}]
                        route_list["details"][0]["plates"].append(placa)
                        #new_format_date = data["date"].split("-")
                        datetime_ = {"color": color_capricho, "datetime": f'{data["range"]}'}
                        # Se le agrega los details "details": [{"color": 0,"datetime": "08:36 - 11:06"}]
                        route_list["details"][0]["datetimes"].append(datetime_)
                        # Recorremos los stops
                        for stop in data["stops"]:
                            if stop["name"] not in stops_by_route[route_list["route"]]:
                                stops_by_route[route_list["route"]][stop["name"]] = {
                                        "plannedtime": [],
                                        "actualtime": [],
                                        "min": []
                                    }
                        for stop in data["stops"]:
                            where_to_save = stops_by_route[route_list["route"]][stop["name"]]
                            where_to_save["plannedtime"].append({"color": color_capricho,"hora": stop["plannedtime"]})
                            where_to_save["actualtime"].append({"color": color_capricho, "hora": stop["actualtime"]})
                            min_dict = {"color": color_capricho, "time": stop["differencetime"]["time"], "state": stop["differencetime"]["status"]}
                            where_to_save["min"].append(min_dict)
                for stops_of_route in stops_by_route[route_list["route"]]:
                    hp = stops_by_route[route_list["route"]][stops_of_route]["plannedtime"]
                    he = stops_by_route[route_list["route"]][stops_of_route]["actualtime"]
                    mi = stops_by_route[route_list["route"]][stops_of_route]["min"]
                    stops_ = {"name": stops_of_route, "hplanificada": hp, "hejecutada": he, "min": mi}
                    route_list["details"][0]["stops"].append(stops_)
                tipocolor = len(route_list["details"][0]["datetimes"])
                if tipocolor % 2 != 0:
                    self.change_color_index(self.indice_color)
                cant_rutinas = [{"color": self.change_color_index(self.indice_color), "minatrasados": 0, "minadelantado" : 0, "sumaminutos":0} for _ in range(len(route_list["details"][0]["stops"][0]["hejecutada"]))]
                for rutinas_p in route_list["details"][0]["stops"]:
                    contm = 0
                    for minutos in rutinas_p["min"]:
                        minsatrasados = 0
                        minsadelantados = 0
                        minutos = minutos["time"]
                        if len(minutos) >= 2  and minutos[0] == "-":
                            minsatrasados = int(minutos)
                        elif len(minutos) >= 2  and minutos[0] == "+":
                            minsadelantados = int(minutos)
                        cant_rutinas[contm]["minatrasados"] = cant_rutinas[contm]["minatrasados"] + minsatrasados
                        cant_rutinas[contm]["minadelantado"] = cant_rutinas[contm]["minadelantado"] + minsadelantados
                        cant_rutinas[contm]["sumaminutos"] = cant_rutinas[contm]["minadelantado"] + cant_rutinas[contm]["minatrasados"]
                        contm += 1
                    
                route_list["details"][0]["mins"] = cant_rutinas
            return routes_list
    
    def change_color_index(self, prueba):
            self.indice_color = prueba
            if self.indice_color == 0:
                self.indice_color = 1 
            elif self.indice_color == 1:
                self.indice_color = 0
            return self.indice_color
                
    def responseDataMongo(self, datamongo):
        datamostrar = []
        sorted_list = sorted(datamongo, key=self.extract_start_time)
        sorted_list2 = sorted(sorted_list, key = self.compare)
        # Aquí se está utilizando la función sorted para ordenar la lista de objetos.
        # La función sorted toma dos argumentos: la lista a ordenar y una función key que especifica el criterio de ordenamiento.
        # En este caso, se está especificando la función extract_start_time como la función key.
        # La función sorted llamará a extract_start_time para cada objeto en la lista y utilizará el valor devuelto para ordenar la lista.
        # Finalmente, la lista ordenada se asigna a la variable sorted_list.
        for rutina in sorted_list2:
            rutinam = {}
            rutinam['id'] = str(rutina['_id'])
            rutinam['placa'] = rutina['placa']
            rutinam['rutina'] = rutina['rutina']
            rutinam['ruta'] = rutina['ruta']
            rutinam['fecha'] = rutina['fecha']
            summinutosatra = 0
            sumaminutosadela = 0
            for parada in rutina['rutinaparadas']:
                if parada["min"][0:1] == "-" and  len(parada["min"]) >= 2:
                    summinutosatra += int(parada["min"])
                elif parada["min"][0:1] == "+" and  len(parada["min"]) >= 2:
                    sumaminutosadela += int(parada["min"])
            rutinam['atrasadostotal'] = str(summinutosatra)
            rutinam['adelantadostotal'] = str(sumaminutosadela)
            rutinam['rutinaparadas'] = rutina['rutinaparadas']
            datamostrar.append(rutinam)
        return datamostrar
    def extract_start_time(self, obj):
        # Esta función toma un objeto de la lista como argumento
        # y devuelve la hora de inicio de la rutina.
        return obj["rutina"].split("-")[0].strip()
    
    def compare(self, obj1):
        date1 = datetime.strptime(obj1["fecha"], "%d-%m-%Y")
        return date1


    def parsearRutinaEstatica(self, datamongo):
        listdata = []
        for rutina in datamongo:
            ahora = datetime.now()
            horaregistro = rutina["rutinaparadas"][-1]["horaejecutada"]
            # Crear un objeto datetime para las 15:56
            hora_registro = datetime(ahora.year, ahora.month, ahora.day, int(horaregistro[:1]), int(horaregistro[3:4]))
            # Calcular la diferencia entre la hora actual y las 15:56
            diferencia = ahora - hora_registro
            if diferencia.total_seconds() >= 720:
                dataparsed = {}
                dataparsed["route"] = rutina["ruta"]
                dataparsed["plate"] = rutina["placa"]
                dataparsed["range"] = rutina["rutina"]
                stops = []
                for parada in rutina["rutinaparadas"]:
                    stop = {}
                    stop["name"] = parada["parada"]
                    stop["plannedtime"] = parada["horaplanificada"]
                    stop["actualtime"] = parada["horaejecutada"]
                    status = 0
                    if parada["min"] == "0" or parada["min"] == "-":
                        status = 3
                    elif len(parada["min"]) >= 2 and parada["min"][0] == "-":
                        status = 1
                    else:
                        status = 2
                    stop["differencetime"] = {"time": parada["min"], "status": status}
                    stops.append(stop)
                dataparsed["stops"] = stops
                listdata.append(dataparsed)
        return listdata
    


    


        




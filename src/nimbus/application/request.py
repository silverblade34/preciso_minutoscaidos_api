import requests

class RequestsData:
    # instance attributes
    def __init__(self, token, depot):
        self.headers = {"Authorization": f"Token {token}"}
        self.depot = depot
        self.token = token 

    def get_rides(self):
        url = f"https://nimbus.wialon.com/api/depot/{self.depot}/rides"
        payload = ""
        headers = self.headers
        response = requests.request("GET", url, data=payload, headers=headers)
        data = response.json()
        return data

    def get_names_of_units(self):
        url_get_sid = "https://hst-api.wialon.com/wialon/ajax.html"
        querystring_for_sid = {
            "svc": "token/login",
            "params": '{"token":"a21e2472955b1cb0847730f34edcf3e83301C4C2D8408F8D941473C73B84C2E6996C4E27","fl":"2"}',
        }
        payload = ""
        response_from_sid = requests.request(
            "GET", url_get_sid, data=payload, params=querystring_for_sid
        )
        result_sid = response_from_sid.json()
        url = "https://hst-api.wialon.com/wialon/ajax.html"
        querystring = {
            "svc": "core/search_items",
            "params": '{"spec":{"itemsType":"avl_unit","propName":"sys_name","propValueMask":"*","sortType":"sys_name",          "propType":"propitemname"  },                "force":1,           "flags":1,           "from":0,           "to":0 }',
            "sid": f"{result_sid['eid']}",
        }   
        payload = ""
        response = requests.request("GET", url, data=payload, params=querystring)
        print(url)
        result = response.json()
        return result["items"]

    # ! timetables and stop_routes
    def get_timetables_per_routes(self):
        url = f"https://nimbus.wialon.com/api/depot/{self.depot}/routes"
        payload = ""
        headers = self.headers
        response = requests.request("GET", url, data=payload, headers=headers)
        result = response.json()
        # ? Ordernar data
        lista = {}
        paradas = {}
        try:
            for route in result["routes"]:
                paradas[route["n"]] = []
                for timetable in route["tt"]:
                    lista[timetable["id"]] = route["n"]
                for stop_route in route["st"]:
                    paradas[route["n"]].append(stop_route["id"])

        except Exception as e:
            raise Exception("Token inservible")

        return [lista, paradas]

    def get_units_per_route(self):
        url = f"https://nimbus.wialon.com/api/depot/{self.depot}/routes"
        payload = ""
        headers = self.headers
        response = requests.request("GET", url, data=payload, headers=headers)
        result = response.json()

        return result

    def get_stops_names(self):
        url = f"https://nimbus.wialon.com/api/depot/{self.depot}/stops"
        payload = ""
        headers = self.headers
        response = requests.request("GET", url, data=payload, headers=headers)
        stops = response.json()
        # ? Order data
        stops = stops["stops"]
        names_per_id = {}
        for stop in stops:
            names_per_id[stop["id"]] = stop["n"]
        return names_per_id
    
    def consumirRutas(self):
        headers={
            "Authorization":f"Token {self.token}"
            }
        response = requests.get(f'https://nimbus.wialon.com/api/depot/{self.depot}/routes', headers=headers)
        raw = response.json()
        routes = raw["routes"]
        listrutas = []
        for ruta in routes:
            if ruta["a"] == True:
                rutaobj = {}
                rutaobj["id"] = ruta["id"]
                rutaobj["n"] = ruta["n"]
                listrutas.append(rutaobj)
        return listrutas


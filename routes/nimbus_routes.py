from decouple import config 
from flask import Flask, request, json, jsonify, send_from_directory
from flask_api import status 
from flask_cors import CORS, cross_origin
# from src.clientes.infrastructure.controller import ClientController
from src.nimbus.infrastructure.controller import NimbusController
from include.validators import parsedRespond, hasErrorMsg, checkArgs, inspectCred, hasErrorMsgToken
#from app import app  -> Nos sirve para gunicorn
#from __main__ import app
from app import app

CORS(app)
# CORS(app, resources={'%s%s/%s' % (config('API_PATH'), config('API_VERSION')): {"origins": "http://localhost"}})

@cross_origin                          
@app.route('%s%s/%s' % (config('API_PATH'), config('API_VERSION'),  'rides_per_route'), methods=["POST"])
def listar_details_minutos():
    try:
        _nimbusCL = NimbusController()
        print("--------------------1")
        data = _nimbusCL.orderController(request.json['token'], request.json['depot'])  
        return parsedRespond(data)
    except Exception as err:
        return hasErrorMsgToken(err)
    
@cross_origin                          
@app.route('%s%s/%s' % (config('API_PATH'), config('API_VERSION'),  'mostrar_rutinas'), methods=["POST"])
def mostrar_rutinas_mongo():
    try:
        _nimbusCL = NimbusController()
        data = _nimbusCL.mostrar_rutinas_mongo(request.json['fechaIni'], request.json['fechaFin'], request.json['ruc'], request.json['ruta'])
        return parsedRespond(data)
    except Exception as err:
        return hasErrorMsg(err)
    
@app.route('%s%s/%s' % (config('API_PATH'), config('API_VERSION'),  'rutas/listar'), methods=["POST"])
def listar_rutas():
    try:
        _nimbusCL = NimbusController()
        data = _nimbusCL.listarRutasEnviar(request.json['token'],request.json['depot'])  
        return parsedRespond(data)
    except Exception as err:
        return hasErrorMsg(err)

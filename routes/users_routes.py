from decouple import config 
from flask import Flask, request, json, jsonify, send_from_directory
from flask_api import status 
from flask_cors import CORS, cross_origin
# from src.clientes.infrastructure.controller import ClientController
from src.users.infrastructure.controller import UserController
from include.validators import parsedRespond, hasErrorMsg, checkArgs, inspectCred, parsedRespond2
#from app import app
from __main__ import app

CORS(app)

@cross_origin                          
@app.route('%s%s/%s' % (config('API_PATH'), config('API_VERSION'),  'login'), methods=["POST"])
def validar_usuario():
    try:
        _userCL = UserController()
        data = _userCL.validarUsuario(request.json['user'], request.json['pass'])
        return parsedRespond2(data)
    except Exception as err:
        return hasErrorMsg(err)

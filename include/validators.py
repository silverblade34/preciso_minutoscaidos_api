from flask import Flask, request, json, jsonify, send_from_directory
import json
from flask_api import status


def parsedRespond(data):
    temp = {
        'data': data,
        'status': True,
        'message': 'ok'
    }
    return jsonify(temp)

def parsedRespond2(data):
    temp = {
        'data': data,
        'status': True,
        'message': 'Usuario Verificado'
    }
    return jsonify(temp)

def hasErrorMsg(err):
    temp = {
        'message': str(err),
        'status': False
    }

    return jsonify(temp), status.HTTP_400_BAD_REQUEST

def hasErrorMsgToken(err):
    temp = {
        'message': "El token se ha vencido",
        'status': False
    }

    return jsonify(temp), status.HTTP_400_BAD_REQUEST

def checkArgs(list, argsx):
    for item in list:
        if item in argsx:
            pass
        else:
            temp = '''No se encuentra el argumento: %s''' % (item)
            raise Exception(temp)


def inspectCred(hds):
    raw_bearer_token = hds.get('Authorization')
    if raw_bearer_token:
        els = raw_bearer_token.split(' ')
        bearer_token = els[1]
        return bearer_token
    else:
        raise Exception("Requiere autentificación")

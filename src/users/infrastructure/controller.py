from .mongod import MongodUser
from ..application.response import UserResponse
import requests

class UserController:
    def __init__(self):
        self.mongo = MongodUser()
        self.response = UserResponse()
        
    def validarUsuario(self, user, pasw):
        raw = self.mongo.userConnect(user, pasw)
        rawcliente = self.mongo.tbclienteConnect(raw['cliente_ruc']) 
        parsed = self.response.parsedUser(rawcliente)
        return parsed
    
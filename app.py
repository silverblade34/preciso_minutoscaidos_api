# from decouple import config
from flask import Flask    
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

import routes.users_routes 
import routes.nimbus_routes


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
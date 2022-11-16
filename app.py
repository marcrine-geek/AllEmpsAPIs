from flask import Flask
from db import db
from config import DevelopmentConfig
from flask_cors import CORS 

from backend.models import UserModel
from flask_restx import Api,fields
from authroute.auth import api as usersReg
from authroute.auth import api2 as authUser

from authroute.auth import Register, Login

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

CORS(app)

api = Api(app, version = "1.0", 
		  title = "AllEmps", 
		  description = "Admin panel",
          doc="/docs")

# adding the namespaces
api.add_namespace(usersReg, path='/api')
api.add_namespace(authUser)

@app.route('/', methods=['GET'])
def hello():
    return "hello"


if __name__ == '__main__':    
    app.run()

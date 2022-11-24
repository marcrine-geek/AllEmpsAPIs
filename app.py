from cmath import log
from flask import Flask
from db import db, mail
from config import DevelopmentConfig
from flask_cors import CORS 
from flask_jwt_extended import JWTManager

from backend.models import UserModel
from backend.models import UserpostsModel

from flask_restx import Api,fields
from routes.routes import api as usersReg
from routes.routes import api2 as authUser

from routes.routes import Register, Login, login_required
from routes.resetPassword import reset_password_namespace
from flask import request

from utils.dto import UserDto

user = UserDto.user

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

mail.init_app(app)

JWTManager(app)

CORS(app)

api = Api(app, version = "1.0", 
		  title = "AllEmps", 
		  description = "Admin panel",
          doc="/docs")

# adding the namespaces
api.add_namespace(usersReg, path='/api')
api.add_namespace(authUser)
api.add_namespace(reset_password_namespace, path='/api/v1/')

@app.route('/', methods=['GET'])
def hello():
    return "hello"
    
if __name__ == '__main__':    
    app.run()

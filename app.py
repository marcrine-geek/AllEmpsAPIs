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

@app.route('/update/user/details', methods=['POST'])
@login_required
def update():
    return "success"

@app.route('/all/users/posts', methods=['GET'])
@login_required
def allposts():
    return "all posts"

@app.route('/update/post', methods=['POST'])
@login_required
def update_post():
    return "updated posts"

@app.route('/remove/post', methods=['DELETE'])
@login_required
def delete_post():
    return "post deleted"

@app.route('/add/member/to/channel', methods=['POST'])
@login_required
def join_channel():
    return "welcome to channel"

@app.route('/users/channel', methods=['GET'])
@login_required
def user_channel():
    return "channels"

@app.route('/members/in/channel', methods=['GET'])
@login_required
def members():
    return "members"

@app.route('/upload/file', methods=['POST'])
@login_required
def upload_file():
    return "file upload"

@app.route('/upload/image', methods=['POST'])
@login_required
def upload_image():
    return "image upload"

@app.route('/follow', methods=['POST'])
@login_required
def follow():
    return "follow member"

@app.route('/unfollow', methods=['DELETE'])
@login_required
def unfollow():
    return "unfollow member"

@app.route('/followers', methods=['GET'])
@login_required
def followers():
    return "followers"
    
if __name__ == '__main__':    
    app.run()

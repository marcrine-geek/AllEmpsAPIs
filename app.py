import os
from flask import Flask, flash, request, redirect, send_file, session, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
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

# upload files and images endpoint
UPLOAD_FOLDER = '/home/marcrine/Documents/AllEmpsAPIs/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/fileupload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # image_path = session.get('UPLOAD_FOLDER', None)
            # return send_file(image_path)
            return redirect(url_for('download_file', name=filename))
  
if __name__ == '__main__':    
    app.run()

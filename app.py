from flask import Flask
from db import db
from config import DevelopmentConfig
from flask_cors import CORS 

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

CORS(app)


@app.route('/', methods=['GET'])
def hello():
    return "hello"

if __name__ == '__main__':    
    app.run()

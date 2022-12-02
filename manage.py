from flask import Flask
from config import DevelopmentConfig
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from db import db
from app import app
from backend.models import UserModel
from backend.models import UserpostsModel
from backend.models import ChannelsModel
from backend.models import ChannelpostsModel
from backend.models import CmembersModel

app.config.from_object(DevelopmentConfig)

db.init_app(app)

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

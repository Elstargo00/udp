import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

SECRET_KEY = os.urandom(32)

app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/elstargo/Documents/allin/udp/migrations/database/dev-all_dics.db'

db = SQLAlchemy(app)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

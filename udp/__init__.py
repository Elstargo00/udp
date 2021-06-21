# udp/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

SECRET_KEY = os.urandom(32)

app.config['SECRET_KEY'] = SECRET_KEY

# database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'dota_match.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)
# # # # # # #

# login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'
# # # # # # #


# import blueprint and register to app
from udp.error_pages.error_handler import error_pages
from udp.cores.views import cores
from udp.users.views import users


app.register_blueprint(error_pages)
app.register_blueprint(cores)
app.register_blueprint(users)
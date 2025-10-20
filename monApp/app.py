from flask import Flask
app = Flask(__name__)
from flask_bootstrap5 import Bootstrap
Bootstrap(app)

#Config options-Make sure you created a 'config.py' file.
app.config.from_object('config')

#Create database connection object
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
db.init_app(app)


# Fait bugger le fichier pour l'instant
"""
from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login"
"""
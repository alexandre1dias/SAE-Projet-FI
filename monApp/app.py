from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap5 import Bootstrap


app = Flask(__name__)
Bootstrap(app)
#Config options-Make sure you created a 'config.py' file.
app.config.from_object('config')

#Create database connection object

db = SQLAlchemy()
db.init_app(app)


# Fait bugger le fichier pour l'instant
"""
from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login"
"""
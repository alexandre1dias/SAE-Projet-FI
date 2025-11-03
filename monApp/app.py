from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap5 import Bootstrap
from .connexionPythonSQL import ouvrir_connexion
from config import LOGIN, PASSWD, SERVEUR, BD


app = Flask(__name__)
Bootstrap(app)
#Config options-Make sure you created a 'config.py' file.
app.config.from_object('config')

#Create database connection object

db = ouvrir_connexion(LOGIN, PASSWD, SERVEUR, BD)



# Fait bugger le fichier pour l'instant
"""
from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login"
"""
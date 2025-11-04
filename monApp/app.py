from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap5 import Bootstrap
from flask_login import LoginManager
from .connexionPythonSQL import ouvrir_connexion
from config import LOGIN, PASSWD, SERVEUR, BD

#Creation de l'app
app = Flask(__name__)

#Ajout de la config
app.config.from_object('config')

#Ajout de extension
db = SQLAlchemy(app)
Bootstrap(app)

#login_manager = LoginManager(app)


#Connexion à la BD avec python (peut etre inutile)
cnx = ouvrir_connexion(LOGIN, PASSWD, SERVEUR, BD)



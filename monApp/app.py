from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap5 import Bootstrap
from flask_login import LoginManager
from config import LOGIN, PASSWD, SERVEUR, BD

#Creation de l'app
app = Flask(__name__)

#Ajout de la config
app.config.from_object('config')

#Ajout de extension
db = SQLAlchemy(app)
Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = "login" # Indique à Flask-Login quelle est la vue de connexion

@login_manager.user_loader
def load_user(user_id):
    """
    Fonction requise par Flask-Login pour charger un utilisateur à partir de son ID.
    Charge un Membre ou un Admin en fonction du 'user_type' stocké dans la session.
    """
    from .modelBD import MembreBD, AdminBD 
    
    # Récupère le type d'utilisateur stocké dans la session
    user_type = session.get('user_type') 
    
    if user_type == 'admin':
        return AdminBD.query.get(int(user_id))
    elif user_type == 'membre':
        return MembreBD.query.get(int(user_id))
    
    return None # Si le type n'est pas défini ou inconnu
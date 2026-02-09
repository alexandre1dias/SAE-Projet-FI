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
from .models import MembreBD, AdminBD 

login_manager = LoginManager(app)
login_manager.login_view = "login" # Indique à Flask-Login quelle est la vue de connexion

@login_manager.user_loader
def load_user(user_id):
    """
    Fonction requise par Flask-Login pour charger un utilisateur à partir de son ID.
    Charge un Membre ou un Admin en fonction du 'user_type' stocké dans la session.
    """
    from .models import MembreBD, AdminBD 

    # Récupère le type d'utilisateur stocké dans la session
    user_type = session.get('user_type') 
    
    # Cas normal : on a le type dans la session
    if user_type == 'admin':
        return AdminBD.query.get(int(user_id))
    elif user_type == 'membre':
        return MembreBD.query.get(int(user_id))
    
    # Cas de secours : Utile pour les tests ou si la session expire mal
    # On cherche d'abord si c'est un admin
    admin = AdminBD.query.get(int(user_id))
    if admin:
        return admin
        
    # Sinon on cherche si c'est un membre
    return MembreBD.query.get(int(user_id))

from . import commands

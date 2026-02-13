from config import ALLOWED_EXTENSIONS
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
import re
from functools import wraps
from .app import app
from flask import session, abort
from flask_login import current_user
from .forms import *
from monApp.models import *

#========================================================#
#====================   Décorateurs  ====================#
#========================================================#
# Décorateur pour vérifier si l'utilisateur est un admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # On vérifie si l'objet current_user est une instance de la classe AdminBD
        if not current_user.is_authenticated or not isinstance(current_user, AdminBD):
            abort(400)  # Déclenche l'erreur "Accès Interdit" Admin
        return f(*args, **kwargs)
    return decorated_function

# Décorateur pour vérifier si l'utilisateur est un membre
def membre_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # On vérifie l'instance MembreBD
        if not current_user.is_authenticated or not isinstance(current_user, MembreBD):
            abort(401)  # Déclenche l'erreur "Accès Interdit" Membre
        return f(*args, **kwargs)
    return decorated_function

# Décorateur pour vérifier si l'utilisateur est un membre du comite ou un admin
def comite_ou_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Liste des status du comite
        statuts_comite = [
            'Président', 'Vice-président', 'Secrétaire Général',
            'Trésorier Général', 'Membre du Comité'
        ]
        # Vérifications basées sur les objets
        is_admin = isinstance(current_user, AdminBD)
        is_comite_membre = (
            isinstance(current_user, MembreBD) and
            current_user.statut in statuts_comite
        )
        if not (current_user.is_authenticated and (is_admin or is_comite_membre)):
            abort(405)  # Déclenche l'erreur "Accès Interdit"
        return f(*args, **kwargs)
    return decorated_function

#======================================================#
#====================   Fonctions  ====================#
#======================================================#
# Définir les extensions de fichiers autorisées
def allowed_file(filename):
    """Vérifie si l'extension du fichier est autorisée."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Vérificateur de mot de passe, vérifie si le mot de passe est complexe
def est_mot_de_passe_fort(password):
    # Vérifie la longueur (min 8 caractères)
    if len(password) < 8:
        return False
    # Vérifie la présence d'au moins une minuscule
    if not re.search(r"[a-z]", password):
        return False
    # Vérifie la présence d'au moins une majuscule
    if not re.search(r"[A-Z]", password):
        return False
    # Vérifie la présence d'au moins un chiffre
    if not re.search(r"[0-9]", password):
        return False
    # Vérifie la présence d'au moins un caractère spécial (!@#$%^&*)
    if not re.search(r"[ !@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True

# fonction pour récupérer un utilisateur (Membre ou Admin) par email
def get_user_by_email(email):
    return MembreBD.query.filter_by(email=email).first() or AdminBD.query.filter_by(email=email).first()

# fonction pour simuler l'envoi d'email
def simuler_envoi_email(email, link):
    print("\n" + "="*50)
    print(f"SIMULATION D'ENVOI D'EMAIL À : {email}")
    print(f"LIEN : {link}")
    print("="*50 + "\n")

# initialisation de Flask-Mail et du Serializer pour les tokens
# variables de config MAIL_* sont définies dans app.config
mail = Mail(app)
# source : https://stackoverflow.com/questions/34043847/forcing-itsdangerous-urlsafetimedserializer-to-give-old-signature
s = URLSafeTimedSerializer(app.config.get('SECRET_KEY', 'default-secret-key'))

# Injecter les notifications dans tous les templates
@app.context_processor
def inject_notifications():
    unread_count = 0
    notifications_list = []
    if current_user.is_authenticated:
        user_type = session.get('user_type')
        if user_type == 'membre':
            query = NotifsBD.query.filter_by(idMembre=current_user.id)
        elif user_type == 'admin':
            query = NotifsBD.query.filter_by(idAdmin=current_user.id)
        else:
            query = None

        if query:
            unread_count = query.filter_by(lue=False).count()
            notifications_list = query.order_by(NotifsBD.timestamp.desc()).limit(10).all()

    return dict(unread_count=unread_count, notifications_list=notifications_list)
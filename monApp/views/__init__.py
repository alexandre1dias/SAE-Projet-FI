from flask import Blueprint
from .authentifications_views import auth_bp
from .generals_views import general_bp
from .articles_views import articles_bp
from .competitions_views import competitions_bp
from .calendrier_views import calendrier_bp
from .evenenents_club_views import events_club_bp
from .reunions_views import reunions_bp
from .profil_membre_views import profil_bp
from .parametres_views import parametres_bp
from .notifications_views import notifications_bp
from .menu_admin_views import admin_bp

# Liste de tous les blueprints à enregistrer
all_blueprints = [
    auth_bp,
    general_bp,
    articles_bp,
    competitions_bp,
    calendrier_bp,
    events_club_bp,
    reunions_bp,
    profil_bp,
    parametres_bp,
    notifications_bp,
    admin_bp
]

def register_blueprints(app):
    """
    Enregistre tous les blueprints dans l'application Flask
    """
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)
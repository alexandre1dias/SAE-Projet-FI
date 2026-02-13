from flask import Blueprint, render_template
from monApp.app import db

erreurs_bp = Blueprint('erreurs', __name__)

#==========================================================#
#====================   Pages Erreur   ====================#
#==========================================================#

@erreurs_bp.app_errorhandler(404)
def page_not_found(e):
    # Le fichier gestion_erreur.html est à la racine de templates
    return render_template('gestion_erreur.html',
                           error_code=404,
                           error_title="Page non trouvée",
                           error_message="Désolé, la page que vous cherchez n'existe pas ou a été déplacée."), 404

@erreurs_bp.app_errorhandler(500)
def internal_server_error(e):
    db.session.rollback()
    return render_template('gestion_erreur.html',
                           error_code=500,
                           error_title="Erreur interne du serveur",
                           error_message="Une erreur inattendue s'est produite. Notre équipe technique a été notifiée."), 500

@erreurs_bp.app_errorhandler(403)
def forbidden_access(e):
    return render_template('gestion_erreur.html',
                           error_code=403,
                           error_title="Accès Interdit",
                           error_message="Vous n'avez pas les autorisations nécessaires pour accéder à cette page."), 403

@erreurs_bp.app_errorhandler(400)
def admin_access(e):
    return render_template('gestion_erreur.html',
                           error_code=400,
                           error_title="Accès Interdit",
                           error_message="Cette page est réservée au compte de type Admin"), 400

@erreurs_bp.app_errorhandler(401)
def membre_access(e):
    return render_template('gestion_erreur.html',
                           error_code=401,
                           error_title="Accès Interdit",
                           error_message="Cette page est réservée au compte de type Membre"), 401

@erreurs_bp.app_errorhandler(405)
def comite_access(e):
    return render_template('gestion_erreur.html',
                           error_code=405,
                           error_title="Accès Interdit",
                           error_message="Cette page est réservée au membre du comité"), 405

@erreurs_bp.app_errorhandler(410)
def page_prive(e):
    return render_template('gestion_erreur.html',
                           error_code=410,
                           error_title="Accès Interdit",
                           error_message="Cette page est privée, vous ne pouvez pas y accéder"), 410
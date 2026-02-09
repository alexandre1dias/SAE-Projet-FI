from .app import app, db
from flask import render_template




#==========================================================#
#====================   Pages Erreur   ====================#
#==========================================================#
# Page d'erreur pour les ressources non trouvées (404).
@app.errorhandler(404)
def page_not_found(e):
    return render_template('gestion_erreur.html',
                           error_code=404,
                           error_title="Page non trouvée",
                           error_message="Désolé, la page que vous cherchez n'existe pas ou a été déplacée."), 404

# Page d'erreur pour les erreurs internes du serveur (500).
@app.errorhandler(500)
def internal_server_error(e):
    db.session.rollback()
    return render_template('gestion_erreur.html',
                           error_code=500,
                           error_title="Erreur interne du serveur",
                           error_message="Une erreur inattendue s'est produite. Notre équipe technique a été notifiée."), 500

# Page d'erreur pour les accès interdits (403).
@app.errorhandler(403)
def forbidden_access(e):
    return render_template('gestion_erreur.html',
                           error_code=403,
                           error_title="Accès Interdit",
                           error_message="Vous n'avez pas les autorisations nécessaires pour accéder à cette page."), 403

# Page d'erreur spécifique pour les accès réservés aux administrateurs (400).
@app.errorhandler(400)
def admin_access(e):
    return render_template('gestion_erreur.html',
                           error_code=400,
                           error_title="Accès Interdit",
                           error_message="Cette page est réservé au compte de type Admin"), 400

# Page d'erreur spécifique pour les accès réservés aux membres (401).
@app.errorhandler(401)
def membre_access(e):
    return render_template('gestion_erreur.html',
                           error_code=401,
                           error_title="Accès Interdit",
                           error_message="Cette page est réservé au compte de type Membre"), 401

# Page d'erreur spécifique pour les accès réservés au comité (405).
@app.errorhandler(405)
def comite_access(e):
    return render_template('gestion_erreur.html',
                           error_code=405,
                           error_title="Accès Interdit",
                           error_message="Cette page est réservé au membre du comité"), 405

@app.errorhandler(410)
def page_prive(e):
    return render_template('gestion_erreur.html',
                           error_code=410,
                           error_title="Accès Interdit",
                           error_message="Cette page esyt privée, vous ne pouvez pas y acceder"), 410
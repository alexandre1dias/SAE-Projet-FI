from flask import Blueprint, render_template, request, url_for, redirect, session, flash, jsonify, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date
from sqlalchemy import or_
import shutil
import os

from monApp.app import app, db
from monApp.forms import *
from monApp.models import *
from monApp.services import *
from monApp.gestion_erreurs import *
from config import TITLE, AUJOURDHUI

# Création du Blueprint
notifications_bp = Blueprint('notifications', __name__)

#==================================================================#
#====================   Routes Notifications   ====================#
#==================================================================#
# Route pour marquer une notification comme lue et rediriger vers son lien
@notifications_bp.route("/read_notification/<int:id_notif>")
@login_required
def read_notification(id_notif):
    notif = NotifsBD.query.get_or_404(id_notif)
    if session.get('user_type') == 'membre':
        if notif.idMembre != current_user.id:
            abort(403)
    elif session.get('user_type') == 'admin':
        if notif.idAdmin != current_user.id:
            abort(403)
    else:
        abort(403)
    notif.lue = True
    db.session.commit()
    target_url = request.referrer or url_for('general.index')
    if notif.link and notif.link != '#':
        if notif.link.startswith('#'):
            base_target = target_url.split('#')[0]
            return redirect(base_target + notif.link) 
        return redirect(notif.link)
    return redirect(target_url)

# Route pour supprimer une notification
@notifications_bp.route("/delete_notification/<int:id_notif>", methods=['POST'])
@login_required
def delete_notification(id_notif):
    notif = NotifsBD.query.get_or_404(id_notif)
    # Vérification que la notif appartient bien à l'utilisateur connecté
    if session.get('user_type') == 'membre':
        if notif.idMembre != current_user.id:
            abort(403)
    elif session.get('user_type') == 'admin':
        if notif.idAdmin != current_user.id:
            abort(403)
    else:
        abort(403)

    # Supprimer les dépendances dans les tables de liaison avant de supprimer la notification
    # Cela évite l'erreur IntegrityError car la cascade n'est pas configurée en SQL
    db.session.execute(recevoir_a.delete().where(recevoir_a.c.idNotifs == id_notif))
    db.session.execute(recevoir_m.delete().where(recevoir_m.c.idNotifs == id_notif))

    db.session.delete(notif)
    db.session.commit()
    return redirect(request.referrer or url_for('general.index'))
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
reunions_bp = Blueprint('reunions', __name__)

#====================   Pages Reunions   ====================#
# Page affichant toutes les réunions - Réservée à Admin et Membre du Comité.
@reunions_bp.route("/reunion/")
@reunions_bp.route("/reunion/<string:etat>")
@login_required
@comite_ou_admin_required
def reunion(etat="prochaine"):
    passee = (etat == "passees")
    filtre = FiltreForm(request.args if request.args else None)
    page = request.args.get('page', 1, type=int)
    filtre.tri.choices = [('date_desc', 'Plus récent'),
                          ('date_asc', 'Plus ancien')]
    lesReunions = ReunionBD.query
    if passee:
        lesReunions = lesReunions.filter(ReunionBD.dateFinRE < AUJOURDHUI)
    else:
        lesReunions = lesReunions.filter(ReunionBD.dateDebutRE >= AUJOURDHUI)
    if filtre.tri.data == "date_asc":
        lesReunions = lesReunions.order_by(ReunionBD.dateDebutRE.asc())
    else:
        lesReunions = lesReunions.order_by(ReunionBD.dateDebutRE.desc())
    pagination = lesReunions.paginate(page=page, per_page=6, error_out=False)
    ids_evenements_inscrits = set()
    if current_user.is_authenticated and session.get('user_type') == 'membre':
        participations = ParticiperBD.query.filter_by(
            id_membre=current_user.id).all()
        ids_evenements_inscrits = {p.id_event for p in participations}

    return render_template("reunion.html",
                           title=TITLE + "- Réunions",
                           pagination=pagination,
                           filtre=filtre,
                           passee=passee,
                           user_registered_event_ids=ids_evenements_inscrits)

# Page de consultation d'une réunion - Réservée à Admin et Membres du Comité.
@reunions_bp.route("/reunion/consultation/<int:idReunion>")
@login_required
@comite_ou_admin_required
def reunion_view(idReunion):
    reunion = ReunionBD.query.get(idReunion)
    origine = request.args.get('origine', 'default')
    return render_template("reunion_view.html",title=TITLE+"- Consultatiion d'une réunion", selectedReunion = reunion, origine=origine)

# Vue de suppression d'une réunion - Réservée aux administrateurs.
@reunions_bp.route("/reunion/delete/<int:idReunion>", methods=['POST'])
@login_required
@admin_required
def reunion_delete(idReunion):
    reunion = ReunionBD.query.get_or_404(idReunion)
    db.session.delete(reunion)
    db.session.commit()
    return redirect(url_for('reunions.reunion'))

# Vue d'inscription à une réunion - Réservée aux membres du comité et aux admins.
@reunions_bp.route("/reunion/inscrire/<int:idReunion>", methods=['GET'])
@login_required
@comite_ou_admin_required
def inscrire_reunion(idReunion):
    reunion_objet = ReunionBD.query.get_or_404(idReunion)
    id_evenement_a_inscrire = reunion_objet.idEvent
    try:
        nouvelle_participation = ParticiperBD(id_membre=current_user.id,
                                                id_event=id_evenement_a_inscrire)
        db.session.add(nouvelle_participation)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    return redirect(url_for('reunions.reunion'))

# Vue de désinscription d'une réunion - Réservée aux membres du comité et aux admins.
@reunions_bp.route("/reunion/desinscrire/<int:idReunion>", methods=['GET'])
@login_required
@comite_ou_admin_required
def desinscrire_reunion(idReunion):
    reunion_objet = ReunionBD.query.get_or_404(idReunion)
    id_evenement = reunion_objet.idEvent
    participation = ParticiperBD.query.filter_by(id_membre=current_user.id, id_event=id_evenement).first()
    if participation:
        try:
            db.session.delete(participation)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    return redirect(url_for('reunions.reunion'))

# Page de modification d'une réunion - Réservée à l'Admin.
@reunions_bp.route("/reunion/update/<int:idReunion>", methods=['GET', 'POST'])
@login_required
@admin_required
def reunion_update(idReunion):
    reunion = ReunionBD.query.get_or_404(idReunion)
    if request.method == 'POST':
        reunion.nom = request.form['nom']
        reunion.typeReunionRE = request.form['type_reunion']
        reunion.ville = request.form['ville']
        reunion.adresse = request.form['adresse']
        reunion.rapportRE = request.form['description']
        # Mettre à jour les dates et heures
        reunion.dateDebutRE = datetime.strptime(request.form['date_debut'], '%Y-%m-%d').date()
        reunion.heureDebutRE = request.form['heure_debut']
        reunion.dateFinRE = datetime.strptime(request.form['date_fin'], '%Y-%m-%d').date()
        reunion.heureFinRE = request.form['heure_fin']
        db.session.commit()
        return redirect(url_for('reunions.reunion_view', idReunion=reunion.id))
    return render_template("reunion_update.html", title=TITLE + "- Modification d'une réunion", reunion=reunion)
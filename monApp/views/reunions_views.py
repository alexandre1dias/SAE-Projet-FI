from flask import Blueprint, render_template, request, url_for, redirect, session
from flask_login import login_required, current_user
from datetime import datetime, date

from monApp.app import db
from monApp.forms import FiltreForm
from monApp.models import ReunionBD, ParticiperBD
from monApp.services import admin_required, comite_ou_admin_required
from config import TITLE, AUJOURDHUI

reunions_bp = Blueprint('reunions', __name__)

#====================   Pages Reunions   ====================#


@reunions_bp.route("/reunion/")
@reunions_bp.route("/reunion/<string:etat>")
@login_required
@comite_ou_admin_required
def reunion(etat="prochaine"):
    passee = (etat == "passees")
    filtre = FiltreForm(request.args if request.args else None)
    page = request.args.get('page', 1, type=int)
    dates_bd = db.session.query(ReunionBD.dateDebutRE).distinct().all()
    annees_set = set()
    for (d,) in dates_bd:
        if d:
            annee_debut = d.year if d.month >= 8 else d.year - 1
            annees_set.add(
                (str(annee_debut), f"{annee_debut}-{annee_debut + 1}"))
    if annees_set:
        choix_tries = sorted(list(annees_set), key=lambda x: x[0], reverse=True)
        filtre.annee_scolaire.choices = choix_tries
        if filtre.annee_scolaire.data not in [c[0] for c in choix_tries]:
            filtre.annee_scolaire.data = choix_tries[0][0]
    annee_selectionnee = filtre.annee_scolaire.data
    lesReunions = ReunionBD.query
    if annee_selectionnee:
        try:
            an_debut = int(annee_selectionnee)
            debut_saison = date(an_debut, 8, 1)
            fin_saison = date(an_debut + 1, 7, 31)
            lesReunions = lesReunions.filter(
                ReunionBD.dateDebutRE >= debut_saison, ReunionBD.dateDebutRE
                <= fin_saison)
        except (ValueError, TypeError):
            pass
    filtre.tri.choices = [('date_desc', 'Plus récent'),
                          ('date_asc', 'Plus ancien')]
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
    return render_template("reunions/reunion.html",
                           title=TITLE + "- Réunions",
                           pagination=pagination,
                           filtre=filtre,
                           passee=passee,
                           user_registered_event_ids=ids_evenements_inscrits)


@reunions_bp.route("/reunion/consultation/<int:idReunion>")
@login_required
@comite_ou_admin_required
def reunion_view(idReunion):
    reunion = ReunionBD.query.get(idReunion)
    origine = request.args.get('origine', 'default')
    return render_template("reunions/reunion_view.html",
                           title=TITLE + "- Consultatiion d'une réunion",
                           selectedReunion=reunion,
                           origine=origine)


@reunions_bp.route("/reunion/delete/<int:idReunion>", methods=['POST'])
@login_required
@admin_required
def reunion_delete(idReunion):
    reunion = ReunionBD.query.get_or_404(idReunion)
    db.session.delete(reunion)
    db.session.commit()
    return redirect(url_for('reunions.reunion'))


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
    except Exception:
        db.session.rollback()

    return redirect(url_for('reunions.reunion'))


@reunions_bp.route("/reunion/desinscrire/<int:idReunion>", methods=['GET'])
@login_required
@comite_ou_admin_required
def desinscrire_reunion(idReunion):
    reunion_objet = ReunionBD.query.get_or_404(idReunion)
    id_evenement = reunion_objet.idEvent
    participation = ParticiperBD.query.filter_by(id_membre=current_user.id,
                                                 id_event=id_evenement).first()
    if participation:
        try:
            db.session.delete(participation)
            db.session.commit()
        except Exception:
            db.session.rollback()
    return redirect(url_for('reunions.reunion'))


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

        reunion.dateDebutRE = datetime.strptime(request.form['date_debut'],
                                                '%Y-%m-%d').date()
        reunion.heureDebutRE = request.form['heure_debut']
        reunion.dateFinRE = datetime.strptime(request.form['date_fin'],
                                              '%Y-%m-%d').date()
        reunion.heureFinRE = request.form['heure_fin']
        db.session.commit()
        return redirect(url_for('reunions.reunion_view', idReunion=reunion.id))
    return render_template("reunions/reunion_update.html",
                           title=TITLE + "- Modification d'une réunion",
                           reunion=reunion)

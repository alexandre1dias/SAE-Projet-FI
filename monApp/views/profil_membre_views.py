from flask import Blueprint, render_template, request, url_for, redirect, session, abort
from flask_login import login_required, current_user
from sqlalchemy import or_

from monApp.app import db
from monApp.forms import FiltreForm
from monApp.models import ResultatBD, CompetitionBD, ParticiperBD, ReunionBD, EventClubBD, MembreBD
from monApp.services import membre_required
from config import TITLE, AUJOURDHUI

# Création du Blueprint
profil_bp = Blueprint('profil', __name__)

#==========================================================#
#====================   Pages Profil   ====================#
#==========================================================#

@profil_bp.route("/resultat_membre/")
@login_required
@membre_required
def resultat_membre():
    filtre = FiltreForm(request.args if request.args else None)
    page = request.args.get('page', 1, type=int)
    filtre.tri.choices = [('date_desc', 'Plus récent'),
                          ('date_asc', 'Plus ancien'),
                          ('resultat', 'Resultat')]
    lesCompete = ResultatBD.query.join(CompetitionBD).filter(
        ResultatBD.id_membre == current_user.id)
    if filtre.armes.data:
        lesCompete = lesCompete.filter(
            CompetitionBD.type_arme.in_(filtre.armes.data))

    if filtre.type_competition.data:
        lesCompete = lesCompete.filter(
            CompetitionBD.typeComp.in_(filtre.type_competition.data))
    if filtre.tri.data == "date_asc":
        lesCompete = lesCompete.order_by(CompetitionBD.date_debut.asc())
    elif filtre.tri.data == "resultat":
        lesCompete = lesCompete.order_by(ResultatBD.resultat.asc())
    else:
        lesCompete = lesCompete.order_by(CompetitionBD.date_debut.desc())

    pagination = lesCompete.paginate(page=page, per_page=8, error_out=False)
    return render_template("profils_membre/resultat_membre.html",
                           title=TITLE + "- Résultat du Membre",
                           resultats=pagination.items,
                           pagination=pagination,
                           filtre=filtre)

@profil_bp.route("/evenement_membre/")
@login_required
@membre_required
def evenement_membre():
    filtre = FiltreForm(request.args if request.args else None)
    page = request.args.get('page', 1, type=int)
    type_page = request.args.get('type', 'competitions')
    etat = request.args.get('etat', 'avenir')
    filtre.tri.choices = [('date_desc', 'Plus récent'),
                          ('date_asc', 'Plus ancien')]
    query = None
    if type_page == 'competitions':
        query = CompetitionBD.query.join(
            ParticiperBD,
            CompetitionBD.id_event == ParticiperBD.id_event).filter(
                ParticiperBD.id_membre == current_user.id)
        if etat == 'passees':
            query = query.filter(CompetitionBD.date_debut < AUJOURDHUI)
        else:
            query = query.filter(CompetitionBD.date_debut >= AUJOURDHUI)

        if filtre.armes.data:
            query = query.filter(CompetitionBD.type_arme.in_(
                filtre.armes.data))

        if filtre.type_competition.data:
            query = query.filter(
                CompetitionBD.typeComp.in_(filtre.type_competition.data))

        if filtre.recherche.data:
            terme = f"%{filtre.recherche.data}%"
            query = query.filter(
                or_(CompetitionBD.nom.ilike(terme),
                    CompetitionBD.ville.ilike(terme)))
        if filtre.tri.data == 'date_asc':
            query = query.order_by(CompetitionBD.date_debut.asc())
        elif filtre.tri.data == 'nom':
            query = query.order_by(CompetitionBD.nom.asc())
        else:
            query = query.order_by(CompetitionBD.date_debut.desc())
    elif type_page == 'reunions':
        query = ReunionBD.query.join(
            ParticiperBD, ReunionBD.idEvent == ParticiperBD.id_event).filter(
                ParticiperBD.id_membre == current_user.id)

        if etat == 'passees':
            query = query.filter(ReunionBD.dateDebutRE < AUJOURDHUI)
        else:
            query = query.filter(ReunionBD.dateDebutRE >= AUJOURDHUI)

        if filtre.recherche.data:
            terme = f"%{filtre.recherche.data}%"
            query = query.filter(ReunionBD.nom.ilike(terme))

        if filtre.tri.data == 'date_asc':
            query = query.order_by(ReunionBD.dateDebutRE.asc())
        else:
            query = query.order_by(ReunionBD.dateDebutRE.desc())
    elif type_page == 'event_club':
        query = EventClubBD.query.join(
            ParticiperBD,
            EventClubBD.id_event == ParticiperBD.id_event).filter(
                ParticiperBD.id_membre == current_user.id)
        if etat == 'passees':
            query = query.filter(EventClubBD.dateDebutEV < AUJOURDHUI)
        else:
            query = query.filter(EventClubBD.dateDebutEV >= AUJOURDHUI)

        if filtre.recherche.data:
            terme = f"%{filtre.recherche.data}%"
            query = query.filter(EventClubBD.NomEV.ilike(terme))

        if filtre.tri.data == 'date_asc':
            query = query.order_by(EventClubBD.dateDebutEV.asc())
        else:
            query = query.order_by(EventClubBD.dateDebutEV.desc())
    else:
        return redirect(url_for('profil.evenement_membre', type='competitions'))
    pagination = query.paginate(page=page, per_page=8, error_out=False)
    return render_template("profils_membre/evenement_membre.html",
                           title=TITLE + "- Vos Évènements",
                           pagination=pagination,
                           type_page=type_page,
                           etat=etat,
                           filtre=filtre)


@profil_bp.route("/profil_view/<int:idM>")
@login_required 
def profil_view(idM):
    if not session.get("user_type") == "admin":
        if current_user.id != idM:
            abort(410)
    origine = request.args.get('origine', 'gerer_profils')
    id_competition = request.args.get('idCompetition', type=int)
    id_event_club = request.args.get('idEventClub', type=int)
    unMembre = db.session.get(MembreBD,idM)
    return render_template("profils_membre/profil_view.html", title=TITLE + "- Profil Membre", selectedMembre=unMembre, origine=origine, idCompetition=id_competition, idEventClub=id_event_club)
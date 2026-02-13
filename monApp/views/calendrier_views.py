from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from flask_login import login_required, current_user
from monApp.app import db
from monApp.forms import FiltreForm, EventForm
from monApp.models import CompetitionBD, ReunionBD, EventClubBD, EntrainementBD, EvenementBD, MembreBD, AdminBD, ParticiperBD
from monApp.services import admin_required
from config import TITLE

calendrier_bp = Blueprint('calendrier', __name__)

#====================   Pages Calendrier   ====================#

@calendrier_bp.route("/calendrier/")
def calendrier():
    filtre = FiltreForm(request.args if request.args else None)
    return render_template("calendrier/calendrier.html", title=TITLE+"- Calendrier", filtre=filtre)

@calendrier_bp.route('/api/events')
def get_events():
    sexes = request.args.getlist('sexe')
    niveaux = request.args.getlist('niveau')
    armes = request.args.getlist('armes')
    type_competition = request.args.getlist('type_competition')
    types_event = request.args.getlist('type_event')

    all_events = []

    # Compétitions
    if not types_event or 'Compétition' in types_event:
        query_comp = CompetitionBD.query
        if armes:
            query_comp = query_comp.filter(CompetitionBD.type_arme.in_(armes))
        if sexes:
            query_comp = query_comp.filter(CompetitionBD.sexe.in_(sexes))
        if type_competition:
            query_comp = query_comp.filter(CompetitionBD.typeComp.in_(type_competition))
        if niveaux:
            query_comp = query_comp.filter(CompetitionBD.niveaux.in_(niveaux))

        for event in query_comp.all():
            all_events.append({
                'id': f"comp_{event.id}",
                'title': event.nom,
                'start': f"{event.date_debut.isoformat()}T{event.heure_debut}",
                'end': f"{event.date_fin.isoformat()}T{event.heure_fin}",
                'color': '#007bff',
                'extendedProps': {
                    'url': url_for('competitions.competition_view', idCompetition=event.id, origine='calendrier'),
                    'type': 'Compétition',
                    'description': event.description,
                    'niveaux': event.niveaux,
                    'arme': event.type_arme
                }
            })

    # Réunions
    if not types_event or 'Réunion' in types_event:
        voir_reunions = False
        if current_user.is_authenticated:
            if isinstance(current_user, AdminBD):
                voir_reunions = True
            elif isinstance(current_user, MembreBD):
                statuts_comite = [
                    'Président', 'Vice-président', 'Vice-Président',
                    'Secrétaire Général', 'Trésorier Général', 'Membre du Comité'
                ]
                if current_user.statut in statuts_comite:
                    voir_reunions = True

        if voir_reunions:
            for event in ReunionBD.query.all():
                all_events.append({
                    'id': f"reunion_{event.id}",
                    'title': event.nom,
                    'start': f"{event.dateDebutRE.isoformat()}T{event.heureDebutRE}",
                    'end': f"{event.dateFinRE.isoformat()}T{event.heureFinRE}" if event.dateFinRE and event.heureFinRE else None,
                    'color': '#ffc107',
                    'extendedProps': {
                        'url': url_for('reunions.reunion_view', idReunion=event.id, origine='calendrier'),
                        'type': 'Réunion',
                        'description': event.rapportRE
                    }
                })

    # Event Club
    if not types_event or 'Évènement du club' in types_event:
        if current_user.is_authenticated:
            query_club = EventClubBD.query
            for event in query_club.all():
                all_events.append({
                    'id': f"club_{event.idEventClub}",
                    'title': event.NomEV,
                    'start': f"{event.dateDebutEV.isoformat()}T{event.heureDebutEV}",
                    'end': f"{event.dateFinEV.isoformat()}T{event.heureFinEV}",
                    'color': '#28a745',
                    'extendedProps': {
                        'url': url_for('events_club.club_view', idEventClub=event.idEventClub, origine='calendrier'),
                        'type': 'Événement du Club',
                        'description': event.descriptionEV,
                        'niveaux': event.niveauxEV
                    }
                })

    # Entrainement
    if not types_event or 'Entrainement' in types_event:
        for event in EntrainementBD.query.all():
            all_events.append({
                'id': f"entrainement_{event.id}",
                'title': f"Entraînement {event.niveau} {event.type_arme}",
                'start': f"{event.date.isoformat()}T{event.heure_debut}",
                'end': f"{event.date.isoformat()}T{event.heure_fin}",
                'color': '#dc3545',
                'extendedProps': {
                    'type': 'Entraînement',
                    'description': f"Jour: {event.jour}",
                    'niveaux': event.niveau,
                    'arme': event.type_arme,
                    'ville': event.ville,
                    'adresse': event.adresse
                }
            })
    return jsonify(all_events)

@calendrier_bp.route("/add_event/", methods=["GET", "POST"])
@login_required
@admin_required
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        try:
            new_event = EvenementBD()
            db.session.add(new_event)
            db.session.commit()

            event_id = new_event.id
            category = form.category.data

            if category == 'Compétition':
                new_specific_event = CompetitionBD(
                    id_event=event_id,
                    nom=form.title.data,
                    date_debut=form.start_date.data.date(),
                    heure_debut=form.start_date.data.time().strftime('%H:%M'),
                    date_fin=form.end_date.data.date(),
                    heure_fin=form.end_date.data.time().strftime('%H:%M'),
                    description=form.description.data,
                    niveaux=", ".join(form.level.data),
                    sexe=form.sexe.data,
                    type_arme=form.arme.data,
                    typeComp=form.type.data,
                    passee=False,
                    ville=form.ville.data,
                    adresse=form.adresse.data
                )
            elif category == 'Réunion':
                new_specific_event = ReunionBD(
                    idEvent=event_id,
                    nom=form.title.data,
                    dateDebutRE=form.start_date.data.date(),
                    heureDebutRE=form.start_date.data.time().strftime('%H:%M'),
                    dateFinRE=form.end_date.data.date(),
                    heureFinRE=form.end_date.data.time().strftime('%H:%M'),
                    ville=form.ville.data,
                    adresse=form.adresse.data,
                    typeReunionRE=form.type_reunion.data if form.type_reunion.data else "Générale"
                )
                statuts_comite = ['Président', 'Vice-président', 'Vice-Président', 'Secrétaire Général', 'Trésorier Général', 'Membre du Comité']
                membres_comite = MembreBD.query.filter(MembreBD.statut.in_(statuts_comite)).all()
                for membre in membres_comite:
                    participation = ParticiperBD(id_membre=membre.id, id_event=event_id)
                    db.session.add(participation)
            elif category == 'Evenement du club':
                new_specific_event = EventClubBD(
                    id_event=event_id,
                    NomEV=form.title.data,
                    dateDebutEV=form.start_date.data.date(),
                    heureDebutEV=form.start_date.data.time().strftime('%H:%M'),
                    dateFinEV=form.end_date.data.date(),
                    heureFinEV=form.end_date.data.time().strftime('%H:%M'),
                    descriptionEV=form.description.data,
                    niveauxEV=", ".join(form.level.data),
                    passeeEV=False,
                    villeEV=form.ville.data,
                    adresseEV=form.adresse.data
                )
            elif category == 'Entraînement':
                new_specific_event = EntrainementBD(
                    id_event=event_id,
                    date=form.start_date.data.date(),
                    heure_debut=form.start_date.data.time().strftime('%H:%M'),
                    heure_fin=form.end_date.data.time().strftime('%H:%M'),
                    type_arme=form.arme.data,
                    niveau=", ".join(form.level.data),
                    jour=form.start_date.data.strftime('%A'),
                    ville=form.ville.data,
                    adresse=form.adresse.data
                )
            db.session.add(new_specific_event)
            db.session.commit()
            return redirect(url_for('calendrier.calendrier'))
        except Exception:
            db.session.rollback()
    return render_template("calendrier/add_event.html", title=TITLE + "- Ajouter un événement", form=form)
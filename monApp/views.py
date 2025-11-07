from .app import app, db
from flask import render_template, request, url_for, redirect, session, abort
from config import TITLE, AUJOURDHUI
from flask_login import logout_user, login_user, login_required, current_user
from .forms import *
from .connexionPythonSQL import *
from monApp.modelBD import *
from flask import jsonify
from functools import wraps
from datetime import datetime

# Décorateur pour vérifier si l'utilisateur est un admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or session.get('user_type') != 'admin':
            abort(400)  # Déclenche l'erreur "Accès Interdit" Admin
        return f(*args, **kwargs)
    return decorated_function

# Décorateur pour vérifier si l'utilisateur est un membre
def membre_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or session.get('user_type') != 'membre':
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
        # Premiere condition: verifie si admin
        is_admin = (session.get('user_type') == 'admin')
        # Deuxieme condition: verifie si comite
        is_comite_membre = (
            session.get('user_type') == 'membre' and
            current_user.statut in statuts_comite
        )
        #Verification
        if not (current_user.is_authenticated and (is_admin or is_comite_membre)):
            abort(405)  # Déclenche l'erreur "Accès Interdit" Comite
        return f(*args, **kwargs)
    return decorated_function


#==========================================================#
#====================   Page Accueil   ====================#
#==========================================================#
@app.route("/")
@app.route("/index/")
def index():
    les_derniers_articles = PresseBD.query.order_by(PresseBD.dateP.desc()).limit(3).all()
    les_dernieres_informations = InformationBD.query.order_by(InformationBD.dateIN.desc()).limit(3).all()
    les_dernieres_competitions = CompetitionBD.query.filter_by(passee=True).order_by(CompetitionBD.date_debut.desc()).limit(3).all()
    return render_template("index.html", title = TITLE, articles=les_derniers_articles, informations=les_dernieres_informations, competitions=les_dernieres_competitions)

#==================================================================#
#====================   Pages Renseignements   ====================#
#==================================================================#
@app.route("/adresse/")
def adresse():
    return render_template("adresse.html",title=TITLE+"- Adresse")

@app.route("/horaires/")
def horaires():
    return render_template("horaire.html",title=TITLE+"- Horaires")

@app.route("/adhesions/")
def adhesions():
    return render_template("adhesion.html",title=TITLE+"- Adhésions")

@app.route("/materiel/")
def materiel():
    return render_template("materiel.html",title=TITLE+"- Matériel et tenues")

#==================================================================#
#====================   Pages Escrim feminin   ====================#
#==================================================================#
@app.route("/escrime-feminin/")
def escrime_feminin():
    return render_template("escrime_feminin.html",title=TITLE+"- L'escrime Féminin")


#==============================================================#
#====================   Pages Evenements   ====================#
#==============================================================#

#====================   Pages Calendrier   ====================#
@app.route("/calendrier/")
def calendrier():
    return render_template("calendrier.html", title=TITLE+"- Calendrier")

@app.route('/api/events')
def get_events():
    all_events = []
    query_comp = CompetitionBD.query.filter(db.or_(CompetitionBD.passee == False, CompetitionBD.passee == None))
    for event in query_comp.all():
        all_events.append({
            'id': f"comp_{event.id}",
            'title': event.nom,
            'start': f"{event.date_debut.isoformat()}T{event.heure_debut}",
            'end': f"{event.date_fin.isoformat()}T{event.heure_fin}",
            'color': '#007bff',
            'extendedProps': {
                'url': url_for('competition_view', idCompetition=event.id, origine='calendrier'),
                'type': 'Compétition',
                'description': event.description,
                'niveaux': event.niveaux,
                'arme': event.type_arme
            }
        })
    for event in ReunionBD.query.all():
        all_events.append({
            'id': f"reunion_{event.id}",
            'title': event.nom,
            'start': f"{event.dateDebutRE.isoformat()}T{event.heureDebutRE}",
            'end': f"{event.dateFinRE.isoformat()}T{event.heureFinRE}" if event.dateFinRE and event.heureFinRE else None,
            'color': '#ffc107',
            'extendedProps': {
                'url': url_for('reunion_view', idReunion=event.id, origine='calendrier'),
                'type': 'Réunion',
                'description': event.rapportRE,
                'niveaux': event.niveauRE
            }
        })
    query_club = EventClubBD.query.filter(db.or_(EventClubBD.passeeEV == False, EventClubBD.passeeEV == None))
    for event in query_club.all():
        all_events.append({
            'id': f"club_{event.idEventClub}",
            'title': event.NomEV,
            'start': f"{event.dateDebutEV.isoformat()}T{event.heureDebutEV}",
            'end': f"{event.dateFinEV.isoformat()}T{event.heureFinEV}",
            'color': '#28a745',
            'extendedProps': {
                'url': url_for('club_view', idEventClub=event.idEventClub, origine='calendrier'),
                'type': 'Événement du Club',
                'description': event.descriptionEV,
                'niveaux': event.niveauxEV
            }
        })
    for event in EntrainementBD.query.all():
        all_events.append({
            'id': f"entrainement_{event.id}",
            'title': f"Entraînement {event.niveau} {event.type_arme}",
            'start': f"{event.date.isoformat()}T{event.heure_debut}",
            'end': f"{event.date.isoformat()}T{event.heure_fin}",
            'color': '#dc3545',
            'extendedProps': {
                'type': 'Entraînement',
                'description': f"Lieu: {event.ville}, Jour: {event.jour}",
                'niveaux': event.niveau,
                'arme': event.type_arme
            }
        })
    return jsonify(all_events)

@app.route("/add_event/", methods=["GET", "POST"])
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
                    niveauRE=", ".join(form.level.data),
                    ville=form.ville.data,
                    adresse=form.adresse.data
                )
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
            return redirect(url_for('calendrier'))
        except Exception as e:
            db.session.rollback()
    return render_template("add_event.html", title=TITLE + "- Ajouter un événement", form=form)


#====================   Pages Competitions   ====================#
@app.route("/competitions/")
def competitions():
    lesCompetitions = CompetitionBD.query.all()
    lesCompetitions.sort(key=lambda x: x.date_debut, reverse=True)
    
    #events_a_venir = [e for e in evenements if (getattr(e, 'date_debut', None) or getattr(e, 'dateDebutRE', None) or getattr(e, 'dateDebutEV', None)) >= AUJOURDHUI]
    #events_passes = [e for e in evenements if (getattr(e, 'date_fin', None) or getattr(e, 'dateFinRE', None) or getattr(e, 'dateFinEV', None)) < AUJOURDHUI]
    return render_template("competitions.html", title=TITLE+"- Competitions", competitions=lesCompetitions)

@app.route("/competitions/<int:idCompetition>/view")
def competition_view(idCompetition):
    uneCompetition = CompetitionBD.query.get(idCompetition)
    origine = request.args.get('origine', 'default')
    deja_inscrit = False
    est_eligible = False
    if current_user.is_authenticated and session.get('user_type') == 'membre':
        participation = ParticiperBD.query.filter_by(
            id_membre=current_user.id, 
            id_event=uneCompetition.id_event
        ).first()
        deja_inscrit = participation is not None
        membre_niveau = current_user.niveau
        competition_niveaux = uneCompetition.niveaux
        surclassement_map = {'M9': 'M11', 'M11': 'M13', 'M13': 'M15', 'M15': 'M17','M17': 'M20', 'M20': 'Senior', 'Senior': 'Vétéran'}
        surclassement_niveau = surclassement_map.get(membre_niveau)
        if competition_niveaux:
            niveaux_liste = competition_niveaux.split(',')
            if membre_niveau in niveaux_liste:
                est_eligible = True
            elif surclassement_niveau and surclassement_niveau in niveaux_liste:
                est_eligible = True
    resultats = ResultatBD.query.filter_by(id_competition=idCompetition).all()
    resultats.sort(key=lambda x: x.resultat)
    return render_template("competition_view.html",title=TITLE+"- Consultation de la competition",competition=uneCompetition,origine=origine,deja_inscrit=deja_inscrit,est_eligible=est_eligible, lesResultats = resultats)

@app.route("/inscrire/competition/<int:idCompetition>", methods=['GET'])
@login_required
@membre_required
def inscrire_competition(idCompetition):
    competition_obj = CompetitionBD.query.get_or_404(idCompetition)
    id_evenement_a_inscrire = competition_obj.id_event
    deja_inscrit = ParticiperBD.query.filter_by(
        id_membre=current_user.id,
        id_event=id_evenement_a_inscrire
    ).first()
    try:
        nouvelle_participation = ParticiperBD(id_membre=current_user.id, id_event=id_evenement_a_inscrire)
        db.session.add(nouvelle_participation)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('competition_view', idCompetition=idCompetition))

@app.route("/desinscrire/competition/<int:idCompetition>", methods=['GET'])
@login_required
def desinscrire_competition(idCompetition):
    competition_obj = CompetitionBD.query.get_or_404(idCompetition)
    participation = ParticiperBD.query.filter_by(id_membre=current_user.id, id_event=competition_obj.id_event).first()
    if participation:
        try:
            db.session.delete(participation)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    return redirect(url_for('competition_view', idCompetition=idCompetition))

@app.route("/competition_update/<int:idCompetition>", methods=['GET', 'POST'])
@login_required
@admin_required
def competition_update(idCompetition):
    competition = CompetitionBD.query.get_or_404(idCompetition)
    origine = request.args.get('origine', 'default')
    if request.method == 'POST':
        try:
            competition.nom = request.form['nom']
            competition.ville = request.form['ville']
            competition.adresse = request.form['adresse']
            competition.date_debut = datetime.strptime(request.form['date_debut'], '%Y-%m-%d').date()
            competition.heure_debut = request.form['heure_debut']
            competition.date_fin = datetime.strptime(request.form['date_fin'], '%Y-%m-%d').date()
            competition.heure_fin = request.form['heure_fin']
            competition.type_arme = request.form['type_arme']
            competition.sexe = request.form['sexe']
            competition.description = request.form['description']
            db.session.commit()
            return redirect(url_for('competition_view', idCompetition=competition.id, origine=origine))
        except Exception as e:
            db.session.rollback()
    # Récupérer la liste des participants
    participations = ParticiperBD.query.filter_by(id_event=competition.id_event).all()
    participants = [p.membre for p in participations]

    return render_template("competition_update.html",title=TITLE+"- Modification de la competition", competition=competition, lesParticipants = participants, origine=origine)

@app.route("/competition/<int:idCompetition>/classer/<int:idMembre>", methods=['POST'])
@login_required
@admin_required
def classer_membre(idCompetition, idMembre):
    competition = CompetitionBD.query.get_or_404(idCompetition)
    classement = request.form.get('classement')
    if not classement:
        return redirect(url_for('competition_update', idCompetition=idCompetition))
    
    if not classement.isdigit():
        return redirect(url_for('competition_update', idCompetition=idCompetition))
    
    resultat_existant = ResultatBD.query.filter_by(id_competition=idCompetition,id_membre=idMembre).first()
    if resultat_existant:
        resultat_existant.resultat = classement
    else:
        nouveau_resultat = ResultatBD(resultat=classement, date=competition.date_fin, type_arme=competition.type_arme, type_compete=competition.typeComp, id_competition=idCompetition, id_membre=idMembre)
        db.session.add(nouveau_resultat)
    db.session.commit()

    
    return redirect(url_for('competition_update', idCompetition=idCompetition))

@app.route("/competition/<int:idC>/delete/<int:idM>", methods=['POST'])
@login_required
@admin_required
def delete_membre_competition(idC, idM):
    competition = CompetitionBD.query.get_or_404(idC)
    participation = ParticiperBD.query.filter_by(id_event=competition.id_event, id_membre=idM).first_or_404()
    try:
        db.session.delete(participation)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('competition_update', idCompetition=idC))
    
@app.route("/competition_delete/<int:idCompetition>", methods=['POST'])
@login_required # Assure que seul un utilisateur connecté peut supprimer
@admin_required
def competition_delete(idCompetition):
    competition_a_supprimer = CompetitionBD.query.get_or_404(idCompetition)
    id_event_parent = competition_a_supprimer.id_event
    try:
        ParticiperBD.query.filter_by(id_event=id_event_parent).delete()
        db.session.delete(competition_a_supprimer)
        if id_event_parent:
            evenement_parent = EvenementBD.query.get(id_event_parent)
            if evenement_parent:
                db.session.delete(evenement_parent)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('competitions'))

#====================   Pages Evenement du club   ====================#
@app.route("/evenement_club/")
def evenement_club():
    lesEventClubs = EventClubBD.query.all()
    ids_evenements_inscrits = set()
    if current_user.is_authenticated and session.get('user_type') == 'membre':
        participations = ParticiperBD.query.filter_by(id_membre=current_user.id).all()
        ids_evenements_inscrits = {p.id_event for p in participations}
    return render_template("evenement_club.html",title=TITLE+"- Evenements du Club",eventsclub=lesEventClubs, user_registered_event_ids=ids_evenements_inscrits)

@app.route("/evenement_club/<int:idEventClub>/club_view/")
def club_view(idEventClub):
    unEventClub = EventClubBD.query.get(idEventClub)
    origine = request.args.get('origine', 'default')

    deja_inscrit = False
    if current_user.is_authenticated and session.get('user_type') == 'membre':
        participation = ParticiperBD.query.filter_by(id_membre=current_user.id, id_event=unEventClub.id_event).first()
        deja_inscrit = participation is not None
    return render_template("club_view.html",title=TITLE+"- un évenement du club",selectedEventClub=unEventClub, deja_inscrit=deja_inscrit, origine=origine)

 
@app.route("/evenement_club/<int:idEventClub>/club_update/", methods=['GET', 'POST'])
@login_required
@admin_required
def club_update(idEventClub):
    unEventClub = EventClubBD.query.get_or_404(idEventClub)

    if request.method == 'POST':
        try:
            unEventClub.NomEV = request.form['nom']
            unEventClub.adresseEV = request.form['lieu']
            unEventClub.descriptionEV = request.form['description']
            unEventClub.dateDebutEV = datetime.strptime(request.form['date_debut'], '%Y-%m-%d').date()
            unEventClub.heureDebutEV = request.form['heure_debut']
            unEventClub.dateFinEV = datetime.strptime(request.form['date_fin'], '%Y-%m-%d').date()
            unEventClub.heureFinEV = request.form['heure_fin']
            db.session.commit()
            return redirect(url_for('club_view', idEventClub=unEventClub.idEventClub))
        except Exception as e:
            db.session.rollback()
    participations = ParticiperBD.query.filter_by(id_event=unEventClub.id_event).all()
    participants = [p.membre for p in participations]
    lesMembres = MembreBD.query.all()
    nonParticipant = list(set(lesMembres) - set(participants))
    membreAInscrire = []
    return render_template("club_update.html",title=TITLE+"- Modification d'un évenement du club", eventClub=unEventClub, participants=participants , nonParticipant=nonParticipant, membreAInscrire = membreAInscrire)

@app.route("/evenement_club/<int:idEventClub>/club_update/incrire_membres", methods=['GET', 'POST'])
@login_required
@admin_required
def incrire_membres_event_club(idEventClub, membreAInscrire):
    for membre in membreAInscrire:
        evenement_club_obj = EventClubBD.query.get_or_404(idEventClub)
        id_evenement_a_inscrire = evenement_club_obj.id_event
        nouvelle_participation = ParticiperBD(id_membre=membre.id, id_event=id_evenement_a_inscrire)
        db.session.add(nouvelle_participation)
    db.session.commit()
    return redirect(url_for('club_update', idEventClub=idEventClub))
            
 
        

@app.route("/evenement_club/<int:idEventClub>/delete/<int:idM>", methods=['POST'])
@login_required
@admin_required
def delete_membre_eventClub(idEventClub, idM):
    eventClub = EventClubBD.query.get_or_404(idEventClub)
    participation = ParticiperBD.query.filter_by(id_event=eventClub.id_event, id_membre=idM).first_or_404()
    try:
        db.session.delete(participation)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('club_update', idEventClub=idEventClub))

@app.route("/evenement_club/<int:idEventClub>/club_delete/", methods=['POST'])
@login_required
@admin_required
def club_delete(idEventClub):
    evenement_a_supprimer = EventClubBD.query.get_or_404(idEventClub)
    db.session.delete(evenement_a_supprimer)
    db.session.commit()
    return redirect(url_for('evenement_club'))

@app.route("/inscrire/club/<int:idEventClub>", methods=['GET'])
@login_required
@membre_required
def inscrire_club(idEventClub):
    evenement_club_obj = EventClubBD.query.get_or_404(idEventClub)
    id_evenement_a_inscrire = evenement_club_obj.id_event

    deja_inscrit = ParticiperBD.query.filter_by(
        id_membre=current_user.id,
        id_event=id_evenement_a_inscrire
    ).first()
    try:
        nouvelle_participation = ParticiperBD(id_membre=current_user.id, id_event=id_evenement_a_inscrire)
        db.session.add(nouvelle_participation)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('club_view', idEventClub=idEventClub))

@app.route("/desinscrire/club/<int:idEventClub>", methods=['GET'])
@login_required
@membre_required
def desinscrire_club(idEventClub):
    evenement_club_obj = EventClubBD.query.get_or_404(idEventClub)
    participation = ParticiperBD.query.filter_by(id_membre=current_user.id, id_event=evenement_club_obj.id_event).first()
    if participation:
        db.session.delete(participation)
        db.session.commit()
    return redirect(url_for('club_view', idEventClub=idEventClub))


#====================   Pages Reunions   ====================#
#Page affichant toutes les réunions - Reservée à Admin et Membre du Comité
@app.route("/reunion/")
@login_required
@comite_ou_admin_required
def reunion():
    reunions = ReunionBD.query.all()
    aujourdhui = datetime.now().date()
    prochaines_reunions = [r for r in reunions if r.dateDebutRE and r.dateDebutRE >= aujourdhui]
    anciennes_reunions = [r for r in reunions if r.dateFinRE and r.dateFinRE < aujourdhui]
    ids_evenements_inscrits = set()
    if current_user.is_authenticated and session.get('user_type') == 'membre':
        participations = ParticiperBD.query.filter_by(id_membre=current_user.id).all()
        ids_evenements_inscrits = {p.id_event for p in participations}
    return render_template("reunion.html", title=TITLE + "- Réunion", prochaines_reunions=prochaines_reunions, anciennes_reunions=anciennes_reunions,user_registered_event_ids = ids_evenements_inscrits)

#Page de consultation d'une réunion - Reservée à Admin et Membres du Comité
@app.route("/reunion/consultation/<int:idReunion>")
@login_required
@comite_ou_admin_required
def reunion_view(idReunion):
    reunion = ReunionBD.query.get(idReunion)
    origine = request.args.get('origine', 'default')
    return render_template("reunion_view.html",title=TITLE+"- Consultatiion d'une réunion", selectedReunion = reunion, origine=origine)

#Vue de suppression d'une réunion - Reservée à Admin et Membres du Comité
@app.route("/reunion/delete/<int:idReunion>", methods=['POST'])
@login_required
@admin_required
def reunion_delete(idReunion):
    reunion = ReunionBD.query.get_or_404(idReunion)
    db.session.delete(reunion)
    db.session.commit()
    return redirect(url_for('reunion'))

#Vue d'inscription d'une réunion - Reservée aux Membres du Comité
@app.route("/reunion/inscrire/<int:idReunion>", methods=['GET'])
@login_required
@comite_ou_admin_required
def inscrire_reunion(idReunion):
    reunion_objet = ReunionBD.query.get_or_404(idReunion)
    id_evenement_a_inscrire = reunion_objet.idEvent
    deja_inscrit = ParticiperBD.query.filter_by(
        id_membre=current_user.id,
        id_event=id_evenement_a_inscrire
    ).first()
    try:
        nouvelle_participation = ParticiperBD(id_membre=current_user.id,
                                                id_event=id_evenement_a_inscrire)
        db.session.add(nouvelle_participation)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('reunion'))

#Vue de d'inscription d'une réunion - Reservée aux Membres du Comité
@app.route("/reunion/desinscrire/<int:idReunion>", methods=['GET'])
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
    return redirect(url_for('reunion'))

#Page d'update d'une réunion - Reservée  à l'Admin
@app.route("/reunion/update/<int:idReunion>", methods=['GET', 'POST'])
@login_required
@admin_required
def reunion_update(idReunion):
    reunion = ReunionBD.query.get_or_404(idReunion)
    if request.method == 'POST':
        reunion.nom = request.form['nom']
        reunion.ville = request.form['ville']
        reunion.adresse = request.form['adresse']
        reunion.rapportRE = request.form['description']
        # Mettre à jour les dates et heures
        reunion.dateDebutRE = datetime.strptime(request.form['date_debut'], '%Y-%m-%d').date()
        reunion.heureDebutRE = request.form['heure_debut']
        reunion.dateFinRE = datetime.strptime(request.form['date_fin'], '%Y-%m-%d').date()
        reunion.heureFinRE = request.form['heure_fin']
        db.session.commit()
        return redirect(url_for('reunion_view', idReunion=reunion.id))
    return render_template("reunion_update.html", title=TITLE + "- Modification d'une réunion", reunion=reunion)


#==============================================================#
#====================   Pages Actualités   ====================#
#==============================================================#
#Vues pour Informations
@app.route("/informations/")
def informations():
    lesInformations = InformationBD.query.all()
    return render_template("informations.html",title=TITLE+"- Informations",informations=lesInformations)

#Vues pour Presse
@app.route("/presse/")
def presse():
    lesArticles = PresseBD.query.all()
    return render_template("presse.html",title=TITLE+"- Presse",articles = lesArticles)


#============================================================#
#====================   Pages A propos   ====================#
#============================================================#

@app.route("/about/")
def about():
    return render_template("about.html",title=TITLE+"- A propos")

@app.route("/historique/")
def historique():
    return render_template("historique.html",title=TITLE+"- Historique") 

@app.route("/comite_cercle/")
def comite_cercle():
    return render_template("comite_cercle.html",title=TITLE+"- Comité directeur du Cercle")

#==========================================================#
#====================   Page Contact   ====================#
#==========================================================#
@app.route("/contact/", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            nouveau_message = FormulaireBD(
                type=form.type_form.data,
                sujet=form.sujet.data,
                email=form.email.data,
                description=form.description.data,
                date=datetime.now().date(),
                repondu=False
            )
            db.session.add(nouveau_message)
            db.session.commit()
            return redirect(url_for('contact'))
        except Exception as e:
            db.session.rollback()
    return render_template("contact.html", title=TITLE+"- Contact", form=form)


#==========================================================#
#====================   Pages Profil   ====================#
#==========================================================#

@app.route("/resultat_membre/")
@login_required
@membre_required
def resultat_membre():
    les_resultats = ResultatBD.query.filter_by(id_membre=current_user.id).all()
    return render_template("resultat_membre.html", title=TITLE+"- Résultat du Membre", resultats=les_resultats)

@app.route("/evenement_membre/")
@login_required
@membre_required
def evenement_membre():
    participations = ParticiperBD.query.filter_by(id_membre=current_user.id).all()
    ids_evenements = [p.id_event for p in participations]

    evenements = []
    if ids_evenements:
        les_competitions = CompetitionBD.query.filter(CompetitionBD.id_event.in_(ids_evenements)).all()
        les_reunions = ReunionBD.query.filter(ReunionBD.idEvent.in_(ids_evenements)).all()
        les_evenements_club = EventClubBD.query.filter(EventClubBD.id_event.in_(ids_evenements)).all()
        evenements.extend(les_competitions)
        evenements.extend(les_reunions)
        evenements.extend(les_evenements_club)

    events_a_venir = [e for e in evenements if (getattr(e, 'date_debut', None) or getattr(e, 'dateDebutRE', None) or getattr(e, 'dateDebutEV', None)) >= AUJOURDHUI]
    events_passes = [e for e in evenements if (getattr(e, 'date_fin', None) or getattr(e, 'dateFinRE', None) or getattr(e, 'dateFinEV', None)) < AUJOURDHUI]


    return render_template("evenement_membre.html", title=TITLE+"- Vos Évènements",
                           events_a_venir=events_a_venir, events_passes=events_passes)

@app.route("/profil_view/<int:idM>")
def profil_view(idM):
    # origine corresponds à l'origine de l'utilisateur. 
    origine = request.args.get('origine', 'gerer_profils')
    id_competition = request.args.get('idCompetition', type=int)
    id_event_club = request.args.get('idEventClub', type=int)
    unMembre = db.session.get(MembreBD,idM)
    return render_template("profil_view.html", title=TITLE + "- Profil Membre", selectedMembre=unMembre, origine=origine, idCompetition=id_competition, idEventClub=id_event_club)

#==============================================================#
#====================   Pages Menu Admin   ====================#
#==============================================================#
@app.route("/gerer_formulaires/")
@login_required
@admin_required
def gerer_formulaires():
    les_formulaires = FormulaireBD.query.order_by(FormulaireBD.date.desc()).filter(FormulaireBD.repondu == False).all()
    les_formulaires.sort(key=lambda x: x.date, reverse=True) 
    return render_template("gerer_formulaires.html", title=TITLE+"- Géstion des Formulaires", formulaires=les_formulaires)

@app.route("/gerer_anciens_formulaires/")
@login_required
@admin_required
def gerer_anciens_formulaires():
    les_formulaires = FormulaireBD.query.order_by(FormulaireBD.date.desc()).filter(FormulaireBD.repondu == True).all()
    return render_template("gerer_anciens_formulaires.html", title=TITLE+"- Géstion des Anciens Formulaires", formulaires=les_formulaires)

@app.route("/formulaire_view/<int:idFormulaire>")
@login_required
@admin_required
def formulaire_view(idFormulaire):
    unFormulaire = FormulaireBD.query.get_or_404(idFormulaire)
    return render_template("formulaire_view.html",title=TITLE+"- Consultation de Formulaire", selectedFormulaire=unFormulaire)

@app.route("/formulaire_delete/<int:idFormulaire>", methods=['POST'])
@login_required
@admin_required
def formulaire_delete(idFormulaire):
    formulaire = FormulaireBD.query.get_or_404(idFormulaire)
    db.session.delete(formulaire)
    db.session.commit()
    return redirect(url_for('gerer_anciens_formulaires'))

@app.route("/repondre_formulaire/<int:idFormulaire>", methods=['POST'])
@login_required
@admin_required
def repondre_formulaire(idFormulaire):
    reponse = request.form.get('reponse')
    leFormulaire = FormulaireBD.query.get_or_404(idFormulaire)
    
    #Logique d'envoi d'email à ajouter ici
    # Par exemple : send_email(to=formulaire.email, subject=f"Re: {leFormulaire.sujet}", body=reponse)
    #une fois la réponse envoyée, on supprime le formulaire
    leFormulaire.reponse = reponse
    leFormulaire.repondu = True
    db.session.commit()
    return redirect(url_for('gerer_formulaires'))

#Vue pour la gestion des Profils
@app.route("/gerer_profils/")
@login_required
@admin_required
def gerer_profils():
    lesMembres = db.session.query(MembreBD).filter(MembreBD.activite == True).all()
    lesMembres.sort(key=lambda x: x.date_inscription, reverse=True) 
    return render_template("gerer_profils.html",title=TITLE+"- Géstion des Profils", membres = lesMembres)

@app.route ('/gerer_profils/desinscrire/<int:idM>', methods =("POST" ,))
@login_required
@admin_required
def desinscrireMembre(idM):
    membre = db.session.get(MembreBD, idM)
    membre.activite = False
    db.session.commit()
    return redirect(url_for('gerer_profils'))

@app.route ('/gerer_anciens_profils/reinscrire/<int:idM>', methods =("POST" ,))
@login_required
@admin_required
def reinscrireMembre(idM):
    membre = db.session.get(MembreBD, idM)
    membre.activite = True
    db.session.commit()
    return redirect(url_for('gerer_ancien_profils'))


@app.route("/gerer_profils/ancien/")
@login_required
@admin_required
def gerer_ancien_profils():
    lesMembres = db.session.query(MembreBD).filter(MembreBD.activite == False).all() 
    return render_template("gerer_ancien_profils.html",title=TITLE+"- Géstion des Anciens Profils", membres = lesMembres)

@app.route("/profil_edit/<int:idM>", methods=["GET", "POST"])
@login_required
def profil_edit(idM):
    unMembre = db.session.get(MembreBD,idM)
    unForm = ModifForm(obj=unMembre)
    origine = request.args.get('origine', 'profil')

    if unForm.validate_on_submit():
        action = request.form.get('submit_action')
        if action == 'admin_save':
            unForm.populate_obj(unMembre)
            db.session.commit()
            return redirect(url_for('gerer_profils'))
        elif action == 'membre_request':
            uneModif = unMembre.modifications.first()
            if not uneModif:
                uneModif = ModifBD(id_membre=idM)
                db.session.add(uneModif)
            uneModif.nom = unForm.nom.data
            uneModif.prenom = unForm.prenom.data
            uneModif.email = unForm.email.data
            uneModif.sexe = unForm.sexe.data
            uneModif.ddn = unForm.ddn.data
            uneModif.date = datetime.now()
            uneModif.justification = unForm.justification.data
            db.session.commit()
            return redirect(url_for('profil_view', idM=unMembre.id, origine='profil'))
    return render_template("profil_edit.html", title=TITLE + "- Modifier Profil", selectedMembre=unMembre, updateForm = unForm, origine = origine)

@app.route('/profil_edit/<int:idM>/desinscrit/', methods=["GET", "POST"])
@login_required
def desinscrit_profil(idM):
    membreDesinscrit = db.session.get(MembreBD, idM)
    membreDesinscrit.activite = False
    db.session.commit()
    return redirect(url_for('gerer_profils'))

@app.route('/profil_edit/<int:idM>/reinscrit/')
def reinscrit_profil(idM):
    membreReinscrit = db.session.get(MembreBD, idM)
    membreReinscrit.activite = True
    db.session.commit()
    return redirect(url_for('gerer_ancien_profils'))

#Vue pour la gestion des inscription/modification
@app.route("/gerer_inscriptions/")
@login_required
@admin_required
def gerer_inscriptions():
    lesInscriptions = db.session.query(InscriptionBD).all()
    lesModifs = db.session.query(ModifBD).all()
    lesRequetes = lesInscriptions + lesModifs
    # Trie par date de la liste
    lesRequetes.sort(key=lambda x: x.date, reverse=True)  
    return render_template("gerer_inscriptions.html",title=TITLE+"- Géstion des Inscriptions", requetes=lesRequetes)

@app.route ('/accepter_inscription/<int:idI>', methods =("POST" ,))
@login_required
@admin_required
def accepter_inscription(idI):
    inscription = db.session.get(InscriptionBD, idI)
    nouveauMembre = MembreBD(
        nom=inscription.nom,
        prenom=inscription.prenom,
        email=inscription.email,
        ddn=inscription.ddn,
        sexe=inscription.sexe,
        mdp_hash=inscription.mdp_hash
    )
    db.session.add(nouveauMembre)
    db.session.delete(inscription)
    db.session.commit()
    return redirect(url_for('gerer_inscriptions'))

@app.route ('/accepter_modifications/<int:idModif>', methods =("POST" ,))
@login_required
@admin_required
def accepter_modifications(idModif):
    modifications = db.session.get(ModifBD, idModif)
    if modifications and modifications.membre:
        membre_a_modifier = modifications.membre
        membre_a_modifier.nom = modifications.nom
        membre_a_modifier.prenom = modifications.prenom
        membre_a_modifier.email = modifications.email
        membre_a_modifier.ddn = modifications.ddn
        membre_a_modifier.sexe = modifications.sexe
        db.session.delete(modifications)
        db.session.commit()
    return redirect(url_for('gerer_inscriptions'))

@app.route('/refuser_inscription/<int:idI>', methods=["POST"])
@login_required
@admin_required
def refuser_inscription(idI):
    #La justification, elle est pour l'instant inutile et devrat plus tard etre envoyer par mail
    justification = request.form.get('justification')
    inscription_a_supprimer = db.session.get(InscriptionBD, idI)
    db.session.delete(inscription_a_supprimer)
    db.session.commit()
    return redirect(url_for('gerer_inscriptions'))

@app.route('/refuser_modification/<int:idM>', methods=["POST"])
@login_required
@admin_required
def refuser_modification(idM):
    #La justification, elle est pour l'instant inutile et devrat plus tard etre envoyer par mail
    justification = request.form.get('justification')
    modification_a_supprimer = db.session.get(ModifBD, idM)
    db.session.delete(modification_a_supprimer)
    db.session.commit()
    return redirect(url_for('gerer_inscriptions'))

#==============================================================#
#====================   Pages Paramètres   ====================#
#==============================================================#
@app.route('/parametres/')
def parametres():
    form = ParametresForm()
    return render_template("parametres.html", 
                         title=TITLE+"- Paramètres du Membre", 
                         form=form)

@app.route("/parametres_notifs/", methods=["GET", "POST"])
@login_required
def parametres_notifs():
    user_type = session.get('user_type')
    parametres = None

    if user_type == 'membre':
        # Récupère les paramètres de l'utilisateur membre, ou en crée de nouveaux si non existants
        parametres = ParametreNotifMembreBD.query.filter_by(idMembre=current_user.id).first()
        if not parametres:
            parametres = ParametreNotifMembreBD(idMembre=current_user.id)
            db.session.add(parametres)
            db.session.commit()

        if request.method == 'POST':
            # Mettre à jour les préférences du membre
            parametres.eventInscriptionSite = 'event_insc_site' in request.form
            parametres.evenementInscriptionMail = 'event_insc_mail' in request.form
            parametres.eventNouveauSite = 'event_new_site' in request.form
            parametres.eventNouveauMail = 'event_new_mail' in request.form
            parametres.eventAnnulationSite = 'event_cancel_site' in request.form
            parametres.eventAnnulationMail = 'event_cancel_mail' in request.form
            parametres.resultatNouveauSite = 'result_new_site' in request.form
            parametres.resultatNouveauMail = 'result_new_mail' in request.form
            parametres.reponseFormulaireSite = 'form_resp_site' in request.form
            parametres.reponseFormulaireMail = 'form_resp_mail' in request.form
            parametres.modifProfilSite = 'profile_mod_site' in request.form
            parametres.modifProfilMail = 'profile_mod_mail' in request.form
            db.session.commit()
            return redirect(url_for('parametres_notifs'))

    elif user_type == 'admin':
        # Récupère les paramètres de l'utilisateur admin, ou en crée de nouveaux si non existants
        parametres = ParametreNotifAdminBD.query.filter_by(idAdmin=current_user.id).first()
        if not parametres:
            parametres = ParametreNotifAdminBD(idAdmin=current_user.id)
            db.session.add(parametres)
            db.session.commit()

        if request.method == 'POST':
            # Mettre à jour les préférences de l'admin
            parametres.formulaireDemandeSite = 'form_req_site' in request.form
            parametres.formulaireDemandeMail = 'form_req_mail' in request.form
            parametres.formulaireQuestionSite = 'form_question_site' in request.form
            parametres.formulaireQuestionMail = 'form_question_mail' in request.form
            parametres.formulaireSignalementSite = 'form_report_site' in request.form
            parametres.formulaireSignalementMail = 'form_report_mail' in request.form
            parametres.demandeModifSite = 'profile_change_site' in request.form
            parametres.demandeModifMail = 'profile_change_mail' in request.form
            parametres.demandeInscriptionSite = 'signup_req_site' in request.form
            parametres.demandeInscriptionMail = 'signup_req_mail' in request.form
            db.session.commit()
            return redirect(url_for('parametres_notifs'))

    return render_template("parametres_notifs.html", title=TITLE+"- Paramètres notifications", parametres=parametres)

@app.route("/changer_mdp/", methods=['GET', 'POST'])
@login_required
def changer_mdp():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        # Vérifier si l'ancien mot de passe est correct
        if current_user.mdp_hash != form.old_password.data:
            return redirect(url_for('changer_mdp'))
        # Vérifier si les nouveaux mots de passe correspondent
        if form.new_password.data != form.confirm_new_password.data:
            return redirect(url_for('changer_mdp'))
        # Mettre à jour le mot de passe
        current_user.mdp_hash = form.new_password.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("changer_mdp.html", form=form, title=TITLE+"- Changer mot de passe")

#=============================================================#
#====================   Pages Connexion   ====================#
#=============================================================#

@app.route ("/login/", methods =("GET","POST"))
def login():
    # Si l'utilisateur est déjà connecté, on le redirige vers l'accueil
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # 1. Essayer de trouver un utilisateur (membre ou admin)
        utilisateur = MembreBD.query.filter_by(email=form.email.data).first()
        est_admin = False

        # 2. Si ce n'est pas un membre, essayer de trouver un admin
        if utilisateur is None:
            utilisateur = AdminBD.query.filter_by(email=form.email.data).first()
            est_admin = True

        # 3. Vérifier si un utilisateur a été trouvé 
        if utilisateur is None: 
            return redirect(url_for('login', message = "emailIncorrect"))
        
        # 4. Vérifier si le mot de passe est correct
        # La vérification du mot de passe est une comparaison directe
        if utilisateur.mdp_hash != form.password.data:
            return redirect(url_for('login', message = "mdpIncorrect"))
        
        # 5. Vérifier si le compte membre est actif
        if not est_admin and not utilisateur.activite:
            return redirect(url_for('login', message = "desincrit"))

        # Connexion de l'utilisateur
        login_user(utilisateur)
        # Stocker le type d'utilisateur dans la session
        session['user_type'] = 'admin' if est_admin else 'membre'
        # Redirection vers la page demandée ou l'accueil
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('index'))  
    
    message = request.args.get('message')
    return render_template("login.html", title=TITLE + "- Connexion", form=form, message=message)

@app.route("/inscription/", methods=["GET", "POST"])
def inscription():
    unForm = InscriptionForm()
    if unForm.validate_on_submit():
        nouvelle_inscription = InscriptionBD(
            email=unForm.Login.data,           
            nom=unForm.nom.data,
            prenom=unForm.prenom.data,
            ddn=unForm.date_naissance.data,
            sexe=unForm.sexe.data,
            mdp_hash=unForm.password.data # Note: Le mot de passe devrait être haché ici
        )
        try:
            if current_user.is_authenticated and session.get('user_type') == 'admin':
                nouveauMembre = MembreBD(
                    nom=nouvelle_inscription.nom,
                    prenom=nouvelle_inscription.prenom,
                    email=nouvelle_inscription.email,
                    ddn=nouvelle_inscription.ddn,
                    sexe=nouvelle_inscription.sexe,
                    mdp_hash=nouvelle_inscription.mdp_hash
                )
                db.session.add(nouveauMembre)
                db.session.commit()
                return redirect(url_for('gerer_profils'))
            else:
                db.session.add(nouvelle_inscription)
                db.session.commit()
                return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
    return render_template("inscription.html",title=TITLE+"- Inscriptions", form=unForm)

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


#==========================================================#
#====================   Pages Erreur   ====================#
#==========================================================#
@app.errorhandler(404)
def page_not_found(e):
    return render_template('gestion_erreur.html',
                           error_code=404,
                           error_title="Page non trouvée",
                           error_message="Désolé, la page que vous cherchez n'existe pas ou a été déplacée."), 404

@app.errorhandler(500)
def internal_server_error(e):
    db.session.rollback() 
    return render_template('gestion_erreur.html',
                           error_code=500,
                           error_title="Erreur interne du serveur",
                           error_message="Une erreur inattendue s'est produite. Notre équipe technique a été notifiée."), 500

@app.errorhandler(403)
def forbidden_access(e):
    return render_template('gestion_erreur.html',
                           error_code=403,
                           error_title="Accès Interdit",
                           error_message="Vous n'avez pas les autorisations nécessaires pour accéder à cette page."), 403

@app.errorhandler(400)
def admin_access(e):
    return render_template('gestion_erreur.html',
                           error_code=400,
                           error_title="Accès Interdit",
                           error_message="Cette page est réservé au compte de type Admin"), 400

@app.errorhandler(401)
def membre_access(e):
    return render_template('gestion_erreur.html',
                           error_code=401,
                           error_title="Accès Interdit",
                           error_message="Cette page est réservé au compte de type Membre"), 401

@app.errorhandler(405)
def comite_access(e):
    return render_template('gestion_erreur.html',
                           error_code=405,
                           error_title="Accès Interdit",
                           error_message="Cette page est réservé au membre du comité"), 405

if __name__ == "__main__":
    app.run()
    db.close()

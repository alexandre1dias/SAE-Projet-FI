from .app import app, db
from flask import render_template, request, url_for, redirect, flash, session
from config import TITLE
from flask_login import logout_user, login_user, login_required, current_user
from .forms import LoginForm, EventForm, PasswordChangeForm, InscriptionForm, MembreForm, ContactForm, ParametresForm, Parametres_updateForm
from .connexionPythonSQL import *
from monApp.modelBD import *
from datetime import datetime
from flask import jsonify
#from .models import Event

@app.route("/")
@app.route("/index/")
def index():
    return render_template("index.html", title = TITLE)

@app.route("/about/")
def about():
    return render_template("about.html",title=TITLE+"- A propos")

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
                date=datetime.now().date()
            )
            db.session.add(nouveau_message)
            db.session.commit()
            return redirect(url_for('contact'))
        except Exception as e:
            db.session.rollback()
    return render_template("contact.html", title=TITLE+"- Contact", form=form)

@app.route("/escrime-feminin/")
def escrime_feminin():
    return render_template("escrime_feminin.html",title=TITLE+"- L'escrime Féminin")

#Vues pour les Renseignements
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

#Vues pour les A propos
@app.route("/historique/")
def historique():
    return render_template("historique.html",title=TITLE+"- Historique") 

@app.route("/comite_cercle/")
def comite_cercle():
    return render_template("comite_cercle.html",title=TITLE+"- Comité directeur du Cercle")

#Vues pour les Evenements 
@app.route("/calendrier/")
def calendrier():
    return render_template("calendrier.html", title=TITLE+"- Calendrier")

@app.route("/competitions/")
def competitions():
    lesCompetitions = CompetitionBD.query.all()
    return render_template("competitions.html", title=TITLE+"- Competitions", competitions=lesCompetitions)

@app.route("/competitions/<int:idCompetition>/competition_view")
def competition_view(idCompetition):
    uneCompetition = CompetitionBD.query.get(idCompetition)
    origine = request.args.get('origine', 'default')
    return render_template("competition_view.html",title=TITLE+"- Consultation de la competition",selectedCompetition=uneCompetition, origine=origine)


@app.route("/competition_update/<int:idCompetition>", methods=['GET', 'POST'])
def competition_update(idCompetition):
    competition = CompetitionBD.query.get_or_404(idCompetition)
    if request.method == 'POST':
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
        return redirect(url_for('competition_view', idCompetition=competition.id))
    return render_template("competition_update.html",title=TITLE+"- Modification de la competition", competition=competition)

@app.route("/competition_delete/<int:idCompetition>", methods=['POST'])
@login_required # Assure que seul un utilisateur connecté peut supprimer
def competition_delete(idCompetition):
    competition_to_delete = CompetitionBD.query.get_or_404(idCompetition)
    db.session.delete(competition_to_delete)
    db.session.commit()
    return redirect(url_for('competitions')) # Redirige vers la liste des compétitions

@app.route("/evenement_club/")
def evenement_club():
    lesEventClubs = EventClubBD.query.all()
    return render_template("evenement_club.html",title=TITLE+"- Evenements du Club",eventsclub=lesEventClubs)

@app.route("/evenement_club/<int:idEventClub>/club_view/")
def club_view(idEventClub):
    unEventClub = EventClubBD.query.get(idEventClub)
    origine = request.args.get('origine', 'default')
    return render_template("club_view.html",title=TITLE+"- un évenement du club",selectedEventClub=unEventClub, origine=origine)

@app.route("/evenement_club/<int:idEventClub>/club_update/", methods=['GET', 'POST'])
@login_required
def club_update(idEventClub):
    unEventClub = EventClubBD.query.get_or_404(idEventClub)
    # Logique de mise à jour à implémenter
    return render_template("club_update.html",title=TITLE+"- Modification d'un évenement du club", eventClub=unEventClub)

@app.route("/evenement_club/<int:idEventClub>/club_delete/", methods=['POST'])
@login_required
def club_delete(idEventClub):
    event_to_delete = EventClubBD.query.get_or_404(idEventClub)
    db.session.delete(event_to_delete)
    db.session.commit()
    flash('L\'événement a été supprimé avec succès.', 'success')
    return redirect(url_for('evenement_club'))

@app.route("/reunion/")
def reunion():
    reunions = ReunionBD.query.all()
    today = datetime.now().date()
    prochaines_reunions = [r for r in reunions if r.dateDebutRE and r.dateDebutRE >= today]
    anciennes_reunions = [r for r in reunions if r.dateDebutRE and r.dateDebutRE < today]
    user_registered_event_ids = set()
    if current_user.is_authenticated and session.get('user_type') == 'membre':
        participations = ParticiperBD.query.filter_by(id_membre=current_user.id).all()
        user_registered_event_ids = {p.id_event for p in participations}
    return render_template("reunion.html", title=TITLE + "- Réunion", prochaines_reunions=prochaines_reunions, anciennes_reunions=anciennes_reunions,user_registered_event_ids = user_registered_event_ids)

@app.route("/reunion_view/<int:idReunion>")
def reunion_view(idReunion):
    reunion = ReunionBD.query.get(idReunion)
    origine = request.args.get('origine', 'default')
    return render_template("reunion_view.html",title=TITLE+"- Consultatiion d'une réunion", selectedReunion = reunion, origine=origine)

@app.route("/reunion_delete/<int:idReunion>", methods=['POST'])
def reunion_delete(idReunion):
    reunion = ReunionBD.query.get_or_404(idReunion)
    db.session.delete(reunion)
    db.session.commit()
    flash('La réunion a été supprimée avec succès.', 'success')
    return redirect(url_for('reunion'))

@app.route("/inscrire/reunion/<int:idReunion>", methods=['GET'])
@login_required
def inscrire_reunion(idReunion):
    reunion_obj = ReunionBD.query.get_or_404(idReunion)
    event_id_to_register = reunion_obj.idEvent

    deja_inscrit = ParticiperBD.query.filter_by(
        id_membre=current_user.id,
        id_event=event_id_to_register
    ).first()
    if deja_inscrit:
        flash('Vous êtes déjà inscrit à cet événement.', 'info')
    else:
        try:
            nouvelle_participation = ParticiperBD(
                id_membre=current_user.id,
                id_event=event_id_to_register
            )
            db.session.add(nouvelle_participation)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    return redirect(url_for('reunion'))

@app.route("/reunion/desinscrire/<int:idReunion>", methods=['GET'])
@login_required
def desinscrire_reunion(idReunion):
    reunion_obj = ReunionBD.query.get_or_404(idReunion)
    event_id = reunion_obj.idEvent
    participation = ParticiperBD.query.filter_by(id_membre=current_user.id, id_event=event_id).first()
    if participation:
        try:
            db.session.delete(participation)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    return redirect(url_for('reunion'))


@app.route("/reunion_update/<int:idReunion>", methods=['GET', 'POST'])
def reunion_update(idReunion):
    reunion = ReunionBD.query.get_or_404(idReunion)
    if request.method == 'POST':
        reunion.nom = request.form['nom']
        reunion.lieu = request.form['lieu']
        reunion.rapportRE = request.form['description']
        # Mettre à jour les dates et heures
        reunion.dateDebutRE = datetime.strptime(request.form['date_debut'], '%Y-%m-%d').date()
        reunion.heureDebutRE = request.form['heure_debut']
        reunion.dateFinRE = datetime.strptime(request.form['date_fin'], '%Y-%m-%d').date()
        reunion.heureFinRE = request.form['heure_fin']
        db.session.commit()
        flash('La réunion a été mise à jour avec succès.', 'success')
        return redirect(url_for('reunion_view', idReunion=reunion.id))
    return render_template("reunion_update.html", title=TITLE + "- Modification d'une réunion", reunion=reunion)

#Vues pour le Profil
@app.route("/resultat_membre/")
@login_required
def resultat_membre():
    les_resultats = ResultatBD.query.filter_by(id_membre=current_user.id).all()
    return render_template("resultat_membre.html", title=TITLE+"- Résultat du Membre", resultats=les_resultats)

@app.route("/evenement_membre/")
@login_required
def evenement_membre():

    today = datetime.now().date()
    participations = ParticiperBD.query.filter_by(id_membre=current_user.id).all()
    event_ids = [p.id_event for p in participations]

    events = []
    if event_ids:
        competitions = CompetitionBD.query.filter(CompetitionBD.id_event.in_(event_ids)).all()
        reunions = ReunionBD.query.filter(ReunionBD.idEvent.in_(event_ids)).all()
        event_clubs = EventClubBD.query.filter(EventClubBD.id_event.in_(event_ids)).all()
        events.extend(competitions)
        events.extend(reunions)
        events.extend(event_clubs)

    events_a_venir = [e for e in events if (getattr(e, 'date_debut', None) or getattr(e, 'dateRE', None) or getattr(e, 'dateDebutEV', None)) >= today]
    events_passes = [e for e in events if (getattr(e, 'date_debut', None) or getattr(e, 'dateRE', None) or getattr(e, 'dateDebutEV', None)) < today]

    return render_template("evenement_membre.html", title=TITLE+"- Vos Évènements",
                           events_a_venir=events_a_venir, events_passes=events_passes)

@app.route('/parametres/')
def parametres():
    form = ParametresForm()
    return render_template("parametres.html", 
                         title=TITLE+"- Paramètres du Membre", 
                         form=form)

@app.route('/parametres_update/')
def parametres_update():
    form = Parametres_updateForm()
    return render_template("parametres_update.html", 
                         title=TITLE+"- Paramètres du Membre", 
                         form=form)

@app.route("/changer_mdp/", methods=['GET', 'POST'])
@login_required
def changer_mdp():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        # Vérifier si l'ancien mot de passe est correct
        if current_user.mdp_hash != form.old_password.data:
            flash("L'ancien mot de passe est incorrect.", 'danger')
            return redirect(url_for('changer_mdp'))

        # Vérifier si les nouveaux mots de passe correspondent
        if form.new_password.data != form.confirm_new_password.data:
            flash("Les nouveaux mots de passe ne correspondent pas.", 'danger')
            return redirect(url_for('changer_mdp'))

        # Mettre à jour le mot de passe
        current_user.mdp_hash = form.new_password.data
        db.session.commit()
        flash("Votre mot de passe a été mis à jour avec succès.", 'success')
        return redirect(url_for('index'))
    return render_template("changer_mdp.html", form=form, title=TITLE+"- Changer mot de passe")


#Vues notification
@app.route("/parametres_notifs/")
def parametres_notifs():
    return render_template("parametres_notifs.html",title=TITLE+"- Paramètres notifications")

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

#Vues pour Admin
@app.route("/gerer_formulaires/")
def gerer_formulaires():
    les_formulaires = FormulaireBD.query.order_by(FormulaireBD.date.desc()).filter(FormulaireBD.repondu == False).all()
    return render_template("gerer_formulaires.html", title=TITLE+"- Géstion des Formulaires", formulaires=les_formulaires)

@app.route("/gerer_anciens_formulaires/")
def gerer_anciens_formulaires():
    les_formulaires = FormulaireBD.query.order_by(FormulaireBD.date.desc()).filter(FormulaireBD.repondu == True).all()
    return render_template("gerer_anciens_formulaires.html", title=TITLE+"- Géstion des Anciens Formulaires", formulaires=les_formulaires)

@app.route("/formulaire_view/<int:idFormulaire>")
def formulaire_view(idFormulaire):
    unFormulaire = FormulaireBD.query.get_or_404(idFormulaire)
    return render_template("formulaire_view.html",title=TITLE+"- Consultation de Formulaire", selectedFormulaire=unFormulaire)

@app.route("/formulaire_delete/<int:idFormulaire>", methods=['POST'])
@login_required
def formulaire_delete(idFormulaire):
    formulaire_a_supprimer = FormulaireBD.query.get_or_404(idFormulaire)
    db.session.delete(formulaire_a_supprimer)
    db.session.commit()
    return redirect(url_for('gerer_formulaires'))

@app.route("/repondre_formulaire/<int:idFormulaire>", methods=['POST'])
@login_required
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
def gerer_profils():
    lesMembres = db.session.query(MembreBD).filter(MembreBD.activite == True).all()
    return render_template("gerer_profils.html",title=TITLE+"- Géstion des Profils", membres = lesMembres)

@app.route("/gerer_profils/ancien/")
def gerer_ancien_profils():
    lesMembres = db.session.query(MembreBD).filter(MembreBD.activite == False).all()
    return render_template("gerer_ancien_profils.html",title=TITLE+"- Géstion des Anciens Profils", membres = lesMembres)

@app.route("/profil_view/<int:idM>/<int:origine>")
def profil_view(idM, origine):
    # origine corresponds à l'origine de l'utilisateur. 0 correspond au menu de Membre: Vos information,
    # 1 corresponds à gerer_profils et 2 à gerer_ancien_profil
    unMembre = db.session.get(MembreBD,idM)
    return render_template("profil_view.html", title=TITLE + "- Profil Membre", selectedMembre=unMembre, origine = origine)

@app.route("/profil_edit/<int:idM>/<int:origine>", methods=["GET", "POST"])
def profil_edit(idM, origine):
    unMembre = db.session.get(MembreBD,idM)
    unForm = MembreForm(obj=unMembre)
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
            db.session.commit()
            return redirect(url_for('profil_view', idM=unMembre.id, origine=0))
    return render_template("profil_edit.html", title=TITLE + "- Modifier Profil", selectedMembre=unMembre, updateForm = unForm, origine = origine)

@app.route('/profil_edit/<int:idM>/desinscrit/')
def desinscritProfil(idM):
    membreDesinscrit = db.session.get(MembreBD, idM)
    membreDesinscrit.activite = False
    db.session.commit()
    return redirect(url_for('gerer_profils'))

@app.route('/profil_edit/<int:idM>/reinscrit/')
def reinscritProfil(idM):
    membreReinscrit = db.session.get(MembreBD, idM)
    membreReinscrit.activite = True
    db.session.commit()
    return redirect(url_for('gerer_ancien_profils'))


#Vue pour la gestion des inscription/modification
@app.route("/gerer_inscriptions/")
def gerer_inscriptions():
    lesInscriptions = db.session.query(InscriptionBD).all()
    lesModifs = db.session.query(ModifBD).all()
    lesRequetes = lesInscriptions + lesModifs
    # Trie par date de la liste
    lesRequetes.sort(key=lambda x: x.date, reverse=True)  
    return render_template("gerer_inscriptions.html",title=TITLE+"- Géstion des Inscriptions", requetes=lesRequetes)



#Vues pour le login 
@app.route ("/login/", methods =("GET","POST"))
def login():
    # Si l'utilisateur est déjà connecté, on le redirige vers l'accueil
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # 1. Essayer de trouver un membre
        user = MembreBD.query.filter_by(email=form.email.data).first()
        is_admin = False
        
        # 2. Si ce n'est pas un membre, essayer de trouver un admin
        if user is None:
            user = AdminBD.query.filter_by(email=form.email.data).first()
            is_admin = True

        # 3. Vérifier si un utilisateur a été trouvé et si le mot de passe est correct
        # La vérification du mot de passe est une comparaison directe
        if user is None or user.mdp_hash != form.password.data:
            return redirect(url_for('login'))
        
        # Connexion de l'utilisateur
        login_user(user)
        
        # Stocker le type d'utilisateur dans la session
        session['user_type'] = 'admin' if is_admin else 'membre'

        # Redirection vers la page suivante ou l'accueil
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('index'))
        
    return render_template("login.html", title=TITLE + "- Connexion", form=form)

@app.route("/inscription/", methods=["GET", "POST"])
def inscription():
    unForm = InscriptionForm()
    if unForm.validate_on_submit():
        new_inscription = InscriptionBD(
            email=unForm.Login.data,           
            nom=unForm.nom.data,
            prenom=unForm.prenom.data,
            ddn=unForm.date_naissance.data,
            sexe=unForm.sexe.data,
            mdp_hash=unForm.password.data
        )
        try:
            db.session.add(new_inscription)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            
    # Si le formulaire n'est PAS valide, la page est re-rendue
    # et les erreurs s'afficheront grâce aux modifs du Problème n°1
    return render_template("inscription.html",title=TITLE+"- Inscriptions", form=unForm)

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

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


# Route pour ajouter un événement
@app.route("/add_event/", methods=["GET", "POST"])
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

if __name__ == "__main__":
    app.run()
    db.close()

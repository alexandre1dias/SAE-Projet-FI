from .app import app, db
from flask import render_template, request, url_for, redirect, session, abort, flash
from config import TITLE, AUJOURDHUI
from flask_login import logout_user, login_user, login_required, current_user
from .forms import *
from monApp.modelBD import *
from flask import jsonify
from functools import wraps
from datetime import datetime
from sqlalchemy import or_,asc, desc
import shutil
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


# Définir les extensions de fichiers autorisées
ALLOWED_EXTENSIONS = {'webp','png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Vérifie si l'extension du fichier est autorisée."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Décorateur pour vérifier si l'utilisateur est un admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # On vérifie si l'objet current_user est une instance de la classe AdminBD
        if not current_user.is_authenticated or not isinstance(current_user, AdminBD):
            abort(400)  # Déclenche l'erreur "Accès Interdit" Admin
        return f(*args, **kwargs)
    return decorated_function

# Décorateur pour vérifier si l'utilisateur est un membre
def membre_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # On vérifie l'instance MembreBD
        if not current_user.is_authenticated or not isinstance(current_user, MembreBD):
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
        # Vérifications basées sur les objets
        is_admin = isinstance(current_user, AdminBD)
        is_comite_membre = (
            isinstance(current_user, MembreBD) and
            current_user.statut in statuts_comite
        )
        if not (current_user.is_authenticated and (is_admin or is_comite_membre)):
            abort(405)  # Déclenche l'erreur "Accès Interdit"
        return f(*args, **kwargs)
    return decorated_function

#Vérificateur de mot de passe, vérifie si le mot de passe est complexe
def est_mot_de_passe_fort(password):
    # Vérifie la longueur (min 8 caractères)
    if len(password) < 8:
        return False
    # Vérifie la présence d'au moins une minuscule
    if not re.search(r"[a-z]", password):
        return False
    # Vérifie la présence d'au moins une majuscule
    if not re.search(r"[A-Z]", password):
        return False
    # Vérifie la présence d'au moins un chiffre
    if not re.search(r"[0-9]", password):
        return False
    # Vérifie la présence d'au moins un caractère spécial (!@#$%^&*)
    if not re.search(r"[ !@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True

# fonction pour récupérer un utilisateur (Membre ou Admin) par email
def get_user_by_email(email):
    return MembreBD.query.filter_by(email=email).first() or AdminBD.query.filter_by(email=email).first()

# fonction pour simuler l'envoi d'email
def simuler_envoi_email(email, link):
    print("\n" + "="*50)
    print(f"SIMULATION D'ENVOI D'EMAIL À : {email}")
    print(f"LIEN : {link}")
    print("="*50 + "\n")

# initialisation de Flask-Mail et du Serializer pour les tokens
# variables de config MAIL_* sont définies dans app.config
mail = Mail(app)
# source : https://stackoverflow.com/questions/34043847/forcing-itsdangerous-urlsafetimedserializer-to-give-old-signature
s = URLSafeTimedSerializer(app.config.get('SECRET_KEY', 'default-secret-key'))

# Injecter les notifications dans tous les templates
@app.context_processor
def inject_notifications():
    unread_count = 0
    notifications_list = []
    if current_user.is_authenticated:
        user_type = session.get('user_type')
        if user_type == 'membre':
            query = NotifsBD.query.filter_by(idMembre=current_user.id)
        elif user_type == 'admin':
            query = NotifsBD.query.filter_by(idAdmin=current_user.id)
        else:
            query = None
            
        if query:
            unread_count = query.filter_by(lue=False).count()
            notifications_list = query.order_by(NotifsBD.timestamp.desc()).limit(10).all()
            
    return dict(unread_count=unread_count, notifications_list=notifications_list)

# Route pour marquer une notification comme lue et rediriger vers son lien
@app.route("/read_notification/<int:id_notif>")
@login_required
def read_notification(id_notif):
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

    notif.lue = True
    db.session.commit()

    if notif.link and notif.link != '#':
        return redirect(notif.link)
    return redirect(request.referrer or url_for('index'))

# Route pour supprimer une notification
@app.route("/delete_notification/<int:id_notif>", methods=['POST'])
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
    return redirect(request.referrer or url_for('index'))

#==========================================================#
#====================   Page Accueil   ====================#
#==========================================================#
# Affiche la page d'accueil avec les dernières actualités.
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
# Affiche la page avec l'adresse du club.
@app.route("/adresse/")
def adresse():
    return render_template("adresse.html",title=TITLE+"- Adresse")

# Affiche la page des horaires d'entraînement.
@app.route("/horaires/")
def horaires():
    les_horaires = HoraireBD.query.all()
    ordre_jours = {
        'Lundi': 1,
        'Mardi': 2,
        'Mercredi': 3,
        'Jeudi': 4,
        'Vendredi': 5,
        'Samedi': 6,
        'Dimanche': 7
    }
    les_horaires.sort(key=lambda x: (ordre_jours.get(x.jour, 8), x.heure_debut))
    return render_template("horaire.html", title=TITLE+"- Horaires", horaires=les_horaires)

# Affiche la page avec les informations sur l'adhésion.
@app.route("/adhesions/")
def adhesions():
    tarifs_adhesion = TarifBD.query.filter_by(categorie='Adhesion').all()
    return render_template("adhesion.html", title=TITLE+"- Adhésions", tarifs=tarifs_adhesion)

# Affiche la page d'information sur le matériel et la location.
@app.route("/materiel/")
def materiel():
    tarifs_materiel = TarifBD.query.filter_by(categorie='Materiel').all()
    return render_template("materiel.html", title=TITLE+"- Matériel et tenues", tarifs=tarifs_materiel)

#==================================================================#
#====================   Pages Escrim feminin   ====================#
#==================================================================#
# Affiche la page dédiée à l'escrime féminine.
@app.route("/escrime-feminin/")
def escrime_feminin():
    return render_template("escrime_feminin.html",title=TITLE+"- L'escrime Féminin")


#==============================================================#
#====================   Pages Evenements   ====================#
#==============================================================#

#====================   Pages Calendrier   ====================#
# Affiche le calendrier interactif des événements.
@app.route("/calendrier/")
def calendrier():
    return render_template("calendrier.html", title=TITLE+"- Calendrier")

# API pour fournir les données des événements au calendrier FullCalendar.
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
    voir_reunions = False
    if current_user.is_authenticated:
        # On utilise isinstance pour être sûr du type d'objet
        if isinstance(current_user, AdminBD):
            voir_reunions = True
        elif isinstance(current_user, MembreBD):
            statuts_comite = [
                'Président', 'Vice-président', 'Vice-Président', 
                'Secrétaire Général', 'Trésorier Général', 'Membre du Comité'
            ]
            if current_user.statut in statuts_comite:
                voir_reunions = True

    # Si l'utilisateur a les droits, on ajoute les réunions
    if voir_reunions:
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
                    'description': event.rapportRE
                }
            })
    if current_user.is_authenticated:
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
                'description': f"Jour: {event.jour}",
                'niveaux': event.niveau,
                'arme': event.type_arme,
                'ville': event.ville,
                'adresse': event.adresse
            }
        })
    return jsonify(all_events)

# Page pour ajouter un nouvel événement - Réservée aux administrateurs.
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
                    ville=form.ville.data,
                    adresse=form.adresse.data,
                    typeReunionRE=form.type_reunion.data if form.type_reunion.data else "Générale"
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
            print(f"ERREUR SQL/CODE : {e}")  # AJOUT POUR DEBUG
    else:
        print(f"ERREUR FORMULAIRE : {form.errors}")
    return render_template("add_event.html", title=TITLE + "- Ajouter un événement", form=form)

#================================================================#
#====================   Pages Competitions   ====================#
#================================================================#

# Affiche la liste de toutes les compétitions.
@app.route("/competitions/")
@app.route("/competitions/<string:etat>") 
def competitions(etat="prochaine"): 
    passee = (etat == "passees")
    filtre = FiltreForm(request.args if request.args else None)
    page = request.args.get('page', 1, type=int)
    lesCompetitions = CompetitionBD.query

    filtre.tri.choices = [
        ('date_desc', 'Plus récent'), 
        ('date_asc', 'Plus ancien')
    ]
    
    if filtre.tri.data == "date_asc":
        lesCompetitions = lesCompetitions.order_by(CompetitionBD.date_debut.asc())
    else:
        lesCompetitions = lesCompetitions.order_by(CompetitionBD.date_debut.desc())

    lesCompetitions = lesCompetitions.filter(CompetitionBD.passee == passee)     
    
    if filtre.sexe.data:
        lesCompetitions = lesCompetitions.filter(CompetitionBD.sexe.in_(filtre.sexe.data))
    if filtre.niveau.data:
        lesCompetitions = lesCompetitions.filter(or_(*(CompetitionBD.niveaux.like(f"%{n}%") for n in filtre.niveau.data)))
    if filtre.armes.data:
        lesCompetitions = lesCompetitions.filter(CompetitionBD.type_arme.in_(filtre.armes.data))
    if filtre.type_competition.data:
        lesCompetitions = lesCompetitions.filter(CompetitionBD.typeComp.in_(filtre.type_competition.data))
    pagination = lesCompetitions.paginate(page=page, per_page=6, error_out=False)
    return render_template("competitions.html", title=TITLE+"- Competitions", pagination=pagination,filtre = filtre, passee=passee)


# Affiche les détails d'une compétition spécifique.
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

    # Vérifie si un classement PDF existe pour cette compétition
    classement_pdf_path = os.path.join(app.root_path, 'static', 'classements', str(uneCompetition.id), 'classement.pdf')
    classement_pdf_exists = os.path.exists(classement_pdf_path)
    return render_template("competition_view.html",title=TITLE+"- Consultation de la competition",competition=uneCompetition,origine=origine,deja_inscrit=deja_inscrit,est_eligible=est_eligible, lesResultats = resultats, classement_pdf_exists=classement_pdf_exists)

# Permet à un membre de s'inscrire à une compétition.
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

# Permet à un utilisateur (membre ou admin) de se désinscrire d'une compétition.
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

# Page de modification d'une compétition - Réservée aux administrateurs.
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

# Page pour sélectionner les membres à inscrire à une compétition - Réservée aux administrateurs.
@app.route("/competition/<int:idC>/inscrire_membres", methods=['GET'])
@login_required
@admin_required
def inscrire_membres_competition(idC):
    competition = CompetitionBD.query.get_or_404(idC)

    membres_a_inscrire_ids = request.args.getlist('membres_a_inscrire_ids', type=int)
    if not membres_a_inscrire_ids:
        membres_a_inscrire_ids = []
    if 'add' in request.args:
        membres_a_inscrire_ids.append(int(request.args.get('add')))
    if 'remove' in request.args:
        membres_a_inscrire_ids.remove(int(request.args.get('remove')))
    participations = ParticiperBD.query.filter_by(id_event=competition.id_event).all()
    participants_ids = {p.id_membre for p in participations}
    tous_les_non_participants = MembreBD.query.filter(MembreBD.id.notin_(participants_ids), MembreBD.activite == True).all()
    surclassement_map = {'M9': 'M11', 'M11': 'M13', 'M13': 'M15', 'M15': 'M17','M17': 'M20', 'M20': 'Senior', 'Senior': 'Vétéran'}
    niveaux_liste = [niveau.strip() for niveau in competition.niveaux.split(',')]
    non_participants_eligibles = []
    for non_participant in tous_les_non_participants:
        surclassement_niveau = surclassement_map.get(non_participant.niveau)
        est_eligible = (non_participant.niveau in niveaux_liste) or \
                       (surclassement_niveau and surclassement_niveau in niveaux_liste)
        if est_eligible:
            non_participants_eligibles.append(non_participant)
    return render_template("competition_inscrire_membre.html", title=TITLE+"- Inscrire des membres", competition=competition, non_participants=non_participants_eligibles, membres_a_inscrire_ids=membres_a_inscrire_ids)

# Traite l'inscription de plusieurs membres à une compétition - Réservée aux administrateurs.
@app.route("/competition/<int:idC>/inscription_membres", methods=['POST'])
@login_required
@admin_required
def inscription_membres_competition(idC):
    competition = CompetitionBD.query.get_or_404(idC)
    membres_a_inscrire_ids = request.form.getlist('membres_a_inscrire')

    for membre_id in membres_a_inscrire_ids:
        deja_inscrit = ParticiperBD.query.filter_by(id_membre=membre_id, id_event=competition.id_event).first()
        if not deja_inscrit:
            nouvelle_participation = ParticiperBD(id_membre=membre_id, id_event=competition.id_event)
            db.session.add(nouvelle_participation)
    db.session.commit()
    return redirect(url_for('competition_update', idCompetition=idC))

# Enregistre ou met à jour le classement d'un membre pour une compétition - Réservée aux administrateurs.
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

# Gère le téléversement du fichier PDF du classement pour une compétition
@app.route("/competition/<int:idCompetition>/upload_classement", methods=['POST'])
@login_required
@admin_required
def upload_classement_competition(idCompetition):
    competition = CompetitionBD.query.get_or_404(idCompetition)
    
    if 'classement_pdf' not in request.files:
        flash('Aucun fichier n\'a été envoyé.', 'danger')
        return redirect(url_for('competition_update', idCompetition=idCompetition))
        
    file = request.files['classement_pdf']
    
    if file.filename == '':
        flash('Aucun fichier sélectionné.', 'danger')
        return redirect(url_for('competition_update', idCompetition=idCompetition))
        
    if file and file.filename.lower().endswith('.pdf'):
        filename = "classement.pdf" # Nom de fichier fixe pour le retrouver facilement
        dossier_classement = os.path.join(app.root_path, 'static', 'classements', str(competition.id))
        os.makedirs(dossier_classement, exist_ok=True)
        file.save(os.path.join(dossier_classement, filename))
        flash('Le classement PDF a été téléversé avec succès.', 'success')
    else:
        flash('Type de fichier non autorisé. Veuillez téléverser un fichier PDF.', 'danger')
    return redirect(url_for('competition_update', idCompetition=idCompetition))

# Supprime la participation d'un membre à une compétition - Réservée aux administrateurs.
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
    
# Ajoute une image à une compétition
@app.route("/competition/<int:idCompetition>/add_image", methods=['POST'])
@login_required
@admin_required
def add_image_competition(idCompetition):
    competition = CompetitionBD.query.get_or_404(idCompetition)
    
    if 'image' not in request.files:
        flash('Aucun fichier image n\'a été envoyé.', 'danger')
        return redirect(url_for('competition_update', idCompetition=idCompetition))
        
    file = request.files['image']
    
    if file.filename == '':
        flash('Aucun fichier image sélectionné.', 'danger')
        return redirect(url_for('competition_update', idCompetition=idCompetition))
        
    if file:
        filename = secure_filename(file.filename)
        # Création d'un dossier unique pour chaque compétition pour éviter les conflits de noms
        dossier_images = os.path.join(app.root_path, 'static', 'images', 'competitions', str(competition.id))
        os.makedirs(dossier_images, exist_ok=True)
        
        file.save(os.path.join(dossier_images, filename))
        
        # L'URL stockée en BDD est relative au dossier 'static'
        image_url = os.path.join('images', 'competitions', str(competition.id), filename).replace('\\', '/')
        
        alt_text = request.form.get('alt', filename)
        prive = 'prive' in request.form
        
        try:
            nouvelle_image = ImageAppBD(urlI=image_url, alt=alt_text, prive=prive)
            competition.images_rc.append(nouvelle_image)
            db.session.add(nouvelle_image)
            db.session.commit()
            flash('Image ajoutée avec succès.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de l\'ajout de l\'image à la base de données.', 'danger')
    
    return redirect(url_for('competition_update', idCompetition=idCompetition))

# Supprime une image d'une compétition
@app.route("/competition/delete_image/<int:idImage>", methods=['POST'])
@login_required
@admin_required
def delete_image_competition(idImage):
    idCompetition = request.form.get('idCompetition')
    if not idCompetition:
        flash('ID de compétition manquant.', 'danger')
        return redirect(request.referrer or url_for('index'))

    competition = CompetitionBD.query.get_or_404(idCompetition)
    image_a_retirer = ImageAppBD.query.get_or_404(idImage)

    # On vérifie si l'image est bien dans la liste de la compétition
    if image_a_retirer in competition.images_rc:
        # On retire l'association
        competition.images_rc.remove(image_a_retirer)

        # Supprime le fichier physique
        try:
            image_path = os.path.join(app.static_folder, image_a_retirer.urlI)
            if os.path.exists(image_path):
                os.remove(image_path)
            # Optionnel : supprime le dossier s'il est vide
            image_dir = os.path.dirname(image_path)
            if not os.listdir(image_dir):
                os.rmdir(image_dir)
        except Exception as e:
            flash(f"Erreur lors de la suppression du fichier : {e}", "danger")

        # Supprime l'image de la base de données
        db.session.delete(image_a_retirer)
        db.session.commit()
        flash('L\'image a été retirée de la compétition.', 'success')
    else:
        flash('Cette image n\'était pas associée à cette compétition.', 'warning')

    return redirect(url_for('competition_update', idCompetition=idCompetition))

# Supprime une compétition et toutes ses participations - Réservée aux administrateurs.
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
# Affiche la liste des événements du club.
@app.route("/evenement_club/")
@app.route("/evenement_club/<string:etat>")
def evenement_club(etat="prochaine"):
    passee = (etat == "passees")
    filtre = FiltreForm(request.args if request.args else None)
    page = request.args.get('page', 1, type=int)
    lesEvements = EventClubBD.query
    filtre.tri.choices = [
        ('date_desc', 'Plus récent'),
        ('date_asc', 'Plus ancien')
    ]

    if filtre.tri.data == "date_asc":
        lesEvements = lesEvements.order_by(EventClubBD.dateDebutEV.asc())
    else:
        lesEvements = lesEvements.order_by(EventClubBD.dateDebutEV.desc())

    lesEvements = lesEvements.filter(EventClubBD.passeeEV == passee)
    pagination = lesEvements.paginate(page=page, per_page=6, error_out=False)

    return render_template("evenement_club.html",
                           title=TITLE + "- Evenements du Club",
                           pagination=pagination,
                           filtre=filtre,
                           passee=passee)

# Affiche les détails d'un événement de club spécifique.
@app.route("/evenement_club/<int:idEventClub>/club_view/")
def club_view(idEventClub):
    unEventClub = EventClubBD.query.get(idEventClub)
    origine = request.args.get('origine', 'default')

    deja_inscrit = False
    if current_user.is_authenticated and session.get('user_type') == 'membre':
        participation = ParticiperBD.query.filter_by(id_membre=current_user.id, id_event=unEventClub.id_event).first()
        deja_inscrit = participation is not None
    return render_template("club_view.html",title=TITLE+"- un évenement du club",selectedEventClub=unEventClub, deja_inscrit=deja_inscrit, origine=origine)

# Page de modification d'un événement de club - Réservée aux administrateurs.
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
    return render_template("club_update.html",title=TITLE+"- Modification d'un évenement du club", eventClub=unEventClub, participants=participants)

# Page pour sélectionner les membres à inscrire à un événement de club - Réservée aux administrateurs.
@app.route("/evenement_club/<int:idEventClub>/inscrire_membres", methods=['GET'])
@login_required
@admin_required
def inscrire_membres_event_club(idEventClub):
    event_club = EventClubBD.query.get_or_404(idEventClub)
    membres_a_inscrire_ids = request.args.getlist('membres_a_inscrire_ids', type=int)
    if not membres_a_inscrire_ids:
        membres_a_inscrire_ids = []
    if 'add' in request.args:
        membres_a_inscrire_ids.append(int(request.args.get('add')))
    if 'remove' in request.args:
        membres_a_inscrire_ids.remove(int(request.args.get('remove')))
    participations = ParticiperBD.query.filter_by(id_event=event_club.id_event).all()
    participants_ids = {p.id_membre for p in participations}
    non_participants = MembreBD.query.filter(MembreBD.id.notin_(participants_ids), MembreBD.activite == True).all()
    return render_template("club_inscrire_membre.html", title=TITLE+"- Inscrire des membres", eventClub=event_club, non_participants=non_participants, membres_a_inscrire_ids=membres_a_inscrire_ids)

# Traite l'inscription de plusieurs membres à un événement de club - Réservée aux administrateurs.
@app.route("/evenement_club/<int:idEventClub>/inscription_membres", methods=['POST'])
@login_required
@admin_required
def inscription_membres_event_club(idEventClub):
    event_club = EventClubBD.query.get_or_404(idEventClub)
    membres_a_inscrire_ids = request.form.getlist('membres_a_inscrire')
    for membre_id in membres_a_inscrire_ids:
        deja_inscrit = ParticiperBD.query.filter_by(id_membre=membre_id, id_event=event_club.id_event).first()
        if not deja_inscrit:
            nouvelle_participation = ParticiperBD(id_membre=membre_id, id_event=event_club.id_event)
            db.session.add(nouvelle_participation)
    db.session.commit()
    return redirect(url_for('club_update', idEventClub=idEventClub))

# Supprime la participation d'un membre à un événement de club - Réservée aux administrateurs.
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

# Supprime un événement de club - Réservée aux administrateurs.
@app.route("/evenement_club/<int:idEventClub>/club_delete/", methods=['POST'])
@login_required
@admin_required
def club_delete(idEventClub):
    evenement_a_supprimer = EventClubBD.query.get_or_404(idEventClub)
    db.session.delete(evenement_a_supprimer)
    db.session.commit()
    return redirect(url_for('evenement_club'))

# Permet à un membre de s'inscrire à un événement de club.
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

# Permet à un membre de se désinscrire d'un événement de club.
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

@app.route('/club/add_image/<int:idEventClub>', methods=['POST'])
@login_required
@admin_required
def add_image_club(idEventClub):
    """Ajoute une image à un événement du club."""
    event_club = EventClubBD.query.get_or_404(idEventClub)
    
    if 'image' not in request.files:
        flash('Aucun fichier sélectionné.', 'danger')
        return redirect(url_for('club_update', idEventClub=idEventClub))
        
    file = request.files['image']
    alt_text = request.form.get('alt', 'Image pour l\'événement ' + event_club.NomEV)
    is_prive = 'prive' in request.form

    if file.filename == '':
        flash('Aucun fichier image sélectionné.', 'warning')
        return redirect(url_for('club_update', idEventClub=idEventClub))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Crée un dossier spécifique pour l'événement s'il n'existe pas
        upload_folder = os.path.join(app.static_folder, 'images', 'events_club', str(event_club.idEventClub))
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # Chemin à stocker en BDD, relatif au dossier 'static'
        db_url = os.path.join('images', 'events_club', str(event_club.idEventClub), filename).replace('\\', '/')

        # Crée l'objet Image et l'associe à l'événement
        try:
            new_image = ImageAppBD(urlI=db_url, alt=alt_text, prive=is_prive)
            event_club.images_re.append(new_image)
            db.session.add(new_image)
            db.session.commit()
            flash('Image ajoutée avec succès !', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de l\'ajout de l\'image : {e}', 'danger')
    else:
        flash('Type de fichier non autorisé.', 'danger')

    return redirect(url_for('club_update', idEventClub=idEventClub))


@app.route('/club/delete_image/<int:idImage>', methods=['POST'])
@login_required
@admin_required
def delete_image_club(idImage):
    """Supprime une image d'un événement du club."""
    idEventClub = request.form.get('idEventClub')
    if not idEventClub:
        flash("ID de l'événement manquant.", "danger")
        return redirect(url_for('index'))

    image_to_delete = ImageAppBD.query.get_or_404(idImage)
    event_club = EventClubBD.query.get_or_404(idEventClub)

    if image_to_delete in event_club.images_re:
        # Supprime l'association
        event_club.images_re.remove(image_to_delete)

        # Supprime le fichier physique
        try:
            image_path = os.path.join(app.static_folder, image_to_delete.urlI)
            if os.path.exists(image_path):
                os.remove(image_path)
            
            # Optionnel : supprime le dossier s'il est vide
            image_dir = os.path.dirname(image_path)
            if not os.listdir(image_dir):
                os.rmdir(image_dir)
                
        except Exception as e:
            flash(f"Erreur lors de la suppression du fichier : {e}", "danger")

        # Supprime l'image de la base de données
        db.session.delete(image_to_delete)
        db.session.commit()

        flash("L'image a été retirée de l'événement.", "success")
    else:
        flash("Cette image n'était pas associée à cet événement.", "warning")
        
    return redirect(url_for('club_update', idEventClub=idEventClub))

#====================   Pages Reunions   ====================#
# Page affichant toutes les réunions - Réservée à Admin et Membre du Comité.
@app.route("/reunion/")
@login_required
@comite_ou_admin_required
def reunion():
    reunions = ReunionBD.query.all()
    prochaines_reunions = [r for r in reunions if r.dateDebutRE and r.dateDebutRE >= AUJOURDHUI]
    anciennes_reunions = [r for r in reunions if r.dateFinRE and r.dateFinRE < AUJOURDHUI]
    ids_evenements_inscrits = set()
    if current_user.is_authenticated and session.get('user_type') == 'membre':
        participations = ParticiperBD.query.filter_by(id_membre=current_user.id).all()
        ids_evenements_inscrits = {p.id_event for p in participations}
    return render_template("reunion.html", title=TITLE + "- Réunion", prochaines_reunions=prochaines_reunions, anciennes_reunions=anciennes_reunions,user_registered_event_ids = ids_evenements_inscrits)

# Page de consultation d'une réunion - Réservée à Admin et Membres du Comité.
@app.route("/reunion/consultation/<int:idReunion>")
@login_required
@comite_ou_admin_required
def reunion_view(idReunion):
    reunion = ReunionBD.query.get(idReunion)
    origine = request.args.get('origine', 'default')
    return render_template("reunion_view.html",title=TITLE+"- Consultatiion d'une réunion", selectedReunion = reunion, origine=origine)

# Vue de suppression d'une réunion - Réservée aux administrateurs.
@app.route("/reunion/delete/<int:idReunion>", methods=['POST'])
@login_required
@admin_required
def reunion_delete(idReunion):
    reunion = ReunionBD.query.get_or_404(idReunion)
    db.session.delete(reunion)
    db.session.commit()
    return redirect(url_for('reunion'))

# Vue d'inscription à une réunion - Réservée aux membres du comité et aux admins.
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

# Vue de désinscription d'une réunion - Réservée aux membres du comité et aux admins.
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

# Page de modification d'une réunion - Réservée à l'Admin.
@app.route("/reunion/update/<int:idReunion>", methods=['GET', 'POST'])
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
        return redirect(url_for('reunion_view', idReunion=reunion.id))
    return render_template("reunion_update.html", title=TITLE + "- Modification d'une réunion", reunion=reunion)


#==============================================================#
#====================   Pages Actualités   ====================#
#==============================================================#
# Affiche la page listant toutes les informations.
@app.route("/informations/")
def informations():
    lesInformations = InformationBD.query.order_by(InformationBD.dateIN.desc(), InformationBD.heureIN.desc()).all()
    return render_template("informations.html", title=TITLE+"- Informations", informations=lesInformations)

@app.route("/admin/add_information/", methods=["GET", "POST"])
@login_required
@admin_required
def add_information():
    form = InformationForm()
    if form.validate_on_submit():
        now = datetime.now()
        nouvelle_info = InformationBD(
            titreIN=form.titre.data,
            contenuIN=form.contenu.data,
            dateIN=now.date(),
            heureIN=now.strftime('%H:%M')
        )
        try:
            db.session.add(nouvelle_info)
            db.session.commit()
            return redirect(url_for('informations'))
        except Exception as e:
            db.session.rollback()
    return render_template("admin_form_information.html", title="Ajouter une information", form=form)

@app.route("/admin/edit_information/<int:idI>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_information(idI):
    info = InformationBD.query.get_or_404(idI)
    form = InformationForm()
    if request.method == 'GET':
        form.titre.data = info.titreIN
        form.contenu.data = info.contenuIN
    if form.validate_on_submit():
        info.titreIN = form.titre.data
        info.contenuIN = form.contenu.data
        try:
            db.session.commit()
            return redirect(url_for('informations'))
        except Exception as e:
            db.session.rollback()
    return render_template("admin_form_information.html", title="Modifier une information", form=form)

@app.route("/admin/delete_information/<int:idI>", methods=["POST"])
@login_required
@admin_required
def delete_information(idI):
    info = InformationBD.query.get_or_404(idI)
    try:
        db.session.delete(info)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('informations'))

# Affiche la page listant tous les articles de presse.
@app.route("/presse/")
def presse():
    lesArticles = PresseBD.query.order_by(PresseBD.dateP.desc()).all()
    return render_template("presse.html",title=TITLE+"- Presse",articles = lesArticles)

@app.route("/admin/add_presse/", methods=["GET", "POST"])
@login_required
@admin_required
def add_presse():
    form = PresseForm()
    if form.validate_on_submit():
        now = datetime.now()
        nouveau_presse = PresseBD(
            titreP=form.titre.data,
            contenuP=form.contenu.data,
            lienP=form.lien.data,
            dateP=now.date(),
            heureP=now.strftime('%H:%M')
        )
        try:
            db.session.add(nouveau_presse)
            db.session.commit()
            return redirect(url_for('presse'))
        except Exception as e:
            db.session.rollback()
    return render_template("admin_form_presse.html", title="Ajouter un article de presse", form=form)

@app.route("/admin/edit_presse/<int:idP>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_presse(idP):
    article_presse = PresseBD.query.get_or_404(idP)
    form = PresseForm()
    if request.method == 'GET':
        # Pré-remplissage du formulaire
        form.titre.data = article_presse.titreP
        form.contenu.data = article_presse.contenuP
        form.lien.data = article_presse.lienP
    if form.validate_on_submit():
        article_presse.titreP = form.titre.data
        article_presse.contenuP = form.contenu.data
        article_presse.lienP = form.lien.data
        try:
            db.session.commit()
            return redirect(url_for('presse'))
        except Exception as e:
            db.session.rollback()
    return render_template("admin_form_presse.html", title="Modifier l'article de presse", form=form)

@app.route("/admin/delete_presse/<int:idP>", methods=["POST"])
@login_required
@admin_required
def delete_presse(idP):
    article_presse = PresseBD.query.get_or_404(idP)
    try:
        db.session.delete(article_presse)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('presse'))

@app.route("/articles/")
def articles():
    les_articles = ArticleBD.query.order_by(ArticleBD.date.desc()).all()
    return render_template("articles.html", title=TITLE+"- Articles du Club", articles=les_articles)

@app.route("/article/<int:idA>")
def article_detail(idA):
    article = ArticleBD.query.get_or_404(idA)
    return render_template("article_detail.html", title=article.titre, article=article)

@app.route("/admin/add_article/", methods=["GET", "POST"])
@login_required
@admin_required
def add_article():
    form = ArticleForm()
    if form.validate_on_submit():
        # Créer l'article en base pour avoir l'ID
        nouveau_article = ArticleBD(
            titre=form.titre.data,
            contenu=form.contenu.data,
            date=datetime.now().date()
        )
        db.session.add(nouveau_article)
        db.session.commit()
        # Gestion des images
        if form.images.data:
            # Création du chemin : static/images/articles/<ID_ARTICLE>
            dossier_article = os.path.join(app.root_path, 'static/images/articles', str(nouveau_article.id))
            # On crée le dossier s'il n'existe pas
            os.makedirs(dossier_article, exist_ok=True)
            for file in form.images.data:
                if file.filename:
                    filename = secure_filename(file.filename)
                    # Sauvegarde dans le sous-dossier
                    file.save(os.path.join(dossier_article, filename))
                    nouvelle_image = ImageArticleBD(nom=filename, id_article=nouveau_article.id)
                    db.session.add(nouvelle_image)
            db.session.commit()
        return redirect(url_for('articles'))
    return render_template("admin_form_article.html", title="Rédiger un article", form=form)

@app.route("/admin/edit_article/<int:idA>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_article(idA):
    article = ArticleBD.query.get_or_404(idA)
    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        article.titre = form.titre.data
        article.contenu = form.contenu.data
        if form.images.data:
            # Cible le dossier de l'article existant
            dossier_article = os.path.join(app.root_path, 'static/images/articles', str(article.id))
            os.makedirs(dossier_article, exist_ok=True)

            for file in form.images.data:
                if file.filename:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(dossier_article, filename))
                    nouvelle_image = ImageArticleBD(nom=filename, id_article=article.id)
                    db.session.add(nouvelle_image)
        db.session.commit()
        return redirect(url_for('articles'))
    return render_template("admin_form_article.html", title="Modifier un article", form=form, article=article)

@app.route("/admin/delete_article/<int:idA>", methods=["POST"])
@login_required
@admin_required
def delete_article(idA):
    article = ArticleBD.query.get_or_404(idA)
    # Suppression du dossier complet de l'article (images incluses)
    dossier_article = os.path.join(app.root_path, 'static/images/articles', str(article.id))
    if os.path.exists(dossier_article):
        # Supprime le dossier et tout ce qu'il contient
        shutil.rmtree(dossier_article)
    try:
        db.session.delete(article)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('articles'))

@app.route("/admin/delete_image_article/<int:idImg>", methods=["POST"])
@login_required
@admin_required
def delete_image_article(idImg):
    image = ImageArticleBD.query.get_or_404(idImg)
    article_id = image.id_article
    # On reconstruit le chemin avec l'ID de l'article
    chemin_image = os.path.join(app.root_path, 'static/images/articles', str(article_id), image.nom)
    try:
        if os.path.exists(chemin_image):
            os.remove(chemin_image)
    except:
        pass
    db.session.delete(image)
    db.session.commit()
    return redirect(url_for('edit_article', idA=article_id))

#============================================================#
#====================   Pages A propos   ====================#
#============================================================#
# Affiche la page de l'historique du club.
@app.route("/historique/")
def historique():
    return render_template("historique.html",title=TITLE+"- Historique")

# Affiche la page de présentation du comité directeur.
@app.route("/comite_cercle/")
def comite_cercle():
    comite = {
        "president": MembreBD.query.filter_by(statut='Président').first(),
        "vicePresident": MembreBD.query.filter_by(statut='Vice-Président').first(),
        "tresorier": MembreBD.query.filter_by(statut='Trésorier Général').first(),
        "secretaire": MembreBD.query.filter_by(statut='Secrétaire Générale').first()
    }
    membres = MembreBD.query.filter_by(statut='Membre du Comité').all()
    return render_template("comite_cercle.html", title=TITLE+"- Comité directeur du Cercle", comite=comite, membres=membres)

#==========================================================#
#====================   Page Contact   ====================#
#==========================================================#
# Affiche le formulaire de contact et traite sa soumission.
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

            # Création des notifications pour les administrateurs
            admins = AdminBD.query.all()
            type_f = form.type_form.data
            
            for admin in admins:
                params = admin.parametres_notif_admin
                if params:
                    notify = False
                    if type_f == 'Question' and params.formulaireQuestionSite:
                        notify = True
                    elif type_f == 'Demande' and params.formulaireDemandeSite:
                        notify = True
                    elif type_f == 'Signalement' and params.formulaireSignalementSite:
                        notify = True
                    
                    if notify:
                        notif = NotifsBD(
                            typeN="Formulaire Contact",
                            sourceN=f"{type_f} : {form.email.data}",
                            lue=False,
                            timestamp=datetime.now(),
                            link=url_for('formulaire_view', idFormulaire=nouveau_message.id),
                            idAdmin=admin.id
                        )
                        db.session.add(notif)
            db.session.commit()

            return redirect(url_for('contact'))
        except Exception as e:
            db.session.rollback()
    return render_template("contact.html", title=TITLE+"- Contact", form=form)


#==========================================================#
#====================   Pages Profil   ====================#
#==========================================================#
# Affiche les résultats de compétition du membre connecté.
@app.route("/resultat_membre/")
@login_required
@membre_required
def resultat_membre():
    les_resultats = ResultatBD.query.filter_by(id_membre=current_user.id).all()
    return render_template("resultat_membre.html", title=TITLE+"- Résultat du Membre", resultats=les_resultats)

# Affiche les événements auxquels le membre connecté est inscrit.
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

# Affiche le profil public d'un membre.
@app.route("/profil_view/<int:idM>")
def profil_view(idM):
    if not session.get("user_type") == "admin":
        if current_user.id != idM:
            abort(410)
    # origine corresponds à l'origine de l'utilisateur.
    origine = request.args.get('origine', 'gerer_profils')
    id_competition = request.args.get('idCompetition', type=int)
    id_event_club = request.args.get('idEventClub', type=int)
    unMembre = db.session.get(MembreBD,idM)
    return render_template("profil_view.html", title=TITLE + "- Profil Membre", selectedMembre=unMembre, origine=origine, idCompetition=id_competition, idEventClub=id_event_club)

#==============================================================#
#====================   Pages Menu Admin   ====================#
#==============================================================#
# Affiche les formulaires de contact non répondus - Réservée aux administrateurs.
@app.route("/gerer_formulaires/")
@login_required
@admin_required
def gerer_formulaires():
    filtre = FiltreForm(request.args if request.args else None)
    page = request.args.get('page', 1, type=int)
    liste = FormulaireBD.query\
        .filter(FormulaireBD.repondu == False)\
        .order_by(FormulaireBD.date.desc())

    if filtre.type_formulaire.data:
        liste = liste.filter(FormulaireBD.type.in_(filtre.type_formulaire.data))

    pagination = liste.paginate(page=page, per_page=15, error_out=False)
    return render_template("gerer_formulaires.html",
        title=TITLE + "- Gestion des Formulaires",pagination=pagination,filtre=filtre)

# Affiche les formulaires de contact déjà traités - Réservée aux administrateurs.
@app.route("/gerer_anciens_formulaires/")
@login_required
@admin_required
def gerer_anciens_formulaires():
    filtre = FiltreForm(request.args if request.args else None)
    page = request.args.get('page', 1, type=int)
    liste = db.session.query(FormulaireBD)\
        .filter(FormulaireBD.repondu == True)\
        .order_by(FormulaireBD.date.desc())

    if filtre.type_formulaire.data:
        liste = liste.filter(FormulaireBD.type.in_(filtre.type_formulaire.data))

    pagination = liste.paginate(page=page, per_page=15, error_out=False)
    return render_template("gerer_anciens_formulaires.html",
        title=TITLE + "- Gestion des Anciens Formulaires",pagination=pagination,filtre=filtre)

# Affiche le détail d'un formulaire de contact - Réservée aux administrateurs.
@app.route("/formulaire_view/<int:idFormulaire>")
@login_required
@admin_required
def formulaire_view(idFormulaire):
    unFormulaire = FormulaireBD.query.get_or_404(idFormulaire)
    return render_template("formulaire_view.html",title=TITLE+"- Consultation de Formulaire", selectedFormulaire=unFormulaire)

# Supprime un formulaire de contact - Réservée aux administrateurs.
@app.route("/formulaire_delete/<int:idFormulaire>", methods=['POST'])
@login_required
@admin_required
def formulaire_delete(idFormulaire):
    formulaire = FormulaireBD.query.get_or_404(idFormulaire)
    db.session.delete(formulaire)
    db.session.commit()
    return redirect(url_for('gerer_anciens_formulaires'))

# Permet de répondre à un formulaire et de le marquer comme traité - Réservée aux administrateurs.
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

# Affiche la liste des membres actifs pour la gestion - Réservée aux administrateurs.
@app.route("/gerer_profils/")
@login_required
@admin_required
def gerer_profils():
    filtre = FiltreForm(request.args if request.args else None)
    page = request.args.get('page', 1, type=int)
    liste = MembreBD.query\
        .filter(MembreBD.activite == True)\
        .order_by(MembreBD.date_inscription.desc())
    liste = liste.filter(MembreBD.sexe.in_(filtre.sexe.data))
    if filtre.niveau.data:
        liste = liste.filter(MembreBD.niveau.in_(filtre.niveau.data))
    if filtre.recherche.data:
        terme = f"%{filtre.recherche.data}%"
        liste = liste.filter(
            or_(
                MembreBD.nom.ilike(terme),
                MembreBD.prenom.ilike(terme),
                MembreBD.email.ilike(terme)
            )
        )
    # Maintenant .paginate() fonctionnera
    pagination = liste.paginate(page=page, per_page=15, error_out=False)
    return render_template("gerer_profils.html",
        title=TITLE + "- Gestion des Profils",pagination=pagination,filtre=filtre)

# Désactive le compte d'un membre.
@app.route('/gerer_profils/desinscrire/<int:idM>', methods=["GET", "POST"])
@login_required
def desinscrireMembre(idM):
    # On récupère le membre ciblé
    membre = db.session.get(MembreBD, idM)
    if not membre:
        abort(404)
    # Si ce n'est pas un admin, l'utilisateur ne peut cibler que lui-même.
    if session.get('user_type') != 'admin' and current_user.id != idM:
        abort(403)
    # Désactivation
    membre.activite = False
    membre.statut = "Ancien Membre"
    db.session.commit()
    # Redirection
    if current_user.id == idM:
        logout_user()
        flash("Votre compte a été désactivé avec succès.", "success")
        return redirect(url_for('index'))
    else:
        return redirect(url_for('gerer_profils'))

# Réactive le compte d'un ancien membre - Réservée aux administrateurs.
@app.route ('/gerer_anciens_profils/reinscrire/<int:idM>', methods =("POST" ,))
@login_required
@admin_required
def reinscrireMembre(idM):
    membre = db.session.get(MembreBD, idM)
    membre.activite = True
    membre.statut = "Membre"
    db.session.commit()
    return redirect(url_for('gerer_ancien_profils'))

# Affiche la liste des membres inactifs - Réservée aux administrateurs.
@app.route("/gerer_profils/ancien/")
@login_required
@admin_required
def gerer_ancien_profils():
    filtre = FiltreForm(request.args) if request.args else FiltreForm()
    page = request.args.get('page', 1, type=int)
    liste = MembreBD.query\
        .filter(MembreBD.activite == False)\
        .order_by(MembreBD.date_inscription.desc())

    liste = liste.filter(MembreBD.sexe.in_(filtre.sexe.data))
    if filtre.niveau.data:
        liste = liste.filter(MembreBD.niveau.in_(filtre.niveau.data))
    if filtre.recherche.data:
        terme = f"%{filtre.recherche.data}%"
        liste = liste.filter(
            or_(
                MembreBD.nom.ilike(terme),
                MembreBD.prenom.ilike(terme),
                MembreBD.email.ilike(terme)
            )
        )
    pagination = liste.paginate(page=page, per_page=15, error_out=False)
    return render_template("gerer_ancien_profils.html",
        title=TITLE + "- Gestion des Anciens Profils",pagination=pagination,filtre=filtre)

# Page de modification d'un profil, accessible par le membre lui-même ou un admin.
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
        # Création des notifications pour les administrateurs
            admins = AdminBD.query.all()
            
            for admin in admins:
                params = admin.parametres_notif_admin
                if params:
                    notify = False
                    if params.demandeModifSite:
                        notify = True
                    
                    if notify:
                        notif = NotifsBD(
                            typeN="Demande Modification",
                            sourceN=f"Modification : {unForm.email.data}",
                            lue=False,
                            timestamp=datetime.now(),
                            link=url_for('gerer_inscriptions', type='modification'),
                            idAdmin=admin.id
                        )
                        db.session.add(notif)
            db.session.commit()    
            return redirect(url_for('profil_view', idM=unMembre.id, origine='profil'))
    return render_template("profil_edit.html", title=TITLE + "- Modifier Profil", selectedMembre=unMembre, updateForm = unForm, origine = origine)

# Affiche les demandes d'inscription et de modification de profil - Réservée aux administrateurs.
@app.route("/gerer_inscriptions/")
@login_required
@admin_required
def gerer_inscriptions():
    page = request.args.get('page', 1, type=int)
    type_page = request.args.get('type',
                                 'inscription') 
    if type_page == 'modification':
        lesRequetes = ModifBD.query.order_by(ModifBD.date.asc())
    else:
        type_page = 'inscription'
        lesRequetes = InscriptionBD.query.order_by(
            InscriptionBD.date.asc())
    pagination = lesRequetes.paginate(page=page, per_page=7, error_out=False)
    return render_template("gerer_inscriptions.html",
                           title=TITLE + "- Gestion des Inscriptions",
                           pagination=pagination,
                           type_page=type_page)

# Accepte une demande d'inscription et crée un nouveau membre - Réservée aux administrateurs.
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
    nouveauNotif=ParametreNotifMembreBD(
        idMembre=nouveauMembre.id,
        eventInscriptionSite=True,
        evenementInscriptionMail=True,
        eventNouveauSite=True,
        eventNouveauMail=True,
        eventAnnulationSite=True,
        eventAnnulationMail=True,
        resultatNouveauSite=True,
        resultatNouveauMail=True,
        reponseFormulaireSite=True,
        reponseFormulaireMail=True,
        modifProfilSite=True,
        modifProfilMail=True
    )
    db.session.add(nouveauNotif)
    db.session.commit()
    nouveauMembre.idParaNotif = nouveauNotif.idParamNotifMembre
    db.session.commit()
    return redirect(url_for('gerer_inscriptions'))

# Accepte une demande de modification de profil - Réservée aux administrateurs.
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

# Refuse et supprime une demande d'inscription - Réservée aux administrateurs.
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

# Refuse et supprime une demande de modification - Réservée aux administrateurs.
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

@app.route("/admin/gestion_tarifs/", methods=["GET", "POST"])
@login_required
@admin_required
def gestion_tarifs():
    form = TarifForm()
    if form.validate_on_submit():
        nouveau_tarif = TarifBD(
            nom=form.nom.data,
            prix=form.prix.data,
            description=form.description.data,
            categorie=form.categorie.data
        )
        try:
            db.session.add(nouveau_tarif)
            db.session.commit()
            return redirect(url_for('gestion_tarifs'))
        except Exception as e:
            db.session.rollback()
    les_tarifs = TarifBD.query.order_by(TarifBD.categorie, TarifBD.prix).all()
    return render_template("admin_gestion_tarifs.html", title="Gestion Tarifs", form=form, tarifs=les_tarifs)

@app.route("/admin/delete_tarif/<int:idT>", methods=["POST"])
@login_required
@admin_required
def delete_tarif(idT):
    tarif = TarifBD.query.get_or_404(idT)
    try:
        db.session.delete(tarif)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('gestion_tarifs'))

@app.route("/admin/edit_tarif/<int:idT>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_tarif(idT):
    tarif = TarifBD.query.get_or_404(idT)
    form = TarifForm(obj=tarif)
    if form.validate_on_submit():
        form.populate_obj(tarif)
        db.session.commit()
        return redirect(url_for('gestion_tarifs'))
    return render_template("admin_edit_tarif.html", title="Modifier Tarif", form=form)


@app.route("/admin/gestion_horaires/", methods=["GET", "POST"])
@login_required
@admin_required
def gestion_horaires():
    form = HoraireForm()
    if form.validate_on_submit():
        nouveau_horaire = HoraireBD(
            jour=form.jour.data,
            heure_debut=form.heure_debut.data,
            heure_fin=form.heure_fin.data,
            activite=form.activite.data,
            details=form.details.data
        )
        try:
            db.session.add(nouveau_horaire)
            db.session.commit()
            return redirect(url_for('gestion_horaires'))
        except Exception as e:
            db.session.rollback()
    les_horaires = HoraireBD.query.all()
    ordre_jours = {'Lundi': 1, 'Mardi': 2, 'Mercredi': 3, 'Jeudi': 4, 'Vendredi': 5, 'Samedi': 6, 'Dimanche': 7}
    les_horaires.sort(key=lambda x: ordre_jours.get(x.jour, 8))
    return render_template("admin_gestion_horaires.html", title="Gestion Horaires", form=form, horaires=les_horaires)

@app.route("/admin/delete_horaire/<int:idH>", methods=["POST"])
@login_required
@admin_required
def delete_horaire(idH):
    horaire = HoraireBD.query.get_or_404(idH)
    try:
        db.session.delete(horaire)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('gestion_horaires'))

@app.route("/admin/edit_horaire/<int:idH>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_horaire(idH):
    horaire = HoraireBD.query.get_or_404(idH)
    form = HoraireForm(obj=horaire)
    if form.validate_on_submit():
        form.populate_obj(horaire)
        db.session.commit()
        return redirect(url_for('gestion_horaires'))
    return render_template("admin_edit_horaire.html", title="Modifier Horaire", form=form)

#==============================================================#
#====================   Pages Paramètres   ====================#
#==============================================================#
# Affiche la page des paramètres du compte (vue générale).
@app.route('/parametres/')
def parametres():
    form = ParametresForm()
    return render_template("parametres.html",
                         title=TITLE+"- Paramètres du Membre",
                         form=form)

# Gère les paramètres de notification pour les membres et les administrateurs.
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

# Permet à l'utilisateur connecté de changer son mot de passe.
@app.route("/changer_mdp/", methods=['GET', 'POST'])
@login_required
def changer_mdp():
    form = MdpChangeForm()
    if form.validate_on_submit():
        # verifie ancien mot de passe 
        if not check_password_hash(current_user.mdp_hash, form.old_password.data):
            flash("L'ancien mot de passe est incorrect.", 'danger')
            return redirect(url_for('changer_mdp'))
        # verifie correspondance
        if form.new_password.data != form.confirm_new_password.data:
            flash("Les nouveaux mots de passe ne correspondent pas.", 'danger')
            return redirect(url_for('changer_mdp'))
        # verifie si mdp fort
        if not est_mot_de_passe_fort(form.new_password.data):
             flash("Le mot de passe est trop faible (8 carac, Maj, min, chiffre, spécial requis).", 'danger')
             return redirect(url_for('changer_mdp'))
        # maj le mdp
        current_user.mdp_hash = generate_password_hash(form.new_password.data, method='pbkdf2:sha256')
        db.session.commit()
        flash("Votre mot de passe a été mis à jour avec succès.", 'success')
        return redirect(url_for('index'))
    return render_template("changer_mdp.html", form=form, title=TITLE+"- Changer mot de passe")

#=============================================================#
#====================   Pages Connexion   ====================#
#=============================================================#
# Gère la connexion des membres et des administrateurs.
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
        if not check_password_hash(utilisateur.mdp_hash, form.password.data):
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
        if check_password_hash(utilisateur.mdp_hash, form.password.data):
            return redirect(next_page) if next_page else redirect(url_for('index'))

    message = request.args.get('message')
    return render_template("login.html", title=TITLE + "- Connexion", form=form, message=message)

# Gère l'inscription de nouveaux utilisateurs (demande ou création directe par admin).
@app.route("/inscription/", methods=["GET", "POST"])
def inscription():
    unForm = InscriptionForm()
    if unForm.validate_on_submit():
        mdp_clair = unForm.password.data
        utilisateur_existant = MembreBD.query.filter_by(email=unForm.Login.data).first()
        demande_existante = InscriptionBD.query.filter_by(email=unForm.Login.data).first()
        if not est_mot_de_passe_fort(mdp_clair):
            # On renvoie une erreur si le mot de passe est trop faible
            return render_template("inscription.html",
                                   title=TITLE+"- Inscriptions",
                                   form=unForm,
                                   message_erreur="Le mot de passe doit contenir 8 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.")
        if not unForm.nom.data[0].isupper() or not unForm.prenom.data[0].isupper():
            #renvoie une erreur si le nom ou le prénom ne commence pas par une majuscule
            return render_template("inscription.html",
                                   title=TITLE+"- Inscriptions",
                                   form=unForm,
                                   erreur_nom ="le Nom et le Prénom doivent commencer par une majuscule.")
        if utilisateur_existant or demande_existante:
            return render_template("inscription.html",
                                  title = TITLE+"- Inscriptions",
                                  form = unForm,
                                  erreur_email= "L'email que vous avez rentrez est deja utilisé")
        try:
            if current_user.is_authenticated and session.get('user_type') == 'admin':
                nouveauMembre = MembreBD(
                    nom=unForm.nom.data,
                    prenom=unForm.prenom.data,
                    email=unForm.Login.data,
                    ddn=unForm.date_naissance.data,
                    sexe=unForm.sexe.data,
                    mdp_hash=generate_password_hash(unForm.password.data, method='pbkdf2:sha256')
                )
                db.session.add(nouveauMembre)
                db.session.commit()
                nouveauNotif=ParametreNotifMembreBD(
                    idMembre=nouveauMembre.id,
                    eventInscriptionSite=True,
                    evenementInscriptionMail=True,
                    eventNouveauSite=True,
                    eventNouveauMail=True,
                    eventAnnulationSite=True,
                    eventAnnulationMail=True,
                    resultatNouveauSite=True,
                    resultatNouveauMail=True,
                    reponseFormulaireSite=True,
                    reponseFormulaireMail=True,
                    modifProfilSite=True,
                    modifProfilMail=True
                )
                db.session.add(nouveauNotif)
                db.session.commit()
                nouveauMembre.idParaNotif = nouveauNotif.idParamNotifMembre
                db.session.commit()
                return redirect(url_for('gerer_profils'))
            else:
                nouvelle_inscription = InscriptionBD(
                    email=unForm.Login.data,           
                    nom=unForm.nom.data,
                    prenom=unForm.prenom.data,
                    ddn=unForm.date_naissance.data,
                    sexe=unForm.sexe.data,
                    mdp_hash= generate_password_hash(unForm.password.data,method='pbkdf2:sha256'),
                    date=datetime.now().date()
                )
                db.session.add(nouvelle_inscription)
                db.session.commit()

                # Création des notifications pour les administrateurs
                admins = AdminBD.query.all()
                
                for admin in admins:
                    params = admin.parametres_notif_admin
                    if params:
                        notify = False
                        if params.demandeInscriptionSite:
                            notify = True
                        
                        if notify:
                            notif = NotifsBD(
                                typeN="Demande Inscription",
                                sourceN=f"Inscription : {unForm.Login.data}",
                                lue=False,
                                timestamp=datetime.now(),
                                link=url_for('gerer_inscriptions', type='inscription'),
                                idAdmin=admin.id
                            )
                            db.session.add(notif)
                db.session.commit()    

                return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            print(f"ERREUR INSCRIPTION : {e}")
            # Affiche l'erreur sur la page pour que l'utilisateur sache ce qui se passe
            return render_template("inscription.html", 
                                   title=TITLE+"- Inscriptions", 
                                   form=unForm, 
                                   message_erreur=f"Erreur technique : {str(e)}")
    return render_template("inscription.html",title=TITLE+"- Inscriptions", form=unForm)

@app.route("/mdp_oublier/", methods=["GET", "POST"])
def mdp_oublier():
    form = MdpOublieForm()
    if form.validate_on_submit():
        email = form.email.data
        user = get_user_by_email(email)
        
        if user:
            token = s.dumps(email, salt='email-recover')
            link = url_for('reset_with_token', token=token, _external=True)
            
            # Simulation d'envoi 
            simuler_envoi_email(email, link)
        
        flash("Si cet email correspond à un compte, un lien de réinitialisation vous a été envoyé.", "info") 
        return redirect(url_for('login'))
    return render_template("mdp_oublier.html", title=TITLE + "- Mot de passe oublié", form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        # Cette ligne décode le token , récupère l’email qui y était stocké et vérifie que le token n’a pas été modifié / il a été généré avec le bon salt
        email = s.loads(token, salt='email-recover', max_age=3600) # 1 heure d'expiration
    except (SignatureExpired, Exception):
        flash("Le lien de réinitialisation est invalide ou a expiré.", "danger")
        return redirect(url_for('mdp_oublier'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = get_user_by_email(email)
        if user:
            if not est_mot_de_passe_fort(form.password.data):
                flash("Le mot de passe est trop faible (8 carac, Maj, min, chiffre, spécial requis).", 'danger')
                return render_template('reset_password.html', form=form, title="Réinitialisation mot de passe")
            
            user.mdp_hash = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            db.session.commit()
            flash("Votre mot de passe a été mis à jour avec succès.", "success")
            return redirect(url_for('login'))
        else:
            flash("Utilisateur introuvable.", "danger")
            return redirect(url_for('login'))
            
    return render_template('reset_password.html', form=form, title="Réinitialisation mot de passe")

# Déconnecte l'utilisateur.
@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


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

if __name__ == "__main__":
    app.run()
    db.close()

from .app import app, db
from flask import render_template, request, url_for, redirect, flash, session
from config import TITLE
from flask_login import logout_user, login_user, login_required, current_user
from .forms import LoginForm, EventForm,PasswordChangeForm,InscriptionForm, MembreForm
from .connexionPythonSQL import *

from monApp.modelBD import MembreBD,ReunionBD,CompetitionBD,InscriptionBD,AdminBD,EvenementBD,ParticiperBD

from datetime import datetime


from .forms import LoginForm, EventForm
from flask import jsonify
#from .models import Event

@app.route("/")
@app.route("/index/")
def index():
    return render_template("index.html", title = TITLE)

@app.route("/about/")
def about():
    return render_template("about.html",title=TITLE+"- A propos")

@app.route("/contact/")
def contact():
    return render_template("contact.html",title=TITLE+"- Conctact")

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
    return render_template("calendrier.html",title=TITLE+"- Calendrier")

@app.route("/competitions/")
def competitions():
    lesCompetitions = CompetitionBD.query.all()
    return render_template("competitions.html", title=TITLE+"- Competitions", competitions=lesCompetitions)

@app.route("/competitions/<int:idCompetition>/competition_view")
def competition_view(idCompetition):
    uneCompetition = CompetitionBD.query.get(idCompetition)
    return render_template("competition_view.html",title=TITLE+"- Consultation de la competition",selectedCompetition=uneCompetition)

@app.route("/competition_update/")
def competition_update():
    return render_template("competition_update.html",title=TITLE+"- Modification de la competition")

@app.route("/evenement_club/")
def evenement_club():
    return render_template("evenement_club.html",title=TITLE+"- Evenements du Club")

@app.route("/club_view/")
def club_view():
    return render_template("club_view.html",title=TITLE+"- un évenement du club")

@app.route("/club_update/")
def club_update():
    return render_template("club_update.html",title=TITLE+"- Modification d'un évenement du club")

@app.route("/reunion/")
def reunion():
    reunions = ReunionBD.query.all()
    today = datetime.now().date()
    prochaines_reunions = [r for r in reunions if r.dateRE and r.dateRE >= today]
    anciennes_reunions = [r for r in reunions if r.dateRE and r.dateRE < today]
    user_registered_event_ids = set()
    if current_user.is_authenticated and session.get('user_type') == 'membre':
        participations = ParticiperBD.query.filter_by(id_membre=current_user.id).all()
        user_registered_event_ids = {p.id_event for p in participations}
    return render_template("reunion.html", title=TITLE + "- Réunion", prochaines_reunions=prochaines_reunions, anciennes_reunions=anciennes_reunions,user_registered_event_ids = user_registered_event_ids)

@app.route("/reunion_view/<int:idReunion>")
def reunion_view(idReunion):
    reunion = ReunionBD.query.get(idReunion)
    return render_template("reunion_view.html",title=TITLE+"- Consultatiion d'une réunion", selectedReunion = reunion)

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
        # Pour la date, il faut la convertir de string en objet date
        reunion.dateRE = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        reunion.rapportRE = request.form['description']
        db.session.commit()
        flash('La réunion a été mise à jour avec succès.', 'success')
        return redirect(url_for('reunion_view', idReunion=reunion.id))
    return render_template("reunion_update.html", title=TITLE + "- Modification d'une réunion", reunion=reunion)

#Vues pour le Profil
@app.route("/resultat_membre/")
def resultat_membre():
    return render_template("resultat_membre.html",title=TITLE+"- Résultat du Membre")

@app.route("/evenement_membre/")
def evenement_membre():
    return render_template("evenement_membre.html",title=TITLE+"- Résultat du Membre")

@app.route('/parametres/')
def parametres():
    from .forms import ParametresForm
    form = ParametresForm()
    return render_template("parametres.html", 
                         title=TITLE+"- Paramètres du Membre", 
                         form=form)

@app.route('/parametres_update/')
def parametres_update():
    from .forms import Parametres_updateForm
    form = Parametres_updateForm()
    return render_template("parametres_update.html", 
                         title=TITLE+"- Paramètres du Membre", 
                         form=form)

@app.route("/changer_mdp/")
def changer_mdp():
    unForm = PasswordChangeForm()
    #Code à faire
    return render_template ("changer_mdp.html",form=unForm, title=TITLE+"- Changer mot de passe")


#Vues notification
@app.route("/parametres_notifs/")
def parametres_notifs():
    return render_template("parametres_notifs.html",title=TITLE+"- Paramètres notifications")

#Vues pour Article 
@app.route("/articles/")
def articles():
    return render_template("articles.html",title=TITLE+"- Articles")

#Vues pour Admin
@app.route("/gerer_formulaires/")
def gerer_formulaires():
    return render_template("gerer_formulaires.html",title=TITLE+"- Géstion des Formulaires")

@app.route("/formulaire_view/")
def formulaire_view():
    return render_template("formulaire_view.html",title=TITLE+"- Consultation de Formulaire")


#Vue pour la gestion des Profils
@app.route("/gerer_profils/")
def gerer_profils():
    # On commence la requête de base pour les membres actifs
    query = db.session.query(MembreBD).filter(MembreBD.activite == True)

    # On récupère les arguments de la requête GET
    search_term = request.args.get('recherche')
    sexes = request.args.getlist('sexe')
    niveaux = request.args.getlist('niveau')

    # Filtrage par barre de recherche (nom, prénom, email)
    if search_term:
        search_like = f"%{search_term}%"
        query = query.filter(
            db.or_(
                MembreBD.nom.like(search_like),
                MembreBD.prenom.like(search_like),
                MembreBD.email.like(search_like)
            )
        )

    # Filtrage par sexe
    if sexes:
        query = query.filter(MembreBD.sexe.in_(sexes))

    # Filtrage par niveau
    if niveaux:
        query = query.filter(MembreBD.niveau.in_(niveaux))

    lesMembres = query.all()
    return render_template("gerer_profils.html",title=TITLE+"- Géstion des Profils", membres = lesMembres, filtres=request.args)

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
        unForm.populate_obj(unMembre)
        db.session.commit()
        return redirect(url_for('gerer_profils'))
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




@app.route("/gerer_inscriptions/")
def gerer_inscriptions():
    return render_template("gerer_inscriptions.html",title=TITLE+"- Géstion des Inscriptions")



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

@app.route("/inscription/", methods=["GET", "POST"])  # Accepte GET et POST
def inscription():
    unForm = InscriptionForm()
    if unForm.validate_on_submit():
        existing_inscription = db.session.scalar(
            db.select(InscriptionBD).where(InscriptionBD.email == unForm.Login.data)
        )
        existing_membre = db.session.scalar(
            db.select(MembreBD).where(MembreBD.email == unForm.Login.data)
        )
        if existing_inscription or existing_membre:
            return render_template("inscription.html", title=TITLE+"- Inscriptions", form=unForm)
        if unForm.password.data != unForm.confirm_password.data:
            return render_template("inscription.html", title=TITLE+"- Inscriptions", form=unForm)
        new_inscription = InscriptionBD(
            email=unForm.Login.data,           
            nom=unForm.nom.data,
            prenom=unForm.prenom.data,
            ddn=unForm.date_naissance.data,
            sexe=unForm.sexe.data,
            mdp_hash=unForm.password.data,
            acceptee=False
        )
        try:
            db.session.add(new_inscription)
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

# Route pour ajouter un événement
@app.route("/add_event/", methods=["GET", "POST"])
# @login_required # Décommentez cette ligne si vous voulez que seuls les utilisateurs connectés puissent ajouter des événements
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        new_event = Event(
            title=form.title.data,
            start=form.start_date.data,
            end=form.end_date.data if form.end_date.data else None,
            description=form.description.data,
            category=form.category.data,
            level=", ".join(form.level.data)
        )
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('calendrier'))
    return render_template("add_event.html", title=TITLE + "- Ajouter un événement", form=form)

##Vue pour Calendrier 
#@app.route('/api/events')
#def get_events():
#    #events = Event.query.all()
#    events_data = []
#    for event in events:
#        events_data.append(event.to_dict())
#    return jsonify(events_data)


if __name__ == "__main__":
    app.run()
    db.close()

from .app import app, db
from flask import render_template, request, url_for, redirect, flash
from config import TITLE
from flask_login import logout_user, login_user, login_required
from .forms import LoginForm, EventForm,PasswordChangeForm,InscriptionForm
from .connexionPythonSQL import *
from monApp.modelBD import MembreBD,Reunion

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
    return render_template("competitions.html",title=TITLE+"- Competitions")

@app.route("/competition_view/")
def competition_view():
    return render_template("competition_view.html",title=TITLE+"- Consultation de la competition")

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
    reunions = Reunion.query.all()
    today = datetime.now().date() #on s'assure d'avoir un objet date
    prochaines_reunions = [r for r in reunions if r.dateRE and r.dateRE >= today]
    anciennes_reunions = [r for r in reunions if r.dateRE and r.dateRE < today]
    return render_template("reunion.html", title=TITLE + "- Réunion", prochaines_reunions=prochaines_reunions, anciennes_reunions=anciennes_reunions)

@app.route("/reunion_view/<int:idReunion>")
def reunion_view(idReunion):
    reunion = Reunion.query.get(idReunion)
    return render_template("reunion_view.html",title=TITLE+"- Consultatiion d'une réunion", selectedReunion = reunion)

@app.route("/reunion_delete/<int:idReunion>", methods=['POST'])
def reunion_delete(idReunion):
    reunion = Reunion.query.get_or_404(idReunion)
    db.session.delete(reunion)
    db.session.commit()
    flash('La réunion a été supprimée avec succès.', 'success')
    return redirect(url_for('reunion'))


@app.route("/reunion_update/<int:idReunion>", methods=['GET', 'POST'])
def reunion_update(idReunion):
    reunion = Reunion.query.get_or_404(idReunion)
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

@app.route("/gerer_profils/")
def gerer_profils():
    lesMembres = db.session.query(MembreBD).all()
    return render_template("gerer_profils.html",title=TITLE+"- Géstion des Profils", membres = lesMembres)

@app.route("/gerer_ancier_profils/")
def gerer_ancier_profils():
    return render_template("gerer_ancier_profils.html",title=TITLE+"- Géstion des Anciens Profils")

@app.route("/profil_view/<int:user_id>")
def profil_view(user_id):
    current_user = {
        'id': user_id,
        'nom': 'Doe',
        'prenom': 'John',
        'age': 30,
        'date_naissance': '15/05/1994',
        'sexe': 'Homme',
        'date_inscription': '15/05/2023',
        'categorie': 'Senior',
        'niveau': 'National',
        'email': 'john.doe@example.com',
        'statut': 'Membre Actif'
    }
    return render_template("profil_view.html", title=TITLE + "- Profil Membre", user=current_user)

@app.route("/profil_edit/<int:user_id>", methods=["GET", "POST"])
def profil_edit(user_id):
    current_user = {
        'id': user_id,
        'nom': 'Doe',
        'prenom': 'John',
        'age': 30,
        'date_naissance': '1994-05-15',
        'categorie': 'Senior',
        'niveau': 'National',
        'email': 'john.doe@example.com',
        'statut': 'Membre Actif'
    }

    return render_template("profil_edit.html", title=TITLE + "- Modifier Profil", user=current_user)

@app.route("/gerer_inscriptions/")
def gerer_inscriptions():
    return render_template("gerer_inscriptions.html",title=TITLE+"- Géstion des Inscriptions")



#Vues pour le login 
@app.route ("/login/", methods =("GET","POST"))
def login():
    unForm = LoginForm()
    unUser=None
    if not unForm.is_submitted():
        unForm.next.data = request.args.get('next')
    elif unForm.validate_on_submit():
        unUser = unForm.get_authenticated_user()
        if unUser:
            login_user(unUser)
            next = unForm.next.data or url_for("index",name=unUser.Login)
            return redirect(next)
    return render_template ("login.html",form=unForm) 

@app.route("/inscription/")
def inscription():
    unForm = InscriptionForm()
    return render_template("inscription.html",title=TITLE+"- Inscriptions", form=unForm)

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
        flash('Événement ajouté avec succès!', 'success') # Vous pouvez afficher un message de succès
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

from .app import app, db
from flask import render_template, request,url_for , redirect
from config import TITLE
from flask_login import logout_user, login_user, login_required
from .forms import LoginForm


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

#Vue pour les Evenements 
@app.route("/calendrier/")
def calendrier():
    return render_template("calendrier.html",title=TITLE+"- Calendrier")

@app.route("/competitions/")
def competitions():
    return render_template("competitions.html",title=TITLE+"- Competitions")

@app.route("/competition_view/")
def competition_view():
    return render_template("competition_view.html",title=TITLE+"- Competition")

@app.route("/evenement_club/")
def evenement_club():
    return render_template("evenement_club.html",title=TITLE+"- Evenement du Club")

@app.route("/reunion/")
def reunion():
    return render_template("reunion.html",title=TITLE+"- Reunion")


#Vue pour le Profil
@app.route("/resultat_membre/")
def resultat_membre():
    return render_template("resultat_membre.html",title=TITLE+"- Résultat du Membre")

@app.route("/evenement_membre/")
def evenement_membre():
    return render_template("evenement_membre.html",title=TITLE+"- Résultat du Membre")

@app.route("/parametres/")
def parametres():
    return render_template("parametres.html",title=TITLE+"- Paramètres du Membre")

#Vue notification
@app.route("/notifications/")
def notifications():
    return render_template("notifications.html",title=TITLE+"- Notifications")

#Vue pour Article 
@app.route("/articles/")
def articles():
    return render_template("articles.html",title=TITLE+"- Articles")


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
 
if __name__ == "__main__":
    app.run()

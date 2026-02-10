from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from flask_login import current_user
from datetime import datetime, date

from monApp.app import db
from monApp.forms import ContactForm
from monApp.models import (PresseBD, InformationBD, CompetitionBD, MembreBD, 
                            AdminBD, FormulaireBD, RemplirBD, NotifsBD, 
                            HoraireBD, TarifBD)
from config import TITLE

general_bp = Blueprint('general', __name__)

#==========================================================#
#====================   Page Accueil   ====================#
#==========================================================#

@general_bp.route("/")
@general_bp.route("/index/")
def index():
    les_derniers_articles = PresseBD.query.order_by(PresseBD.dateP.desc()).limit(3).all()
    les_dernieres_informations = InformationBD.query.order_by(InformationBD.dateIN.desc()).limit(3).all()
    les_dernieres_competitions = CompetitionBD.query.filter_by(passee=True).order_by(CompetitionBD.date_debut.desc()).limit(3).all()
    return render_template("generals/index.html", title=TITLE, articles=les_derniers_articles, informations=les_dernieres_informations, competitions=les_dernieres_competitions)

#==================================================================#
#====================   Pages Renseignements   ====================#
#==================================================================#

@general_bp.route("/adresse/")
def adresse():
    return render_template("generals/adresse.html",title=TITLE+"- Adresse")

@general_bp.route("/horaires/")
def horaires():
    les_horaires = HoraireBD.query.all()
    ordre_jours = {
        'Lundi': 1, 'Mardi': 2, 'Mercredi': 3, 'Jeudi': 4,
        'Vendredi': 5, 'Samedi': 6, 'Dimanche': 7
    }
    les_horaires.sort(key=lambda x: (ordre_jours.get(x.jour, 8), x.heure_debut))
    return render_template("generals/horaire.html", title=TITLE+"- Horaires", horaires=les_horaires)

@general_bp.route("/adhesions/")
def adhesions():
    tarifs_adhesion = TarifBD.query.filter_by(categorie='Adhesion').all()
    return render_template("generals/adhesion.html", title=TITLE+"- Adhésions", tarifs=tarifs_adhesion)

@general_bp.route("/materiel/")
def materiel():
    tarifs_materiel = TarifBD.query.filter_by(categorie='Materiel').all()
    return render_template("generals/materiel.html", title=TITLE+"- Matériel et tenues", tarifs=tarifs_materiel)

#==================================================================#
#====================   Pages Escrim feminin   ====================#
#==================================================================#

@general_bp.route("/escrime-feminin/")
def escrime_feminin():
    return render_template("generals/escrime_feminin.html",title=TITLE+"- L'escrime Féminin")

#==========================================================#
#====================   Page Contact   ====================#
#==========================================================#

@general_bp.route("/contact/", methods=("GET", "POST",))
def contact():
    admin = AdminBD.query.first()
    mail_question = admin.formulaireQuestionMail if admin else False
    mail_demande = admin.formulaireDemandeMail if admin else False
    mail_signalement = admin.formulaireSignalementMail if admin else False
    form = ContactForm()
    if form.validate_on_submit():
        type_f = form.type_form.data
        sujet = form.sujet.data
        email = form.email.data
        description = form.description.data
        nouveau_formulaire = FormulaireBD(
            type=type_f,
            sujet=sujet,
            email=email,
            description=description,
            date=date.today(),
            repondu=False
        )
        if current_user.is_authenticated and session.get('user_type') == 'membre':
            nouveau_formulaire.idMembre = current_user.id
            remplir = RemplirBD(id_membre=current_user.id)
            nouveau_formulaire.remplissages.append(remplir)
        db.session.add(nouveau_formulaire)
        
        if admin:
            notify_site = False
            if type_f == 'Question' and admin.formulaireQuestionSite:
                notify_site = True
            elif type_f == 'Demande' and admin.formulaireDemandeSite:
                notify_site = True
            elif type_f == 'Signalement' and admin.formulaireSignalementSite:
                notify_site = True     
            if notify_site:
                notif = NotifsBD(
                    typeN='formulaire',
                    sourceN=f"Nouveau formulaire ({type_f}) de {email}",
                    lue=False,
                    timestamp=datetime.now(),
                    idAdmin=admin.id,
                    link=url_for('admin.gerer_formulaires', _external=True)
                )
                db.session.add(notif)
        db.session.commit()
        flash('Votre message a bien été envoyé.', 'success')
        return redirect(url_for('general.contact'))
    return render_template("generals/contact.html", 
                           form=form, 
                           title=TITLE+"- Contact",
                           mail_question=mail_question,
                           mail_demande=mail_demande,
                           mail_signalement=mail_signalement)

#============================================================#
#====================   Pages A propos   ====================#
#============================================================#

@general_bp.route("/historique/")
def historique():
    return render_template("generals/historique.html",title=TITLE+"- Historique")

@general_bp.route("/comite_cercle/")
def comite_cercle():
    comite = {
        "president": MembreBD.query.filter_by(statut='Président').first(),
        "vicePresident": MembreBD.query.filter_by(statut='Vice-Président').first(),
        "tresorier": MembreBD.query.filter_by(statut='Trésorier Général').first(),
        "secretaire": MembreBD.query.filter_by(statut='Secrétaire Générale').first()
    }
    membres = MembreBD.query.filter_by(statut='Membre du Comité').all()
    return render_template("generals/comite_cercle.html", title=TITLE+"- Comité directeur du Cercle", comite=comite, membres=membres)
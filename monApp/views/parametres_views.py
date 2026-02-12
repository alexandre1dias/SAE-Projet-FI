from flask import Blueprint, render_template, request, url_for, redirect, session, flash, jsonify, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from monApp.app import app, db
from monApp.forms import ParametresForm, MdpChangeForm
from monApp.models import *
from monApp.services import est_mot_de_passe_fort
from config import TITLE

# Création du Blueprint
parametres_bp = Blueprint('parametres', __name__)

#==============================================================#
#====================   Pages Paramètres   ====================#
#==============================================================#


@parametres_bp.route('/parametres/')
def parametres():
    form = ParametresForm()
    return render_template("parametres/parametres.html",
                           title=TITLE + "- Paramètres du Membre",
                           form=form)


@parametres_bp.route("/parametres_notifs/", methods=["GET", "POST"])
@login_required
def parametres_notifs():
    """
    Gère les préférences de notifications pour Membres et Admins.
    """
    if request.method == 'POST':
        user_type = session.get('user_type')
        if user_type == 'membre':
            current_user.eventInscriptionSite = 'event_insc_site' in request.form
            current_user.evenementInscriptionMail = 'event_insc_mail' in request.form
            current_user.eventNouveauSite = 'event_new_site' in request.form
            current_user.eventNouveauMail = 'event_new_mail' in request.form
            current_user.eventAnnulationSite = 'event_cancel_site' in request.form
            current_user.eventAnnulationMail = 'event_cancel_mail' in request.form
            current_user.resultatNouveauSite = 'result_new_site' in request.form
            current_user.resultatNouveauMail = 'result_new_mail' in request.form
            current_user.reponseFormulaireSite = 'form_resp_site' in request.form
            current_user.reponseFormulaireMail = 'form_resp_mail' in request.form
            current_user.modifProfilSite = 'profile_mod_site' in request.form
            current_user.modifProfilMail = 'profile_mod_mail' in request.form
        elif user_type == 'admin':
            current_user.formulaireDemandeSite = 'form_req_site' in request.form
            current_user.formulaireDemandeMail = 'form_req_mail' in request.form
            current_user.formulaireQuestionSite = 'form_question_site' in request.form
            current_user.formulaireQuestionMail = 'form_question_mail' in request.form
            current_user.formulaireSignalementSite = 'form_report_site' in request.form
            current_user.formulaireSignalementMail = 'form_report_mail' in request.form
            current_user.demandeModifSite = 'profile_change_site' in request.form
            current_user.demandeModifMail = 'profile_change_mail' in request.form
            current_user.demandeInscriptionSite = 'signup_req_site' in request.form
            current_user.demandeInscriptionMail = 'signup_req_mail' in request.form

        db.session.commit()
        return redirect(url_for('parametres.parametres_notifs'))
    return render_template("parametres/parametres_notifs.html",
                           title=TITLE + "- Paramètres notifications",
                           parametres=current_user)


@parametres_bp.route("/changer_mdp/", methods=['GET', 'POST'])
@login_required
def changer_mdp():
    form = MdpChangeForm()
    if form.validate_on_submit():
        if not check_password_hash(current_user.mdp_hash,
                                   form.old_password.data):
            flash("L'ancien mot de passe est incorrect.", 'danger')
            return redirect(url_for('parametres.changer_mdp'))
        if form.new_password.data != form.confirm_new_password.data:
            flash("Les nouveaux mots de passe ne correspondent pas.", 'danger')
            return redirect(url_for('parametres.changer_mdp'))
        if not est_mot_de_passe_fort(form.new_password.data):
            flash(
                "Le mot de passe est trop faible (8 carac, Maj, min, chiffre, spécial requis).",
                'danger')
            return redirect(url_for('parametres.changer_mdp'))

        current_user.mdp_hash = generate_password_hash(form.new_password.data,
                                                       method='pbkdf2:sha256')
        db.session.commit()
        flash("Votre mot de passe a été mis à jour avec succès.", 'success')
        return redirect(url_for('general.index'))
    return render_template("parametres/changer_mdp.html",
                           form=form,
                           title=TITLE + "- Changer mot de passe")

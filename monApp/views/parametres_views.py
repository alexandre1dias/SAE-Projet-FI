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

@app.route("/parametres_notifs/", methods=["GET", "POST"])
@login_required
def parametres_notifs():
    """
    Gère les préférences de notifications pour Membres et Admins.
    Les champs sont maintenant mis à jour directement sur current_user.
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
        return redirect(url_for('parametres_notifs'))
    return render_template("parametres_notifs.html", title=TITLE+"- Paramètres notifications", parametres=current_user)

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
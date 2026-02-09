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
        if utilisateur_existant or demande_existante:
            return render_template("inscription.html",
                                  title = TITLE+"- Inscriptions",
                                  form = unForm,
                                  erreur_email= "L'email que vous avez rentrez est deja utilisé")
        try:
            if current_user.is_authenticated and session.get('user_type') == 'admin':
                nouveauMembre = MembreBD(
                    nom=unForm.nom.data.capitalize(),
                    prenom=unForm.prenom.data.capitalize(),
                    email=unForm.Login.data,
                    ddn=unForm.date_naissance.data,
                    sexe=unForm.sexe.data,
                    numTel=unForm.numTel.data,
                    mdp_hash=generate_password_hash(unForm.password.data, method='pbkdf2:sha256'),
                    # Initialisation directe des notifications
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
                db.session.add(nouveauMembre)
                db.session.commit()
                return redirect(url_for('gerer_profils'))
            else:
                nouvelle_inscription = InscriptionBD(
                    email=unForm.Login.data,
                    nom=unForm.nom.data.capitalize(),
                    prenom=unForm.prenom.data.capitalize(),
                    ddn=unForm.date_naissance.data,
                    sexe=unForm.sexe.data,
                    numTel=unForm.numTel.data,
                    mdp_hash= generate_password_hash(unForm.password.data,method='pbkdf2:sha256'),
                    date=datetime.now().date()
                )
                db.session.add(nouvelle_inscription)
                db.session.commit()

                # Création des notifications pour les administrateurs
                admins = AdminBD.query.all()

                for admin in admins:
                    notify = False
                    if admin.demandeInscriptionSite:
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
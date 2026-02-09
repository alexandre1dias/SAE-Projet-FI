from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from flask_login import logout_user, login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import SignatureExpired
from datetime import datetime
from monApp.app import db
from monApp.forms import LoginForm, InscriptionForm, MdpOublieForm, ResetPasswordForm
from monApp.models import MembreBD, AdminBD, InscriptionBD, NotifsBD
from monApp.services import est_mot_de_passe_fort, get_user_by_email, s, simuler_envoi_email
from config import TITLE

auth_bp = Blueprint('auth', __name__)

#=============================================================#
#====================   Pages Connexion   ====================#
#=============================================================#

@auth_bp.route("/login/", methods=("GET","POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('general.index'))

    form = LoginForm()
    if form.validate_on_submit():
        utilisateur = MembreBD.query.filter_by(email=form.email.data).first()
        est_admin = False

        if utilisateur is None:
            utilisateur = AdminBD.query.filter_by(email=form.email.data).first()
            est_admin = True

        if utilisateur is None:
            return redirect(url_for('auth.login', message="emailIncorrect"))

        if not check_password_hash(utilisateur.mdp_hash, form.password.data):
            return redirect(url_for('auth.login', message="mdpIncorrect"))

        if not est_admin and not utilisateur.activite:
            return redirect(url_for('auth.login', message="desincrit"))

        login_user(utilisateur)
        session['user_type'] = 'admin' if est_admin else 'membre'
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('general.index'))

    message = request.args.get('message')
    return render_template("authentifications/login.html", title=TITLE + "- Connexion", form=form, message=message)

@auth_bp.route("/inscription/", methods=["GET", "POST"])
def inscription():
    unForm = InscriptionForm()
    if unForm.validate_on_submit():
        mdp_clair = unForm.password.data
        utilisateur_existant = MembreBD.query.filter_by(email=unForm.Login.data).first()
        demande_existante = InscriptionBD.query.filter_by(email=unForm.Login.data).first()
        
        if not est_mot_de_passe_fort(mdp_clair):
            return render_template("authentifications/inscription.html",
                                   title=TITLE+"- Inscriptions",
                                   form=unForm,
                                   message_erreur="Le mot de passe doit contenir 8 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.")
        if utilisateur_existant or demande_existante:
            return render_template("authentifications/inscription.html",
                                  title=TITLE+"- Inscriptions",
                                  form=unForm,
                                  erreur_email="L'email que vous avez rentré est déjà utilisé")
        try:
            # Création directe par un admin
            if current_user.is_authenticated and session.get('user_type') == 'admin':
                nouveauMembre = MembreBD(
                    nom=unForm.nom.data.capitalize(),
                    prenom=unForm.prenom.data.capitalize(),
                    email=unForm.Login.data,
                    ddn=unForm.date_naissance.data,
                    sexe=unForm.sexe.data,
                    numTel=unForm.numTel.data,
                    mdp_hash=generate_password_hash(unForm.password.data, method='pbkdf2:sha256'),
                    # CORRECTION: On applique les propriétés à nouveauMembre, pas current_user (l'admin)
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
                    modifProfilMail=True,
                    activite=True
                )
                db.session.add(nouveauMembre)
                db.session.commit()
                return redirect(url_for('admin.gerer_profils'))
            
            # Demande d'inscription (visiteur)
            else:
                nouvelle_inscription = InscriptionBD(
                    email=unForm.Login.data,
                    nom=unForm.nom.data.capitalize(),
                    prenom=unForm.prenom.data.capitalize(),
                    ddn=unForm.date_naissance.data,
                    sexe=unForm.sexe.data,
                    numTel=unForm.numTel.data,
                    mdp_hash=generate_password_hash(unForm.password.data, method='pbkdf2:sha256'),
                    date=datetime.now().date()
                )
                db.session.add(nouvelle_inscription)
                db.session.commit()

                admins = AdminBD.query.all()
                for admin in admins:
                    if admin.demandeInscriptionSite:
                        notif = NotifsBD(
                            typeN="Demande Inscription",
                            sourceN=f"Inscription : {unForm.Login.data}",
                            lue=False,
                            timestamp=datetime.now(),
                            link=url_for('admin.gerer_inscriptions', type='inscription'),
                            idAdmin=admin.id
                        )
                        db.session.add(notif)
                db.session.commit()

                return redirect(url_for('general.index'))
        except Exception as e:
            db.session.rollback()
            print(f"ERREUR INSCRIPTION : {e}")
            return render_template("authentifications/inscription.html",
                                   title=TITLE+"- Inscriptions",
                                   form=unForm,
                                   message_erreur=f"Erreur technique : {str(e)}")
    return render_template("authentifications/inscription.html", title=TITLE+"- Inscriptions", form=unForm)

@auth_bp.route("/mdp_oublier/", methods=["GET", "POST"])
def mdp_oublier():
    form = MdpOublieForm()
    if form.validate_on_submit():
        email = form.email.data
        user = get_user_by_email(email)

        if user:
            token = s.dumps(email, salt='email-recover')
            link = url_for('auth.reset_with_token', token=token, _external=True)
            simuler_envoi_email(email, link)

        flash("Si cet email correspond à un compte, un lien de réinitialisation vous a été envoyé.", "info")
        return redirect(url_for('auth.login'))
    return render_template("authentifications/mdp_oublier.html", title=TITLE + "- Mot de passe oublié", form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        email = s.loads(token, salt='email-recover', max_age=3600)
    except (SignatureExpired, Exception):
        flash("Le lien de réinitialisation est invalide ou a expiré.", "danger")
        return redirect(url_for('auth.mdp_oublier'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = get_user_by_email(email)
        if user:
            if not est_mot_de_passe_fort(form.password.data):
                flash("Le mot de passe est trop faible (8 carac, Maj, min, chiffre, spécial requis).", 'danger')
                return render_template('authentifications/reset_password.html', form=form, title="Réinitialisation mot de passe")

            user.mdp_hash = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            db.session.commit()
            flash("Votre mot de passe a été mis à jour avec succès.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("Utilisateur introuvable.", "danger")
            return redirect(url_for('auth.login'))

    return render_template('authentifications/reset_password.html', form=form, title="Réinitialisation mot de passe")

@auth_bp.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('general.index'))
from flask import Blueprint, render_template, request, url_for, redirect, session, flash, jsonify, abort
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date
from sqlalchemy import or_
import shutil
import os

from monApp.app import app, db
from monApp.forms import *
from monApp.models import *
from monApp.services import *
from monApp.gestion_erreurs import *
from config import TITLE, AUJOURDHUI

# Création du Blueprint
admin_bp = Blueprint('admin', __name__)

#==============================================================#
#====================   Pages Menu Admin   ====================#
#==============================================================#
# Affiche les formulaires de contact non répondus - Réservée aux administrateurs.
@admin_bp.route("/gerer_formulaires/")
@login_required
@admin_required
def gerer_formulaires():
    mode = request.args.get('mode', 'attente')
    repondu = (mode == 'repondus')
    filtre = FiltreForm(request.args if request.args else None)
    page = request.args.get('page', 1, type=int)
    filtre.tri.choices = [('date_desc', 'Plus récent'),
                          ('date_asc', 'Plus ancien')]
    
    liste = FormulaireBD.query.filter(FormulaireBD.repondu == repondu)
    if filtre.type_formulaire.data:
        liste = liste.filter(FormulaireBD.type.in_(filtre.type_formulaire.data))
    if filtre.tri.data == 'date_asc':
        liste = liste.order_by(FormulaireBD.date.asc())
    else:
        liste = liste.order_by(FormulaireBD.date.desc())
    
    pagination = liste.paginate(page=page, per_page=15, error_out=False)
    return render_template("gerer_formulaires.html",
        title=TITLE + " - Gestion des Formulaires",
        pagination=pagination,
        filtre=filtre,
        mode=mode)

# Affiche le détail d'un formulaire de contact - Réservée aux administrateurs.
@admin_bp.route("/formulaire_view/<int:idFormulaire>")
@login_required
@admin_required
def formulaire_view(idFormulaire):
    unFormulaire = FormulaireBD.query.get_or_404(idFormulaire)
    return render_template("formulaire_view.html",title=TITLE+"- Consultation de Formulaire", selectedFormulaire=unFormulaire)

# Supprime un formulaire de contact - Réservée aux administrateurs.
@admin_bp.route("/formulaire_delete/<int:idFormulaire>", methods=['POST'])
@login_required
@admin_required
def formulaire_delete(idFormulaire):
    formulaire = FormulaireBD.query.get_or_404(idFormulaire)
    db.session.delete(formulaire)
    db.session.commit()
    return redirect(url_for('admin.gerer_formulaires'))

# Permet de récupérer le contenue de la réponse
@admin_bp.route("/api/get_reponse/<int:idFormulaire>")
@login_required
def api_get_reponse(idFormulaire):
    """API pour récupérer la réponse d'un formulaire sans recharger la page"""
    formulaire = FormulaireBD.query.get_or_404(idFormulaire)
    if session.get('user_type') == 'membre' and formulaire.idMembre != current_user.id:
        return jsonify({'error': 'Non autorisé'}), 403
    return jsonify({
        'sujet': formulaire.sujet,
        'reponse': formulaire.reponse,
        'date': formulaire.date.strftime('%d/%m/%Y') if formulaire.date else 'Date inconnue'
    })

# Permet à répondre à un formulaire et de le marquer comme traité - Réservée aux administrateurs.
@admin_bp.route("/repondre_formulaire/<int:idFormulaire>", methods=['POST'])
@login_required
@admin_required
def repondre_formulaire(idFormulaire):
    reponse = request.form.get('reponse')
    leFormulaire = FormulaireBD.query.get_or_404(idFormulaire)
    leFormulaire.reponse = reponse
    leFormulaire.repondu = True
    if leFormulaire.membre and leFormulaire.membre.reponseFormulaireSite:
        link_special = f"#view_response_{leFormulaire.id}"
        notif = NotifsBD(
            typeN='Réponse Formulaire',
            sourceN=f"Réponse à : {leFormulaire.sujet}",
            lue=False,
            timestamp=datetime.now(),
            idMembre=leFormulaire.membre.id,
            link=link_special
        )
        db.session.add(notif)
    db.session.commit()
    return redirect(url_for('admin.gerer_formulaires'))

# Affiche la liste des membres actifs pour la gestion - Réservée aux administrateurs.
@admin_bp.route("/gerer_profils/")
@login_required
@admin_required
def gerer_profils():
    # Récupération du mode
    mode = request.args.get('mode', 'actifs')
    ancien = (mode == 'anciens')
    
    filtre = FiltreForm(request.args if request.args else None)
    page = request.args.get('page', 1, type=int)
    
    # Configuration des choix de tri
    filtre.tri.choices = [('date_desc', 'Plus récent'), ('date_asc', 'Plus ancien'),
                ('nom_asc', 'Nom A-Z'), ('nom_desc', 'Nom Z-A'), ('prenom_asc', 'Prenom A-Z'), 
                ('prenom_desc', 'Prenom Z-A'),('age_asc', 'Plus agé'), ('age_desc', 'Plus jeune')]
    
    # Filtrage Actif / Ancien
    if ancien:
        liste = MembreBD.query.filter(MembreBD.activite == False)
        titre_page = "Anciens Membres"
    else:
        liste = MembreBD.query.filter(MembreBD.activite == True)
        titre_page = "Gestion des Profils"

    # Application des filtres du formulaire
    if filtre.sexe.data:
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
    
    # Application du tri
    if filtre.tri.data == 'date_asc': liste = liste.order_by(MembreBD.date_inscription.asc())
    elif filtre.tri.data == 'nom_desc': liste = liste.order_by(MembreBD.nom.desc())
    elif filtre.tri.data == 'nom_asc': liste = liste.order_by(MembreBD.nom.asc())
    elif filtre.tri.data == 'prenom_desc': liste = liste.order_by(MembreBD.prenom.desc())
    elif filtre.tri.data == 'prenom_asc': liste = liste.order_by(MembreBD.prenom.asc())
    elif filtre.tri.data == 'age_desc': liste = liste.order_by(MembreBD.ddn.desc())
    elif filtre.tri.data == 'age_asc': liste = liste.order_by(MembreBD.ddn.asc())
    else: liste = liste.order_by(MembreBD.date_inscription.desc())

    # Pagination
    pagination = liste.paginate(page=page, per_page=15, error_out=False)
    
    return render_template("gerer_profils.html",
        title=TITLE + " - " + titre_page,
        pagination=pagination,
        membres=pagination.items, 
        filtre=filtre,
        mode=mode)

# Désactive le compte d'un membre.
@admin_bp.route('/gerer_profils/desinscrire/<int:idM>', methods=["GET", "POST"])
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
    if current_user.id == idM and session.get('user_type') != 'admin':
        logout_user()
        flash("Votre compte a été désactivé avec succès.", "success")
        return redirect(url_for('general.index'))
    else:
        return redirect(url_for('admin.gerer_profils'))

# Réactive le compte d'un ancien membre - Réservée aux administrateurs.
@app.route ('/gerer_anciens_profils/reinscrire/<int:idM>', methods =("POST" ,))
@login_required
@admin_required
def reinscrireMembre(idM):
    membre = db.session.get(MembreBD, idM)
    membre.activite = True
    membre.statut = "Membre"
    db.session.commit()
    return redirect(url_for('admin.gerer_profils'))

# Page de modification d'un profil, accessible par le membre lui-même ou un admin.
@admin_bp.route("/profil_edit/<int:idM>", methods=["GET", "POST"])
@login_required
def profil_edit(idM):
    unMembre = db.session.get(MembreBD, idM)
    unForm = ModifForm(obj=unMembre)
    origine = request.args.get('origine', 'profil')
    if unForm.validate_on_submit():
        action = request.form.get('submit_action')
        if action == 'admin_save':
            unForm.populate_obj(unMembre)
            db.session.commit()
            return redirect(url_for('admin.gerer_profils'))
        elif action == 'membre_request':
            # 1. On récupère la modification existante ou on en crée une nouvelle
            uneModif = unMembre.modifications.first()
            if not uneModif:
                uneModif = ModifBD(id_membre=idM)
                db.session.add(uneModif)
            
            # 2. On met à jour les champs de 'uneModif' avec les données du formulaire
            uneModif.nom = unForm.nom.data
            uneModif.prenom = unForm.prenom.data
            uneModif.numLicense = unForm.numLicense.data
            uneModif.email = unForm.email.data
            uneModif.sexe = unForm.sexe.data
            uneModif.ddn = unForm.ddn.data
            uneModif.numTel = unForm.numTel.data
            uneModif.date = datetime.now()
            uneModif.justification = unForm.justification.data
            
            # 3. Notification des administrateurs
            admins = AdminBD.query.all()
            for admin in admins:
                if admin.demandeModifSite:
                    notif = NotifsBD(
                        typeN='modification',
                        sourceN=f"Demande de modification de {unMembre.prenom} {unMembre.nom}",
                        lue=False,
                        timestamp=datetime.now(),
                        idAdmin=admin.id,
                        link=url_for('admin.gerer_profils', _external=True)
                    )
                    db.session.add(notif)
            
            db.session.commit()
            return redirect(url_for('profil.profil_view', idM=idM, origine='profil'))   
    return render_template("profil_edit.html", updateForm=unForm, selectedMembre=unMembre, title=TITLE+"- Édition Profil")

# Affiche les demandes d'inscription et de modification de profil - Réservée aux administrateurs.
@admin_bp.route("/gerer_inscriptions/")
@login_required
@admin_required
def gerer_inscriptions():
    page = request.args.get('page', 1, type=int)
    type_page = request.args.get('type',
                                 'inscription')
    if type_page == 'modification':
        lesRequetes = ModifBD.query.order_by(ModifBD.date.desc())
    else:
        type_page = 'inscription'
        lesRequetes = InscriptionBD.query.order_by(
            InscriptionBD.date.desc())
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
        numTel=inscription.numTel,
        mdp_hash=inscription.mdp_hash,
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
    db.session.delete(inscription)
    db.session.commit()
    return redirect(url_for('admin.gerer_inscriptions'))

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
        membre_a_modifier.numTel = modifications.numTel
        db.session.delete(modifications)
        db.session.commit()
    return redirect(url_for('admin.gerer_inscriptions'))

# Refuse et supprime une demande d'inscription - Réservée aux administrateurs.
@admin_bp.route('/refuser_inscription/<int:idI>', methods=["POST"])
@login_required
@admin_required
def refuser_inscription(idI):
    #La justification, elle est pour l'instant inutile et devrat plus tard etre envoyer par mail
    justification = request.form.get('justification')
    inscription_a_supprimer = db.session.get(InscriptionBD, idI)
    db.session.delete(inscription_a_supprimer)
    db.session.commit()
    return redirect(url_for('admin.gerer_inscriptions'))

# Refuse et supprime une demande de modification - Réservée aux administrateurs.
@admin_bp.route('/refuser_modification/<int:idM>', methods=["POST"])
@login_required
@admin_required
def refuser_modification(idM):
    #La justification, elle est pour l'instant inutile et devrat plus tard etre envoyer par mail
    justification = request.form.get('justification')
    modification_a_supprimer = db.session.get(ModifBD, idM)
    db.session.delete(modification_a_supprimer)
    db.session.commit()
    return redirect(url_for('admin.gerer_inscriptions'))

@admin_bp.route("/admin/gestion_tarifs/", methods=["GET", "POST"])
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
            return redirect(url_for('admin.gestion_tarifs'))
        except Exception as e:
            db.session.rollback()
    les_tarifs = TarifBD.query.order_by(TarifBD.categorie, TarifBD.prix).all()
    return render_template("admin_gestion_tarifs.html", title="Gestion Tarifs", form=form, tarifs=les_tarifs)

@admin_bp.route("/admin/delete_tarif/<int:idT>", methods=["POST"])
@login_required
@admin_required
def delete_tarif(idT):
    tarif = TarifBD.query.get_or_404(idT)
    try:
        db.session.delete(tarif)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('admin.gestion_tarifs'))

@admin_bp.route("/admin/edit_tarif/<int:idT>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_tarif(idT):
    tarif = TarifBD.query.get_or_404(idT)
    form = TarifForm(obj=tarif)
    if form.validate_on_submit():
        form.populate_obj(tarif)
        db.session.commit()
        return redirect(url_for('admin.gestion_tarifs'))
    return render_template("admin_edit_tarif.html", title="Modifier Tarif", form=form)


@admin_bp.route("/admin/gestion_horaires/", methods=["GET", "POST"])
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
            return redirect(url_for('admin.gestion_horaires'))
        except Exception as e:
            db.session.rollback()
    les_horaires = HoraireBD.query.all()
    ordre_jours = {'Lundi': 1, 'Mardi': 2, 'Mercredi': 3, 'Jeudi': 4, 'Vendredi': 5, 'Samedi': 6, 'Dimanche': 7}
    les_horaires.sort(key=lambda x: ordre_jours.get(x.jour, 8))
    return render_template("admin_gestion_horaires.html", title="Gestion Horaires", form=form, horaires=les_horaires)

@admin_bp.route("/admin/delete_horaire/<int:idH>", methods=["POST"])
@login_required
@admin_required
def delete_horaire(idH):
    horaire = HoraireBD.query.get_or_404(idH)
    try:
        db.session.delete(horaire)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('admin.gestion_horaires'))

@admin_bp.route("/admin/edit_horaire/<int:idH>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_horaire(idH):
    horaire = HoraireBD.query.get_or_404(idH)
    form = HoraireForm(obj=horaire)
    if form.validate_on_submit():
        form.populate_obj(horaire)
        db.session.commit()
        return redirect(url_for('admin.gestion_horaires'))
    return render_template("admin_edit_horaire.html", title="Modifier Horaire", form=form)
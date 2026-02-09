#================================================================#
#====================   Pages Competitions   ====================#
#================================================================#

@app.route("/competitions/")
@app.route("/competitions/<string:etat>")
def competitions(etat="prochaines"): # Valeur par défaut : pluriel 'prochaines'
    if request.args.get('etat'):
        etat = request.args.get('etat')
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
    return render_template("evenements/competitions.html", title=TITLE+"- Competitions", pagination=pagination, filtre=filtre, etat=etat)


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

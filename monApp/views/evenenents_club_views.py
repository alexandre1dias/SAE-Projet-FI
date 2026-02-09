#====================   Pages Evenement du club   ====================#
# Affiche la liste des événements du club.
@app.route("/evenement_club/")
@app.route("/evenement_club/<string:etat>")
@login_required
def evenement_club(etat="prochaine"):
    passee = (etat == "passees")
    filtre = FiltreForm(request.args if request.args else None)
    page = request.args.get('page', 1, type=int)
    lesEvements = EventClubBD.query
    filtre.tri.choices = [
        ('date_desc', 'Plus récent'),
        ('date_asc', 'Plus ancien')
    ]

    if filtre.tri.data == "date_asc":
        lesEvements = lesEvements.order_by(EventClubBD.dateDebutEV.asc())
    else:
        lesEvements = lesEvements.order_by(EventClubBD.dateDebutEV.desc())

    lesEvements = lesEvements.filter(EventClubBD.passeeEV == passee)
    pagination = lesEvements.paginate(page=page, per_page=6, error_out=False)

    return render_template("evenement_club.html",
                           title=TITLE + "- Evenements du Club",
                           pagination=pagination,
                           filtre=filtre,
                           passee=passee)

# Affiche les détails d'un événement de club spécifique.
@app.route("/evenement_club/<int:idEventClub>/club_view/")
@login_required
def club_view(idEventClub):
    unEventClub = EventClubBD.query.get(idEventClub)
    origine = request.args.get('origine', 'default')

    deja_inscrit = False
    if current_user.is_authenticated and session.get('user_type') == 'membre':
        participation = ParticiperBD.query.filter_by(id_membre=current_user.id, id_event=unEventClub.id_event).first()
        deja_inscrit = participation is not None
    return render_template("club_view.html",title=TITLE+"- un évenement du club",selectedEventClub=unEventClub, deja_inscrit=deja_inscrit, origine=origine)

# Page de modification d'un événement de club - Réservée aux administrateurs.
@app.route("/evenement_club/<int:idEventClub>/club_update/", methods=['GET', 'POST'])
@login_required
@admin_required
def club_update(idEventClub):
    unEventClub = EventClubBD.query.get_or_404(idEventClub)

    if request.method == 'POST':
        try:
            unEventClub.NomEV = request.form['nom']
            unEventClub.adresseEV = request.form['lieu']
            unEventClub.descriptionEV = request.form['description']
            unEventClub.dateDebutEV = datetime.strptime(request.form['date_debut'], '%Y-%m-%d').date()
            unEventClub.heureDebutEV = request.form['heure_debut']
            unEventClub.dateFinEV = datetime.strptime(request.form['date_fin'], '%Y-%m-%d').date()
            unEventClub.heureFinEV = request.form['heure_fin']
            db.session.commit()
            return redirect(url_for('club_view', idEventClub=unEventClub.idEventClub))
        except Exception as e:
            db.session.rollback()
    participations = ParticiperBD.query.filter_by(id_event=unEventClub.id_event).all()
    participants = [p.membre for p in participations]
    lesMembres = MembreBD.query.all()
    return render_template("club_update.html",title=TITLE+"- Modification d'un évenement du club", eventClub=unEventClub, participants=participants)

# Page pour sélectionner les membres à inscrire à un événement de club - Réservée aux administrateurs.
@app.route("/evenement_club/<int:idEventClub>/inscrire_membres", methods=['GET'])
@login_required
@admin_required
def inscrire_membres_event_club(idEventClub):
    event_club = EventClubBD.query.get_or_404(idEventClub)
    membres_a_inscrire_ids = request.args.getlist('membres_a_inscrire_ids', type=int)
    if not membres_a_inscrire_ids:
        membres_a_inscrire_ids = []
    if 'add' in request.args:
        membres_a_inscrire_ids.append(int(request.args.get('add')))
    if 'remove' in request.args:
        membres_a_inscrire_ids.remove(int(request.args.get('remove')))
    participations = ParticiperBD.query.filter_by(id_event=event_club.id_event).all()
    participants_ids = {p.id_membre for p in participations}
    non_participants = MembreBD.query.filter(MembreBD.id.notin_(participants_ids), MembreBD.activite == True).all()
    return render_template("club_inscrire_membre.html", title=TITLE+"- Inscrire des membres", eventClub=event_club, non_participants=non_participants, membres_a_inscrire_ids=membres_a_inscrire_ids)

# Traite l'inscription de plusieurs membres à un événement de club - Réservée aux administrateurs.
@app.route("/evenement_club/<int:idEventClub>/inscription_membres", methods=['POST'])
@login_required
@admin_required
def inscription_membres_event_club(idEventClub):
    event_club = EventClubBD.query.get_or_404(idEventClub)
    membres_a_inscrire_ids = request.form.getlist('membres_a_inscrire')
    for membre_id in membres_a_inscrire_ids:
        deja_inscrit = ParticiperBD.query.filter_by(id_membre=membre_id, id_event=event_club.id_event).first()
        if not deja_inscrit:
            nouvelle_participation = ParticiperBD(id_membre=membre_id, id_event=event_club.id_event)
            db.session.add(nouvelle_participation)
    db.session.commit()
    return redirect(url_for('club_update', idEventClub=idEventClub))

# Supprime la participation d'un membre à un événement de club - Réservée aux administrateurs.
@app.route("/evenement_club/<int:idEventClub>/delete/<int:idM>", methods=['POST'])
@login_required
@admin_required
def delete_membre_eventClub(idEventClub, idM):
    eventClub = EventClubBD.query.get_or_404(idEventClub)
    participation = ParticiperBD.query.filter_by(id_event=eventClub.id_event, id_membre=idM).first_or_404()
    try:
        db.session.delete(participation)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('club_update', idEventClub=idEventClub))

# Supprime un événement de club - Réservée aux administrateurs.
@app.route("/evenement_club/<int:idEventClub>/club_delete/", methods=['POST'])
@login_required
@admin_required
def club_delete(idEventClub):
    evenement_a_supprimer = EventClubBD.query.get_or_404(idEventClub)
    db.session.delete(evenement_a_supprimer)
    db.session.commit()
    return redirect(url_for('evenement_club'))

# Permet à un membre de s'inscrire à un événement de club.
@app.route("/inscrire/club/<int:idEventClub>", methods=['GET'])
@login_required
@membre_required
def inscrire_club(idEventClub):
    evenement_club_obj = EventClubBD.query.get_or_404(idEventClub)
    id_evenement_a_inscrire = evenement_club_obj.id_event

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
    return redirect(url_for('club_view', idEventClub=idEventClub))

# Permet à un membre de se désinscrire d'un événement de club.
@app.route("/desinscrire/club/<int:idEventClub>", methods=['GET'])
@login_required
@membre_required
def desinscrire_club(idEventClub):
    evenement_club_obj = EventClubBD.query.get_or_404(idEventClub)
    participation = ParticiperBD.query.filter_by(id_membre=current_user.id, id_event=evenement_club_obj.id_event).first()
    if participation:
        db.session.delete(participation)
        db.session.commit()
    return redirect(url_for('club_view', idEventClub=idEventClub))

@app.route('/club/add_image/<int:idEventClub>', methods=['POST'])
@login_required
@admin_required
def add_image_club(idEventClub):
    """Ajoute une image à un événement du club."""
    event_club = EventClubBD.query.get_or_404(idEventClub)

    if 'image' not in request.files:
        flash('Aucun fichier sélectionné.', 'danger')
        return redirect(url_for('club_update', idEventClub=idEventClub))

    file = request.files['image']
    alt_text = request.form.get('alt', 'Image pour l\'événement ' + event_club.NomEV)
    is_prive = 'prive' in request.form

    if file.filename == '':
        flash('Aucun fichier image sélectionné.', 'warning')
        return redirect(url_for('club_update', idEventClub=idEventClub))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Crée un dossier spécifique pour l'événement s'il n'existe pas
        upload_folder = os.path.join(app.static_folder, 'images', 'events_club', str(event_club.idEventClub))
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # Chemin à stocker en BDD, relatif au dossier 'static'
        db_url = os.path.join('images', 'events_club', str(event_club.idEventClub), filename).replace('\\', '/')

        # Crée l'objet Image et l'associe à l'événement
        try:
            new_image = ImageAppBD(urlI=db_url, alt=alt_text, prive=is_prive)
            event_club.images_re.append(new_image)
            db.session.add(new_image)
            db.session.commit()
            flash('Image ajoutée avec succès !', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de l\'ajout de l\'image : {e}', 'danger')
    else:
        flash('Type de fichier non autorisé.', 'danger')

    return redirect(url_for('club_update', idEventClub=idEventClub))


@app.route('/club/delete_image/<int:idImage>', methods=['POST'])
@login_required
@admin_required
def delete_image_club(idImage):
    """Supprime une image d'un événement du club."""
    idEventClub = request.form.get('idEventClub')
    if not idEventClub:
        flash("ID de l'événement manquant.", "danger")
        return redirect(url_for('index'))

    image_to_delete = ImageAppBD.query.get_or_404(idImage)
    event_club = EventClubBD.query.get_or_404(idEventClub)

    if image_to_delete in event_club.images_re:
        # Supprime l'association
        event_club.images_re.remove(image_to_delete)

        # Supprime le fichier physique
        try:
            image_path = os.path.join(app.static_folder, image_to_delete.urlI)
            if os.path.exists(image_path):
                os.remove(image_path)

            # Optionnel : supprime le dossier s'il est vide
            image_dir = os.path.dirname(image_path)
            if not os.listdir(image_dir):
                os.rmdir(image_dir)

        except Exception as e:
            flash(f"Erreur lors de la suppression du fichier : {e}", "danger")

        # Supprime l'image de la base de données
        db.session.delete(image_to_delete)
        db.session.commit()

        flash("L'image a été retirée de l'événement.", "success")
    else:
        flash("Cette image n'était pas associée à cet événement.", "warning")

    return redirect(url_for('club_update', idEventClub=idEventClub))
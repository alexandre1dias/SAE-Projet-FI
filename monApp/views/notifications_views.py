#==================================================================#
#====================   Routes Notifications   ====================#
#==================================================================#
# Route pour marquer une notification comme lue et rediriger vers son lien
@app.route("/read_notification/<int:id_notif>")
@login_required
def read_notification(id_notif):
    notif = NotifsBD.query.get_or_404(id_notif)
    if session.get('user_type') == 'membre':
        if notif.idMembre != current_user.id:
            abort(403)
    elif session.get('user_type') == 'admin':
        if notif.idAdmin != current_user.id:
            abort(403)
    else:
        abort(403)
    notif.lue = True
    db.session.commit()
    target_url = request.referrer or url_for('index')
    if notif.link and notif.link != '#':
        if notif.link.startswith('#'):
            base_target = target_url.split('#')[0]
            return redirect(base_target + notif.link) 
        return redirect(notif.link)
    return redirect(target_url)

# Route pour supprimer une notification
@app.route("/delete_notification/<int:id_notif>", methods=['POST'])
@login_required
def delete_notification(id_notif):
    notif = NotifsBD.query.get_or_404(id_notif)
    # Vérification que la notif appartient bien à l'utilisateur connecté
    if session.get('user_type') == 'membre':
        if notif.idMembre != current_user.id:
            abort(403)
    elif session.get('user_type') == 'admin':
        if notif.idAdmin != current_user.id:
            abort(403)
    else:
        abort(403)

    # Supprimer les dépendances dans les tables de liaison avant de supprimer la notification
    # Cela évite l'erreur IntegrityError car la cascade n'est pas configurée en SQL
    db.session.execute(recevoir_a.delete().where(recevoir_a.c.idNotifs == id_notif))
    db.session.execute(recevoir_m.delete().where(recevoir_m.c.idNotifs == id_notif))

    db.session.delete(notif)
    db.session.commit()
    return redirect(request.referrer or url_for('index'))
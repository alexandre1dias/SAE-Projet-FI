from flask import Blueprint, render_template, request, url_for, redirect, session, abort
from flask_login import login_required, current_user
from monApp.app import db
from monApp.models import NotifsBD, recevoir_a, recevoir_m

notifications_bp = Blueprint('notifications', __name__)

#==================================================================#
#====================   Routes Notifications   ====================#
#==================================================================#

@notifications_bp.route("/read_notification/<int:id_notif>")
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
    target_url = request.referrer or url_for('general.index')
    if notif.link and notif.link != '#':
        if notif.link.startswith('#'):
            base_target = target_url.split('#')[0]
            return redirect(base_target + notif.link) 
        return redirect(notif.link)
    return redirect(target_url)

@notifications_bp.route("/delete_notification/<int:id_notif>", methods=['POST'])
@login_required
def delete_notification(id_notif):
    notif = NotifsBD.query.get_or_404(id_notif)
    if session.get('user_type') == 'membre':
        if notif.idMembre != current_user.id:
            abort(403)
    elif session.get('user_type') == 'admin':
        if notif.idAdmin != current_user.id:
            abort(403)
    else:
        abort(403)

    # Suppression manuelle dans les tables d'association
    db.session.execute(recevoir_a.delete().where(recevoir_a.c.idNotifs == id_notif))
    db.session.execute(recevoir_m.delete().where(recevoir_m.c.idNotifs == id_notif))

    db.session.delete(notif)
    db.session.commit()
    return redirect(request.referrer or url_for('general.index'))
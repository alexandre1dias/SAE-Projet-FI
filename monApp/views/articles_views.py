from flask import Blueprint, render_template, request, url_for, redirect, session, flash, jsonify, abort
from flask_login import login_required, current_user
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
articles_bp = Blueprint('articles', __name__)

#==============================================================#
#====================   Pages Actualités   ====================#
#==============================================================#
# Affiche la page listant toutes les informations.
@articles_bp.route("/informations/")
def informations():
    filtre = FiltreForm(request.args)

    # Récupération des années existantes en base pour le filtre
    dates_bd = db.session.query(InformationBD.dateIN).distinct().all()
    annees_set = set()
    for (d,) in dates_bd:
        if d:
            annee_debut = d.year if d.month >= 8 else d.year - 1
            annees_set.add((str(annee_debut), f"{annee_debut}-{annee_debut + 1}"))
    
    if annees_set:
        choix_tries = sorted(list(annees_set), key=lambda x: x[0], reverse=True)
        filtre.annee_scolaire.choices = choix_tries
        if filtre.annee_scolaire.data not in [c[0] for c in choix_tries]:
            filtre.annee_scolaire.data = choix_tries[0][0]

    annee_selectionnee = filtre.annee_scolaire.data
    les_infos = InformationBD.query
    filtre.tri.choices = [('date_desc', 'Plus récent'),
                          ('date_asc', 'Plus ancien')]
    
    if filtre.recherche.data:
        les_infos = les_infos.filter(InformationBD.titreIN.ilike(f"%{filtre.recherche.data}%"))

    if annee_selectionnee:
        try:
            an_debut = int(annee_selectionnee)
            debut_saison = date(an_debut, 8, 1)
            fin_saison = date(an_debut + 1, 7, 31)
            les_infos = les_infos.filter(InformationBD.dateIN >= debut_saison,
                                 InformationBD.dateIN <= fin_saison)
        except (ValueError, TypeError):
            pass
    if filtre.tri.data == 'date_asc':
        les_infos = les_infos.order_by(InformationBD.dateIN.asc(), InformationBD.heureIN.asc())
    else:
        les_infos = les_infos.order_by(InformationBD.dateIN.desc(), InformationBD.heureIN.desc())

    page = request.args.get('page', 1, type=int)
    pagination = les_infos.paginate(page=page, per_page=6, error_out=False)

    return render_template("informations.html",
                           title=TITLE + " - Informations",
                           pagination=pagination,
                           filtre=filtre)

@articles_bp.route("/admin/add_information/", methods=["GET", "POST"])
@login_required
@admin_required
def add_information():
    form = InformationForm()
    if form.validate_on_submit():
        now = datetime.now()
        nouvelle_info = InformationBD(
            titreIN=form.titre.data,
            contenuIN=form.contenu.data,
            dateIN=now.date(),
            heureIN=now.strftime('%H:%M')
        )
        try:
            db.session.add(nouvelle_info)
            db.session.commit()
            return redirect(url_for('articles.informations'))
        except Exception as e:
            db.session.rollback()
    return render_template("admin_form_information.html", title="Ajouter une information", form=form)

@articles_bp.route("/admin/edit_information/<int:idI>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_information(idI):
    info = InformationBD.query.get_or_404(idI)
    form = InformationForm()
    if request.method == 'GET':
        form.titre.data = info.titreIN
        form.contenu.data = info.contenuIN
    if form.validate_on_submit():
        info.titreIN = form.titre.data
        info.contenuIN = form.contenu.data
        try:
            db.session.commit()
            return redirect(url_for('articles.informations'))
        except Exception as e:
            db.session.rollback()
    return render_template("admin_form_information.html", title="Modifier une information", form=form)

@articles_bp.route("/admin/delete_information/<int:idI>", methods=["POST"])
@login_required
@admin_required
def delete_information(idI):
    info = InformationBD.query.get_or_404(idI)
    try:
        db.session.delete(info)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('articles.informations'))


# Affiche la page listant tous les articles de presse.
@articles_bp.route("/presse/")
def presse():
    page = request.args.get('page', 1, type=int)
    filtre = FiltreForm(request.args)

    # Récupération des années existantes en base pour le filtre
    dates_bd = db.session.query(PresseBD.dateP).distinct().all()
    annees_set = set()
    for (d,) in dates_bd:
        if d:
            annee_debut = d.year if d.month >= 8 else d.year - 1
            annees_set.add((str(annee_debut), f"{annee_debut}-{annee_debut + 1}"))
    
    if annees_set:
        choix_tries = sorted(list(annees_set), key=lambda x: x[0], reverse=True)
        filtre.annee_scolaire.choices = choix_tries
        if filtre.annee_scolaire.data not in [c[0] for c in choix_tries]:
            filtre.annee_scolaire.data = choix_tries[0][0]

    annee_selectionnee = filtre.annee_scolaire.data
    filtre.tri.choices = [('date_desc', 'Plus récent'),
                          ('date_asc', 'Plus ancien')]
    les_presses = PresseBD.query
    if filtre.recherche.data:
        les_presses = les_presses.filter(PresseBD.titreP.ilike(f"%{filtre.recherche.data}%"))
    if annee_selectionnee:
        try:
            an_debut = int(annee_selectionnee)
            debut_saison = date(an_debut, 8, 1)
            fin_saison = date(an_debut + 1, 7, 31)
            les_presses = les_presses.filter(PresseBD.dateP >= debut_saison,
                                 PresseBD.dateP <= fin_saison)
        except (ValueError, TypeError):
            pass
    if filtre.tri.data == 'date_asc':
        les_presses = les_presses.order_by(PresseBD.dateP.asc(), PresseBD.idPresse.asc())
    else:
        les_presses = les_presses.order_by(PresseBD.dateP.desc(), PresseBD.idPresse.desc())
    pagination = les_presses.paginate(page=page, per_page=6, error_out=False)
    return render_template("presse.html",
                           title=TITLE + "- Presse",
                           pagination=pagination,
                           articles=pagination.items,
                           filtre=filtre)

@articles_bp.route("/admin/add_presse/", methods=["GET", "POST"])
@login_required
@admin_required
def add_presse():
    form = PresseForm()
    if form.validate_on_submit():
        now = datetime.now()
        nouveau_presse = PresseBD(
            titreP=form.titre.data,
            contenuP=form.contenu.data,
            lienP=form.lien.data,
            dateP=now.date(),
            heureP=now.strftime('%H:%M')
        )
        db.session.add(nouveau_presse)
        db.session.commit()
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            dossier_presse = os.path.join(app.root_path, 'static', 'images', 'presse', str(nouveau_presse.idPresse))
            os.makedirs(dossier_presse, exist_ok=True)
            file.save(os.path.join(dossier_presse, filename))
            nouveau_presse.imageP = filename
            db.session.commit()
        return redirect(url_for('articles.presse'))
    return render_template("admin_form_presse.html", title="Ajouter un article de presse", form=form)

@articles_bp.route("/admin/edit_presse/<int:idP>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_presse(idP):
    article_presse = PresseBD.query.get_or_404(idP)
    form = PresseForm()
    if request.method == 'GET':
        form.titre.data = article_presse.titreP
        form.contenu.data = article_presse.contenuP
        form.lien.data = article_presse.lienP
    if form.validate_on_submit():
        article_presse.titreP = form.titre.data
        article_presse.contenuP = form.contenu.data
        article_presse.lienP = form.lien.data
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            dossier_presse = os.path.join(app.root_path, 'static', 'images', 'presse', str(article_presse.idPresse))
            os.makedirs(dossier_presse, exist_ok=True)
            if article_presse.imageP:
                ancien_chemin = os.path.join(dossier_presse, article_presse.imageP)
                if os.path.exists(ancien_chemin):
                    os.remove(ancien_chemin)
            file.save(os.path.join(dossier_presse, filename))
            article_presse.imageP = filename
        db.session.commit()
        return redirect(url_for('articles.presse'))
    return render_template("admin_form_presse.html", title="Modifier l'article de presse", form=form)

@articles_bp.route("/admin/delete_presse/<int:idP>", methods=["POST"])
@login_required
@admin_required
def delete_presse(idP):
    article_presse = PresseBD.query.get_or_404(idP)
    dossier_presse = os.path.join(app.root_path, 'static', 'images', 'presse', str(article_presse.idPresse))
    if os.path.exists(dossier_presse):
        shutil.rmtree(dossier_presse)
    try:
        db.session.delete(article_presse)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('articles.presse'))

@articles_bp.route("/articles/")
def articles():
    page = request.args.get('page', 1, type=int)
    filtre = FiltreForm(request.args)

    # Récupération des années existantes en base pour le filtre
    dates_bd = db.session.query(ArticleBD.date).distinct().all()
    annees_set = set()
    for (d,) in dates_bd:
        if d:
            annee_debut = d.year if d.month >= 8 else d.year - 1
            annees_set.add((str(annee_debut), f"{annee_debut}-{annee_debut + 1}"))
    
    if annees_set:
        choix_tries = sorted(list(annees_set), key=lambda x: x[0], reverse=True)
        filtre.annee_scolaire.choices = choix_tries
        if filtre.annee_scolaire.data not in [c[0] for c in choix_tries]:
            filtre.annee_scolaire.data = choix_tries[0][0]

    annee_selectionnee = filtre.annee_scolaire.data
    filtre.tri.choices = [('date_desc', 'Plus récent'),
                          ('date_asc', 'Plus ancien')]
    les_articles = ArticleBD.query
    if filtre.recherche.data:
        les_articles = les_articles.filter(
            ArticleBD.titre.ilike(f"%{filtre.recherche.data}%"))
    if annee_selectionnee:
        try:
            an_debut = int(annee_selectionnee)
            debut_saison = date(an_debut, 8, 1)
            fin_saison = date(an_debut + 1, 7, 31)
            les_articles = les_articles.filter(ArticleBD.date >= debut_saison, ArticleBD.date
                                 <= fin_saison)
        except (ValueError, TypeError):
            pass
    if filtre.tri.data == 'date_asc':
        les_articles = les_articles.order_by(ArticleBD.date.asc(), ArticleBD.id.asc())
    else:
        les_articles = les_articles.order_by(ArticleBD.date.desc(), ArticleBD.id.desc())
    pagination = les_articles.paginate(page=page, per_page=6, error_out=False)
    return render_template("articles.html",
                           title=TITLE + " - Articles du Club",
                           pagination=pagination,
                           articles=pagination,
                           filtre=filtre)

@articles_bp.route("/article/<int:idA>")
def article_detail(idA):
    article = ArticleBD.query.get_or_404(idA)
    return render_template("article_detail.html", title=article.titre, article=article)

@articles_bp.route("/admin/add_article/", methods=["GET", "POST"])
@login_required
@admin_required
def add_article():
    form = ArticleForm()
    if form.validate_on_submit():
        # Créer l'article en base pour avoir l'ID
        nouveau_article = ArticleBD(
            titre=form.titre.data,
            contenu=form.contenu.data,
            date=datetime.now().date()
        )
        db.session.add(nouveau_article)
        db.session.commit()
        # Gestion des images
        if form.images.data:
            # Création du chemin : static/images/articles/<ID_ARTICLE>
            dossier_article = os.path.join(app.root_path, 'static/images/articles', str(nouveau_article.id))
            # On crée le dossier s'il n'existe pas
            os.makedirs(dossier_article, exist_ok=True)
            for file in form.images.data:
                if file.filename:
                    filename = secure_filename(file.filename)
                    # Sauvegarde dans le sous-dossier
                    file.save(os.path.join(dossier_article, filename))
                    nouvelle_image = ImageArticleBD(nom=filename, id_article=nouveau_article.id)
                    db.session.add(nouvelle_image)
            db.session.commit()
        return redirect(url_for('articles.articles'))
    return render_template("admin_form_article.html", title="Rédiger un article", form=form)

@articles_bp.route("/admin/edit_article/<int:idA>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_article(idA):
    article = ArticleBD.query.get_or_404(idA)
    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        article.titre = form.titre.data
        article.contenu = form.contenu.data
        if form.images.data:
            # Cible le dossier de l'article existant
            dossier_article = os.path.join(app.root_path, 'static/images/articles', str(article.id))
            os.makedirs(dossier_article, exist_ok=True)

            for file in form.images.data:
                if file.filename:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(dossier_article, filename))
                    nouvelle_image = ImageArticleBD(nom=filename, id_article=article.id)
                    db.session.add(nouvelle_image)
        db.session.commit()
        return redirect(url_for('articles.articles'))
    return render_template("admin_form_article.html", title="Modifier un article", form=form, article=article)

@articles_bp.route("/admin/delete_article/<int:idA>", methods=["POST"])
@login_required
@admin_required
def delete_article(idA):
    article = ArticleBD.query.get_or_404(idA)
    # Suppression du dossier complet de l'article (images incluses)
    dossier_article = os.path.join(app.root_path, 'static/images/articles', str(article.id))
    if os.path.exists(dossier_article):
        # Supprime le dossier et tout ce qu'il contient
        shutil.rmtree(dossier_article)
    try:
        db.session.delete(article)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('articles.articles'))

@articles_bp.route("/admin/delete_image_article/<int:idImg>", methods=["POST"])
@login_required
@admin_required
def delete_image_article(idImg):
    image = ImageArticleBD.query.get_or_404(idImg)
    article_id = image.id_article
    # On reconstruit le chemin avec l'ID de l'article
    chemin_image = os.path.join(app.root_path, 'static/images/articles', str(article_id), image.nom)
    try:
        if os.path.exists(chemin_image):
            os.remove(chemin_image)
    except:
        pass
    db.session.delete(image)
    db.session.commit()
    return redirect(url_for('articles.edit_article', idA=article_id))

@articles_bp.route("/ffescrime/", methods=["GET", "POST"])
def ffescrime():
    return render_template("ffescrime.html", title=TITLE+"- FFEscrime")

#============================================================#
#====================   Pages A propos   ====================#
#============================================================#
# Affiche la page de l'historique du club.
@articles_bp.route("/historique/")
def historique():
    return render_template("historique.html",title=TITLE+"- Historique")

# Affiche la page de présentation du comité directeur.
@articles_bp.route("/comite_cercle/")
def comite_cercle():
    comite = {
        "president": MembreBD.query.filter_by(statut='Président').first(),
        "vicePresident": MembreBD.query.filter_by(statut='Vice-Président').first(),
        "tresorier": MembreBD.query.filter_by(statut='Trésorier Général').first(),
        "secretaire": MembreBD.query.filter_by(statut='Secrétaire Générale').first()
    }
    membres = MembreBD.query.filter_by(statut='Membre du Comité').all()
    return render_template("comite_cercle.html", title=TITLE+"- Comité directeur du Cercle", comite=comite, membres=membres)
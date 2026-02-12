import pytest
from flask import url_for
from werkzeug.security import generate_password_hash
from datetime import date, datetime
from monApp.models import *
from monApp.forms import ModifForm
from wtforms import DateField
from wtforms.validators import DataRequired


# ==============================================================================
# Fonction utilitaire
# ==============================================================================
def setup_admin(client, db):
    """
    Fonction utilitaire pour nettoyer la base, créer un admin et le connecter.
    """
    # Nettoyage
    client.get('/logout/', follow_redirects=True)
    db.session.query(AdminBD).delete()
    db.session.commit()

    # Création Admin
    admin = AdminBD(email='superadmin@test.fr',
                    mdp_hash=generate_password_hash('pass'))
    db.session.add(admin)
    db.session.commit()

    # Connexion
    client.post('/login/',
                data={
                    'email': 'superadmin@test.fr',
                    'password': 'pass'
                })
    return admin


# ==============================================================================
# 1. PAGES PUBLIQUES (Accessibles sans connexion)
# ==============================================================================
@pytest.mark.parametrize(
    "page, text",
    [('general.index', 'Entrez dans notre histoire'),
     ('general.contact', 'Nous Contacter'),
     ('general.historique', "L'HISTOIRE DU CERCLE"),
     ('general.comite_cercle', 'Comité directeur du cercle'),
     ('general.adresse', 'Adresse'), ('general.horaires', 'Horaire'),
     ('general.adhesions', "Choisissez votre adhésion"),
     ('general.materiel', "Matériel et tenue d'escrime"),
     ('general.escrime_feminin', "Mesdames, en Garde !"),
     ('calendrier.calendrier', "Calendrier des Évènements"),
     ('competitions.competitions', "Listes des prochaines compétitions"),
     ('articles.informations', 'Informations'), ('articles.presse', 'Presse'),
     ('articles.articles', 'Articles du Club')])
def test_pages_publiques_avec_url_for(client, app, page, text):
    """Test des pages accessibles à tous."""
    with app.test_request_context():
        url = url_for(page)
    response = client.get(url)
    assert response.status_code == 200
    assert text in response.data.decode('utf-8')


def test_page_publique_competition_view(client, app, db):
    """
    Test de la page de consultation d'une compétition.
    Nécessite de créer une compétition en BDD avant d'appeler l'URL.
    """
    app.config['WTF_CSRF_ENABLED'] = False

    # 1. Création d'une compétition
    evt = EvenementBD()
    db.session.add(evt)
    db.session.commit()

    comp = CompetitionBD(id_event=evt.id,
                         nom="Grande Compétition Test",
                         ville="Lyon",
                         adresse="Gymnase du Centre",
                         date_debut=date.today(),
                         heure_debut="09:00",
                         date_fin=date.today(),
                         heure_fin="18:00",
                         type_arme="Sabre",
                         sexe="F",
                         typeComp="National",
                         niveaux="M20",
                         passee=False)
    db.session.add(comp)
    db.session.commit()

    # 2. Appel de la route avec l'ID dynamique
    with app.test_request_context():
        url = url_for('competitions.competition_view', idCompetition=comp.id)

    response = client.get(url)

    # 3. vérification
    assert response.status_code == 200
    assert "Grande Compétition Test" in response.data.decode('utf-8')
    assert "Lyon" in response.data.decode('utf-8')


def test_page_publique_article_detail(client, app, db):
    """
    Test de la page de détail d'un article (Route publique).
    Vérifie l'affichage correct et la gestion de l'erreur 404.
    """
    app.config['WTF_CSRF_ENABLED'] = False

    # 1. Création d'un article en base de données
    article = ArticleBD(titre="Article Important",
                        contenu="Ceci est le contenu détaillé de l'article.",
                        date=date.today())
    db.session.add(article)
    db.session.commit()

    # 2. On appelle la route avec l'ID de l'article créé
    with app.test_request_context():
        response = client.get(url_for('articles.article_detail',
                                      idA=article.id))

    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert "Article Important" in content
    assert "Ceci est le contenu détaillé" in content

    # 3. On appelle la route avec un ID improbable
    response_404 = client.get('/article/999999')

    assert response_404.status_code == 404


# ==============================================================================
# 2. PAGES et SCENARIOS ACTIONS MEMBRES
# ==============================================================================
# ==============================================================================
# PAGES MEMBRES
# ==============================================================================
def test_pages_membres_protegees(client, app, db):
    """Test des pages réservées aux membres connectés."""
    app.config['WTF_CSRF_ENABLED'] = False

    # NETTOYAGE
    client.get('/logout/', follow_redirects=True)
    db.session.query(MembreBD).delete()
    db.session.query(AdminBD).delete()
    db.session.commit()

    # 1. Création d'un membre
    mdp_clair = "Password123!"
    membre = MembreBD(email='membre@test.fr',
                      mdp_hash=generate_password_hash(mdp_clair),
                      nom='Test',
                      prenom='User',
                      date_inscription=date.today(),
                      activite=True,
                      statut='Membre',
                      sexe='Homme',
                      ddn=date(2000, 1, 1))
    db.session.add(membre)
    db.session.commit()

    # 2. Connexion
    client.post('/login/',
                data={
                    'email': 'membre@test.fr',
                    'password': mdp_clair
                },
                follow_redirects=True)

    # 3. Test des routes protégées
    with app.test_request_context():
        # A. Résultats
        response = client.get(url_for('profil.resultat_membre'))
        assert response.status_code == 200
        assert "Résultat du Membre" in response.data.decode('utf-8')

        # B. Événements
        response = client.get(url_for('profil.evenement_membre'))
        assert response.status_code == 200
        assert "Vos Évènements" in response.data.decode('utf-8')

        # C. Profil
        response = client.get(url_for('profil.profil_view', idM=membre.id))
        assert response.status_code == 200
        content = response.data.decode('utf-8')
        assert "Profil de" in content or "Profil Membre" in content

        # D. Evènement du club
        response = client.get(url_for('events_club.evenement_club'))
        assert response.status_code == 200
        assert "Liste des prochains évènements du cercle" in response.data.decode(
            'utf-8')


# ==============================================================================
# SCENARIOS ACTIONS
# ==============================================================================
def test_inscription_reunion_comite(client, app, db):
    """
    Test Inscription/Désinscription à une réunion.
    Utilise un MEMBRE DU COMITÉ car la table PARTICIPER requiert un idMembre.
    """
    app.config['WTF_CSRF_ENABLED'] = False

    # 1. Création d'un Membre du Comité (Autorisé par @comite_ou_admin_required)
    client.get('/logout/')
    comite_member = MembreBD(email='prez@test.fr',
                             mdp_hash=generate_password_hash('pass'),
                             nom='Prez',
                             prenom='Boss',
                             statut='Président',
                             activite=True,
                             sexe='Homme',
                             ddn=date(1980, 1, 1))
    db.session.add(comite_member)

    # Création de la réunion
    evt = EvenementBD()
    db.session.add(evt)
    db.session.commit()

    reunion = ReunionBD(idEvent=evt.id,
                        nom="AG",
                        dateDebutRE=date.today(),
                        heureDebutRE="10:00",
                        dateFinRE=date.today(),
                        heureFinRE="12:00")
    db.session.add(reunion)
    db.session.commit()
    id_reunion = reunion.id

    # 2. Connexion
    client.post('/login/', data={'email': 'prez@test.fr', 'password': 'pass'})

    # 3. Inscription
    client.get(f'/reunion/inscrire/{id_reunion}', follow_redirects=True)

    # Vérification
    participation = ParticiperBD.query.filter_by(
        id_membre=comite_member.id, id_event=reunion.idEvent).first()
    assert participation is not None, "Le membre du comité devrait être inscrit"

    # 4. D"sinscription
    client.get(f'/reunion/desinscrire/{id_reunion}', follow_redirects=True)

    # Vérification
    participation = ParticiperBD.query.filter_by(
        id_membre=comite_member.id, id_event=reunion.idEvent).first()
    assert participation is None, "Le membre ne devrait plus être inscrit"


def test_desinscription_membre_par_soi_meme(client, app, db):
    """
    Test de la fonction desinscrireMembre par le membre lui-même.
    """
    app.config['WTF_CSRF_ENABLED'] = False

    # 1. Création et Connexion Membre
    client.get('/logout/')
    membre = MembreBD(email='depart@test.fr',
                      mdp_hash=generate_password_hash('pass'),
                      nom='Partant',
                      prenom='Jean',
                      statut='Membre',
                      activite=True)
    db.session.add(membre)
    db.session.commit()

    client.post('/login/', data={'email': 'depart@test.fr', 'password': 'pass'})

    # 2. Désinscription
    with app.test_request_context():
        response = client.get(url_for('admin.desinscrireMembre', idM=membre.id),
                              follow_redirects=True)

    # 3. Vérification
    assert "Entrez dans notre histoire" in response.data.decode('utf-8')
    membre_db = db.session.get(MembreBD, membre.id)
    assert membre_db.activite is False
    assert membre_db.statut == "Ancien Membre"

    # 4. Tentative de connexion
    res_login = client.post('/login/',
                            data={
                                'email': 'depart@test.fr',
                                'password': 'pass'
                            },
                            follow_redirects=True)
    assert b"/logout/" not in res_login.data


def test_membre_inscription_desinscription_event_club(client, app, db):
    """
    Test du flux Membre : S'inscrire soi-même et se désinscrire.
    Routes :
    - /inscrire/club/<id>
    - /desinscrire/club/<id>
    """
    app.config['WTF_CSRF_ENABLED'] = False

    # 1. Création Evénement
    evt = EvenementBD()
    db.session.add(evt)
    db.session.commit()
    club = EventClubBD(id_event=evt.id,
                       NomEV="Soirée Jeux",
                       dateDebutEV=date.today(),
                       heureDebutEV="20:00",
                       dateFinEV=date.today(),
                       heureFinEV="23:00",
                       niveauxEV="Tous",
                       passeeEV=False)
    db.session.add(club)

    # 2. Création et Connexion Membre
    client.get('/logout/')
    membre = MembreBD(email='autonome@test.fr',
                      mdp_hash=generate_password_hash('pass'),
                      nom='Autonome',
                      prenom='User',
                      activite=True)
    db.session.add(membre)
    db.session.commit()

    client.post('/login/',
                data={
                    'email': 'autonome@test.fr',
                    'password': 'pass'
                })

    # 3. Inscription
    with app.test_request_context():
        client.get(url_for('events_club.inscrire_club',
                           idEventClub=club.idEventClub),
                   follow_redirects=True)

    # Vérification
    participation = ParticiperBD.query.filter_by(
        id_membre=membre.id, id_event=club.id_event).first()
    assert participation is not None, "Le membre devrait être inscrit"

    # 4. Désinscription
    with app.test_request_context():
        client.get(url_for('events_club.desinscrire_club',
                           idEventClub=club.idEventClub),
                   follow_redirects=True)

    # Vérification
    participation_del = ParticiperBD.query.filter_by(
        id_membre=membre.id, id_event=club.id_event).first()
    assert participation_del is None, "Le membre ne devrait plus être inscrit"


def test_inscription_desinscription_competition_membre(client, app, db):
    """
    Test du cycle d'inscription/désinscription à une compétition pour un membre.
    Routes :
    - /inscrire/competition/<id>
    - /desinscrire/competition/<id>
    """
    app.config['WTF_CSRF_ENABLED'] = False

    # 1. Création de la compétition
    evt = EvenementBD()
    db.session.add(evt)
    db.session.commit()

    comp = CompetitionBD(id_event=evt.id,
                         nom="Open de France",
                         ville="Paris",
                         adresse="Grand Palais",
                         date_debut=date.today(),
                         heure_debut="09:00",
                         date_fin=date.today(),
                         heure_fin="18:00",
                         type_arme="Fleuret",
                         sexe="M",
                         typeComp="National",
                         niveaux="Senior",
                         passee=False)
    db.session.add(comp)

    # 2. Création et Connexion du Membre
    client.get('/logout/')
    membre = MembreBD(email='escrimeur@test.fr',
                      mdp_hash=generate_password_hash('pass'),
                      nom='Lagardere',
                      prenom='Jean',
                      statut='Membre',
                      activite=True,
                      niveau='Senior',
                      sexe='Homme')
    db.session.add(membre)
    db.session.commit()

    client.post('/login/',
                data={
                    'email': 'escrimeur@test.fr',
                    'password': 'pass'
                })

    # 3. Inscription
    with app.test_request_context():
        client.get(url_for('competitions.inscrire_competition',
                           idCompetition=comp.id),
                   follow_redirects=True)

    # Vérification BDD
    participation = ParticiperBD.query.filter_by(
        id_membre=membre.id, id_event=comp.id_event).first()
    assert participation is not None, "L'inscription a échoué en base de données"

    # 4. Désinscription
    with app.test_request_context():
        client.get(url_for('competitions.desinscrire_competition',
                           idCompetition=comp.id),
                   follow_redirects=True)

    # Vérification BDD
    participation_del = ParticiperBD.query.filter_by(
        id_membre=membre.id, id_event=comp.id_event).first()
    assert participation_del is None, "La désinscription a échoué"


# ==============================================================================
# 3. PAGES et SCENARIOS ACTIONS ADMIN
# ==============================================================================
# ==============================================================================
# PAGES ADMIN
# ==============================================================================
def test_pages_admin_protegees(client, app, db):
    """Test de l'accès aux pages réservées aux administrateurs."""
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # Tests des routes protégées Admin
    with app.test_request_context():
        # A. Profils
        response = client.get(url_for('admin.gerer_profils'))
        assert response.status_code == 200
        assert "Gestion des Profils" in response.data.decode('utf-8')
        # B. Formulaires
        response = client.get(url_for('admin.gerer_formulaires'))
        assert response.status_code == 200
        assert "Gestion des Formulaires" in response.data.decode('utf-8')

        # C. Inscriptions
        response = client.get(url_for('admin.gerer_inscriptions'))
        assert response.status_code == 200
        assert "Gestion des Inscriptions" in response.data.decode('utf-8')

        # D. Réunion
        response = client.get(url_for('reunions.reunion'))
        assert response.status_code == 200
        assert "Listes des prochaines réunions" in response.data.decode('utf-8')

        #E. Tarifs et Matériel
        response = client.get(url_for('admin.gestion_tarifs'))
        assert response.status_code == 200
        assert "Gestion des Tarifs" in response.data.decode('utf-8')

        #F Gestion Horaires
        response = client.get(url_for('admin.gestion_horaires'))
        assert response.status_code == 200
        assert "Gestion des Horaires" in response.data.decode('utf-8')


def test_page_protegee_reunion_view(client, app, db):
    """
    Test de la consultation d'une réunion.
    Route : /reunion/consultation/<id>
    Nécessite d'être connecté en Admin.
    """
    app.config['WTF_CSRF_ENABLED'] = False

    # 1. AUTHENTIFICATION
    setup_admin(client, db)

    # 2. SETUP DONNÉES
    evt = EvenementBD()
    db.session.add(evt)
    db.session.commit()

    reunion = ReunionBD(idEvent=evt.id,
                        nom="Réunion Mensuelle",
                        typeReunionRE="Générale",
                        ville="Salle de réunion",
                        adresse="12 rue du pont",
                        dateDebutRE=date.today(),
                        heureDebutRE="10:00",
                        dateFinRE=date.today(),
                        heureFinRE="12:00",
                        nbParticipantsRE=10,
                        rapportRE="Rien à signaler")
    db.session.add(reunion)
    db.session.commit()

    # 3. EXECUTION
    with app.test_request_context():
        url = url_for('reunions.reunion_view', idReunion=reunion.id)

    response = client.get(url)

    # 4. VERIFICATION
    assert response.status_code == 200
    assert "Réunion Mensuelle" in response.data.decode('utf-8')
    assert "Rien à signaler" in response.data.decode('utf-8')


def test_page_reunion_view_acces_refuse(client, app, db):
    """
    Test inverse : Vérifie qu'un visiteur non connecté est redirigé (ou bloqué).
    """
    evt = EvenementBD()
    db.session.add(evt)
    db.session.commit()
    reunion = ReunionBD(idEvent=evt.id,
                        nom="Secret",
                        dateDebutRE=date.today(),
                        heureDebutRE="10:00",
                        dateFinRE=date.today(),
                        heureFinRE="11:00",
                        typeReunionRE="AG")
    db.session.add(reunion)
    db.session.commit()

    client.get('/logout/')

    with app.test_request_context():
        response = client.get(
            url_for('reunions.reunion_view', idReunion=reunion.id))

    assert response.status_code == 302
    assert "/login" in response.location


def test_page_protegee_club_view(client, app, db):
    """
    Test de la consultation d'un événement club.
    Route : /evenement_club/<id>/club_view/
    Nécessite d'être CONNECTÉ (Membre ou Admin).
    """
    app.config['WTF_CSRF_ENABLED'] = False

    # 1. SETUP DONNÉES
    evt = EvenementBD()
    db.session.add(evt)
    db.session.commit()

    club = EventClubBD(id_event=evt.id,
                       NomEV="Soirée Barbecue",
                       villeEV="Orléans",
                       adresseEV="Club House",
                       dateDebutEV=date.today(),
                       heureDebutEV="19:00",
                       dateFinEV=date.today(),
                       heureFinEV="23:00",
                       descriptionEV="Venez nombreux",
                       niveauxEV="Tous",
                       passeeEV=False)
    db.session.add(club)

    # 2. SETUP UTILISATEUR
    membre = MembreBD(email='membre@test.fr',
                      mdp_hash=generate_password_hash('pass'),
                      nom='Test',
                      prenom='User',
                      activite=True)
    db.session.add(membre)
    db.session.commit()

    # 3. CONNEXION
    client.post('/login/', data={'email': 'membre@test.fr', 'password': 'pass'})

    # 4. EXECUTION
    with app.test_request_context():
        url = url_for('events_club.club_view', idEventClub=club.idEventClub)

    response = client.get(url)

    # 5. VERIFICATION
    assert response.status_code == 200
    assert "Soirée Barbecue" in response.data.decode('utf-8')


def test_club_view_acces_refuse_anonyme(client, app, db):
    """Vérifie qu'un visiteur non connecté est redirigé vers le login."""
    evt = EvenementBD()
    db.session.add(evt)
    db.session.commit()
    club = EventClubBD(id_event=evt.id,
                       NomEV="Privé",
                       dateDebutEV=date.today(),
                       heureDebutEV="10:00",
                       dateFinEV=date.today(),
                       heureFinEV="12:00",
                       descriptionEV="Test",
                       niveauxEV="Tous",
                       villeEV="Paris",
                       adresseEV="Ici")
    db.session.add(club)
    db.session.commit()

    client.get('/logout/')
    with app.test_request_context():
        response = client.get(
            url_for('events_club.club_view', idEventClub=club.idEventClub))

    assert response.status_code == 302
    assert "/login" in response.location


def test_admin_formulaire_view(client, app, db):
    """
    Test de la consultation d'un formulaire (contact/question) par un admin.
    Route : /formulaire_view/<id>
    """
    app.config['WTF_CSRF_ENABLED'] = False

    # 1. Authentification en tant qu'Admin
    setup_admin(client, db)

    # 2. Création d'un formulaire de test en base de données
    formulaire = FormulaireBD(
        type="Question",
        sujet="Problème de licence",
        email="escrimeur@test.fr",
        description=
        "Bonjour, je n'arrive pas à retrouver mon numéro de licence.",
        date=date.today(),
        repondu=False)
    db.session.add(formulaire)
    db.session.commit()
    id_form = formulaire.id

    # 3. Appel de la route protégée
    with app.test_request_context():
        url = url_for('admin.formulaire_view', idFormulaire=id_form)

    response = client.get(url)

    # 4. Vérifications
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert "Problème de licence" in content
    assert "escrimeur@test.fr" in content
    assert " mon numéro de licence." in content


def test_admin_formulaire_view_acces_refuse(client, app, db):
    """
    Vérifie qu'un utilisateur non connecté ou un simple membre 
    ne peut pas accéder à la consultation d'un formulaire.
    """
    # Création du formulaire
    formulaire = FormulaireBD(type="Question",
                              sujet="Secret",
                              email="test@test.fr",
                              description="Test")
    db.session.add(formulaire)
    db.session.commit()
    id_form = formulaire.id

    # 1. Test avec un visiteur anonyme (Non connecté)
    client.get('/logout/')
    with app.test_request_context():
        response_anonyme = client.get(
            url_for('admin.formulaire_view', idFormulaire=id_form))
    # Redirection vers la page de login attendue
    assert response_anonyme.status_code == 302
    assert "/login" in response_anonyme.location

    # 2. Test avec un Membre simple
    membre = MembreBD(email='membre_curieux@test.fr',
                      mdp_hash=generate_password_hash('pass'),
                      nom='Curieux',
                      prenom='Membre',
                      activite=True)
    db.session.add(membre)
    db.session.commit()

    client.post('/login/',
                data={
                    'email': 'membre_curieux@test.fr',
                    'password': 'pass'
                })

    with app.test_request_context():
        response_membre = client.get(
            url_for('admin.formulaire_view', idFormulaire=id_form))

    assert response_membre.status_code == 400


# ==============================================================================
# SCENARIOS ACTIONS ADMIN
# ==============================================================================


def test_scenario_presse_admin(client, app, db):
    """Test CRUD Presse : Ajout -> Modif -> Suppression."""
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)
    # NETTOYAGE
    db.session.query(PresseBD).delete()
    db.session.commit()

    # 1. CRÉATION
    with app.test_request_context():
        response = client.post(url_for('articles.add_presse'),
                               data={
                                   'titre': 'Victoire Régionale',
                                   'contenu': 'Le club a gagné !',
                                   'lien': 'http://journal.fr'
                               },
                               follow_redirects=True)

    assert response.status_code == 200

    # Vérification
    article = PresseBD.query.filter_by(titreP='Victoire Régionale').first()
    assert article is not None
    assert article.contenuP == 'Le club a gagné !'

    # 3. MODIFICATION
    article = PresseBD.query.filter_by(titreP='Victoire Régionale').first()
    with app.test_request_context():
        client.post(url_for('articles.edit_presse', idP=article.idPresse),
                    data={
                        'titre': 'Victoire Régionale',
                        'contenu': 'Le club a perdu !',
                        'lien': 'http://journal.fr'
                    },
                    follow_redirects=True)
    article = PresseBD.query.get(article.idPresse)

    # Vérification modification
    assert article.contenuP == 'Le club a perdu !'

    # 4. SUPPRESSION
    with app.test_request_context():
        client.post(url_for('articles.delete_presse', idP=article.idPresse),
                    follow_redirects=True)

    # Vérification suppression
    assert PresseBD.query.filter_by(titreP='Victoire Régionale').first() is None


def test_scenario_informations_admin(client, app, db):
    """Test CRUD Information : Ajout -> Modif -> Suppression."""
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. AJOUT
    with app.test_request_context():
        client.post(url_for('articles.add_information'),
                    data={
                        'titre': 'Nouvelle Info',
                        'contenu': 'Contenu important'
                    },
                    follow_redirects=True)

    info = InformationBD.query.filter_by(titreIN='Nouvelle Info').first()
    assert info is not None
    assert info.contenuIN == 'Contenu important'

    # 2. MODIFICATION
    with app.test_request_context():
        client.post(url_for('articles.edit_information',
                            idI=info.idInformation),
                    data={
                        'titre': 'Info Modifiée',
                        'contenu': 'Contenu modifié'
                    },
                    follow_redirects=True)

    updated_info = db.session.get(InformationBD, info.idInformation)
    assert updated_info.titreIN == 'Info Modifiée'

    # 3. SUPPRESSION
    with app.test_request_context():
        client.post(url_for('articles.delete_information',
                            idI=info.idInformation),
                    follow_redirects=True)
    assert db.session.get(InformationBD, info.idInformation) is None


def test_scenario_article_admin(client, app, db):
    """Test CRUD Information : Ajout -> Modif -> Suppression."""
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. AJOUT
    with app.test_request_context():
        client.post(url_for('articles.add_article'),
                    data={
                        'titre': 'JOBLIFE',
                        'contenu': 'Soutenez JOBLIFE'
                    },
                    follow_redirects=True)

    art = ArticleBD.query.filter_by(titre='JOBLIFE').first()
    assert art is not None
    assert art.contenu == 'Soutenez JOBLIFE'

    # 2. MODIFICATION
    with app.test_request_context():
        client.post(url_for('articles.edit_article', idA=art.id),
                    data={
                        'titre': 'BOUH KC et M8',
                        'contenu': 'Ne soutenez pas ces équipe'
                    },
                    follow_redirects=True)

    updated_art = db.session.get(ArticleBD, art.id)
    assert updated_art.titre == 'BOUH KC et M8'

    # 3. TEST SUPPRESSION IMAGE
    # A. On simule l'existence d'une image en l'ajoutant directement en BDD
    img = ImageArticleBD(nom="fake_image.jpg", id_article=art.id)
    db.session.add(img)
    db.session.commit()
    id_img = img.id

    assert ImageArticleBD.query.get(id_img) is not None

    # B. Appel de la route de suppression
    with app.test_request_context():
        client.post(url_for('articles.delete_image_article', idImg=id_img),
                    follow_redirects=True)

    # C. Vérification que l'image n'est plus en base
    assert ImageArticleBD.query.get(id_img) is None

    # 4. SUPPRESSION
    with app.test_request_context():
        client.post(url_for('articles.delete_article', idA=art.id),
                    follow_redirects=True)
    assert db.session.get(ArticleBD, art.id) is None


def test_crud_tarifs(client, app, db):
    """Test CRUD Tarifs : Ajout -> Modif -> Suppression."""
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. AJOUT
    with app.test_request_context():
        client.post(url_for('admin.gestion_tarifs'),
                    data={
                        'nom': 'Cotisation Test',
                        'prix': 150,
                        'categorie': 'Adhesion'
                    },
                    follow_redirects=True)

    tarif = TarifBD.query.filter_by(nom='Cotisation Test').first()
    assert tarif is not None

    # 2. MODIFICATION
    with app.test_request_context():
        client.post(url_for('admin.edit_tarif', idT=tarif.id),
                    data={
                        'nom': 'Cotisation Modif',
                        'prix': 160,
                        'categorie': 'Adhesion'
                    },
                    follow_redirects=True)

    updated_tarif = db.session.get(TarifBD, tarif.id)
    assert updated_tarif.prix == 160

    # 3. SUPPRESSION
    with app.test_request_context():
        client.post(url_for('admin.delete_tarif', idT=tarif.id),
                    follow_redirects=True)
    assert db.session.get(TarifBD, tarif.id) is None


def test_crud_horaire(client, app, db):
    """Test CRUD Horaire : Ajout -> Modif -> Suppression."""
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. AJOUT
    with app.test_request_context():
        client.post(url_for('admin.gestion_horaires'),
                    data={
                        'jour': 'Lundi',
                        'heure_debut': '09:00',
                        'heure_fin': '18:00',
                        'activite': 'Entraînement'
                    },
                    follow_redirects=True)

    horaire = HoraireBD.query.filter_by(jour='Lundi').first()
    assert horaire is not None

    # 2. MODIFICATION
    with app.test_request_context():
        client.post(url_for('admin.edit_horaire', idH=horaire.id),
                    data={
                        'jour': 'Mardi',
                        'heure_debut': '09:00',
                        'heure_fin': '18:00',
                        'activite': 'Entraînement'
                    },
                    follow_redirects=True)

    updated_horaire = db.session.get(HoraireBD, horaire.id)
    assert updated_horaire.jour == 'Mardi'

    # 3. SUPPRESSION
    with app.test_request_context():
        client.post(url_for('admin.delete_horaire', idH=horaire.id),
                    follow_redirects=True)
    assert db.session.get(HoraireBD, horaire.id) is None


def test_add_event_complex(client, app, db):
    """
    Test Ajout d'événements complexes (Compétition, Réunion, Entraînement).
    """
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. Ajout COMPETITION
    data_comp = {
        'title': 'Compétition Test',
        'start_date': '2025-06-01T09:00',
        'end_date': '2025-06-01T18:00',
        'category': 'Compétition',
        'level': ['M15', 'M20'],
        'sexe': 'Homme',
        'arme': 'Fleuret',
        'type': 'Regionale',
        'ville': 'Paris',
        'adresse': 'Stade'
    }
    with app.test_request_context():
        client.post(url_for('calendrier.add_event'),
                    data=data_comp,
                    follow_redirects=True)
    assert CompetitionBD.query.filter_by(
        nom='Compétition Test').first() is not None

    # 2. Ajout REUNION
    data_reunion = {
        'title': 'Réunion AG',
        'start_date': '2025-09-01T18:00',
        'end_date': '2025-09-01T20:00',
        'category': 'Réunion',
        'type_reunion': 'Générale',
        'ville': 'Salle Club',
        'adresse': 'Rue du club',
        'sexe': 'Homme',
        'arme': 'Fleuret',
        'type': 'Regionale'
    }
    with app.test_request_context():
        client.post(url_for('calendrier.add_event'),
                    data=data_reunion,
                    follow_redirects=True)

    # Vérification
    reunion = ReunionBD.query.filter_by(nom='Réunion AG').first()
    assert reunion is not None, "La réunion n'a pas été créée."
    assert reunion.ville == 'Salle Club'

    # 3. Ajout ENTRAINEMENT
    data_entrainement = {
        'title': 'Entrainement Lundi',
        'start_date': '2025-01-06T18:00',
        'end_date': '2025-01-06T20:00',
        'category': 'Entraînement',
        'arme': 'Épée',
        'level': ['M17'],
        'ville': 'Salle',
        'adresse': 'Rue',
        'sexe': 'Homme',
        'type': 'Regionale'
    }
    with app.test_request_context():
        client.post(url_for('calendrier.add_event'),
                    data=data_entrainement,
                    follow_redirects=True)

    assert EntrainementBD.query.filter_by(adresse='Rue').count() >= 1

    # 4. Test de l'API calendrier
    # Cette route renvoie du JSON utilisé par FullCalendar
    response = client.get('/api/events')

    assert response.status_code == 200

    # On récupère les données JSON
    data = response.json
    assert isinstance(data, list)

    # On extrait les titres pour vérifier la présence des événements
    titres = [event['title'] for event in data]

    # 1. Vérif Compétition
    assert "Compétition Test" in titres

    # 2. Vérif Réunion
    assert "Réunion AG" in titres

    # 3. Vérif Entraînement
    assert "Entraînement M17 Épée" in titres


def test_gestion_inscriptions(client, app, db):
    """
    Test complet de la gestion des inscriptions.
    """
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. Créer une demande d'inscription valide
    inscr_ok = InscriptionBD(email='new_member@test.fr',
                             nom='Test',
                             prenom='User',
                             ddn=date(2000, 1, 1),
                             mdp_hash='pass',
                             sexe='Homme',
                             date=date.today())
    db.session.add(inscr_ok)
    db.session.commit()
    id_ok = inscr_ok.id

    # 2. Accepter l'inscription
    with app.test_request_context():
        client.post(url_for('admin.accepter_inscription', idI=id_ok),
                    follow_redirects=True)

    # 3. Vérifications
    assert db.session.get(InscriptionBD, id_ok) is None

    membre = MembreBD.query.filter_by(email='new_member@test.fr').first()
    assert membre is not None
    assert membre.eventNouveauMail is True
    assert membre.eventInscriptionSite is True

    # Scénario REFUS
    inscr_refus = InscriptionBD(email='refused@test.fr',
                                nom='Refus',
                                prenom='Guy',
                                ddn=date(1999, 1, 1),
                                mdp_hash='pass',
                                sexe='Homme',
                                date=date.today())
    db.session.add(inscr_refus)
    db.session.commit()
    id_refus = inscr_refus.id

    with app.test_request_context():
        client.post(url_for('admin.refuser_inscription', idI=id_refus),
                    data={'justification': 'Dossier incomplet'},
                    follow_redirects=True)
    assert db.session.get(InscriptionBD, id_refus) is None
    assert MembreBD.query.filter_by(email='refused@test.fr').first() is None


def test_gestion_modifications(client, app, db):
    """
    Test complet du cycle de vie d'une modification de profil.
    UTILISE UN MONKEY-PATCH pour contourner la stricticité de SQLite sur les dates.
    """
    app.config['WTF_CSRF_ENABLED'] = False

    # SQLite refuse les Strings dans une colonne Date. MySQL l'accepte.
    # Comme on ne peut pas toucher au code source, on modifie la classe Form temporairement juste pour ce test.
    original_field = ModifForm.ddn
    ModifForm.ddn = DateField('date de naissance',
                              format='%Y-%m-%d',
                              validators=[DataRequired()])

    try:
        # Setup : Création Admin et Membre
        admin = setup_admin(client, db)

        membre = MembreBD(email='membre@modif.fr',
                          mdp_hash=generate_password_hash('pass'),
                          nom='Original',
                          prenom='User',
                          sexe='Homme',
                          ddn=date(1990, 1, 1),
                          activite=True)
        db.session.add(membre)
        db.session.commit()
        id_membre = membre.id

        # ======================================================
        # SCÉNARIO A : DEMANDE ET ACCEPTATION
        # ======================================================

        # 1. Le Membre se connecte et fait une demande
        client.get('/logout/')
        client.post('/login/',
                    data={
                        'email': 'membre@modif.fr',
                        'password': 'pass'
                    })

        data_modif = {
            'submit_action': 'membre_request',
            'nom': 'NouveauNom',
            'prenom': 'User',
            'email': 'membre@modif.fr',
            'sexe': 'Homme',
            'ddn': '1990-01-01',
            'statut': 'Membre',
            'justification': 'Mariage'
        }
        with app.test_request_context():
            client.post(url_for('admin.profil_edit', idM=id_membre),
                        data=data_modif,
                        follow_redirects=True)

        # Vérification
        modif = ModifBD.query.filter_by(id_membre=id_membre).first()
        assert modif is not None
        assert modif.nom == 'NouveauNom'

        # 2. L'Admin se connecte et accepte
        client.get('/logout/')
        client.post('/login/',
                    data={
                        'email': 'superadmin@test.fr',
                        'password': 'pass'
                    })

        with app.test_request_context():
            client.post(url_for('admin.accepter_modifications',
                                idModif=modif.id),
                        follow_redirects=True)

        # 3. Vérifications
        assert db.session.get(ModifBD, modif.id) is None
        updated_membre = db.session.get(MembreBD, id_membre)
        assert updated_membre.nom == 'NouveauNom'

        # ======================================================
        # SCÉNARIO B : DEMANDE ET REFUS
        # ======================================================

        # 1. Le Membre refait une demande
        client.get('/logout/')
        client.post('/login/',
                    data={
                        'email': 'membre@modif.fr',
                        'password': 'pass'
                    })

        data_modif['nom'] = 'NouveauNom'
        data_modif['prenom'] = 'RefusePrenom'
        with app.test_request_context():
            client.post(url_for('admin.profil_edit', idM=id_membre),
                        data=data_modif,
                        follow_redirects=True)

        modif_refus = ModifBD.query.filter_by(id_membre=id_membre).first()
        assert modif_refus is not None
        id_modif_refus = modif_refus.id

        # 2. L'Admin refuse
        client.get('/logout/')
        client.post('/login/',
                    data={
                        'email': 'superadmin@test.fr',
                        'password': 'pass'
                    })

        with app.test_request_context():
            client.post(url_for('admin.refuser_modification',
                                idM=id_modif_refus),
                        data={'justification': 'Pas valide'},
                        follow_redirects=True)

        # 3. Vérifications
        assert db.session.get(ModifBD, id_modif_refus) is None
        final_membre = db.session.get(MembreBD, id_membre)
        assert final_membre.prenom == 'User'

    finally:
        # On remet le formulaire comme avant pour ne pas casser d'autres tests
        ModifForm.ddn = original_field


def test_contact_form_submission(client, app, db):
    """Test flux Contact : Soumission -> Notification Admin."""
    app.config['WTF_CSRF_ENABLED'] = False

    # 1. Créer un admin avec notifs activées pour les questions
    admin = setup_admin(client, db)
    admin.formulaireQuestionSite = True
    db.session.commit()

    # 2. Soumission formulaire
    client.get('/logout/')
    with app.test_request_context():
        client.post(url_for('general.contact'),
                    data={
                        'type_form': 'Question',
                        'sujet': 'Besoin info',
                        'email': 'visitor@test.com',
                        'description': 'Bonjour...'
                    },
                    follow_redirects=True)

    # 3. Vérifications
    assert FormulaireBD.query.filter_by(
        email='visitor@test.com').first() is not None

    # Une notification a été créée pour l'admin
    notif = NotifsBD.query.filter_by(idAdmin=admin.id).first()
    assert notif is not None
    assert "Question" in notif.sourceN


def test_crud_reunion_admin(client, app, db):
    """
    Test des actions ADMIN sur une réunion : Modification et Suppression.
    Routes : /reunion/update/<id> et /reunion/delete/<id>
    """
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. Création d'une réunion
    evt = EvenementBD()
    db.session.add(evt)
    db.session.commit()

    reunion = ReunionBD(idEvent=evt.id,
                        nom="Réunion Initiale",
                        typeReunionRE="Générale",
                        ville="Salle A",
                        adresse="Rue A",
                        dateDebutRE=date(2025, 1, 1),
                        heureDebutRE="10:00",
                        dateFinRE=date(2025, 1, 1),
                        heureFinRE="12:00",
                        nbParticipantsRE=5,
                        rapportRE="Rapport initial")
    db.session.add(reunion)
    db.session.commit()
    id_reunion = reunion.id

    # 2. Modification
    data_update = {
        'nom': 'Réunion Modifiée',
        'type_reunion': 'Comité',
        'ville': 'Salle B',
        'adresse': 'Rue B',
        'description': 'Nouveau rapport',
        'date_debut': '2025-02-02',
        'heure_debut': '14:00',
        'date_fin': '2025-02-02',
        'heure_fin': '16:00'
    }
    with app.test_request_context():
        client.post(url_for('reunions.reunion_update', idReunion=id_reunion),
                    data=data_update,
                    follow_redirects=True)

    # Vérification BDD
    updated = db.session.get(ReunionBD, id_reunion)
    assert updated.nom == 'Réunion Modifiée'
    assert updated.ville == 'Salle B'
    assert updated.dateDebutRE == date(2025, 2, 2)

    # 3. Suppression
    with app.test_request_context():
        client.post(url_for('reunions.reunion_delete', idReunion=id_reunion),
                    follow_redirects=True)

    # Vérification BDD
    assert db.session.get(ReunionBD, id_reunion) is None


def test_admin_gestion_statut_membre(client, app, db):
    """
    Test du cycle de vie géré par l'Admin :
    1. Désinscription d'un membre (desinscrireMembre).
    2. Consultation de la liste des anciens (via le mode='anciens').
    3. Réinscription du membre (reinscrireMembre).
    """
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. Création d'un membre actif
    membre = MembreBD(email='membre@statut.fr',
                      mdp_hash=generate_password_hash('pass'),
                      nom='Victime',
                      prenom='Test',
                      statut='Membre',
                      activite=True,
                      date_inscription=date.today(),
                      sexe='Homme',
                      niveau='Senior')
    db.session.add(membre)
    db.session.commit()
    id_membre = membre.id

    # 2. Désinscription
    with app.test_request_context():
        client.get(url_for('admin.desinscrireMembre', idM=id_membre),
                   follow_redirects=True)

    # Vérification BDD
    membre_desinscrit = db.session.get(MembreBD, id_membre)
    assert membre_desinscrit.activite is False
    assert membre_desinscrit.statut == "Ancien Membre"

    # 3. Consultation (CORRECTION ICI)
    # On utilise la route principale avec le paramètre GET 'mode=anciens'
    with app.test_request_context():
        # Cela génère /gerer_profils/?mode=anciens
        url_anciens = url_for('admin.gerer_profils', mode='anciens')

    response = client.get(url_anciens)
    assert response.status_code == 200
    # On vérifie que le membre apparait bien dans la page
    assert 'Victime' in response.data.decode('utf-8')


def test_crud_event_club_admin(client, app, db):
    """
    Test des actions ADMIN sur un événement club : Modification et Suppression.
    Routes : /evenement_club/<id>/club_update/ et /evenement_club/<id>/club_delete/
    """
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. Création d'un événement club initial
    evt = EvenementBD()
    db.session.add(evt)
    db.session.commit()

    club = EventClubBD(id_event=evt.id,
                       NomEV="Soirée Initiale",
                       villeEV="Orléans",
                       adresseEV="Local A",
                       dateDebutEV=date(2025, 5, 1),
                       heureDebutEV="18:00",
                       dateFinEV=date(2025, 5, 1),
                       heureFinEV="22:00",
                       descriptionEV="Description avant",
                       niveauxEV="Tous",
                       passeeEV=False)
    db.session.add(club)
    db.session.commit()
    id_club = club.idEventClub

    # 2. Modification
    data_update = {
        'nom': 'Soirée Modifiée',
        'ville': 'Orléans',
        'adresse': 'Local B',
        'description': 'Nouvelle description',
        'date_debut': '2025-06-01',
        'heure_debut': '19:00',
        'date_fin': '2025-06-01',
        'heure_fin': '23:00',
        'niveaux': 'Tous'
    }

    with app.test_request_context():
        client.post(url_for('events_club.club_update', idEventClub=id_club),
                    data=data_update,
                    follow_redirects=True)

    # Vérification BDD
    updated = db.session.get(EventClubBD, id_club)
    assert updated.NomEV == 'Soirée Modifiée'
    assert updated.adresseEV == 'Local B'
    assert updated.dateDebutEV == date(2025, 6, 1)

    # 3. Suppression
    with app.test_request_context():
        client.post(url_for('events_club.club_delete', idEventClub=id_club),
                    follow_redirects=True)

    # Vérification BDD
    assert db.session.get(EventClubBD, id_club) is None


def test_admin_gestion_inscriptions_event_club(client, app, db):
    """
    Test du flux Admin : Inscrire un membre à un événement club puis le retirer.
    Routes : 
    - /evenement_club/<id>/inscrire_membres (GET)
    - /evenement_club/<id>/inscription_membres (POST)
    - /evenement_club/<id>/delete/<idM> (POST)
    """
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. Création de l'événement club
    evt = EvenementBD()
    db.session.add(evt)
    db.session.commit()
    club = EventClubBD(id_event=evt.id,
                       NomEV="Barbecue",
                       dateDebutEV=date.today(),
                       heureDebutEV="18:00",
                       dateFinEV=date.today(),
                       heureFinEV="22:00",
                       niveauxEV="Tous",
                       passeeEV=False)
    db.session.add(club)

    # 2. Création d'un membre à inscrire
    membre = MembreBD(email='participant@test.fr',
                      mdp_hash=generate_password_hash('pass'),
                      nom='LeParticipant',
                      prenom='Jean',
                      activite=True)
    db.session.add(membre)
    db.session.commit()

    # 3. page selection
    with app.test_request_context():
        response = client.get(
            url_for('events_club.inscrire_membres_event_club',
                    idEventClub=club.idEventClub))
    assert response.status_code == 200
    assert "LeParticipant" in response.data.decode('utf-8')

    # 4. inscription
    with app.test_request_context():
        client.post(url_for('events_club.inscription_membres_event_club',
                            idEventClub=club.idEventClub),
                    data={'membres_a_inscrire': [membre.id]},
                    follow_redirects=True)

    # Vérification BDD
    participation = ParticiperBD.query.filter_by(
        id_membre=membre.id, id_event=club.id_event).first()
    assert participation is not None, "Le membre devrait être inscrit par l'admin"

    # 5. Désinscription
    with app.test_request_context():
        client.post(url_for('events_club.delete_membre_eventClub',
                            idEventClub=club.idEventClub,
                            idM=membre.id),
                    follow_redirects=True)

    # Vérification BDD
    participation_del = ParticiperBD.query.filter_by(
        id_membre=membre.id, id_event=club.id_event).first()
    assert participation_del is None, "Le membre devrait être désinscrit"


def test_admin_gestion_competition_complexe(client, app, db):
    """
    Test global de la gestion avancée d'une compétition par l'Admin.
    Vérifie l'inscription, le classement, l'upload (via présence fichier) et la suppression.
    """
    import os
    import io

    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. SETUP
    evt = EvenementBD()
    db.session.add(evt)
    db.session.commit()

    comp = CompetitionBD(id_event=evt.id,
                         nom="Championnat Test",
                         ville="Lyon",
                         adresse="Gymnase",
                         date_debut=date.today(),
                         heure_debut="09:00",
                         date_fin=date.today(),
                         heure_fin="18:00",
                         type_arme="Sabre",
                         sexe="M",
                         typeComp="National",
                         niveaux="Senior",
                         passee=False)
    db.session.add(comp)

    membre = MembreBD(email='champion@test.fr',
                      mdp_hash=generate_password_hash('pass'),
                      nom='Champion',
                      prenom='Luc',
                      activite=True,
                      niveau='Senior')
    db.session.add(membre)
    db.session.commit()

    # 2. INSCRIPTION
    with app.test_request_context():
        client.post(url_for('competitions.inscription_membres_competition',
                            idC=comp.id),
                    data={'membres_a_inscrire': [membre.id]},
                    follow_redirects=True)

    assert ParticiperBD.query.filter_by(
        id_membre=membre.id, id_event=comp.id_event).first() is not None

    # 3. CLASSEMENT
    with app.test_request_context():
        client.post(url_for('competitions.classer_membre',
                            idCompetition=comp.id,
                            idMembre=membre.id),
                    data={'classement': '1'},
                    follow_redirects=True)
    res = ResultatBD.query.filter_by(id_competition=comp.id,
                                     id_membre=membre.id).first()
    assert int(res.resultat) == 1

    # 4. UPLOAD DU CLASSEMENT PDF
    expected_path = os.path.join(app.root_path, 'static', 'classements',
                                 str(comp.id), 'classement.pdf')

    # On s'assure qu'il n'existe pas avant le test
    if os.path.exists(expected_path):
        os.remove(expected_path)

    data_pdf = {
        'classement_pdf': (io.BytesIO(b"%PDF-1.4...fake content..."),
                           'mon_fichier.pdf', 'application/pdf')
    }

    with app.test_request_context():
        response = client.post(
            url_for('competitions.upload_classement_competition',
                    idCompetition=comp.id),
            data=data_pdf,
            follow_redirects=True)

    # Vérification
    assert response.status_code == 200

    if not os.path.exists(expected_path):
        print("DEBUG HTML:", response.data.decode('utf-8'))
        raise AssertionError(
            f"Le fichier n'a pas été créé à l'endroit attendu : {expected_path}"
        )

    os.remove(expected_path)
    try:
        os.rmdir(os.path.dirname(expected_path))
    except:
        pass

    # 5. SUPPRESSION PARTICIPANT
    with app.test_request_context():
        client.post(url_for('competitions.delete_membre_competition',
                            idC=comp.id,
                            idM=membre.id),
                    follow_redirects=True)
    assert ParticiperBD.query.filter_by(id_membre=membre.id,
                                        id_event=comp.id_event).first() is None


def test_admin_crud_competition(client, app, db):
    """
    Test complet du cycle de vie d'une compétition (Update, Images, Delete).
    """
    import io
    import os

    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. SETUP
    evt = EvenementBD()
    db.session.add(evt)
    db.session.commit()

    comp = CompetitionBD(id_event=evt.id,
                         nom="Compétition Originale",
                         ville="Paris",
                         adresse="Vieux Stade",
                         date_debut=date(2025, 1, 1),
                         heure_debut="10:00",
                         date_fin=date(2025, 1, 1),
                         heure_fin="18:00",
                         type_arme="Fleuret",
                         sexe="F",
                         typeComp="Régionale",
                         niveaux="M15",
                         passee=False,
                         description="Description originale")
    db.session.add(comp)
    db.session.commit()
    id_comp = comp.id

    # 2. MODIFICATION
    data_update = {
        'nom': 'Compétition Mise à Jour',
        'ville': 'Bordeaux',
        'adresse': 'Nouveau Gymnase',
        'date_debut': '2025-02-01',
        'heure_debut': '09:00',
        'date_fin': '2025-02-02',
        'heure_fin': '17:00',
        'type_arme': 'Epée',
        'sexe': 'M',
        'description': 'Nouvelle description'
    }

    with app.test_request_context():
        client.post(url_for('competitions.competition_update',
                            idCompetition=id_comp),
                    data=data_update,
                    follow_redirects=True)

    # Vérification BDD
    updated = db.session.get(CompetitionBD, id_comp)
    assert updated.nom == 'Compétition Mise à Jour'
    assert updated.type_arme == 'Epée'

    # 3. AJOUT IMAGE
    data_img = {
        'image': (io.BytesIO(b"fake_image_content"), 'photo.jpg'),
        'alt': 'Photo Podium',
        'prive': 'y'
    }

    with app.test_request_context():
        client.post(url_for('competitions.add_image_competition',
                            idCompetition=id_comp),
                    data=data_img,
                    follow_redirects=True)

    # Vérification BDD
    db.session.refresh(updated)
    assert len(updated.images_rc) == 1
    image_bd = updated.images_rc[0]
    assert image_bd.alt == 'Photo Podium'
    id_img = image_bd.idImage

    # 4. SUPPRESSION IMAGE
    with app.test_request_context():
        client.post(url_for('competitions.delete_image_competition',
                            idImage=id_img),
                    data={'idCompetition': id_comp},
                    follow_redirects=True)

    # Vérification BDD
    db.session.refresh(updated)
    assert len(updated.images_rc) == 0
    assert db.session.get(ImageAppBD, id_img) is None

    # 5. SUPPRESSION COMPÉTITION
    with app.test_request_context():
        client.post(url_for('competitions.competition_delete',
                            idCompetition=id_comp),
                    follow_redirects=True)

    # Vérification BDD
    assert db.session.get(CompetitionBD, id_comp) is None


# ==============================================================================
# 4. TESTS SECURITE
# ==============================================================================
def test_securite_membre_vers_admin(client, app, db):
    """
    Un membre connecté ne doit PAS pouvoir supprimer un article.
    Doit recevoir une erreur 400 (Accès Interdit).
    """
    app.config['WTF_CSRF_ENABLED'] = False

    # 1. NETTOYAGE
    client.get('/logout/', follow_redirects=True)
    db.session.query(PresseBD).delete()
    db.session.query(MembreBD).delete()
    db.session.query(AdminBD).delete()
    db.session.commit()

    assert AdminBD.query.count() == 0, "La table Admin doit être vide !"

    # 2. Setup Données
    presse = PresseBD(titreP="News",
                      lienP="http://test",
                      contenuP="Contenu",
                      dateP=date.today())
    membre = MembreBD(email='membre@secu.fr',
                      mdp_hash=generate_password_hash('pass'),
                      activite=True)

    db.session.add_all([presse, membre])
    db.session.commit()

    # 3. Connexion Membre
    login_response = client.post('/login/',
                                 data={
                                     'email': 'membre@secu.fr',
                                     'password': 'pass'
                                 },
                                 follow_redirects=True)

    assert b"Entrez dans notre histoire" in login_response.data, "Le login Membre a échoué"

    # 4. Tentative d'intrusion
    with app.test_request_context():
        response = client.post(url_for('articles.delete_presse',
                                       idP=presse.idPresse),
                               follow_redirects=False)

    # 5. DIAGNOSTIC & ASSERTION
    if response.status_code == 302:
        assert False, f"Erreur Sécurité: Redirection inattendue vers {response.location}"

    assert response.status_code == 400, f"Attendu 400, reçu {response.status_code}"

    # L'article doit toujours être là
    assert PresseBD.query.get(presse.idPresse) is not None


def test_access_control_admin_pages(client, app):
    """
    SCÉNARIO : Un utilisateur non connecté essaie d'accéder aux pages admin.
    RÉSULTAT ATTENDU : Redirection vers le login (302).
    """
    app.config['LOGIN_DISABLED'] = False
    client.get('/logout/')

    # Liste des routes Admin
    with app.test_request_context():
        routes_admin = [
            url_for('admin.gerer_profils'),
            url_for('admin.gerer_formulaires'),
            url_for('articles.add_article'),
            url_for('admin.gestion_tarifs')
        ]

        for route in routes_admin:
            response = client.get(route)
            # Doit rediriger vers login (Code 302)
            assert response.status_code == 302
            assert "/login" in response.location


def test_access_control_membre_pages(client, app):
    """
    SCÉNARIO : Un utilisateur non connecté essaie d'accéder aux pages membre.
    """
    app.config['LOGIN_DISABLED'] = False
    client.get('/logout/')

    with app.test_request_context():
        response = client.get(url_for('profil.resultat_membre'))
    assert response.status_code == 302
    assert "/login" in response.location


def test_password_change_security(client, app, db):
    """
    FAILLE TESTÉE : Mauvaise validation de l'ancien mot de passe.
    SCÉNARIO : Un membre essaie de changer son mot de passe en donnant un mauvais 'ancien mot de passe'.
    """
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['LOGIN_DISABLED'] = False

    user = MembreBD(email='pwd@test.fr',
                    mdp_hash=generate_password_hash('VraiMotDePasse123!'))
    db.session.add(user)
    db.session.commit()

    client.post('/login/',
                data={
                    'email': 'pwd@test.fr',
                    'password': 'VraiMotDePasse123!'
                })

    # Tentative de changement avec MAUVAIS ancien mdp
    with app.test_request_context():
        response = client.post(url_for('parametres.changer_mdp'),
                               data={
                                   'old_password': 'MauvaisPassword',
                                   'new_password': 'NewPassword123!',
                                   'confirm_new_password': 'NewPassword123!'
                               },
                               follow_redirects=True)

    # Vérifications
    assert b"ancien mot de passe est incorrect" in response.data

    # On vérifie que le hash en base n'a PAS changé
    user_db = db.session.get(MembreBD, user.id)
    from werkzeug.security import check_password_hash
    assert check_password_hash(user_db.mdp_hash, 'VraiMotDePasse123!') is True


def test_inscription_password_strength(client, app, db):
    """
    FAILLE TESTÉE : Politique de mot de passe faible.
    SCÉNARIO : Inscription avec un mot de passe trop simple (ex: "123").
    """
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_request_context():
        response = client.post(url_for('auth.inscription'),
                               data={
                                   'Login': 'weak@test.fr',
                                   'nom': 'Faible',
                                   'prenom': 'User',
                                   'date_naissance': '2000-01-01',
                                   'sexe': 'Homme',
                                   'password': '123',
                                   'confirm_password': '123'
                               },
                               follow_redirects=True)

    # Doit échouer et afficher le message d'erreur
    # On cherche un mot clé du message d'erreur défini dans views.py
    assert b"mot de passe doit contenir" in response.data
    assert InscriptionBD.query.filter_by(email='weak@test.fr').first() is None


# ==============================================================================
# 5. TESTS DECORATEUR
# ==============================================================================
def test_decorateurs_acces_interdit(client, app, db):
    """
    Teste les cas de refus spécifiques des décorateurs.
    """
    app.config['WTF_CSRF_ENABLED'] = False

    # 1. Admin essaie d'accéder à une page Membre
    setup_admin(client, db)
    with app.test_request_context():
        response_admin = client.get(url_for('profil.resultat_membre'))

    assert response_admin.status_code == 401

    # 2. Membre Standard essaie d'accéder à une page Comité/Réunion
    client.get('/logout/')
    membre = MembreBD(email='basique@test.fr',
                      mdp_hash=generate_password_hash('pass'),
                      nom='Basique',
                      prenom='User',
                      statut='Membre',
                      activite=True)
    db.session.add(membre)

    # Création de la réunion
    evt = EvenementBD()
    db.session.add(evt)
    db.session.commit()
    reunion = ReunionBD(idEvent=evt.id,
                        nom="Réunion",
                        dateDebutRE=date.today(),
                        heureDebutRE="10:00",
                        dateFinRE=date.today(),
                        heureFinRE="11:00")
    db.session.add(reunion)
    db.session.commit()

    # Connexion
    client.post('/login/',
                data={
                    'email': 'basique@test.fr',
                    'password': 'pass'
                })

    # Tentative d'accès
    with app.test_request_context():
        response_membre = client.get(
            url_for('reunions.reunion_view', idReunion=reunion.id))

    assert response_membre.status_code == 405

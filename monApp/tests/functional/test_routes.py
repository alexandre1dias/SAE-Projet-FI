import pytest
from flask import url_for
from werkzeug.security import generate_password_hash
from datetime import date, datetime
from monApp.modelBD import *

# ==============================================================================
# HELPER (Fonction utilitaire)
# ==============================================================================
def setup_admin(client, db):
    """
    Fonction utilitaire pour nettoyer la base, créer un admin et le connecter.
    Utilisée dans les tests CRUD Admin.
    """
    # Nettoyage
    client.get('/logout/', follow_redirects=True)
    db.session.query(AdminBD).delete()
    db.session.commit()

    # Création Admin
    admin = AdminBD(email='superadmin@test.fr', mdp_hash=generate_password_hash('pass'))
    db.session.add(admin)
    db.session.commit()

    # Connexion
    client.post('/login/', data={'email': 'superadmin@test.fr', 'password': 'pass'})
    return admin

# ==============================================================================
# 1. PAGES PUBLIQUES (Accessibles sans connexion)
# ==============================================================================
@pytest.mark.parametrize("page, text", [
    ('index', 'Entrez dans notre histoire'),
    ('contact', 'Nous Contacter'),
    ('historique', "L'HISTOIRE DU CERCLE"),
    ('comite_cercle', 'Comité directeur du cercle'),
    ('adresse', 'Adresse'),
    ('horaires', 'Horaire'),
    ('adhesions', "Choississez votre adhésion"),
    ('materiel', "Matériel et tenue d'escrime"),
    ('escrime_feminin', "Mesdames, en Garde !"),
    ('calendrier', "Calendrier des Évènements"),
    ('competitions', "Listes des prochaines compétitions"),
    ('informations', 'Informations'),
    ('presse', 'Presse'),
    ('articles', 'Articles du Club')
])
def test_pages_publiques_avec_url_for(client, app, page, text):
    """Test des pages accessibles à tous."""
    with app.test_request_context():
        url = url_for(page)
    response = client.get(url)
    assert response.status_code == 200
    assert text in response.data.decode('utf-8')

# ==============================================================================
# 2. PAGES MEMBRES
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
    membre = MembreBD(
        email='membre@test.fr', 
        mdp_hash=generate_password_hash(mdp_clair),
        nom='Test',
        prenom='User',
        date_inscription=date.today(),
        activite=True,
        statut='Membre',
        sexe='Homme',
        ddn=date(2000, 1, 1)
    )
    db.session.add(membre)
    db.session.commit()

    # 2. Connexion
    client.post('/login/', data={
        'email': 'membre@test.fr',
        'password': mdp_clair
    }, follow_redirects=True)

    # 3. Test des routes protégées
    with app.test_request_context():
        # A. Résultats
        response = client.get(url_for('resultat_membre'))
        assert response.status_code == 200
        assert "Résultat du Membre" in response.data.decode('utf-8')

        # B. Événements
        response = client.get(url_for('evenement_membre'))
        assert response.status_code == 200
        assert "Vos Évènements" in response.data.decode('utf-8')

        # C. Profil
        response = client.get(url_for('profil_view', idM=membre.id)) 
        assert response.status_code == 200
        content = response.data.decode('utf-8')
        assert "Profil de" in content or "Profil Membre" in content

# ==============================================================================
# 3. PAGES ADMIN (Accès basique)
# ==============================================================================
def test_pages_admin_protegees(client, app, db):
    """Test de l'accès aux pages réservées aux administrateurs."""
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # Tests des routes protégées Admin
    with app.test_request_context():
        # A. Profils
        response = client.get(url_for('gerer_profils'))
        assert response.status_code == 200
        assert "Gestion des Profils" in response.data.decode('utf-8')

        # B. Formulaires
        response = client.get(url_for('gerer_formulaires'))
        assert response.status_code == 200
        content = response.data.decode('utf-8')
        assert "Gestion des Formulaires" in content or "Géstion des Formulaires" in content

        # C. Inscriptions
        response = client.get(url_for('gerer_inscriptions'))
        assert response.status_code == 200
        content = response.data.decode('utf-8')
        assert "Gestion des Inscriptions" in content or "Géstion des Inscriptions" in content

# ==============================================================================
# 4. SCENARIOS ACTIONS ADMIN
# ==============================================================================

def test_scenario_presse_admin(client, app, db):
    """Test CRUD Presse : Ajout -> Vérif -> Suppression."""
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)
    # NETTOYAGE
    db.session.query(PresseBD).delete()
    db.session.commit()

    # 1. CRÉATION
    response = client.post('/admin/add_presse/', data={
        'titre': 'Victoire Régionale',
        'contenu': 'Le club a gagné !',
        'lien': 'http://journal.fr'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # 2. VÉRIFICATION BDD
    article = PresseBD.query.filter_by(titreP='Victoire Régionale').first()
    assert article is not None
    assert article.contenuP == 'Le club a gagné !'

    # 3. SUPPRESSION
    client.post(f'/admin/delete_presse/{article.idPresse}', follow_redirects=True)
    
    # Vérification suppression
    assert PresseBD.query.filter_by(titreP='Victoire Régionale').first() is None

def test_crud_informations(client, app, db):
    """Test CRUD Information : Ajout -> Modif -> Suppression."""
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. AJOUT
    client.post('/admin/add_information/', data={
        'titre': 'Nouvelle Info',
        'contenu': 'Contenu important'
    }, follow_redirects=True)
    
    info = InformationBD.query.filter_by(titreIN='Nouvelle Info').first()
    assert info is not None
    assert info.contenuIN == 'Contenu important'

    # 2. MODIFICATION
    client.post(f'/admin/edit_information/{info.idInformation}', data={
        'titre': 'Info Modifiée',
        'contenu': 'Contenu modifié'
    }, follow_redirects=True)
    
    updated_info = db.session.get(InformationBD, info.idInformation)
    assert updated_info.titreIN == 'Info Modifiée'

    # 3. SUPPRESSION
    client.post(f'/admin/delete_information/{info.idInformation}', follow_redirects=True)
    assert db.session.get(InformationBD, info.idInformation) is None

def test_crud_tarifs(client, app, db):
    """Test CRUD Tarifs : Ajout -> Modif -> Suppression."""
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. AJOUT
    client.post('/admin/gestion_tarifs/', data={
        'nom': 'Cotisation Test',
        'prix': 150,
        'categorie': 'Adhesion'
    }, follow_redirects=True)
    
    tarif = TarifBD.query.filter_by(nom='Cotisation Test').first()
    assert tarif is not None

    # 2. MODIFICATION
    client.post(f'/admin/edit_tarif/{tarif.id}', data={
        'nom': 'Cotisation Modif',
        'prix': 160,
        'categorie': 'Adhesion'
    }, follow_redirects=True)
    
    updated_tarif = db.session.get(TarifBD, tarif.id)
    assert updated_tarif.prix == 160

    # 3. SUPPRESSION
    client.post(f'/admin/delete_tarif/{tarif.id}', follow_redirects=True)
    assert db.session.get(TarifBD, tarif.id) is None

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
    client.post('/add_event/', data=data_comp, follow_redirects=True)
    assert CompetitionBD.query.filter_by(nom='Compétition Test').first() is not None

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
    client.post('/add_event/', data=data_reunion, follow_redirects=True)
    
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
    client.post('/add_event/', data=data_entrainement, follow_redirects=True)
    
    assert EntrainementBD.query.filter_by(adresse='Rue').count() >= 1


def test_gestion_inscriptions(client, app, db):
    """Test flux Inscription : Création demande -> Acceptation -> Création Membre."""
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. Créer une demande d'inscription
    inscr = InscriptionBD(
        email='new_member@test.fr', nom='Test', prenom='User', 
        ddn=date(2000,1,1), mdp_hash='pass', sexe='Homme', date=date.today()
    )
    db.session.add(inscr)
    db.session.commit()

    # 2. Accepter l'inscription via la route admin
    client.post(f'/accepter_inscription/{inscr.id}', follow_redirects=True)
    
    # 3. Vérifications
    assert db.session.get(InscriptionBD, inscr.id) is None
    
    # Le membre doit être créé
    membre = MembreBD.query.filter_by(email='new_member@test.fr').first()
    assert membre is not None
    
    # Les paramètres de notification doivent être initialisés
    assert membre.idParaNotif is not None
    param = ParametreNotifMembreBD.query.get(membre.idParaNotif)
    assert param.eventNouveauMail is True

def test_contact_form_submission(client, app, db):
    """Test flux Contact : Soumission -> Notification Admin."""
    app.config['WTF_CSRF_ENABLED'] = False
    
    # 1. Créer un admin avec notifs activées pour les questions
    admin = setup_admin(client, db)
    params = ParametreNotifAdminBD(idAdmin=admin.id, formulaireQuestionSite=True)
    db.session.add(params)
    db.session.commit()

    # 2. Soumission formulaire
    client.get('/logout/')
    client.post('/contact/', data={
        'type_form': 'Question',
        'sujet': 'Besoin info',
        'email': 'visitor@test.com',
        'description': 'Bonjour...'
    }, follow_redirects=True)

    # 3. Vérifications
    assert FormulaireBD.query.filter_by(email='visitor@test.com').first() is not None
    
    # Une notification a été créée pour l'admin
    notif = NotifsBD.query.filter_by(idAdmin=admin.id).first()
    assert notif is not None
    assert "Question" in notif.sourceN

# ==============================================================================
# 5. TESTS SECURITE
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
    presse = PresseBD(titreP="News", lienP="http://test", contenuP="Contenu", dateP=date.today())
    membre = MembreBD(email='membre@secu.fr', mdp_hash=generate_password_hash('pass'), activite=True)
    
    db.session.add_all([presse, membre])
    db.session.commit()

    # 3. Connexion Membre
    login_response = client.post('/login/', data={
        'email': 'membre@secu.fr', 
        'password': 'pass'
    }, follow_redirects=True)
    
    assert b"Entrez dans notre histoire" in login_response.data, "Le login Membre a échoué"

    # 4. Tentative d'intrusion
    response = client.post(f'/admin/delete_presse/{presse.idPresse}', follow_redirects=False)

    # 5. DIAGNOSTIC & ASSERTION
    if response.status_code == 302:
        assert False, f"Erreur Sécurité: Redirection inattendue vers {response.location}"
    
    assert response.status_code == 400, f"Attendu 400, reçu {response.status_code}"
    
    # L'article doit toujours être là
    assert PresseBD.query.get(presse.idPresse) is not None
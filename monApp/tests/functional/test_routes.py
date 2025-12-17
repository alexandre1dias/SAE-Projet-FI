import pytest
from flask import url_for
from werkzeug.security import generate_password_hash
from datetime import date
from monApp.modelBD import *

# ==============================================================================
# 1. PAGES PUBLIQUES (Accessibles sans connexion, sans ID)
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
# 2. PAGES MEMBRES (Nécessitent connexion)
# ==============================================================================
def test_pages_membres_protegees(client, app, db):
    """Test des pages réservées aux membres connectés."""
    app.config['WTF_CSRF_ENABLED'] = False
    
    # NETTOYAGE : On s'assure qu'aucun utilisateur n'est connecté avant de commencer
    client.get('/logout/', follow_redirects=True)

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
    # A. Résultats
    with app.test_request_context():
        url_res = url_for('resultat_membre')
    response = client.get(url_res)
    assert response.status_code == 200
    assert "Résultat du Membre" in response.data.decode('utf-8')

    # B. Événements
    with app.test_request_context():
        url_evt = url_for('evenement_membre')
    response = client.get(url_evt)
    assert response.status_code == 200
    assert "Vos Évènements" in response.data.decode('utf-8')

    # C. Profil
    with app.test_request_context():
        url_profil = url_for('profil_view', idM=membre.id) 
    response = client.get(url_profil)
    assert response.status_code == 200
    # On vérifie l'un ou l'autre titre selon votre template
    content = response.data.decode('utf-8')
    assert "Profil de" in content or "Profil Membre" in content
    
    # D. Événements du Club
    with app.test_request_context():
        url_evt_club = url_for('evenement_club') 
    response = client.get(url_evt_club)
    assert response.status_code == 200
    assert "Evenements du Club" in response.data.decode('utf-8')

# ==============================================================================
# 3. PAGES ADMIN (Nécessitent connexion Admin)
# ==============================================================================
def test_pages_admin_protegees(client, app, db):
    """Test des pages réservées aux administrateurs."""
    app.config['WTF_CSRF_ENABLED'] = False
    
    # NETTOYAGE : Indispensable pour que le login Admin fonctionne
    # Sinon la vue /login/ redirige vers l'accueil car le client est encore connecté en Membre
    client.get('/logout/', follow_redirects=True)

    # 1. Création d'un administrateur
    mdp_clair = "AdminPass123!"
    admin = AdminBD(
        email='admin@test.fr', 
        mdp_hash=generate_password_hash(mdp_clair)
    )
    db.session.add(admin)
    db.session.commit()

    # 2. Connexion
    client.post('/login/', data={
        'email': 'admin@test.fr',
        'password': mdp_clair
    }, follow_redirects=True)

    # 3. Tests des routes protégées Admin
    
    # A. Gestion des profils
    with app.test_request_context():
        url = url_for('gerer_profils')
    response = client.get(url)
    assert response.status_code == 200
    assert "Gestion des Profils" in response.data.decode('utf-8')

    # B. Gestion des formulaires
    with app.test_request_context():
        url = url_for('gerer_formulaires')
    response = client.get(url)
    assert response.status_code == 200
    assert "Gestion des Formulaires" in response.data.decode('utf-8')

    # C. Gestion des inscriptions
    with app.test_request_context():
        url = url_for('gerer_inscriptions')
    response = client.get(url)
    assert response.status_code == 200
    assert "Gestion des Inscriptions" in response.data.decode('utf-8')
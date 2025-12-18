import pytest
from flask import url_for
from werkzeug.security import generate_password_hash
from datetime import date, datetime
from monApp.modelBD import *
from monApp.forms import ModifForm
from wtforms import DateField
from wtforms.validators import DataRequired

# ==============================================================================
# Fonction utilitaire
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

    comp = CompetitionBD(
        id_event=evt.id,
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
        passee=False
    )
    db.session.add(comp)
    db.session.commit()

    # 2. Appel de la route avec l'ID dynamique
    with app.test_request_context():
        url = url_for('competition_view', idCompetition=comp.id)
    
    response = client.get(url)

    # 3. vérification
    assert response.status_code == 200
    assert "Grande Compétition Test" in response.data.decode('utf-8')
    assert "Lyon" in response.data.decode('utf-8')

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

        # D. Evènement du club
        response = client.get(url_for('evenement_club'))
        assert response.status_code == 200
        assert "Liste des prochains évènements du cercle" in response.data.decode('utf-8')

# ==============================================================================
# 3. PAGES ADMIN
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
        assert "Gestion des Formulaires" in response.data.decode('utf-8')

        # C. Inscriptions
        response = client.get(url_for('gerer_inscriptions'))
        assert response.status_code == 200
        assert "Gestion des Inscriptions" in response.data.decode('utf-8')

        # D. Réunion
        response = client.get(url_for('reunion'))
        assert response.status_code == 200
        assert "Listes des prochaines réunions" in response.data.decode('utf-8')

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

    reunion = ReunionBD(
        idEvent=evt.id,
        nom="Réunion Mensuelle",
        typeReunionRE="Générale",
        ville="Salle de réunion",
        adresse="12 rue du pont",
        dateDebutRE=date.today(),
        heureDebutRE="10:00",
        dateFinRE=date.today(),
        heureFinRE="12:00",
        nbParticipantsRE=10,
        rapportRE="Rien à signaler"
    )
    db.session.add(reunion)
    db.session.commit()

    # 3. EXECUTION
    with app.test_request_context():
        url = url_for('reunion_view', idReunion=reunion.id)
    
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
    reunion = ReunionBD(idEvent=evt.id, nom="Secret", dateDebutRE=date.today(), 
                        heureDebutRE="10:00", dateFinRE=date.today(), heureFinRE="11:00", typeReunionRE="AG")
    db.session.add(reunion)
    db.session.commit()

    client.get('/logout/') 
    
    response = client.get(f'/reunion/consultation/{reunion.id}')
    
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

    club = EventClubBD(
        id_event=evt.id,
        NomEV="Soirée Barbecue",
        villeEV="Orléans",
        adresseEV="Club House",
        dateDebutEV=date.today(),
        heureDebutEV="19:00",
        dateFinEV=date.today(),
        heureFinEV="23:00",
        descriptionEV="Venez nombreux",
        niveauxEV="Tous",
        passeeEV=False
    )
    db.session.add(club)
    
    # 2. SETUP UTILISATEUR
    membre = MembreBD(
        email='membre@test.fr', 
        mdp_hash=generate_password_hash('pass'),
        nom='Test', prenom='User', activite=True
    )
    db.session.add(membre)
    db.session.commit()

    # 3. CONNEXION
    client.post('/login/', data={'email': 'membre@test.fr', 'password': 'pass'})

    # 4. EXECUTION
    with app.test_request_context():
        url = url_for('club_view', idEventClub=club.idEventClub)
    
    response = client.get(url)

    # 5. VERIFICATION
    assert response.status_code == 200
    assert "Soirée Barbecue" in response.data.decode('utf-8')

def test_club_view_acces_refuse_anonyme(client, app, db):
    """Vérifie qu'un visiteur non connecté est redirigé vers le login."""
    evt = EvenementBD()
    db.session.add(evt)
    db.session.commit()
    club = EventClubBD(id_event=evt.id, NomEV="Privé", dateDebutEV=date.today(), 
                       heureDebutEV="10:00", dateFinEV=date.today(), heureFinEV="12:00", 
                       descriptionEV="Test", niveauxEV="Tous", villeEV="Paris", adresseEV="Ici")
    db.session.add(club)
    db.session.commit()

    client.get('/logout/')
    response = client.get(f'/evenement_club/{club.idEventClub}/club_view/')
    
    assert response.status_code == 302
    assert "/login" in response.location

# ==============================================================================
# 4. SCENARIOS ACTIONS ADMIN
# ==============================================================================

def test_scenario_presse_admin(client, app, db):
    """Test CRUD Presse : Ajout -> Modif -> Suppression."""
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
    
    # Vérification
    article = PresseBD.query.filter_by(titreP='Victoire Régionale').first()
    assert article is not None
    assert article.contenuP == 'Le club a gagné !'

    # 3. MODIFICATION
    article = PresseBD.query.filter_by(titreP='Victoire Régionale').first()
    client.post(f'/admin/edit_presse/{article.idPresse}', data={
        'titre': 'Victoire Régionale',
        'contenu': 'Le club a perdu !',
        'lien': 'http://journal.fr'
    }, follow_redirects=True)
    article = PresseBD.query.get(article.idPresse)

    # Vérification modification
    assert article.contenuP == 'Le club a perdu !'

    # 4. SUPPRESSION
    client.post(f'/admin/delete_presse/{article.idPresse}', follow_redirects=True)
    
    # Vérification suppression
    assert PresseBD.query.filter_by(titreP='Victoire Régionale').first() is None

def test_scenario_informations_admin(client, app, db):
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

def test_scenario_article_admin(client, app, db):
    """Test CRUD Information : Ajout -> Modif -> Suppression."""
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # 1. AJOUT
    client.post('/admin/add_article/', data={
        'titre': 'JOBLIFE',
        'contenu': 'Soutenez JOBLIFE'
    }, follow_redirects=True)
    
    art = ArticleBD.query.filter_by(titre='JOBLIFE').first()
    assert art is not None
    assert art.contenu == 'Soutenez JOBLIFE'

    # 2. MODIFICATION
    client.post(f'/admin/edit_article/{art.id}', data={
        'titre': 'FUCK KC et M8',
        'contenu': 'Ne soutenez pas ces sionniste'
    }, follow_redirects=True)
    
    updated_art = db.session.get(ArticleBD, art.id)
    assert updated_art.titre == 'FUCK KC et M8'

    # 3. TEST SUPPRESSION IMAGE
    # A. On simule l'existence d'une image en l'ajoutant directement en BDD
    img = ImageArticleBD(nom="fake_image.jpg", id_article=art.id)
    db.session.add(img)
    db.session.commit()
    id_img = img.id

    assert ImageArticleBD.query.get(id_img) is not None

    # B. Appel de la route de suppression
    client.post(f'/admin/delete_image_article/{id_img}', follow_redirects=True)

    # C. Vérification que l'image n'est plus en base
    assert ImageArticleBD.query.get(id_img) is None

    # 4. SUPPRESSION
    client.post(f'/admin/delete_article/{art.id}', follow_redirects=True)
    assert db.session.get(ArticleBD, art.id) is None

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
    """
    Test complet de la gestion des inscriptions :
    1. Acceptation d'une demande -> Création Membre.
    2. Refus d'une demande -> Suppression demande sans création Membre.
    """
    app.config['WTF_CSRF_ENABLED'] = False
    setup_admin(client, db)

    # ======================================================
    # SCÉNARIO 1 : ACCEPTATION
    # ======================================================
    # 1. Créer une demande d'inscription valide
    inscr_ok = InscriptionBD(
        email='new_member@test.fr', nom='Test', prenom='User', 
        ddn=date(2000,1,1), mdp_hash='pass', sexe='Homme', date=date.today()
    )
    db.session.add(inscr_ok)
    db.session.commit()
    id_ok = inscr_ok.id

    # 2. Accepter l'inscription
    client.post(f'/accepter_inscription/{id_ok}', follow_redirects=True)
    
    # 3. Vérifications
    # La demande d'inscription doit avoir disparu
    assert db.session.get(InscriptionBD, id_ok) is None
    
    # Le membre doit avoir été créé
    membre = MembreBD.query.filter_by(email='new_member@test.fr').first()
    assert membre is not None
    
    # Les paramètres de notification doivent être initialisés
    assert membre.idParaNotif is not None
    param = ParametreNotifMembreBD.query.get(membre.idParaNotif)
    assert param.eventNouveauMail is True

    # ======================================================
    # SCÉNARIO 2 : REFUS
    # ======================================================
    # 1. Créer une deuxième demande
    inscr_refus = InscriptionBD(
        email='refused@test.fr', nom='Refus', prenom='Guy', 
        ddn=date(1999,1,1), mdp_hash='pass', sexe='Homme', date=date.today()
    )
    db.session.add(inscr_refus)
    db.session.commit()
    id_refus = inscr_refus.id

    # 2. Refuser l'inscription
    client.post(f'/refuser_inscription/{id_refus}', data={
        'justification': 'Dossier incomplet ou incohérent'
    }, follow_redirects=True)

    # 3. Vérifications
    # La demande d'inscription doit avoir disparu
    assert db.session.get(InscriptionBD, id_refus) is None
    
    # Le membre ne doit pas avoir été créé
    membre_refus = MembreBD.query.filter_by(email='refused@test.fr').first()
    assert membre_refus is None

def test_gestion_modifications(client, app, db):
    """
    Test complet du cycle de vie d'une modification de profil.
    UTILISE UN MONKEY-PATCH pour contourner la stricticité de SQLite sur les dates.
    """
    app.config['WTF_CSRF_ENABLED'] = False
    
    # SQLite refuse les Strings dans une colonne Date. MySQL l'accepte.
    # Comme on ne peut pas toucher au code source, on modifie la classe Form temporairement juste pour ce test.
    original_field = ModifForm.ddn
    ModifForm.ddn = DateField('date de naissance', format='%Y-%m-%d', validators=[DataRequired()])
    
    try:
        # Setup : Création Admin et Membre
        admin = setup_admin(client, db)
        
        membre = MembreBD(
            email='membre@modif.fr', mdp_hash=generate_password_hash('pass'),
            nom='Original', prenom='User', sexe='Homme', ddn=date(1990, 1, 1),
            activite=True
        )
        db.session.add(membre)
        db.session.commit()
        id_membre = membre.id

        # ======================================================
        # SCÉNARIO A : DEMANDE ET ACCEPTATION
        # ======================================================
        
        # 1. Le Membre se connecte et fait une demande
        client.get('/logout/')
        client.post('/login/', data={'email': 'membre@modif.fr', 'password': 'pass'})
        
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
        client.post(f'/profil_edit/{id_membre}', data=data_modif, follow_redirects=True)
        
        # Vérification
        modif = ModifBD.query.filter_by(id_membre=id_membre).first()
        assert modif is not None
        assert modif.nom == 'NouveauNom'

        # 2. L'Admin se connecte et accepte
        client.get('/logout/')
        client.post('/login/', data={'email': 'superadmin@test.fr', 'password': 'pass'})
        
        client.post(f'/accepter_modifications/{modif.id}', follow_redirects=True)
        
        # 3. Vérifications
        assert db.session.get(ModifBD, modif.id) is None
        updated_membre = db.session.get(MembreBD, id_membre)
        assert updated_membre.nom == 'NouveauNom'

        # ======================================================
        # SCÉNARIO B : DEMANDE ET REFUS
        # ======================================================
        
        # 1. Le Membre refait une demande
        client.get('/logout/')
        client.post('/login/', data={'email': 'membre@modif.fr', 'password': 'pass'})
        
        data_modif['nom'] = 'NouveauNom' 
        data_modif['prenom'] = 'RefusePrenom' 
        client.post(f'/profil_edit/{id_membre}', data=data_modif, follow_redirects=True)
        
        modif_refus = ModifBD.query.filter_by(id_membre=id_membre).first()
        assert modif_refus is not None
        id_modif_refus = modif_refus.id

        # 2. L'Admin refuse
        client.get('/logout/')
        client.post('/login/', data={'email': 'superadmin@test.fr', 'password': 'pass'})
        
        client.post(f'/refuser_modification/{id_modif_refus}', data={
            'justification': 'Pas valide'
        }, follow_redirects=True)
        
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

def test_access_control_admin_pages(client, app):
    """
    SCÉNARIO : Un utilisateur non connecté essaie d'accéder aux pages admin.
    RÉSULTAT ATTENDU : Redirection vers le login (302).
    """
    app.config['LOGIN_DISABLED'] = False
    client.get('/logout/')

    # Liste des routes Admin
    routes_admin = [
        '/gerer_profils/',
        '/gerer_formulaires/',
        '/admin/add_article/',
        '/admin/gestion_tarifs/'
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

    response = client.get('/resultat_membre/')
    assert response.status_code == 302
    assert "/login" in response.location

def test_password_change_security(client, app, db):
    """
    FAILLE TESTÉE : Mauvaise validation de l'ancien mot de passe.
    SCÉNARIO : Un membre essaie de changer son mot de passe en donnant un mauvais 'ancien mot de passe'.
    """
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['LOGIN_DISABLED'] = False
    
    user = MembreBD(email='pwd@test.fr', mdp_hash=generate_password_hash('VraiMotDePasse123!'))
    db.session.add(user)
    db.session.commit()
    
    client.post('/login/', data={'email': 'pwd@test.fr', 'password': 'VraiMotDePasse123!'})

    # Tentative de changement avec MAUVAIS ancien mdp
    response = client.post('/changer_mdp/', data={
        'old_password': 'MauvaisPassword',
        'new_password': 'NewPassword123!',
        'confirm_new_password': 'NewPassword123!'
    }, follow_redirects=True)

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
    
    response = client.post('/inscription/', data={
        'Login': 'weak@test.fr',
        'nom': 'Faible',
        'prenom': 'User',
        'date_naissance': '2000-01-01',
        'sexe': 'Homme',
        'password': '123',
        'confirm_password': '123'
    }, follow_redirects=True)

    # Doit échouer et afficher le message d'erreur
    # On cherche un mot clé du message d'erreur défini dans views.py
    assert b"mot de passe doit contenir" in response.data
    assert InscriptionBD.query.filter_by(email='weak@test.fr').first() is None
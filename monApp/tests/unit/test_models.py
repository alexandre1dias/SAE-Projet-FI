from datetime import date, datetime
from monApp.modelBD import *

# ==============================================================================
# 1. TEST MEMBRE & AUTH
# ==============================================================================

def test_new_membre(app, db):
    """Test de création d'un membre basique."""
    new_membre = MembreBD(
        nom='Desgranges',
        prenom='Lucas',
        email='lucas@gmail.com',
        mdp_hash='Lucas@0506',
        date_inscription=date(2025, 12, 16),
        sexe='Homme',
        ddn=date(2006, 5, 6),
        statut='Membre',
        activite=1
    )
    db.session.add(new_membre)
    db.session.commit()

    membre = MembreBD.query.filter_by(email='lucas@gmail.com').first()
    assert membre.nom == 'Desgranges'
    assert membre.prenom == 'Lucas'
    assert membre.ddn == date(2006, 5, 6)

def test_admin(app, db):
    """Test de la table ADMINISTRATEUR."""
    admin = AdminBD(email='admin@escrime.fr', mdp_hash='admin123')
    db.session.add(admin)
    db.session.commit()

    retrieved = AdminBD.query.first()
    assert retrieved.email == 'admin@escrime.fr'

def test_inscription_attente(app, db):
    """Test de la table INSCRIPTION (demandes en attente)."""
    inscr = InscriptionBD(
        email='nouveau@test.fr',
        nom='Dupont',
        prenom='Jean',
        ddn=date(2000, 1, 1),
        mdp_hash='pass123',
        sexe='Homme',
        date=date.today()
    )
    db.session.add(inscr)
    db.session.commit()

    assert InscriptionBD.query.count() == 1

# ==============================================================================
# 2. TEST EVENEMENTS & TYPES (Héritage / FK)
# ==============================================================================

def test_evenement_generique(app, db):
    """Test de la table mère EVENEMENT."""
    event = EvenementBD() # L'ID est généré automatiquement
    db.session.add(event)
    db.session.commit()
    assert event.id is not None

def test_competition(app, db):
    """Test COMPETITION (lié à EVENEMENT)."""
    # 1. Créer l'événement parent
    event = EvenementBD()
    db.session.add(event)
    db.session.flush() # Pour générer l'ID event sans commit

    # 2. Créer la compétition liée
    compet = CompetitionBD(
        nom='Compétition Régionale',
        ville='Orléans',
        date_debut=date(2024, 6, 1),
        date_fin=date(2024, 6, 2),
        type_arme='Fleuret',
        sexe='F',
        id_event=event.id # Lien FK
    )
    db.session.add(compet)
    db.session.commit()

    assert compet.evenement.id == event.id
    assert compet.nom == 'Compétition Régionale'

def test_reunion(app, db):
    """Test REUNION (lié à EVENEMENT)."""
    event = EvenementBD()
    db.session.add(event)
    db.session.flush()

    reunion = ReunionBD(
        nom='AG 2024',
        dateDebutRE=date(2024, 9, 1),
        dateFinRE=date(2024, 9, 1),
        idEvent=event.id
    )
    db.session.add(reunion)
    db.session.commit()
    
    assert ReunionBD.query.first().nom == 'AG 2024'

def test_entrainement(app, db):
    """Test ENTRAINEMENT (lié à EVENEMENT)."""
    event = EvenementBD()
    db.session.add(event)
    db.session.flush()

    entrainement = EntrainementBD(
        jour='Lundi',
        date=date(2024, 1, 1),
        id_event=event.id
    )
    db.session.add(entrainement)
    db.session.commit()
    
    assert EntrainementBD.query.first().jour == 'Lundi'

def test_event_club(app, db):
    """Test EVENTCLUB (lié à EVENEMENT)."""
    event = EvenementBD()
    db.session.add(event)
    db.session.flush()

    evt_club = EventClubBD(
        NomEV='Barbecue Fin Année',
        dateDebutEV=date(2024, 7, 1),
        dateFinEV=date(2024, 7, 1),
        id_event=event.id
    )
    db.session.add(evt_club)
    db.session.commit()
    
    assert EventClubBD.query.first().NomEV == 'Barbecue Fin Année'

# ==============================================================================
# 3. TEST RELATIONS (Participer, Résultats)
# ==============================================================================

def test_participer(app, db):
    """Test de la table d'association PARTICIPER (Membre <-> Event)."""
    # Création des parents
    m = MembreBD(email='p@test.fr', nom='P', prenom='P', date_inscription=date.today())
    e = EvenementBD()
    db.session.add_all([m, e])
    db.session.flush()

    # Création de l'association
    participation = ParticiperBD(id_event=e.id, id_membre=m.id)
    db.session.add(participation)
    db.session.commit()

    # Vérification via la relation SQLAlchemy
    assert m.evenements_inscrits.count() == 1
    assert m.evenements_inscrits[0].id_event == e.id

def test_resultat(app, db):
    """Test RESULTAT (Membre <-> Competition)."""
    # Setup
    m = MembreBD(email='r@test.fr', date_inscription=date.today())
    evt = EvenementBD()
    db.session.add_all([m, evt])
    db.session.flush()
    
    comp = CompetitionBD(id_event=evt.id, nom='Open France')
    db.session.add(comp)
    db.session.flush()

    # Résultat
    res = ResultatBD(
        resultat='1er',
        date=date(2024, 5, 5),
        id_competition=comp.id,
        id_membre=m.id
    )
    db.session.add(res)
    db.session.commit()

    assert ResultatBD.query.first().resultat == '1er'

# ==============================================================================
# 4. TEST FORMULAIRES & INTERACTION
# ==============================================================================

def test_formulaire_et_reponse(app, db):
    """Test FORMULAIRE_CONTACT, REPONDRE et REMPLIR."""
    # Acteurs
    membre = MembreBD(email='user@f.fr', date_inscription=date.today())
    admin = AdminBD(email='admin@f.fr')
    db.session.add_all([membre, admin])
    db.session.flush()

    # Formulaire
    form = FormulaireBD(
        sujet='Question',
        email='user@f.fr',
        date=date.today(),
        idMembre=membre.id
    )
    db.session.add(form)
    db.session.flush()

    # Association Remplir (Membre -> Form)
    remplir = RemplirBD(id_formulaire=form.id, id_membre=membre.id)
    # Association Repondre (Admin -> Form)
    repondre = RepondreBD(id_formulaire=form.id, id_admin=admin.id)
    
    db.session.add_all([remplir, repondre])
    db.session.commit()

    assert len(form.remplissages) == 1
    assert len(form.reponses) == 1

def test_modif_membre(app, db):
    """Test table MODIFICATION (demande de modif profil)."""
    m = MembreBD(email='modif@test.fr', date_inscription=date.today())
    db.session.add(m)
    db.session.flush()

    modif = ModifBD(
        id_membre=m.id,
        email='new@test.fr',
        nom='NouveauNom',
        date=date.today()
    )
    db.session.add(modif)
    db.session.commit()
    
    assert m.modifications.first().nom == 'NouveauNom'

# ==============================================================================
# 5. TEST PARAMETRES NOTIFICATIONS
# ==============================================================================

def test_param_notif_membre(app, db):
    """Test PARAMETRE_NOTIF_MEMBRE."""
    m = MembreBD(email='notif@test.fr', date_inscription=date.today())
    db.session.add(m)
    db.session.flush()

    # Attention à la contrainte circulaire expliquée précédemment
    # Ici on crée juste le paramètre lié au membre
    param = ParametreNotifMembreBD(
        idMembre=m.id,
        eventNouveauMail=True,
        eventNouveauSite=False
    )
    db.session.add(param)
    db.session.commit()
    
    assert ParametreNotifMembreBD.query.filter_by(idMembre=m.id).first().eventNouveauMail is True

def test_param_notif_admin(app, db):
    """Test PARAMETRE_NOTIF_ADMIN."""
    a = AdminBD(email='admin@notif.fr')
    db.session.add(a)
    db.session.flush()

    param = ParametreNotifAdminBD(
        idAdmin=a.id,
        formulaireDemandeMail=True
    )
    db.session.add(param)
    db.session.commit()

    assert a.parametres_notif_admin.formulaireDemandeMail is True

# ==============================================================================
# 6. TEST CMS (Articles, Tarifs, Horaires, Info, Presse, Images)
# ==============================================================================

def test_article_et_images(app, db):
    """Test ARTICLE et IMAGE_ARTICLE."""
    art = ArticleBD(
        titre='Championnat',
        contenu='Super contenu',
        date=date.today()
    )
    db.session.add(art)
    db.session.flush()

    img = ImageArticleBD(
        nom='photo.jpg',
        id_article=art.id
    )
    db.session.add(img)
    db.session.commit()

    assert len(art.images) == 1
    assert art.images[0].nom == 'photo.jpg'

def test_contenu_statique(app, db):
    """Test groupé pour HORAIRE, TARIF, INFORMATION, PRESSE."""
    h = HoraireBD(jour='Lundi', heure_debut='18h')
    t = TarifBD(nom='Adulte', prix=200)
    i = InformationBD(titreIN='Info Club', dateIN=date.today())
    p = PresseBD(titreP='Journal Local', dateP=date.today())

    db.session.add_all([h, t, i, p])
    db.session.commit()

    assert HoraireBD.query.count() == 1
    assert TarifBD.query.count() == 1
    assert InformationBD.query.count() == 1
    assert PresseBD.query.count() == 1

def test_image_app(app, db):
    """Test IMAGEAPP (Gallerie)."""
    img = ImageAppBD(urlI='/static/img/logo.png', alt='Logo')
    db.session.add(img)
    db.session.commit()
    
    assert ImageAppBD.query.filter_by(alt='Logo').first() is not None

# ==============================================================================
# 7. TEST NOTIFICATION
# ==============================================================================

def test_notification(app, db):
    """Test NOTIFICATION."""
    # Création d'un timestamp propre avec datetime
    ts = datetime(2025, 11, 20, 10, 0, 0)
    
    notif = NotifsBD(
        typeN='modification',
        sourceN='Test Source',
        lue=False,
        timestamp=ts,
        link='http://test.com/modif/1'
    )
    db.session.add(notif)
    db.session.commit()

    saved_notif = NotifsBD.query.first()
    assert saved_notif is not None
    assert saved_notif.typeN == 'modification'
    assert saved_notif.lue is False
    assert saved_notif.timestamp == ts

# ==============================================================================
# 8. TEST RELATIONS MANY-TO-MANY (IMAGES)
# ==============================================================================

def test_relation_image_competition(app, db):
    """Test Many-to-Many entre COMPETITION et IMAGEAPP."""
    evt = EvenementBD()
    db.session.add(evt)
    db.session.flush()

    comp = CompetitionBD(id_event=evt.id, nom="Compétition Photo")
    img_comp = ImageAppBD(urlI="test_comp.jpg", alt="Test")
    
    # Ajout via la relation
    comp.images_rc.append(img_comp)
    db.session.add(comp)
    db.session.add(img_comp)
    db.session.commit()

    assert len(comp.images_rc) == 1
    assert comp.images_rc[0].urlI == "test_comp.jpg"

def test_relation_image_event_club(app, db):
    """Test Many-to-Many entre EVENTCLUB et IMAGEAPP."""
    evt = EvenementBD()
    db.session.add(evt)
    db.session.flush()

    club = EventClubBD(id_event=evt.id, NomEV="Club Photo")
    img_club = ImageAppBD(urlI="test_club.jpg", alt="TestClub")
    
    # Ajout via la relation
    club.images_re.append(img_club)
    db.session.add(club)
    db.session.add(img_club)
    db.session.commit()

    assert len(club.images_re) == 1
    assert club.images_re[0].urlI == "test_club.jpg"

# ==============================================================================
# 9. TEST TABLES ASSOCIATION & NOTIFICATIONS AVANCÉES
# ==============================================================================

def test_tables_liaison_notification(app, db):
    """
    Test technique pour valider l'existence des tables 'recevoir_a' et 'recevoir_m'.
    Ces tables n'ont pas de relation directe mappée dans NotifsBD, on teste donc 
    l'insertion brute pour garantir la couverture du code SQLAlchmey.
    """
    notif = NotifsBD(typeN="Test Liaison", timestamp=datetime.now(), lue=False)
    admin = AdminBD(email="admin_liaison@test.fr", mdp_hash="pass")
    membre = MembreBD(email="membre_liaison@test.fr", mdp_hash="pass")
    
    db.session.add_all([notif, admin, membre])
    db.session.commit()

    # Insertion directe dans les tables de liaison définies dans modelBD.py
    ins_a = recevoir_a.insert().values(idNotifs=notif.idNotifs, idAdmin=admin.id)
    ins_m = recevoir_m.insert().values(idNotifs=notif.idNotifs, idMembre=membre.id)
    
    db.session.execute(ins_a)
    db.session.execute(ins_m)
    db.session.commit()

    # Si aucune erreur n'est levée, les tables existent et sont fonctionnelles.
    assert True

def test_notification_fk_users(app, db):
    """Test des clés étrangères idAdmin et idMembre dans NOTIFS."""
    admin = AdminBD(email="admin_fk@test.fr", mdp_hash="pass")
    membre = MembreBD(email="membre_fk@test.fr", mdp_hash="pass")
    db.session.add_all([admin, membre])
    db.session.flush()

    notif_complete = NotifsBD(
        typeN="Info FK", 
        timestamp=datetime.now(),
        lue=True, 
        idAdmin=admin.id,
        idMembre=membre.id
    )
    db.session.add(notif_complete)
    db.session.commit()
    
    assert notif_complete.idAdmin == admin.id
    assert notif_complete.idMembre == membre.id
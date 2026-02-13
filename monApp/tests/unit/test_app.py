from flask import session
from flask_login import login_user
from monApp.models import AdminBD, MembreBD
from monApp.app import load_user

def test_load_user_fallback(client, app, db):
    """
    Teste la fonction load_user quand 'user_type' n'est PAS dans la session.
    """
    # 1. Création d'un Admin (ID 1)
    admin = AdminBD(email='admin_load@test.fr', mdp_hash='pass')
    db.session.add(admin)
    db.session.commit()
    
    # 2. Création d'un membre "tampon" (ID 1)
    # Cet utilisateur aura le même ID que l'admin, on ne l'utilise pas pour le test
    membre_tampon = MembreBD(email='tampon@test.fr', mdp_hash='pass')
    db.session.add(membre_tampon)
    db.session.commit()

    # 3. Création du membre CIBLE (ID 2)
    # Comme il n'y a pas d'Admin avec l'ID 2, le fallback fonctionnera correctement
    membre = MembreBD(email='membre_load@test.fr', mdp_hash='pass')
    db.session.add(membre)
    db.session.commit()
    
    id_admin = admin.id
    id_membre = membre.id

    with app.test_request_context():
        # CAS 1 : Fallback Admin (ID 1)
        # Admin(1) existe (et Membre(1) aussi). La fonction priorise Admin.
        if 'user_type' in session:
            session.pop('user_type')
        
        loaded_admin = load_user(id_admin)
        assert loaded_admin is not None
        assert loaded_admin.email == 'admin_load@test.fr'
        assert isinstance(loaded_admin, AdminBD)

        # CAS 2 : Fallback Membre (ID 2)
        # Admin(2) n'existe PAS. Membre(2) existe. La fonction trouve le Membre.
        loaded_membre = load_user(id_membre)
        assert loaded_membre is not None
        assert loaded_membre.email == 'membre_load@test.fr'
        assert isinstance(loaded_membre, MembreBD)

        # CAS 3 : ID Inconnu
        assert load_user(9999) is None
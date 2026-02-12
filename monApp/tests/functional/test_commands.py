import pytest
from werkzeug.security import check_password_hash
from monApp.models import AdminBD
from monApp.commands import change_admin_password

# ==============================================================================
# TESTS DES COMMANDES CLI
# ==============================================================================


def test_change_admin_password_success(app, db):
    """
    Test du succès de la commande CLI pour modifier le mot de passe d'un admin.
    Vérifie l'affichage console et la mise à jour effective du hash en BDD.
    """
    # 1. SETUP
    admin = AdminBD(email='admin_cli@test.fr', mdp_hash='vieux_hash_invalide')
    db.session.add(admin)
    db.session.commit()

    # 2. Initialisation du runner CLI de Flask
    runner = app.test_cli_runner()

    # 3. EXECUTION
    result = runner.invoke(change_admin_password,
                           ['admin_cli@test.fr', 'NouveauSuperMdp123!'])

    # 4. VERIFICATIONS CLI
    assert result.exit_code == 0
    assert "Succès : Le mot de passe pour l'admin 'admin_cli@test.fr' a été mis à jour." in result.output

    # 5. VERIFICATIONS BDD
    updated_admin = db.session.get(AdminBD, admin.id)
    assert updated_admin.mdp_hash != 'vieux_hash_invalide'
    assert check_password_hash(updated_admin.mdp_hash,
                               'NouveauSuperMdp123!') is True


def test_change_admin_password_failure(app, db):
    """
    Test de l'échec de la commande CLI quand l'email n'existe pas.
    Vérifie que l'erreur s'affiche correctement sans crasher l'application.
    """
    # 1. NETTOYAGE
    db.session.query(AdminBD).delete()
    db.session.commit()

    # 2. Initialisation du runner CLI
    runner = app.test_cli_runner()

    # 3. EXECUTION : Email fantôme
    result = runner.invoke(change_admin_password,
                           ['inconnu@test.fr', 'NouveauSuperMdp123!'])

    # 4. VERIFICATIONS
    assert result.exit_code == 0
    assert "Erreur : Aucun administrateur trouvé avec l'email 'inconnu@test.fr'." in result.output

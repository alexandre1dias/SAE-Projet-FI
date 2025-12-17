import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from monApp.app import app as flask_app
from monApp.app import db as _db
from monApp.modelBD import *


# ===============================================================
# 1. Configuration Application
# ===============================================================
@pytest.fixture(scope='session')
def app():
    """
    Configure l'application Flask pour le mode TEST.
    """
    flask_app.config.update({
        "TESTING":
        True,
        "WTF_CSRF_ENABLED":
        False,
        "SQLALCHEMY_DATABASE_URI":
        "sqlite:///:memory:",
        "SECRET_KEY":
        "cle_secrete_temporaire_pour_les_tests"
    })

    with flask_app.app_context():
        yield flask_app


# ===============================================================
# 2. Configuration Base de Données (Remplacement de Session)
# ===============================================================
@pytest.fixture(scope='function')
def db(app):
    """
    Crée une base SQLite isolée et REMPLACE la session globale de l'app.
    """
    # A. Création du moteur SQLite manuel
    engine = create_engine('sqlite:///:memory:')
    connection = engine.connect()

    # B. Création des tables sur ce moteur SQLite
    # Le @compiles plus haut empêche le crash sur LONGTEXT
    _db.metadata.create_all(bind=engine)

    # C. "HACK" : On crée une nouvelle factory de session liée à SQLite
    # et on remplace celle de l'application par celle-ci.
    session_factory = sessionmaker(bind=connection)
    new_db_session = scoped_session(session_factory)

    # On sauvegarde l'ancienne session (MySQL) pour la remettre après
    old_session = _db.session
    _db.session = new_db_session

    yield _db

    # E. Nettoyage et remise en état
    _db.session.remove()
    _db.metadata.drop_all(bind=engine)
    connection.close()
    engine.dispose()

    # On remet la session originale pour ne pas casser d'autres tests potentiels
    _db.session = old_session


@pytest.fixture(scope='function')
def client(app, db):
    return app.test_client()
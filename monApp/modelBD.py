
from .app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class MembreBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table MEMBRE, compatible Flask-Login.
    """
    __tablename__ = 'MEMBRE'
    
    # Mappage des colonnes SQL
    id = db.Column('idMembre', db.Integer, primary_key=True)
    nom = db.Column('nomM', db.String(41))
    prenom = db.Column('prenomM', db.String(41))
    email = db.Column('emailM', db.String(41), unique=True, nullable=False)
    mdp_hash = db.Column('mdpM', db.String(128), nullable=False) # Idem, varchar(16) est trop court
    date_inscription = db.Column(db.Date)
    sexe = db.Column('sexeM', db.String(5))
    ddn = db.Column('ddnM', db.Date)
    niveau = db.Column(db.String(15))
    statut = db.Column(db.String(15))
    activite = db.Column(db.Boolean)

class ReunionBD(UserMixin, db.Model):
    __tablename__ = 'REUNION'

    id = db.Column('idReunion', db.Integer, primary_key=True)
    nom= db.Column('nomRE' , db.String(41))
    lieu = db.Column('lieuRE', db.String(20))
    dateRE = db.Column(db.Date)
    heureDebutRE = db.Column('heureDebutRE', db.String(5))
    nbParticipantsRE = db.Column('nbParticipantsRE', db.Integer)
    typeReunionRE = db.Column('typeReunionRE', db.String(15))
    rapportRE = db.Column('rapportRE', db.String(200))
    niveauRE = db.Column('niveauRE', db.String(15)) 
    idEvent = db.Column('idEvent', db.Integer) 
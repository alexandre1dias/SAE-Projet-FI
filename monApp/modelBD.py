
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



class EvenementnBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table EVENEMENT, compatible Flask-Login.
    """
    __tablename__ = 'EVENEMENT'
    
    # Mappage de la colonne SQL
    id = db.Column('idEvent', db.Integer, primary_key=True)




class CompetitionBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table COMPETITION, compatible Flask-Login.
    """
    __tablename__ = 'COMPETITION'
    
    # Mappage des colonnes SQL
    id = db.Column('idCompetition', db.Integer, primary_key=True)
    nom = db.Column('nomCo', db.String(50))
    ville = db.Column('villeCo', db.String(50))
    adresse = db.Column('adresseCo', db.String(50))
    date_debut = db.Column('dateDebutCo', db.Date)
    heure_debut = db.Column('heureDebutCo', db.String(5))
    date_fin = db.Column('dateFinCo', db.Date)
    heure_fin = db.Column('heureFinCo', db.String(5))
    type_arme = db.Column('typeArmeCo', db.String(12))
    nb_participants = db.Column('nbParticipantsCo', db.Integer)
    sexe = db.Column('sexeCo', db.String(5))
    typeComp = db.Column('typeCompete', db.String(15))
    description = db.Column('descriptionCo', db.String(255))
    niveaux = db.Column('niveauCo', db.String(15))
    classement = db.Column('classementCo', db.String(20))
    passee = db.Column('passeeCO', db.Boolean)
    #Clé étrangère
    id_event = db.Column('idEvent', db.Integer, db.ForeignKey('EVENEMENT.idEvent'))
    evenement = db.relationship('EvenementnBD', backref=db.backref('competitions', lazy=True))



    
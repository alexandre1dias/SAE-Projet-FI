
from .app import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class MembreBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table MEMBRE, compatible Flask-Login.
    """
    __tablename__ = 'MEMBRE'
    
    # Mappage des colonnes SQL
    id = db.Column('idMembre', db.Integer, primary_key=True)
    nom = db.Column('nomM', db.String(41))
    prenom = db.Column('prenomM', db.String(41))
    email = db.Column('emailM', db.String(100), unique=True, nullable=False)
    mdp_hash = db.Column('mdpM', db.String(128))
    date_inscription = db.Column(db.Date)
    sexe = db.Column('sexeM', db.String(5))
    ddn = db.Column('ddnM', db.Date)
    age = db.Column(db.Integer)
    niveau = db.Column(db.String(15))
    statut = db.Column(db.String(30))
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


class EvenementBD(UserMixin, db.Model):
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
    evenement = db.relationship('EvenementBD', backref=db.backref('competitions', lazy=True))

    
class AdminBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table ADMINISTRATEUR, compatible Flask-Login.
    """
    __tablename__ = 'ADMINISTRATEUR'
    
    # Mappage des colonnes SQL
    id = db.Column('idAdmin', db.Integer, primary_key=True)
    email = db.Column('emailA', db.String(41), unique=True, nullable=False)
    mdp_hash = db.Column('mdpA', db.String(64))


class InscriptionBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table INSCRIPTION, compatible Flask-Login.
    """
    __tablename__ = 'INSCRIPTION'
    
    # Mappage des colonnes SQL
    id = db.Column('idInscription', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column('mailInscr', db.String(41), unique=True, nullable=False)
    nom = db.Column('nomI', db.String(41))
    prenom = db.Column('prenomI', db.String(41))
    ddn = db.Column('ddnI', db.Date)
    mdp_hash = db.Column('mdpI', db.String(128), nullable=False)
    sexe = db.Column('sexeI', db.String(5))
    date = db.Column('dateInscription', db.Date)


class ModifBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table MODIFICATION, compatible Flask-Login.
    """
    __tablename__ = 'MODIFICATION'
    
    id = db.Column('idModif', db.Integer, primary_key=True)
    id_membre = db.Column('idMembre', db.Integer, db.ForeignKey('MEMBRE.idMembre'), nullable=False)
    nom = db.Column('nomModif', db.String(41))
    prenom = db.Column('prenomModif', db.String(41))
    email = db.Column('emailModif', db.String(100), unique=True, nullable=False)
    sexe = db.Column('sexeModif', db.String(5))
    ddn = db.Column('ddnModif', db.Date)
    date = db.Column('dateModif', db.Date)
    membre = db.relationship('MembreBD', backref=db.backref('modifications', lazy='dynamic'))


class ParticiperBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table PARTICIPER, compatible Flask-Login.
    Lie un Membre à un Evenement.
    """
    __tablename__ = 'PARTICIPER'

    id_event = db.Column('idEvent', db.Integer, db.ForeignKey('EVENEMENT.idEvent'), primary_key=True)
    id_membre = db.Column('idMembre', db.Integer, db.ForeignKey('MEMBRE.idMembre'), primary_key=True)

    membre = db.relationship('MembreBD', backref=db.backref('evenements_inscrits', lazy='dynamic'))
    evenement = db.relationship('EvenementBD', backref=db.backref('participants', lazy='dynamic'))

class RepondreBD(db.Model):
    """
    Table d'association entre un administrateur et un formulaire auquel il a répondu.
    """
    __tablename__ = 'REPONDRE'
    id_formulaire = db.Column('idFormulaire', db.Integer, db.ForeignKey('FORMULAIRE_CONTACT.idFormulaire'), primary_key=True)
    id_admin = db.Column('idAdmin', db.Integer, db.ForeignKey('ADMINISTRATEUR.idAdmin'), primary_key=True)

class RemplirBD(db.Model):
    """
    Table d'association entre un membre et un formulaire qu'il a rempli.
    """
    __tablename__ = 'REMPLIR'
    id_formulaire = db.Column('idFormulaire', db.Integer, db.ForeignKey('FORMULAIRE_CONTACT.idFormulaire'), primary_key=True)
    id_membre = db.Column('idMembre', db.Integer, db.ForeignKey('MEMBRE.idMembre'), primary_key=True)

class FormulaireBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table FORMULAIRE_CONTACT.
    Combine les champs pour l'admin et pour la soumission.
    """
    __tablename__ = 'FORMULAIRE_CONTACT'

    id = db.Column('idFormulaire', db.Integer, primary_key=True)
    
    type_form = db.Column('typeFC', db.String(20))
    sujet = db.Column('sujetFC', db.String(100))
    email = db.Column('mailFC', db.String(41))
    description = db.Column('descriptionFC', db.String(500))
    date = db.Column('dateFC', db.Date)
    
    idMembre = db.Column(db.Integer, db.ForeignKey('MEMBRE.idMembre'))
    idAdmin = db.Column(db.Integer, db.ForeignKey('ADMINISTRATEUR.idAdmin'))

    membre = db.relationship('MembreBD', backref=db.backref('formulaires', lazy=True))
    admin = db.relationship('AdminBD', backref=db.backref('formulaires', lazy=True))

    reponses = db.relationship('RepondreBD', backref='formulaire', cascade="all, delete-orphan")
    remplissages = db.relationship('RemplirBD', backref='formulaire', cascade="all, delete-orphan")

class EventClubBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table COMPETITION, compatible Flask-Login.
    """
    __tablename__ = 'EVENTCLUB'
    
    # Mappage des colonnes SQL
    idEventClub = db.Column(db.Integer, primary_key=True)
    NomEV = db.Column(db.String(50))
    villeEV = db.Column(db.String(50))
    adresseEV = db.Column(db.String(50))
    dateDebutEV = db.Column(db.Date)
    heureDebutEV = db.Column(db.String(5))
    dateFinEV = db.Column(db.Date)
    heureFinEV = db.Column(db.String(5))
    nbParticipantEV = db.Column(db.Integer)
    descriptionEV = db.Column(db.String(255))
    niveauxEV = db.Column(db.String(45))
    passeeEV = db.Column(db.Boolean)
    #Clé étrangère
    id_event = db.Column('idEvent', db.Integer, db.ForeignKey('EVENEMENT.idEvent'))
    evenement = db.relationship('EvenementBD', backref=db.backref('eventclub', lazy=True))


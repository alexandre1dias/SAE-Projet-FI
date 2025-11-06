
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
    nom = db.Column('nomRE' , db.String(41))
    ville = db.Column('villeRE', db.String(50))
    adresse = db.Column('adresseRE', db.String(50))
    dateDebutRE = db.Column(db.Date)
    heureDebutRE = db.Column(db.String(5))
    dateFinRE = db.Column(db.Date)
    heureFinRE = db.Column(db.String(5))
    nbParticipantsRE = db.Column(db.Integer)
    typeReunionRE = db.Column(db.String(15))
    rapportRE = db.Column(db.String(200))
    niveauRE = db.Column(db.String(15)) 
    idEvent = db.Column(db.Integer, db.ForeignKey('EVENEMENT.idEvent'))
    evenement = db.relationship('EvenementBD', backref=db.backref('reunions', lazy=True))


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
    id_event = db.Column('idEvent', db.Integer, db.ForeignKey('EVENEMENT.idEvent'))
    evenement = db.relationship('EvenementBD', backref=db.backref('competitions', lazy=True))
    resultats = db.relationship('ResultatBD', backref='competition', lazy=True, cascade='all, delete-orphan')

class EntrainementBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table ENTRAINEMENT.
    """
    __tablename__ = 'ENTRAINEMENT'

    id = db.Column('idEntrainement', db.Integer, primary_key=True)
    jour = db.Column('jourEN', db.String(8))
    ville = db.Column('villeEN', db.String(50))
    adresse = db.Column('adresseEN', db.String(50))
    date = db.Column('dateEN', db.Date)
    heure_debut = db.Column('heureDebutEN', db.String(5))
    heure_fin = db.Column('heureFinEN', db.String(5))
    type_arme = db.Column('typeArmeEN', db.String(12))
    niveau = db.Column('niveauEN', db.String(15))
    id_event = db.Column('idEvent', db.Integer, db.ForeignKey('EVENEMENT.idEvent'))
    evenement = db.relationship('EvenementBD', backref=db.backref('entrainements', lazy=True))


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
    
    type = db.Column('typeFC', db.String(20))
    sujet = db.Column('sujetFC', db.String(100))
    email = db.Column('mailFC', db.String(41))
    description = db.Column('descriptionFC', db.String(500))
    date = db.Column('dateFC', db.Date)
    reponse = db.Column(db.String(300))
    repondu = db.Column(db.Boolean)

    
    idMembre = db.Column(db.Integer, db.ForeignKey('MEMBRE.idMembre'))
    idAdmin = db.Column(db.Integer, db.ForeignKey('ADMINISTRATEUR.idAdmin'))

    membre = db.relationship('MembreBD', backref=db.backref('formulaires', lazy=True))
    admin = db.relationship('AdminBD', backref=db.backref('formulaires', lazy=True))

    reponses = db.relationship('RepondreBD', backref='formulaire', cascade="all, delete-orphan")
    remplissages = db.relationship('RemplirBD', backref='formulaire', cascade="all, delete-orphan")

class EventClubBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table EventClub, compatible Flask-Login.
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

class ResultatBD(db.Model):
    """
    Modèle SQLAlchemy pour la table RESULTAT.
    """
    __tablename__ = 'RESULTAT'

    id = db.Column('idResultat', db.Integer, primary_key=True)
    resultat = db.Column(db.String(50))
    date = db.Column('dateRE', db.Date)
    type_arme = db.Column('typeArmeRE', db.String(12))
    type_compete = db.Column('typeCompeteRE', db.String(15))
    id_competition = db.Column('idCompetition', db.Integer, db.ForeignKey('COMPETITION.idCompetition'))
    id_membre = db.Column('idMembre', db.Integer, db.ForeignKey('MEMBRE.idMembre'))

    membre = db.relationship('MembreBD', backref='resultats')

class InformationBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table INFORMATION, compatible Flask-Login.
    """
    __tablename__ = 'INFORMATION'
    
    # Mappage des colonnes SQL
    idInformation = db.Column(db.Integer, primary_key=True)
    dateIN = db.Column(db.Date)
    heureIN = db.Column(db.String(5))
    titreIN = db.Column(db.String(50))
    contenuIN = db.Column(db.String(600))

class PresseBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table PRESSE, compatible Flask-Login.
    """
    __tablename__ = 'PRESSE'
    
    # Mappage des colonnes SQL
    idPresse = db.Column(db.Integer, primary_key=True)
    dateP = db.Column(db.Date)
    heureP = db.Column(db.String(5))
    titreP = db.Column(db.String(50))
    contenuP = db.Column(db.String(600))
    lienP = db.Column(db.String(255))


class ParametreNotifAdminBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table PARAMETRE_NOTIF_ADMIN, compatible Flask-Login.
    """
    __tablename__ = 'PARAMETRE_NOTIF_ADMIN'
    
    # Mappage des colonnes SQL  
    idParamNotifAdmin = db.Column(db.Integer, primary_key=True)
    formulaireDemandeSite = db.Column(db.Boolean)
    formulaireDemandeMail = db.Column(db.Boolean)
    formulaireQuestionSite = db.Column(db.Boolean)
    formulaireQuestionMail = db.Column(db.Boolean)
    formulaireSignalementSite = db.Column(db.Boolean)
    formulaireSignalementMail = db.Column(db.Boolean)
    demandeModifSite = db.Column(db.Boolean)
    demandeModifMail = db.Column(db.Boolean)
    demandeInscriptionSite = db.Column(db.Boolean)
    demandeInscriptionMail = db.Column(db.Boolean)
    idAdmin = db.Column(db.Integer, db.ForeignKey('ADMINISTRATEUR.idAdmin'))
    admin = db.relationship('AdminBD', backref=db.backref('parametres_notif_admin', uselist=False))



class ParametreNotifMembreBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table PARAMETRE_NOTIF_MEMBRE, compatible Flask-Login.
    """
    __tablename__ = 'PARAMETRE_NOTIF_MEMBRE'
    
    # Mappage des colonnes SQL
    idParamNotifMembre = db.Column(db.Integer, primary_key=True)
    eventInscriptionSite = db.Column(db.Boolean)
    evenementInscriptionMail = db.Column(db.Boolean)
    eventNouveauSite = db.Column(db.Boolean)
    eventNouveauMail = db.Column(db.Boolean)
    eventAnnulationSite = db.Column(db.Boolean)
    eventAnnulationMail = db.Column(db.Boolean)
    resultatNouveauSite = db.Column(db.Boolean)
    resultatNouveauMail = db.Column(db.Boolean)
    reponseFormulaireSite = db.Column(db.Boolean)
    reponseFormulaireMail = db.Column(db.Boolean)
    modifProfilSite = db.Column(db.Boolean)
    modifProfilMail = db.Column(db.Boolean)
    idMembre = db.Column(db.Integer, db.ForeignKey('MEMBRE.idMembre'))
    membre = db.relationship('MembreBD', backref=db.backref('parametres_notif_membre', uselist=False))
from .app import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

image_competition_association = db.Table(
    'IMAGERC',
    db.Column('idImage',
              db.Integer,
              db.ForeignKey('IMAGEAPP.idImage'),
              primary_key=True),
    db.Column('idCompetition',
              db.Integer,
              db.ForeignKey('COMPETITION.idCompetition'),
              primary_key=True))

image_evenement_club_association = db.Table(
    'IMAGERE',
    db.Column('idImage',
              db.Integer,
              db.ForeignKey('IMAGEAPP.idImage'),
              primary_key=True),
    db.Column('idEventClub',
              db.Integer,
              db.ForeignKey('EVENTCLUB.idEventClub'),
              primary_key=True))

recevoir_a = db.Table(
    'RECEVOIRA',
    db.Column('idNotifs',
              db.Integer,
              db.ForeignKey('NOTIFS.idNotifs'),
              primary_key=True),
    db.Column('idAdmin',
              db.Integer,
              db.ForeignKey('ADMINISTRATEUR.idAdmin'),
              primary_key=True))

recevoir_m = db.Table(
    'RECEVOIRM',
    db.Column('idNotifs',
              db.Integer,
              db.ForeignKey('NOTIFS.idNotifs'),
              primary_key=True),
    db.Column('idMembre',
              db.Integer,
              db.ForeignKey('MEMBRE.idMembre'),
              primary_key=True))


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
    #On est obliger de définire les valeurs de date_inscription, statut et activite malgre les Default dans la table Membre car l'ORM ecrase toute les valeurs de la table
    date_inscription = db.Column(db.Date, server_default=func.current_date())
    sexe = db.Column('sexeM', db.String(5))
    ddn = db.Column('ddnM', db.Date)
    age = db.Column(db.Integer)
    niveau = db.Column(db.String(15))
    statut = db.Column(db.String(30), server_default='Membre')
    activite = db.Column(db.Boolean, server_default='1')
    numTel = db.Column(db.String(20))
    numLicense = db.Column(db.String(67))
    eventInscriptionSite = db.Column(db.Boolean, default=True, nullable=False)
    evenementInscriptionMail = db.Column(db.Boolean,
                                         default=True,
                                         nullable=False)
    eventNouveauSite = db.Column(db.Boolean, default=True, nullable=False)
    eventNouveauMail = db.Column(db.Boolean, default=True, nullable=False)
    eventAnnulationSite = db.Column(db.Boolean, default=True, nullable=False)
    eventAnnulationMail = db.Column(db.Boolean, default=True, nullable=False)
    resultatNouveauSite = db.Column(db.Boolean, default=True, nullable=False)
    resultatNouveauMail = db.Column(db.Boolean, default=True, nullable=False)
    reponseFormulaireSite = db.Column(db.Boolean, default=True, nullable=False)
    reponseFormulaireMail = db.Column(db.Boolean, default=True, nullable=False)
    modifProfilSite = db.Column(db.Boolean, default=True, nullable=False)
    modifProfilMail = db.Column(db.Boolean, default=True, nullable=False)


#====================   Tables de Evenements   ====================#
class EvenementBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table EVENEMENT.
    """
    __tablename__ = 'EVENEMENT'

    id = db.Column('idEvent', db.Integer, primary_key=True)
    # Lien vers ReunionBD
    reunions = db.relationship('ReunionBD',
                               back_populates='evenement',
                               cascade='all, delete-orphan',
                               lazy=True)
    competitions = db.relationship('CompetitionBD',
                                   back_populates='evenement',
                                   cascade='all, delete-orphan',
                                   lazy=True)
    event_clubs = db.relationship('EventClubBD',
                                  back_populates='evenement',
                                  cascade='all, delete-orphan',
                                  lazy=True)

    def __repr__(self):
        return f"<Evenement {self.id}>"


class ReunionBD(UserMixin, db.Model):
    __tablename__ = 'REUNION'

    id = db.Column('idReunion', db.Integer, primary_key=True)
    nom = db.Column('nomRE', db.String(41))
    ville = db.Column('villeRE', db.String(50))
    adresse = db.Column('adresseRE', db.String(50))
    dateDebutRE = db.Column(db.Date)
    heureDebutRE = db.Column(db.String(5))
    dateFinRE = db.Column(db.Date)
    heureFinRE = db.Column(db.String(5))
    nbParticipantsRE = db.Column(db.Integer)
    typeReunionRE = db.Column(db.String(15))
    rapportRE = db.Column(db.String(200))
    idEvent = db.Column(db.Integer, db.ForeignKey('EVENEMENT.idEvent'))
    evenement = db.relationship('EvenementBD', back_populates='reunions')


class CompetitionBD(UserMixin, db.Model):
    __tablename__ = 'COMPETITION'

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
    description = db.Column('descriptionCo', db.String(200))
    niveaux = db.Column('niveauCo', db.String(45))
    classement = db.Column('classementCo', db.String(20))
    passee = db.Column('passeeCO', db.Boolean)
    # Clé étrangère et Relations
    id_event = db.Column('idEvent', db.Integer,
                         db.ForeignKey('EVENEMENT.idEvent'))
    evenement = db.relationship('EvenementBD', back_populates='competitions')
    resultats = db.relationship('ResultatBD',
                                backref='competition',
                                lazy=True,
                                cascade='all, delete-orphan')
    images_rc = db.relationship('ImageAppBD',
                                secondary=image_competition_association,
                                lazy='subquery',
                                backref=db.backref('competitions_associees',
                                                   lazy=True))


class EventClubBD(UserMixin, db.Model):
    __tablename__ = 'EVENTCLUB'

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
    # Clé étrangère et Relations
    id_event = db.Column('idEvent', db.Integer,
                         db.ForeignKey('EVENEMENT.idEvent'))
    evenement = db.relationship('EvenementBD', back_populates='event_clubs')
    images_re = db.relationship('ImageAppBD',
                                secondary=image_evenement_club_association,
                                lazy='subquery',
                                backref=db.backref('eventclubs_associes',
                                                   lazy=True))


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
    id_event = db.Column('idEvent', db.Integer,
                         db.ForeignKey('EVENEMENT.idEvent'))
    evenement = db.relationship('EvenementBD',
                                backref=db.backref('entrainements', lazy=True))


class AdminBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table ADMINISTRATEUR, compatible Flask-Login.
    """
    __tablename__ = 'ADMINISTRATEUR'

    # Mappage des colonnes SQL
    id = db.Column('idAdmin', db.Integer, primary_key=True)
    email = db.Column('emailA', db.String(41), unique=True, nullable=False)
    mdp_hash = db.Column('mdpA', db.String(64))
    formulaireDemandeSite = db.Column(db.Boolean, default=True, nullable=False)
    formulaireDemandeMail = db.Column(db.Boolean, default=True, nullable=False)
    formulaireQuestionSite = db.Column(db.Boolean, default=True, nullable=False)
    formulaireQuestionMail = db.Column(db.Boolean, default=True, nullable=False)
    formulaireSignalementSite = db.Column(db.Boolean,
                                          default=True,
                                          nullable=False)
    formulaireSignalementMail = db.Column(db.Boolean,
                                          default=True,
                                          nullable=False)
    demandeModifSite = db.Column(db.Boolean, default=True, nullable=False)
    demandeModifMail = db.Column(db.Boolean, default=True, nullable=False)
    demandeInscriptionSite = db.Column(db.Boolean, default=True, nullable=False)
    demandeInscriptionMail = db.Column(db.Boolean, default=True, nullable=False)


class InscriptionBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table INSCRIPTION, compatible Flask-Login.
    """
    __tablename__ = 'INSCRIPTION'

    # Mappage des colonnes SQL
    id = db.Column('idInscription',
                   db.Integer,
                   primary_key=True,
                   autoincrement=True)
    email = db.Column('mailInscr', db.String(41), unique=True, nullable=False)
    nom = db.Column('nomI', db.String(41))
    prenom = db.Column('prenomI', db.String(41))
    ddn = db.Column('ddnI', db.Date)
    numTel = db.Column('numTelI', db.String(20))
    mdp_hash = db.Column('mdpI', db.String(128), nullable=False)
    sexe = db.Column('sexeI', db.String(5))
    date = db.Column('dateInscription', db.Date)


class ModifBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table MODIFICATION, compatible Flask-Login.
    """
    __tablename__ = 'MODIFICATION'

    id = db.Column('idModif', db.Integer, primary_key=True)
    id_membre = db.Column('idMembre',
                          db.Integer,
                          db.ForeignKey('MEMBRE.idMembre'),
                          nullable=False)
    nom = db.Column('nomModif', db.String(41))
    prenom = db.Column('prenomModif', db.String(41))
    email = db.Column('emailModif', db.String(100), unique=True, nullable=False)
    sexe = db.Column('sexeModif', db.String(5))
    ddn = db.Column('ddnModif', db.Date)
    numTel = db.Column('numTelModif', db.String(20))
    date = db.Column('dateModif', db.Date)
    numLicense = db.Column(db.String(67))
    justification = db.Column('justificationModif', db.String(200))
    membre = db.relationship('MembreBD',
                             backref=db.backref('modifications',
                                                lazy='dynamic'))


class ParticiperBD(UserMixin, db.Model):
    """
    Modèle SQLAlchemy pour la table PARTICIPER, compatible Flask-Login.
    Lie un Membre à un Evenement.
    """
    __tablename__ = 'PARTICIPER'

    id_event = db.Column('idEvent',
                         db.Integer,
                         db.ForeignKey('EVENEMENT.idEvent'),
                         primary_key=True)
    id_membre = db.Column('idMembre',
                          db.Integer,
                          db.ForeignKey('MEMBRE.idMembre'),
                          primary_key=True)

    membre = db.relationship('MembreBD',
                             backref=db.backref('evenements_inscrits',
                                                lazy='dynamic'))
    evenement = db.relationship('EvenementBD',
                                backref=db.backref('participants',
                                                   lazy='dynamic'))


class RepondreBD(db.Model):
    """
    Table d'association entre un administrateur et un formulaire auquel il a répondu.
    """
    __tablename__ = 'REPONDRE'
    id_formulaire = db.Column('idFormulaire',
                              db.Integer,
                              db.ForeignKey('FORMULAIRE_CONTACT.idFormulaire'),
                              primary_key=True)
    id_admin = db.Column('idAdmin',
                         db.Integer,
                         db.ForeignKey('ADMINISTRATEUR.idAdmin'),
                         primary_key=True)


class RemplirBD(db.Model):
    """
    Table d'association entre un membre et un formulaire qu'il a rempli.
    """
    __tablename__ = 'REMPLIR'
    id_formulaire = db.Column('idFormulaire',
                              db.Integer,
                              db.ForeignKey('FORMULAIRE_CONTACT.idFormulaire'),
                              primary_key=True)
    id_membre = db.Column('idMembre',
                          db.Integer,
                          db.ForeignKey('MEMBRE.idMembre'),
                          primary_key=True)


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

    membre = db.relationship('MembreBD',
                             backref=db.backref('formulaires', lazy=True))
    admin = db.relationship('AdminBD',
                            backref=db.backref('formulaires', lazy=True))

    reponses = db.relationship('RepondreBD',
                               backref='formulaire',
                               cascade="all, delete-orphan")
    remplissages = db.relationship('RemplirBD',
                                   backref='formulaire',
                                   cascade="all, delete-orphan")


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
    id_competition = db.Column('idCompetition', db.Integer,
                               db.ForeignKey('COMPETITION.idCompetition'))
    id_membre = db.Column('idMembre', db.Integer,
                          db.ForeignKey('MEMBRE.idMembre'))

    membre = db.relationship('MembreBD',
                             backref=db.backref('resultats', lazy=True))


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
    imageP = db.Column(db.String(255))


class HoraireBD(db.Model):
    __tablename__ = 'HORAIRE'
    id = db.Column('idHoraire', db.Integer, primary_key=True)
    jour = db.Column(db.String(10))
    heure_debut = db.Column('heureDebut', db.String(5))
    heure_fin = db.Column('heureFin', db.String(5))
    activite = db.Column(db.String(100))
    details = db.Column(db.String(255))


class TarifBD(db.Model):
    __tablename__ = 'TARIF'
    id = db.Column('idTarif', db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    prix = db.Column(db.Integer)
    description = db.Column(db.String(255))
    categorie = db.Column(db.String(20))


class ImageArticleBD(db.Model):
    """
    Table stockant les multiples images d'un article.
    """
    __tablename__ = 'IMAGEARTICLE'

    id = db.Column('idImageArticle', db.Integer, primary_key=True)
    nom = db.Column('nomI', db.String(255))
    id_article = db.Column('idArticle', db.Integer,
                           db.ForeignKey('ARTICLE.idArticle'))


class ArticleBD(db.Model):
    __tablename__ = 'ARTICLE'

    id = db.Column('idArticle', db.Integer, primary_key=True)
    titre = db.Column('titreA', db.String(100))
    contenu = db.Column('contenuA', db.Text)
    date = db.Column('dateA', db.Date)
    images = db.relationship('ImageArticleBD',
                             backref='article',
                             lazy=True,
                             cascade="all, delete-orphan")


class ImageAppBD(db.Model):
    __tablename__ = 'IMAGEAPP'

    idImage = db.Column(db.Integer, primary_key=True)
    urlI = db.Column(db.String(255))
    prive = db.Column(db.Boolean)
    alt = db.Column(db.String(21))


class NotifsBD(db.Model):
    __tablename__ = 'NOTIFS'

    idNotifs = db.Column(db.Integer, primary_key=True)
    typeN = db.Column(db.String(1255))
    sourceN = db.Column(db.String(255))
    lue = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    link = db.Column(db.String(255))
    idAdmin = db.Column(db.Integer, db.ForeignKey('ADMINISTRATEUR.idAdmin'))
    idMembre = db.Column(db.Integer, db.ForeignKey('MEMBRE.idMembre'))

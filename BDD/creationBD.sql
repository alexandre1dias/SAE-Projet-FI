CREATE TABLE ADMINISTRATEUR(
    idAdmin integer AUTO_INCREMENT,
    emailA varchar(41) unique,
    mdpA varchar(256) not null,
    formulaireDemandeSite boolean DEFAULT true not null,
    formulaireDemandeMail boolean DEFAULT true not null,
    formulaireQuestionSite boolean DEFAULT true not null,
    formulaireQuestionMail boolean DEFAULT true not null,
    formulaireSignalementSite boolean DEFAULT true not null,
    formulaireSignalementMail boolean DEFAULT true not null,
    demandeModifSite boolean DEFAULT true not null,
    demandeModifMail boolean DEFAULT true not null,
    demandeInscriptionSite boolean DEFAULT true not null,
    demandeInscriptionMail boolean DEFAULT true not null,
    PRIMARY KEY(idAdmin)
);
    
create table MEMBRE(
    idMembre integer AUTO_INCREMENT,
    nomM varchar(41) not null,
    prenomM varchar(41) not null,
    emailM varchar(100) unique,
    mdpM varchar(256) not null,
    date_inscription date DEFAULT CURRENT_DATE,
    sexeM varchar(5) not null,
    ddnM date not null,
    age integer not null,
    niveau varchar(15) not null,
    statut varchar(30) DEFAULT "Membre",
    activite boolean DEFAULT True,
    numTel varchar(20),
    numLicense varchar(67) default null,
    eventInscriptionSite boolean DEFAULT true not null,
    evenementInscriptionMail boolean DEFAULT true not null,
    eventNouveauSite boolean DEFAULT true not null,
    eventNouveauMail boolean DEFAULT true not null,
    eventAnnulationSite boolean DEFAULT true not null,
    eventAnnulationMail boolean DEFAULT true not null,
    resultatNouveauSite boolean DEFAULT true not null,
    resultatNouveauMail boolean DEFAULT true not null,
    reponseFormulaireSite boolean DEFAULT true not null,
    reponseFormulaireMail boolean DEFAULT true not null,
    modifProfilSite boolean DEFAULT true not null,
    modifProfilMail boolean DEFAULT true not null,
    PRIMARY KEY(idMembre)
);

create table NOTIFS(
    idNotifs integer AUTO_INCREMENT,
    typeN varchar(1255) not null,
    sourceN varchar(255) not null,
    lue boolean DEFAULT false,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    link VARCHAR(255),
    idMembre integer,
    idAdmin integer,
    PRIMARY KEY(idNotifs)
);

create table RECEVOIRM(
    idNotifs integer,
    idMembre integer,
    PRIMARY KEY(idNotifs, idMembre)
);

create table RECEVOIRA(
    idNotifs integer,
    idAdmin integer,
    PRIMARY KEY(idNotifs, idAdmin)

);

create table FORMULAIRE_CONTACT(
    idFormulaire integer AUTO_INCREMENT,
    typeFC varchar(20) not null,
    sujetFC varchar(100) not null,
    mailFC varchar(41) not null,
    descriptionFC varchar(500),
    dateFC date,
    reponse varchar(300),
    repondu boolean default false,
    idMembre integer,
    idAdmin integer,
    PRIMARY KEY(idFormulaire)
);

create table REPONDRE(
    idFormulaire integer,
    idAdmin integer,
    PRIMARY KEY(idFormulaire, idAdmin)
);

create table REMPLIR(
    idFormulaire integer,
    idMembre integer,
    PRIMARY KEY(idFormulaire, idMembre)
);

create table INSCRIPTION(
    idInscription integer AUTO_INCREMENT,
    mailInscr varchar(100) unique,
    nomI varchar(41) not null,
    prenomI varchar(41) not null,
    ddnI date not null,
    mdpI varchar(256) not null,
    sexeI varchar(5) not null,
    dateInscription date not null,
    numTelI varchar(20),
    PRIMARY KEY(idInscription)
);


create table MODIFICATION(
    idModif integer AUTO_INCREMENT,
    nomModif varchar(41),
    prenomModif varchar(41) ,
    emailModif varchar(100),
    sexeModif varchar(5),
    ddnModif date,
    numTelModif varchar(20),
    dateModif date,
    numLicense varchar(67) DEFAULT NULL,
    justificationModif varchar(500),
    idMembre integer,
    PRIMARY KEY(idModif)
);


create table GENERER(
    idInscription integer,
    idMembre integer,
    PRIMARY KEY(idInscription, idMembre)
);

create table EVENEMENT(
    idEvent integer AUTO_INCREMENT,
    PRIMARY KEY(idEvent)
);

create table PARTICIPER(
    idEvent integer,
    idMembre integer,
    PRIMARY KEY(idEvent, idMembre)
);

create table ENTRAINEMENT(
    idEntrainement integer AUTO_INCREMENT,
    jourEN varchar(8) not null,
    villeEN varchar(50) not null,
    adresseEN varchar(50) not null,
    dateEN date not null,
    heureDebutEN varchar(5) not null,
    heureFinEN varchar(5) not null,
    typeArmeEN varchar(12) not null,
    niveauEN varchar(45) not null,
    idEvent integer,
    PRIMARY KEY(idEntrainement)

);

create table REUNION(
    idReunion integer AUTO_INCREMENT,
    nomRE varchar(100) not null,
    villeRE varchar(50),
    adresseRE varchar(50),
    datedebutRE date not null,
    heureDebutRE varchar(5) not null,
    dateFinRE date not null,
    heureFinRE varchar(5) not null,
    nbParticipantsRE integer,
    typeReunionRE varchar(64) not null,
    rapportRE varchar(200),
    idEvent integer,
    PRIMARY KEY(idReunion)

);

create table COMPETITION(
    idCompetition integer AUTO_INCREMENT,
    nomCO varchar(50) not null,
    villeCO varchar(50) not null,
    adresseCO varchar(50) not null,
    dateDebutCO date not null,
    heureDebutCO varchar(5) not null,
    dateFinCO date not null,
    heureFinCO varchar(5) not null,
    typeArmeCO varchar(12) not null,
    nbParticipantsCO integer,
    sexeCO varchar(5) not null,
    typeCompete varchar(15) not null,
    descriptionCO varchar(200), 
    niveauCO varchar(45) not null,
    classementCO varchar(20),
    passeeCO boolean,
    idEvent integer,
    PRIMARY KEY(idCompetition)
);

create table EVENTCLUB(
    idEventClub integer AUTO_INCREMENT,
    NomEV varchar(50) not null,
    villeEV varchar(50) not null,
    adresseEV varchar(50) not null,
    dateDebutEV date not null,
    heureDebutEV varchar(5) not null,
    dateFinEV date not null,
    heureFinEV varchar(5) not null,
    nbParticipantEV integer,
    descriptionEV varchar(200) not null,
    niveauxEV varchar(45) not null,
    passeeEV boolean,
    idEvent integer,
    PRIMARY KEY(idEventClub)
);

create table RESULTAT(
    idResultat integer AUTO_INCREMENT,
    resultat integer,
    dateRE date not null,
    typeArmeRE varchar(12) not null,
    typeCompeteRE varchar(15) not null,
    idCompetition integer,
    idMembre integer,
    PRIMARY KEY(idResultat)
);

create table RESULTER(
    idResultat integer,
    idCompetition integer,
    PRIMARY KEY(idResultat, idCompetition)
);

create table AVOIR(
    idResultat integer,
    idMembre integer,
    PRIMARY KEY(idResultat, idMembre)
);

create table IMAGEAPP(
    idImage integer AUTO_INCREMENT,
    urlI varchar(255) not null,
    prive boolean,
    alt varchar(21),
    PRIMARY KEY(idImage)
);

create table IMAGERC(
    idImage integer,
    idCompetition integer,
    PRIMARY KEY(idImage, idCompetition)
);

create table IMAGERE(
    idImage integer,
    idEventClub integer,
    PRIMARY KEY(idImage, idEventClub)
);

create table INFORMATION(
    idInformation integer AUTO_INCREMENT,
    dateIN date not null,
    heureIN varchar(5) not null,
    titreIN varchar(50) not null,
    contenuIN varchar(600),
    PRIMARY KEY(idInformation)
);

create table PRESSE(
    idPresse integer AUTO_INCREMENT,
    dateP date,
    heureP varchar(5) not null,
    titreP varchar(550) not null,
    contenuP varchar(600),
    lienP varchar(255) not null,
    imageP VARCHAR(255),
    PRIMARY KEY(idPresse)
);

CREATE TABLE HORAIRE (
    idHoraire integer AUTO_INCREMENT,
    jour varchar(10) not null,
    heureDebut varchar(5) not null,
    heureFin varchar(5) not null,
    activite varchar(100) not null,
    details varchar(255),
    PRIMARY KEY(idHoraire)
);

CREATE TABLE TARIF (
    idTarif integer AUTO_INCREMENT,
    nom varchar(50) not null,
    prix integer not null,
    description varchar(255),
    categorie varchar(20) not null,
    PRIMARY KEY(idTarif)
);

CREATE TABLE ARTICLE (
    idArticle integer AUTO_INCREMENT,
    titreA varchar(500) not null,
    contenuA text,
    dateA date not null,
    imgA varchar(255),
    PRIMARY KEY(idArticle)
);

CREATE TABLE IMAGEARTICLE (
    idImageArticle integer AUTO_INCREMENT,
    nomI varchar(255) not null,
    idArticle integer not null,
    PRIMARY KEY(idImageArticle)
);

CREATE TABLE REINITIALISATION_MDP(
    idReinit integer AUTO_INCREMENT,
    emailReinit varchar(100) not null,
    codeReinit varchar(9),
    dateDemande DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dateAcceptation DATETIME,
    acceptee boolean DEFAULT false not null,
    utilisee boolean DEFAULT false not null,
    expiration DATETIME,
    PRIMARY KEY(idReinit)
);

-- Ajout des contraintes de clé étrangère

ALTER TABLE MODIFICATION ADD FOREIGN KEY (idMembre) REFERENCES MEMBRE(idMembre);

ALTER TABLE NOTIFS ADD FOREIGN KEY (idMembre) REFERENCES MEMBRE(idMembre);
ALTER TABLE NOTIFS ADD FOREIGN KEY (idAdmin) REFERENCES ADMINISTRATEUR(idAdmin);

ALTER TABLE RECEVOIRM ADD FOREIGN KEY (idNotifs) REFERENCES NOTIFS(idNotifs);
ALTER TABLE RECEVOIRM ADD FOREIGN KEY (idMembre) REFERENCES MEMBRE(idMembre);

ALTER TABLE RECEVOIRA ADD FOREIGN KEY (idNotifs) REFERENCES NOTIFS(idNotifs);
ALTER TABLE RECEVOIRA ADD FOREIGN KEY (idAdmin) REFERENCES ADMINISTRATEUR(idAdmin);

ALTER TABLE FORMULAIRE_CONTACT ADD FOREIGN KEY (idMembre) REFERENCES MEMBRE(idMembre);
ALTER TABLE FORMULAIRE_CONTACT ADD FOREIGN KEY (idAdmin) REFERENCES ADMINISTRATEUR(idAdmin);

ALTER TABLE REPONDRE ADD FOREIGN KEY (idFormulaire) REFERENCES FORMULAIRE_CONTACT(idFormulaire);
ALTER TABLE REPONDRE ADD FOREIGN KEY (idAdmin) REFERENCES ADMINISTRATEUR(idAdmin);

ALTER TABLE REMPLIR ADD FOREIGN KEY (idFormulaire) REFERENCES FORMULAIRE_CONTACT(idFormulaire);
ALTER TABLE REMPLIR ADD FOREIGN KEY (idMembre) REFERENCES MEMBRE(idMembre);

ALTER TABLE GENERER ADD FOREIGN KEY (idInscription) REFERENCES INSCRIPTION(idInscription);
ALTER TABLE GENERER ADD FOREIGN KEY (idMembre) REFERENCES MEMBRE(idMembre);

ALTER TABLE PARTICIPER ADD FOREIGN KEY (idEvent) REFERENCES EVENEMENT(idEvent);
ALTER TABLE PARTICIPER ADD FOREIGN KEY (idMembre) REFERENCES MEMBRE(idMembre);

ALTER TABLE ENTRAINEMENT ADD FOREIGN KEY (idEvent) REFERENCES EVENEMENT(idEvent);
ALTER TABLE REUNION ADD FOREIGN KEY (idEvent) REFERENCES EVENEMENT(idEvent);
ALTER TABLE COMPETITION ADD FOREIGN KEY (idEvent) REFERENCES EVENEMENT(idEvent);
ALTER TABLE EVENTCLUB ADD FOREIGN KEY (idEvent) REFERENCES EVENEMENT(idEvent);

ALTER TABLE RESULTAT ADD FOREIGN KEY (idCompetition) REFERENCES COMPETITION(idCompetition);
ALTER TABLE RESULTAT ADD FOREIGN KEY (idMembre) REFERENCES MEMBRE(idMembre);

ALTER TABLE RESULTER ADD FOREIGN KEY (idResultat) REFERENCES RESULTAT(idResultat);
ALTER TABLE RESULTER ADD FOREIGN KEY (idCompetition) REFERENCES COMPETITION(idCompetition);

ALTER TABLE AVOIR ADD FOREIGN KEY (idResultat) REFERENCES RESULTAT(idResultat);
ALTER TABLE AVOIR ADD FOREIGN KEY (idMembre) REFERENCES MEMBRE(idMembre);

ALTER TABLE IMAGERC ADD FOREIGN KEY (idImage) REFERENCES IMAGEAPP(idImage);
ALTER TABLE IMAGERC ADD FOREIGN KEY (idCompetition) REFERENCES COMPETITION(idCompetition);

ALTER TABLE IMAGERE ADD FOREIGN KEY (idImage) REFERENCES IMAGEAPP(idImage);
ALTER TABLE IMAGERE ADD FOREIGN KEY (idEventClub) REFERENCES EVENTCLUB(idEventClub);

ALTER TABLE IMAGEARTICLE ADD FOREIGN KEY (idArticle) REFERENCES ARTICLE(idArticle);
CREATE TABLE ADMINISTRATEUR(
    idAdmin integer AUTO_INCREMENT,
    emailA varchar(41) unique,
    mdpA varchar(64) not null,
    idParamNotifAdmin integer,
    PRIMARY KEY(idAdmin)
);

create table PARAMETRE_NOTIF_ADMIN(
    idParamNotifAdmin integer AUTO_INCREMENT,
    formulaireDemandeSite boolean not null,
    formulaireDemandeMail boolean not null,
    formulaireQuestionSite boolean not null,
    formulaireQuestionMail boolean not null,
    formulaireSignalementSite boolean not null,
    formulaireSignalementMail boolean not null,
    demandeModifSite boolean not null,
    demandeModifMail boolean not null,
    demandeInscriptionSite boolean not null,
    demandeInscriptionMail boolean not null,
    idAdmin integer,
    PRIMARY KEY(idParamNotifAdmin)
);

create table PARAMETRE_NOTIF_MEMBRE(
    idParamNotifMembre integer AUTO_INCREMENT,
    eventInscriptionSite boolean not null,
    evenementInscriptionMail boolean not null,
    eventNouveauSite boolean not null,
    eventNouveauMail boolean not null,
    eventAnnulationSite boolean not null,
    eventAnnulationMail boolean not null,
    resultatNouveauSite boolean not null,
    resultatNouveauMail boolean not null,
    reponseFormulaireSite boolean not null,
    reponseFormulaireMail boolean not null,
    modifProfilSite boolean not null,
    modifProfilMail boolean not null,
    idMembre integer,
    PRIMARY KEY(idParamNotifMembre)
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
    idParamNotifMembre integer,
    PRIMARY KEY(idMembre)
);

create table NOTIFS(
    idNotifs integer AUTO_INCREMENT,
    typeN varchar(19) not null,
    sourceN varchar(255) not null,
    lue boolean DEFAULT false,
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
    mdpI varchar(64) not null,
    sexeI varchar(5) not null,
    dateInscription date not null,
    PRIMARY KEY(idInscription)
);


create table MODIFICATION(
    idModif integer AUTO_INCREMENT,
    nomModif varchar(41),
    prenomModif varchar(41) ,
    emailModif varchar(100),
    sexeModif varchar(5),
    ddnModif date,
    dateModif date,
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
    villeRE varchar(50) not null,
    adresseRE varchar(50) not null,
    datedebutRE date not null,
    heureDebutRE varchar(5) not null,
    dateFinRE date not null,
    heureFinRE varchar(5) not null,
    nbParticipantsRE integer,
    typeReunionRE varchar(15) not null,
    rapportRE varchar(200),
    niveauRE varchar(45),
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

create table IMAGERIN(
    idImage integer,
    idInformation integer,
    PRIMARY KEY(idImage, idInformation)
);

create table PRESSE(
    idPresse integer AUTO_INCREMENT,
    dateP date,
    heureP varchar(5) not null,
    titreP varchar(50) not null,
    contenuP varchar(600),
    lienP varchar(255) not null,
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
    titreA varchar(100) not null,
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


-- Ajout des contraintes de clé étrangère

ALTER TABLE MODIFICATION ADD FOREIGN KEY (idMembre) REFERENCES MEMBRE(idMembre);

ALTER TABLE ADMINISTRATEUR ADD FOREIGN KEY (idParamNotifAdmin) REFERENCES PARAMETRE_NOTIF_ADMIN(idParamNotifAdmin);

ALTER TABLE PARAMETRE_NOTIF_ADMIN ADD FOREIGN KEY (idAdmin) REFERENCES ADMINISTRATEUR(idAdmin);

ALTER TABLE PARAMETRE_NOTIF_MEMBRE ADD FOREIGN KEY (idMembre) REFERENCES MEMBRE(idMembre);

ALTER TABLE MEMBRE ADD FOREIGN KEY (idParamNotifMembre) REFERENCES PARAMETRE_NOTIF_MEMBRE(idParamNotifMembre);

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

ALTER TABLE IMAGERIN ADD FOREIGN KEY (idImage) REFERENCES IMAGEAPP(idImage);
ALTER TABLE IMAGERIN ADD FOREIGN KEY (idInformation) REFERENCES INFORMATION(idInformation);

ALTER TABLE IMAGE_ARTICLE ADD FOREIGN KEY (idArticle) REFERENCES ARTICLE(idArticle);
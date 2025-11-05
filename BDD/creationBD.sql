CREATE TABLE ADMINISTRATEUR(
    idAdmin integer AUTO_INCREMENT,
    emailA varchar(41),
    mdpA varchar(64),
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
    resuletatNouveauMail boolean not null,
    reponseFormulaireSite boolean not null,
    reponseFormulaireMail boolean not null,
    modifProfilSite boolean not null,
    modifProfilMail boolean not null,
    idMembre integer,
    PRIMARY KEY(idParamNotifMembre)
);
    
create table MEMBRE(
    idMembre integer AUTO_INCREMENT,
    nomM varchar(41),
    prenomM varchar(41),
    emailM varchar(41),
    mdpM varchar(64),
    date_inscription date,
    sexeM varchar(5),
    ddnM date,
    age integer,
    niveau varchar(15),
    statut varchar(30),
    activite boolean,
    idParamNotifMembre integer,
    PRIMARY KEY(idMembre)
);

create table NOTIFS(
    idNotifs integer AUTO_INCREMENT,
    typeN varchar(19),
    sourceN varchar(255),
    lue boolean,
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
    typeFC varchar(15),
    sujetFC varchar(20),
    mailFC varchar(41),
    descriptionFC varchar(200),
    dateFC date,
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
    mailInscr varchar(41),
    nomI varchar(41),
    prenomI varchar(41),
    ddnI date,
    mdpI varchar(64),
    sexeI varchar(5),
    acceptee boolean,
    PRIMARY KEY(idInscription)
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
    jourEN varchar(8),
    lieuEN varchar(20),
    dateEN date,
    heureDebutEN varchar(5),
    heureFinEN varchar(5),
    typeArmeEN varchar(12),
    niveauEN varchar(15),
    idEvent integer,
    PRIMARY KEY(idEntrainement)

);

create table REUNION(
    idReunion integer AUTO_INCREMENT,
    nomRE varchar(20),
    lieuRE varchar(20),
    dateRE date,
    heureDebutRE varchar(5),
    nbParticipantsRE integer,
    typeReunionRE varchar(15),
    rapportRE varchar(200),
    niveauRE varchar(15),
    idEvent integer,
    PRIMARY KEY(idReunion)

);

create table COMPETITION(
    idCompetition integer AUTO_INCREMENT,
    nomCO varchar(50),
    villeCO varchar(50),
    adresseCO varchar(50),
    dateDebutCO date,
    heureDebutCO varchar(5),
    dateFinCO date,
    heureFinCO varchar(5),
    typeArmeCO varchar(12),
    nbParticipantsCO integer,
    sexeCO varchar(5),
    typeCompete varchar(15),
    descriptionCO varchar(200), 
    niveauCO varchar(15),
    classementCO varchar(20),
    passeeCO boolean,
    idEvent integer,
    PRIMARY KEY(idCompetition)
);

create table EVENTCLUB(
    idEventClub integer AUTO_INCREMENT,
    NomEV varchar(50),
    villeEV varchar(50),
    adresseEV varchar(50),
    dateDebutEV date,
    heureDebutEV varchar(5),
    dateFinEV date,
    heureFinEV varchar(5),
    nbParticipantEV integer,
    descriptionEV varchar(200),
    niveauxEV varchar(45),
    passeeEV boolean,
    idEvent integer,
    PRIMARY KEY(idEventClub)
);

create table RESULTAT(
    idResultat integer AUTO_INCREMENT,
    resultat varchar(50),
    dateRE date,
    typeArmeRE varchar(12),
    typeCompeteRE varchar(15),
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
    urlI varchar(255),
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

create table ACTUALITE(
    idActualite integer AUTO_INCREMENT,
    dateAC date,
    heureAC varchar(5),
    nomAC varchar(15),
    categorieAC varchar(15),
    PRIMARY KEY(idActualite)
);

create table IMAGERA(
    idImage integer,
    idActualite integer,
    PRIMARY KEY(idImage, idActualite)
);

-- Ajout des contraintes de clé étrangère

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

ALTER TABLE IMAGERA ADD FOREIGN KEY (idImage) REFERENCES IMAGEAPP(idImage);
ALTER TABLE IMAGERA ADD FOREIGN KEY (idActualite) REFERENCES ACTUALITE(idActualite);
-- Désactivation de la vérification des clés étrangères 
SET FOREIGN_KEY_CHECKS=0;

-- Insertion des administrateurs (existant)
INSERT INTO ADMINISTRATEUR (emailA, mdpA, idParamNotifAdmin) VALUES
('admin@escrime.com', 'pbkdf2:sha256:1000000$qqixfFaza1lTKCXZ$b0e14f826b68f1fd03cf666f754ee7551b1ec336e1737323d9d7b501e1cc8f87', NULL); --mdp:motdepasseadmin

-- Insertion des paramètres de notification pour les administrateurs (existant)
INSERT INTO PARAMETRE_NOTIF_ADMIN (idParamNotifAdmin, formulaireDemandeSite, formulaireDemandeMail, formulaireQuestionSite, formulaireQuestionMail, formulaireSignalementSite, formulaireSignalementMail, demandeModifSite, demandeModifMail, demandeInscriptionSite, demandeInscriptionMail, idAdmin) VALUES
(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);

-- Mise à jour de l'administrateur (existant)
UPDATE ADMINISTRATEUR SET idParamNotifAdmin = 1 WHERE idAdmin = 1;

-- Insertion des membres (existants 1-8)
INSERT INTO MEMBRE (nomM, prenomM, emailM, mdpM, date_inscription, sexeM, ddnM, statut, activite, idParamNotifMembre) VALUES
('Dupont', 'Jean', 'jean.dupont@email.com', 'pbkdf2:sha256:1000000$tT64PE5pXmf8H5xp$7954b1dfebb585db1408f2b3f3f1064f8deeb074e8941034179f161638233e5a', '2023-01-15', 'Homme', '1995-05-20', 'Membre', 1, NULL), -- mdp:mdp123
('Durand', 'Marie', 'marie.durand@email.com', 'pbkdf2:sha256:1000000$c6IE52kZ3Yrdbkvu$b0aafc941c8602f009ce4cc686e374576d865ee0b4d521b3407e9e1fb632edc7', '2023-02-20', 'Femme', '2008-08-10', 'Membre', 1, NULL), -- mdp:mdp456
('Martin', 'Paul', 'paul.martin@email.com', 'pbkdf2:sha256:1000000$IYgGm2G0tHtJrOqP$f69840820f3fb35f5c0a49b7a8d8150d1e1047d94dba27fa717cffb923032a6d', '2022-09-01', 'Homme', '2015-03-25', 'Ancien Membre', 0, NULL),-- mdp:mdp789
('Eche', 'Régis', 'regis.eche@email.com', 'pbkdf2:sha256:1000000$ykcxRPliFcJbZmY9$4069b9516459c50051202f84ba708cc3e0d8f3e3939f0d7590e47876cefc0dac', '2000-01-01', 'Homme', '1975-02-07','Président', 1, NULL),-- mdp:mdp741
('Dominique', 'MARQUET', 'dom.mar@email.com', 'pbkdf2:sha256:1000000$vWV2QiPn3dN6hr4W$3dd808a8f7f2bec74b5ff34c44c0c777955e83bda1a8183a0153106e4665f9b0', '2006-01-01', 'Homme', '1974-02-07','Vice-Président', 1, NULL),-- mdp:mdp442
('Bernard', 'DELADERIERE', 'ber.del@email.com', 'pbkdf2:sha256:1000000$CQyHolHqSrk4qIAa$a5f22728417e72a3a9f7e79d3fe0cab81f167ab7a8fa80bd243ef8135911d6d8', '1999-01-01', 'Homme', '1976-02-07','Trésorier Général', 1, NULL),-- mdp:mdp5231
('Pascale', 'LHOMME', 'pas.lhm@email.com', 'pbkdf2:sha256:1000000$02eNZYjkYEzZK4zy$12b29b9fd98dfac13b9606b141587c117ee510e2cb02ac054be74ef40d2923ae', '2002-01-01', 'Femme', '1978-02-07','Secrétaire Générale', 1, NULL),-- mdp:mdp433
('Christophe', 'LECHOPIER', 'chr.lec@email.com', 'pbkdf2:sha256:1000000$35JA6vIpcTUyLuh7$108c8dc3dc6880c01853dcb8d2cfb99830bbaf37fe830e20fbcf99f9109bd99b', '2005-01-01', 'Homme', '1969-02-07','Membre du Comité', 1, NULL),-- mdp:mdp541
('Petit', 'Lucas', 'lucas.petit@email.com', 'pbkdf2:sha256:1000000$cBIfWWnFZa0AJLut$35374e4ffada5d72a3971137a11e066dca0406d5e9bfef951b390162a6ab77ab', '2024-09-05', 'Homme', '2010-06-15', 'Membre', 1, NULL),-- mdp:mdpL1
('Moreau', 'Chloé', 'chloe.moreau@email.com', 'pbkdf2:sha256:1000000$VUBF6WrY5IUcX9eY$7f43355adf3dae0bf457ea486e1184818baf2092b185ad5aaf29fab9985be68c', '2024-09-10', 'Femme', '2013-03-10', 'Membre', 1, NULL),-- mdp:mdpC2
('Garcia', 'Alice', 'alice.garcia@email.com', 'pbkdf2:sha256:1000000$XJSBBfHcblFzhkSU$dffbeb82aefc94cf5fe953bb0fc26fb92671b4d87c2b34df140d26f0a95dffaf', '2024-09-12', 'Femme', '2000-01-01', 'Membre', 1, NULL),-- mdp:mdpA3
('Robert', 'Tom', 'tom.robert@email.com', 'pbkdf2:sha256:1000000$vXfAPYB4hs92DWDL$6634eb39bbb811c3f994dc5f1904c96bbfee8041e629c9eaf91d85aee72bebfb', '2024-09-15', 'Homme', '1985-11-30', 'Ancien Membre', 0, NULL),-- mdp:mdT4
('Richard', 'Léa', 'lea.richard@email.com', 'pbkdf2:sha256:1000000$IsM9yi8r6jErCft0$0d46f92b1592e8ee6ea324931cecfc54c7d63d17afc638835eda7555a7c434cf', '2024-10-01', 'Femme', '2005-07-20', 'Membre', 1, NULL),-- mdp:mdpL5
('Garnier', 'Hugo', 'hugo.garnier@email.com', 'pbkdf2:sha256:1000000$Qq6Be7oaQ5IxAdDJ$1a218b0462f3ff16fcfd0153449d4322df618093c194588bec37a6846ad0f6bc', '2025-01-10', 'Homme', '2008-04-12', 'Membre', 1, NULL), -- M17, -- mdp:mdp14
('Roux', 'Manon', 'manon.roux@email.com', 'pbkdf2:sha256:1000000$SmlP0INXlKVzL9Ci$0a456d2eb9a1ce9511931ad6673e31deee352da9776e894aefa22d67b30f7fa3', '2025-01-11', 'Femme', '2009-11-01', 'Membre', 1, NULL), -- M17, -- mdp:mdp15
('David', 'Léo', 'leo.david@email.com', 'pbkdf2:sha256:1000000$KNmYCB9WhgTnc4mv$2bfb12bb8def3ce29cad637299b30973ebf98fbdbcf6ab8db7c9ca852c9e89c3', '2025-01-12', 'Homme', '2012-07-20', 'Membre', 1, NULL), -- M13, -- mdp:mdp16
('Bertrand', 'Camille', 'camille.bertrand@email.com', 'pbkdf2:sha256:1000000$A8HyfeoHG8DPVyAn$8c49c94ff40a87202874dbf846db1d0398566a08cb900beb6315aed5203fc4bf', '2025-01-13', 'Femme', '2011-01-30', 'Membre', 1, NULL), -- M15, -- mdp:mdp17
('Morel', 'Arthur', 'arthur.morel@email.com', 'pbkdf2:sha256:1000000$85Mh62uJq1WRCcJh$f747243e91663784bf8fbe0b90f36f82c35c507e97f946156f3558c17d1b7a45', '2025-01-14', 'Homme', '2013-03-15', 'Membre', 1, NULL), -- M13, -- mdp:mdp18
('Fournier', 'Zoé', 'zoe.fournier@email.com', 'pbkdf2:sha256:1000000$dyWIOH1iQvbHk0tF$c04c39d8cb6a5670e18337375312b759848517cb49763ff3dfa83ce519e07366', '2025-01-15', 'Femme', '2005-08-25', 'Membre', 1, NULL), -- M20, -- mdp:mdp19
('Girard', 'Jules', 'jules.girard@email.com', 'pbkdf2:sha256:1000000$LNeqvPwiwZqA22DQ$3e9ddce6f16be69576157c91622d068106cacef22fab3ce16e0f648cec5d81f0', '2025-02-01', 'Homme', '2004-05-10', 'Membre', 1, NULL), -- Senior, -- mdp:mdp20
('Bonnet', 'Emma', 'emma.bonnet@email.com', 'pbkdf2:sha256:1000000$wCXBxrNDlH1gAnvN$a6938a5e70396c3aeb1c5eac4cb268560711fe9ace2d1e35d544f4f9e2751b2b', '2025-02-02', 'Femme', '1999-02-18', 'Membre', 1, NULL), -- Senior, -- mdp:mdp21
('Dubois', 'Gabriel', 'gabriel.dubois@email.com', 'pbkdf2:sha256:1000000$VDmJhDFmVC6wIfkL$d7cae03822ac53fd80cf9dfa61ea375178b23f426d46faae41a4d763fa4f5185', '2025-02-03', 'Homme', '1980-12-05', 'Membre', 1, NULL), -- Vétéran, -- mdp:mdp22
('Leclerc', 'Louise', 'louise.leclerc@email.com', 'pbkdf2:sha256:1000000$BZKJrkuUBmOoLNoi$528d2156faddacd368c0aac55ab0ccbb62288e8254aea918e524083c9473eb3a', '2025-02-04', 'Femme', '1975-09-08', 'Membre', 1, NULL), -- Vétéran, -- mdp:mdp23
('Meyer', 'Adam', 'adam.meyer@email.com', 'pbkdf2:sha256:1000000$1is048WOxoNES71r$b97ebcfc4cbfbc7a96fdea8c0009b7b79183b41414a34e83c804e776b0baf4ab', '2025-02-05', 'Homme', '2016-01-02', 'Membre', 1, NULL), -- M9, -- mdp:mdp24
('Barbier', 'Rose', 'rose.barbier@email.com', 'pbkdf2:sha256:1000000$3I9QhSjcjoXSPa9P$037c0e66fcce4c7c19dc9bc262f4ecd9785ebb8836a2cc228ae22dffeff3a567', '2025-02-06', 'Femme', '2010-06-19', 'Membre', 1, NULL), -- M15, -- mdp:mdp25
('Brun', 'Raphaël', 'raphael.brun@email.com', 'pbkdf2:sha256:1000000$yKBUb3YcRM8zJDGZ$b2725b95124bec99a74957330a157b3e50360584c9837cc0b20e56a9801ca47f', '2025-02-07', 'Homme', '2007-03-22', 'Membre', 1, NULL), -- M20, -- mdp:mdp26
('Guerin', 'Jade', 'jade.guerin@email.com', 'pbkdf2:sha256:1000000$BSUlRpE3xzqi6vmp$937acb97f20466581b6ed23251bbb7229a11dc82103f5ca56f8271393cb89c37', '2025-02-08', 'Femme', '2006-10-14', 'Membre', 1, NULL), -- M20, -- mdp:mdp27
('Perrin', 'Louis', 'louis.perrin@email.com', 'pbkdf2:sha256:1000000$gA0OIy4Y8pp77OUq$50839f6bb05e575c4685b32465dd7777118f9854f375025960343996a5b63bc6', '2025-02-09', 'Homme', '2002-04-01', 'Membre', 1, NULL), -- Senior, -- mdp:mdp28
('Mercier', 'Ambre', 'ambre.mercier@email.com', 'pbkdf2:sha256:1000000$pY73HZsjm6kI3d8v$aa5459b16d8f8688b39235b89a377a46e37ab51a9fc97e733df86580dc049dad', '2025-02-10', 'Femme', '1995-07-07', 'Membre', 1, NULL), -- Senior, -- mdp:mdp29
('Chevalier', 'Nathan', 'nathan.chevalier@email.com', 'pbkdf2:sha256:1000000$8EnWXLsPQN138pYp$adea984b04f0c2d27ce70d96a446d8d6d11fb99be5b44b0731e3581c2e72744c', '2025-02-11', 'Homme', '2013-08-11', 'Membre', 1, NULL), -- M13, -- mdp:mdp30
('Lemoine', 'Anna', 'anna.lemoine@email.com', 'pbkdf2:sha256:1000000$a2KjLjndSgeTYohP$c43519084319b0d7da53ad91dcef220bd433ba2401b86f73e114a20163c84337', '2025-02-12', 'Femme', '2015-05-05', 'Membre', 1, NULL), -- M11, -- mdp:mdp31
('Benali', 'Mohamed', 'mohamed.benali@email.com', 'pbkdf2:sha256:1000000$423gCfPo7UAvS5VT$1ad6422ebbb177ec1da4accd42a9afb64881ace8c6b83120d14989a8057eca44', '2025-02-13', 'Homme', '1990-11-30', 'Membre', 1, NULL), -- Senior, -- mdp:mdp32
('Roy', 'Inès', 'ines.roy@email.com', 'pbkdf2:sha256:1000000$c9CVNnJlJY4gA2Qy$9ba9aa234f30fede19fbf8dae5358d62bbe731c81cf95653f7cd8488b318ab29', '2025-02-14', 'Femme', '1988-01-20', 'Membre', 1, NULL); -- Senior, -- mdp:mdp33


-- Insertion des paramètres de notification pour les membres (existants 1-3)
INSERT INTO PARAMETRE_NOTIF_MEMBRE (eventInscriptionSite, evenementInscriptionMail, eventNouveauSite, eventNouveauMail, eventAnnulationSite, eventAnnulationMail, resultatNouveauSite, resultatNouveauMail, reponseFormulaireSite, reponseFormulaireMail, modifProfilSite, modifProfilMail, idMembre) VALUES
(1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1),
(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2),
(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3);

-- Ajouts de paramètres de notification (existants 4-13)
INSERT INTO PARAMETRE_NOTIF_MEMBRE (eventInscriptionSite, evenementInscriptionMail, eventNouveauSite, eventNouveauMail, eventAnnulationSite, eventAnnulationMail, resultatNouveauSite, resultatNouveauMail, reponseFormulaireSite, reponseFormulaireMail, modifProfilSite, modifProfilMail, idMembre) VALUES
(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4),
(1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 5),
(1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 6),
(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7),
(0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 8),
(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9),
(1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 10),
(1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 11),
(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12),
(1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 13),
(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 14),
(1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 15),
(1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 16),
(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 17),
(1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 18),
(1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 19),
(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 20),
(1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 21),
(0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 22),
(1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 23),
(1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 24),
(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 25),
(1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 26),
(1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 27),
(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 28),
(1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 29),
(1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 30),
(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 31),
(1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 32),
(1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 33);



-- Mise à jour des membres pour lier leurs paramètres de notification (existants 1-3)
UPDATE MEMBRE SET idParamNotifMembre = 1 WHERE idMembre = 1;
UPDATE MEMBRE SET idParamNotifMembre = 2 WHERE idMembre = 2;
UPDATE MEMBRE SET idParamNotifMembre = 3 WHERE idMembre = 3;
UPDATE MEMBRE SET idParamNotifMembre = 4 WHERE idMembre = 4;
UPDATE MEMBRE SET idParamNotifMembre = 5 WHERE idMembre = 5;
UPDATE MEMBRE SET idParamNotifMembre = 6 WHERE idMembre = 6;
UPDATE MEMBRE SET idParamNotifMembre = 7 WHERE idMembre = 7;
UPDATE MEMBRE SET idParamNotifMembre = 8 WHERE idMembre = 8;
UPDATE MEMBRE SET idParamNotifMembre = 9 WHERE idMembre = 9;
UPDATE MEMBRE SET idParamNotifMembre = 10 WHERE idMembre = 10;
UPDATE MEMBRE SET idParamNotifMembre = 11 WHERE idMembre = 11;
UPDATE MEMBRE SET idParamNotifMembre = 12 WHERE idMembre = 12;
UPDATE MEMBRE SET idParamNotifMembre = 13 WHERE idMembre = 13;
UPDATE MEMBRE SET idParamNotifMembre = 14 WHERE idMembre = 14;
UPDATE MEMBRE SET idParamNotifMembre = 15 WHERE idMembre = 15;
UPDATE MEMBRE SET idParamNotifMembre = 16 WHERE idMembre = 16;
UPDATE MEMBRE SET idParamNotifMembre = 17 WHERE idMembre = 17;
UPDATE MEMBRE SET idParamNotifMembre = 18 WHERE idMembre = 18;
UPDATE MEMBRE SET idParamNotifMembre = 19 WHERE idMembre = 19;
UPDATE MEMBRE SET idParamNotifMembre = 20 WHERE idMembre = 20;
UPDATE MEMBRE SET idParamNotifMembre = 21 WHERE idMembre = 21;
UPDATE MEMBRE SET idParamNotifMembre = 22 WHERE idMembre = 22;
UPDATE MEMBRE SET idParamNotifMembre = 23 WHERE idMembre = 23;
UPDATE MEMBRE SET idParamNotifMembre = 24 WHERE idMembre = 24;
UPDATE MEMBRE SET idParamNotifMembre = 25 WHERE idMembre = 25;
UPDATE MEMBRE SET idParamNotifMembre = 26 WHERE idMembre = 26;
UPDATE MEMBRE SET idParamNotifMembre = 27 WHERE idMembre = 27;
UPDATE MEMBRE SET idParamNotifMembre = 28 WHERE idMembre = 28;
UPDATE MEMBRE SET idParamNotifMembre = 29 WHERE idMembre = 29;
UPDATE MEMBRE SET idParamNotifMembre = 30 WHERE idMembre = 30;
UPDATE MEMBRE SET idParamNotifMembre = 31 WHERE idMembre = 31;
UPDATE MEMBRE SET idParamNotifMembre = 32 WHERE idMembre = 32;
UPDATE MEMBRE SET idParamNotifMembre = 33 WHERE idMembre = 33;


-- Insertion des événements 
INSERT INTO EVENEMENT () VALUES
(), (), (), (), (), (),
-- Événements pour les compétitions 
(), (), (), (), (), (), (), (), (),
-- Événements pour les eventclubs 
(), (), (), (), (), (), (), (), (), (), (),
-- Compétitions (IDs 27-30)
(), (), (), (),
-- Entraînements (IDs 31-32)
(), (),
-- Réunions (IDs 33-34)
(), (),
-- EventClubs (IDs 35-37)
(), (), ();


-- Insertion des compétitions (existantes)
INSERT INTO COMPETITION (nomCO, villeCO, adresseCO, dateDebutCO, heureDebutCO, dateFinCO, heureFinCO, typeArmeCO, sexeCO, typeCompete, descriptionCO, niveauCO, classementCO,passeeCO, idEvent) VALUES
('Tournoi Régional', 'Orléans', '123 Rue du Sport', '2024-05-10', '09:00', '2024-05-11', '18:00', 'Épée', 'Homme', 'Régional', 'Compétition ouverte à tous les niveaux régionaux.', 'Senior', 'En cours', 1,1),
('Championnat M17', 'Tours', '456 Avenue de la Victoire', '2024-06-15', '08:30', '2024-06-15', '19:00', 'Fleuret', 'Femme', 'National', 'Championnat national pour la catégorie M17.', 'M17', NULL, 1,2),
('Championnat M17 Futur', 'Tours', '456 Avenue de la Victoire', '2026-06-15', '08:30', '2026-06-15', '19:00', 'Fleuret', 'Femme', 'National', 'Championnat national pour la catégorie M17.', 'M17', NULL, 0,6),
('Open de Blois', 'Blois', '1 Rue de la Halle', '2025-09-20', '09:00', '2025-09-21', '17:00', 'Sabre', 'Homme', 'National', 'Open national de sabre masculin.', 'Senior', NULL, 0, 7),
('Circuit National M20', 'Paris', '2 Avenue de la Porte', '2025-10-11', '08:00', '2025-10-12', '18:00', 'Épée', 'Femme', 'National', 'Étape du circuit national M20 épée.', 'M20', NULL, 0, 8),
('Tournoi des Ducs', 'Bourges', '3 Place Séraucourt', '2025-11-08', '10:00', '2025-11-08', '16:00', 'Fleuret', 'Femme', 'Régional', 'Tournoi amical fleuret féminin.', 'Senior', NULL, 0, 9),
('Challenge de Noël M15', 'Orléans', '123 Rue du Sport', '2025-12-13', '09:30', '2025-12-13', '17:30', 'Sabre', 'Homme', 'Régional', 'Compétition pour les jeunes sabreurs.', 'M15', NULL, 0, 10),
('Coupe de la Nouvelle Année', 'Tours', '456 Avenue de la Victoire', '2026-01-10', '09:00', '2026-01-11', '18:00', 'Épée', 'Homme', 'Régional', 'Première compétition de l''année.', 'Senior', NULL, 0, 11),
('Tournoi de la Chandeleur', 'Vierzon', '4 Rue de la Paix', '2024-02-03', '09:00', '2024-02-04', '17:00', 'Fleuret', 'Femme', 'Régional', 'Tournoi régional de début d''année.', 'M17', 'Terminé', 1, 12),
('Grand Prix de Printemps', 'Chartres', '5 Boulevard de la Liberté', '2024-03-22', '08:30', '2024-03-23', '19:00', 'Sabre', 'Homme', 'National', 'Grand prix national de sabre.', 'Senior', 'Terminé', 1, 13),
('Critérium M13', 'Châteauroux', '6 Avenue du Stade', '2024-04-12', '10:00', '2024-04-12', '16:00', 'Épée', 'Femme', 'Régional', 'Critérium pour les jeunes épéistes.', 'M13', 'Terminé', 1, 14),
('Mémorial Jean Moulin', 'Montargis', '7 Rue de la Résistance', '2023-11-11', '09:00', '2023-11-11', '18:00', 'Épée', 'Homme', 'Régional', 'Tournoi commémoratif toutes armes.', 'M17,M20,Senior', 'Terminé', 1, 15),
('Tournoi d''Automne M20', 'Orléans', '123 Rue du Sport', '2025-09-27', '09:00', '2025-09-28', '18:00', 'Fleuret', 'Homme', 'Régional', 'Tournoi de début de saison M20 fleuret.', 'M20', NULL, 0, 27),
('Challenge M13/M15', 'Blois', '1 Rue de la Halle', '2026-02-07', '10:00', '2026-02-07', '17:00', 'Sabre', 'Femme', 'Régional', 'Compétition amicale pour M13 et M15.', 'M13,M15', NULL, 0, 28),
('Coupe de Pâques Senior', 'Tours', '456 Avenue de la Victoire', '2026-04-04', '08:30', '2026-04-05', '19:00', 'Épée', 'Femme', 'Régional', 'Compétition épée dames senior.', 'Senior,Vétéran', NULL, 0, 29),
('Circuit National Vétérans', 'Paris', '2 Avenue de la Porte', '2025-05-01', '09:00', '2025-05-01', '18:00', 'Fleuret', 'Homme', 'National', 'Étape nationale pour les vétérans.', 'Vétéran', 'Terminé', 1, 30);


-- Insertion des entraînements (existants)
INSERT INTO ENTRAINEMENT (jourEN, villeEN, adresseEN, dateEN, heureDebutEN, heureFinEN, typeArmeEN, niveauEN, idEvent) VALUES
('Lundi', 'Blois', '5 rue de la salle', '2025-11-10', '18:00', '20:00', 'Sabre', 'Tous', 3),
('Mardi', 'Orléans', 'Gymnase A', '2025-11-11', '18:00', '20:00', 'Fleuret', 'M13,M15', 31),
('Jeudi', 'Orléans', 'Gymnase A', '2025-11-13', '19:00', '21:30', 'Épée', 'M17,M20,Senior', 32);


-- Insertion des réunions (existante)
INSERT INTO REUNION (nomRE, villeRE, adresseRE, dateDebutRE, heureDebutRE, dateFinRE, heureFinRE, nbParticipantsRE, typeReunionRE, rapportRE, niveauRE, idEvent) VALUES
('AG Annuelle', 'Blois', '5 rue de la salle', '2024-09-05', '19:00', '2024-09-05', '21:00', 10050, 'Assemblée', 'Rapport annuel des activités et finances.', 'Tous', 4),
('Réunion Comité Directeur', 'Orléans', 'Salle du Club', '2025-11-15', '20:00', '2025-11-15', '22:00', 8, 'Comité', 'Préparation budget 2026 et calendrier.', 'Comité', 33),
('Réunion Bénévoles Fête du Club', 'Orléans', 'Salle du Club', '2024-06-20', '19:00', '2024-06-20', '20:00', 15, 'Organisation', 'Répartition des tâches pour la fête du 6 juillet.', 'Tous', 34),
('Réunion Entraîneurs', 'Orléans', 'Stade Omnisports', '2024-09-10', '18:30', '2024-09-10', '20:30', 12, 'Technique', 'Mise au point planning entraînements.', 'Coachs', 35),
('Commission Sponsoring', 'Blois', '5 rue de la salle', '2025-01-20', '19:30', '2025-01-20', '21:30', 5, 'Finance', 'Recherche de nouveaux partenaires 2025.', 'Comité', 36),
('Réunion Parents U15', 'Orléans', 'Salle du Club', '2024-09-15', '18:00', '2024-09-15', '19:30', 45, 'Information', 'Présentation de la saison et déplacements.', 'Tous', 37),
('Bilan Mi-Saison', 'Orléans', 'Salle du Club', '2025-02-10', '20:00', '2025-02-10', '22:00', 10, 'Comité', 'Analyse des résultats sportifs intermédiaires.', 'Comité', 38),
('Préparation Tournoi Printemps', 'Blois', 'Centre Sportif', '2025-03-05', '19:00', '2025-03-05', '20:30', 8, 'Organisation', 'Logistique et réservation des arbitres.', 'Bénévoles', 39),
('Vœux du Président', 'Orléans', 'Salle des Fêtes', '2026-01-10', '19:00', '2026-01-10', '22:00', 120, 'Cérémonie', 'Présentation des vœux et galette des rois.', 'Tous', 40),
('Point Budget Prévisionnel', 'Blois', '5 rue de la salle', '2026-02-15', '18:30', '2026-02-15', '20:30', 6, 'Finance', 'Ajustement du budget pour la fin de saison.', 'Comité', 41),
('Réunion Fin de Saison', 'Orléans', 'Salle du Club', '2026-05-20', '19:30', '2026-05-20', '21:00', 30, 'Organisation', 'Organisation du barbecue de fin d''année.', 'Bénévoles', 42),
('Assemblée Générale Extraordinaire', 'Orléans', 'Stade Omnisports', '2026-06-15', '20:00', '2026-06-15', '22:30', 90, 'Assemblée', 'Vote pour le changement de statuts du club.', 'Tous', 43);


-- Insertion des événements de club (existants)
INSERT INTO EVENTCLUB (NomEV, villeEV, adresseEV, dateDebutEV, heureDebutEV, dateFinEV, heureFinEV, nbParticipantEV, descriptionEV, niveauxEV, passeeEV, idEvent) VALUES
-- 6 événements passés
('Fête du Club 2023', 'Orléans', '789 Boulevard de la Fête', '2023-07-01', '12:00', '2023-07-01', '22:00', 100, 'Journée festive pour tous les membres et leurs familles.', 'Tous', 1, 5),
('Stage de Pâques', 'Orléans', 'Gymnase A', '2024-04-15', '09:00', '2024-04-19', '17:00', 20, 'Stage intensif toutes armes pour les jeunes.', 'M13,M15,M17', 1, 16),
('Portes Ouvertes', 'Orléans', 'Gymnase A', '2023-09-09', '10:00', '2023-09-09', '17:00', 50, 'Journée découverte de l''escrime pour le public.', 'Tous', 1, 17),
('Téléthon Escrime', 'Orléans', 'Place du Martroi', '2023-12-02', '10:00', '2023-12-02', '18:00', 150, 'Démonstrations et initiations au profit du Téléthon.', 'Tous', 1, 18),
('Galette des Rois', 'Salle du Club', 'Orléans', '2024-01-13', '16:00', '2024-01-13', '18:00', 60, 'Partage de la galette des rois avec les membres.', 'Tous', 1, 19),
('Tournoi Interne de Noël', 'Gymnase A', 'Orléans', '2023-12-16', '14:00', '2023-12-16', '18:00', 40, 'Petit tournoi amical pour finir l''année.', 'Tous', 1, 20),
('Fête du Club 2024', 'Orléans', '789 Boulevard de la Fête', '2024-07-06', '12:00', '2024-07-06', '22:00', 100, 'Journée festive pour tous les membres et leurs familles.', 'Tous', 1, 21),
('Stage d''été', 'Orléans', 'Gymnase A', '2024-08-19', '09:00', '2024-08-23', '17:00', 25, 'Stage de pré-saison pour tous les compétiteurs.', 'M15,M17,M20,Senior', 1, 22),
('Journée Portes Ouvertes 2024', 'Orléans', 'Gymnase A', '2024-09-07', '10:00', '2024-09-07', '17:00', 50, 'Venez découvrir l''escrime et notre club !', 'Tous', 1, 23),
('Sortie Club à Chambord', 'Chambord', 'Château de Chambord', '2024-10-05', '09:00', '2024-10-05', '18:00', 40, 'Visite du château et pique-nique.', 'Tous', 1, 24),
('Soirée Halloween', 'Salle du Club', 'Orléans', '2024-10-31', '19:00', '2024-10-31', '23:00', 50, 'Soirée déguisée pour les membres.', 'Tous', 1, 25),
('Tournoi Interne de la Toussaint', 'Gymnase A', 'Orléans', '2024-11-02', '14:00', '2024-11-02', '18:00', 40, 'Tournoi amical ouvert à tous les membres.', 'Tous', 1, 26),
('Arbre de Noël 2025', 'Orléans', 'Salle du Club', '2025-12-20', '15:00', '2025-12-20', '18:00', 70, 'Goûter de Noël, venue du Père Noël et petits cadeaux.', 'Tous', 0, 35),
('Stage de Février 2026', 'Orléans', 'Gymnase A', '2026-02-16', '09:00', '2026-02-20', '17:00', 30, 'Stage de perfectionnement multi-armes.', 'M13,M15,M17', 0, 36),
('Nettoyage de Printemps', 'Orléans', 'Salle du Club', '2025-04-05', '09:00', '2025-04-05', '13:00', 25, 'Matinée rangement et nettoyage du matériel et de la salle.', 'Tous', 1, 37);


-- Insertion des participations aux événements (corrigée)
INSERT INTO PARTICIPER (idEvent, idMembre) VALUES
(1, 20), -- Jules (Senior/H) participe au Tournoi Régional (Senior)
(3, 1), -- Jean participe à l'entraînement
(3, 2), -- Marie participe à l'entraînement
(4, 1), -- Jean participe à l'AG (Réunion)
(5, 1), -- Jean participe à la Fête du Club 2023 (passé)
(5, 2), -- Marie participe à la Fête du Club 2023 (passé)
(21, 1), -- Jean participe à la Fête du Club 2024 (passé)
(21, 2), -- Marie participe à la Fête du Club 2024 (passé)
(21, 3), -- Paul participe à la Fête du Club 2024 (passé)
(28, 10), -- Lucas (M15/H) s'inscrit au Challenge M13/M15 (Mixte)
(29, 12), -- Alice (Senior/F) s'inscrit à la Coupe de Pâques (Femme/Senior,Vétéran)
(29, 7),  -- Pascale (Vétéran/F) s'inscrit à la Coupe de Pâques (Femme/Senior,Vétéran)
(7, 1),   -- Jean (Senior/H) s'inscrit à l'Open de Blois (Homme/Senior)
(31, 11), -- Chloé (M13) à l'entraînement Fleuret M13/M15
(32, 1),  -- Jean (Senior) à l'entraînement Épée M17/M20/Senior
(32, 12), -- Alice (Senior) à l'entraînement Épée M17/M20/Senior
(33, 4), (33, 5), (33, 6), (33, 7), (33, 8),
(37, 1), (37, 2), (37, 4),
(32, 14), -- Hugo (M17/H) -> Entraînement Épée (idEvent 32: M17,M20,Senior)
(6, 15),  -- Manon (M17/F) -> Champ M17 Futur (idEvent 6: M17/F)
(36, 15), -- Manon (M17/F) -> Stage Février 2026 (idEvent 36: M13,M15,M17)
(28, 16), -- Léo (M13/H) -> Challenge M13/M15 (idEvent 28: M13,M15/Mixte)
(31, 16), -- Léo (M13/H) -> Entraînement Fleuret (idEvent 31: M13,M15)
(10, 17), -- Camille (M15/F) -> Challenge Noël M15 (idEvent 10: M15/Mixte)
(28, 17), -- Camille (M15/F) -> Challenge M13/M15 (idEvent 28: M13,M15/Mixte)
(36, 17), -- Camille (M15/F) -> Stage Février 2026 (idEvent 36: M13,M15,M17)
(31, 18), -- Arthur (M13/H) -> Entraînement Fleuret (idEvent 31: M13,M15)
(28, 18), -- Arthur (M13/H) -> Challenge M13/M15 (idEvent 28: M13,M15/Mixte)
(32, 19), -- Zoé (M20/F) -> Entraînement Épée (idEvent 32: M17,M20,Senior)
(7, 20),  -- Jules (Senior/H) -> Open de Blois (idEvent 7: Senior/H)
(11, 20), -- Jules (Senior/H) -> Coupe Nouvelle Année (idEvent 11: Senior/H)
(9, 21),  -- Emma (Senior/F) -> Tournoi des Ducs (idEvent 9: Senior/F)
(29, 21), -- Emma (Senior/F) -> Coupe Pâques Senior (idEvent 29: Senior,Vétéran/F)
(29, 23), -- Louise (Vétéran/F) -> Coupe Pâques Senior (idEvent 29: Senior,Vétéran/F)
(10, 25), -- Rose (M15/F) -> Challenge Noël M15 (idEvent 10: M15/Mixte)
(31, 25), -- Rose (M15/F) -> Entraînement Fleuret (idEvent 31: M13,M15)
(27, 26), -- Raphaël (M20/H) -> Tournoi Automne M20 (idEvent 27: M20/H)
(8, 26),  -- Raphaël (M20/H) -> Circuit National M20 (idEvent 8: M20/Mixte)
(8, 27),  -- Jade (M20/F) -> Circuit National M20 (idEvent 8: M20/Mixte)
(7, 28),  -- Louis (Senior/H) -> Open de Blois (idEvent 7: Senior/H)
(9, 29),  -- Ambre (Senior/F) -> Tournoi des Ducs (idEvent 9: Senior/F)
(28, 30), -- Nathan (M13/H) -> Challenge M13/M15 (idEvent 28: M13,M15/Mixte)
(11, 32), -- Mohamed (Senior/H) -> Coupe Nouvelle Année (idEvent 11: Senior/H)
(29, 33); -- Inès (Senior/F) -> Coupe Pâques Senior (idEvent 29: Senior,Vétéran/F)




-- Insertion des résultats (existants)
INSERT INTO RESULTAT (resultat, dateRE, typeArmeRE, typeCompeteRE, idCompetition, idMembre) VALUES
(2, '2024-05-11', 'Épée', 'Régional', 1, 1),
(16, '2024-06-15', 'Fleuret', 'National', 2, 2),
(5, '2024-02-04', 'Fleuret', 'Régional', 9, 2),
(12, '2024-03-23', 'Sabre', 'National', 10, 1),
(3, '2024-04-12', 'Épée', 'Régional', 11, 2),
(22, '2025-05-01', 'Sabre', 'National', 16, 6),
(8, '2025-05-01', 'Fleuret', 'National', 16, 7);


-- Tables de liaison pour les résultats (AVOIR, RESULTER) (existantes)
INSERT INTO AVOIR (idResultat, idMembre) VALUES
(1, 1),
(2, 2),
(3, 2),
(4, 1),
(5, 2),
(6, 6),
(7, 7);

INSERT INTO RESULTER (idResultat, idCompetition) VALUES
(1, 1),
(2, 2),
(3, 9),
(4, 10),
(5, 11),
(6, 16),
(7, 16);


-- Insertion des formulaires de contact (existants)
INSERT INTO FORMULAIRE_CONTACT (typeFC, sujetFC, mailFC, descriptionFC, dateFC, idMembre, idAdmin) VALUES
('Question', 'Horaires', 'visiteur@email.com', 'Quels sont les horaires pour les débutants ?', '2024-04-10', NULL, 1),
('Signalement', 'Matériel défectueux', 'jean.dupont@email.com', 'Le fil de corps n°12 est cassé au niveau de la prise.', '2025-10-28', 1, 1),
('Question', 'Stage de Février', 'lucas.petit@email.com', 'Le stage de février 2026 est-il ouvert aux M15 ?', '2025-11-06', 9, 1),
('Demande', 'Photo de profil', 'visiteur.externe@email.com', 'Pouvez-vous supprimer ma photo de la galerie ?', '2025-11-01', NULL, 1),
('Question', 'Tarifs famille', 'famille.martin@email.com', 'Proposez-vous des réductions pour les familles nombreuses ?', '2025-09-15', NULL, 1),
('Signalement', 'Vestiaire', 'paul.martin@email.com', 'La porte du vestiaire hommes ne ferme plus correctement.', '2025-10-02', 3, 1),
('Demande', 'Facture', 'jean.dupont@email.com', 'Pourrais-je recevoir une facture pour mon adhésion ?', '2025-10-05', 1, 1),
('Question', 'Compétition M13', 'leo.david@email.com', 'Est-ce que je peux participer à la compétition M15 le mois prochain ?', '2025-11-12', 16, 1),
('Demande', 'Stage Toussaint', 'parents.hugo@email.com', 'Reste-t-il des places pour le stage de la Toussaint ?', '2025-10-20', NULL, 1),
('Question', 'Matériel', 'nouveau@email.com', 'Faut-il acheter son propre matériel dès la première année ?', '2025-09-05', NULL, 1),
('Signalement', 'Lumière piste 3', 'louis.perrin@email.com', 'L\'éclairage au dessus de la piste 3 clignote.', '2025-11-10', 28, 1),
('Demande', 'Attestation', 'manon.roux@email.com', 'J\'ai besoin d\'une attestation de pratique pour mon CE.', '2025-11-15', 15, 1),
('Question', 'Bénévolat', 'benevole@email.com', 'Comment devenir bénévole pour la prochaine compétition ?', '2025-10-30', NULL, 1),
('Demande', 'Remboursement', 'ancien@email.com', 'Je me suis blessé, est-il possible de se faire rembourser une partie de la cotisation ?', '2025-11-01', NULL, 1),
('Signalement', 'Propreté', 'rose.barbier@email.com', 'Les douches n\'étaient pas très propres hier soir.', '2025-11-18', 25, 1),
('Question', 'Horaires vacances', 'zoe.fournier@email.com', 'Y a-t-il entraînement pendant les vacances de Noël ?', '2025-12-10', 19, 1),
('Demande', 'Partenariat', 'sponsor@entreprise.com', 'Nous souhaiterions sponsoriser votre club.', '2025-09-20', NULL, 1),
('Question', 'Catégorie âge', 'parent.curieux@email.com', 'Mon fils a 7 ans, peut-il commencer l\'escrime ?', '2025-09-01', NULL, 1),
('Signalement', 'Site web', 'geek@email.com', 'Il y a une faute d\'orthographe sur la page d\'accueil.', '2025-11-20', NULL, 1),
('Demande', 'Essai', 'sportif@email.com', 'Est-il possible de faire une séance d\'essai gratuite ?', '2025-09-10', NULL, 1),
('Question', 'Tenue', 'chloe.moreau@email.com', 'Quelle taille de veste dois-je commander ?', '2025-10-15', 10, 1),
('Signalement', 'Parking', 'jules.girard@email.com', 'Le portail du parking est resté ouvert cette nuit.', '2025-11-22', 20, 1);

-- Tables de liaison pour les formulaires (REPONDRE, REMPLIR) (existantes)
INSERT INTO REPONDRE (idFormulaire, idAdmin) VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 1),
(5, 1);

INSERT INTO REMPLIR (idFormulaire, idMembre) VALUES
(2, 2),
(3, 1),
(4, 9);


-- Insertion des inscriptions en attente (existante)
INSERT INTO INSCRIPTION (mailInscr, nomI, prenomI, ddnI, mdpI, sexeI,dateInscription) VALUES
('nouveau.membre@email.com', 'Nouveau', 'Alice', '2000-01-01', 'mdpsecure', 'Femme', '2025-10-23'),
('sam.leroy@email.com', 'Leroy', 'Samuel', '1998-12-10', 'mdpSam1', 'Homme', '2025-11-05'),
('emma.g@email.com', 'Garnier', 'Emma', '2011-02-05', 'mdpEmma2', 'Femme', '2025-11-07'),
('julie.faure@email.com', 'Faure', 'Julie', '2005-06-15', 'mdpJulie1', 'Femme', '2025-11-10'),
('thomas.blanc@email.com', 'Blanc', 'Thomas', '2012-09-20', 'mdpThomas2', 'Homme', '2025-11-12'),
('sophie.martin@email.com', 'Martin', 'Sophie', '1990-03-30', 'mdpSophie3', 'Femme', '2025-11-15'),
('luc.simon@email.com', 'Simon', 'Luc', '2001-12-05', 'mdpLuc4', 'Homme', '2025-11-18'),
('clara.michel@email.com', 'Michel', 'Clara', '2014-07-14', 'mdpClara5', 'Femme', '2025-11-20'),
('lucas.m@email.com', 'Martin', 'Lucas', '2005-03-12', 'mdpLucas1', 'Homme', '2025-11-21'),
('sophie.d@email.com', 'Dubois', 'Sophie', '1995-07-22', 'mdpSophie2', 'Femme', '2025-11-22'),
('thomas.b@email.com', 'Bernard', 'Thomas', '2010-11-30', 'mdpThomas3', 'Homme', '2025-11-23'),
('lea.p@email.com', 'Petit', 'Léa', '2000-09-05', 'mdpLea4', 'Femme', '2025-11-24'),
('nathan.r@email.com', 'Robert', 'Nathan', '2012-01-15', 'mdpNathan5', 'Homme', '2025-11-25'),
('manon.r@email.com', 'Richard', 'Manon', '2008-05-20', 'mdpManon6', 'Femme', '2025-11-26'),
('leo.d@email.com', 'Durand', 'Léo', '2015-12-10', 'mdpLeo7', 'Homme', '2025-11-27'),
('camille.v@email.com', 'Vidal', 'Camille', '1992-04-18', 'mdpCamille8', 'Femme', '2025-11-28'),
('hugo.m@email.com', 'Morel', 'Hugo', '2003-08-25', 'mdpHugo9', 'Homme', '2025-11-29'),
('chloe.l@email.com', 'Lambert', 'Chloé', '2014-02-14', 'mdpChloe10', 'Femme', '2025-11-30'),
('antoine.r@email.com', 'Renard', 'Antoine', '2000-05-20', 'mdpAntoine11', 'Homme', '2025-12-01'),
('sarah.b@email.com', 'Boucher', 'Sarah', '1998-11-15', 'mdpSarah12', 'Femme', '2025-12-02'),
('maxime.l@email.com', 'Lefevre', 'Maxime', '2010-02-28', 'mdpMaxime13', 'Homme', '2025-12-03'),
('elise.m@email.com', 'Mercier', 'Elise', '2013-07-10', 'mdpElise14', 'Femme', '2025-12-04'),
('alexandre.d@email.com', 'Dumont', 'Alexandre', '1995-09-05', 'mdpAlex15', 'Homme', '2025-12-05'),
('charlotte.g@email.com', 'Girard', 'Charlotte', '2005-12-12', 'mdpCharlotte16', 'Femme', '2025-12-06'),
('nicolas.p@email.com', 'Payet', 'Nicolas', '1980-03-30', 'mdpNicolas17', 'Homme', '2025-12-07'),
('audrey.f@email.com', 'Fontaine', 'Audrey', '1992-06-18', 'mdpAudrey18', 'Femme', '2025-12-08'),
('benjamin.r@email.com', 'Robin', 'Benjamin', '2008-01-25', 'mdpBenjamin19', 'Homme', '2025-12-09'),
('mathilde.s@email.com', 'Sanchez', 'Mathilde', '2011-08-14', 'mdpMathilde20', 'Femme', '2025-12-10');


-- Insertion des modifications en attente (existante)
INSERT INTO MODIFICATION (nomModif, prenomModif, emailModif, sexeModif, ddnModif, dateModif, idMembre) VALUES
('Durand', 'Marie', 'marie.durand45@email.com', 'Homme', '2008-10-10', '2025-10-20', 2),
('Dupont', 'Jean', 'jean.dupont.pro@email.com', 'Homme', '1995-05-20', '2025-11-01', 1),
('Martin', 'Paul', 'paul.martin.new@email.com', 'Homme', '2015-03-25', '2025-11-05', 3),
('Eche', 'Régis', 'regis.president@email.com', 'Homme', '1975-02-07', '2025-11-08', 4),
('Petit', 'Lucas', 'lucas.petit@email.com', 'Homme', '2010-06-16', '2025-11-12', 9),
('Robert-Deval', 'Tom', 'tom.robert@email.com', 'Homme', '1985-11-30', '2025-11-15', 12),
('Girard', 'Jules', 'jules.girard.pro@email.com', 'Homme', '2004-05-10', '2025-11-20', 20),
('Bonnet', 'Emma', 'emma.bonnet.new@email.com', 'Femme', '1999-02-18', '2025-11-21', 21),
('Dubois', 'Gabriel', 'gabriel.dubois.pro@email.com', 'Homme', '1980-12-05', '2025-11-22', 22),
('Leclerc', 'Louise', 'louise.leclerc.perso@email.com', 'Femme', '1975-09-08', '2025-11-23', 23),
('Meyer', 'Adam', 'adam.meyer.parent@email.com', 'Homme', '2016-01-02', '2025-11-24', 24),
('Barbier', 'Rose', 'rose.barbier.new@email.com', 'Femme', '2010-06-19', '2025-11-25', 25),
('Brun', 'Raphaël', 'raphael.brun.etu@email.com', 'Homme', '2007-03-22', '2025-11-26', 26),
('Guerin', 'Jade', 'jade.guerin.pro@email.com', 'Femme', '2006-10-14', '2025-11-27', 27),
('Perrin', 'Louis', 'louis.perrin.new@email.com', 'Homme', '2002-04-01', '2025-11-28', 28),
('Mercier', 'Ambre', 'ambre.mercier.art@email.com', 'Femme', '1995-07-07', '2025-11-29', 29),
('Chevalier', 'Nathan', 'nathan.chevalier.parent@email.com', 'Homme', '2013-08-11', '2025-11-30', 30),
('Lemoine', 'Anna', 'anna.lemoine.new@email.com', 'Femme', '2015-05-05', '2025-12-01', 31),
('Benali', 'Mohamed', 'mohamed.benali.pro@email.com', 'Homme', '1990-11-30', '2025-12-02', 32),
('Roy', 'Inès', 'ines.roy.perso@email.com', 'Femme', '1988-01-20', '2025-12-03', 33),
('Dupont', 'Jean', 'jean.dupont.v2@email.com', 'Homme', '1995-05-20', '2025-12-04', 1),
('Durand', 'Marie', 'marie.durand.v2@email.com', 'Femme', '2008-08-10', '2025-12-05', 2),
('Martin', 'Paul', 'paul.martin.v2@email.com', 'Homme', '2015-03-25', '2025-12-06', 3),
('Eche', 'Régis', 'regis.eche.v2@email.com', 'Homme', '1975-02-07', '2025-12-07', 4),
('Marquet', 'Dominique', 'dom.mar.new@email.com', 'Homme', '1974-02-07', '2025-12-08', 5),
('Deladeriere', 'Bernard', 'ber.del.new@email.com', 'Homme', '1976-02-07', '2025-12-09', 6),
('Lhomme', 'Pascale', 'pas.lhm.new@email.com', 'Femme', '1978-02-07', '2025-12-10', 7);



-- Insertion des notifications (existantes)
INSERT INTO NOTIFS (typeN, sourceN, lue, timestamp, link, idMembre, idAdmin) VALUES
('Demande Inscription', 'Formulaire', 0, '2025-11-20 10:00:00', '/gerer_inscriptions/', NULL, 1),
('Nouveau Résultat', 'Compétition', 0, '2025-11-21 14:30:00', '/resultat_membre/', 1, NULL),
('Nouveau Résultat', 'Compétition', 1, '2025-11-21 14:35:00', '/resultat_membre/', 2, NULL),
('Evenement', 'Nouvel événement : Arbre de Noël 2025', 0, '2025-12-01 09:00:00', '/evenement_club/', 1, NULL),
('Evenement', 'Nouvel événement : Arbre de Noël 2025', 1, '2025-12-01 09:00:00', '/evenement_club/', 2, NULL),
('Admin', 'Maintenance du site prévue le 10/11', 0, '2025-11-09 18:00:00', NULL, 1, 1);


-- Tables de liaison pour les notifications (RECEVOIRA, RECEVOIRM) (existantes)
INSERT INTO RECEVOIRA (idNotifs, idAdmin) VALUES
(1, 1);

INSERT INTO RECEVOIRM (idNotifs, idMembre) VALUES
(2, 1),
(3, 2);

-- Ajouts de liaisons notifications (existantes)
INSERT INTO RECEVOIRM (idNotifs, idMembre) VALUES
(4, 1),
(5, 2);

INSERT INTO RECEVOIRA (idNotifs, idAdmin) VALUES
(6, 1);


-- Insertion des images (existantes)
INSERT INTO IMAGEAPP (urlI, prive, alt) VALUES
('/static/images/compet_1.jpg', 0, 'Tournoi régional épée'),
('/static/images/fete_club.png', 0, 'Affiche fête du club');

-- Ajouts d'images (existantes)
INSERT INTO IMAGEAPP (urlI, prive, alt) VALUES
('/static/images/stage_paques.jpg', 0, 'Stage de Pâques 2024'),
('/static/images/podium_gp_printemps.jpg', 0, 'Podium GP Printemps'),
('/static/images/entrainement_jeunes.jpg', 0, 'Entraînement M13/M15'),
('/static/images/logo_app.png', 0, 'Logo Cercle Escrime');


-- Liaison des images aux compétitions et événements (existantes)
INSERT INTO IMAGERC (idImage, idCompetition) VALUES (1, 1);
INSERT INTO IMAGERE (idImage, idEventClub) VALUES (2, 1);

-- Ajouts de liaisons images (existantes)
INSERT INTO IMAGERE (idImage, idEventClub) VALUES (3, 2);
INSERT INTO IMAGERC (idImage, idCompetition) VALUES (4, 10);


-- Insertion dans INFORMATION (existante)
INSERT INTO INFORMATION (dateIN, heureIN, titreIN, contenuIN) VALUES
('2023-08-15', '10:27','Reception des nouveaux gants','Nous vous informons que les gants que nous attendions sont là'),
('2025-09-01', '09:00', 'Reprise des entraînements', 'La saison 2025-2026 commence ! Les entraînements reprennent aux horaires habituels dès cette semaine.'),
('2025-10-30', '14:00', 'Fermeture Toussaint', 'Le gymnase sera fermé le 1er Novembre. Les entraînements du vendredi sont annulés.'),
('2025-11-05', '11:00', 'Nouvelle boutique club', 'La nouvelle boutique en ligne du club est ouverte. Commandez vos tenues et équipements !');


-- Liaison des images aux informations (existante)
INSERT INTO IMAGERIN (idImage, idInformation) VALUES (1, 1);

-- Ajouts de liaisons images-informations (existantes)
INSERT INTO IMAGERIN (idImage, idInformation) VALUES (5, 2), (6, 4);


-- Insertion dans PRESSE (existante)
INSERT INTO PRESSE (dateP, heureP, titreP, contenuP,lienP) VALUES
('2025-12-15','15:45','WHITELIST','Compléter votre collection en achetant des booster !!!','https://whitelist.fr/'),
('2025-12-15','15:45','JOBLIFE',"Venez soutenir l'équipe JOBLIFE !!!",'https://joblife.fr/');

-- Insertion des tarifs d'adhésion
INSERT INTO TARIF (nom, prix, description, categorie) VALUES 
('Initiation', 225, 'Jeunes et adultes débutants 1ère année', 'Adhesion'),
('Scolaires', 235, 'Avec certificat de scolarité', 'Adhesion'),
('Étudiants', 235, 'Université ou grandes écoles', 'Adhesion'),
('Autres adultes', 255, 'Tarif standard adulte', 'Adhesion');

-- Insertion du tarif matériel
INSERT INTO TARIF (nom, prix, description, categorie) VALUES 
('Location annuelle complète', 45, 'Veste, pantalon et sous-cuirasse fournis pour l''année. Le gant n''est pas fourni.', 'Materiel');

-- Insertion des horaires du Mardi
INSERT INTO HORAIRE (jour, heureDebut, heureFin, activite, details) VALUES 
('Mardi', '19h00', '21h15', 'Entraînement Épée', 'M17, M20, seniors, vétérans');

-- Insertion des horaires du Mercredi
INSERT INTO HORAIRE (jour, heureDebut, heureFin, activite, details) VALUES 
('Mercredi', '17h00', '18h00', 'Initiation Fleuret', 'Débutants jeunes filles et garçons (8 à 12 ans)'),
('Mercredi', '18h15', '19h45', 'Entraînement Fleuret ou Épée', 'M11 à M20'),
('Mercredi', '19h45', '21h15', 'Entraînement – Escrime loisir épée', 'Réservé aux débutants ados et adultes H&F');

-- Insertion des horaires du Vendredi
INSERT INTO HORAIRE (jour, heureDebut, heureFin, activite, details) VALUES 
('Vendredi', '19h00', '21h15', 'Entraînement Épée', 'Entraînement libre M17 à vétérans');

-- Réactiver la vérification des clés étrangères
SET FOREIGN_KEY_CHECKS=1;
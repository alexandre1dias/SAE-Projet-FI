-- Désactivation de la vérification des clés étrangères 
SET FOREIGN_KEY_CHECKS=0;

-- Insertion des administrateurs (avec idParamNotifAdmin initialement à NULL pour éviter la dépendance circulaire)
INSERT INTO ADMINISTRATEUR (emailA, mdpA, idParamNotifAdmin) VALUES
('admin@escrime.com', 'motdepasseadmin', NULL);

-- Insertion des paramètres de notification pour les administrateurs
INSERT INTO PARAMETRE_NOTIF_ADMIN (idParamNotifAdmin, formulaireDemandeSite, formulaireDemandeMail, formulaireQuestionSite, formulaireQuestionMail, formulaireSignalementSite, formulaireSignalementMail, demandeModifSite, demandeModifMail, demandeInscriptionSite, demandeInscriptionMail, idAdmin) VALUES
(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);

-- Mise à jour de l'administrateur pour lier ses paramètres de notification
UPDATE ADMINISTRATEUR SET idParamNotifAdmin = 1 WHERE idAdmin = 1;

-- Insertion des membres (avec idParamNotifMembre initialement à NULL)
INSERT INTO MEMBRE (nomM, prenomM, emailM, mdpM, date_inscription, sexeM, ddnM, statut, activite, idParamNotifMembre) VALUES
('Dupont', 'Jean', 'jean.dupont@email.com', 'mdp123', '2023-01-15', 'Homme', '1995-05-20', 'Membre', 1, NULL),
('Durand', 'Marie', 'marie.durand@email.com', 'mdp456', '2023-02-20', 'Femme', '2008-08-10', 'Membre', 1, NULL),
('Martin', 'Paul', 'paul.martin@email.com', 'mdp789', '2022-09-01', 'Homme', '2015-03-25', 'Ancien Membre', 0, NULL),
('Eche', 'Régis', 'regis.eche@email.com', 'mdp741', '2000-01-01', 'Homme', '1975-02-07','Président', 1, NULL),
('Dominique', 'MARQUET', 'dom.mar@email.com', 'mdp442', '2006-01-01', 'Homme', '1974-02-07','Vice-Président', 1, NULL),
('Bernard', 'DELADERIERE', 'ber.del@email.com', 'mdp5231', '1999-01-01', 'Homme', '1976-02-07','Trésorier Général', 1, NULL),
('Pascale', 'LHOMME', 'pas.lhm@email.com', 'mdp433', '2002-01-01', 'Femme', '1978-02-07','Secrétaire Générale', 1, NULL),
('Christophe', 'LECHOPIER', 'chr.lec@email.com', 'mdp541', '2005-01-01', 'Homme', '1969-02-07','Membre du Comité', 1, NULL);

-- Insertion des paramètres de notification pour les membres
INSERT INTO PARAMETRE_NOTIF_MEMBRE (eventInscriptionSite, evenementInscriptionMail, eventNouveauSite, eventNouveauMail, eventAnnulationSite, eventAnnulationMail, resultatNouveauSite, resultatNouveauMail, reponseFormulaireSite, reponseFormulaireMail, modifProfilSite, modifProfilMail, idMembre) VALUES
(1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1),
(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2),
(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3);

-- Mise à jour des membres pour lier leurs paramètres de notification
UPDATE MEMBRE SET idParamNotifMembre = 1 WHERE idMembre = 1;
UPDATE MEMBRE SET idParamNotifMembre = 2 WHERE idMembre = 2;
UPDATE MEMBRE SET idParamNotifMembre = 3 WHERE idMembre = 3;

-- Insertion des événements (table parente)
INSERT INTO EVENEMENT () VALUES
(), (), (), (), (), (),
-- Événements pour les compétitions
(), (), (), (), (), (), (), (), (),
-- Événements pour les eventclubs
(), (), (), (), (), (), (), (), (), (), ();

-- Insertion des compétitions
INSERT INTO COMPETITION (nomCO, villeCO, adresseCO, dateDebutCO, heureDebutCO, dateFinCO, heureFinCO, typeArmeCO, nbParticipantsCO, sexeCO, typeCompete, descriptionCO, niveauCO, classementCO,passeeCO, idEvent) VALUES
('Tournoi Régional', 'Orléans', '123 Rue du Sport', '2024-05-10', '09:00', '2024-05-11', '18:00', 'Épée', 64, 'Mixte', 'Régional', 'Compétition ouverte à tous les niveaux régionaux.', 'Senior', 'En cours', 1,1),
('Championnat M17', 'Tours', '456 Avenue de la Victoire', '2024-06-15', '08:30', '2024-06-15', '19:00', 'Fleuret', 32, 'Femme', 'National', 'Championnat national pour la catégorie M17.', 'M17', NULL, 1,2),
('Championnat M17 Futur', 'Tours', '456 Avenue de la Victoire', '2026-06-15', '08:30', '2026-06-15', '19:00', 'Fleuret', 32, 'Femme', 'National', 'Championnat national pour la catégorie M17.', 'M17', NULL, 0,6),
('Open de Blois', 'Blois', '1 Rue de la Halle', '2025-09-20', '09:00', '2025-09-21', '17:00', 'Sabre', 48, 'Homme', 'National', 'Open national de sabre masculin.', 'Senior', NULL, 0, 7),
('Circuit National M20', 'Paris', '2 Avenue de la Porte', '2025-10-11', '08:00', '2025-10-12', '18:00', 'Épée', 128, 'Mixte', 'National', 'Étape du circuit national M20 épée.', 'M20', NULL, 0, 8),
('Tournoi des Ducs', 'Bourges', '3 Place Séraucourt', '2025-11-08', '10:00', '2025-11-08', '16:00', 'Fleuret', 32, 'Femme', 'Régional', 'Tournoi amical fleuret féminin.', 'Senior', NULL, 0, 9),
('Challenge de Noël M15', 'Orléans', '123 Rue du Sport', '2025-12-13', '09:30', '2025-12-13', '17:30', 'Sabre', 64, 'Mixte', 'Régional', 'Compétition pour les jeunes sabreurs.', 'M15', NULL, 0, 10),
('Coupe de la Nouvelle Année', 'Tours', '456 Avenue de la Victoire', '2026-01-10', '09:00', '2026-01-11', '18:00', 'Épée', 50, 'Homme', 'Régional', 'Première compétition de l''année.', 'Senior', NULL, 0, 11),
('Tournoi de la Chandeleur', 'Vierzon', '4 Rue de la Paix', '2024-02-03', '09:00', '2024-02-04', '17:00', 'Fleuret', 40, 'Mixte', 'Régional', 'Tournoi régional de début d''année.', 'M17', 'Terminé', 1, 12),
('Grand Prix de Printemps', 'Chartres', '5 Boulevard de la Liberté', '2024-03-22', '08:30', '2024-03-23', '19:00', 'Sabre', 80, 'Homme', 'National', 'Grand prix national de sabre.', 'Senior', 'Terminé', 1, 13),
('Critérium M13', 'Châteauroux', '6 Avenue du Stade', '2024-04-12', '10:00', '2024-04-12', '16:00', 'Épée', 32, 'Femme', 'Départemental', 'Critérium pour les jeunes épéistes.', 'M13', 'Terminé', 1, 14),
('Mémorial Jean Moulin', 'Montargis', '7 Rue de la Résistance', '2023-11-11', '09:00', '2023-11-11', '18:00', 'Toutes', 90, 'Mixte', 'Régional', 'Tournoi commémoratif toutes armes.', 'Tous', 'Terminé', 1, 15);

-- Insertion des entraînements
INSERT INTO ENTRAINEMENT (jourEN, villeEN, adresseEN, dateEN, heureDebutEN, heureFinEN, typeArmeEN, niveauEN, idEvent) VALUES
('Lundi', 'Blois', '5 rue de la salle', '2024-04-29', '18:00', '20:00', 'Sabre', 'Tous', 3);

-- Insertion des réunions
INSERT INTO REUNION (nomRE, villeRE, adresseRE, dateDebutRE, heureDebutRE, dateFinRE, heureFinRE, nbParticipantsRE, typeReunionRE, rapportRE, niveauRE, idEvent) VALUES
('AG Annuelle', 'Blois', '5 rue de la salle', '2024-09-05', '19:00', '2024-09-05', '21:00', 10050, 'Assemblée', 'Rapport annuel des activités et finances.', 'Tous', 4);

-- Insertion des événements de club (6 passés, 6 à venir)
INSERT INTO EVENTCLUB (NomEV, villeEV, adresseEV, dateDebutEV, heureDebutEV, dateFinEV, heureFinEV, nbParticipantEV, descriptionEV, niveauxEV, passeeEV, idEvent) VALUES
-- 6 événements passés
('Fête du Club 2023', 'Orléans', '789 Boulevard de la Fête', '2023-07-01', '12:00', '2023-07-01', '22:00', 100, 'Journée festive pour tous les membres et leurs familles.', 'Tous', 1, 5),
('Stage de Pâques', 'Orléans', 'Gymnase A', '2024-04-15', '09:00', '2024-04-19', '17:00', 20, 'Stage intensif toutes armes pour les jeunes.', 'M13,M15,M17', 1, 16),
('Portes Ouvertes', 'Orléans', 'Gymnase A', '2023-09-09', '10:00', '2023-09-09', '17:00', 50, 'Journée découverte de l''escrime pour le public.', 'Tous', 1, 17),
('Téléthon Escrime', 'Orléans', 'Place du Martroi', '2023-12-02', '10:00', '2023-12-02', '18:00', 150, 'Démonstrations et initiations au profit du Téléthon.', 'Tous', 1, 18),
('Galette des Rois', 'Salle du Club', 'Orléans', '2024-01-13', '16:00', '2024-01-13', '18:00', 60, 'Partage de la galette des rois avec les membres.', 'Tous', 1, 19),
('Tournoi Interne de Noël', 'Gymnase A', 'Orléans', '2023-12-16', '14:00', '2023-12-16', '18:00', 40, 'Petit tournoi amical pour finir l''année.', 'Tous', 1, 20),
-- 6 événements à venir
('Fête du Club 2024', 'Orléans', '789 Boulevard de la Fête', '2024-07-06', '12:00', '2024-07-06', '22:00', 100, 'Journée festive pour tous les membres et leurs familles.', 'Tous', 0, 21),
('Stage d''été', 'Orléans', 'Gymnase A', '2024-08-19', '09:00', '2024-08-23', '17:00', 25, 'Stage de pré-saison pour tous les compétiteurs.', 'M15,M17,M20,Senior', 0, 22),
('Journée Portes Ouvertes 2024', 'Orléans', 'Gymnase A', '2024-09-07', '10:00', '2024-09-07', '17:00', 50, 'Venez découvrir l''escrime et notre club !', 'Tous', 0, 23),
('Sortie Club à Chambord', 'Chambord', 'Château de Chambord', '2024-10-05', '09:00', '2024-10-05', '18:00', 40, 'Visite du château et pique-nique.', 'Tous', 0, 24),
('Soirée Halloween', 'Salle du Club', 'Orléans', '2024-10-31', '19:00', '2024-10-31', '23:00', 50, 'Soirée déguisée pour les membres.', 'Tous', 0, 25),
('Tournoi Interne de la Toussaint', 'Gymnase A', 'Orléans', '2024-11-02', '14:00', '2024-11-02', '18:00', 40, 'Tournoi amical ouvert à tous les membres.', 'Tous', 0, 26);

-- Insertion des participations aux événements
INSERT INTO PARTICIPER (idEvent, idMembre) VALUES
(1, 1), -- Jean participe au Tournoi Régional
(2, 2), -- Marie participe au Championnat M17
(3, 1), -- Jean participe à l'entraînement
(3, 2), -- Marie participe à l'entraînement
(4, 1), -- Jean participe à l'AG (Réunion)
(5, 1), -- Jean participe à la Fête du Club 2023 (passé)
(5, 2), -- Marie participe à la Fête du Club 2023 (passé)
(21, 1), -- Jean participe à la Fête du Club 2024 (futur)
(21, 2), -- Marie participe à la Fête du Club 2024 (futur)
(21, 3); -- Paul participe à la Fête du Club 2024 (futur)

-- Insertion des résultats
INSERT INTO RESULTAT (resultat, dateRE, typeArmeRE, typeCompeteRE, idCompetition, idMembre) VALUES
('2ème place', '2024-05-11', 'Épée', 'Régional', 1, 1),
('16ème place', '2024-06-15', 'Fleuret', 'National', 2, 2);

-- Tables de liaison pour les résultats (AVOIR, RESULTER)
INSERT INTO AVOIR (idResultat, idMembre) VALUES
(1, 1),
(2, 2);

INSERT INTO RESULTER (idResultat, idCompetition) VALUES
(1, 1),
(2, 2);

-- Insertion des formulaires de contact
INSERT INTO FORMULAIRE_CONTACT (typeFC, sujetFC, mailFC, descriptionFC, dateFC, idMembre, idAdmin) VALUES
('Question', 'Horaires', 'visiteur@email.com', 'Quels sont les horaires pour les débutants ?', '2024-04-10', NULL, 1),
('Demande', 'Inscription', 'marie.durand@email.com', 'Je souhaite avoir plus d\'informations sur l\'inscription.', '2023-02-15', 2, 1);

-- Tables de liaison pour les formulaires (REPONDRE, REMPLIR)
INSERT INTO REPONDRE (idFormulaire, idAdmin) VALUES
(1, 1),
(2, 1);

INSERT INTO REMPLIR (idFormulaire, idMembre) VALUES
(2, 2);

-- Insertion des inscriptions en attente
INSERT INTO INSCRIPTION (mailInscr, nomI, prenomI, ddnI, mdpI, sexeI,dateInscription) VALUES
('nouveau.membre@email.com', 'Nouveau', 'Alice', '2000-01-01', 'mdpsecure', 'Femme', '2025-10-23');

INSERT INTO MODIFICATION (nomModif, prenomModif, emailModif, sexeModif, ddnModif, dateModif, idMembre) VALUES
('Durand', 'Marie', 'marie.durand45@email.com', 'Homme', '2008-10-10', '2025-10-20', 2);


-- Insertion des notifications
INSERT INTO NOTIFS (typeN, sourceN, lue, idMembre, idAdmin) VALUES
('Demande Inscription', 'Formulaire', 0, NULL, 1),
('Nouveau Résultat', 'Compétition', 0, 1, NULL),
('Nouveau Résultat', 'Compétition', 1, 2, NULL);

-- Tables de liaison pour les notifications (RECEVOIRA, RECEVOIRM)
INSERT INTO RECEVOIRA (idNotifs, idAdmin) VALUES
(1, 1);

INSERT INTO RECEVOIRM (idNotifs, idMembre) VALUES
(2, 1),
(3, 2);

-- Insertion des images
INSERT INTO IMAGEAPP (urlI, prive, alt) VALUES
('/static/images/compet_1.jpg', 0, 'Tournoi régional épée'),
('/static/images/fete_club.png', 0, 'Affiche fête du club');

-- Liaison des images aux compétitions et événements
INSERT INTO IMAGERC (idImage, idCompetition) VALUES (1, 1);
INSERT INTO IMAGERE (idImage, idEventClub) VALUES (2, 1);

-- Insertion dans INFORMATION
INSERT INTO INFORMATION (dateIN, heureIN, titreIN, contenuIN) VALUES
('2023-08-15', '10:27','Reception des nouveaux gants','Nous vous informons que les gants que nous attendions sont là');

-- Liaison des images aux informations
INSERT INTO IMAGERIN (idImage, idInformation) VALUES (1, 1);

-- Insertion dans PRESSE
INSERT INTO PRESSE (dateP, heureP, titreP, contenuP,lienP) VALUES
('2025-11-11','23:23','escrime et passion','le cercle à eu le droit à une article du jornal local','https://www.journaldeBloissabrelaserquitournerigolo.com');

-- Liaison des images aux informations
INSERT INTO IMAGERP (idImage, idPresse) VALUES (1, 1);


-- Réactiver la vérification des clés étrangères
SET FOREIGN_KEY_CHECKS=1;
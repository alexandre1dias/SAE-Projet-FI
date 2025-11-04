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
INSERT INTO MEMBRE (nomM, prenomM, emailM, mdpM, date_inscription, sexeM, ddnM, niveau, statut, activite, idParamNotifMembre) VALUES
('Dupont', 'Jean', 'jean.dupont@email.com', 'mdp123', '2023-01-15', 'Homme', '1995-05-20', 'Senior', 'Membre Actif', 1, NULL),
('Durand', 'Marie', 'marie.durand@email.com', 'mdp456', '2023-02-20', 'Femme', '2008-08-10', 'M17', 'Membre Actif', 1, NULL),
('Martin', 'Paul', 'paul.martin@email.com', 'mdp789', '2022-09-01', 'Homme', '2015-03-25', 'M9', 'Membre Inactif', 0, NULL);

-- Insertion des paramètres de notification pour les membres
INSERT INTO PARAMETRE_NOTIF_MEMBRE (eventInscriptionSite, evenementInscriptionMail, eventNouveauSite, eventNouveauMail, eventAnnulationSite, eventAnnulationMail, resultatNouveauSite, resuletatNouveauMail, reponseFormulaireSite, reponseFormulaireMail, modifProfilSite, modifProfilMail, idMembre) VALUES
(1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1),
(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2),
(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3);

-- Mise à jour des membres pour lier leurs paramètres de notification
UPDATE MEMBRE SET idParamNotifMembre = 1 WHERE idMembre = 1;
UPDATE MEMBRE SET idParamNotifMembre = 2 WHERE idMembre = 2;
UPDATE MEMBRE SET idParamNotifMembre = 3 WHERE idMembre = 3;

-- Insertion des événements (table parente)
INSERT INTO EVENEMENT () VALUES
(), (), (), (), (), ();

-- Insertion des compétitions
INSERT INTO COMPETITION (nomCO, villeCO, adresseCO, dateDebutCO, heureDebutCO, dateFinCO, heureFinCO, typeArmeCO, nbParticipantsCO, sexeCO, typeCompete, descriptionCO, niveauCO, classementCO, idEvent) VALUES
('Tournoi Régional', 'Orléans', '123 Rue du Sport', '2024-05-10', '09:00', '2024-05-11', '18:00', 'Épée', 64, 'Mixte', 'Régional', 'Compétition ouverte à tous les niveaux régionaux.', 'Senior', 'En cours', 1),
('Championnat M17', 'Tours', '456 Avenue de la Victoire', '2024-06-15', '08:30', '2024-06-15', '19:00', 'Fleuret', 32, 'Femme', 'National', 'Championnat national pour la catégorie M17.', 'M17', NULL, 2);

-- Insertion des entraînements
INSERT INTO ENTRAINEMENT (jourEN, lieuEN, dateEN, heureDebutEN, heureFinEN, typeArmeEN, niveauEN, idEvent) VALUES
('Lundi', 'Gymnase A', '2024-04-29', '18:00', '20:00', 'Sabre', 'Tous', 3);

-- Insertion des réunions
INSERT INTO REUNION (nomRE, lieuRE, dateRE, heureDebutRE, nbParticipantsRE, typeReunionRE, rapportRE, niveauRE, idEvent) VALUES
('AG Annuelle', 'Salle du Club', '2024-09-05', '19:00', 50, 'Assemblée', 'Rapport annuel des activités et finances.', 'Tous', 4);

-- Insertion des événements de club
INSERT INTO EVENTCLUB (NomEV, villeEV, adresseEV, dateDebutEV, heureDebutEV, dateFinEV, heureFinEV, nbParticipantEV, descriptionEV, niveauxEV, idEvent) VALUES
('Fête du Club', 'Orléans', '789 Boulevard de la Fête', '2024-07-01', '12:00', '2024-07-01', '22:00', 100, 'Journée festive pour tous les membres et leurs familles.', 'Tous', 5);

-- Insertion des participations aux événements
INSERT INTO PARTICIPER (idEvent, idMembre) VALUES
(1, 1), -- Jean participe au Tournoi Régional
(2, 2), -- Marie participe au Championnat M17
(3, 1), -- Jean participe à l'entraînement
(3, 2), -- Marie participe à l'entraînement
(4, 1), -- Jean participe à l'AG
(5, 1), -- Jean participe à la Fête du Club
(5, 2), -- Marie participe à la Fête du Club
(5, 3); -- Paul participe à la Fête du Club

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
INSERT INTO INSCRIPTION (mailInscr, nomI, prenomI, ddnI, mdpI, sexeI, acceptee, idMembre) VALUES
('nouveau.membre@email.com', 'Nouveau', 'Alice', '2000-01-01', 'mdpsecure', 'Femme', 0, NULL);

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

-- Insertion des actualités
INSERT INTO ACTUALITE (dateAC, heureAC, nomAC, categorieAC) VALUES
('2024-05-12', '10:00', 'Bravo Jean !', 'Résultats');

-- Liaison des images aux actualités
INSERT INTO IMAGERA (idImage, idActualite) VALUES (1, 1);

-- Réactiver la vérification des clés étrangères
SET FOREIGN_KEY_CHECKS=1;

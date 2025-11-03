-- Pour gérer les dépendances circulaires, on désactive temporairement la vérification des clés étrangères
SET FOREIGN_KEY_CHECKS = 0;

-- Insertion dans ADMINSTRATEUR
INSERT INTO ADMINSTRATEUR (idAdmin, emailA, mdpA, idParamNotifAdmin) VALUES
(1, 'admin@escrime-club.com', 'admin_password', 1);

-- Insertion dans PARAMETRE_NOTIF_ADMIN
INSERT INTO PARAMETRE_NOTIF_ADMIN (idParamNotifAdmin, formulaireDemandeSite, formulaireDemandeMail, formulaireQuestionSite, formulaireQuestionMail, formulaireSignalementSite, formulaireSignalementMail, demandeModifSite, demandeModifMail, demandeInscriptionSite, demandeInscriptionMail, idAdmin) VALUES
(1, true, true, true, true, true, true, true, true, true, true, 1);

-- Insertion dans MEMBRE
INSERT INTO MEMBRE (idMembre, nomM, prenomM, emailM, mdpM, date_inscription, sexeM, ddnM, niveau, statut, activite, idParamNotifMembre) VALUES
(1, 'Dupont', 'Jean', 'jean.dupont@email.com', 'password123', '2023-01-15', 'H', '1998-05-20', 'Senior', 'Membre Actif', 'Fleuret', 1),
(2, 'Martin', 'Sophie', 'sophie.martin@email.com', 'password456', '2023-02-20', 'F', '2005-08-10', 'M17', 'Membre Actif', 'Épée', 2);

-- Insertion dans PARAMETRE_NOTIF_MEMBRE
INSERT INTO PARAMETRE_NOTIF_MEMBRE (idParamNotifMembre, eventInscriptionSite, evenementInscriptionMail, eventNouveauSite, eventNouveauMail, eventAnnulationSite, eventAnnulationMail, resultatNouveauSite, resuletatNouveauMail, reponseFormulaireSite, reponseFormulaireMail, modifProfilSite, modifProfilMail, idMembre) VALUES
(1, true, false, true, true, true, false, true, true, true, true, true, false, 1),
(2, true, true, true, true, true, true, true, true, true, true, true, true, 2);

-- Réactivation des contraintes pour la suite
SET FOREIGN_KEY_CHECKS = 1;

-- Mise à jour des dépendances circulaires (si nécessaire, mais les insertions ci-dessus devraient fonctionner avec la désactivation temporaire)
-- UPDATE ADMINSTRATEUR SET idParamNotifAdmin = 1 WHERE idAdmin = 1;
-- UPDATE MEMBRE SET idParamNotifMembre = 1 WHERE idMembre = 1;
-- UPDATE MEMBRE SET idParamNotifMembre = 2 WHERE idMembre = 2;

-- Insertion dans EVENEMENT (entité parente pour les types d'événements)
INSERT INTO EVENEMENT (idEvent) VALUES
(1), -- Entrainement
(2), -- Compétition
(3), -- Réunion
(4), -- Événement Club
(5); -- Autre compétition

-- Insertion dans ENTRAINEMENT
INSERT INTO ENTRAINEMENT (idEntrainement, jourEN, lieuEN, dateEN, heureDebutEN, heureFinEN, typeArmeEN, niveauEN, idEvent) VALUES
(1, 'Lundi', 'Gymnase A', '2024-09-09', '18:00', '20:00', 'Fleuret', 'Tous', 1);

-- Insertion dans COMPETITION
INSERT INTO COMPETITION (idCompetition, nomCO, villeCO, adresseCO, dateDebutCO, heureDebutCO, dateFinCO, heureFinCO, typeArmeCO, nbParticipantsCO, sexeCO, typeCompete, descriptionCO, niveauCO, classementCO, idEvent) VALUES
(1, 'Tournoi Régional', 'Orléans', '123 rue du Sport', '2024-10-05', '09:00', '2024-10-06', '18:00', 'Épée', 64, 'Mixte', 'Individuel', 'Compétition ouverte à tous les licenciés de la région.', 'Régional', NULL, 2),
(2, 'Challenge M17', 'Tours', '456 av. de la Victoire', '2024-11-12', '08:30', '2024-11-12', '19:00', 'Sabre', 32, 'H', 'Individuel', 'Challenge national pour la catégorie M17.', 'National', NULL, 5);

-- Insertion dans REUNION
INSERT INTO REUNION (idReunion, nomRE, lieuRE, dateRE, heureDebutRE, nbParticipantsRE, typeReunionRE, rapportRE, niveauRE, idEvent) VALUES
(1, 'AG Annuelle', 'Salle du Club', '2024-09-15', '19:00', 30, 'Assemblée', 'Rapport à venir', 'Tous', 3);

-- Insertion dans EVENTCLUB
INSERT INTO EVENTCLUB (idEventClub, NomEV, villeEV, adresseEV, dateDebutEV, heureDebutEV, dateFinEV, heureFinEV, nbParticipantEV, descriptionEV, niveauxEV, idEvent) VALUES
(1, 'Fête du Club', 'Orléans', 'Gymnase A', '2025-06-28', '14:00', '2025-06-28', '22:00', 100, 'Journée festive pour tous les membres et leur famille.', 'Tous', 4);

-- Insertion dans PARTICIPER (membres participant à des événements)
INSERT INTO PARTICIPER (idEvent, idMembre) VALUES
(2, 1), -- Jean Dupont participe à la compétition 1
(2, 2), -- Sophie Martin participe à la compétition 1
(3, 1), -- Jean Dupont participe à la réunion 1
(4, 1), -- Jean Dupont participe à la fête du club
(4, 2); -- Sophie Martin participe à la fête du club

-- Insertion dans INSCRIPTION (nouvelles demandes d'inscription)
INSERT INTO INSCRIPTION (idInscription, mailInscr, nomI, prenomI, ddnI, mdpI, sexeI, acceptée, idMembre) VALUES
(1, 'nouveau.membre@email.com', 'Nouveau', 'Pierre', '2002-01-30', 'new_password', 'H', false, NULL);

-- Insertion dans FORMULAIRE_CONTACT
INSERT INTO FORMULAIRE_CONTACT (idFormulaire, typeFC, sujetFC, mailFC, descriptionFC, dateFC, idMembre, idAdmin) VALUES
(1, 'Question', 'Horaires', 'visiteur@email.com', 'Quels sont les horaires pour les débutants ?', '2024-05-10', NULL, NULL),
(2, 'Demande', 'Changement de mail', 'jean.dupont@email.com', 'Je souhaite changer mon adresse email.', '2024-05-12', 1, NULL);

-- Insertion dans REMPLIR (qui a rempli le formulaire)
INSERT INTO REMPLIR (idFormulaire, idMembre) VALUES
(2, 1);

-- Insertion dans REPONDRE (quel admin a répondu)
INSERT INTO REPONDRE (idFormulaire, idAdmin) VALUES
(1, 1);

-- Insertion dans RESULTAT
INSERT INTO RESULTAT (idResultat, resultat, dateRE, typeArmeRE, typeCompeteRE, idCompetition, idMembre) VALUES
(1, '2ème place', '2024-10-06', 'Épée', 'Individuel', 1, 2),
(2, '16ème place', '2024-10-06', 'Épée', 'Individuel', 1, 1);

-- Insertion dans AVOIR (lien résultat <-> membre)
INSERT INTO AVOIR (idResultat, idMembre) VALUES
(1, 2),
(2, 1);

-- Insertion dans RESULTER (lien résultat <-> compétition)
INSERT INTO RESULTER (idResultat, idCompetition) VALUES
(1, 1),
(2, 1);

-- Insertion dans ACTUALITE
INSERT INTO ACTUALITE (idActualite, dateAC, heureAC, nomAC, categorieAC) VALUES
(1, '2024-10-07', '10:00', 'Résultats Tournoi', 'Compétition');

-- Insertion dans IMAGEAPP
INSERT INTO IMAGEAPP (idImage, urlI, prive, alt) VALUES
(1, '/static/images/compet_regional_2024.jpg', false, 'Podium de la compétition régionale 2024'),
(2, '/static/images/fete_club_2025.png', false, 'Ambiance à la fête du club'),
(3, '/static/images/entrainement_fleuret.jpg', true, 'Entrainement fleuret du lundi soir');

-- Insertion dans IMAGERC (lien image <-> compétition)
INSERT INTO IMAGERC (idImage, idCompetition) VALUES
(1, 1);

-- Insertion dans IMAGERE (lien image <-> événement club)
INSERT INTO IMAGERE (idImage, idEventClub) VALUES
(2, 1);

-- Insertion dans IMAGERA (lien image <-> actualité)
INSERT INTO IMAGERA (idImage, idActualite) VALUES
(1, 1);

-- Insertion dans NOTIFS
INSERT INTO NOTIFS (idNotifs, typeN, sourceN, lue, idMembre, idAdmin) VALUES
(1, 'Nouveau Résultat', 'Compétition', false, 2, NULL),
(2, 'Demande Inscription', 'Inscription', false, NULL, 1);

-- Insertion dans RECEVOIRM (notification pour membre)
INSERT INTO RECEVOIRM (idNotifs, idMembre) VALUES
(1, 2);

-- Insertion dans RECEVOIRA (notification pour admin)
INSERT INTO RECEVOIRA (idNotifs, idAdmin) VALUES
(2, 1);

-- Note : La table GENERER n'est pas peuplée car elle lie une inscription à un membre,
-- ce qui se produit généralement après qu'un admin a accepté l'inscription et créé le compte membre.
-- Vous pourriez l'utiliser après avoir traité l'inscription de 'Pierre Nouveau'.


-- Création de l'administrateur principal pour les tests de l'application.
insert into ADMIN (IdAdmin, nomA, prenomA, emailA, mdpA, date_embaucheA, statutA)
values (1, 'Admin', 'Principal', 'a','a', '2020-08-10', 'Administrateur');

-- Création de membres existants pour peupler la base de données avec des utilisateurs de test.
insert into MEMBRE (idMembre, nomM, prenomM, emailM, mdp, date_inscription, sexeM, ddnM, statut, activite, IdParamNotifMembre)
values (1, 'Dias', 'Alexandre', 'alexandredias@gmail.com', 'fakerlegoat', '2020-08-10', 'M', '2005-09-27', 'Membre',1,NULL);

insert into MEMBRE (idMembre, nomM, prenomM, emailM, mdp, date_inscription, sexeM, ddnM, statut, activite, IdParamNotifMembre)
values (2, 'Clément', 'Schmit', 'clementschmit@gmail.com', 'leraidersdu41', '2020-08-10', 'M', '2006-01-26', 'Membre',1,NULL);

-- SCÉNARIOS D'INSCRIPTION

-- Cas 1 : Une inscription déjà acceptée (acceptée = 1).
insert into INSCRIPTION (idInscription, mailInscr, nomI, prenomI, ddnI, mdpI, sexeI, acceptée)
values (1, 'kurucelikerman@gmail.com', 'Kurucelik', 'Erman', '2006-01-08', 'lesouleveurdepoids', 'M', 1);

-- Cas 2 : Une nouvelle demande d'inscription en attente de validation (acceptée = 0).
insert into INSCRIPTION (idInscription, mailInscr, nomI, prenomI, ddnI, mdpI, sexeI, acceptée)
values (2, 'desgrangeslucas@gmail.com', 'Desgranges', 'Lucas', '2006-05-06', 'mdpdeLucas', 'M', 0);

-- INSERTIONS POUR SIMULER LES NOTIFICATIONS ADMINS

-- Insertion pour tester notif d'une nouvelle inscription dans les insertions ci-dessus

-- Insertion pour tester notif d'un nouveau formulaire de contact (type Question)
insert into FORMULAIRE_CONTACT (idFormulaire, typeFC, sujetFC, mailFC, descriptionFC, dateFC, idMembre, IdAdmin)
values (1, 'Question', 'Question sur le matériel', 'visiteur.anonyme@email.com', 'Bonjour, faut-il acheter son propre masque pour la séance découverte ?', CURDATE(), NULL, 1);

-- Insertion pour tester notif d'une demande de modification de profil (type Modification)
insert into FORMULAIRE_CONTACT (idFormulaire, typeFC, sujetFC, mailFC, descriptionFC, dateFC, idMembre, IdAdmin)
values (2, 'Modification', 'Demande de changement de niveau', 'alexandredias@gmail.com', 'Bonjour, je pense que mon niveau devrait être mis à jour sur mon profil. Merci.', CURDATE(), 1, 1);

-- INSERTIONS POUR SIMULER LES NOTIFICATIONS MEMBRES

-- Notif pour une réponse à un formulaire de contact 
INSERT INTO NOTIFS (IdNotifs, typeN, sourceN, lue, idMembre, IdAdmin)
VALUES (1, 'ReponseFormulaire', 'Un administrateur a répondu à votre formulaire : "Demande de changement de niveau"', 0, 1, 1);
INSERT INTO RECEVOIRM (idMembre, idNotifs) VALUES (1, 1);

-- Notif pour un nouveau résultat ajouté
INSERT INTO NOTIFS (IdNotifs, typeN, sourceN, lue, idMembre, IdAdmin)
VALUES (2, 'NouveauResultat', 'Nouveau résultat ajouté : 3ème place au tournoi régional', 0, 2, 1);
INSERT INTO RECEVOIRM (idMembre, idNotifs) VALUES (2, 2);

-- Notif pour l'inscription à un événement
INSERT INTO NOTIFS (IdNotifs, typeN, sourceN, lue, idMembre, IdAdmin)
VALUES (3, 'InscriptionEvenement', 'Vous avez été inscrit à l''événement : Entraînement Sabre M17', 0, 1, 1);
INSERT INTO RECEVOIRM (idMembre, idNotifs) VALUES (1, 3);

-- INSERTIONS POUR TESTER L'INSCRIPTION A UN EVENEMENT SELON LE NIVEAU

-- 1. Création d'un membre de test avec un niveau 'M15'
insert into MEMBRE (idMembre, nomM, prenomM, emailM, mdp, date_inscription, sexeM, ddnM, statut, activite, IdParamNotifMembre, niveau)
values (10, 'Testeur', 'Niveau', 'test.niveau@gmail.com', 'password', '2023-01-01', 'M', '2008-01-01', 'Membre', 1, NULL, 'M15');

-- 2. Création de 3 événements (compétitions) avec des niveaux différents
-- Événement au même niveau (M15) -> Inscription autorisée
INSERT INTO EVENEMENT (idEvenement) VALUES (1);
INSERT INTO COMPETITION (idCompete, NomCO, dateDebutCO, niveauxCO, idEvent) VALUES (1, 'Tournoi Régional M15', '2024-06-10', 'M15', 1);

-- Événement au niveau +1 (M17) -> Inscription autorisée
INSERT INTO EVENEMENT (idEvenement) VALUES (2);
INSERT INTO COMPETITION (idCompete, NomCO, dateDebutCO, niveauxCO, idEvent) VALUES (2, 'Open National M17', '2024-06-15', 'M17', 2);

-- Événement au niveau +2 (M20) -> Inscription non autorisée
INSERT INTO EVENEMENT (idEvenement) VALUES (3);
INSERT INTO COMPETITION (idCompete, NomCO, dateDebutCO, niveauxCO, idEvent) VALUES (3, 'Championnat Senior M20', '2024-06-20', 'M20', 3);

-- 3. Tentatives d'inscription du membre (idMembre = 3) aux événements
-- Cas 1 : Inscription autorisée (même niveau)
INSERT INTO PARTICIPER (idMembre, idEvenement) VALUES (10, 1);
-- Cas 2 : Inscription autorisée (niveau +1)
INSERT INTO PARTICIPER (idMembre, idEvenement) VALUES (10, 2);
-- Cas 3 : Inscription qui devrait être bloquée par le trigger (niveau +2)
INSERT INTO PARTICIPER (idMembre, idEvenement) VALUES (10, 3);

-- INSERTIONS POUR TESTER L'INSCRIPTION A UNE COMPETITION SELON LE SEXE

-- 1. Création de membres de test (un homme, une femme)
insert into MEMBRE (idMembre, nomM, prenomM, emailM, mdp, date_inscription, sexeM, ddnM, statut, activite, IdParamNotifMembre, niveau)
values (4, 'Testeur', 'Homme', 'test.homme@gmail.com', 'password', '2023-01-01', 'M', '2000-01-01', 'Membre', 1, NULL, 'Senior');
insert into MEMBRE (idMembre, nomM, prenomM, emailM, mdp, date_inscription, sexeM, ddnM, statut, activite, IdParamNotifMembre, niveau)
values (5, 'Testeuse', 'Femme', 'test.femme@gmail.com', 'password', '2023-01-01', 'F', '2000-01-01', 'Membre', 1, NULL, 'Senior');

-- 2. Création de 3 compétitions avec des contraintes de sexe différentes
INSERT INTO EVENEMENT (idEvenement) VALUES (4);
INSERT INTO COMPETITION (idCompete, NomCO, dateDebutCO, niveauxCO, sexeCO, idEvent) VALUES (4, 'Compétition Masculine', '2024-07-01', 'Senior', 'Masculin', 4);

INSERT INTO EVENEMENT (idEvenement) VALUES (5);
INSERT INTO COMPETITION (idCompete, NomCO, dateDebutCO, niveauxCO, sexeCO, idEvent) VALUES (5, 'Compétition Féminine', '2024-07-05', 'Senior', 'Féminin', 5);

INSERT INTO EVENEMENT (idEvenement) VALUES (6);
INSERT INTO COMPETITION (idCompete, NomCO, dateDebutCO, niveauxCO, sexeCO, idEvent) VALUES (6, 'Compétition Mixte', '2024-07-10', 'Senior', 'Mixte', 6);

-- 3. Tentatives d'inscription
-- Cas valides
INSERT INTO PARTICIPER (idMembre, idEvenement) VALUES (4, 4); -- Homme dans compétition masculine
INSERT INTO PARTICIPER (idMembre, idEvenement) VALUES (5, 5); -- Femme dans compétition féminine
INSERT INTO PARTICIPER (idMembre, idEvenement) VALUES (4, 6); -- Homme dans compétition mixte
INSERT INTO PARTICIPER (idMembre, idEvenement) VALUES (5, 6); -- Femme dans compétition mixte
INSERT INTO PARTICIPER (idMembre, idEvenement) VALUES (4, 5); -- Tentative : Homme dans compétition féminine
INSERT INTO PARTICIPER (idMembre, idEvenement) VALUES (5, 4); -- Tentative : Femme dans compétition masculine

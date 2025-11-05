
-- Création de l'administrateur principal pour les tests de l'application.
insert into ADMINISTRATEUR (IdAdmin, emailA, mdpA)
values (1, 'a','a');

-- INSERTIONS POUR TESTER LE TRIGGER DE CALCUL DE NIVEAU MEMBRE

-- Membres de différents âges pour tester le calcul automatique du niveau.
insert into MEMBRE (idMembre, nomM, prenomM, emailM, mdpM, date_inscription, sexeM, ddnM, statut, activite, IdParamNotifMembre)
values (2, 'Jeune', 'Membre', 'jeune.membre@gmail.com', 'password', '2023-01-01', 'M', '2010-01-01', 'Membre', 1, NULL);

insert into MEMBRE (idMembre, nomM, prenomM, emailM, mdpM, date_inscription, sexeM, ddnM, statut, activite, IdParamNotifMembre)
values (3, 'Adulte', 'Membre', 'adulte.membre@gmail.com', 'password', '2023-01-01', 'M', '1990-01-01', 'Membre', 1, NULL);


-- INSCRIPTION POUR TESTER LE TRIGGER D'ACCEPTATION D'INSCRIPTION

--Une inscription.
insert into INSCRIPTION (idInscription, mailInscr, nomI, prenomI, ddnI, mdpI, sexeI, acceptee)
values (1, 'kurucelikerman@gmail.com', 'Kurucelik', 'Erman', '2006-01-08', 'lesouleveurdepoids', 'M', 0);

-- Mise à jour de l'inscription pour l'accepter.
UPDATE INSCRIPTION SET acceptee = 1 WHERE idInscription = 1;

-- INSERTIONS POUR TESTER L'INSCRIPTION A UN EVENEMENT SELON LE NIVEAU

-- 1. Création d'un membre de test.
-- La date de naissance '2009-01-01' assure que le trigger 'calcul_niveau_membre'
-- lui assignera le niveau 'M15' (âge de 15 ans en 2024).
insert into MEMBRE (idMembre, nomM, prenomM, emailM, mdpM, date_inscription, sexeM, ddnM, statut, activite, IdParamNotifMembre)
values (10, 'Testeur', 'Niveau', 'test.niveau@gmail.com', 'password', '2023-01-01', 'M', '2011-01-01', 'Membre', 1, NULL);

-- 2. Création de 3 événements (compétitions) avec des niveaux différents
-- Événement au même niveau (M15) -> Inscription autorisée
INSERT INTO EVENEMENT (idEvent) VALUES (1);
INSERT INTO COMPETITION (idCompetition, NomCO, dateDebutCO, niveauCO, idEvent) VALUES (1, 'Tournoi Régional M15', '2024-06-10', 'M15', 1);

-- Événement au niveau +1 (M17) -> Inscription autorisée
INSERT INTO EVENEMENT (idEvent) VALUES (2);
INSERT INTO COMPETITION (idCompetition, NomCO, dateDebutCO, niveauCO, idEvent) VALUES (2, 'Open National M17', '2024-06-15', 'M17', 2);

-- Événement au niveau +2 (M20) -> Inscription non autorisée
INSERT INTO EVENEMENT (idEvent) VALUES (3);
INSERT INTO COMPETITION (idCompetition, NomCO, dateDebutCO, niveauCO, idEvent) VALUES (3, 'Championnat Senior M20', '2024-06-20', 'M20', 3);

-- 3. Tentatives d'inscription du membre (idMembre = 10) aux événements
-- Cas 1 : Inscription autorisée (même niveau)
INSERT INTO PARTICIPER (idMembre, idEvent) VALUES (10, 1);
-- Cas 2 : Inscription autorisée (niveau +1)
INSERT INTO PARTICIPER (idMembre, idEvent) VALUES (10, 2);
-- Cas 3 : Inscription qui devrait être bloquée par le trigger (niveau +2)
INSERT INTO PARTICIPER (idMembre, idEvent) VALUES (10, 3);

-- INSERTIONS POUR TESTER L'INSCRIPTION A UNE COMPETITION SELON LE SEXE

-- 1. Création de membres de test (un homme, une femme)
insert into MEMBRE (idMembre, nomM, prenomM, emailM, mdpM, date_inscription, sexeM, ddnM, statut, activite, IdParamNotifMembre, niveau)
values (4, 'Testeur', 'Homme', 'test.homme@gmail.com', 'password', '2023-01-01', 'M', '2000-01-01', 'Membre', 1, NULL, 'Senior');
insert into MEMBRE (idMembre, nomM, prenomM, emailM, mdpM, date_inscription, sexeM, ddnM, statut, activite, IdParamNotifMembre, niveau)
values (5, 'Testeuse', 'Femme', 'test.femme@gmail.com', 'password', '2023-01-01', 'F', '2000-01-01', 'Membre', 1, NULL, 'Senior');

-- 2. Création de 2 compétitions avec des contraintes de sexe différentes
INSERT INTO EVENEMENT (idEvent) VALUES (4);
INSERT INTO COMPETITION (idCompetition, NomCO, dateDebutCO, niveauCO, sexeCO, idEvent) VALUES (4, 'Compétition Masculine', '2024-07-01', 'Senior', 'H', 4);

INSERT INTO EVENEMENT (idEvent) VALUES (5);
INSERT INTO COMPETITION (idCompetition, NomCO, dateDebutCO, niveauCO, sexeCO, idEvent) VALUES (5, 'Compétition Féminine', '2024-07-05', 'Senior', 'F', 5);

-- 3. Tentatives d'inscription
-- Cas valides
INSERT INTO PARTICIPER (idMembre, idEvent) VALUES (4, 4); -- Homme dans compétition masculine
INSERT INTO PARTICIPER (idMembre, idEvent) VALUES (5, 5); -- Femme dans compétition féminine

-- Cas invalides (devraient être bloqués par le trigger verif_genre_competition)
INSERT INTO PARTICIPER (idMembre, idEvent) VALUES (4, 5); -- Tentative : Homme dans compétition féminine
INSERT INTO PARTICIPER (idMembre, idEvent) VALUES (5, 4); -- Tentative : Femme dans compétition masculine


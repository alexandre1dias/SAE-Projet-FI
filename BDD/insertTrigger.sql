-- ####################################################################
-- FICHIER DE TEST POUR LES TRIGGERS
-- ####################################################################

-- ====================================================================
-- TEST: calcul_niveau_age_membre (BEFORE INSERT ON MEMBRE)
-- ====================================================================
-- Membres de différents âges pour tester le calcul automatique du niveau.
-- Le trigger doit calculer 'age' et 'niveau'.
INSERT INTO MEMBRE (idMembre, nomM, prenomM, emailM, mdpM, date_inscription, sexeM, ddnM, statut, activite, IdParamNotifMembre)
VALUES (2, 'Jeune', 'Membre', 'jeune.membre@gmail.com', 'password', '2023-01-01', 'M', '2010-01-01', 'Membre', 1, NULL);
INSERT INTO MEMBRE (idMembre, nomM, prenomM, emailM, mdpM, date_inscription, sexeM, ddnM, statut, activite, IdParamNotifMembre)
VALUES (3, 'Adulte', 'Membre', 'adulte.membre@gmail.com', 'password', '2023-01-01', 'M', '1990-01-01', 'Membre', 1, NULL);

-- ====================================================================
-- TEST: mise_a_jour_niveau_age_membre (BEFORE UPDATE ON MEMBRE)
-- ====================================================================
-- Le trigger doit recalculer 'age' et 'niveau' si 'ddnM' change.
UPDATE MEMBRE SET ddnM = '2005-01-01' WHERE idMembre = 3;

-- ====================================================================
-- TEST: verif_niveau_competition (BEFORE INSERT ON PARTICIPER)
-- ====================================================================
-- 1. Création d'un membre de test.
-- ddnM '2011-01-01' -> le trigger 'calcul_niveau_age_membre'
-- doit lui assigner le niveau 'M13'.
INSERT INTO MEMBRE (idMembre, nomM, prenomM, emailM, mdpM, date_inscription, sexeM, ddnM, statut, activite, IdParamNotifMembre)
VALUES (10, 'Testeur', 'Niveau', 'test.niveau@gmail.com', 'password', '2023-01-01', 'M', '2012-01-01', 'Membre', 1, NULL);
-- 2. Création des événements et compétitions
-- Événement au même niveau (M13) -> Inscription autorisée
INSERT INTO EVENEMENT (idEvent) VALUES (1);
INSERT INTO COMPETITION (idCompetition, NomCO, dateDebutCO, niveauCO, idEvent, villeCO, adresseCO, heureDebutCO, dateFinCO, heureFinCO, typeArmeCO, sexeCO, typeCompete, passeeCO) 
VALUES (1, 'Tournoi Régional M13', '2024-06-10', 'M13', 1, 'Paris', '1 Rue A', '09:00', '2024-06-10', '18:00', 'Fleuret', 'H', 'Regionale', 0);
-- Événement au niveau +1 (M15) -> Inscription autorisée (surclassement)
INSERT INTO EVENEMENT (idEvent) VALUES (2);
INSERT INTO COMPETITION (idCompetition, NomCO, dateDebutCO, niveauCO, idEvent, villeCO, adresseCO, heureDebutCO, dateFinCO, heureFinCO, typeArmeCO, sexeCO, typeCompete, passeeCO) 
VALUES (2, 'Open National M15', '2024-06-15', 'M15', 2, 'Lyon', '2 Rue B', '09:00', '2024-06-15', '18:00', 'Fleuret', 'H', 'National', 0);
-- Événement au niveau +2 (M17) -> Inscription non autorisée
INSERT INTO EVENEMENT (idEvent) VALUES (3);
INSERT INTO COMPETITION (idCompetition, NomCO, dateDebutCO, niveauCO, idEvent, villeCO, adresseCO, heureDebutCO, dateFinCO, heureFinCO, typeArmeCO, sexeCO, typeCompete, passeeCO) 
VALUES (3, 'Championnat M17', '2024-06-20', 'M17', 3, 'Lille', '3 Rue C', '09:00', '2024-06-20', '18:00', 'Fleuret', 'H', 'National', 0);
-- 3. Tentatives d'inscription du membre (idMembre = 10, niveau M13)
-- Cas 1 : Inscription autorisée (même niveau M13)
INSERT INTO PARTICIPER (idMembre, idEvent) VALUES (10, 1);
-- Cas 2 : Inscription autorisée (niveau +1, M15)
INSERT INTO PARTICIPER (idMembre, idEvent) VALUES (10, 2);
-- Cas 3 : Inscription qui devrait être bloquée par le trigger (niveau +2, M17)
INSERT INTO PARTICIPER (idMembre, idEvent) VALUES (10, 3);

-- ====================================================================
-- TEST: verif_genre_competition (BEFORE INSERT ON PARTICIPER)
-- ====================================================================
-- 1. Création de membres de test (un homme 'M', une femme 'F')
INSERT INTO MEMBRE (idMembre, nomM, prenomM, emailM, mdpM, date_inscription, sexeM, ddnM, statut, activite, IdParamNotifMembre, niveau)
VALUES (4, 'Testeur', 'Homme', 'test.homme@gmail.com', 'password', '2023-01-01', 'M', '2000-01-01', 'Membre', 1, NULL, 'Senior');
INSERT INTO MEMBRE (idMembre, nomM, prenomM, emailM, mdpM, date_inscription, sexeM, ddnM, statut, activite, IdParamNotifMembre, niveau)
VALUES (5, 'Testeuse', 'Femme', 'test.femme@gmail.com', 'password', '2023-01-01', 'F', '2000-01-01', 'Membre', 1, NULL, 'Senior');
-- 2. Création de compétitions (CORRIGÉES)
-- Compétition Masculine (sexeCO = 'H')
INSERT INTO EVENEMENT (idEvent) VALUES (4);
INSERT INTO COMPETITION (idCompetition, NomCO, dateDebutCO, niveauCO, sexeCO, idEvent, villeCO, adresseCO, heureDebutCO, dateFinCO, heureFinCO, typeArmeCO, typeCompete, passeeCO) 
VALUES (4, 'Compétition Masculine', '2024-07-01', 'Senior', 'H', 4, 'Bordeaux', '4 Rue D', '09:00', '2024-07-01', '18:00', 'Épée', 'Regionale', 0);
-- Compétition Féminine (sexeCO = 'F')
INSERT INTO EVENEMENT (idEvent) VALUES (5);
INSERT INTO COMPETITION (idCompetition, NomCO, dateDebutCO, niveauCO, sexeCO, idEvent, villeCO, adresseCO, heureDebutCO, dateFinCO, heureFinCO, typeArmeCO, typeCompete, passeeCO) 
VALUES (5, 'Compétition Féminine', '2024-07-05', 'Senior', 'F', 5, 'Nantes', '5 Rue E', '09:00', '2024-07-05', '18:00', 'Sabre', 'Regionale', 0);
-- 3. Tentatives d'inscription
-- Cas valides
INSERT INTO PARTICIPER (idMembre, idEvent) VALUES (4, 4); -- Homme ('M') dans compétition 'H'
INSERT INTO PARTICIPER (idMembre, idEvent) VALUES (5, 5); -- Femme ('F') dans compétition 'F'
-- Cas invalides (devraient être bloqués par le trigger verif_genre_competition)
INSERT INTO PARTICIPER (idMembre, idEvent) VALUES (4, 5); -- Tentative : Homme ('M') dans compétition 'F'
INSERT INTO PARTICIPER (idMembre, idEvent) VALUES (5, 4); -- Tentative : Femme ('F') dans compétition 'H'

-- ====================================================================
-- TEST: date_inscription (BEFORE INSERT ON INSCRIPTION)
-- ====================================================================
-- Insertion SANS date. Le trigger doit la remplir.
INSERT INTO INSCRIPTION (mailInscr, nomI, prenomI, ddnI, mdpI, sexeI) 
VALUES ('test.trigger@mail.com', 'Test', 'Trigger', '2000-01-01', 'pass', 'M');
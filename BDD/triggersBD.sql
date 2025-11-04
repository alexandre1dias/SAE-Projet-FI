DELIMITER // -- les délimiters MySQL se présentent ainsi, avec des // ou des $$. 

CREATE OR REPLACE TRIGGER verif_genre_competition
BEFORE INSERT ON PARTICIPER

FOR EACH ROW
BEGIN
    DECLARE genre_membre VARCHAR(255);
    DECLARE genre_competition VARCHAR(255);
    -- Récupérer le genre requis pour la compétition, s'il y en a un.
    -- Si l'événement n'est pas une compétition, genre_competition restera NULL.
    SELECT sexeCO INTO genre_competition
    FROM COMPETITION
    WHERE idEvent = NEW.idEvent
    LIMIT 1;

    -- Si l'événement est une compétition (genre_competition n'est pas NULL)
    IF genre_competition IS NOT NULL THEN
        -- Récupérer le sexe du membre qui tente de s'inscrire
        SELECT sexeM INTO genre_membre
        FROM MEMBRE
        WHERE idMembre = NEW.idMembre;

        -- Si la compétition est masculine ('H') et que le membre n'est pas un homme ('M')
        IF genre_competition = 'H' AND genre_membre != 'M' THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Inscription impossible : cette compétition est réservée aux hommes.';
        -- Si la compétition est féminine ('F') et que le membre n'est pas une femme ('F')
        ELSEIF genre_competition = 'F' AND genre_membre != 'F' THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Inscription impossible : cette compétition est réservée aux femmes.';
        END IF;
    END IF;
END;
//

DELIMITER ;

DELIMITER //

CREATE OR REPLACE TRIGGER verif_niveau_competition
BEFORE INSERT ON PARTICIPER
FOR EACH ROW
BEGIN
    DECLARE membre_niveau VARCHAR(20);
    DECLARE competition_niveau VARCHAR(255);
    DECLARE surclassement_niveau VARCHAR(20);

    -- Récupère le niveau requis par la compétition.
    -- Si l'événement n'est pas une compétition, la variable restera NULL et le trigger ne fera rien.
    SELECT niveauCO INTO competition_niveau
    FROM COMPETITION
    WHERE idEvent = NEW.idEvent
    LIMIT 1;

    -- Si c'est une compétition avec un niveau défini
    IF competition_niveau IS NOT NULL THEN
        -- Récupère le niveau actuel du membre
        SELECT niveau INTO membre_niveau
        FROM MEMBRE
        WHERE idMembre = NEW.idMembre;

        -- Détermine le niveau de surclassement autorisé (niveau N+1)
        SET surclassement_niveau = CASE membre_niveau
            WHEN 'M9' THEN 'M11'
            WHEN 'M11' THEN 'M13'
            WHEN 'M13' THEN 'M15'
            WHEN 'M15' THEN 'M17'
            WHEN 'M17' THEN 'M20'
            WHEN 'M20' THEN 'Senior'
            WHEN 'Senior' THEN 'Vétéran'
            ELSE NULL -- Pas de surclassement pour les vétérans ou autres cas
        END;

        -- Vérifie si le niveau de la compétition est autorisé pour le membre.
        -- Un membre peut participer à une compétition de son niveau OU du niveau immédiatement supérieur (surclassement).
        -- On utilise FIND_IN_SET pour vérifier si le niveau du membre (ou son niveau de surclassement)
        -- se trouve dans la liste des niveaux autorisés pour la compétition (ex: "M17,M20").
        IF NOT (FIND_IN_SET(membre_niveau, competition_niveau) > 0 OR (surclassement_niveau IS NOT NULL AND FIND_IN_SET(surclassement_niveau, competition_niveau) > 0)) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Inscription impossible : le niveau du membre ne correspond pas à celui de la compétition.';
        END IF;
    END IF;
END;
//

DELIMITER ;

DELIMITER //

CREATE OR REPLACE TRIGGER creation_membre_apres_acceptation
AFTER UPDATE ON INSCRIPTION
FOR EACH ROW
BEGIN
    -- Vérifie si l'inscription vient d'être acceptée (passe de 0 à 1)
    IF NEW.acceptee = 1 AND OLD.acceptee <> 1 THEN -- (OLD.acceptée <> 1 permet de savoir si le membre n'est pas déjà crée)
        INSERT INTO MEMBRE (nomM, prenomM, emailM, mdpM, ddnM, sexeM, date_inscription, niveau, statut, activite, IdParamNotifMembre)
        VALUES (NEW.nomI, NEW.prenomI, NEW.mailInscr, NEW.mdpI, NEW.ddnI, NEW.sexeI, NOW(), NULL, 'Membre', 1, NULL);
    END IF;
END;
//

DELIMITER ;


-- NOTIFICATION POUR formulaire de contact, inscription , demande de modification 

DELIMITER //

CREATE OR REPLACE TRIGGER notif_admin_inscription
AFTER INSERT ON INSCRIPTION
FOR EACH ROW
BEGIN
    INSERT INTO NOTIFS (typeN, sourceN, lue, idMembre, IdAdmin)
    VALUES ('Inscription', CONCAT('Nouvelle inscription : ', NEW.nomI, ' ', NEW.prenomI), 0, NEW.idMembre, 1); -- ici IdAdmin = 1 par exemple
    
END;
//

DELIMITER ;

DELIMITER //

CREATE OR REPLACE TRIGGER notif_admin_formulaire
AFTER INSERT ON FORMULAIRE_CONTACT
FOR EACH ROW
BEGIN
    INSERT INTO NOTIFS (typeN, sourceN, lue, idMembre, IdAdmin)
    VALUES ('Formulaire', CONCAT('Nouveau formulaire : ', NEW.sujetFC), 0, NEW.idMembre, 1);
END;
//

DELIMITER ;

DELIMITER //

CREATE OR REPLACE TRIGGER notif_admin_modif
AFTER INSERT ON FORMULAIRE_CONTACT
FOR EACH ROW
BEGIN
    INSERT INTO NOTIFS (typeN, sourceN, lue, idMembre, IdAdmin)
    VALUES ('DemandeModification', CONCAT('Nouvelle demande de modification'), 0, NEW.idMembre, 1);
END;
//

DELIMITER ;

-- Trigger pour calculer le niveau d’un membre à partir de sa date de naissance


DELIMITER //

CREATE OR REPLACE TRIGGER calcul_niveau_membre
BEFORE INSERT ON MEMBRE
FOR EACH ROW
BEGIN
    DECLARE annee INT;
    DECLARE age INT;

    -- Calcule le niveau uniquement si aucun n'est fourni lors de l'insertion.
    -- Cela permet de forcer un niveau pour les tests ou des cas spécifiques.
    IF NEW.niveau IS NULL THEN
        SET annee = YEAR(NEW.ddnM);
        SET age = YEAR(CURDATE()) - annee; -- Détermine l'age approximatif

        -- Détermination du niveau selon l'age
        SET NEW.niveau = CASE
            WHEN age < 10 THEN 'M9'
            WHEN age BETWEEN 10 AND 11 THEN 'M11'
            WHEN age BETWEEN 12 AND 13 THEN 'M13'
            WHEN age BETWEEN 14 AND 15 THEN 'M15'
            WHEN age BETWEEN 16 AND 17 THEN 'M17'
            WHEN age BETWEEN 18 AND 19 THEN 'M20'
            WHEN age BETWEEN 20 AND 39 THEN 'Senior'
            ELSE 'Vétéran'
        END;
    END IF;
END;
//

DELIMITER ;

DELIMITER //

CREATE OR REPLACE TRIGGER mise_a_jour_niveau_membre
BEFORE UPDATE ON MEMBRE
FOR EACH ROW
BEGIN
    DECLARE annee INT;
    DECLARE age INT;

    -- Recalcule le niveau uniquement si la date de naissance a été modifiée.
    -- Cela évite d'écraser le niveau lors de la mise à jour d'autres champs (ex: statut, email).
    IF NEW.ddnM != OLD.ddnM THEN
        SET annee = YEAR(NEW.ddnM);
        SET age = YEAR(CURDATE()) - annee; -- Détermine l'age approximatif

        -- Détermination du niveau selon l'age
        SET NEW.niveau = CASE
            WHEN age < 10 THEN 'M9'
            WHEN age BETWEEN 10 AND 11 THEN 'M11'
            WHEN age BETWEEN 12 AND 13 THEN 'M13'
            WHEN age BETWEEN 14 AND 15 THEN 'M15'
            WHEN age BETWEEN 16 AND 17 THEN 'M17'
            WHEN age BETWEEN 18 AND 19 THEN 'M20'
            WHEN age BETWEEN 20 AND 39 THEN 'Senior'
            ELSE 'Vétéran'
        END;
    END IF;
END;
//

DELIMITER ;


-- Quand un formulaire de contact a une réponse
/**
DELIMITER //

CREATE OR REPLACE TRIGGER notif_membre_reponse_formulaire
AFTER INSERT ON REPONDRE
FOR EACH ROW
BEGIN
    DECLARE membre_id INT;

    -- Récupérer l'idMembre associé à ce résultat depuis la table REPONDRE
    SELECT idMembre INTO membre_id FROM REPONDRE WHERE idRepondre = NEW.idRepondre;
    INSERT INTO Notifs (typeN, sourceN, lue, idMembre, IdAdmin)
    VALUES ('RéponseFormulaire', CONCAT('Votre formulaire a reçu une réponse'), 0, NEW.idMembre, NULL);
END;
//

DELIMITER ;

-- Quand une demande de modification est acceptée

DELIMITER //

CREATE OR REPLACE TRIGGER notif_membre_modif_acceptee
AFTER UPDATE ON FORMULAIRE_CONTACT
FOR EACH ROW
BEGIN
    IF NEW.acceptee = 1 AND OLD.acceptee <> 1 THEN -- (OLD.acceptee <> 1 permet de savoir si la demande n'a pas déjà été acceptee)
        INSERT INTO Notifs (typeN, sourceN, lue, idMembre, IdAdmin)
        VALUES ('DemandeModif', 'Votre demande de modification a été acceptée', 0, NEW.idMembre, NULL);
    END IF;
END;
//

DELIMITER ;
**/ 

-- Quand de nouveaux résultats sont ajoutés

DELIMITER //

CREATE OR REPLACE TRIGGER notif_membre_nouveau_resultat
AFTER INSERT ON RESULTER
FOR EACH ROW
BEGIN
    DECLARE membre_id INT;

    -- Récupérer l'idMembre associé à ce résultat depuis la table RESULTAT
    SELECT idMembre INTO membre_id FROM RESULTAT WHERE idResultat = NEW.idResultat;

    INSERT INTO NOTIFS (typeN, sourceN, lue, idMembre, IdAdmin)
    VALUES ('Resultat', 'Un nouveau résultat a été ajouté', 0, membre_id, NULL);
END;
//

DELIMITER ;

-- Event Crée

DELIMITER //

CREATE OR REPLACE TRIGGER notif_membre_evenement_cree
AFTER INSERT ON EVENEMENT
FOR EACH ROW
BEGIN
    -- ici on notifie tous les membres
    INSERT INTO NOTIFS (typeN, sourceN, lue, idMembre, IdAdmin)
    SELECT 'Evenement', CONCAT('Un nouvel événement est créé'), 0, idMembre, NULL
    FROM MEMBRE;
END;
//

DELIMITER ;


-- quand un membre s'inscrit à un evenement

DELIMITER //

CREATE OR REPLACE TRIGGER notif_membre_inscription_evenement
AFTER INSERT ON PARTICIPER
FOR EACH ROW
BEGIN
    INSERT INTO NOTIFS (typeN, sourceN, lue, idMembre, IdAdmin)
    VALUES ('Inscription', 'Vous êtes inscrit à un événement', 0, NEW.idMembre, NULL);
END;
//

DELIMITER ;

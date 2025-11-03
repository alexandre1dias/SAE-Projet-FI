DELIMITER // -- les délimiters MySQL se présentent ainsi, avec des // ou des $$. 

CREATE TRIGGER verif_genre_competition
BEFORE INSERT ON Participer
FOR EACH ROW
BEGIN
    DECLARE genre_membre VARCHAR(255);
    DECLARE genre_competition VARCHAR(255);
    DECLARE est_competition INT;

    -- vérifier si l'événement est une compétition
    SELECT COUNT(*), sexeCO INTO est_competition, genre_competition
    FROM Competition
    WHERE idEvent = NEW.idEvenement
    GROUP BY sexeCO;

    -- si c'est une compétition (est_competition > 0)
    IF est_competition > 0 THEN
        -- on récupère le sexe du membre
        SELECT sexeM INTO genre_membre
        FROM Membre
        WHERE idMembre = NEW.idMembre;

        --si la compétition est pour 'Homme' et que le membre n'est pas 'M'
        IF genre_competition = 'Masculin' AND genre_membre != 'M' THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Inscription impossible : cette compétition est réservée aux hommes.';
        END IF;

        --si la compétition est pour 'Femme' et que le membre n'est pas 'F'
        IF genre_competition = 'Féminin' AND genre_membre != 'F' THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Inscription impossible : cette compétition est réservée aux femmes.';
        END IF;
    END IF;
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER verif_niveau_competition
BEFORE INSERT ON Participer
FOR EACH ROW
BEGIN
    DECLARE membre_niveau VARCHAR(20);
    DECLARE niveaux_competition VARCHAR(255);
    DECLARE membre_num INT;
    DECLARE est_valide INT DEFAULT 0;

    -- Vérifie si l'événement est une compétition
    SELECT niveauCO INTO niveaux_competition
    FROM Competition
    WHERE idEvent = NEW.idEvenement
    LIMIT 1;

    -- Si c'est une compétition avec des niveaux définis
    IF niveaux_competition IS NOT NULL THEN
        -- Récupère le niveau du membre
        SELECT niveau INTO membre_niveau
        FROM Membre
        WHERE idMembre = NEW.idMembre;

        -- Convertit le niveau du membre en nombre
        SET membre_num = CASE membre_niveau
            WHEN 'M9' THEN 1
            WHEN 'M11' THEN 2
            WHEN 'M13' THEN 3
            WHEN 'M15' THEN 4
            WHEN 'M17' THEN 5
            WHEN 'M20' THEN 6
            WHEN 'Senior' THEN 7
            WHEN 'Vétéran' THEN 8
            ELSE 0
        END;

        -- Vérifie si le niveau du membre ou le suivant est dans la liste des niveaux autorisés
        IF niveaux_competition LIKE CONCAT('%', membre_niveau, '%') THEN
            SET est_valide = 1;
        ELSE
        --Si ce n’est pas le cas, on teste le niveau juste superieur
            SET est_valide = CASE
                WHEN niveaux_competition LIKE CONCAT('%',
                    CASE membre_num + 1
                        WHEN 2 THEN 'M11'
                        WHEN 3 THEN 'M13'
                        WHEN 4 THEN 'M15'
                        WHEN 5 THEN 'M17'
                        WHEN 6 THEN 'M20'
                        WHEN 7 THEN 'Senior'
                        WHEN 8 THEN 'Vétéran'
                        ELSE ''
                    END, '%')
                THEN 1 ELSE 0 END;
        END IF;

        -- Si le niveau n'est pas compatible → erreur
        IF est_valide = 0 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Inscription impossible : le niveau du membre ne correspond pas à celui de la compétition.';
        END IF;
    END IF;
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER creation_membre_apres_acceptation
AFTER UPDATE ON Inscription
FOR EACH ROW
BEGIN
    -- Vérifie si l'inscription vient d'être acceptée (passe de 0 à 1)
    IF NEW.acceptée = 1 AND OLD.acceptée <> 1 THEN -- (OLD.acceptée <> 1 permet de savoir si le membre n'est pas déjà crée)
        INSERT INTO Membre (nomM, prenomM, emailM, mdp, ddnM, sexeM, date_inscription, niveau, statut, activite, IdParamNotifMembre)
        VALUES (NEW.nomI, NEW.prenomI, NEW.mailInscr, NEW.mdpI, NEW.ddnI, NEW.sexeI, NOW(), NULL, NULL, NULL, NULL);
    END IF;
END;
//

DELIMITER ;


-- NOTIFICATION POUR formulaire de contact, inscription , demande de modification 

DELIMITER //

CREATE TRIGGER notif_admin_inscription
AFTER INSERT ON Inscription
FOR EACH ROW
BEGIN
    INSERT INTO Notifs (typeN, sourceN, lue, idMembre, IdAdmin)
    VALUES ('Inscription', CONCAT('Nouvelle inscription : ', NEW.nomI, ' ', NEW.prenomI), 0, NEW.idMembre, 1); -- ici IdAdmin = 1 par exemple
    
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER notif_admin_formulaire
AFTER INSERT ON Formulaire_Contact
FOR EACH ROW
BEGIN
    INSERT INTO Notifs (typeN, sourceN, lue, idMembre, IdAdmin)
    VALUES ('Formulaire', CONCAT('Nouveau formulaire : ', NEW.sujetFC), 0, NEW.idMembre, 1);
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER notif_admin_modif
AFTER INSERT ON DemandeModif
FOR EACH ROW
BEGIN
    INSERT INTO Notifs (typeN, sourceN, lue, idMembre, IdAdmin)
    VALUES ('DemandeModification', CONCAT('Nouvelle demande de modification'), 0, NEW.idMembre, 1);
END;
//

DELIMITER ;

-- Trigger pour calculer le niveau d’un membre à partir de sa date de naissance


DELIMITER //

CREATE TRIGGER calcul_niveau_membre
BEFORE INSERT ON Membre
FOR EACH ROW
BEGIN
    DECLARE annee INT;


    SET annee = YEAR(NEW.ddnM);
    SET @age = YEAR(CURDATE()) - annee; -- Détermine l'age approximatif

    -- Détermination du niveau selon l'age
    SET NEW.niveau = CASE
        WHEN @age < 10 THEN 'M9'
        WHEN @age BETWEEN 10 AND 11 THEN 'M11'
        WHEN @age BETWEEN 12 AND 13 THEN 'M13'
        WHEN @age BETWEEN 14 AND 15 THEN 'M15'
        WHEN @age BETWEEN 16 AND 17 THEN 'M17'
        WHEN @age BETWEEN 18 AND 20 THEN 'M20'
        WHEN @age BETWEEN 21 AND 39 THEN 'Senior'
        ELSE 'Vétéran'
    END;
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER mise_a_jour_niveau_membre
BEFORE UPDATE ON Membre
FOR EACH ROW
BEGIN
    DECLARE age INT;

    SET annee = YEAR(NEW.ddnM);
    SET @age = YEAR(CURDATE()) - annee; -- Détermine l'age approximatif

    -- Détermination du niveau selon l'age
    SET NEW.niveau = CASE
        WHEN @age < 10 THEN 'M9'
        WHEN @age BETWEEN 10 AND 11 THEN 'M11'
        WHEN @age BETWEEN 12 AND 13 THEN 'M13'
        WHEN @age BETWEEN 14 AND 15 THEN 'M15'
        WHEN @age BETWEEN 16 AND 17 THEN 'M17'
        WHEN @age BETWEEN 18 AND 20 THEN 'M20'
        WHEN @age BETWEEN 21 AND 39 THEN 'Senior'
        ELSE 'Vétéran'
    END;
END;
//

DELIMITER ;


-- Quand un formulaire de contact a une réponse

DELIMITER //

CREATE TRIGGER notif_membre_reponse_formulaire
AFTER INSERT ON Repondre
FOR EACH ROW
BEGIN
    INSERT INTO Notifs (typeN, sourceN, lue, idMembre, IdAdmin)
    VALUES ('RéponseFormulaire', CONCAT('Votre formulaire a reçu une réponse'), 0, NEW.idMembre, NULL);
END;
//

DELIMITER ;

-- Quand une demande de modification est acceptée

DELIMITER //

CREATE TRIGGER notif_membre_modif_acceptee
AFTER UPDATE ON DemandeModif
FOR EACH ROW
BEGIN
    IF NEW.acceptée = 1 AND OLD.acceptée <> 1 THEN -- (OLD.acceptée <> 1 permet de savoir si la demande n'a pas déjà été acceptée)
        INSERT INTO Notifs (typeN, sourceN, lue, idMembre, IdAdmin)
        VALUES ('DemandeModif', 'Votre demande de modification a été acceptée', 0, NEW.idMembre, NULL);
    END IF;
END;
//

DELIMITER ;


-- Quand de nouveaux résultats sont ajoutés

DELIMITER //

CREATE TRIGGER notif_membre_nouveau_resultat
AFTER INSERT ON Resulter
FOR EACH ROW
BEGIN
    INSERT INTO Notifs (typeN, sourceN, lue, idMembre, IdAdmin)
    VALUES ('NouveauResultat', 'Un nouveau résultat a été ajouté', 0, NEW.idMembre, NULL);
END;
//

DELIMITER ;

-- Event Crée

DELIMITER //

CREATE TRIGGER notif_membre_evenement_cree
AFTER INSERT ON Evenement
FOR EACH ROW
BEGIN
    -- ici on notifie tous les membres
    INSERT INTO Notifs (typeN, sourceN, lue, idMembre, IdAdmin)
    SELECT 'NouvelEvenement', CONCAT('Un nouvel événement est créé'), 0, idMembre, NULL
    FROM Membre;
END;
//

DELIMITER ;

-- Event annulé 

DELIMITER //

CREATE TRIGGER notif_membre_evenement_annule
AFTER UPDATE ON Evenement
FOR EACH ROW
BEGIN
    IF NEW.annule = 1 AND OLD.annule <> 1 THEN
        INSERT INTO Notifs (typeN, sourceN, lue, idMembre, IdAdmin)
        SELECT 'EvenementAnnule', CONCAT('Un événement auquel vous étiez inscrit a été annulé'), 0, idMembre, NULL
        FROM Participer
        WHERE idEvenement = NEW.idEvenement;
    END IF;
END;
//

DELIMITER ;


-- quand un membre s'inscrit à un evenement

DELIMITER //

CREATE TRIGGER notif_membre_inscription_evenement
AFTER INSERT ON Participer
FOR EACH ROW
BEGIN
    INSERT INTO Notifs (typeN, sourceN, lue, idMembre, IdAdmin)
    VALUES ('InscriptionEvenement', 'Vous êtes inscrit à un événement', 0, NEW.idMembre, NULL);
END;
//

DELIMITER ;

DELIMITER //
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


-- Trigger pour calculer le niveau d’un membre à partir de sa date de naissance
DELIMITER //
CREATE OR REPLACE TRIGGER calcul_niveau_age_membre
BEFORE INSERT ON MEMBRE
FOR EACH ROW
BEGIN
    DECLARE calcul_age INT;
    SET calcul_age = (YEAR(CURDATE()) - YEAR(NEW.ddnM)) - (CASE WHEN DATE_FORMAT(CURDATE(), '%m%d') < DATE_FORMAT(NEW.ddnM, '%m%d') THEN 1 ELSE 0 END);
    IF NEW.niveau IS NULL THEN
        SET NEW.niveau = CASE
            WHEN calcul_age < 10 THEN 'M9'
            WHEN calcul_age BETWEEN 10 AND 11 THEN 'M11'
            WHEN calcul_age BETWEEN 12 AND 13 THEN 'M13'
            WHEN calcul_age BETWEEN 14 AND 15 THEN 'M15'
            WHEN calcul_age BETWEEN 16 AND 17 THEN 'M17'
            WHEN calcul_age BETWEEN 18 AND 19 THEN 'M20'
            WHEN calcul_age BETWEEN 20 AND 39 THEN 'Senior'
            ELSE 'Vétéran'
        END;
    END IF;
    IF NEW.age IS NULL THEN
        SET NEW.age = calcul_age;
    END IF;
END;
//
DELIMITER ;


DELIMITER //
CREATE OR REPLACE TRIGGER mise_a_jour_niveau_age_membre
BEFORE UPDATE ON MEMBRE
FOR EACH ROW
BEGIN
    DECLARE calcul_age INT;
    IF NEW.ddnM != OLD.ddnM THEN
        SET calcul_age = (YEAR(CURDATE()) - YEAR(NEW.ddnM)) - (CASE WHEN DATE_FORMAT(CURDATE(), '%m%d') < DATE_FORMAT(NEW.ddnM, '%m%d') THEN 1 ELSE 0 END);

        SET NEW.niveau = CASE
            WHEN calcul_age < 10 THEN 'M9'
            WHEN calcul_age BETWEEN 10 AND 11 THEN 'M11'
            WHEN calcul_age BETWEEN 12 AND 13 THEN 'M13'
            WHEN calcul_age BETWEEN 14 AND 15 THEN 'M15'
            WHEN calcul_age BETWEEN 16 AND 17 THEN 'M17'
            WHEN calcul_age BETWEEN 18 AND 19 THEN 'M20'
            WHEN calcul_age BETWEEN 20 AND 39 THEN 'Senior'
            ELSE 'Vétéran'
        END;
        SET NEW.age = calcul_age;
    END IF;
END;
//
DELIMITER ;


DELIMITER //
create or replace trigger date_inscription before insert on INSCRIPTION for each ROW
begin
    if New.dateInscription IS NULL THEN
        set New.dateInscription = CURDATE();
    end if;
end;
//
DELIMITER ;

-- definie compétition comme passée si sa date de fin est plus petite qu'aujourd'hui
DELIMITER //
-- Création de l'événement planifié
CREATE OR REPLACE EVENT mettre_a_jour_statut_competition
ON SCHEDULE EVERY 1 MINUTE STARTS NOW()
DO
BEGIN
    -- Met à jour la colonne 'passeeCO' à vrai (1) pour toutes les compétitions
    -- dont la date de fin est antérieure à la date actuelle
    -- et qui ne sont pas déjà marquées comme passées.
    UPDATE COMPETITION
    SET passeeCO = 1
    WHERE dateFinCO < CURDATE() AND (passeeCO = 0 OR passeeCO IS NULL);
END;
//
DELIMITER ;

DELIMITER //
-- Trigger pour vérifier si les rôles de président et vice-president sont unique lors de l'INSERTION d'un nouveau membre
CREATE OR REPLACE TRIGGER verif_role_unique_insert
BEFORE INSERT ON MEMBRE
FOR EACH ROW
BEGIN
    DECLARE president_cpt INT;
    DECLARE vice_president_cpt INT;

    -- Vérifier si on essaie d'insérer un Président
    IF NEW.statut = 'Président' THEN
        SELECT COUNT(*) INTO president_cpt FROM MEMBRE WHERE statut = 'Président';
        IF president_cpt > 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Un président est déjà désigné. Impossible d''en ajouter un second.';
        END IF;
    END IF;

    -- Vérifier si on essaie d'insérer un Vice-Président
    IF NEW.statut = 'Vice-Président' THEN
        SELECT COUNT(*) INTO vice_president_cpt FROM MEMBRE WHERE statut = 'Vice-Président';
        IF vice_president_cpt > 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Un vice-président est déjà désigné. Impossible d''en ajouter un second.';
        END IF;
    END IF;
END;
//
DELIMITER ;

DELIMITER //
-- Trigger pour vérifier si les rôles de président et vice-president sont unique lors de l'UPDATE d'un membre
CREATE OR REPLACE TRIGGER verif_role_unique_update
BEFORE UPDATE ON MEMBRE
FOR EACH ROW
BEGIN
    DECLARE president_cpt INT;
    DECLARE vice_president_cpt INT;

    -- On vérifie uniquement si le statut est MODIFIÉ pour devenir 'Président'
    IF NEW.statut = 'Président' AND NEW.statut != OLD.statut THEN -- on vérifie la modification du statut
        SELECT COUNT(*) INTO president_cpt FROM MEMBRE WHERE statut = 'Président';
        IF president_cpt > 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Un président est déjà désigné. Impossible de nommer un second président.';
        END IF;
    END IF;

    -- On vérifie uniquement si le statut est MODIFIÉ pour devenir 'Vice-Président'
    IF NEW.statut = 'Vice-Président' AND NEW.statut != OLD.statut THEN -- on vérifie la modification du statut
        SELECT COUNT(*) INTO vice_president_cpt FROM MEMBRE WHERE statut = 'Vice-Président';
        IF vice_president_cpt > 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Un vice-président est déjà désigné. Impossible de nommer un second vice-président.';
        END IF;
    END IF;
END;
//
DELIMITER ;
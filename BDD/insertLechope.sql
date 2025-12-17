-- ============================================================
-- SCRIPT CORRECTIF POUR CHRISTOPHE LECHOPIER (ID 8)
-- ============================================================

SET FOREIGN_KEY_CHECKS=0;

-- 1. NETTOYAGE PRÉALABLE (Pour éviter les doublons si on relance)
DELETE FROM PARTICIPER WHERE idEvent BETWEEN 47 AND 76;
DELETE FROM COMPETITION WHERE idEvent BETWEEN 47 AND 76;
DELETE FROM REUNION WHERE idEvent BETWEEN 47 AND 76;
DELETE FROM EVENTCLUB WHERE idEvent BETWEEN 47 AND 76;
DELETE FROM EVENEMENT WHERE idEvent BETWEEN 47 AND 76;

-- 2. MISE À JOUR DE SÉCURITÉ DU MEMBRE
-- On s'assure que Christophe a bien le niveau Vétéran pour correspondre aux compétitions
UPDATE MEMBRE 
SET niveau = 'Vétéran' 
WHERE idMembre = 8;

-- 3. CRÉATION DES ID DANS LA TABLE MÈRE (EVENEMENT)
INSERT INTO EVENEMENT () VALUES 
(), (), (), (), (), (), (), (), (), (), -- 47 à 56 (Compétitions)
(), (), (), (), (), (), (), (), (), (), -- 57 à 66 (Réunions)
(), (), (), (), (), (), (), (), (), (); -- 67 à 76 (EventClub)

-- ============================================================
-- 4. INSERTION DES COMPÉTITIONS (ID 47-56)
-- CORRECTION : Toutes passées en 'Vétéran' pour éviter l'erreur 1644
-- ============================================================
INSERT INTO COMPETITION (nomCO, villeCO, adresseCO, dateDebutCO, heureDebutCO, dateFinCO, heureFinCO, typeArmeCO, sexeCO, typeCompete, descriptionCO, niveauCO, classementCO, passeeCO, idEvent) VALUES
('Circuit National Vétéran 1', 'Saint-Denis', 'Rue de la Légion', '2025-10-05', '08:00', '2025-10-06', '18:00', 'Épée', 'Homme', 'National', 'Premier circuit national vétéran de la saison.', 'Vétéran', NULL, 0, 47),
('Tournoi des Maîtres', 'Levallois', 'Place G. Pompidou', '2025-11-15', '09:00', '2025-11-15', '19:00', 'Épée', 'Homme', 'Régional', 'Tournoi open vétéran.', 'Vétéran', NULL, 0, 48), -- Corrigé ici (Senior -> Vétéran)
('Championnat de Ligue Vétéran', 'Orléans', '123 Rue du Sport', '2026-01-20', '08:30', '2026-01-20', '17:00', 'Épée', 'Homme', 'Régional', 'Championnat régional pour la qualif.', 'Vétéran', NULL, 0, 49),
('Challenge du Vignoble', 'Bordeaux', 'Av. des Vignes', '2026-02-10', '09:00', '2026-02-11', '16:00', 'Épée', 'Homme', 'National', 'Grand tournoi convivial vétérans.', 'Vétéran', NULL, 0, 50),
('Open de la Cité', 'Carcassonne', 'Remparts Sud', '2026-03-05', '08:00', '2026-03-06', '18:00', 'Épée', 'Homme', 'National', 'Circuit national Épée Homme Vétéran.', 'Vétéran', NULL, 0, 51),
('Tournoi Inter-Clubs', 'Tours', '456 Avenue de la Victoire', '2026-04-12', '10:00', '2026-04-12', '18:00', 'Épée', 'Homme', 'Régional', 'Rencontre amicale par équipes.', 'Vétéran', NULL, 0, 52),
('Championnat de France Vétéran', 'Nantes', 'Salle Mangin', '2026-05-20', '08:00', '2026-05-21', '20:00', 'Épée', 'Homme', 'National', 'L''événement majeur de la saison vétéran.', 'Vétéran', NULL, 0, 53),
('Mémorial du Doyen', 'Chartres', '5 Boulevard de la Liberté', '2026-06-15', '09:00', '2026-06-15', '17:00', 'Épée', 'Homme', 'Régional', 'Tournoi de fin de saison.', 'Vétéran', NULL, 0, 54),
('Circuit Européen EVF', 'Thionville', 'Gymnase Municipal', '2026-10-10', '08:00', '2026-10-12', '18:00', 'Épée', 'Homme', 'International', 'Étape du circuit européen vétérans.', 'Vétéran', NULL, 0, 55),
('Coupe d''Automne', 'Blois', '1 Rue de la Halle', '2026-11-22', '09:00', '2026-11-22', '18:00', 'Épée', 'Homme', 'Régional', 'Préparation pour la nouvelle saison.', 'Vétéran', NULL, 0, 56);

-- ============================================================
-- 5. INSERTION DES RÉUNIONS (ID 57-66)
-- ============================================================
INSERT INTO REUNION (nomRE, villeRE, adresseRE, dateDebutRE, heureDebutRE, dateFinRE, heureFinRE, nbParticipantsRE, typeReunionRE, rapportRE, niveauRE, idEvent) VALUES
('Comité Directeur - Rentrée', 'Orléans', 'Salle du Club', '2025-09-05', '19:00', '2025-09-05', '21:00', 12, 'Comité', 'Validé', 'Comité', 57),
('Commission Finances', 'Orléans', 'Bureau Trésorier', '2025-10-12', '18:30', '2025-10-12', '20:30', 5, 'Commission', 'En cours', 'Comité', 58),
('Réunion Prépa Tournoi', 'Orléans', 'Salle d''armes', '2025-11-02', '20:00', '2025-11-02', '22:00', 20, 'Organisation', 'Fait', 'Bénévoles', 59),
('AG Ordinaire 2025', 'Orléans', 'Salle Polyvalente', '2025-12-15', '10:00', '2025-12-15', '12:00', 50, 'Assemblée', 'Validé', 'Tous', 60),
('Comité Directeur - Hiver', 'Orléans', 'Salle du Club', '2026-01-10', '19:00', '2026-01-10', '21:00', 12, 'Comité', NULL, 'Comité', 61),
('Réunion Mairie', 'Orléans', 'Hôtel de Ville', '2026-02-20', '14:00', '2026-02-20', '15:30', 4, 'Externe', NULL, 'Bureau', 62),
('Commission Partenariats', 'Orléans', 'Visio', '2026-03-15', '18:00', '2026-03-15', '19:30', 6, 'Commission', NULL, 'Comité', 63),
('Comité Directeur - Printemps', 'Orléans', 'Salle du Club', '2026-04-10', '19:30', '2026-04-10', '21:30', 12, 'Comité', NULL, 'Comité', 64),
('Orga Fête du Club 2026', 'Orléans', 'Club House', '2026-05-25', '20:00', '2026-05-25', '22:00', 15, 'Organisation', NULL, 'Bénévoles', 65),
('AG Élective', 'Orléans', 'Gymnase', '2026-06-28', '10:00', '2026-06-28', '13:00', 60, 'Assemblée', NULL, 'Tous', 66);

-- ============================================================
-- 6. INSERTION DES EVENTCLUB (ID 67-76)
-- ============================================================
INSERT INTO EVENTCLUB (NomEV, villeEV, adresseEV, dateDebutEV, heureDebutEV, dateFinEV, heureFinEV, nbParticipantEV, descriptionEV, niveauxEV, passeeEV, idEvent) VALUES
('Pot de Rentrée 2025', 'Orléans', 'Club House', '2025-09-08', '18:00', '2025-09-08', '20:00', 40, 'Accueil des nouveaux adhérents.', 'Tous', 0, 67),
('Journée Portes Ouvertes 25', 'Orléans', 'Gymnase', '2025-09-15', '09:00', '2025-09-15', '17:00', 100, 'Démonstrations pour le public.', 'Tous', 0, 68),
('Soirée Beaujolais 2025', 'Orléans', 'Club House', '2025-11-21', '20:00', '2025-11-21', '23:00', 30, 'Dégustation conviviale adultes.', 'Adulte', 0, 69),
('Stage Arbitrage Club', 'Orléans', 'Salle Vidéo', '2025-12-05', '19:00', '2025-12-05', '21:00', 10, 'Formation des jeunes arbitres (Encadrant).', 'M15,M17,M20', 0, 70),
('Galette des Rois 2026', 'Orléans', 'Club House', '2026-01-12', '16:00', '2026-01-12', '18:00', 50, 'Moment convivial.', 'Tous', 0, 71),
('Réparation Matériel', 'Orléans', 'Atelier', '2026-02-15', '09:00', '2026-02-15', '12:00', 8, 'Entretien des pistes et fils.', 'Bénévole', 0, 72),
('Soirée Fondue', 'Orléans', 'Restaurant', '2026-03-20', '20:00', '2026-03-20', '23:00', 25, 'Repas section Loisir/Vétéran.', 'Adulte', 0, 73),
('Barbecue Fin Saison 26', 'Orléans', 'Jardin', '2026-06-20', '19:00', '2026-06-20', '23:00', 80, 'Grande fête de clôture.', 'Tous', 0, 74),
('Forum des Assos 2026', 'Orléans', 'Parc Expos', '2026-09-06', '08:00', '2026-09-06', '18:00', 10, 'Tenue du stand du club.', 'Bénévole', 0, 75),
('Sortie Accrobranche', 'Orléans', 'Forêt', '2026-09-20', '14:00', '2026-09-20', '17:00', 20, 'Journée cohésion.', 'Tous', 0, 76);

-- ============================================================
-- 7. INSERTION DES PARTICIPATIONS (ID 8 = Christophe)
-- ============================================================
INSERT INTO PARTICIPER (idMembre, idEvent) VALUES
-- Compétitions (Vétéran)
(8, 47), (8, 48), (8, 49), (8, 50), (8, 51), 
(8, 52), (8, 53), (8, 54), (8, 55), (8, 56),
-- Réunions (Membre du Comité)
(8, 57), (8, 58), (8, 59), (8, 60), (8, 61), 
(8, 62), (8, 63), (8, 64), (8, 65), (8, 66),
-- EventClub (Vie du club)
(8, 67), (8, 68), (8, 69), (8, 70), (8, 71), 
(8, 72), (8, 73), (8, 74), (8, 75), (8, 76);

SET FOREIGN_KEY_CHECKS=1;
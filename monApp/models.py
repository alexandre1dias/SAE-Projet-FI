class Parametre_Notif_Admin:
    """Représente les paramètres de notification pour un administrateur."""
    def __init__(self, IdParamNotifAdmin, formulaireDemandeSite, formulaireDemandeMail, formulaireQuestionSite, formulaireQuestionMail, formulaireSignalementSite, formulaireSignalementMail, demandeModifSite, demandeModifMail, demandeInscriptionSite, demandeInscriptionMail, IdAdmin):
        """
        Initialise les paramètres de notification d'un administrateur.

        Args:
            IdParamNotifAdmin (int): L'identifiant unique des paramètres.
            formulaireDemandeSite (bool): Notification site pour une demande.
            formulaireDemandeMail (bool): Notification mail pour une demande.
            formulaireQuestionSite (bool): Notification site pour une question.
            formulaireQuestionMail (bool): Notification mail pour une question.
            formulaireSignalementSite (bool): Notification site pour un signalement.
            formulaireSignalementMail (bool): Notification mail pour un signalement.
            demandeModifSite (bool): Notification site pour une demande de modification.
            demandeModifMail (bool): Notification mail pour une demande de modification.
            demandeInscriptionSite (bool): Notification site pour une demande d'inscription.
            demandeInscriptionMail (bool): Notification mail pour une demande d'inscription.
            IdAdmin (int): L'identifiant de l'administrateur associé.
        """
        self.IdParamNotifAdmin = IdParamNotifAdmin
        self.formulaireDemandeSite = formulaireDemandeSite
        self.formulaireDemandeSite = formulaireDemandeSite
        self.formulaireDemandeMail = formulaireDemandeMail
        self.formulaireQuestionSite = formulaireQuestionSite
        self.formulaireQuestionMail = formulaireQuestionMail
        self.formulaireSignalementSite = formulaireSignalementSite
        self.formulaireSignalementMail = formulaireSignalementMail
        self.demandeModifSite = demandeModifSite
        self.demandeModifMail = demandeModifMail
        self.demandeInscriptionSite = demandeInscriptionSite
        self.demandeInscriptionMail = demandeInscriptionMail
        self.IdAdmin = IdAdmin

class Parametre_Notif_Membre:
    """Représente les paramètres de notification pour un membre."""
    def __init__(self, IdParamNotifMembre, eventInscriptionSite, eventInscriptionMail, eventNouveauSite, eventNouveauMail, eventAnnulationSite, eventAnnulationMail, resultatNouveauSite, resultatNouveauMail, reponseFormulaireSite, reponseFormulaireMail, modifProfilSite, modifProfilMail, idMembre):
        """
        Initialise les paramètres de notification d'un membre.

        Args:
            IdParamNotifMembre (int): L'identifiant unique des paramètres.
            eventInscriptionSite (bool): Notification site pour l'inscription à un événement.
            eventInscriptionMail (bool): Notification mail pour l'inscription à un événement.
            eventNouveauSite (bool): Notification site pour un nouvel événement.
            eventNouveauMail (bool): Notification mail pour un nouvel événement.
            eventAnnulationSite (bool): Notification site pour l'annulation d'un événement.
            eventAnnulationMail (bool): Notification mail pour l'annulation d'un événement.
            resultatNouveauSite (bool): Notification site pour un nouveau résultat.
            resultatNouveauMail (bool): Notification mail pour un nouveau résultat.
            reponseFormulaireSite (bool): Notification site pour une réponse à un formulaire.
            reponseFormulaireMail (bool): Notification mail pour une réponse à un formulaire.
            modifProfilSite (bool): Notification site pour une modification de profil.
            modifProfilMail (bool): Notification mail pour une modification de profil.
            idMembre (int): L'identifiant du membre associé.
        """
        self.IdParamNotifMembre = IdParamNotifMembre
        self.eventInscriptionSite = eventInscriptionSite
        self.eventInscriptionMail = eventInscriptionMail
        self.eventNouveauSite = eventNouveauSite
        self.eventNouveauMail = eventNouveauMail
        self.eventAnnulationSite = eventAnnulationSite
        self.eventAnnulationMail = eventAnnulationMail
        self.resultatNouveauSite = resultatNouveauSite
        self.resultatNouveauMail = resultatNouveauMail
        self.reponseFormulaireSite = reponseFormulaireSite
        self.reponseFormulaireMail = reponseFormulaireMail
        self.modifProfilSite = modifProfilSite
        self.modifProfilMail = modifProfilMail
        self.idMembre = idMembre

class Notifs:
    """Représente une notification."""
    def __init__(self, IdNotifs, typeN, sourceN, lue, idMembre , IdAdmin):
        """
        Initialise une notification.

        Args:
            IdNotifs (int): L'identifiant unique de la notification.
            typeN (str): Le type de la notification.
            sourceN (str): La source (le créateur) de la notification.
            lue (bool): Indique si la notification a été lue.
            idMembre (int): L'identifiant du membre destinataire (si applicable).
            IdAdmin (int): L'identifiant de l'administrateur destinataire (si applicable).
        """
        self.IdNotifs = IdNotifs
        self.typeN = typeN
        self.sourceN = sourceN
        self.lue = lue
        self.idMembre = idMembre
        self.IdAdmin = IdAdmin


class RecevoirM:
    """Table d'association entre un membre et une notification."""
    def __init__(self, idMembre, idNotifs):
        """
        Initialise la relation entre un membre et une notification.

        Args:
            idMembre (int): L'identifiant du membre.
            idNotifs (int): L'identifiant de la notification.
        """
        self.idMembre = idMembre
        self.idNotifs = idNotifs

class RecevoirA:
    """Table d'association entre un administrateur et une notification."""
    def __init__(self, idAdmin, idNotifs):
        """
        Initialise la relation entre un administrateur et une notification.

        Args:
            idAdmin (int): L'identifiant de l'administrateur.
            idNotifs (int): L'identifiant de la notification.
        """
        self.idAdmin = idAdmin
        self.idNotifs = idNotifs

class Membre:
    """Représente un membre du club."""
    def __init__(self, idMembre, nomM, prenomM, emailM, mdp, date_inscription, sexeM, ddnM, niveau, statut, activite, IdParamNotifMembre):
        """
        Initialise un membre.

        Args:
            idMembre (int): L'identifiant unique du membre.
            nomM (str): Le nom du membre.
            prenomM (str): Le prénom du membre.
            emailM (str): L'adresse email du membre.
            mdp (str): Le mot de passe haché du membre.
            date_inscription (date): La date d'inscription du membre.
            sexeM (str): Le sexe du membre.
            ddnM (date): La date de naissance du membre.
            niveau (str): Le niveau du membre (ex: M9, Senior).
            statut (str): Le statut du membre (ex: Membre, Président).
            activite (bool): Indique si le membre est actif.
            IdParamNotifMembre (int): L'identifiant des paramètres de notification du membre.
        """
        self.idMembre = idMembre
        self.nomM = nomM
        self.prenomM = prenomM
        self.emailM = emailM
        self.mdp = mdp
        self.date_inscription = date_inscription
        self.sexeM = sexeM
        self.ddnM = ddnM
        self.niveau = niveau
        self.statut = statut
        self.activite = activite
        self.IdParamNotifMembre = IdParamNotifMembre

class Admin:
    """Représente un administrateur du système."""
    def __init__(self, IdAdmin, emailA, mdpA, IdParamNotifAdmin):
        """
        Initialise un administrateur.

        Args:
            IdAdmin (int): L'identifiant unique de l'administrateur.
            emailA (str): L'adresse email de l'administrateur.
            mdpA (str): Le mot de passe haché de l'administrateur.
            IdParamNotifAdmin (int): L'identifiant des paramètres de notification de l'administrateur.
        """
        self.IdAdmin = IdAdmin
        self.emailA = emailA
        self.mdpA = mdpA
        self.IdParamNotifAdmin = IdParamNotifAdmin


class Formulaire_Contact:
    """Représente une soumission de formulaire de contact."""
    def __init__(self, idFormulaire, typeFC, sujetFC, mailFC, descriptionFC, dateFC, idMembre , IdAdmin):
        """
        Initialise un formulaire de contact.

        Args:
            idFormulaire (int): L'identifiant unique du formulaire.
            typeFC (str): Le type de formulaire (ex: Question, Signalement).
            sujetFC (str): Le sujet du formulaire.
            mailFC (str): L'email de la personne qui a soumis le formulaire.
            descriptionFC (str): Le contenu du message.
            dateFC (date): La date de soumission.
            idMembre (int): L'identifiant du membre qui a rempli (si applicable).
            IdAdmin (int): L'identifiant de l'admin qui a répondu (si applicable).
        """
        self.idFormulaire = idFormulaire
        self.typeFC = typeFC
        self.sujetFC = sujetFC
        self.mailFC = mailFC
        self.descriptionFC = descriptionFC
        self.dateFC = dateFC
        self.idMembre = idMembre
        self.IdAdmin = IdAdmin


class Repondre:
    """Table d'association entre un administrateur et un formulaire auquel il a répondu."""
    def __init__(self, idAdmin, idFormulaire):
        """
        Initialise la relation entre un admin et un formulaire.

        Args:
            idAdmin (int): L'identifiant de l'administrateur.
            idFormulaire (int): L'identifiant du formulaire.
        """
        self.idAdmin = idAdmin
        self.idFormulaire = idFormulaire

class Remplir:
    """Table d'association entre un membre et un formulaire qu'il a rempli."""
    def __init__(self, idMembre, idFormulaire):
        """
        Initialise la relation entre un membre et un formulaire.

        Args:
            idMembre (int): L'identifiant du membre.
            idFormulaire (int): L'identifiant du formulaire.
        """
        self.idMembre = idMembre
        self.idFormulaire = idFormulaire

class Inscription:
    """Représente une demande d'inscription."""
    def __init__(self, idInscription, mailInscr, nomI, prenomI, ddnI, mdpI, sexeI, acceptée, idMembre):
        """
        Initialise une demande d'inscription.

        Args:
            idInscription (int): L'identifiant unique de la demande.
            mailInscr (str): L'email pour l'inscription.
            nomI (str): Le nom de la personne.
            prenomI (str): Le prénom de la personne.
            ddnI (date): La date de naissance.
            mdpI (str): Le mot de passe choisi (haché).
            sexeI (str): Le sexe de la personne.
            acceptée (bool): Indique si la demande a été acceptée.
            idMembre (int): L'identifiant du membre créé après acceptation.
        """
        self.idInscription = idInscription
        self.mailInscr = mailInscr
        self.nomI = nomI
        self.prenomI = prenomI
        self.ddnI = ddnI
        self.mdpI = mdpI
        self.sexeI = sexeI
        self.acceptée = acceptée
        self.idMembre = idMembre


class Generer:
    """Table d'association entre un membre et sa demande d'inscription."""
    def __init__(self, idMembre, idInscription):
        """
        Initialise la relation entre un membre et une inscription.

        Args:
            idMembre (int): L'identifiant du membre.
            idInscription (int): L'identifiant de la demande d'inscription.
        """
        self.idMembre = idMembre
        self.idInscription = idInscription

class Evenement:
    """Représente un événement générique (sert de classe mère)."""
    def __init__(self, idEvenement):
        """
        Initialise un événement.

        Args:
            idEvenement (int): L'identifiant unique de l'événement.
        """
        self.idEvenement = idEvenement

class Participer:
    """Table d'association entre un membre et un événement auquel il participe."""
    def __init__(self, idMembre, idEvenement):
        """
        Initialise la participation d'un membre à un événement.

        Args:
            idMembre (int): L'identifiant du membre.
            idEvenement (int): L'identifiant de l'événement.
        """
        self.idMembre = idMembre
        self.idEvenement = idEvenement

class Entrainement:
    """Représente une session d'entraînement."""
    def __init__(self,  idEntrainement, jourEN, lieuEN, dateEN, heureDebutEN, heureFinEN, typeArmeEN, niveauxEN, idEvent):
        """
        Initialise un entraînement.

        Args:
            idEntrainement (int): L'identifiant unique de l'entraînement.
            jourEN (str): Le jour de la semaine.
            lieuEN (str): Le lieu de l'entraînement.
            dateEN (date): La date de l'entraînement.
            heureDebutEN (time): L'heure de début.
            heureFinEN (time): L'heure de fin.
            typeArmeEN (str): Le type d'arme (Fleuret, Épée, Sabre).
            niveauxEN (str): Les niveaux concernés.
            idEvent (int): L'identifiant de l'événement parent.
        """
        self.idEntrainement = idEntrainement
        self.jourEN = jourEN
        self.lieuEN = lieuEN
        self.dateEN = dateEN
        self.heureDebutEN = heureDebutEN
        self.heureFinEN = heureFinEN
        self.typeArmeEN = typeArmeEN
        self.niveauxEN = niveauxEN
        self.idEvent = idEvent

class Reunion:
    """Représente une réunion."""
    def __init__(self, idReunionu, nomRE, lieuRE,  dateRE, heureDebutRE, nbParticipantRE, typeReunionRE, rapportRE, niveauxRE, idEvent):
        """
        Initialise une réunion.

        Args:
            idReunionu (int): L'identifiant unique de la réunion.
            nomRE (str): Le nom de la réunion.
            lieuRE (str): Le lieu de la réunion.
            dateRE (date): La date de la réunion.
            heureDebutRE (time): L'heure de début.
            nbParticipantRE (int): Le nombre de participants.
            typeReunionRE (str): Le type de réunion (ex: AG, Comité).
            rapportRE (str): Le rapport ou compte-rendu de la réunion.
            niveauxRE (str): Les niveaux concernés.
            idEvent (int): L'identifiant de l'événement parent.
        """
        self.idReunionu = idReunionu
        self.nomRE = nomRE
        self.lieuRE = lieuRE
        self.dateRE = dateRE
        self.heureDebutRE = heureDebutRE
        self.nbParticipantRE = nbParticipantRE
        self.typeReunionRE = typeReunionRE
        self.rapportRE = rapportRE
        self.niveauxRE = niveauxRE
        self.idEvent = idEvent
    
class Competition:
    """Représente une compétition."""
    def __init__(self, idCompete, NomCO, villeCO, adresseCO, dateDebutCO, heureDebutCO, dateFinCO, heureFinCO, typeArmeCO, nbParticipantCO, sexeCO, typeCompete, DescriptionCO, niveauxCO, classementCO, idEvent):
        """
        Initialise une compétition.

        Args:
            idCompete (int): L'identifiant unique de la compétition.
            NomCO (str): Le nom de la compétition.
            villeCO (str): La ville où se déroule la compétition.
            adresseCO (str): L'adresse de la compétition.
            dateDebutCO (date): La date de début.
            heureDebutCO (time): L'heure de début.
            dateFinCO (date): La date de fin.
            heureFinCO (time): L'heure de fin.
            typeArmeCO (str): Le type d'arme.
            nbParticipantCO (int): Le nombre de participants.
            sexeCO (str): Le sexe concerné (Masculin, Féminin, Mixte).
            typeCompete (str): Le type de compétition (Régionale, Nationale).
            DescriptionCO (str): La description de la compétition.
            niveauxCO (str): Les niveaux concernés.
            classementCO (str): Le classement final.
            idEvent (int): L'identifiant de l'événement parent.
        """
        self.idCompete = idCompete
        self.NomCO = NomCO
        self.villeCO = villeCO
        self.adresseCO = adresseCO
        self.dateDebutCO = dateDebutCO
        self.heureDebutCO = heureDebutCO
        self.dateFinCO = dateFinCO
        self.heureFinCO = heureFinCO
        self.typeArmeCO = typeArmeCO
        self.nbParticipantCO = nbParticipantCO
        self.sexeCO = sexeCO
        self.typeCompete = typeCompete
        self.DescriptionCO = DescriptionCO
        self.niveauxCO = niveauxCO
        self.classementCO = classementCO
        self.idEvent = idEvent
    
class EventClub:
    """Représente un événement interne au club."""
    def __init__(self,  idEventClub, NomEV, villeEV, adresseEV, dateDebutEV, heureDebutEV, dateFinEV, nbParticipantEV, descriptionEV, niveauxEV, idEvent):
        """
        Initialise un événement de club.

        Args:
            idEventClub (int): L'identifiant unique de l'événement.
            NomEV (str): Le nom de l'événement.
            villeEV (str): La ville de l'événement.
            adresseEV (str): L'adresse de l'événement.
            dateDebutEV (date): La date de début.
            heureDebutEV (time): L'heure de début.
            dateFinEV (date): La date de fin.
            nbParticipantEV (int): Le nombre de participants.
            descriptionEV (str): La description de l'événement.
            niveauxEV (str): Les niveaux concernés.
            idEvent (int): L'identifiant de l'événement parent.
        """
        self.idEventClub = idEventClub
        self.NomEV = NomEV
        self.villeEV = villeEV
        self.adresseEV = adresseEV
        self.dateDebutEV = dateDebutEV
        self.heureDebutEV = heureDebutEV
        self.dateFinEV = dateFinEV
        self.nbParticipantEV = nbParticipantEV
        self.descriptionEV = descriptionEV
        self.niveauxEV = niveauxEV
        self.idEvent = idEvent
    
class Resultat:
    """Représente le résultat d'un membre à une compétition."""
    def __init__(self, idResultat, resultat, dateRE, typeArmeRE, typeCompete, idEvent, idMembre):
        """
        Initialise un résultat.

        Args:
            idResultat (int): L'identifiant unique du résultat.
            resultat (str): Le résultat obtenu (ex: 1er, 5ème).
            dateRE (date): La date du résultat.
            typeArmeRE (str): Le type d'arme.
            typeCompete (str): Le type de compétition.
            idEvent (int): L'identifiant de l'événement (compétition) associé.
            idMembre (int): L'identifiant du membre associé.
        """
        self.idResultat = idResultat
        self.resultat = resultat
        self.dateRE = dateRE
        self.typeArmeRE = typeArmeRE
        self.typeCompete = typeCompete
        self.idEvent = idEvent
        self.idMembre = idMembre

class Resulter:
    """Table d'association entre un membre et un résultat."""
    def __init__(self, idMembre, idResultat):
        """
        Initialise la relation entre un membre et un résultat.

        Args:
            idMembre (int): L'identifiant du membre.
            idResultat (int): L'identifiant du résultat.
        """
        self.idMembre = idMembre
        self.idResultat = idResultat

class Avoir:
    """Table d'association entre un résultat et un membre (relation inverse de Resulter)."""
    def __init__(self, idResultat, idMembre):
        """
        Initialise la relation entre un résultat et un membre.

        Args:
            idResultat (int): L'identifiant du résultat.
            idMembre (int): L'identifiant du membre.
        """
        self.idResultat = idResultat
        self.idMembre = idMembre

class Image:
    """Représente une image."""
    def __init__(self, idImage, urlI, privee, alt):
        """
        Initialise une image.

        Args:
            idImage (int): L'identifiant unique de l'image.
            urlI (str): L'URL de l'image.
            privee (bool): Indique si l'image est privée.
            alt (str): Le texte alternatif de l'image.
        """
        self.idImage = idImage
        self.urlI = urlI
        self.privee = privee
        self.alt = alt

class ImageC:
    """Table d'association entre une image et une compétition."""
    def __init__(self, idImage, idCompete):
        """
        Initialise la relation entre une image et une compétition.

        Args:
            idImage (int): L'identifiant de l'image.
            idCompete (int): L'identifiant de la compétition.
        """
        self.idImage = idImage
        self.idCompete = idCompete

class ImageE:
    """Table d'association entre une image et un événement de club."""
    def __init__(self, idImage, idEventClub):
        """
        Initialise la relation entre une image et un événement de club.

        Args:
            idImage (int): L'identifiant de l'image.
            idEventClub (int): L'identifiant de l'événement de club.
        """
        self.idImage = idImage
        self.idEventClub = idEventClub

class Actualite:
    """Représente une actualité ou un article."""
    def __init__(self, idActualité, dateAC, heureAC, nomAC, catégorieAC):
        """
        Initialise une actualité.

        Args:
            idActualité (int): L'identifiant unique de l'actualité.
            dateAC (date): La date de publication.
            heureAC (time): L'heure de publication.
            nomAC (str): Le titre de l'actualité.
            catégorieAC (str): La catégorie de l'actualité.
        """
        self.idActualité = idActualité
        self.dateAC = dateAC
        self.heureAC = heureAC
        self.nomAC = nomAC
        self.catégorieAC = catégorieAC

class ImageA:
    """Table d'association entre une image et une actualité."""
    def __init__(self, idImage, idActualité):
        """
        Initialise la relation entre une image et une actualité.

        Args:
            idImage (int): L'identifiant de l'image.
            idActualité (int): L'identifiant de l'actualité.
        """
        self.idImage = idImage
        self.idActualité = idActualité

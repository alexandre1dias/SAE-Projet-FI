class Parametre_Notif_Admin:
    def __init__(self, IdParamNotifAdmin, formulaireDemandeSite, formulaireDemandeMail, formulaireQuestionSite, formulaireQuestionMail, formulaireSignalementSite, formulaireSignalementMail, demandeModifSite, demandeModifMail, demandeInscriptionSite, demandeInscriptionMail, IdAdmin):
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
    def __init__(self, IdParamNotifMembre, eventInscriptionSite, eventInscriptionMail, eventNouveauSite, eventNouveauMail, eventAnnulationSite, eventAnnulationMail, resultatNouveauSite, resultatNouveauMail, reponseFormulaireSite, reponseFormulaireMail, modifProfilSite, modifProfilMail, idMembre):
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
    def __init__(self, IdNotifs, typeN, sourceN, lue, idMembre , IdAdmin):
        self.IdNotifs = IdNotifs
        self.typeN = typeN
        self.sourceN = sourceN
        self.lue = lue
        self.idMembre = idMembre
        self.IdAdmin = IdAdmin


class RecevoirM:
    def __init__(self, idMembre, idNotifs):
        self.idMembre = idMembre
        self.idNotifs = idNotifs

class RecevoirA:
    def __init__(self, idAdmin, idNotifs):
        self.idAdmin = idAdmin
        self.idNotifs = idNotifs

class Membre:
    def __init__(self, idMembre, nomM, prenomM, emailM, mdp, date_inscription, sexeM, ddnM, niveau, statut, activite, IdParamNotifMembre):
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
    def __init__(self, IdAdmin, emailA, mdpA, IdParamNotifAdmin):
        self.IdAdmin = IdAdmin
        self.emailA = emailA
        self.mdpA = mdpA
        self.IdParamNotifAdmin = IdParamNotifAdmin


class Formulaire_Contact:
    def __init__(self, idFormulaire, typeFC, sujetFC, mailFC, descriptionFC, dateFC, idMembre , IdAdmin):
        self.idFormulaire = idFormulaire
        self.typeFC = typeFC
        self.sujetFC = sujetFC
        self.mailFC = mailFC
        self.descriptionFC = descriptionFC
        self.dateFC = dateFC
        self.idMembre = idMembre
        self.IdAdmin = IdAdmin


class Repondre:
    def __init__(self, idAdmin, idFormulaire):
        self.idAdmin = idAdmin
        self.idFormulaire = idFormulaire

class Remplir:
    def __init__(self, idMembre, idFormulaire):
        self.idMembre = idMembre
        self.idFormulaire = idFormulaire

class Inscription:
    def __init__(self, idInscription, mailInscr, nomI, prenomI, ddnI, mdpI, sexeI, acceptée, idMembre):
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
    def __init__(self, idMembre, idInscription):
        self.idMembre = idMembre
        self.idInscription = idInscription

class Evenement:
    def __init__(self, idEvenement):
        self.idEvenement = idEvenement

class Participer:
    def __init__(self, idMembre, idEvenement):
        self.idMembre = idMembre
        self.idEvenement = idEvenement

class Entrainement:
    def __init__(self,  idEntrainement, jourEN, lieuEN, dateEN, heureDebutEN, heureFinEN, typeArmeEN, niveauxEN):
        self.idEntrainement = idEntrainement
        self.jourEN = jourEN
        self.lieuEN = lieuEN
        self.dateEN = dateEN
        self.heureDebutEN = heureDebutEN
        self.heureFinEN = heureFinEN
        self.typeArmeEN = typeArmeEN
        self.niveauxEN = niveauxEN

class Reunion:
    def __init__(self, idReunionu, nomRE, lieuRE,  dateRE, heureDebutRE, nbParticipantRE, typeReunionRE, rapportRE, niveauxRE, idEvent):
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
    def __init__(self, idCompete, NomCO, villeCO, adresseCO, dateDebutCO, heureDebutCO, dateFinCO, heureFinCO, typeArmeCO, nbParticipantCO, sexeCO, typeCompete, DescriptionCO, niveauxCO, classementCO, idEvent):
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
    def __init__(self,  idEventClub, NomEV, villeEV, adresseEV, dateDebutEV, heureDebutEV, dateFinEV, nbParticipantEV, descriptionEV, niveauxEV, idEvent):
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
    def __init__(self, idResultat, resultat, dateRE, typeArmeRE, typeCompete, idEvent):
        self.idResultat = idResultat
        self.resultat = resultat
        self.dateRE = dateRE
        self.typeArmeRE = typeArmeRE
        self.typeCompete = typeCompete
        self.idEvent = idEvent

class Resulter:
    def __init__(self, idMembre, idResultat):
        self.idMembre = idMembre
        self.idResultat = idResultat

class Avoir:
    def __init__(self, idResultat, idMembre):
        self.idResultat = idResultat
        self.idMembre = idMembre

class Image:
    def __init__(self, idImage, url, privee, alt):
        self.idImage = idImage
        self.url = url
        self.privee = privee
        self.alt = alt

class ImageC:
    def __init__(self, idImage, idCompete):
        self.idImage = idImage
        self.idCompete = idCompete

class ImageE:
    def __init__(self, idImage, idEventClub):
        self.idImage = idImage
        self.idEventClub = idEventClub

class Actualite:
    def __init__(self, idActualité, dateAC, heureAC, nomAC, catégorieAC):
        self.idActualité = idActualité
        self.dateAC = dateAC
        self.heureAC = heureAC
        self.nomAC = nomAC
        self.catégorieAC = catégorieAC

class ImageA:
    def __init__(self, idImage, idActualité):
        self.idImage = idImage
        self.idActualité = idActualité

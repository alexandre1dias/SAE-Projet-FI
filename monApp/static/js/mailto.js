function gererEnvoi(estActif, lien) {
    if (estActif) {
        window.location.href = lien;
        var confirmation = confirm("Votre logiciel de messagerie vient de s'ouvrir.\n\nAvez-vous bien envoyé le mail ?\n\n(Cliquez sur OK pour finaliser l'enregistrement sur le site, ou Annuler pour stopper l'opération)");
        return confirmation;
    }
    return true;
}

function MailtoInscription() {
    var nom = document.getElementById('inputNom').value;
    var prenom = document.getElementById('inputPrenom').value;
    var email = document.getElementById('inputEmail').value;
    var sexe = document.getElementById('inputSexe').value;
    var form = document.getElementById('formInscription');
    var actif = form.dataset.mailActif === 'true';
    var destinataire = "blois.escrime@wanadoo.fr";
    var sujetFinal = "[Demande Inscription] " + prenom + " " + nom;
    var corpsFinal = "Bonjour,\n\nJe souhaite m'inscrire au club.\n" +
                        "Voici mes informations :\n" +
                        "- Nom : " + nom + "\n" +
                        "- Prénom : " + prenom + "\n" +
                        "- Email : " + email + "\n" +
                        "- Sexe : " + sexe + "\n\n" +
                        "Cordialement.";
    var lien = "mailto:" + destinataire + 
               "?subject=" + encodeURIComponent(sujetFinal) + 
               "&body=" + encodeURIComponent(corpsFinal);
    return gererEnvoi(actif, lien);
}

function MailtoModification() {
    var activeBtn = document.activeElement;
    var form = document.getElementById('formModification');
    var nom = document.getElementById('inputNom').value;
    var prenom = document.getElementById('inputPrenom').value;
    var motifElement = document.getElementById('inputJustification');
    var motif = motifElement ? motifElement.value : "";
    if (activeBtn && activeBtn.value === 'admin_save') {
        var actif = form.dataset.membreMailActif === 'true';
        var emailDest = form.dataset.membreEmail;
        var sujet = "[Profil] Mise à jour de vos informations";
        var corps = "Bonjour " + prenom + " " + nom + ",\n\n" +
                    "Un administrateur a modifié directement votre profil.\n";
        if (motif !== "") {
            corps += "Justification : " + motif + "\n";
        }
        corps += "\nCordialement.";
        var lien = "mailto:" + emailDest + 
                   "?subject=" + encodeURIComponent(sujet) + 
                   "&body=" + encodeURIComponent(corps);
        return gererEnvoi(actif, lien);
    }
    var actifAdmin = form.dataset.mailActif === 'true';
    var destinataireAdmin = "blois.escrime@wanadoo.fr";
    var sujetFinal = "[Modification Profil] " + prenom + " " + nom;
    var corpsFinal = "Bonjour,\nJe souhaite modifier mon profil.\nJustification : " + motif;
    var lienAdmin = "mailto:" + destinataireAdmin + 
               "?subject=" + encodeURIComponent(sujetFinal) + 
               "&body=" + encodeURIComponent(corpsFinal);
    return gererEnvoi(actifAdmin, lienAdmin);
}

function MailtoContact() {
    var typeForm = document.querySelector('input[name="type_form"]:checked');
    var typeTexte = typeForm ? typeForm.value : "Contact";
    var sujetInput = document.getElementById('inputSujet').value;
    var emailInput = document.getElementById('inputEmail').value;
    var descInput = document.getElementById('inputDescription').value;
    var form = document.getElementById('formContact');
    var configMail = {
        'Question': form.dataset.mailQuestion === 'true',
        'Demande': form.dataset.mailDemande === 'true',
        'Signalement': form.dataset.mailSignalement === 'true'
    };
    var actif = configMail[typeTexte];
    var destinataire = "blois.escrime@wanadoo.fr";
    var sujetFinal = "[" + typeTexte + "] " + sujetInput;
    var corpsFinal = "Envoyé par : " + emailInput + "\n\n" + descInput;
    var lien = "mailto:" + destinataire + 
               "?subject=" + encodeURIComponent(sujetFinal) + 
               "&body=" + encodeURIComponent(corpsFinal);
    return gererEnvoi(actif, lien);
}

function MailtoDesinscription(idM, email, prenom, nom) {
    var justificationElement = document.getElementById('justification-' + idM);
    var justification = justificationElement ? justificationElement.value : "Non spécifiée";
    var actif = true; 
    var sujetFinal = "[Désinscription] Information concernant votre compte - Cercle d'escrime";
    var corpsFinal = "Bonjour " + prenom + " " + nom + ",\n\n" +
                        "Votre compte a été désactivé pour la raison suivante :\n" +
                        justification + "\n\n" +
                        "Cordialement.";
    var lien = "mailto:" + email + 
               "?subject=" + encodeURIComponent(sujetFinal) + 
               "&body=" + encodeURIComponent(corpsFinal);
    return gererEnvoi(actif, lien);
}

function MailtoAccepterInscription(idI, email, prenom, nom) {
    var sujet = "[Inscription] Bienvenue au Cercle d'escrime !";
    var corps = "Bonjour " + prenom + " " + nom + ",\n\n" +
                "Nous avons le plaisir de vous informer que votre inscription a été validée.\n" +
                "Vous pouvez dès à présent vous connecter à votre espace membre.";
    var lien = "mailto:" + email + "?subject=" + encodeURIComponent(sujet) + "&body=" + encodeURIComponent(corps);
    return gererEnvoi(true, lien);
}

function MailtoAccepterModification(idModif, email, prenom, nom, doitEnvoyer) {
    var actif = (doitEnvoyer === 'true');
    var sujet = "[Profil] Vos modifications ont été validées";
    var corps = "Bonjour " + prenom + " " + nom + ",\n\n" +
                "Les modifications demandées pour votre profil ont été acceptées et appliquées.";
    var lien = "mailto:" + email + "?subject=" + encodeURIComponent(sujet) + "&body=" + encodeURIComponent(corps);
    return gererEnvoi(actif, lien);
}

function MailtoRefuser(type, id, email, prenom, nom, doitEnvoyer) {
    var actif = (doitEnvoyer === undefined) ? true : (doitEnvoyer === 'true');
    var modalSelector = '#refusModal-' + type + '-' + id;
    var justificationElement = document.querySelector(modalSelector + ' textarea[name="justification"]');
    var justification = justificationElement ? justificationElement.value : "";
    var sujet = (type === 'inscription') ? 
        "[Inscription] Information concernant votre demande d'adhésion" : 
        "[Profil] Information concernant votre demande de modification";
    var corpsIntro = (type === 'inscription') ? 
        "Votre demande d'inscription n'a pas pu être acceptée" : 
        "Votre demande de modification de profil a été refusée";
    var corpsFinal = "Bonjour " + prenom + " " + nom + ",\n\n" +
                     corpsIntro + " pour la raison suivante :\n" +
                     justification;
    var lien = "mailto:" + email + "?subject=" + encodeURIComponent(sujet) + "&body=" + encodeURIComponent(corpsFinal);
    return gererEnvoi(actif, lien);
}
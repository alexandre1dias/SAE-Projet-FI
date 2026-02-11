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
    if (activeBtn && activeBtn.value === 'admin_save') return true;
    var nom = document.getElementById('inputNom').value;
    var prenom = document.getElementById('inputPrenom').value;
    var motifElement = document.getElementById('inputJustification');
    var motif = motifElement ? motifElement.value : "";
    var form = document.getElementById('formModification');
    var actif = form.dataset.mailActif === 'true';
    var destinataire = "blois.escrime@wanadoo.fr";
    var sujetFinal = "[Modification Profil] " + prenom + " " + nom;
    var corpsFinal = "Bonjour,\nJe souhaite modifier mon profil.\nJustification : " + motif;
    var lien = "mailto:" + destinataire + 
               "?subject=" + encodeURIComponent(sujetFinal) + 
               "&body=" + encodeURIComponent(corpsFinal);
    return gererEnvoi(actif, lien);
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
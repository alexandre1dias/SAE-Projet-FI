function ouvrirClientMail(estActif, destinataire, sujet, corps) {
    if (estActif) {
        var lien = "mailto:" + destinataire + 
                   "?subject=" + encodeURIComponent(sujet) + 
                   "&body=" + encodeURIComponent(corps);
        window.location.href = lien;
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
                        
    return ouvrirClientMail(actif, destinataire, sujetFinal, corpsFinal);
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
    return ouvrirClientMail(actif, destinataire, sujetFinal, corpsFinal);
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
    return ouvrirClientMail(actif, destinataire, sujetFinal, corpsFinal);
}

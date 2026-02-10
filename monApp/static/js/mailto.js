function ouvrirClientMail(estActif, destinataire, sujet, corps) {
    if (estActif) {
        var lien = "mailto:" + destinataire + 
                   "?subject=" + encodeURIComponent(sujet) + 
                   "&body=" + encodeURIComponent(corps);
        window.location.href = lien;
    }
    return true;
}
(function() {
    // Vérification de la préférence stockée
    // Assurez-vous que 'modeSombre' et 'actif' correspondent à ce que vous utilisez dans votre bouton switch
    var isDarkMode = localStorage.getItem('modeSombre') === 'actif'; 

    if (isDarkMode) {
        // On ajoute la classe. 
        // Note: Comme ce script sera lancé au début du body, document.body est disponible.
        document.body.classList.add('dark-mode');
    }
    console.log("ok")
})();
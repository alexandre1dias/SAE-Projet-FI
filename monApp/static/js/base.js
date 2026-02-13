document.addEventListener('DOMContentLoaded', function() {
    // --- Gestion du Dark Mode ---
    const savedMode = localStorage.getItem('darkMode');
    
    // Appliquer le mode sombre si sauvegardé (sur toutes les pages)
    if (savedMode === 'enabled') {
        document.body.classList.add('dark-mode');
    }

    // Gestion du bouton toggle (uniquement s'il existe sur la page)
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        if (savedMode === 'enabled') {
            darkModeToggle.checked = true;
        }

        darkModeToggle.addEventListener('change', function() {
            if (this.checked) {
                document.body.classList.add('dark-mode');
                localStorage.setItem('darkMode', 'enabled');
            } else {
                document.body.classList.remove('dark-mode');
                localStorage.setItem('darkMode', 'disabled');
            }
        });
    }

    // --- Gestion de la modale de réponse (Notifications) ---
    const hash = window.location.hash;
    if (hash && hash.startsWith('#view_response_')) {
        const formId = hash.split('_')[2];
        
        if (formId) {
            ouvrirModalReponse(formId);
            history.replaceState(null, null, ' '); 
        }
    }
    function ouvrirModalReponse(id) {
        fetch(`/api/get_reponse/${id}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert("Impossible de charger la réponse.");
                    return;
                }
                document.getElementById('modalSujet').textContent = data.sujet;
                document.getElementById('modalReponse').textContent = data.reponse;
                document.getElementById('modalDate').textContent = "Le " + data.date;
                var myModal = new bootstrap.Modal(document.getElementById('reponseModal'));
                myModal.show();
            })
            .catch(error => console.error('Erreur:', error));
    }
});
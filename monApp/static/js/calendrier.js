//Affichage du calendrier
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    if (calendarEl) {

    // Initialisation de la modale Bootstrap
    var eventModal = new bootstrap.Modal(document.getElementById('eventModal'));

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'fr',
        firstDay: 1,
        height: 'auto', 
        fixedWeekCount: false, 
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
        },
        buttonText: {
            today: "Aujourd'hui",
            month: 'Mois',
            week: 'Semaine',
            day: 'Jour',
            list: 'Liste'
        },
        
        events: function(info, successCallback, failureCallback) {
            const urlParams = new URLSearchParams(window.location.search);
            // Récupération de l'URL depuis l'attribut data-api-url
            let baseUrl = calendarEl.dataset.apiUrl;
            let apiUrl = baseUrl + "?" + urlParams.toString();
            
            fetch(apiUrl)
                .then(response => response.json())
                .then(data => {
                    successCallback(data);
                })
                .catch(error => {
                    console.error("Erreur lors de la récupération des événements:", error);
                    failureCallback(error);
                });
        },
        eventClick: function(info) {
            // Si l'événement a une URL (Compétition, Réunion...), on redirige
            if (info.event.extendedProps.url) {
                window.location.href = info.event.extendedProps.url;
            }

            // Sinon (Entraînement), on ouvre la modale
            else {
                let event = info.event;
                let props = event.extendedProps;
                
                document.getElementById('eventModalLabel').innerText = props.type || 'Détails';
                document.getElementById('modalTitle').innerText = event.title;
                document.getElementById('modalType').innerText = props.type || 'Non spécifié';
                document.getElementById('modalVille').innerText = props.ville || 'Non spécifié';
                document.getElementById('modalAdresse').innerText = props.adresse || 'Non spécifié';
                document.getElementById('modalDescription').innerText = props.description || 'Aucune description';
                
                let options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
                document.getElementById('modalStart').innerText = event.start ? event.start.toLocaleDateString('fr-FR', options) : '';
                document.getElementById('modalEnd').innerText = event.end ? event.end.toLocaleTimeString('fr-FR', {hour: '2-digit', minute:'2-digit'}) : '';
                
                // Niveaux
                let elemNiveau = document.getElementById('lineNiveau');
                let spanNiveau = document.getElementById('modalNiveaux');
                if (props.niveaux) {
                    spanNiveau.innerText = props.niveaux;
                    elemNiveau.style.display = 'block';
                } else {
                    elemNiveau.style.display = 'none';
                }
                
                // Armes
                let elemArme = document.getElementById('lineArme');
                let spanArme = document.getElementById('modalArme');
                if (props.arme) {
                    spanArme.innerText = props.arme;
                    elemArme.style.display = 'block';
                } else {
                    elemArme.style.display = 'none';
                }

                eventModal.show();
            }
        }
    });
    calendar.render();
    }
});


document.addEventListener('DOMContentLoaded', function() {
    // On récupère tous les éléments
    const categorySelect = document.getElementById('category_select');
    const levelContainer = document.getElementById('level-field-container');
    const armeContainer = document.getElementById('arme-field-container');
    const sexeContainer = document.getElementById('sexe-field-container');
    const typeContainer = document.getElementById('type-field-container');
    const villeContainer = document.getElementById('ville-field-container');
    const adresseContainer = document.getElementById('adresse-field-container');
    const reunionTypeContainer = document.getElementById('reunion-type-field'); 
    
    function updateFormFields() {
        const selectedCategory = categorySelect.value;
        // On cache TOUT par défaut pour repartir de zéro
        levelContainer.style.display = 'none';
        armeContainer.style.display = 'none';
        sexeContainer.style.display = 'none';
        typeContainer.style.display = 'none';
        villeContainer.style.display = 'none';
        adresseContainer.style.display = 'none';
        reunionTypeContainer.style.display = 'none';
        
        // On affiche seulement ce qui est nécessaire selon la catégorie
        switch (selectedCategory) {
            case 'Compétition':
                levelContainer.style.display = 'block';
                armeContainer.style.display = 'block';
                sexeContainer.style.display = 'block';
                typeContainer.style.display = 'block';
                villeContainer.style.display = 'block';
                adresseContainer.style.display = 'block';
                break;

            case 'Entraînement':
                levelContainer.style.display = 'block';
                armeContainer.style.display = 'block';
                villeContainer.style.display = 'block';
                adresseContainer.style.display = 'block';
                break;

            case 'Evenement du club':
                levelContainer.style.display = 'block';
                villeContainer.style.display = 'block';
                adresseContainer.style.display = 'block';
                break;

            case 'Réunion':
                villeContainer.style.display = 'block';
                adresseContainer.style.display = 'block';
                reunionTypeContainer.style.display = 'block';
                break;
        }
    }
    
    if (categorySelect) {
        categorySelect.addEventListener('change', updateFormFields);
        // On lance la fonction au chargement de la page
        updateFormFields();
    }
});
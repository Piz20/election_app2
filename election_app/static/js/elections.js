// Récupère l'heure actuelle fournie par le contexte Django
const currentTime = new Date(window.currentTime);

// Ouvrir la modale
function openModalElection() {
    const modal = document.getElementById("electionModal");
    modal.style.display = "block";
}

// Fermer la modale
function closeModalElection() {
    const modal = document.getElementById("electionModal");
    modal.style.display = "none";
}

// Gestion de la soumission du formulaire
document.getElementById("createElectionForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Empêche l'envoi classique du formulaire

    const formData = new FormData(this);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(window.createElectionUrl, {
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrfToken,
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Affiche un message de succès
                Swal.fire({
                    title: 'Success!',
                    text: data.message,
                    icon: 'success',
                    confirmButtonText: 'OK',
                }).then(() => {
                    closeModalElection();
                    location.reload(); // Recharge la page
                });
            } else {
                // Gère les erreurs retournées par le serveur
                const form = document.getElementById("createElectionForm");
                const errorMessages = data.errors;

                // Réinitialise les erreurs précédentes
                form.querySelectorAll(".error-message").forEach(errorEl => errorEl.remove());

                // Ajoute de nouvelles erreurs
                for (const [field, errors] of Object.entries(errorMessages)) {
                    const inputElement = form.querySelector(`[name="${field}"]`);
                    if (inputElement) {
                        errors.forEach(error => {
                            const errorEl = document.createElement("div");
                            errorEl.className = "error-message";
                            errorEl.textContent = error;
                            inputElement.parentNode.appendChild(errorEl); // Ajoute après le champ concerné
                        });
                    }
                }

                // Affiche une alerte générique
                Swal.fire({
                    title: 'Error',
                    text: data.message,
                    icon: 'error',
                    confirmButtonText: 'OK',
                });
            }
        })
        .catch(error => {
            console.error("Error submitting form:", error);
            Swal.fire({
                title: 'Error',
                text: 'Something went wrong. Please try again later.',
                icon: 'error',
                confirmButtonText: 'OK',
            });
        });
});

// Mise à jour des statuts des cartes
document.addEventListener("DOMContentLoaded", function () {
    let currentTime = new Date(window.currentTime);

    // Fonction pour mettre à jour les statuts
    function updateStatuses() {
        currentTime = new Date(); // Récupère l'heure actuelle
        document.querySelectorAll(".card").forEach(card => {
            const startDate = new Date(card.getAttribute("data-start-date"));
            const endDate = new Date(card.getAttribute("data-end-date"));

            let status;
            let color;

            // Détermine le statut et le style associé
            if (currentTime < startDate) {
                status = "Not Began";
                color = "green";
            } else if (currentTime >= startDate && currentTime <= endDate) {
                status = "Started";
                color = "red";
            } else {
                status = "Finished";
                color = "black";
            }

            // Met à jour l'élément de statut
            const statusElement = card.querySelector(".card-status");
            if (statusElement) {
                statusElement.textContent = status;
                statusElement.style.color = color;
                statusElement.style.fontWeight = "bold";
            }
        });
    }

    // Met à jour les statuts au chargement
    updateStatuses();

    // Met à jour les statuts toutes les secondes
    setInterval(updateStatuses, 1000);
});
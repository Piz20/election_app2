// election_details.js


const countdownTitle = document.getElementById('countdown-title');
const countdownTimer = document.getElementById('countdown-timer');

// Fonction pour formater le temps (jours, heures, minutes, secondes) - pas de décimales pour les secondes
function formatTime(timeInSeconds) {
    const days = Math.floor(timeInSeconds / (3600 * 24));
    timeInSeconds -= days * 3600 * 24;
    const hours = Math.floor(timeInSeconds / 3600);
    timeInSeconds -= hours * 3600;
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = Math.floor(timeInSeconds % 60); // Utilisez Math.floor pour éliminer les décimales

    return {
        days: days,
        hours: hours,
        minutes: minutes,
        seconds: seconds
    };
}

// Fonction pour mettre à jour le compte à rebours
function updateCountdown() {
    const now = new Date();
    let timeRemaining;

    if (now < electionStartDate) {
        // L'élection n'a pas encore commencé
        timeRemaining = (electionStartDate - now) / 1000; // en secondes
        countdownTitle.innerText = "Time before election begins";
        countdownTimer.style.color = "green"; // Définir la couleur du compte à rebours sur vert
    } else if (now < electionEndDate) {
        // L'élection est en cours
        timeRemaining = (electionEndDate - now) / 1000; // en secondes
        countdownTitle.innerText = "Time before election ends";
        countdownTimer.style.color = "red"; // Définir la couleur du compte à rebours sur rouge
    } else {
        // L'élection est terminée
        countdownTitle.innerText = "Election has ended";
        countdownTimer.innerText = "";
        return;
    }

    const time = formatTime(timeRemaining);

    // Afficher le compte à rebours sans décimales pour les secondes
    countdownTimer.innerText = `${time.days}d ${time.hours}h ${time.minutes}m ${time.seconds}s`;
}

// Mettre à jour le compte à rebours toutes les secondes
setInterval(updateCountdown, 1000);
updateCountdown(); // Initialiser immédiatement le compte à rebours

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('createCandidateForm');

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Empêcher la soumission traditionnelle du formulaire

        const formData = new FormData(form);

        // Envoi du formulaire avec AJAX
        fetch(formActionUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value, // Ajout du token CSRF
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Affiche un message de succès si la soumission est réussie
                    Swal.fire({
                        title: 'Success!',
                        text: 'Candidate added successfully!',
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then(() => {
                        // Rafraîchissez la page ou la section des candidats
                        location.reload(); // Cela recharge la page complète
                    });
                } else {
                    // Si la soumission échoue, affiche un message d'erreur
                    if (data.errors) {
                        // Loop through the form errors and display them
                        Object.keys(data.errors).forEach(field => {
                            const errorContainer = document.getElementById(`error-${field}`);
                            if (errorContainer) {
                                // Display the error message in the corresponding field
                                errorContainer.textContent = data.errors[field].join(", ");
                            }
                        });

                        // General error message (if any)
                        Swal.fire({
                            title: 'Error!',
                            text: data.message || 'There was an issue adding the candidate.',
                            icon: 'error',
                            confirmButtonText: 'OK'
                        });
                    } else {
                        Swal.fire({
                            title: 'Error!',
                            text: 'An unexpected error occurred.',
                            icon: 'error',
                            confirmButtonText: 'OK'
                        });
                    }
                }
            })
            .catch(error => {
                // En cas d'erreur de réseau ou d'autre problème
                Swal.fire({
                    title: 'Error!',
                    text: 'An unexpected error occurred.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            });
    });
});


// Include this function at the top or bottom of your script
function previewPhoto(event) {
    const photoPreviewImage = document.getElementById('photoPreviewImage');
    const photoPreview = document.getElementById('photoPreview');
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            photoPreviewImage.src = e.target.result;
            photoPreviewImage.style.display = 'block'; // Show the preview
        }

        reader.readAsDataURL(file);
    } else {
        // Reset to default image if no file selected
        photoPreviewImage.src = "{% static 'images/default_profile_pic.png' %}";
        photoPreviewImage.style.display = 'none'; // Hide the preview
    }
}


// Function to open the modal for candidate creation
function openModalCandidate() {
    // Get the modal element
    const modal = document.getElementById('candidateModal');
    // Show the modal by changing its display style to 'block'
    modal.style.display = 'block';
}

// Function to close the modal for candidate creation
function closeModalCandidate() {
    // Get the modal element
    const modal = document.getElementById('candidateModal');
    // Close the modal by changing its display style to 'none'
    modal.style.display = 'none';
}

// Close modal when clicking outside the modal content
window.onclick = function (event) {
    const modal = document.getElementById('candidateModal');
    // Check if the click is outside the modal content
    if (event.target === modal) {
        closeModalCandidate();
    }
}

// Function to show confirmation dialog
function confirmVote(button) {
    const candidateId = button.getAttribute('data-candidate-id'); // Récupère l'ID du candidat cliqué
    const candidateName = button.getAttribute('data-candidate-name'); // Récupère le nom du candidat cliqué

    // Base confirmation text
    let confirmationText = `You are about to vote for ${candidateName}. You can modify your choice until the end of the election.`;



    // Show SweetAlert2 confirmation dialog
    Swal.fire({
        title: 'Are you sure?',
        text: confirmationText,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, vote for this candidate!',
        cancelButtonText: 'No, cancel',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            // On confirmation, submit the vote
            voteForCandidate(candidateId);
        }
    });
}


function voteForCandidate(candidateId) {
    // Use the election ID passed from Django
    const electionId = window.electionId; // Ensure this variable is defined in the Django template

    // Retrieve the CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Perform the AJAX request with the dynamic election ID
    fetch(`/election/${electionId}/vote/${candidateId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({candidate_id: candidateId})
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // If the vote is successfully recorded
                Swal.fire(
                    'Success!',
                    data.message || 'Your vote has been successfully recorded.',
                    'success'
                ).then((result) => {
                    if (result.isConfirmed) {
                        // Reload the page after clicking "OK"
                        location.reload();
                    }
                });
            } else if (data.error) {
                // If a specific error is returned from the backend
                Swal.fire(
                    'Error!',
                    data.error, // Display the error message returned by the backend
                    'error'
                );
            } else {
                // If a general error occurs
                Swal.fire(
                    'Error!',
                    'There was an error submitting your vote. Please try again later.',
                    'error'
                );
            }
        })
        .catch(error => {
            // Handle unexpected errors
            Swal.fire(
                'Error!',
                'An unexpected error occurred. Please try again.',
                'error'
            );
            console.error('Unexpected error:', error);
        });
}

// Fonction pour récupérer le token CSRF depuis les cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to handle vote removal
function removeVote(button) {
    var candidateId = button.getAttribute('data-candidate-id');
    var csrfToken = getCookie('csrftoken');  // Get the CSRF token from the cookies

    // Check if the CSRF token is defined
    if (!csrfToken) {
        Swal.fire('Error', 'CSRF token is missing', 'error');
        return;
    }

    fetch('/remove_vote/' + candidateId + '/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  // Include the CSRF token in the headers
        },
        body: JSON.stringify({ 'candidate_id': candidateId })  // Send the candidate ID in the request body
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Display a success message with SweetAlert if the operation is successful
            Swal.fire('Success', data.message, 'success')
                .then(() => {
                    location.reload();  // Reload the page to reflect the updated vote count
                });
        } else {
            // Display an error message with SweetAlert if the operation fails
            Swal.fire('Error', data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire('Error', 'An error occurred while removing the vote', 'error');
    });
}

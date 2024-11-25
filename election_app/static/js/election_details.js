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
window.onclick = function(event) {
    const modal = document.getElementById('candidateModal');
    // Check if the click is outside the modal content
    if (event.target === modal) {
        closeModalCandidate();
    }
}



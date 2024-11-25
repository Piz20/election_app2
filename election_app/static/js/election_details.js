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



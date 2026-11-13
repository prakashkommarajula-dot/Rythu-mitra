/**
 * Main application JavaScript for Rythu Mithra
 */

document.addEventListener('DOMContentLoaded', function () {
    // Enable Bootstrap tooltips if any exist
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    console.log("Rythu Mithra (రైతు మిత్ర) UI Initialized.");
});

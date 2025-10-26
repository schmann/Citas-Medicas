// Main JavaScript file for the application

// Initialize tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Initialize popovers
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
});

// Handle form submissions with CSRF token
$(document).ready(function() {
    // Add CSRF token to all AJAX requests
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        }
    });

    // Initialize Select2 for dropdowns
    if ($.fn.select2) {
        $('.select2').select2({
            theme: 'bootstrap4',
            width: '100%'
        });
    }

    // Initialize datepickers
    if ($.fn.datepicker) {
        $('.datepicker').datepicker({
            format: 'dd/mm/yyyy',
            autoclose: true,
            todayHighlight: true,
            language: 'es'
        });
    }

    // Initialize timepickers
    if ($.fn.timepicker) {
        $('.timepicker').timepicker({
            showMeridian: false,
            minuteStep: 15,
            showInputs: false,
            disableFocus: true
        });
    }
});

// Global error handler for AJAX requests
$(document).ajaxError(function(event, jqXHR, ajaxSettings, thrownError) {
    console.error('AJAX Error:', {
        status: jqXHR.status,
        statusText: jqXHR.statusText,
        responseText: jqXHR.responseText,
        thrownError: thrownError
    });
    
    // Show error message to user
    let errorMessage = 'Ocurrió un error al procesar la solicitud.';
    
    if (jqXHR.status === 0) {
        errorMessage = 'No se pudo conectar con el servidor. Verifique su conexión a internet.';
    } else if (jqXHR.status === 403) {
        errorMessage = 'No tiene permisos para realizar esta acción.';
    } else if (jqXHR.status === 404) {
        errorMessage = 'El recurso solicitado no fue encontrado.';
    } else if (jqXHR.status === 500) {
        errorMessage = 'Error interno del servidor. Por favor, intente nuevamente más tarde.';
    }
    
    // Show error message using Bootstrap toast or alert
    showAlert(errorMessage, 'danger');
});

// Show alert message
function showAlert(message, type = 'info') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    // Add alert to the alerts container or create one if it doesn't exist
    let $alertsContainer = $('#alerts-container');
    if ($alertsContainer.length === 0) {
        $('body').prepend('<div id="alerts-container" class="container mt-3"></div>');
        $alertsContainer = $('#alerts-container');
    }
    
    $alertsContainer.append(alertHtml);
    
    // Auto-remove alert after 5 seconds
    setTimeout(() => {
        $('.alert').alert('close');
    }, 5000);
}

// Format date to YYYY-MM-DD
function formatDate(date) {
    const d = new Date(date);
    let month = '' + (d.getMonth() + 1);
    let day = '' + d.getDate();
    const year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('-');
}

// Format time to HH:MM
function formatTime(date) {
    const d = new Date(date);
    let hours = '' + d.getHours();
    let minutes = '' + d.getMinutes();

    if (hours.length < 2) hours = '0' + hours;
    if (minutes.length < 2) minutes = '0' + minutes;

    return [hours, minutes].join(':');
}

// Export functions for use in other modules
window.App = window.App || {};
window.App.Utils = {
    showAlert: showAlert,
    formatDate: formatDate,
    formatTime: formatTime
};

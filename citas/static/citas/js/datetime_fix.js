// Asegurar que los campos de fecha/hora tengan el formato correcto
// antes de enviar el formulario
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('horariocita_form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            // Obtener los campos de fecha/hora
            const startDatetime = document.getElementById('id_start_datetime');
            const endDatetime = document.getElementById('id_end_datetime');
            
            // Función para formatear la fecha al formato YYYY-MM-DDTHH:MM
            function formatDateTime(datetimeStr) {
                if (!datetimeStr) return '';
                
                // Intentar parsear la fecha en diferentes formatos
                let date = null;
                
                // Formato DD/MM/YYYY HH:MM AM/PM
                const match1 = datetimeStr.match(/^(\d{2})\/(\d{2})\/(\d{4}) (\d{1,2}):(\d{2}) (AM|PM)$/i);
                if (match1) {
                    let [_, day, month, year, hours, minutes, period] = match1;
                    hours = parseInt(hours, 10);
                    if (period.toUpperCase() === 'PM' && hours < 12) hours += 12;
                    if (period.toUpperCase() === 'AM' && hours === 12) hours = 0;
                    
                    date = new Date(year, month - 1, day, hours, minutes);
                } 
                // Formato YYYY-MM-DD HH:MM
                else if (datetimeStr.match(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/)) {
                    date = new Date(datetimeStr.replace(' ', 'T'));
                }
                
                // Formatear a YYYY-MM-DDTHH:MM
                if (date && !isNaN(date.getTime())) {
                    const pad = num => num.toString().padStart(2, '0');
                    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
                }
                
                return datetimeStr;
            }
            
            // Aplicar el formato a los campos de fecha/hora
            if (startDatetime) {
                startDatetime.value = formatDateTime(startDatetime.value);
            }
            
            if (endDatetime) {
                endDatetime.value = formatDateTime(endDatetime.value);
            }
        });
    }
});

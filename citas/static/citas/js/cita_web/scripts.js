/**
 * ===============================================
 * CONFIGURACIÓN GLOBAL Y VARIABLES
 * ===============================================
 */

// Variables globales
const apiUrl = '/citas/';
window.calendar = null;
window.citaSeleccionada = null;
window.medicoSeleccionado = null;
window.especialidadSeleccionada = null;

// Configuración global del calendario
const calendarConfig = {
    // Configuración básica
    initialView: 'timeGridWeek',
    locale: 'es',
    timeZone: 'America/Caracas',
    firstDay: 1, // Lunes como primer día de la semana
    height: 'auto',
    contentHeight: 'auto',
    expandRows: true,
    nowIndicator: true,
    
    // Configuración de la vista de tiempo
    allDaySlot: false,
    slotMinTime: '06:00:00',
    slotMaxTime: '20:00:00',
    slotDuration: '00:30:00',
    slotLabelInterval: '01:00',
    slotLabelFormat: {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true,
        meridiem: 'short',
        timeZoneName: 'short',
        omitCommas: true
    },
    
    // Configuración de eventos
    eventTimeFormat: {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true,
        meridiem: 'short',
        timeZoneName: 'short'
    },
    
    // Barra de herramientas del encabezado
    headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    
    // Textos de los botones
    buttonText: {
        today: 'Hoy',
        month: 'Mes',
        week: 'Semana',
        day: 'Día',
        list: 'Lista'
    },
    
    // Configuración de eventos
    eventTimeFormat: {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true,
        meridiem: 'short',
        timeZoneName: 'short',
        omitCommas: true
    },
    
    // Otras configuraciones
    allDaySlot: false,
    nowIndicator: true,
    navLinks: true,
    selectable: true,
    selectMirror: true,
    selectOverlap: false,
    initialDate: new Date(),
    
    // Formato de hora de los eventos
    eventTimeFormat: {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true,
        meridiem: 'short',
        timeZoneName: 'short',
        omitCommas: true
    },
    
    // Dimensiones
    height: 'auto',
    contentHeight: 'auto',
    expandRows: true
};

/**
 * ===============================================
 * INICIALIZACIÓN DE LA APLICACIÓN
 * ===============================================
 */

$(document).ready(function() {
    console.log('✅ Inicializando la aplicación...');
    
    // Inicializar tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
    
    // Inicializar selects con Select2
    $('.select2').select2({
        theme: 'bootstrap4',
        width: '100%',
        placeholder: 'Seleccione una opción',
    });
    
    // Inicializar el select de médico como deshabilitado hasta que se seleccione especialidad
    $('#medico_id').prop('disabled', true);
    
    // Inicializar el calendario
    inicializarCalendario();
    
    // Manejar cambio de especialidad
    $('#especialidad_id').on('change', function() {
        const especialidadId = $(this).val();
        window.especialidadSeleccionada = especialidadId;
        
        // Limpiar la selección de médico
        $('#medico_id').val('').trigger('change');
        
        // Cargar médicos para la especialidad seleccionada
        if (especialidadId) {
            cargarMedicos(especialidadId);
        } else {
            $('#medico_id').empty().append('<option value="">Seleccione una especialidad primero</option>').prop('disabled', true);
        }
        
        // Limpiar el calendario
        if (window.calendar) {
            window.calendar.removeAllEvents();
        }
    });
    
    // Manejar cambio de médico
    $('#medico_id').on('change', function() {
        const medicoId = $(this).val();
        window.medicoSeleccionado = medicoId;
        
        // Actualizar el calendario si hay un médico seleccionado
        if (window.calendar) {
            if (medicoId) {
                console.log('Cambiando a médico ID:', medicoId);
                // Forzar recarga de eventos y cambiar a vista semanal
                window.calendar.refetchEvents();
                window.calendar.changeView('timeGridWeek');
                // Forzar actualización del calendario
                setTimeout(() => {
                    window.calendar.updateSize();
                }, 100);
            } else {
                // Limpiar el calendario si no hay médico seleccionado
                window.calendar.removeAllEvents();
            }
        }
    });
    
    console.log('✅ Aplicación inicializada correctamente');
});

/**
 * ===============================================
 * FUNCIONES PRINCIPALES
 * ===============================================
 */

/**
 * Inicializa el calendario de FullCalendar
 */
function inicializarCalendario() {
    try {
        console.log('Inicializando calendario...');
        
        // Obtener el elemento del calendario
        const calendarEl = document.getElementById('calendario');
        if (!calendarEl) {
            console.error('No se encontró el elemento con ID "calendario"');
            return;
        }
        
        // Configuración del calendario
        const config = {
            ...calendarConfig,
            events: function(fetchInfo, successCallback, failureCallback) {
                console.log('Solicitando eventos para el rango:', fetchInfo.startStr, 'a', fetchInfo.endStr);
                cargarEventosCalendario(fetchInfo, successCallback, failureCallback);
            },
            eventClick: function(info) {
                console.log('Evento clickeado:', info.event);
                manejarClickEvento(info);
            },
            select: function(selectionInfo) {
                console.log('Rango seleccionado:', selectionInfo.start, 'a', selectionInfo.end);
                manejarSeleccionCalendario(selectionInfo);
            },
            datesSet: function(dateInfo) {
                console.log('Vista cambiada:', dateInfo.view.type, dateInfo.view.title);
            },
            eventDidMount: function(info) {
                console.log('Evento montado:', info.event);
            },
            loading: function(isLoading) {
                console.log('Cargando:', isLoading);
                if (isLoading) {
                    $('.loading-overlay').fadeIn(200);
                } else {
                    $('.loading-overlay').fadeOut(200);
                }
            },
            eventContent: function(arg) {
                const timeText = arg.timeText;
                const title = arg.event.title;
                const eventType = arg.event.extendedProps.tipo;
                const start = arg.event.start;
                const end = arg.event.end;
                
                console.log('🔵 Renderizando evento:', {
                    id: arg.event.id,
                    title,
                    type: eventType,
                    start: start ? start.toISOString() : null,
                    end: end ? end.toISOString() : null,
                    timeText,
                    extendedProps: arg.event.extendedProps
                });
                
                const eventEl = document.createElement('div');
                eventEl.className = `fc-event fc-event-${eventType}`;
                
                // Estilos personalizados para el evento
                eventEl.style.cssText = `
                    padding: 4px 6px;
                    border-radius: 4px;
                    font-size: 0.85em;
                    cursor: pointer;
                    margin: 1px 2px;
                    border-left: 3px solid ${eventType === 'disponibilidad' ? '#28a745' : '#dc3545'};
                    background-color: ${eventType === 'disponibilidad' ? 'rgba(40, 167, 69, 0.1)' : 'rgba(220, 53, 69, 0.1)'};
                `;
                
                eventEl.innerHTML = `
                    <div class="fc-event-time" style="font-weight: bold;">${timeText}</div>
                    <div class="fc-event-title" style="white-space: normal; line-height: 1.2;">${title}</div>
                `;
                
                // Agregar tooltip con más información
                if (arg.event.extendedProps.descripcion) {
                    eventEl.setAttribute('data-bs-toggle', 'tooltip');
                    eventEl.setAttribute('title', arg.event.extendedProps.descripcion);
                    eventEl.setAttribute('data-bs-placement', 'top');
                    eventEl.setAttribute('data-bs-html', 'true');
                }
                
                return { domNodes: [eventEl] };
            }
        };
        
        // Inicializar el calendario
        window.calendar = new FullCalendar.Calendar(calendarEl, config);
        window.calendar.render();
        
        console.log('✅ Calendario inicializado correctamente');
    } catch (error) {
        console.error('❌ Error al inicializar el calendario:', error);
        mostrarAlerta('Error al inicializar el calendario', 'error');
    }
}

/**
 * Carga los eventos del calendario para el médico seleccionado
 */
function cargarEventosCalendario(fetchInfo, successCallback, failureCallback) {
    console.log('🔍 Iniciando carga de eventos...');
    console.log('Médico seleccionado:', window.medicoSeleccionado);
    console.log('Especialidad seleccionada:', window.especialidadSeleccionada);
    
    // Solo cargar eventos si hay un médico seleccionado
    if (!window.medicoSeleccionado) {
        console.log('⚠️ No hay médico seleccionado');
        successCallback([]);
        return;
    }
    
    // Mostrar indicador de carga
    $('.loading-overlay').fadeIn(200);

    // Solo proceder si tenemos tanto el médico como la especialidad seleccionados
    if (!window.medicoSeleccionado || !window.especialidadSeleccionada) {
        console.log('⚠️ No se ha seleccionado médico o especialidad');
        successCallback([]);
        return;
    }
    
    console.log('📅 Rango de fechas solicitado:', {
        start: fetchInfo.startStr,
        end: fetchInfo.endStr
    });

    // Construir la URL con parámetros
    const params = new URLSearchParams();
    params.append('medico_id', window.medicoSeleccionado);
    params.append('especialidad_id', window.especialidadSeleccionada);
    params.append('start', fetchInfo.startStr);
    params.append('end', fetchInfo.endStr);
    
    const url = `${apiUrl}api/obtener-citas-y-disponibilidad/?${params.toString()}`;
    console.log('📡 URL de la solicitud:', url);
    
    // Usar fetch en lugar de $.ajax para mejor manejo de errores
    fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        cache: 'no-store'
    })
    .then(async response => {
        console.log('📥 Respuesta recibida. Estado:', response.status);
        const responseData = await response.text();
        
        try {
            const jsonData = JSON.parse(responseData);
            console.log('📊 Datos de la respuesta (parseados):', jsonData);
            return jsonData;
        } catch (e) {
            console.error('❌ Error al parsear la respuesta:', e);
            console.error('📄 Contenido de la respuesta:', responseData);
            throw new Error('La respuesta no es un JSON válido');
        }
    })
    .then(response => {
        console.log('✅ Datos recibidos de la API:', {
            citas: response.citas ? response.citas.length : 0,
            disponibilidad: response.disponibilidad ? response.disponibilidad.length : 0,
            success: response.success,
            error: response.error
        });
        
        if (!response.success) {
            throw new Error(response.error || 'Error desconocido al obtener los datos');
        }
        
        const events = [];
        
        // Procesar eventos de disponibilidad
        if (response.disponibilidad) {
            console.log('📅 Procesando disponibilidad:', response.disponibilidad);
            
            response.disponibilidad.forEach(disp => {
                try {
                    // Asegurarse de que las fechas estén en el formato correcto
                    let start = new Date(disp.fecha_hora_inicio);
                    let end = new Date(disp.fecha_hora_fin);
                    
                    // Verificar que las fechas sean válidas
                    if (isNaN(start.getTime()) || isNaN(end.getTime())) {
                        console.error('❌ Fecha inválida en disponibilidad:', disp);
                        return;
                    }
                    
                    // Ajustar a la zona horaria de Venezuela (UTC-4:30)
                    const startStr = start.toISOString();
                    const endStr = end.toISOString();
                    
                    console.log('➕ Añadiendo disponibilidad:', {
                        id: `disp-${disp.id}`,
                        start: startStr,
                        end: endStr,
                        original: disp
                    });
                    
                    events.push({
                        id: `disp-${disp.id}`,
                        title: 'Disponible',
                        start: startStr,
                        end: endStr,
                        allDay: false,
                        backgroundColor: '#28a745',
                        borderColor: '#218838',
                        extendedProps: {
                            tipo: 'disponibilidad',
                            descripcion: `Disponibilidad del Dr. ${disp.medico_nombre || 'Médico'}`,
                            rawData: disp
                        }
                    });
                } catch (error) {
                    console.error('❌ Error al procesar disponibilidad:', error, disp);
                }
            });
            
            console.log(`✅ ${response.disponibilidad.length} bloques de disponibilidad procesados`);
        }
        
        // Procesar citas existentes
        if (response.citas) {
            console.log('📅 Procesando citas:', response.citas);
            
            response.citas.forEach(cita => {
                try {
                    // Asegurarse de que las fechas estén en el formato correcto
                    const start = new Date(cita.fecha_hora_inicio);
                    const end = new Date(cita.fecha_hora_fin);
                    
                    // Verificar que las fechas sean válidas
                    if (isNaN(start.getTime()) || isNaN(end.getTime())) {
                        console.error('❌ Fecha inválida en cita:', cita);
                        return;
                    }
                    
                    const startStr = start.toISOString();
                    const endStr = end.toISOString();
                    
                    console.log('➕ Añadiendo cita:', {
                        id: `cita-${cita.id}`,
                        start: startStr,
                        end: endStr,
                        title: `Cita: ${cita.paciente_nombre || 'Paciente'}`
                    });
                    
                    events.push({
                        id: `cita-${cita.id}`,
                        title: `Cita: ${cita.paciente_nombre || 'Paciente'}`,
                        start: startStr,
                        end: endStr,
                        allDay: false,
                        backgroundColor: '#dc3545',
                        borderColor: '#c82333',
                        extendedProps: {
                            tipo: 'cita',
                            descripcion: `Cita con ${cita.paciente_nombre || 'paciente'}`,
                            citaId: cita.id,
                            rawData: cita
                        }
                    });
                } catch (error) {
                    console.error('❌ Error al procesar cita:', error, cita);
                }
            });
            
            console.log(`✅ ${response.citas.length} citas procesadas`);
        }
        
        console.log('📅 Total de eventos procesados:', events.length);
        if (events.length > 0) {
            console.log('📌 Ejemplo de evento:', {
                id: events[0].id,
                title: events[0].title,
                start: events[0].start,
                end: events[0].end
            });
        }
        successCallback(events);
    })
    .catch(error => {
        console.error('❌ Error al cargar la disponibilidad:', error);
        mostrarAlerta('Error al cargar la disponibilidad. Por favor, intente nuevamente.', 'error');
        failureCallback(error);
    })
    .finally(() => {
        $('.loading-overlay').fadeOut(200);
    });
    
    // Terminar la ejecución ya que usamos promesas
    return;
}

/**
 * Maneja el clic en un evento del calendario
 */
function manejarClickEvento(info) {
    const event = info.event;
    
    // Si es una cita, mostrar detalles
    if (event.extendedProps.tipo === 'cita') {
        window.citaSeleccionada = event.extendedProps.citaId;
        mostrarAlerta(`Cita seleccionada: ${event.title}`, 'info');
        // Aquí podrías mostrar un modal con más detalles de la cita
    }
    
    info.jsEvent.preventDefault();
}

/**
 * Maneja la selección de un rango de tiempo en el calendario
 */
function manejarSeleccionCalendario(info) {
    // Solo permitir selección si hay un médico seleccionado
    if (!window.medicoSeleccionado) {
        mostrarAlerta('Por favor seleccione un médico primero', 'warning');
        return;
    }
    
    // Aquí podrías abrir un formulario para agendar una nueva cita
    mostrarAlerta(`Nueva cita programada para: ${info.startStr}`, 'success');
    
    // Limpiar la selección
    window.calendar.unselect();
}

/**
 * ===============================================
 * FUNCIONES AUXILIARES
 * ===============================================
 */

/**
 * Carga los médicos para la especialidad seleccionada
 * @param {number} especialidadId - ID de la especialidad seleccionada
 */
function cargarMedicos(especialidadId) {
    if (!especialidadId) return;
    
    console.log(`Cargando médicos para especialidad: ${especialidadId}`);
    
    // Mostrar indicador de carga
    const $medicoSelect = $('#medico_id');
    $medicoSelect.prop('disabled', true).empty();
    
    // Agregar opción por defecto
    $medicoSelect.append(new Option('Cargando médicos...', '', true, true));
    
    // Realizar la petición AJAX
    $.ajax({
        url: `${apiUrl}api/medicos/`,
        method: 'GET',
        data: {
            especialidad_id: especialidadId
        },
        success: function(response) {
            console.log('Respuesta de la API:', response);
            
            // Verificar si la respuesta es exitosa
            if (response.success && response.medicos) {
                // Limpiar y habilitar el select
                $medicoSelect.empty().prop('disabled', false);
                
                // Agregar opción por defecto
                $medicoSelect.append(new Option('Seleccione un médico', '', true, true));
                
                // Agregar médicos
                response.medicos.forEach(function(medico) {
                    $medicoSelect.append(new Option(
                        `${medico.Nombres_Medico} ${medico.Apellidos_Medicos}`,
                        medico.id_Medico,
                        false,
                        false
                    ));
                });
                
                if (response.medicos.length === 0) {
                    $medicoSelect.append(new Option('No hay médicos disponibles', '', true, true));
                    $medicoSelect.prop('disabled', true);
                }
            } else {
                console.error('Error en la respuesta de la API:', response.error || 'Respuesta inesperada');
                mostrarAlerta('Error al cargar los médicos. ' + (response.error || ''), 'error');
                $medicoSelect.empty().append(new Option('Error al cargar médicos', '', true, true));
                $medicoSelect.prop('disabled', true);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error en la petición AJAX:', {
                status: xhr.status,
                statusText: xhr.statusText,
                responseText: xhr.responseText,
                error: error
            });
            mostrarAlerta('Error al cargar la lista de médicos: ' + (xhr.responseJSON?.error || error), 'error');
            $medicoSelect.empty().prop('disabled', true).append(new Option('Error al cargar', '', true, true));
        },
        complete: function() {
            $('.loading-overlay').fadeOut(200);
        }
    });
}

/**
 * Maneja la selección de un slot en el calendario
 * @param {Object} info - Información del evento de FullCalendar
 */
function seleccionarSlot(info) {
    console.log('Slot seleccionado:', info);
    
    // Verificar si el slot está disponible
    if (info.event && info.event.extendedProps && info.event.extendedProps.disponible === false) {
        mostrarAlerta('Este horario no está disponible. Por favor, seleccione otro.', 'warning');
        return;
    }
    
    // Guardar la cita seleccionada
    window.citaSeleccionada = {
        start: info.event.start,
        end: info.event.end,
        medico_id: window.medicoSeleccionado
    };
    
    console.log('Cita seleccionada:', window.citaSeleccionada);
    
    // Mostrar el botón de confirmar cita
    $('#btn-confirmar-cita').removeClass('d-none');
    
    // Mostrar mensaje de confirmación
    mostrarAlerta('Horario seleccionado. Por favor, complete el formulario y confirme la cita.', 'success');
}

/**
 * Valida el formulario antes de enviar
 * @returns {boolean} - True si el formulario es válido, false en caso contrario
 */
function validarFormulario() {
    if (!$('input[name="paciente_id"]').val()) {
        mostrarAlerta('Debe seleccionar un paciente', 'error');
        return false;
    }
    if (!$('#especialidad_id').val()) {
        mostrarAlerta('Debe seleccionar una especialidad', 'error');
        return false;
    }
    if (!$('#medico_id').val()) {
        mostrarAlerta('Debe seleccionar un médico', 'error');
        return false;
    }
    if (!window.citaSeleccionada) {
        mostrarAlerta('Debe seleccionar un horario para la cita', 'error');
        return false;
    }
    return true;
}

/**
 * Muestra una alerta en la interfaz
 * @param {string} mensaje - Mensaje a mostrar
 * @param {string} tipo - Tipo de alerta (success, error, warning, info)
 */
function mostrarAlerta(mensaje, tipo = 'info') {
    // Limpiar alertas anteriores
    $('#alerta-container').empty();
    
    // Mapear tipos de alerta a clases de Bootstrap
    const clases = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    };
    
    // Iconos para cada tipo de alerta
    const iconos = {
        'success': 'fa-check-circle',
        'error': 'fa-exclamation-circle',
        'warning': 'fa-exclamation-triangle',
        'info': 'fa-info-circle'
    };
    
    // Crear elemento de alerta
    const $alerta = $(`
        <div class="alert ${clases[tipo] || 'alert-info'} alert-dismissible fade show" role="alert">
            <i class="fas ${iconos[tipo] || 'fa-info-circle'} me-2"></i>
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
        </div>
    `);
    
    // Agregar al contenedor
    $('#alerta-container').append($alerta);
    
    // Desaparecer después de 5 segundos (excepto si es un error)
    if (tipo !== 'error') {
        setTimeout(() => {
            $alerta.alert('close');
        }, 5000);
    }
}

    // Inicializar el select de médico como deshabilitado hasta que se seleccione especialidad
    $('#medico_id').prop('disabled', true);
    
    // Inicializar el calendario
    inicializarCalendario();
    
    // Manejar cambio de especialidad
    $('#especialidad_id').on('change', function() {
        const especialidadId = $(this).val();
        window.especialidadSeleccionada = especialidadId;
        
        // Limpiar la selección de médico
        $('#medico_id').val('').trigger('change');
        
        // Cargar médicos para la especialidad seleccionada
        if (especialidadId) {
            cargarMedicos(especialidadId);
        } else {
            $('#medico_id').empty().append('<option value="">Seleccione una especialidad primero</option>').prop('disabled', true);
        }
        
        // Limpiar el calendario
        if (window.calendar) {
            window.calendar.removeAllEvents();
        }
    });
    
    // Manejar cambio de médico
    $('#medico_id').on('change', function() {
        const medicoId = $(this).val();
        window.medicoSeleccionado = medicoId;
        
        // Actualizar el calendario si hay un médico seleccionado
        if (window.calendar) {
            if (medicoId) {
                console.log('Cambiando a médico ID:', medicoId);
                // Forzar recarga de eventos y cambiar a vista semanal
                window.calendar.refetchEvents();
                window.calendar.changeView('timeGridWeek');
                // Forzar actualización del calendario
                setTimeout(() => {
                    window.calendar.updateSize();
                }, 100);
            } else {
                // Limpiar el calendario si no hay médico seleccionado
                window.calendar.removeAllEvents();
            }
        }
    });
    
    // Manejar envío del formulario
    $('#form-cita').on('submit', function(e) {
        e.preventDefault();
        
        if (validarFormulario()) {
            const formData = new FormData(this);
            
            // Agregar los datos de la cita seleccionada
            if (window.citaSeleccionada) {
                formData.append('fecha', window.citaSeleccionada.start.toISOString());
                formData.append('medico_id', window.medicoSeleccionado);
            }
            
            // Mostrar loading
            $('.loading-overlay').fadeIn(200);
            
            // Enviar los datos al servidor
            $.ajax({
                url: $(this).attr('action'),
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                    if (response.success) {
                        mostrarAlerta('Cita agendada correctamente', 'success');
                        // Redirigir a la página de confirmación después de 2 segundos
                        setTimeout(() => {
                            window.location.href = response.redirect_url || '/';
                        }, 2000);
                    } else {
                        mostrarAlerta(response.error || 'Error al agendar la cita', 'error');
                    }
                },
                error: function(xhr) {
                    let errorMessage = 'Error al procesar la solicitud';
                    try {
                        const response = JSON.parse(xhr.responseText);
                        errorMessage = response.error || errorMessage;
                    } catch (e) {
                        console.error('Error parsing error response:', e);
                    }
                    mostrarAlerta(errorMessage, 'error');
                },
                complete: function() {
                    $('.loading-overlay').fadeOut(200);
                }
            });
        }
    });

/**
 * Inicializa el calendario de FullCalendar
 */
function inicializarCalendario() {
    try {
        console.log('Inicializando calendario...');
        
        // Obtener el elemento del calendario
        const calendarEl = document.getElementById('calendario');
        if (!calendarEl) {
            console.error('No se encontró el elemento con ID "calendario"');
            return;
        }
        
        // Configuración del calendario
        const config = {
            ...calendarConfig,
            
            // Mejorar el renderizado de eventos
            eventDidMount: function(info) {
                if (info.event.extendedProps.descripcion) {
                    new bootstrap.Tooltip(info.el, {
                        title: info.event.extendedProps.descripcion,
                        placement: 'top',
                        trigger: 'hover',
                        container: 'body'
                    });
                }
            },
            
            // Función para cargar eventos
            events: function(fetchInfo, successCallback, failureCallback) {
                console.log('Buscando eventos para el rango:', fetchInfo.start, 'a', fetchInfo.end);
                
                // Si no hay médico seleccionado, no cargar eventos
                if (!window.medicoSeleccionado) {
                    console.log('No hay médico seleccionado. No se cargarán eventos.');
                    successCallback([]);
                    return;
                }
                
                // Mostrar loading
                $('.loading-overlay').fadeIn(200);
                
                // Obtener el token CSRF
                function getCookie(name) {
                    let cookieValue = null;
                    if (document.cookie && document.cookie !== '') {
                        const cookies = document.cookie.split(';');
                        for (let i = 0; i < cookies.length; i++) {
                            const cookie = cookies[i].trim();
                            // Buscar el token CSRF
                            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                const csrftoken = getCookie('csrftoken');
                
                // Hacer la petición para obtener la disponibilidad
                $.ajax({
                    url: `${apiUrl}api/obtener-citas-y-disponibilidad/`,
                    type: 'POST',
                    contentType: 'application/json',
                    headers: {
                        'X-CSRFToken': csrftoken  // Incluir el token CSRF en los encabezados
                    },
                    data: JSON.stringify({
                        medico_id: window.medicoSeleccionado,
                        especialidad_id: window.especialidadSeleccionada,
                        start: fetchInfo.start.toISOString().split('T')[0],
                        end: fetchInfo.end.toISOString().split('T')[0]
                    }),
                    success: function(response) {
                        console.log('Eventos cargados:', response);
                        
                        const events = [];
                        
                        // Procesar eventos de disponibilidad
                        if (response.disponibilidad && Array.isArray(response.disponibilidad)) {
                            response.disponibilidad.forEach(function(disp) {
                                events.push({
                                    id: `disp-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
                                    title: disp.title || 'Disponible',
                                    start: disp.start,
                                    end: disp.end,
                                    backgroundColor: disp.backgroundColor || '#dff0d8',
                                    borderColor: disp.borderColor || '#d6e9c6',
                                    display: disp.display || 'background',
                                    className: 'disponible-slot cursor-pointer',
                                    extendedProps: {
                                        tipo: 'disponibilidad',
                                        duracion_cita: (disp.extendedProps && disp.extendedProps.duracion_cita) || 30,
                                        hora: disp.start ? new Date(disp.start).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }) : ''
                                    },
                                    editable: false,
                                    startEditable: false,
                                    durationEditable: false,
                                    resourceEditable: false
                                });
                            });
                        }
                        
                        // Procesar citas existentes
                        if (response.citas && Array.isArray(response.citas)) {
                            response.citas.forEach(function(cita) {
                                events.push({
                                    id: `cita-${cita.id}`,
                                    title: cita.title || 'Cita',
                                    start: cita.start,
                                    end: cita.end,
                                    backgroundColor: cita.backgroundColor || '#4e73df',
                                    borderColor: cita.borderColor || '#4e73df',
                                    textColor: cita.textColor || '#fff',
                                    className: 'cita-agendada',
                                    extendedProps: {
                                        tipo: 'cita',
                                        id_cita: cita.id,
                                        estado: cita.estado || 'PENDIENTE',
                                        paciente: cita.extendedProps?.paciente_nombre || 'Paciente no especificado',
                                        telefono: cita.extendedProps?.paciente_telefono || 'No especificado',
                                        notas: cita.extendedProps?.notas || 'Ninguna',
                                        ...(cita.extendedProps || {})
                                    },
                                    editable: false,
                                    startEditable: false,
                                    durationEditable: false,
                                    resourceEditable: false
                                });
                            });
                        }
                        
                        console.log('Eventos procesados:', events);
                        console.log('Eventos procesados:', events);
                        successCallback(events);
                        
                        // Forzar actualización del calendario después de cargar los eventos
                        setTimeout(() => {
                            window.calendar.updateSize();
                        }, 100);
                    },
                    error: function(xhr, status, error) {
                        console.error('Error al cargar eventos:', {
                            status: xhr.status,
                            statusText: xhr.statusText,
                            responseText: xhr.responseText,
                            error: error
                        });
                        mostrarAlerta('Error al cargar la disponibilidad: ' + (xhr.responseJSON?.error || error), 'error');
                        failureCallback(xhr.responseJSON || { error: error });
                    },
                    complete: function() {
                        $('.loading-overlay').fadeOut(200);
                    }
                });
            },
            // Manejar clic en un evento
            eventClick: function(info) {
                if (info.event.extendedProps.tipo === 'disponible') {
                    seleccionarSlot(info.event);
                }
            },
            // Actualizar título al cambiar de vista/fecha
            datesSet: function(dateInfo) {
                console.log('Cambio de vista/fecha:', dateInfo.view.type, dateInfo.start, dateInfo.end);
                // Actualizar el título con el rango de fechas
                const title = dateInfo.view.title;
                $('.fc-toolbar-title').text(title);
            },
            // Manejar estado de carga
            loading: function(isLoading) {
                if (isLoading) {
                    $('.loading-overlay').fadeIn(200);
                } else {
                    $('.loading-overlay').fadeOut(200);
                }
            }
        };
        
        // Inicializar y renderizar el calendario con la configuración
        window.calendar = new FullCalendar.Calendar(calendarEl, config);
        window.calendar.render();
        
        console.log('✅ Calendario inicializado correctamente');
    } catch (error) {
        console.error('❌ Error al inicializar el calendario:', error);
        mostrarAlerta('Error al inicializar el calendario. Por favor, recargue la página.', 'error');
    }
}

/**
 * Muestra una alerta en la interfaz
 * @param {string} mensaje - Mensaje a mostrar
 * @param {string} tipo - Tipo de alerta (success, error, warning, info)
 */
function mostrarAlerta(mensaje, tipo = 'info') {
    // Limpiar alertas anteriores
    $('#alerta-container').empty();
    
    // Mapear tipos de alerta a clases de Bootstrap
    const clases = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    };
    
    // Crear elemento de alerta
    const $alerta = $(`
        <div class="alert ${clases[tipo] || 'alert-info'} alert-dismissible fade show" role="alert">
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
        </div>
    `);
    
    // Agregar al contenedor
    $('#alerta-container').append($alerta);
    
    // Desaparecer después de 5 segundos
    setTimeout(() => {
        $alerta.alert('close');
    }, 5000);
}

// Inicialización de la aplicación cuando el DOM esté listo
$(document).ready(function() {
    console.log('🚀 Inicializando aplicación...');
    
    // Inicializar tooltips de Bootstrap
    $('[data-bs-toggle="tooltip"]').tooltip();
    
    // Inicializar el calendario
    try {
        console.log('🔄 Inicializando calendario...');
        inicializarCalendario();
        console.log('✅ Calendario inicializado correctamente');
    } catch (error) {
        console.error('❌ Error al inicializar el calendario:', error);
        mostrarAlerta('Error al inicializar el calendario. Por favor, recargue la página.', 'error');
    }
    
    // Manejador de eventos para el cambio de especialidad
    $('#especialidad_id').on('change', function() {
        const especialidadId = $(this).val();
        console.log('🔵 Cambio de especialidad:', especialidadId);
        
        if (especialidadId) {
            window.especialidadSeleccionada = especialidadId;
            $('#medico_id').prop('disabled', false);
            cargarMedicos(especialidadId);
        } else {
            window.especialidadSeleccionada = null;
            $('#medico_id').prop('disabled', true).empty().append('<option value="">Seleccione un médico</option>');
        }
        
        // Limpiar selección de médico
        window.medicoSeleccionado = null;
        $('#medico_id').val('').trigger('change');
    });
    
    // Manejador de eventos para el cambio de médico
    $('#medico_id').on('change', function() {
        const medicoId = $(this).val();
        console.log('🟣 Cambio de médico:', medicoId);
        
        if (medicoId) {
            window.medicoSeleccionado = medicoId;
            
            // Refrescar el calendario para mostrar la disponibilidad del médico
            if (window.calendar) {
                console.log('🔄 Actualizando calendario...');
                window.calendar.refetchEvents();
            }
        } else {
            window.medicoSeleccionado = null;
            
            // Limpiar el calendario
            if (window.calendar) {
                window.calendar.removeAllEvents();
            }
        }
    });
    
    console.log('✅ Aplicación inicializada correctamente');
});
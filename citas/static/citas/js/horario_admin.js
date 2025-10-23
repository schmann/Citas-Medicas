(function($) {
    'use strict';
    
    // Función para inicializar o actualizar los campos Select2
    function initSelect2Fields() {
        // Obtener referencias a los campos
        const $medicoField = $('select[name$="-medico"], #id_medico').first();
        const $especialidadField = $('select[name$="-especialidad"], #id_especialidad').first();
        
        // Si no existen los campos, salir
        if ($medicoField.length === 0 || $especialidadField.length === 0) {
            console.log('Campos de médico o especialidad no encontrados');
            return;
        }
        
        console.log('Inicializando campos:', {
            medico: $medicoField.attr('id') || $medicoField.attr('name'),
            especialidad: $especialidadField.attr('id') || $especialidadField.attr('name')
        });
        
        // Función segura para inicializar o actualizar Select2
        function safeSelect2($element, options) {
            try {
                // Destruir Select2 si ya está inicializado
                if ($.fn.select2 && $element.hasClass('select2-hidden-accessible')) {
                    try {
                        $element.select2('destroy');
                    } catch (e) {
                        console.warn('No se pudo destruir la instancia anterior de Select2:', e);
                    }
                    // Eliminar cualquier contenedor de Select2 existente
                    $element.next('.select2-container').remove();
                }
                
                // Inicializar Select2 con las opciones proporcionadas
                return $element.select2(options);
            } catch (e) {
                console.error('Error al inicializar Select2:', e);
                return $element;
            }
        }
        
        // Inicializar el campo de médico con Select2
        safeSelect2($medicoField, {
            width: '100%',
            placeholder: 'Seleccione un médico',
            allowClear: true
        });
        
        // Inicializar el campo de especialidad con Select2
        const especialidadOptions = {
            width: '78%',
            placeholder: 'Seleccione una especialidad',
            allowClear: true,
            disabled: !$medicoField.val()
        };
        
        safeSelect2($especialidadField, especialidadOptions);
        
        // Función para cargar especialidades
        function cargarEspecialidades(medicoId) {
            if (!medicoId) {
                $especialidadField.empty().prop('disabled', true).trigger('change');
                return;
            }
            
            console.log('Cargando especialidades para el médico ID:', medicoId);
            
            // Mostrar indicador de carga
            $especialidadField.prop('disabled', true).empty();
            
            // Crear un nuevo elemento option para mostrar el mensaje de carga
            const loadingOption = new Option('Cargando especialidades...', '', true, true);
            loadingOption.disabled = true;
            $especialidadField.append(loadingOption);
            
            // Forzar actualización del Select2
            if ($especialidadField.hasClass('select2-hidden-accessible')) {
                $especialidadField.trigger('change.select2');
            }
            
            // Hacer la petición AJAX
            fetch(`/citas/api/get-especialidades/${medicoId}/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Error HTTP: ${response.status}`);
                    }
                    return response.json();
                })
                .then(especialidades => {
                    console.log('Especialidades recibidas:', especialidades);
                    
                    // Limpiar el select
                    $especialidadField.empty();
                    
                    // Añadir opción por defecto
                    $especialidadField.append(new Option('Seleccione una especialidad', '', true, true));
                    
                    if (especialidades && especialidades.length > 0) {
                        // Añadir cada especialidad al select
                        especialidades.forEach(esp => {
                            // Usar el nombre de la propiedad correcta según la respuesta de la API
                            const nombre = esp.nombre || esp.Espacialidad_Medica || 'Especialidad sin nombre';
                            $especialidadField.append(new Option(nombre, esp.id, false, false));
                        });
                    } else {
                        $especialidadField.append(new Option('No hay especialidades disponibles', '', true, true));
                        $especialidadField.find('option:first').prop('disabled', true);
                    }
                    
                    // Habilitar el select
                    $especialidadField.prop('disabled', false);
                    
                    // Actualizar Select2
                    if ($especialidadField.hasClass('select2-hidden-accessible')) {
                        $especialidadField.trigger('change');
                    }
                    
                    console.log('Especialidades cargadas en el select');
                })
                .catch(error => {
                    console.error('Error al cargar especialidades:', error);
                    $especialidadField.empty()
                        .append(new Option('Error al cargar especialidades', '', true, true))
                        .prop('disabled', true);
                    
                    if ($especialidadField.hasClass('select2-hidden-accessible')) {
                        $especialidadField.trigger('change');
                    }
                });
        }
        
        // Manejar cambio en el campo de médico
        $medicoField.off('change.select2').on('change.select2', function() {
            const medicoId = $(this).val();
            console.log('Cambio en campo médico - ID seleccionado:', medicoId);
            cargarEspecialidades(medicoId);
        });
        
        // Manejar evento select2:select para mayor compatibilidad
        $medicoField.off('select2:select').on('select2:select', function(e) {
            const medicoId = $(this).val();
            console.log('Evento select2:select - ID del médico seleccionado:', medicoId);
            cargarEspecialidades(medicoId);
        });
        
        // Cargar especialidades si ya hay un médico seleccionado (en caso de edición)
        if ($medicoField.val()) {
            console.log('Cargando especialidades para médico existente:', $medicoField.val());
            cargarEspecialidades($medicoField.val());
        }
    }
    
    // Inicializar cuando el DOM esté listo
    $(document).ready(function() {
        console.log('Script de horario_admin.js cargado');
        
        // Inicializar los campos al cargar la página
        initSelect2Fields();
        
        // Manejar el evento de adición de formularios en el admin de Django
        $(document).on('formset:added', function(event, $row, formsetName) {
            console.log('Nuevo formulario añadido:', formsetName);
            // Esperar un momento para que se añadan los campos al DOM
            setTimeout(initSelect2Fields, 100);
        });
    });
    
})(django.jQuery);

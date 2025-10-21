/* Script: direccion_admin.js */

console.log('Script direccion_admin.js cargado correctamente');

(function($) {
    $(document).ready(function() {
        console.log('Documento listo, inicializando selectores...');
        
        // --- 1. Definición y Búsqueda de Selectores ---
        
        // Usamos el selector de atributo que termina en el nombre del campo 
        // para manejar posibles prefijos de inlines (e.g., id_direccion-0-campo)
        let $estado = $('select[id$="-estado"]');
        let $ciudad = $('select[id$="-ciudad"]');
        let $municipio = $('select[id$="-municipio"]');
        let $parroquia = $('select[id$="-parroquia"]');
        
        console.log('Selectores encontrados:', {
            estado: $estado.length > 0 ? $estado.attr('id') : 'No encontrado',
            ciudad: $ciudad.length > 0 ? $ciudad.attr('id') : 'No encontrado',
            municipio: $municipio.length > 0 ? $municipio.attr('id') : 'No encontrado',
            parroquia: $parroquia.length > 0 ? $parroquia.attr('id') : 'No encontrado'
        });

        // Verificar que todos los selectores necesarios existen. Si no, detener.
        if ($estado.length === 0 || $municipio.length === 0 || $parroquia.length === 0) {
            console.error('ERROR: No se encontraron todos los selectores de dirección. Deteniendo script.');
            return;
        }

        // --- 2. Funciones de Carga AJAX ---

        // Función auxiliar para realizar la petición AJAX genérica
        function cargarDatos(url_path, paramName, paramValue, $targetSelect, defaultMessage, successCallback) {
            console.log(`=== cargarDatos [${paramName}] ===`);
            
            paramValue = parseInt(paramValue);
            if (isNaN(paramValue) || paramValue <= 0) {
                console.error(`ID de parámetro no válido: ${paramValue}`);
                $targetSelect.empty().append($('<option>', {value: '', text: defaultMessage, selected: true, disabled: true}));
                $targetSelect.prop('disabled', true);
                return Promise.resolve();
            }
            
            const url = `/admin/citas/paciente/${url_path}/?${paramName}=${paramValue}`;
            console.log('URL de la solicitud:', url);
            
            // Limpiar y poner mensaje de carga antes de la petición
            $targetSelect.empty().append($('<option>', {value: '', text: 'Cargando...', selected: true, disabled: true}));
            $targetSelect.prop('disabled', true);

            return new Promise((resolve, reject) => {
                $.ajax({
                    url: url,
                    type: 'GET',
                    dataType: 'json',
                    success: function(data) {
                        console.log(`Datos recibidos para ${$targetSelect.attr('id')}:`, data);
                        
                        $targetSelect.empty().append($('<option>', {value: '', text: defaultMessage, selected: true, disabled: true}));
                        
                        if (data && data.length > 0) {
                            successCallback(data, $targetSelect);
                            console.log(`Se cargaron ${data.length} elementos`);
                        } else {
                            console.warn(`No se encontraron datos para ${$targetSelect.attr('id')}`);
                            $targetSelect.append($('<option>', {value: '', text: `No hay opciones disponibles`, selected: true, disabled: true}));
                        }
                        
                        $targetSelect.prop('disabled', false);
                        resolve(data);
                    },
                    error: function(xhr, status, error) {
                        console.error(`Error al cargar ${$targetSelect.attr('id')}:`, error);
                        $targetSelect.empty().append($('<option>', {value: '', text: 'Error al cargar', selected: true, disabled: true}));
                        reject(error);
                    }
                });
            });
        }
        
        // Función para cargar ciudades
        function cargarCiudades(estadoId) {
            return cargarDatos(
                'get_ciudades', 
                'estado_id', 
                estadoId, 
                $ciudad, 
                'Seleccione una ciudad',
                function(data, $select) {
                    data.forEach(function(ciudad) {
                        $select.append($('<option>', { value: ciudad.id_Ciudad, text: ciudad.nombre }));
                    });
                }
            );
        }

        // Función para cargar municipios
        function cargarMunicipios(estadoId) {
            return cargarDatos(
                'get_municipios', 
                'estado_id', // Asumiendo que municipios también se filtran por estado
                estadoId, 
                $municipio, 
                'Seleccione un municipio',
                function(data, $select) {
                    data.forEach(function(municipio) {
                        $select.append($('<option>', { value: municipio.id_Municipio, text: municipio.nombre }));
                    });
                }
            );
        }

        // Función para cargar parroquias
        function cargarParroquias(municipioId) {
            return cargarDatos(
                'get_parroquias', 
                'municipio_id', 
                municipioId, 
                $parroquia, 
                'Seleccione una parroquia',
                function(data, $select) {
                    data.forEach(function(parroquia) {
                        $select.append($('<option>', { value: parroquia.id_Parroquia, text: parroquia.nombre }));
                    });
                }
            );
        }

        // --- 3. Inicialización y Manejadores de Eventos ---

        function inicializarEventos() {
            console.log('=== inicializarEventos ===');
            
            // Función para limpiar un select dependiente
            function limpiarSelect($select, mensaje) {
                $select.empty().append($('<option>', {
                    value: '',
                    text: mensaje || '---------',
                    selected: true,
                    disabled: true
                }));
            }
            
            // Limpiar y deshabilitar selects dependientes al inicio
            limpiarSelect($ciudad, 'Seleccione un estado primero');
            limpiarSelect($municipio, 'Seleccione un estado primero');
            limpiarSelect($parroquia, 'Seleccione un municipio primero');
            
            $ciudad.prop('disabled', true);
            $municipio.prop('disabled', true);
            $parroquia.prop('disabled', true);
            
            // Manejador para el cambio de Estado
            function manejarCambioEstado() {
                const estadoId = $estado.val();
                console.log('Estado seleccionado (ID):', estadoId);
                
                // Limpiar selects dependientes
                limpiarSelect($ciudad, estadoId ? 'Cargando ciudades...' : 'Seleccione un estado primero');
                limpiarSelect($municipio, estadoId ? 'Cargando municipios...' : 'Seleccione un estado primero');
                limpiarSelect($parroquia, 'Seleccione un municipio primero');

                // Deshabilitar
                $ciudad.prop('disabled', true);
                $municipio.prop('disabled', true);
                $parroquia.prop('disabled', true);
                
                if (estadoId) {
                    // Cargar ciudades y municipios en paralelo
                    Promise.all([
                        cargarCiudades(estadoId),
                        cargarMunicipios(estadoId)
                    ]).then(([ciudadesData, municipiosData]) => {
                        console.log('Carga de ciudades y municipios completada.');
                        
                        // Si se cargan municipios, verificar si hay un municipio preseleccionado
                        const municipioInicial = $municipio.data('initial-value');
                        if (municipioInicial && municipiosData && municipiosData.some(m => m.id_Municipio === municipioInicial)) {
                            $municipio.val(municipioInicial).trigger('change');
                            $municipio.removeData('initial-value'); // Limpiar el valor inicial
                        }
                    }).catch(error => {
                        console.error('Error durante la carga paralela de datos:', error);
                    });
                }
            }
            
            // Manejador para el cambio de Municipio
            function manejarCambioMunicipio() {
                const municipioId = $municipio.val();
                console.log('Municipio seleccionado (ID):', municipioId);
                
                limpiarSelect($parroquia, municipioId ? 'Cargando parroquias...' : 'Seleccione un municipio primero');
                $parroquia.prop('disabled', true);
                
                if (municipioId) {
                    cargarParroquias(municipioId).then(parroquiasData => {
                        // Si hay un valor inicial de parroquia, seleccionarlo
                        const parroquiaInicial = $parroquia.data('initial-value');
                        if (parroquiaInicial && parroquiasData && parroquiasData.some(p => p.id_Parroquia === parroquiaInicial)) {
                            $parroquia.val(parroquiaInicial);
                            $parroquia.removeData('initial-value'); // Limpiar el valor inicial
                        }
                    });
                }
            }
            
            // Almacenar valores iniciales (si existen) antes de limpiar/disparar el change
            $municipio.data('initial-value', $municipio.val());
            $parroquia.data('initial-value', $parroquia.val());
            
            // Asignar manejadores de eventos (usando .off().on() para prevenir múltiples asignaciones)
            $estado.off('change').on('change', manejarCambioEstado);
            $municipio.off('change').on('change', manejarCambioMunicipio);
            
            // Disparar el evento change si ya hay un valor seleccionado
            if ($estado.val()) {
                console.log('Estado inicial detectado, disparando evento change para cargar dependientes...');
                manejarCambioEstado(); // Llama a la función directamente, ya que .trigger('change') a veces falla en inlines
            } else {
                console.log('No se detectó un estado seleccionado inicialmente.');
            }
        }

        inicializarEventos();
    });
})(django.jQuery);
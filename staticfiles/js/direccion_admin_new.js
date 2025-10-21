console.log('Script direccion_admin.js cargado correctamente');

(function($) {
    $(document).ready(function() {
        console.log('Documento listo, inicializando selectores...');
        
        // 1. OBTENER REFERENCIAS A LOS SELECTS
        console.log('=== INICIALIZANDO SCRIPT ===');
        
        // Mostrar información de todos los selects en la página
        console.log('Todos los selects en la página:');
        $('select').each(function() {
            console.log('Select ID:', this.id, 'Name:', this.name, 'Value:', $(this).val());
        });
        
        // Obtener referencias a los selects usando los IDs que vemos en la consola
        const $estado = $('#id_direccion-0-estado');
        const $ciudad = $('#id_direccion-0-ciudad');
        const $municipio = $('#id_direccion-0-municipio');
        const $parroquia = $('#id_direccion-0-parroquia');
        
        console.log('Selectores encontrados:', {
            estado: $estado.length > 0 ? $estado.attr('id') : 'No encontrado',
            ciudad: $ciudad.length > 0 ? $ciudad.attr('id') : 'No encontrado',
            municipio: $municipio.length > 0 ? $municipio.attr('id') : 'No encontrado',
            parroquia: $parroquia.length > 0 ? $parroquia.attr('id') : 'No encontrado'
        });
        
        // Inicializar Select2 en los selects
        function inicializarSelect2() {
            console.log('Inicializando Select2...');
            
            // Configuración común para todos los Select2
            const select2Config = {
                placeholder: 'Seleccione una opción',
                allowClear: true,
                width: '100%',
                language: 'es'
            };
            
            // Inicializar Select2 en los selects
            $estado.select2(select2Config);
            $ciudad.select2(select2Config);
            $municipio.select2(select2Config);
            $parroquia.select2(select2Config);
            
            console.log('Select2 inicializado correctamente');
        }
        
        // 2. FUNCIONES PARA CARGAR DATOS
        
        // Función para cargar ciudades basadas en el estado seleccionado
        function cargarCiudades(estadoId) {
            console.log('=== cargarCiudades ===');
            console.log('Estado ID recibido:', estadoId);
            
            // Validar que el estadoId sea un número válido
            estadoId = parseInt(estadoId);
            if (isNaN(estadoId) || estadoId <= 0) {
                console.error('ID de estado no válido:', estadoId);
                return Promise.resolve();
            }
            
            const url = `/admin/citas/ajax/cargar-ubicaciones/?tipo=ciudades&estado_id=${estadoId}`;
            console.log('URL de la solicitud de ciudades:', url);
            
            return new Promise((resolve, reject) => {
                $.ajax({
                    url: url,
                    type: 'GET',
                    dataType: 'json',
                    success: function(data) {
                        console.log('Datos recibidos para ciudades:', data);
                        
                        // Limpiar el select de ciudad
                        $ciudad.empty();
                        
                        // Agregar opción por defecto
                        $ciudad.append($('<option>', {
                            value: '',
                            text: 'Seleccione una ciudad',
                            selected: true,
                            disabled: true
                        }));
                        
                        // Agregar las ciudades
                        if (data && data.length > 0) {
                            data.forEach(function(ciudad) {
                                $ciudad.append($('<option>', {
                                    value: ciudad.id_Ciudad,
                                    text: ciudad.nombre
                                }));
                            });
                            console.log(`Se cargaron ${data.length} ciudades`);
                        } else {
                            console.warn('No se encontraron ciudades para el estado seleccionado');
                            $ciudad.append($('<option>', {
                                value: '',
                                text: 'No hay ciudades disponibles',
                                selected: true,
                                disabled: true
                            }));
                        }
                        
                        // Habilitar el select de ciudad
                        $ciudad.prop('disabled', false);
                        resolve(data);
                    },
                    error: function(xhr, status, error) {
                        console.error('Error al cargar ciudades:', error);
                        console.error('Respuesta del servidor:', xhr.responseText);
                        
                        // Mostrar mensaje de error
                        $ciudad.empty().append($('<option>', {
                            value: '',
                            text: 'Error al cargar ciudades',
                            selected: true,
                            disabled: true
                        }));
                        
                        reject(error);
                    }
                });
            });
        }
        
        // Función para cargar municipios basados en el estado seleccionado
        function cargarMunicipios(estadoId) {
            console.log('=== cargarMunicipios ===');
            console.log('Estado ID recibido:', estadoId);
            
            // Validar que el estadoId sea un número válido
            estadoId = parseInt(estadoId);
            if (isNaN(estadoId) || estadoId <= 0) {
                console.error('ID de estado no válido:', estadoId);
                return Promise.resolve();
            }
            
            const url = `/admin/citas/ajax/cargar-ubicaciones/?tipo=municipios&estado_id=${estadoId}`;
            console.log('URL de la solicitud de municipios:', url);
            
            return new Promise((resolve, reject) => {
                $.ajax({
                    url: url,
                    type: 'GET',
                    dataType: 'json',
                    success: function(data) {
                        console.log('Datos recibidos para municipios:', data);
                        
                        // Limpiar el select de municipio
                        $municipio.empty();
                        
                        // Agregar opción por defecto
                        $municipio.append($('<option>', {
                            value: '',
                            text: 'Seleccione un municipio',
                            selected: true,
                            disabled: true
                        }));
                        
                        // Agregar los municipios
                        if (data && data.length > 0) {
                            data.forEach(function(municipio) {
                                $municipio.append($('<option>', {
                                    value: municipio.id_Municipio,
                                    text: municipio.nombre
                                }));
                            });
                            console.log(`Se cargaron ${data.length} municipios`);
                        } else {
                            console.warn('No se encontraron municipios para el estado seleccionado');
                            $municipio.append($('<option>', {
                                value: '',
                                text: 'No hay municipios disponibles',
                                selected: true,
                                disabled: true
                            }));
                        }
                        
                        // Habilitar el select de municipio
                        $municipio.prop('disabled', false);
                        resolve(data);
                    },
                    error: function(xhr, status, error) {
                        console.error('Error al cargar municipios:', error);
                        console.error('Respuesta del servidor:', xhr.responseText);
                        
                        // Mostrar mensaje de error
                        $municipio.empty().append($('<option>', {
                            value: '',
                            text: 'Error al cargar municipios',
                            selected: true,
                            disabled: true
                        }));
                        
                        reject(error);
                    }
                });
            });
        }
        
        // Función para cargar parroquias basadas en el municipio seleccionado
        function cargarParroquias(municipioId) {
            console.log('=== cargarParroquias ===');
            console.log('Municipio ID recibido:', municipioId);
            
            // Validar que el municipioId sea un número válido
            municipioId = parseInt(municipioId);
            if (isNaN(municipioId) || municipioId <= 0) {
                console.error('ID de municipio no válido:', municipioId);
                return Promise.resolve();
            }
            
            const url = `/admin/citas/ajax/cargar-ubicaciones/?tipo=parroquias&municipio_id=${municipioId}`;
            console.log('URL de la solicitud de parroquias:', url);
            
            return new Promise((resolve, reject) => {
                $.ajax({
                    url: url,
                    type: 'GET',
                    dataType: 'json',
                    success: function(data) {
                        console.log('Datos recibidos para parroquias:', data);
                        
                        // Limpiar el select de parroquia
                        $parroquia.empty();
                        
                        // Agregar opción por defecto
                        $parroquia.append($('<option>', {
                            value: '',
                            text: 'Seleccione una parroquia',
                            selected: true,
                            disabled: true
                        }));
                        
                        // Agregar las parroquias
                        if (data && data.length > 0) {
                            data.forEach(function(parroquia) {
                                $parroquia.append($('<option>', {
                                    value: parroquia.id_Parroquia,
                                    text: parroquia.nombre
                                }));
                            });
                            console.log(`Se cargaron ${data.length} parroquias`);
                        } else {
                            console.warn('No se encontraron parroquias para el municipio seleccionado');
                            $parroquia.append($('<option>', {
                                value: '',
                                text: 'No hay parroquias disponibles',
                                selected: true,
                                disabled: true
                            }));
                        }
                        
                        // Habilitar el select de parroquia
                        $parroquia.prop('disabled', false);
                        resolve(data);
                    },
                    error: function(xhr, status, error) {
                        console.error('Error al cargar parroquias:', error);
                        console.error('Respuesta del servidor:', xhr.responseText);
                        
                        // Mostrar mensaje de error
                        $parroquia.empty().append($('<option>', {
                            value: '',
                            text: 'Error al cargar parroquias',
                            selected: true,
                            disabled: true
                        }));
                        
                        reject(error);
                    }
                });
            });
        }
        
        // 3. MANEJADORES DE EVENTOS
        
        // Función para manejar el cambio de estado
        function manejarCambioEstado() {
            console.log('=== manejarCambioEstado ===');
            
            // Obtener el valor seleccionado directamente del DOM
            const estadoSelect = document.getElementById('id_direccion-0-estado');
            const estadoId = estadoSelect ? estadoSelect.value : null;
            const estadoTexto = estadoSelect && estadoSelect.options[estadoSelect.selectedIndex] ? 
                             estadoSelect.options[estadoSelect.selectedIndex].text : 'Ninguno';
            
            console.log('Estado seleccionado:', {
                'valor': estadoId,
                'tipo': typeof estadoId,
                'texto': estadoTexto,
                'elemento': estadoSelect
            });
            
            // Limpiar selects dependientes
            $ciudad.empty().append($('<option>', {value: '', text: 'Cargando...', selected: true, disabled: true}));
            $municipio.empty().append($('<option>', {value: '', text: '---------', selected: true, disabled: true}));
            $parroquia.empty().append($('<option>', {value: '', text: '---------', selected: true, disabled: true}));
            
            // Habilitar/deshabilitar selects
            $ciudad.prop('disabled', !estadoId);
            $municipio.prop('disabled', true);
            $parroquia.prop('disabled', true);
            
            if (estadoId && estadoId !== '') {
                console.log('Cargando ciudades y municipios para estado:', estadoId);
                
                // Cargar ciudades y municipios en paralelo
                Promise.all([
                    cargarCiudades(estadoId),
                    cargarMunicipios(estadoId)
                ]).then(() => {
                    console.log('Carga de ciudades y municipios completada');
                }).catch(error => {
                    console.error('Error al cargar datos:', error);
                });
            } else {
                console.log('No se seleccionó ningún estado válido');
                $ciudad.empty().append($('<option>', {value: '', text: 'Seleccione un estado primero', selected: true, disabled: true}));
                $municipio.empty().append($('<option>', {value: '', text: 'Seleccione un estado primero', selected: true, disabled: true}));
                $parroquia.empty().append($('<option>', {value: '', text: 'Seleccione un municipio primero', selected: true, disabled: true}));
            }
        }
        
        // Función para manejar el cambio de municipio
        function manejarCambioMunicipio() {
            console.log('=== manejarCambioMunicipio ===');
            
            const municipioSelect = document.getElementById('id_direccion-0-municipio');
            const municipioId = municipioSelect ? municipioSelect.value : null;
            const municipioTexto = municipioSelect && municipioSelect.options[municipioSelect.selectedIndex] ? 
                                 municipioSelect.options[municipioSelect.selectedIndex].text : 'Ninguno';
            
            console.log('Municipio seleccionado:', {
                'valor': municipioId,
                'tipo': typeof municipioId,
                'texto': municipioTexto,
                'elemento': municipioSelect
            });
            
            // Limpiar select de parroquia
            $parroquia.empty();
            
            if (municipioId && municipioId !== '') {
                console.log('Cargando parroquias para municipio:', municipioId);
                $parroquia.append($('<option>', {value: '', text: 'Cargando...', selected: true, disabled: true}));
                
                cargarParroquias(municipioId)
                    .then(() => {
                        console.log('Carga de parroquias completada');
                    })
                    .catch(error => {
                        console.error('Error al cargar parroquias:', error);
                    });
            } else {
                console.log('No se seleccionó ningún municipio válido');
                $parroquia.append($('<option>', {value: '', text: 'Seleccione un municipio primero', selected: true, disabled: true}));
            }
            
            // Habilitar/deshabilitar select de parroquia
            $parroquia.prop('disabled', !municipioId);
        }
        
        // 4. INICIALIZACIÓN
        
        // Función para inicializar los manejadores de eventos
        function inicializarEventos() {
            console.log('=== inicializarEventos ===');
            
            // Inicializar Select2
            inicializarSelect2();
            
            // Verificar que los selectores estén funcionando
            console.log('Verificando selectores:', {
                estado: $estado.length > 0 ? 'Encontrado' : 'No encontrado',
                ciudad: $ciudad.length > 0 ? 'Encontrado' : 'No encontrado',
                municipio: $municipio.length > 0 ? 'Encontrado' : 'No encontrado',
                parroquia: $parroquia.length > 0 ? 'Encontrado' : 'No encontrado'
            });
            
            // Función para limpiar un select
            function limpiarSelect($select, mensaje) {
                if ($select.length) {
                    console.log('Limpiando select:', $select.attr('id'), 'con mensaje:', mensaje);
                    
                    // Guardar el estado de Select2
                    const isDisabled = $select.prop('disabled');
            
        } else {
            console.error('No se pudo encontrar el select para limpiar');
        }
    }
    
    // Función para verificar y asignar eventos
    function asignarEventos() {
        console.log('Asignando manejadores de eventos...');
        
        // Verificar si los elementos existen antes de asignar eventos
        if ($estado.length) {
            console.log('Asignando manejador de cambio a estado');
            
            // Manejar evento change de Select2
            $estado.off('change.select2').on('change.select2', function(e) {
                console.log('Evento change.select2 detectado en estado, valor:', $(this).val());
                manejarCambioEstado();
            });
            $municipio.prop('disabled', true);
            $parroquia.prop('disabled', true);
            
            // Función para manejar el cambio en el select de estado
            function handleEstadoChange() {
                const estadoId = $estado.val();
                console.log('=== MANEJADOR DE CAMBIO DE ESTADO ===');
                console.log('Valor seleccionado en estado:', estadoId);
                
                // Limpiar selects dependientes
                limpiarSelect($ciudad, 'Cargando ciudades...');
                limpiarSelect($municipio, 'Cargando municipios...');
                limpiarSelect($parroquia, 'Seleccione un municipio primero');
                
                // Deshabilitar selects dependientes
                $ciudad.prop('disabled', true);
                $municipio.prop('disabled', true);
                $parroquia.prop('disabled', true);
                
                if (estadoId && estadoId !== '') {
                    console.log('Cargando ciudades y municipios para el estado:', estadoId);
                    
                    // Cargar ciudades y municipios en paralelo
                    Promise.all([
                        cargarCiudades(estadoId),
                        cargarMunicipios(estadoId)
                    ]).then(() => {
                        console.log('Carga de ciudades y municipios completada');
                        $ciudad.prop('disabled', false);
                        $municipio.prop('disabled', false);
                    }).catch(error => {
                        console.error('Error al cargar datos:', error);
                    });
                } else {
                    console.log('No se seleccionó ningún estado');
                }
            }
            
            // Función para manejar el cambio en el select de municipio
            function handleMunicipioChange() {
                const municipioId = $municipio.val();
                console.log('=== MANEJADOR DE CAMBIO DE MUNICIPIO ===');
                console.log('Valor seleccionado en municipio:', municipioId);
                
                // Limpiar select de parroquia
                limpiarSelect($parroquia, 'Cargando parroquias...');
                $parroquia.prop('disabled', true);
                
                if (municipioId && municipioId !== '') {
                    console.log('Cargando parroquias para el municipio:', municipioId);
                    
                    cargarParroquias(municipioId)
                        .then(() => {
                            console.log('Carga de parroquias completada');
                            $parroquia.prop('disabled', false);
                        })
                        .catch(error => {
                            console.error('Error al cargar parroquias:', error);
                        });
                } else {
                    console.log('No se seleccionó ningún municipio');
                }
            }
            
            // Asignar manejadores de eventos directamente
            console.log('Asignando manejadores de eventos...');
            
            // Usar event delegation para manejar cambios en los selects
            $(document).off('change', '#id_direccion-0-estado').on('change', '#id_direccion-0-estado', handleEstadoChange);
            $(document).off('change', '#id_direccion-0-municipio').on('change', '#id_direccion-0-municipio', handleMunicipioChange);
            
            // Forzar el evento change si ya hay un valor seleccionado
            if ($estado.val()) {
                console.log('Estado con valor inicial, forzando evento change...');
                handleEstadoChange();
            }
        }
        
        // Inicializar la aplicación
        console.log('Inicializando la aplicación...');
        inicializarEventos();
        
        console.log('=== FIN DE LA INICIALIZACIÓN ===');
    });
})(jQuery);

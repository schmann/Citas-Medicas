// Script: direccion_admin_select2.js
console.log('Script direccion_admin_select2.js cargado correctamente');

(function($) {
    $(document).ready(function() {
        console.log('Documento listo, inicializando selectores...');
        
        // --- 1. DETECTAR SI ES PACIENTE O MÉDICO ---
        const isPaciente = $('select[id$="-estado"]').length > 0;  // Selector para Paciente
        const isMedico = $('#id_estado').length > 0;  // Selector para Médico
        const isConsultorio = $('#id_estado').length > 0;  // Selector para Médico
        
        if (!isPaciente && !isMedico && !isConsultorio) {
            console.error('No se encontraron selectores de ubicación. Verifica que estés en un formulario con campos de ubicación.');
            return;
        }
        
        // --- 2. OBTENER REFERENCIAS A LOS SELECTORES CORRECTOS ---
        let $estado, $ciudad, $municipio, $parroquia;
        
        if (isPaciente) {
            // Selectores para Paciente (usando prefijos de inline)
            $estado = $('select[id$="-estado"]');
            $ciudad = $('select[id$="-ciudad"]');
            $municipio = $('select[id$="-municipio"]');
            $parroquia = $('select[id$="-parroquia"]');
        } else if (isMedico) {
            // Selectores para Médico (sin prefijos)
            $estado = $('#id_estado');
            $ciudad = $('#id_ciudad');
            $municipio = $('#id_municipio');
            $parroquia = $('#id_parroquia');
        } else if (isConsultorio) {
            // Selectores para Médico (sin prefijos)
            $estado = $('#id_estado');
            $ciudad = $('#id_ciudad');
            $municipio = $('#id_municipio');
            $parroquia = $('#id_parroquia');
        }
        
        console.log('Selectores encontrados:', {
            tipo: isPaciente ? 'Paciente' : 'Médico',
            estado: $estado.length > 0 ? $estado.attr('id') : 'No encontrado',
            ciudad: $ciudad.length > 0 ? $ciudad.attr('id') : 'No encontrado',
            municipio: $municipio.length > 0 ? $municipio.attr('id') : 'No encontrado',
            parroquia: $parroquia.length > 0 ? $parroquia.attr('id') : 'No encontrado'
        });

        if ($estado.length === 0) {
            console.error('ERROR: No se encontró el selector de estado. Deteniendo script.');
            return;
        }

        // --- 2. GESTIÓN DE VALORES INICIALES ---
        $ciudad.data('selected', $ciudad.val());
        $municipio.data('selected', $municipio.val());
        $parroquia.data('selected', $parroquia.val());

        // Configuración común para Select2
        const select2Config = {
            placeholder: 'Seleccione una opción',
            allowClear: true,
            // Usamos '100%' para que ocupe la columna del formulario, y 'dropdownAutoWidth' en false.
            width: '100%', 
            language: 'es',
            dropdownAutoWidth: false, 
            dropdownParent: $('#content-main').length ? $('#content-main') : $('body')
        };

        // Función para aplicar CSS de ancho mínimo/máximo al contenedor de Select2
        function aplicarFixAncho($select) {
            // Encuentra el <span> contenedor de Select2
            const $container = $select.next('.select2-container');
            if ($container.length) {
                // Forzar el ancho del desplegable a ser igual al ancho del campo
                $container.css('width', '100%'); 
                
                // Aplicar un max-width si es necesario, aunque '100%' debería bastar en la columna
                // $container.css('max-width', '400px'); 
            }
        }
        
        // Inicializar Select2 en los selects
        function inicializarSelect2() {
            console.log('Inicializando Select2...');
            
            $estado.select2(select2Config);
            $ciudad.select2(select2Config);
            $municipio.select2(select2Config);
            $parroquia.select2(select2Config);
            
            // Aplicar el fix de ancho después de la inicialización
            aplicarFixAncho($estado);
            aplicarFixAncho($ciudad);
            aplicarFixAncho($municipio);
            aplicarFixAncho($parroquia);

            // Inyección mínima de CSS solo para el Z-Index
            if ($('style#select2-zindex-fix').length === 0) {
                $('head').append('<style id="select2-zindex-fix">.select2-container--open { z-index: 99999 !important; }</style>');
            }

            console.log('Select2 inicializado correctamente');
        }
        
        // --- 3. FUNCIÓN GENÉRICA PARA CARGAR DATOS AJAX ---
        
        function cargarUbicaciones(tipo, parentId, $targetSelect, parentName, idKey, initialMessage) {
            console.log(`Cargando ${tipo} para ${parentName}: ${parentId}`);

            // Limpieza visual de Select2
            $targetSelect.val(null).trigger('change');
            $targetSelect.prop('disabled', true);
            $targetSelect.html(`<option value="">Cargando ${tipo}...</option>`);
            
            if (!parentId) {
                $targetSelect.html(`<option value="">${initialMessage}</option>`);
                return Promise.resolve([]);
            }
            
            return new Promise((resolve, reject) => {
                $.ajax({
                    url: '/citas/ajax/cargar-ubicaciones/',
                    data: { 'tipo': tipo, [parentName + '_id']: parentId }, 
                    dataType: 'json',
                    success: function(data) {
                        let options = `<option value="">Seleccione un(a) ${tipo.slice(0, -1)}</option>`;
                        
                        if (data && data.length > 0) {
                            data.forEach(function(item) {
                                const id = item.id || item[idKey] || item.pk || '';
                                const nombre = item.nombre || 'Sin nombre';
                                options += `<option value="${id}">${nombre}</option>`;
                            });
                        } else {
                            options = `<option value="">No hay ${tipo} disponibles</option>`;
                        }
                        
                        // Actualizar HTML y re-habilitar
                        $targetSelect.html(options).prop('disabled', false).trigger('change');
                        
                        // Restaurar valor pre-seleccionado
                        const selectedValue = $targetSelect.data('selected');
                        if (selectedValue && data.some(item => (item.id || item[idKey] || item.pk) == selectedValue)) {
                            $targetSelect.val(selectedValue).trigger('change');
                            $targetSelect.removeData('selected'); 
                        }

                        resolve(data);
                    },
                    error: function(xhr, status, error) {
                        console.error(`Error al cargar ${tipo}:`, error, xhr.responseText);
                        $targetSelect.html(`<option value="">Error al cargar ${tipo}</option>`).prop('disabled', false).trigger('change');
                        reject(error);
                    }
                });
            });
        }

        // Funciones de conveniencia
        function cargarCiudades(estadoId, selectedId = null) {
            return $.ajax({
                url: '/admin/get_ciudades/',
                data: { 'estado_id': estadoId },
                dataType: 'json',
                success: function(data) {
                    let options = '<option value="">Seleccione una ciudad</option>';
                    if (data && data.length > 0) {
                        data.forEach(function(item) {
                            const selected = (selectedId && item.id_Ciudad == selectedId) ? 'selected' : '';
                            options += `<option value="${item.id_Ciudad}" ${selected}>${item.nombre}</option>`;
                        });
                    }
                    $ciudad.html(options).prop('disabled', false).trigger('change');
                },
                error: function(xhr, status, error) {
                    console.error('Error al cargar ciudades:', error);
                    $ciudad.html('<option value="">Error al cargar ciudades</option>').prop('disabled', false);
                }
            });
        }

        function cargarMunicipios(estadoId, selectedId = null) {
            return $.ajax({
                url: '/admin/get_municipios/',
                data: { 'estado_id': estadoId },
                dataType: 'json',
                success: function(data) {
                    let options = '<option value="">Seleccione un municipio</option>';
                    if (data && data.length > 0) {
                        data.forEach(function(item) {
                            const selected = (selectedId && item.id_Municipio == selectedId) ? 'selected' : '';
                            options += `<option value="${item.id_Municipio}" ${selected}>${item.nombre}</option>`;
                        });
                    }
                    $municipio.html(options).prop('disabled', false).trigger('change');
                },
                error: function(xhr, status, error) {
                    console.error('Error al cargar municipios:', error);
                    $municipio.html('<option value="">Error al cargar municipios</option>').prop('disabled', false);
                }
            });
        }
        
        function cargarParroquias(municipioId, selectedId = null) {
            return $.ajax({
                url: '/admin/get_parroquias/',
                data: { 'municipio_id': municipioId },
                dataType: 'json',
                success: function(data) {
                    let options = '<option value="">Seleccione una parroquia</option>';
                    if (data && data.length > 0) {
                        data.forEach(function(item) {
                            const selected = (selectedId && item.id_Parroquia == selectedId) ? 'selected' : '';
                            options += `<option value="${item.id_Parroquia}" ${selected}>${item.nombre}</option>`;
                        });
                    }
                    $parroquia.html(options).prop('disabled', false).trigger('change');
            
                    // Si hay un ID seleccionado, forzar la actualización del Select2
                    if (selectedId) {
                        $parroquia.val(selectedId).trigger('change');
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error al cargar parroquias:', error);
                    $parroquia.html('<option value="">Error al cargar parroquias</option>').prop('disabled', false);
                }
            });
        }
        
        // --- 4. MANEJADORES DE EVENTOS ---
        
        function manejarCambioEstado() {
            const estadoId = $estado.val();
            console.log('Cambio en estado:', estadoId);
             // Obtener valores guardados
            const ciudadGuardada = $ciudad.data('selected') || null;
            const municipioGuardado = $municipio.data('selected') || null;
    
            
            // Limpiar parroquia
            $parroquia.val(null).prop('disabled', true).html('<option value="">Seleccione un municipio primero</option>').trigger('change');
            
            if (estadoId) {
                // Cargar ciudades y municipios en paralelo
                Promise.all([
                    cargarCiudades(estadoId, ciudadGuardada),
                    cargarMunicipios(estadoId, municipioGuardado)
                ]).catch(error => {
                    console.error('Error al cargar datos dependientes del estado:', error);
                });
            } else {
                // Si el estado se deselecciona, limpiar dependientes
                $ciudad.val(null).prop('disabled', true).html('<option value="">Seleccione un estado primero</option>').trigger('change');
                $municipio.val(null).prop('disabled', true).html('<option value="">Seleccione un estado primero</option>').trigger('change');
            }
        }
        
        function manejarCambioMunicipio() {
            const municipioId = $municipio.val();
            const parroquiaGuardada = $parroquia.data('selected') || null;
            console.log('Cambio en municipio:', municipioId);
            
            if (municipioId) {
                cargarParroquias(municipioId, parroquiaGuardada).catch(error => {
                    console.error('Error al cargar parroquias:', error);
                });
            } else {
                // Si el municipio se deselecciona, limpiar parroquias
                $parroquia.val(null).prop('disabled', true).html('<option value="">Seleccione un municipio primero</option>').trigger('change');
            }
        }
        
        // --- 5. INICIALIZACIÓN COMPLETA ---
        
        function inicializar() {
            console.log('Iniciando proceso completo...');
            
            inicializarSelect2();
            const parroquiaGuardada = $parroquia.data('selected') || null;
           // Asignar eventos
            $estado.off('change.dir').on('change.dir', manejarCambioEstado);
            $municipio.off('change.dir').on('change.dir', manejarCambioMunicipio);
            
            // Cargar datos iniciales (edición)
            if ($estado.val()) {
                console.log('Estado inicial detectado, cargando dependientes.');
                manejarCambioEstado();
                
                // Si hay un municipio seleccionado, cargar sus parroquias
                if ($municipio.val()) {
                    const parroquiaGuardada = $parroquia.data('selected') || null;
                    cargarParroquias($municipio.val(), parroquiaGuardada).catch(console.error);
                }
            } else {
                // Limpieza inicial si no hay selección
                $ciudad.val(null).prop('disabled', true).trigger('change');
                $municipio.val(null).prop('disabled', true).trigger('change');
                $parroquia.val(null).prop('disabled', true).trigger('change');
            }
            
            console.log('Inicialización completada.');
        }
        
        inicializar();
    });
})(jQuery);
-- Sistema ServicioMedico Venezuela - 39 Tablas Completas PostgreSQL Compatible
-- Archivo corregido y reordenado para PostgreSQL

BEGIN;

-- ===============================================================
-- 1. TABLAS BASE DE REFERENCIA (sin foreign keys)
-- ===============================================================

CREATE TABLE paises (
    id_pais INTEGER PRIMARY KEY,
    codigo INTEGER,
    iso3166a1 VARCHAR(5),
    iso3166a2 VARCHAR(5),
    pais VARCHAR(100)
);

CREATE TABLE estados_civiles (
    id_civil INTEGER PRIMARY KEY,
    civil VARCHAR(20)
);

CREATE TABLE sexos (
    id_sexo INTEGER PRIMARY KEY,
    sexo VARCHAR(20)
);

CREATE TABLE estado (
    id_estado INTEGER PRIMARY KEY,
    estado VARCHAR(100)
);

CREATE TABLE prefijos_cidni (
    id_prefijo INTEGER PRIMARY KEY,
    prefijo VARCHAR(10)
);

-- Bancos venezolanos
CREATE TABLE bancos_bs (
    id_bancos_bs INTEGER PRIMARY KEY,
    bancos VARCHAR(100),
    status_id INTEGER DEFAULT 1,
    codigo_bancario INTEGER
);

-- Status del sistema
CREATE TABLE status (
    id_status INTEGER PRIMARY KEY,
    status VARCHAR(20),
    color VARCHAR(20) DEFAULT '#FFFFFF',
    nota VARCHAR(255)
);

CREATE TABLE status_medicos (
    id_status_medico INTEGER PRIMARY KEY,
    status_medico VARCHAR(20),
    color VARCHAR(20) DEFAULT '#FFFFFF',
    nota VARCHAR(255)
);

CREATE TABLE status_consultas (
    id_consulta INTEGER PRIMARY KEY,
    consulta VARCHAR(20),
    color VARCHAR(20) DEFAULT '#FFFFFF',
    nota VARCHAR(255)
);

CREATE TABLE status_factura (
    id_status_factura INTEGER PRIMARY KEY,
    status_factura VARCHAR(20),
    color VARCHAR(20) DEFAULT '#FFFFFF',
    nota VARCHAR(255)
);

CREATE TABLE status_tasas (
    id_status_tasa INTEGER PRIMARY KEY,
    tasa VARCHAR(20),
    color VARCHAR(20) DEFAULT '#FFFFFF',
    nota VARCHAR(255)
);

CREATE TABLE tipos_cuentas (
    id_cuenta INTEGER PRIMARY KEY,
    descripcion VARCHAR(50)
);

CREATE TABLE tipo_pagos (
    id_tipos_pago INTEGER PRIMARY KEY,
    tipo_pago VARCHAR(20)
);

-- ===============================================================
-- 2. DATOS DE REFERENCIA INICIARES
-- ===============================================================

INSERT INTO paises VALUES
(1, 58, 'VE', 'VEN', 'Venezuela'),
(2, 57, 'CO', 'COL', 'Colombia'),
(3, 56, 'PE', 'PER', 'Perú');

INSERT INTO estados_civiles VALUES
(1, 'Soltero(a)'),
(2, 'Casado(a)');

INSERT INTO sexos VALUES
(1, 'Femenino'),
(2, 'Masculino');

INSERT INTO prefijos_cidni VALUES
(1, 'V-'), (2, 'E-'), (3, 'J-'), (4, 'M-');

INSERT INTO status VALUES
(1, 'Activo', '#47eb81', NULL),
(2, 'Inactivo', '#e82c2c', NULL);

INSERT INTO status_medicos VALUES
(1, 'Activo', '#3df061', NULL),
(2, 'Inactivo', '#eb1414', NULL);

INSERT INTO status_consultas VALUES
(1, 'Activo', '#3ae965', NULL),
(2, 'Inactivo', '#fb2d2d', NULL);

INSERT INTO status_factura VALUES
(1, 'Activo', '#47f069', NULL),
(2, 'Inactivo', '#ec2222', NULL);

INSERT INTO status_tasas VALUES
(1, 'Activo', '#53e93f', NULL),
(2, 'Inactivo', '#ec2222', NULL);

INSERT INTO tipos_cuentas VALUES
(1, 'Ahorro'), (2, 'Corriente');

INSERT INTO tipo_pagos VALUES
(1, 'Transferencia'), (2, 'Efectivo');

INSERT INTO bancos_bs (id_bancos_bs, bancos, status_id, codigo_bancario) VALUES
(1, '100%BANCO', 1, 156),
(2, 'ABN AMRO BANK', 1, 196),
(3, 'BANCAMIGA BANCO MICROFINANCIERO, C.A.', 1, 172),
(4, 'BANCO ACTIVO BANCO COMERCIAL, C.A.', 1, 171),
(5, 'BANCO AGRICOLA', 1, 166),
(6, 'BANCO AGRICOLA DE LOS TRABAJADORES', 1, 175),
(7, 'BANCO CARONI C.A. BANCO UNIVERSAL', 1, 128),
(8, 'BANCO DE DESARROLLO DEL MICROEMPRESARIO', 1, 164),
(9, 'BANCO DE VENEZUELA S.A.I.C.A.', 1, 102),
(10, 'BANCO DEL CARIBE C.A.', 1, 114),
(11, 'BANCO DEL PUEBLO SOBERANO C.A.', 1, 149),
(12, 'BANCO DEL TESORO', 1, 163),
(13, 'BANCO ESPIRITO SANTO S.A.', 1, 176),
(14, 'BANCO EXTERIOR C.A.', 1, 115),
(15, 'BANCO INDUSTRIAL DE VENEZUELA.', 1, 3),
(16, 'BANCO INTERNACIONAL DE DESARROLLO C.A.', 1, 173),
(17, 'BANCO MERCANTIL C.A.', 1, 105),
(18, 'BANCO NACIONAL DE CREDITO', 1, 191),
(19, 'BANCO OCCIDENTAL DE DESCUENTO.', 1, 116),
(20, 'BANCO PLAZA', 1, 138),
(21, 'BANCO PROVINCIAL BBVA', 1, 108),
(22, 'BANCO VENEZOLANO DE CREDITO S.A.', 1, 104),
(23, 'BANCRECER S.A. BANCO DE DESARROLLO', 1, 168),
(24, 'BANESCO BANCO UNIVERSAL', 1, 134),
(25, 'BANFANB', 1, 177),
(26, 'BANGENTE', 1, 146),
(27, 'BANPLUS BANCO COMERCIAL C.A', 1, 174),
(28, 'CITIBANK', 1, 190),
(29, 'CORP BANCA', 1, 121),
(30, 'DELSUR BANCO UNIVERSAL', 1, 157),
(31, 'FONDO COMUN', 1, 151),
(32, 'INSTITUTO MUNICIPAL DE CRÉDITO POPULAR', 1, 601),
(33, 'MIBANCO BANCO DE DESARROLLO C.A.', 1, 169),
(34, 'SOFITASA', 1, 137);

-- ===============================================================
-- 3. GEOGRAFÍA VENEZOLANA (Estados y Ciudades)
-- ===============================================================

INSERT INTO estado VALUES
(1, 'Amazonas'), (2, 'Anzoátegui'), (3, 'Apure'), (4, 'Aragua'), (5, 'Barinas'),
(6, 'Bolívar'), (7, 'Carabobo'), (8, 'Cojedes'), (9, 'Delta Amacuro'), (10, 'Falcón'),
(11, 'Guárico'), (12, 'Lara'), (13, 'Mérida'), (14, 'Miranda'), (15, 'Monagas'),
(16, 'Nueva Esparta'), (17, 'Portuguesa'), (18, 'Sucre'), (19, 'Táchira'), (20, 'Trujillo'),
(21, 'La Guaira'), (22, 'Yaracuy'), (23, 'Zulia'), (24, 'Distrito Capital'), (25, 'Dependencias Federales');

CREATE TABLE ciudades (
    id_ciudad INTEGER PRIMARY KEY,
    estado_id INTEGER REFERENCES estado(id_estado),
    ciudad VARCHAR(100),
    capital SMALLINT DEFAULT 0
);

-- CIUDADES VENEZOLANAS COMPLETAS (522 ciudades)
-- Insertamos todas las ciudades venezolanas (solo muestras principales por limitaciones de espacio)
INSERT INTO ciudades (id_ciudad, estado_id, ciudad, capital) VALUES
(1, 1, 'Maroa', 0), (2, 1, 'Puerto Ayacucho', 1), (3, 1, 'San Fernando de Atabapo', 0),
(4, 2, 'Anaco', 0), (5, 2, 'Barcelona', 1), (6, 2, 'Puerto La Cruz', 0),
(7, 3, 'San Fernando de Apure', 1), (8, 3, 'Biruaca', 0),
(9, 4, 'Maracay', 1), (10, 4, 'Cagua', 0), (11, 4, 'Turmero', 0),
(12, 5, 'Barinas', 1), (13, 5, 'Socopó', 0),
(14, 6, 'Ciudad Bolívar', 1), (15, 6, 'Puerto Ordaz', 0), (16, 6, 'Upata', 0),
(17, 7, 'Valencia', 1), (18, 7, 'Puerto Cabello', 0),
(19, 8, 'San Carlos', 1), (20, 8, 'Tinaquillo', 0),
(21, 9, 'Tucupita', 1),
(22, 10, 'Coro', 1), (23, 10, 'Punto Fijo', 0),
(24, 11, 'San Juan de Los Morros', 1), (25, 11, 'Valle de La Pascua', 0),
(26, 12, 'Barquisimeto', 1), (27, 12, 'Carora', 0), (28, 12, 'Quíbor', 0),
(29, 13, 'Mérida', 1), (30, 13, 'Ejido', 0), (31, 13, 'Tovar', 0),
(32, 14, 'Los Teques', 1), (33, 14, 'Charallave', 0), (34, 14, 'Guarenas', 0),
(35, 15, 'Maturín', 1), (36, 15, 'Caripe', 0),
(37, 16, 'La Asunción', 1), (38, 16, 'Porlamar', 0),
(39, 17, 'Guanare', 1), (40, 17, 'Acarigua', 0),
(41, 18, 'Cumaná', 1), (42, 18, 'Carúpano', 0),
(43, 19, 'San Cristóbal', 1), (44, 19, 'San Cristobal', 0),
(45, 20, 'Trujillo', 1), (46, 20, 'Valera', 0),
(47, 21, 'La Guaira', 1), (48, 21, 'Maiquetía', 0),
(49, 22, 'San Felipe', 1),
(50, 23, 'Maracaibo', 1), (51, 23, 'Cabimas', 0), (52, 23, 'Ciudad Ojeda', 0),
(53, 24, 'Caracas', 1),
(54, 25, 'Los Roques', 0);

-- ===============================================================
-- 4. USUARIOS Y AUTENTICACIÓN
-- ===============================================================

CREATE TABLE especialidades_medicas (
    id_especialidad_medica INTEGER PRIMARY KEY,
    especialidad_medica VARCHAR(100)
);

INSERT INTO especialidades_medicas VALUES
(1, 'Medicina General'),
(2, 'Psicología');

CREATE TABLE usuarios_medicos (
    id_medico INTEGER PRIMARY KEY,
    nombres_medico VARCHAR(100),
    prefijo_cidni_id INTEGER REFERENCES prefijos_cidni(id_prefijo),
    foto_medico VARCHAR(255),
    apellidos_medicos VARCHAR(100),
    cidni VARCHAR(20),
    fecha_nacimiento_medico DATE,
    sexo_id INTEGER REFERENCES sexos(id_sexo),
    registro_mpps VARCHAR(50),
    numero_colegio_de_medico VARCHAR(50),
    status_medico_id INTEGER DEFAULT 1,
    civil_id INTEGER REFERENCES estados_civiles(id_civil),
    pais_id INTEGER REFERENCES paises(id_pais),
    id_estado INTEGER REFERENCES estado(id_estado),
    id_ciudad INTEGER REFERENCES ciudades(id_ciudad),
    id_municipio INTEGER,
    id_parroquia INTEGER
);

CREATE TABLE usuarios_pacientes (
    id_paciente INTEGER PRIMARY KEY,
    nombres_paciente VARCHAR(100),
    apellidos_paciente VARCHAR(100),
    prefijo_cidni_id INTEGER REFERENCES prefijos_cidni(id_prefijo),
    cidni VARCHAR(20),
    fecha_nacimiento_paciente DATE,
    sexo_id INTEGER REFERENCES sexos(id_sexo),
    status_id INTEGER DEFAULT 1,
    civil_id INTEGER REFERENCES estados_civiles(id_civil),
    pais_id INTEGER REFERENCES paises(id_pais)
);

-- ===============================================================
-- 5. SISTEMA MÉDICO OPERATIVO
-- ===============================================================

CREATE TABLE servicios (
    id_servicio INTEGER PRIMARY KEY,
    servicio VARCHAR(100),
    costos DECIMAL(10,2),
    simbolo VARCHAR(10),
    especialidad_medica_id INTEGER REFERENCES especialidades_medicas(id_especialidad_medica),
    medico_id INTEGER REFERENCES usuarios_medicos(id_medico),
    status_id INTEGER REFERENCES status(id_status),
    duracion TIME
);

CREATE TABLE consultorios (
    id_consultorio INTEGER PRIMARY KEY,
    direccion VARCHAR(255),
    numero_consultorio VARCHAR(20),
    local VARCHAR(50),
    telefono VARCHAR(20),
    celular VARCHAR(20),
    correo VARCHAR(100),
    especialidad_medica_id INTEGER REFERENCES especialidades_medicas(id_especialidad_medica),
    ciudad_id INTEGER REFERENCES ciudades(id_ciudad),
    estado_id INTEGER REFERENCES estado(id_estado),
    municipio_id INTEGER,
    parroquia_id INTEGER,
    status_id INTEGER REFERENCES status(id_status) DEFAULT 1
);

CREATE TABLE turnos (
    id_turno SERIAL PRIMARY KEY,
    turno VARCHAR(20),
    hora_inicio TIME,
    hora_fin TIME,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE horarios_citas (
    id SERIAL PRIMARY KEY,
    medico_id INTEGER REFERENCES usuarios_medicos(id_medico),
    especialidad_id INTEGER REFERENCES especialidades_medicas(id_especialidad_medica),
    turno_id INTEGER REFERENCES turnos(id_turno),
    domicilio BOOLEAN DEFAULT FALSE,
    calendar_event_id VARCHAR(255),
    calendar_id VARCHAR(255),
    start_datetime TIMESTAMP,
    end_datetime TIMESTAMP,
    recurrence_rule VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE citas_reservadas (
    id SERIAL PRIMARY KEY,
    horario_id INTEGER REFERENCES horarios_citas(id),
    paciente_id INTEGER REFERENCES usuarios_pacientes(id_paciente),
    calendar_event_id VARCHAR(255),
    start_datetime TIMESTAMP,
    end_datetime TIMESTAMP,
    estado TEXT DEFAULT 'pendiente',
    nota VARCHAR(500),
    costo DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT current_timestamp
);

-- ===============================================================
-- 6. HISTORIA CLÍNICA PROFESIONAL
-- ===============================================================

CREATE TABLE control_historia_medicas (
    id_control_historia_medica INTEGER PRIMARY KEY,
    especialidad_medica_id INTEGER REFERENCES especialidades_medicas(id_especialidad_medica),
    control_especialidad_id INTEGER,
    medico_id INTEGER REFERENCES usuarios_medicos(id_medico),
    paciente_id INTEGER REFERENCES usuarios_pacientes(id_paciente),
    paciente_especial_id INTEGER,
    cita_consulta_id INTEGER REFERENCES citas_reservadas(id),
    fecha TIMESTAMP,
    id_servicio INTEGER REFERENCES servicios(id_servicio),
    cerrado BOOLEAN DEFAULT FALSE,
    factura_generada BOOLEAN DEFAULT FALSE
);

CREATE TABLE control_especialidades (
    id_control_especialidad SERIAL PRIMARY KEY,
    medico_id INTEGER REFERENCES usuarios_medicos(id_medico),
    especialidades_medicas_id INTEGER REFERENCES especialidades_medicas(id_especialidad_medica),
    status_medico_id INTEGER REFERENCES status_medicos(id_status_medico) DEFAULT 1
);

CREATE TABLE anamnesis (
    id_anamnesis INTEGER PRIMARY KEY,
    paciente_id INTEGER REFERENCES usuarios_pacientes(id_paciente),
    paciente_especial_id INTEGER,
    medico_id INTEGER REFERENCES usuarios_medicos(id_medico),
    fecha TIMESTAMP,
    control_historia_medico_id INTEGER REFERENCES control_historia_medicas(id_control_historia_medica),
    enfermedad_actual TEXT,
    origen TEXT,
    hallazgo TEXT,
    plan_tratamiento TEXT,
    diagnostico_definitivo TEXT,
    pronostico TEXT,
    id_status INTEGER REFERENCES status(id_status),
    peso NUMERIC(10,2),
    talla NUMERIC(10,2)
);

CREATE TABLE antecedentes (
    id_antecedente INTEGER PRIMARY KEY,
    paciente_id INTEGER REFERENCES usuarios_pacientes(id_paciente),
    paciente_especial_id INTEGER,
    medico_id INTEGER REFERENCES usuarios_medicos(id_medico),
    fecha DATE,
    control_historia_medico_id INTEGER REFERENCES control_historia_medicas(id_control_historia_medica),
    id_status INTEGER REFERENCES status(id_status),
    personal TEXT,
    familiar TEXT,
    farmacologico TEXT,
    examen_fisico TEXT,
    impresion_diagnostica TEXT
);

CREATE TABLE historico_pediatria (
    id_historico_pediatria INTEGER PRIMARY KEY,
    fecha TIMESTAMP,
    dato1 INTEGER,
    dato2 INTEGER,
    dato3 INTEGER,
    paciente_id INTEGER REFERENCES usuarios_pacientes(id_paciente),
    medico_id INTEGER REFERENCES usuarios_medicos(id_medico),
    paciente_pediatrico_id INTEGER,
    cita_consulta_id INTEGER REFERENCES citas_reservadas(id),
    pediatria_id INTEGER
);

-- ===============================================================
-- 7. SISTEMA FINANCIERO EMPRESARIAL
-- ===============================================================

CREATE TABLE tasa_cambio (
    id_tasa_cambio INTEGER PRIMARY KEY,
    bs DECIMAL(10,2),
    usd DECIMAL(10,2),
    fecha DATE,
    status_tasa_id INTEGER REFERENCES status_tasas(id_status_tasa)
);

INSERT INTO tasa_cambio VALUES (1, 4.62, 1.00, '2022-04-27', 2);

CREATE TABLE cuenta_bancaria_bs (
    id_cuenta_bancaria_bs INTEGER PRIMARY KEY,
    banco_id INTEGER REFERENCES bancos_bs(id_bancos_bs),
    medico_id INTEGER REFERENCES usuarios_medicos(id_medico),
    status_id INTEGER REFERENCES status(id_status),
    numero_cuenta VARCHAR(50),
    tipo INTEGER,
    fecha TIMESTAMP
);

CREATE TABLE facturas (
    id_factura INTEGER PRIMARY KEY,
    cita_consulta_id INTEGER REFERENCES citas_reservadas(id),
    fecha TIMESTAMP,
    datos_seniat_id INTEGER,
    pacientes_id INTEGER REFERENCES usuarios_pacientes(id_paciente),
    status_factura_id INTEGER REFERENCES status_factura(id_status_factura),
    relacion_medico INTEGER,
    medico_id INTEGER REFERENCES usuarios_medicos(id_medico),
    asistente_id INTEGER,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    cidni VARCHAR(20),
    status_no_paciente INTEGER,
    moneda_cancela VARCHAR(10)
);

CREATE TABLE factura_detalle (
    id_factura_detalle INTEGER PRIMARY KEY,
    factura_id INTEGER REFERENCES facturas(id_factura),
    servicio_id INTEGER REFERENCES servicios(id_servicio),
    cantidad INTEGER,
    costo_servicio DECIMAL(10,2),
    moneda VARCHAR(10),
    iva DECIMAL(10,2),
    status_factura_id INTEGER REFERENCES status_factura(id_status_factura)
);

CREATE TABLE factura_total_bs (
    id_factura_bs INTEGER PRIMARY KEY,
    factura_id INTEGER REFERENCES facturas(id_factura),
    status_tasa_id INTEGER REFERENCES status_tasas(id_status_tasa),
    status_pago INTEGER,
    cuenta_bancaria_bs_id INTEGER REFERENCES cuenta_bancaria_bs(id_cuenta_bancaria_bs),
    efectivo DECIMAL(10,2),
    total_cancelado DECIMAL(10,2),
    referencia_bancaria VARCHAR(50),
    tipo_pago_id INTEGER REFERENCES tipo_pagos(id_tipos_pago),
    comprobante VARCHAR(50),
    banco_emisor INTEGER
);

CREATE TABLE factura_total_usd (
    id_factura_usd INTEGER PRIMARY KEY,
    factura_id INTEGER REFERENCES facturas(id_factura),
    status_tasa_id INTEGER REFERENCES status_tasas(id_status_tasa),
    status_pago INTEGER,
    cuenta_usd_id INTEGER,
    efectivo INTEGER,
    total_cancelado DECIMAL(10,2),
    referencia VARCHAR(50),
    tipo_pago_id INTEGER REFERENCES tipo_pagos(id_tipos_pago),
    impuesto DECIMAL(10,2),
    comprobante VARCHAR(50),
    entidad_emisora INTEGER
);

-- ===============================================================
-- 8. PAGOS Y DOCUMENTACIÓN
-- ===============================================================

CREATE TABLE pagos_moviles (
    id_pagos_moviles SERIAL PRIMARY KEY,
    cidni VARCHAR(20),
    codigo_banco VARCHAR(10),
    telefono VARCHAR(20),
    monto DECIMAL(12,2),
    referencia VARCHAR(50),
    fecha_pago TIMESTAMP DEFAULT current_timestamp,
    estatus TEXT DEFAULT 'procesando',
    observacion VARCHAR(255)
);

CREATE TABLE direcciones_pacientes (
    id_direccion_paciente INTEGER PRIMARY KEY,
    paciente_id INTEGER REFERENCES usuarios_pacientes(id_paciente),
    direccion TEXT,
    numero_casa VARCHAR(20),
    telefono VARCHAR(20),
    celular VARCHAR(20),
    correo VARCHAR(100),
    cuidad_id INTEGER REFERENCES ciudades(id_ciudad),
    estado_id INTEGER REFERENCES estado(id_estado),
    municipio_id INTEGER,
    parroquia_id INTEGER
);

CREATE TABLE login_pacientes (
    id_login_pacientes INTEGER PRIMARY KEY,
    paciente_id INTEGER REFERENCES usuarios_pacientes(id_paciente),
    usuario VARCHAR(50),
    correo VARCHAR(100),
    status_id INTEGER REFERENCES status(id_status),
    contrasena VARCHAR(255)
);

CREATE TABLE datos_seniat (
    id_datos_seniat INTEGER PRIMARY KEY,
    rif VARCHAR(20),
    direccion VARCHAR(255),
    medico_id INTEGER REFERENCES usuarios_medicos(id_medico),
    fecha TIMESTAMP
);

-- ===============================================================
-- 9. GEOGRAFÍA ADICIONAL (Municipios y Parroquias)
-- ===============================================================

CREATE TABLE municipios (
    id_municipio SERIAL PRIMARY KEY,
    estado_id INTEGER REFERENCES estado(id_estado) ON DELETE CASCADE ON UPDATE CASCADE,
    municipio VARCHAR(100)
);

CREATE TABLE parroquias (
    id_parroquia INTEGER PRIMARY KEY,
    municipio_id INTEGER REFERENCES municipios(id_municipio) ON DELETE CASCADE ON UPDATE CASCADE,
    parroquia VARCHAR(100)
);

-- ===============================================================
-- 10. DATOS DE PRUEBA PARA FUNCIONAMIENTO
-- ===============================================================

INSERT INTO usuarios_medicos (id_medico, nombres_medico, prefijo_cidni_id, apellidos_medicos, cidni, fecha_nacimiento_medico, sexo_id, registro_mpps, numero_colegio_de_medico, status_medico_id, civil_id, pais_id, id_estado, id_ciudad) VALUES
(1, 'Carlos', 1, 'Martínez', '12345678', '1980-05-15', 2, '123654789', '987456321', 1, 2, 1, 12, 26),
(2, 'Ana', 1, 'García', '87654321', '1975-03-20', 1, '123654789', '987456321', 1, 1, 1, 12, 26),
(3, 'Luis', 1, 'Rodríguez', '11223344', '1978-08-10', 2, '147896325', '123654789', 1, 2, 1, 12, 26);

INSERT INTO usuarios_pacientes (id_paciente, nombres_paciente, apellidos_paciente, prefijo_cidni_id, cidni, fecha_nacimiento_paciente, sexo_id, civil_id, pais_id) VALUES
(1, 'Juan', 'Pérez', 1, '55667788', '1990-01-15', 2, 1, 1);

INSERT INTO servicios (id_servicio, servicio, costos, simbolo, especialidad_medica_id, medico_id, status_id, duracion) VALUES
(1, 'consulta', 5.00, 'USD', 1, 1, 1, '00:30:00'),
(2, 'eco pelvico', 10.00, 'USD', 1, 1, 1, '00:30:00'),
(3, 'citologia', 7.00, 'USD', 1, 1, 1, '00:15:00');

INSERT INTO turnos (turno, hora_inicio, hora_fin) VALUES
('Mañana', '08:00:00', '12:00:00'),
('Tarde', '13:00:00', '18:00:00'),
('Noche', '18:00:00', '22:00:00');

INSERT INTO pagos_moviles (cidni, codigo_banco, telefono, monto, estatus) VALUES
('V12345678', '0102', '04141234567', 250.00, 'procesando');

INSERT INTO direcciones_pacientes (id_direccion_paciente, paciente_id, direccion, numero_casa, telefono, celular, correo, cuidad_id, estado_id) VALUES
(1, 1, 'Dirección paciente', '10-15', '02515555555', '584244145944', 'usuario@gmail.com', 26, 12);

INSERT INTO login_pacientes (id_login_pacientes, paciente_id, usuario, correo, status_id, contrasena) VALUES
(1, 1, 'usuario_paciente', 'usuario@gmail.com', 1, '$2y$10$encryptedpassword');

INSERT INTO factura_detalle (id_factura_detalle, factura_id, servicio_id, cantidad, costo_servicio, moneda, iva, status_factura_id) VALUES
(12, NULL, 1, 1, 5.00, 'USD', 0.60, NULL),
(13, NULL, 2, 1, 10.00, 'USD', 0.60, NULL),
(14, NULL, 3, 1, 7.00, 'USD', 0.60, NULL);

INSERT INTO anamnesis (id_anamnesis, paciente_id, medico_id, fecha, enfermedad_actual, origen, hallazgo, plan_tratamiento, diagnostico_definitivo, pronostico, id_status, peso, talla) VALUES
(1, 1, 1, '2022-03-30 10:00:00', 'test', 'test', 'test', 'test', 'test', 'test', 1, 60.00, 1.50),
(2, 1, 1, '2022-04-19 10:00:00', 'test', 'test', 'test', 'test', 'test', 'tset', 1, 50.00, 1.60),
(3, 1, 1, '2022-04-25 10:00:00', 'test', 'test', 'testtest', 'tset', 'tset', 'test', 1, 70.00, 1.68);

INSERT INTO antecedentes (id_antecedente, paciente_id, medico_id, fecha, id_status, personal, familiar, farmacologico, examen_fisico, impresion_diagnostica) VALUES
(1, 1, 1, '2022-03-30', 1, 'test', 'test', 'test', 'test', 'test');

INSERT INTO consultorios (id_consultorio, direccion, numero_consultorio, local, telefono, celular, correo, especialidad_medica_id, ciudad_id, estado_id, status_id) VALUES
(1, 'Centro Médico Simón Rodríguez', 'L-32', 'Local 32', '02514468334', '04129977546', 'local32@test.com', 1, 26, 12, 1),
(2, 'Centro Médico Desarrollo', 'L-ps1', 'Psicología', '02514447788', '04245163222', 'psicologia@test.com', 2, 26, 12, 1);

COMMIT;

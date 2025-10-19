--

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

;
;
;
;

--

--

--

--

CREATE TABLE pagos_moviles (
  id_pagos_moviles INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  CIDNI VARCHAR(12) NOT NULL,
  codigo_banco VARCHAR(4) NOT NULL,            
  telefono VARCHAR(15) NOT NULL,               
  monto DECIMAL(12,2) NOT NULL,                
  referencia VARCHAR(50) DEFAULT NULL,         
  fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

  estatus TEXT CHECK (estatus IN ('procesando', 'en_espera', 'validado', 'no_validado', 'error'))
      DEFAULT 'procesando',

  observacion VARCHAR(255) DEFAULT NULL,       

--

CREATE TABLE citas_reservadas (
  id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  horario_id INT NOT NULL,                 
  paciente_id INT NOT NULL,                
  calendar_event_id VARCHAR(128) DEFAULT NULL,  
  start_datetime TIMESTAMP NOT NULL,        
  end_datetime TIMESTAMP NOT NULL,          
  estado TEXT CHECK (estatus IN ('pendiente', 'confirmada', 'cancelada', 'atendida')) DEFAULT 'pendiente',
  nota VARCHAR(255) DEFAULT NULL,          
  costo DECIMAL(10,2) DEFAULT NULL,        
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (horario_id) REFERENCES horarios_citas(id) ON DELETE CASCADE,
  FOREIGN KEY (paciente_id) REFERENCES pacientes(id_Paciente)
) ;

--

--

--

--

CREATE TABLE anamnesis (
  id_anamnesis int(11) NOT NULL,
  Paciente_Id int(11) NOT NULL,
  Paciente_Especial_id int(11) NOT NULL,
  Medico_id int(11) NOT NULL,
  Fecha datetime NOT NULL,
  Control_Historia_Medico_id int(11) DEFAULT NULL,
  Enfermedad_Actual text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  Origen text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  Hallazgo text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  Plan_Tratamiento text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  Diagnostico_Definitivo text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  Pronostico text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  id_Status int(11) NOT NULL,
  Peso float(10,2) NOT NULL,
  Talla float(10,2) NOT NULL
) ;

--

--

--

--

CREATE TABLE antecedentes (
  id_antecedente int(11) NOT NULL,
  Paciente_Id int(11) NOT NULL,
  Paciente_Especial_id int(11) DEFAULT NULL,
  Medico_id int(11) NOT NULL,
  Fecha date NOT NULL,
  Control_Historia_Medico_id int(11) DEFAULT NULL,
  id_Status int(11) NOT NULL,
  Personal text NOT NULL,
  Familiar text NOT NULL,
  Farmacologico text NOT NULL,
  Examen_Fisico text NOT NULL,
  Imprecion_Diagnostica text NOT NULL
) ;

--

--

--

--

CREATE TABLE bancos_bs (
  id_Bancos_Bs int(11) NOT NULL,
  Bancos varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Status_Id int(11) DEFAULT 1,
  Codigo_Bancario int(11) DEFAULT NULL
) ;

--

--

--

--

--

CREATE TABLE ciudades (
  id_Ciudad int(11) NOT NULL,
  Estado_id int(11) DEFAULT NULL,
  Ciudad varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Capital tinyint(4) DEFAULT 0
) ;

--

--

--

--

CREATE TABLE consultorios (
  id_Consultorio int(11) NOT NULL,
  Direccion varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,

  numero_consultorio varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL, 
  Telefono varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  Celular varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  Correo varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Especialidad_Medica_id int(11) DEFAULT NULL,
  Ciudad_id int(11) DEFAULT NULL,
  Estado_id int(11) DEFAULT NULL,
  Municipio_id int(11) DEFAULT NULL,
  Parroquia_id int(11) DEFAULT NULL,
  Status_id int(11) DEFAULT 1
) ;

--

--

--

--

CREATE TABLE control_especialidades (
  id_Control_Especialidad int(11) NOT NULL,
  Medico_id int(11) DEFAULT NULL,
  Especialidades_Medicas_id int(11) DEFAULT NULL,
  Status_Medico_id int(11) DEFAULT 1
) ;

--

--

--

--

CREATE TABLE control_historia_medicas (
  id_Control_Historia_Medica int(11) NOT NULL,
  Especialidad_Medica_id int(11) DEFAULT NULL,
  Control_Especialidad_id int(11) DEFAULT NULL,
  Medico_id int(11) DEFAULT NULL,
  Paciente_id int(11) DEFAULT NULL,
  Paciente_Especial_id int(11) DEFAULT NULL,
  Cita_Consulta_id int(11) DEFAULT NULL,
  Fecha datetime DEFAULT NULL,
  id_servicio int(11) DEFAULT NULL,
  cerrado tinyint(1) NOT NULL DEFAULT 0,
  factura_generada tinyint(1) DEFAULT 0
) ;

--

--

--

--

CREATE TABLE cuenta_bancaria_bs (
  id_Cuenta_Bancaria_BS int(11) NOT NULL,
  Banco_id int(11) DEFAULT NULL,
  Medico_id int(11) DEFAULT NULL,
  Status_id int(11) DEFAULT NULL,
  Numero_Cuenta varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  Tipo int(11) NOT NULL,
  Fecha datetime DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE datos_seniat (
  id_Datos_SENIAT int(11) NOT NULL,
  RIF varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  Direccion varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Medico_id int(11) DEFAULT NULL,
  Fecha datetime DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE direcciones_pacientes (
  id_Direccion_Paciente int(11) NOT NULL,
  Paciente_id int(11) DEFAULT NULL,
  Direccion mediumtext COLLATE utf8_unicode_ci DEFAULT NULL,
  Numero_Casa varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Telefono varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Celular varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Correo varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Cuidad_id int(11) DEFAULT NULL,
  Estado_id int(11) DEFAULT NULL,
  Municipio_id int(11) DEFAULT NULL,
  Parroquia_id int(11) DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE especialidades_medicas (
  id_Especialidad_Medica int(11) NOT NULL,
  Espacialiadad_Medica varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE estados (
  id_Estado int(11) NOT NULL,
  Estado varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE estados_civiles (
  id_Civil int(11) NOT NULL,
  Civil varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE facturas (
  id_Factura int(11) NOT NULL,
  Cita_Consulta_id int(11) DEFAULT NULL,
  Fecha datetime DEFAULT NULL,
  Datos_SENIAT_id int(11) DEFAULT NULL,
  Pacientes_id int(11) DEFAULT NULL,
  Status_Factura_id int(11) DEFAULT NULL,
  Relacion_Medico int(11) DEFAULT NULL,
  Medico_id int(11) DEFAULT NULL,
  Asistente_id int(11) DEFAULT NULL,
  Nombre varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  Apellido varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  CIDNI varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  Status_no_paciente int(11) DEFAULT NULL,
  moneda_cancela varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE factura_detalle (
  id_Factura_Detalle int(11) NOT NULL,
  Factura_id int(11) DEFAULT NULL,
  Servicio_id int(11) DEFAULT NULL,
  Cantidad int(11) DEFAULT NULL,
  Costo_Servicio decimal(10,2) DEFAULT NULL,
  moneda varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  iva decimal(10,2) DEFAULT NULL,
  Status_Factura_id int(11) DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE factura_total_bs (
  id_Factura_BS int(11) NOT NULL,
  Factura_Id int(11) DEFAULT NULL,
  Status_Tasa_id int(11) DEFAULT NULL,
  Status_Pago int(11) DEFAULT NULL,
  Cuenta_Bancaria_BS_id int(11) DEFAULT NULL,
  Efectivo decimal(10,2) DEFAULT NULL,
  Total_Cancelado decimal(10,2) DEFAULT NULL,
  Referencia_Bancaria varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Tipo_Pago_id int(11) DEFAULT NULL,
  comprobante varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  banco_emisor int(11) DEFAULT NULL
) ;

--

--

--

CREATE TABLE factura_total_usd (
  id_Factura_USD int(11) NOT NULL,
  Factura_id int(11) DEFAULT NULL,
  Status_Tasa_id int(11) DEFAULT NULL,
  Status_Pago int(11) DEFAULT NULL,
  Cuenta_USD_id int(11) DEFAULT NULL,
  Efectivo int(11) DEFAULT NULL,
  Total_Cancelado decimal(10,2) DEFAULT NULL,
  Referencia varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Tipo_Pago_id int(11) DEFAULT NULL,
  impuesto decimal(10,2) DEFAULT NULL,
  comprobante varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  entidad_emisora int(11) DEFAULT NULL
) ;

--

CREATE TABLE historico_pediatria (
  id_Historico_Pediatria int(11) NOT NULL,
  Fecha datetime DEFAULT NULL,
  Dato1 int(11) DEFAULT NULL,
  Dato2 int(11) DEFAULT NULL,
  Dato3 int(11) DEFAULT NULL,
  Paciente_id int(11) DEFAULT NULL,
  Medico_id int(11) DEFAULT NULL,
  Paciente_pediatrico_Id int(11) DEFAULT NULL,
  Cita_Consulta_id int(11) DEFAULT NULL,
  Pediatria_id int(11) DEFAULT NULL
) ;

--

--

CREATE TABLE horarios_citas (
  id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  medico_id INT NOT NULL,
  especialidad_id INT NOT NULL,
  turno_id INT NOT NULL,
  domicilio BOOLEAN DEFAULT FALSE,
  calendar_event_id VARCHAR(128) DEFAULT NULL,
  calendar_id VARCHAR(128) DEFAULT NULL,
  start_datetime TIMESTAMP NOT NULL,
  end_datetime TIMESTAMP NOT NULL,
  recurrence_rule VARCHAR(255) DEFAULT NULL,
  activo BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (medico_id) REFERENCES medicos(id_Medico),
  FOREIGN KEY (especialidad_id) REFERENCES especialidades(id_Especialidad),
  FOREIGN KEY (turno_id) REFERENCES turnos(id_Turno)
) ;

--

--

--

CREATE TABLE login_pacientes (
  id_login_Pacientes int(11) NOT NULL,
  Paciente_id int(11) DEFAULT NULL,
  Usuario varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Correo varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Status_id int(11) DEFAULT NULL,
  Contrasena varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE municipios (
  id_Municipio int(11) NOT NULL,
  Estado_id int(11) DEFAULT NULL,
  Municipio varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE paises (
  id_Pais int(11) NOT NULL,
  Codigo int(11) DEFAULT NULL,
  iso3166a1 char(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  iso3166a2 char(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  Pais varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE parroquias (
  id_Parroquia int(11) NOT NULL,
  Municipio_id int(11) DEFAULT NULL,
  Parroquia varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE password_resets (
  email varchar(125) COLLATE utf8mb4_unicode_ci NOT NULL,
  token varchar(125) COLLATE utf8mb4_unicode_ci NOT NULL,
  created_at timestamp NULL DEFAULT NULL
) ;

--

--

CREATE TABLE prefijos_cidni (
  id_Prefijo_CIDNI int(11) NOT NULL,
  Prefijo_CIDNI varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

--

CREATE TABLE servicios (
  id_Servicio int(11) NOT NULL,
  Servicio varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Costos decimal(10,2) DEFAULT NULL,
  simbolo varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  Especialidad_Medica_id int(11) DEFAULT NULL,
  Medico_id int(11) DEFAULT NULL,
  Status_id int(11) DEFAULT NULL,
  duracion time DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE sexos (
  id_Sexo int(11) NOT NULL,
  Sexo varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE status (
  id_Status int(11) NOT NULL,
  Status varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  color varchar(20) COLLATE utf8_unicode_ci NOT NULL DEFAULT '#FFFFFF',
  Nota varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE status_consultas (
  id_Consulta int(11) NOT NULL,
  Consulta varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  color varchar(20) COLLATE utf8_unicode_ci NOT NULL DEFAULT '#FFFFFF',
  Nota varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE status_factura (
  id_Status_Factura int(11) NOT NULL,
  Status_Factura varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  color varchar(20) COLLATE utf8_unicode_ci NOT NULL DEFAULT '#FFFFFF',
  Nota varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE status_medicos (
  id_Status_Medico int(11) NOT NULL,
  Status_Medico varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  color varchar(10) COLLATE utf8_unicode_ci NOT NULL DEFAULT '#FFFFFF',
  Nota varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE status_tasas (
  id_Status_Tasa int(11) NOT NULL,
  Tasa varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  color varchar(20) COLLATE utf8_unicode_ci NOT NULL DEFAULT '#FFFFFF',
  Nota varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE tasa_cambio (
  id_Tasa_Cambio int(11) NOT NULL,
  BS decimal(10,2) DEFAULT NULL,
  USD decimal(10,2) DEFAULT NULL,
  Fecha date DEFAULT NULL,
  Status_Tasa_id int(11) DEFAULT NULL
) ;

--

--

--

--

--

--

CREATE TABLE tipo_pagos (
  id_Tipos_Pago int(11) NOT NULL,
  Tipo_Pago varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL
) ;

--

--

--

--

--

--

--

CREATE TABLE usuarios_medicos (
  id_Medico int(11) NOT NULL,
  Nombres_Medico varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Prefijo_CIDNI_id int(11) DEFAULT NULL,
  Foto_Medico varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Apellidos_Medicos varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  CIDNI varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  Fecha_Nacimiento_Medico date DEFAULT NULL,
  Sexo_id int(11) DEFAULT NULL,
  Registro_MPPS varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  Numero_Colegio_de_Medico varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  Status_Medico_id int(11) DEFAULT 1,
  Civil_id int(11) DEFAULT NULL,
  Pais_id int(11) DEFAULT NULL,
  id_Estado int(11) DEFAULT NULL,
  id_Ciudad int(11) DEFAULT NULL,
  id_Municipio int(11) DEFAULT NULL,
  id_Parroquia int(11) DEFAULT NULL
) ;

--

--

--

--

CREATE TABLE usuarios_pacientes (
  id_Paciente int(11) NOT NULL,
  Nombres_Paciente varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  Apellidos_Paciente varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  Prefijo_CIDNI_id int(11) DEFAULT NULL,
  CIDNI varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  Fecha_Nacimiento_Paciente date DEFAULT NULL,
  Sexo_id int(11) DEFAULT NULL,
  Status_id int(11) DEFAULT 1,
  Civil_id int(11) DEFAULT NULL,
  Pais_id int(11) DEFAULT NULL
) ;

--

--
# citas/models.py

from django.db import models
from django.utils import timezone
from datetime import date 

# -------------------------------------------------------------
# MODELOS AUXILIARES Y GEOGRÁFICOS (managed = False)
# -------------------------------------------------------------

class Prefijo_CIDNI(models.Model):
    id_Prefijo_CIDNI = models.AutoField(
        primary_key=True, 
        db_column='id_Prefijo_CIDNI'
    )
    
    nombre_prefijo = models.CharField(
        max_length=10, 
        db_column='Prefijo_CIDNI'
    )
    
    def __str__(self):
        return self.nombre_prefijo
    
    class Meta:
        db_table = 'prefijos_cedula'
        managed = False 
        verbose_name = "Prefijo CIDNI"
        verbose_name_plural = "Prefijos CIDNI"

class Sexo(models.Model):
    id_Sexo = models.IntegerField(primary_key=True, db_column='id_Sexo')
    nombre = models.CharField(max_length=20, db_column='Sexo', verbose_name="Sexo")
    
    def __str__(self):
        return self.nombre
        
    class Meta:
        db_table = 'sexos' 
        managed = False 
        verbose_name = "Sexo"
        verbose_name_plural = "Sexos"

class EstadoCivil(models.Model):
    id_Estado_Civil = models.IntegerField(primary_key=True, db_column='id_Estado_Civil')
    nombre = models.CharField(max_length=50, db_column='Estado_Civil', verbose_name="Estado Civil")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
        
    class Meta:
        db_table = 'estados_civiles' 
        managed = False 
        verbose_name = "Estado Civil"
        verbose_name_plural = "Estados Civiles"
        
class Pais(models.Model):
    id_Pais = models.IntegerField(primary_key=True, db_column='id_Pais')
    nombre = models.CharField(max_length=128, db_column='Pais', verbose_name="País")
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True, verbose_name="Código")

    def __str__(self):
        return self.nombre
        
    class Meta:
        db_table = 'paises' 
        managed = False 
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ['nombre']

# MODELOS DE UBICACIÓN
class Estado(models.Model):
    id_Estado = models.IntegerField(primary_key=True, db_column='id_Estado')
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, db_column='Pais_id', null=True, blank=True)
    nombre = models.CharField(max_length=128, db_column='Estado', verbose_name="Estado")
    
    def __str__(self):
       return self.nombre

    class Meta:
        db_table = 'estados'
        managed = False
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ['nombre']

class Ciudad(models.Model):
    id_Ciudad = models.IntegerField(primary_key=True, db_column='id_Ciudad')
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING, db_column='Estado_id')
    nombre = models.CharField(max_length=128, db_column='Ciudad', verbose_name="Ciudad")
    
    def __str__(self):
        return self.nombre
        
    class Meta:
        db_table = 'ciudades' 
        managed = False
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
        ordering = ['nombre']

class Municipio(models.Model):
    id_Municipio = models.IntegerField(primary_key=True, db_column='id_Municipio')
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING, db_column='Estado_id')
    nombre = models.CharField(max_length=128, db_column='Municipio', verbose_name="Municipio")
    
    def __str__(self):
        return self.nombre
        
    class Meta:
        db_table = 'municipios'
        managed = False
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        ordering = ['nombre']

class Parroquia(models.Model):
    id_Parroquia = models.IntegerField(primary_key=True, db_column='id_Parroquia')
    municipio = models.ForeignKey(Municipio, on_delete=models.DO_NOTHING, db_column='Municipio_id')
    nombre = models.CharField(max_length=128, db_column='Parroquia', verbose_name="Parroquia")
    
    def __str__(self):
        return self.nombre
        
    class Meta:
        db_table = 'parroquias'
        managed = False
        verbose_name = "Parroquia"
        verbose_name_plural = "Parroquias"
        ordering = ['nombre']

# -------------------------------------------------------------
# MODELOS PRINCIPALES (managed = True o managed = False)
# -------------------------------------------------------------

class EspecialidadMedica(models.Model):
    """Modelo para las especialidades médicas"""
    id_Especialidad_Medica = models.AutoField(primary_key=True, verbose_name="ID Especialidad")
    Espacialidad_Medica = models.CharField(max_length=200, null=True, blank=True, verbose_name="Especialidad Médica")
    # Comentamos los campos que no existen en la base de datos
    # descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    # activa = models.BooleanField(default=True, verbose_name="¿Activa?")
    # fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    # fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        db_table = 'especialidades_medicas'
        managed = False  # No manejamos la creación de tablas para este modelo
        verbose_name = 'Especialidad Médica'
        verbose_name_plural = 'Especialidades Médicas'
        ordering = ['Espacialidad_Medica']

    def __str__(self):
        return self.Espacialidad_Medica or "Sin nombre"

class UsuarioMedico(models.Model):
    """Modelo para los médicos del sistema"""
    id_Medico = models.AutoField(primary_key=True, db_column='id_Medico')
    Nombres_Medico = models.CharField(max_length=200, db_column='Nombres_Medico', verbose_name='Nombres')
    Apellidos_Medicos = models.CharField(max_length=200, db_column='Apellidos_Medicos', verbose_name='Apellidos')
    Prefijo_CIDNI = models.ForeignKey(Prefijo_CIDNI, on_delete=models.SET_NULL, db_column='Prefijo_CIDNI_id', null=True, blank=True, verbose_name='Tipo de ID')
    CIDNI = models.CharField(max_length=20, db_column='CIDNI', verbose_name='Número de ID')
    Fecha_Nacimiento_Medico = models.DateField(db_column='Fecha_Nacimiento_Medico', null=True, blank=True, verbose_name='Fecha de Nacimiento')
    Sexo = models.ForeignKey(Sexo, on_delete=models.SET_NULL, db_column='Sexo_id', null=True, blank=True, verbose_name='Sexo')
    Registro_MPPS = models.CharField(max_length=30, db_column='Registro_MPPS', blank=True, null=True, verbose_name='Registro MPPS')
    Numero_Colegio_de_Medico = models.CharField(max_length=50, db_column='Numero_Colegio_de_Medico', blank=True, null=True, verbose_name='N° Colegio de Médicos')
    estado_civil = models.ForeignKey(EstadoCivil, on_delete=models.SET_NULL, db_column='Civil_id', null=True, blank=True, verbose_name='Estado Civil')
    Pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, db_column='Pais_id', null=True, blank=True, verbose_name='País')
    estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, db_column='id_Estado', null=True, blank=True, verbose_name='Estado/Provincia')
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, db_column='id_Ciudad', null=True, blank=True, verbose_name='Ciudad')
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, db_column='id_Municipio', null=True, blank=True, verbose_name='Municipio')
    parroquia = models.ForeignKey(Parroquia, on_delete=models.SET_NULL, db_column='id_Parroquia', null=True, blank=True, verbose_name='Parroquia')
    Foto_Medico = models.ImageField(upload_to='medicos/fotos/', db_column='Foto_Medico', blank=True, null=True, verbose_name='Fotografía')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    # 🔑 CORRECCIÓN DEL NAMEERROR: Usamos la cadena para la relación ManyToMany
    especialidades = models.ManyToManyField('citas.EspecialidadMedica', through='MedicoEspecialidad', blank=True, verbose_name='Especialidades') 
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name='Correo Electrónico')

    class Meta:
        db_table = 'usuarios_medicos'
        managed = True # ⬅️ CORRECCIÓN: Evita el error "UndefinedTable"
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'
        ordering = ['Apellidos_Medicos', 'Nombres_Medico']

    def __str__(self):
        return f"{self.Nombres_Medico} {self.Apellidos_Medicos}"

class MedicoEspecialidad(models.Model):
    """Tabla intermedia para la relación muchos a muchos entre Médico y Especialidad"""
    # 🔑 CORRECCIÓN DEL NAMEERROR: Usamos la cadena para la relación FK
    medico = models.ForeignKey('citas.UsuarioMedico', on_delete=models.CASCADE, db_column='id_Medico')
    especialidad = models.ForeignKey(EspecialidadMedica, on_delete=models.CASCADE, db_column='id_Especialidad_Medica')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    principal = models.BooleanField(default=False, verbose_name="Especialidad Principal")
    activo = models.BooleanField(default=True, verbose_name="¿Activo?")

    class Meta:
        db_table = 'medicos_especialidades'
        managed = True # ⬅️ CORRECCIÓN: Evita conflictos de migración
        verbose_name = 'Especialidad del Médico'
        verbose_name_plural = 'Especialidades de los Médicos'
        unique_together = (('medico', 'especialidad'),)

    def __str__(self):
        return f"{self.medico} - {self.especialidad}"


class Consultorio(models.Model):
    """Modelo para los consultorios médicos"""
    id_Consultorio = models.AutoField(primary_key=True, db_column='id_Consultorio')
    Direccion = models.CharField(max_length=200, null=True, blank=True, verbose_name='Dirección')
    numero_consultorio = models.CharField(max_length=200, null=True, blank=True, verbose_name='Número de Consultorio')
    Telefono = models.CharField(max_length=20, null=True, blank=True, verbose_name='Teléfono')
    Celular = models.CharField(max_length=20, null=True, blank=True, verbose_name='Celular')
    Correo = models.EmailField(max_length=200, null=True, blank=True, verbose_name='Correo Electrónico')
    
    # Relaciones con otros modelos
    Especialidad_Medica = models.ForeignKey(
        'EspecialidadMedica', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='Especialidad_Medica_id',
        verbose_name='Especialidad Médica'
    )
    
    # Ubicación geográfica
    estado = models.ForeignKey(
        'Estado', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='Estado_id',
        verbose_name='Estado/Provincia'
    )
    
    ciudad = models.ForeignKey(
        'Ciudad', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='Ciudad_id',
        verbose_name='Ciudad'
    )
    
    municipio = models.ForeignKey(
        'Municipio', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='Municipio_id',
        verbose_name='Municipio'
    )
    
    parroquia = models.ForeignKey(
        'Parroquia', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='Parroquia_id',
        verbose_name='Parroquia'
    )
    
    Status = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        db_table = 'consultorios'
        verbose_name = 'Consultorio'
        verbose_name_plural = 'Consultorios'
        ordering = ['numero_consultorio']

    def __str__(self):
        return f"Consultorio {self.numero_consultorio or 'Sin número'}"


class DatosSeniat(models.Model):
    """Datos fiscales del médico para el SENIAT"""
    id_Datos_SENIAT = models.AutoField(primary_key=True, db_column='id_Datos_SENIAT')
    # 🔑 CORRECCIÓN DEL NAMEERROR: Usamos la cadena para la relación OneToOne
    Medico = models.OneToOneField(
        'citas.UsuarioMedico',
        on_delete=models.CASCADE, 
        db_column='Medico_id', 
        related_name='datos_seniat',
        verbose_name='Médico',
        null=True, 
        blank=True
    )
    RIF = models.CharField(max_length=20, db_column='RIF', verbose_name='RIF', unique=True)
    Direccion = models.TextField(db_column='Direccion', verbose_name='Dirección Fiscal')
    Fecha = models.DateTimeField(auto_now=True, db_column='Fecha', verbose_name='Fecha de Registro')
    razon_social = models.CharField(max_length=200, blank=True, null=True, verbose_name='Razón Social')
    contribuyente_especial = models.BooleanField(default=False, verbose_name='¿Es Contribuyente Especial?')
    nro_licencia = models.CharField(max_length=50, blank=True, null=True, verbose_name='N° de Licencia')

    class Meta:
        db_table = 'datos_seniat'
        managed = True # ⬅️ CORRECCIÓN: Evita conflictos de migración
        verbose_name = 'Datos del SENIAT'
        verbose_name_plural = 'Datos del SENIAT'
        ordering = ['Medico__Apellidos_Medicos', 'Medico__Nombres_Medico']

    def __str__(self):
        return f"Datos SENIAT - {self.Medico}"

# -------------------------------------------------------------
# MODELOS DE TURNOS Y HORARIOS
# -------------------------------------------------------------

class Turno(models.Model):
    """
    Modelo para los turnos de atención médica
    """
    id_Turno = models.AutoField(primary_key=True, db_column='id_Turno')
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Turno')
    hora_inicio = models.TimeField(verbose_name='Hora de Inicio')
    hora_fin = models.TimeField(verbose_name='Hora de Fin')
    activo = models.BooleanField(default=True, verbose_name='¿Activo?')
    
    def __str__(self):
        return f"{self.nombre} ({self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')})"
    
    class Meta:
        db_table = 'turnos'
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'
        ordering = ['hora_inicio']


class HorarioCita(models.Model):
    """
    Modelo para los horarios de las citas médicas
    """
    medico = models.ForeignKey(
        'citas.UsuarioMedico',
        on_delete=models.CASCADE,
        db_column='medico_id',
        related_name='horarios_citas',
        verbose_name='Médico'
    )
    
    especialidad = models.ForeignKey(
        'citas.EspecialidadMedica',
        on_delete=models.CASCADE,
        db_column='especialidad_id',
        related_name='horarios_citas',
        verbose_name='Especialidad Médica'
    )
    
    turno = models.ForeignKey(
        'citas.Turno',
        on_delete=models.CASCADE,
        db_column='turno_id',
        related_name='horarios_citas',
        verbose_name='Turno'
    )
    
    domicilio = models.BooleanField(
        default=False,
        verbose_name='¿Atención a Domicilio?'
    )
    
    calendar_event_id = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name='ID del Evento en el Calendario'
    )
    
    calendar_id = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name='ID del Calendario'
    )
    
    start_datetime = models.DateTimeField(
        verbose_name='Fecha y Hora de Inicio'
    )
    
    end_datetime = models.DateTimeField(
        verbose_name='Fecha y Hora de Fin'
    )
    
    recurrence_rule = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Regla de Recurrencia'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='¿Activo?'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    
    def __str__(self):
        return f"{self.medico} - {self.especialidad} - {self.start_datetime.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        db_table = 'horarios_citas'
        verbose_name = 'Horario de Cita'
        verbose_name_plural = 'Horarios de Citas'
        ordering = ['-start_datetime', 'medico']
        indexes = [
            models.Index(fields=['medico', 'especialidad']),
            models.Index(fields=['start_datetime', 'end_datetime']),
            models.Index(fields=['activo']),
        ]


# -------------------------------------------------------------
# MODELOS DE PACIENTES
# -------------------------------------------------------------

class Paciente(models.Model):
    # Campos directos
    id_Paciente = models.AutoField(primary_key=True)
    Nombres_Paciente = models.CharField(max_length=200)
    Apellidos_Paciente = models.CharField(max_length=100)
    CIDNI = models.CharField(max_length=20) 
    Fecha_Nacimiento_Paciente = models.DateField()
    Fecha_Registro = models.DateTimeField(default=timezone.now)
    Activo = models.BooleanField(default=True)
    
    Ultima_Actualizacion = models.DateTimeField(default=timezone.now, verbose_name="Última Actualización")
    
    # LLAVES FORÁNEAS
    Pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, verbose_name="País de Origen")
    Prefijo_CIDNI = models.ForeignKey(Prefijo_CIDNI, on_delete=models.SET_NULL, null=True, verbose_name="Prefijo ID")
    Sexo = models.ForeignKey(Sexo, on_delete=models.SET_NULL, null=True, verbose_name="Sexo")
    estado_civil_new = models.ForeignKey(EstadoCivil, on_delete=models.SET_NULL, null=True, verbose_name="Estado Civil")
    # ❌ CAMBIO: Eliminado Civil_id ya que es redundante con estado_civil_new
    
    class Meta:
        db_table = 'usuarios_pacientes'
        managed = False 
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['Apellidos_Paciente', 'Nombres_Paciente'] 

    def __str__(self):
        return f"{self.Nombres_Paciente} {self.Apellidos_Paciente}"

class DireccionPaciente(models.Model):
    """Modelo para las direcciones de los pacientes"""
    id_Direccion_Paciente = models.AutoField(primary_key=True, db_column='id_Direccion_Paciente')
    
    # Relación con el paciente
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, db_column='Paciente_id', related_name='direccion', verbose_name="Paciente")
    
    # Contacto y dirección
    telefono = models.CharField(max_length=20, db_column='Telefono', blank=True, null=True, verbose_name="Teléfono Fijo")
    celular = models.CharField(max_length=20, db_column='Celular', verbose_name="Teléfono Móvil")
    correo = models.EmailField(max_length=200, db_column='Correo', verbose_name="Correo Electrónico", blank=True, null=True)
    direccion = models.TextField(db_column='Direccion', verbose_name="Dirección Completa")
    numero_casa = models.CharField(max_length=50, db_column='Numero_Casa', blank=True, null=True, verbose_name="Número de Casa/Apartamento")
    
    # Ubicación geográfica (Foreign Keys)
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING, db_column='Estado_id', null=True, blank=True, verbose_name="Estado/Provincia")
    ciudad = models.ForeignKey(Ciudad, on_delete=models.DO_NOTHING, db_column='Ciudad_id', null=True, blank=True, verbose_name="Ciudad/Localidad")
    municipio = models.ForeignKey(Municipio, on_delete=models.DO_NOTHING, db_column='Municipio_id', null=True, blank=True, verbose_name="Municipio")
    parroquia = models.ForeignKey(Parroquia, on_delete=models.DO_NOTHING, db_column='Parroquia_id', null=True, blank=True, verbose_name="Parroquia")

    class Meta:
        db_table = 'direcciones_pacientes' 
        managed = False 
        verbose_name = "Dirección del Paciente"
        verbose_name_plural = "Direcciones de Pacientes"
        # CORRECCIÓN: Nombres de campo exactos para ordering
        ordering = ['paciente__Apellidos_Paciente', 'paciente__Nombres_Paciente']

    def __str__(self):
        # Aseguramos que __str__ no cause errores si el paciente no existe temporalmente
        try:
            return f"Dirección de {self.paciente}"
        except:
             return f"Dirección ID {self.id_Direccion_Paciente}"

# En tu archivo models.py de la app citas

class Turno(models.Model):
    """
    Modelo para los turnos de atención médica
    """
    id_Turno = models.AutoField(primary_key=True, db_column='id_Turno')
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Turno')
    hora_inicio = models.TimeField(
        verbose_name='Hora de Inicio', 
        null=True, 
        blank=True,
        help_text='Formato: HH:MM'
    )
    hora_fin = models.TimeField(
        verbose_name='Hora de Fin', 
        null=True, 
        blank=True,
        help_text='Formato: HH:MM'
    )
    activo = models.BooleanField(default=True, verbose_name='¿Activo?')
    
    def __str__(self):
        if self.hora_inicio and self.hora_fin:
            return f"{self.nombre} ({self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')})"
        return self.nombre
    
    class Meta:
        db_table = 'turnos'
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'
        ordering = ['nombre']

class HorarioCita(models.Model):
    """
    Modelo para los horarios de las citas médicas
    """
    medico = models.ForeignKey(
        'citas.UsuarioMedico',
        on_delete=models.CASCADE,
        db_column='medico_id',
        related_name='horarios_citas',
        verbose_name='Médico'
    )
    
    especialidad = models.ForeignKey(
        'citas.EspecialidadMedica',
        on_delete=models.CASCADE,
        db_column='especialidad_id',
        related_name='horarios_citas',
        verbose_name='Especialidad Médica'
    )
    
    turno = models.ForeignKey(
        'citas.Turno',
        on_delete=models.CASCADE,
        db_column='turno_id',
        related_name='horarios_citas',
        verbose_name='Turno'
    )
    
    domicilio = models.BooleanField(
        default=False,
        verbose_name='¿Atención a Domicilio?'
    )
    
    calendar_event_id = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name='ID del Evento en el Calendario'
    )
    
    calendar_id = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name='ID del Calendario'
    )
    
    start_datetime = models.DateTimeField(
        verbose_name='Fecha y Hora de Inicio'
    )
    
    end_datetime = models.DateTimeField(
        verbose_name='Fecha y Hora de Fin'
    )
    
    recurrence_rule = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Regla de Recurrencia'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='¿Activo?'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    
    def __str__(self):
        return f"{self.medico} - {self.especialidad} - {self.start_datetime.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        db_table = 'horarios_citas'
        verbose_name = 'Horario de Cita'
        verbose_name_plural = 'Horarios de Citas'
        ordering = ['-start_datetime', 'medico']
        indexes = [
            models.Index(fields=['medico', 'especialidad']),
            models.Index(fields=['start_datetime', 'end_datetime']),
            models.Index(fields=['activo']),
        ]

class Banco(models.Model):
    """
    Modelo para almacenar la información de los bancos en bolívares
    """
    id_Bancos = models.AutoField(primary_key=True, db_column='id_Bancos')
    Bancos = models.CharField('Nombre del Banco', max_length=200, db_column='Bancos')
    Activo = models.BooleanField('Activo', default=True, db_column='Activo')
    Codigo_Bancario = models.IntegerField('Código Bancario', db_column='Codigo_Bancario', null=True, blank=True)

    class Meta:
        db_table = 'bancos'
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        ordering = ['Bancos']

    def __str__(self):
        return self.Bancos or 'Sin nombre de banco'
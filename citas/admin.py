# citas/admin.py

# Importaciones de Django
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin 
from django.http import JsonResponse
from django.urls import path
from django.utils.safestring import mark_safe

# Importaciones de terceros
from dateutil import rrule
import datetime

# Importar modelos de la aplicación
from .models import (
    HorarioCita, Turno, Paciente, Prefijo_CIDNI, Sexo, EstadoCivil, Pais,
    Estado, Ciudad, Municipio, Parroquia, DireccionPaciente, 
    EspecialidadMedica, UsuarioMedico, DatosSeniat, MedicoEspecialidad,
    Consultorio, Banco
)

# ----------------------------------------------------
# 1. ADMIN SITE PERSONALIZADO (Definición Única y Centralizada)
# ----------------------------------------------------
class CustomAdminSite(admin.AdminSite):
    site_header = 'Unidad Médica Admin'
    site_title = 'Unidad Médica'
    index_title = 'Administración'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get_ciudades/', self.admin_view(self.get_ciudades), name='get_ciudades'),
            path('get_municipios/', self.admin_view(self.get_municipios), name='get_municipios'),
            path('get_parroquias/', self.admin_view(self.get_parroquias), name='get_parroquias'),
        ]
        return custom_urls + urls

    # Métodos de vista para AJAX (para la selección de Ubicaciones)
    def get_ciudades(self, request):
        estado_id = request.GET.get('estado_id')
        if estado_id:
            ciudades = Ciudad.objects.filter(estado_id=estado_id).values('id_Ciudad', 'nombre')
            return JsonResponse(list(ciudades), safe=False)
        return JsonResponse([], safe=False)
    
    def get_municipios(self, request):
        estado_id = request.GET.get('estado_id')
        if estado_id:
            municipios = Municipio.objects.filter(estado_id=estado_id).values('id_Municipio', 'nombre')
            return JsonResponse(list(municipios), safe=False)
        return JsonResponse([], safe=False)
    
    def get_parroquias(self, request):
        municipio_id = request.GET.get('municipio_id')
        if municipio_id:
            parroquias = Parroquia.objects.filter(municipio_id=municipio_id).values('id_Parroquia', 'nombre')
            return JsonResponse(list(parroquias), safe=False)
        return JsonResponse([], safe=False)


# Crear la ÚNICA instancia personalizada de AdminSite
admin_site = CustomAdminSite(name='citas_admin') 

# --------------------------------------------------------------------------
# 2. DEFINICIONES DE HORARIO Y TURNO (Para la Recurrencia)
# --------------------------------------------------------------------------

# Opciones para la regla de repetición (RRULE)
FREQ_CHOICES = (
    ('DAILY', 'Diario'),
    ('WEEKLY', 'Semanal'),
    ('MONTHLY', 'Mensual'),
)

# Opciones para los días de la semana (BYDAY)
DAY_CHOICES = (
    ('MO', 'Lunes'), ('TU', 'Martes'), ('WE', 'Miércoles'), 
    ('TH', 'Jueves'), ('FR', 'Viernes'), ('SA', 'Sábado'), ('SU', 'Domingo'),
)

class HorarioCitaForm(forms.ModelForm):
    """Formulario para gestionar los campos de recurrencia y generar el RRULE."""
    
    # Campos auxiliares que NO existen en el modelo (sólo para la UI)
    recurrence_frequency = forms.ChoiceField(
        choices=FREQ_CHOICES,
        required=False,
        label="Frecuencia de Repetición",
        initial='WEEKLY'
    )
    
    recurrence_byday = forms.MultipleChoiceField(
        choices=DAY_CHOICES,
        required=False,
        label="Días de la semana para repetir (solo si es Semanal)",
        widget=admin.widgets.FilteredSelectMultiple("Días", is_stacked=False)
    )
    
    recurrence_until = forms.DateField(
        required=False,
        label="Repetir hasta (opcional, formato AAAA-MM-DD)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Media:
        css = {
            'all': ('//cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',)
        }
        js = (
            '//code.jquery.com/jquery-3.6.0.min.js',
            '//cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
        )

    class Meta:
        model = HorarioCita
        fields = '__all__'  # Incluir todos los campos por defecto

    def clean(self):
        cleaned_data = super().clean()
        
        freq = cleaned_data.get('recurrence_frequency')
        byday = cleaned_data.get('recurrence_byday')
        until = cleaned_data.get('recurrence_until')
        start_datetime = cleaned_data.get('start_datetime')
        end_datetime = cleaned_data.get('end_datetime')
        
        # Validar que la fecha de inicio sea anterior a la de fin
        if start_datetime and end_datetime and start_datetime >= end_datetime:
            raise forms.ValidationError({
                'end_datetime': 'La fecha/hora de fin debe ser posterior a la de inicio.'
            })
        
        # Si no hay frecuencia, no hay recurrencia.
        if not freq:
            cleaned_data['recurrence_rule'] = None
            return cleaned_data
                
        if freq == 'WEEKLY' and not byday:
            raise forms.ValidationError(
                {'recurrence_byday': 'Debe seleccionar al menos un día si la repetición es semanal.'}
            )


        # 1. Construcción Manual de la Cadena RRULE
        rrule_parts = [f"FREQ={freq}"]
        
        if freq == 'WEEKLY' and byday:
            # Ordenamos los días y los añadimos (Ej: BYDAY=MO,WE,FR)
            rrule_parts.append(f"BYDAY={','.join(byday)}")
            
        if until:
            # El formato UNTIL debe ser UTC sin separadores (AAAA MM DD T HH MM SS Z)
            
            # Obtener el final del día en el que termina la repetición
            dt_until = datetime.datetime.combine(until, datetime.time(23, 59, 59))
            
            # Si start_datetime tiene zona horaria, necesitamos asignársela a dt_until
            if start_datetime and start_datetime.tzinfo:
                # ➡️ CORRECCIÓN AQUÍ: Usamos replace(tzinfo=...) y luego convertimos a UTC
                tz = start_datetime.tzinfo
                dt_until = dt_until.replace(tzinfo=tz).astimezone(datetime.timezone.utc) 
            else:
                # Si no hay zona horaria de inicio, asumimos UTC para UNTIL
                dt_until = dt_until.replace(tzinfo=datetime.timezone.utc)

            rrule_parts.append(f"UNTIL={dt_until.strftime('%Y%m%dT%H%M%SZ')}")

        # Guardamos la cadena RRULE en el campo del modelo
        cleaned_data['recurrence_rule'] = ";".join(rrule_parts)
        
        return cleaned_data


class HorarioCitaAdmin(admin.ModelAdmin):
    form = HorarioCitaForm
    list_display = (
        'medico', 'especialidad', 'turno', 'start_datetime', 'end_datetime', 
        'get_recurrence_display', 'activo', 'domicilio'
    )
    list_filter = ('activo', 'domicilio', 'especialidad', 'turno')
    search_fields = ('medico__Nombres_Medico', 'especialidad__Espacialidad_Medica')
    raw_id_fields = ('medico', 'especialidad', 'turno')
    date_hierarchy = 'start_datetime'
    
    class Media:
        js = ('js/admin/horariocita_admin.js',)
        css = {
            'all': ('css/admin/horariocita_admin.css',)
        }

    fieldsets = (
        ("Información del Horario", {
            # Se usan tuplas para agrupar campos en una fila
            'fields': (
                'medico', 
                'especialidad', 
                'turno', 
                'start_datetime', 
                'end_datetime', 
                'domicilio', 
                'activo',
            )
        }),
        ("Configuración de Recurrencia (Opcional)", {
            'fields': (
                'recurrence_frequency',
                'recurrence_byday',
                'recurrence_until',
            ),
            'classes': ('wide',), 
            'description': 'Define la regla de repetición del horario. Si deja en blanco, será un evento único.'
        }),
       # ("Metadatos de Google Calendar", {
       #     'fields': (
       #         'calendar_event_id',
       #         'calendar_id',
       #         'recurrence_rule', 
       #         'fecha_creacion',
       #         'fecha_actualizacion',
       #     ),
       #     'classes': ('collapse',), 
       # })
    )
    
    readonly_fields = ('calendar_event_id', 'calendar_id', 'recurrence_rule', 'fecha_creacion', 'fecha_actualizacion')

    def get_recurrence_display(self, obj):
        """Muestra la regla de recurrencia de forma legible en la lista."""
        return obj.recurrence_rule if obj.recurrence_rule else 'Evento Único'
    get_recurrence_display.short_description = 'Repetición'


class TurnoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'hora_inicio', 'hora_fin')
    search_fields = ('nombre',)
    ordering = ('hora_inicio',)

# ----------------------------------------------------
# 3. DEFINICIONES DE MEDICO (UsuarioMedico) y ESPECIALIDAD
#    (Se definen antes de MedicoEspecialidadAdmin para evitar NameError/Indexación)
# ----------------------------------------------------

class DatosSeniatInline(admin.StackedInline):
    model = DatosSeniat
    can_delete = False
    extra = 0
    min_num = 1
    max_num = 1
    fields = ('RIF', 'Direccion', 'razon_social', 'contribuyente_especial', 'nro_licencia')
    readonly_fields = ('Fecha',)

class EspecialidadMedicaFilter(admin.SimpleListFilter):
    title = 'especialidad'
    parameter_name = 'especialidad'

    def lookups(self, request, model_admin):
        return EspecialidadMedica.objects.values_list('id_Especialidad_Medica', 'Espacialidad_Medica')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(especialidades__id_Especialidad_Medica=self.value())
        return queryset

class UsuarioMedicoAdmin(admin.ModelAdmin):
    list_display = ('Nombres_Medico', 'Apellidos_Medicos', 'CIDNI', 'get_especialidades', 'activo', 'fecha_registro')
    list_filter = ('activo', 'Sexo', 'estado_civil', 'Pais', 'estado', EspecialidadMedicaFilter)
    search_fields = ('Nombres_Medico', 'Apellidos_Medicos', 'CIDNI', 'Registro_MPPS', 'Numero_Colegio_de_Medico')
    list_per_page = 20
    inlines = [DatosSeniatInline]
    
    fieldsets = (
        ('Información Personal y de Contacto', {
            'fields': [
                'Nombres_Medico',
                'Apellidos_Medicos',
                'Prefijo_CIDNI',
                'CIDNI',
                'Fecha_Nacimiento_Medico',
                'Sexo',
                'estado_civil',
                'telefono',
                'email',
                'Foto_Medico',
                'activo'
            ]
        }),
        ('Información Profesional', {
            'fields': [
                'Registro_MPPS',
                'Numero_Colegio_de_Medico',
            ]
        }),
        ('Ubicación', {
            'fields': [
                'Pais',
                'estado',
                'ciudad',
                'municipio',
                'parroquia'
            ],
            'classes': ('collapse',),
            'description': mark_safe('<p>La selección del estado actualizará las opciones de ciudad, municipio y parroquia.</p>')
        })
    )
    
    class Media:
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
                'admin/css/select2-custom.css',
            )
        }
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
            'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/i18n/es.js',
            'js/direccion_admin_select2.js',
        )
        
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        ubicacion_fields = ['estado', 'ciudad', 'municipio', 'parroquia']
        for field_name in ubicacion_fields:
            if field_name in form.base_fields:
                form.base_fields[field_name].widget.attrs.update({
                    'class': 'select2',
                    'style': 'width: 100%',
                    'data-placeholder': 'Seleccione una opción...'
                })
        form.base_fields['Pais'].initial = 1
        form.base_fields['Pais'].disabled = True
        form.base_fields['Pais'].label = 'País (Venezuela)'
        return form
    
    def get_especialidades(self, obj):
        return ", ".join([e.Espacialidad_Medica for e in obj.especialidades.all()])
    get_especialidades.short_description = 'Especialidades'
    
    def save_model(self, request, obj, form, change):
        obj.Pais_id = 1
        super().save_model(request, obj, form, change)


class EspecialidadMedicaAdmin(admin.ModelAdmin):
    list_display = ('id_Especialidad_Medica', 'Espacialidad_Medica')
    search_fields = ('Espacialidad_Medica',)
    ordering = ('Espacialidad_Medica',)
    list_per_page = 20

# ----------------------------------------------------
# 4. DEFINICIÓN DE INTERSECCIÓN (MedicoEspecialidad)
# ----------------------------------------------------

class MedicoEspecialidadAdminForm(forms.ModelForm):
    class Meta:
        model = MedicoEspecialidad
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'medico' in self.fields:
            self.fields['medico'].label_from_instance = lambda obj: f"{obj.Nombres_Medico} {obj.Apellidos_Medicos}"

class MedicoEspecialidadAdmin(admin.ModelAdmin):
    form = MedicoEspecialidadAdminForm
    list_display = ('get_medico_nombre', 'especialidad', 'principal', 'activo')
    list_filter = ('principal', 'activo')
    search_fields = (
        'medico__Nombres_Medico', 
        'medico__Apellidos_Medicos', 
        'especialidad__Espacialidad_Medica'
    )
    list_select_related = ('medico', 'especialidad')
    # ✅ CORRECCIÓN FINAL: raw_id_fields para evitar E039 con CustomAdminSite
    raw_id_fields = ('medico', 'especialidad') 
    list_per_page = 20
    
    def get_medico_nombre(self, obj):
        return f"{obj.medico.Nombres_Medico} {obj.medico.Apellidos_Medicos}"
    get_medico_nombre.short_description = 'Médico'


# ----------------------------------------------------
# 5. DEFINICIONES DE PACIENTE Y UBICACIÓN
# ----------------------------------------------------

class DireccionPacienteInline(admin.StackedInline):
    model = DireccionPaciente
    max_num = 1
    min_num = 1
    can_delete = False
    
    fieldsets = [
        ("Información de Contacto", {
            'fields': ['celular', 'correo', 'telefono']
        }),
        ("Ubicación Geográfica", {
            'fields': ['estado', 'ciudad', 'municipio', 'parroquia', 'direccion', 'numero_casa'],
            'description': mark_safe('<p>La selección del estado actualizará las opciones de ciudad, municipio y parroquia.</p>')
        })
    ]
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        form = formset.form
        ubicacion_fields = ['estado', 'ciudad', 'municipio', 'parroquia']
        for field_name in ubicacion_fields:
            if field_name in form.base_fields:
                form.base_fields[field_name].widget.attrs.update({
                    'class': 'select2',
                    'style': 'width: 100%',
                    'data-placeholder': 'Seleccione una opción...'
                })
        return formset
    
    class Media:
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
                'admin/css/select2-custom.css',
            )
        }
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
            'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/i18n/es.js',
            'js/direccion_admin_select2.js',
        )

class PacienteAdmin(admin.ModelAdmin):
    inlines = [DireccionPacienteInline]
    
    list_display = (
        'Nombres_Paciente', 'Apellidos_Paciente', 'CIDNI', 'get_prefijo_cidni', 'Pais', 'Activo'
    )
    
    list_filter = ('Activo', 'Pais', 'estado_civil_new')
    search_fields = ('Nombres_Paciente', 'Apellidos_Paciente', 'CIDNI')
    
    fieldsets = (
        ("Información Personal e Identificación", {
            'fields': [
                'Nombres_Paciente', 'Apellidos_Paciente', 'Fecha_Nacimiento_Paciente', 'Pais',
                'Prefijo_CIDNI', 'CIDNI', 'Sexo', 'estado_civil_new', 'Activo'
            ],
            'description': 'Datos personales e identificación del paciente'
        }),
    )
    
    readonly_fields = ('Fecha_Registro', 'Ultima_Actualizacion')
    
    def get_prefijo_cidni(self, obj):
        return obj.Prefijo_CIDNI.nombre_prefijo if obj.Prefijo_CIDNI else ""
    get_prefijo_cidni.short_description = "Prefijo ID"
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'Pais' in form.base_fields:
            form.base_fields['Pais'].initial = 1  
        return form
    
    def save_model(self, request, obj, form, change):
        if not obj.Pais_id:
            obj.Pais_id = 1  
        super().save_model(request, obj, form, change)


# Configuración para los modelos de ubicación geográfica
class PaisAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'codigo')
    list_display = ('nombre', 'codigo')
    list_per_page = 20

class EstadoAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'pais__nombre')
    list_display = ('nombre', 'pais')
    list_filter = ('pais',)
    list_per_page = 20

class CiudadAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'estado__nombre')
    list_display = ('nombre', 'estado')
    list_filter = ('estado', 'estado__pais')
    list_per_page = 20

class MunicipioAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'estado__nombre')
    list_display = ('nombre', 'estado')
    list_filter = ('estado', 'estado__pais')
    list_per_page = 20

class ParroquiaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'municipio__nombre', 'municipio__estado__nombre')
    list_display = ('nombre', 'municipio', 'get_estado')
    list_filter = ('municipio__estado', 'municipio')
    list_per_page = 20
    
    def get_estado(self, obj):
        return obj.municipio.estado if obj.municipio else ''
    get_estado.short_description = 'Estado'

# Registro del modelo Consultorio
class ConsultorioAdmin(admin.ModelAdmin):
    list_display = ('numero_consultorio', 'Direccion', 'Telefono', 'Celular', 'Especialidad_Medica', 'ciudad', 'Status')
    list_filter = ('Status', 'Especialidad_Medica', 'estado', 'ciudad', 'municipio')
    search_fields = ('numero_consultorio', 'Direccion', 'Telefono', 'Celular', 'Correo')
    list_select_related = ('Especialidad_Medica', 'estado', 'ciudad', 'municipio', 'parroquia')
    list_per_page = 20
    autocomplete_fields = ['Especialidad_Medica', 'estado', 'ciudad', 'municipio', 'parroquia']

@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ('Bancos', 'Codigo_Bancario', 'Activo')
    list_filter = ('Activo',)
    search_fields = ('Bancos', 'Codigo_Bancario')
    ordering = ('Bancos',)
# ----------------------------------------------------
# 6. REGISTRO FINAL DE MODELOS EN admin_site
# ----------------------------------------------------

# Desregistrar los modelos de autenticación de la instancia admin por defecto
try:
    admin.site.unregister(User)
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

# Registro en el CustomAdminSite (admin_site)
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin) 

# Modelos de Apoyo
admin_site.register(Prefijo_CIDNI)
admin_site.register(Sexo)
admin_site.register(EstadoCivil)

# Modelos Principales
admin_site.register(EspecialidadMedica, EspecialidadMedicaAdmin)
admin_site.register(UsuarioMedico, UsuarioMedicoAdmin)
admin_site.register(MedicoEspecialidad, MedicoEspecialidadAdmin)
admin_site.register(Paciente, PacienteAdmin)
admin_site.register(Consultorio, ConsultorioAdmin)
admin_site.register(Banco, BancoAdmin)

# Modelos de Horarios
admin_site.register(HorarioCita, HorarioCitaAdmin)
admin_site.register(Turno, TurnoAdmin)

# Modelos Geográficos
admin_site.register(Pais, PaisAdmin)
admin_site.register(Estado, EstadoAdmin)
admin_site.register(Ciudad, CiudadAdmin)
admin_site.register(Municipio, MunicipioAdmin)
admin_site.register(Parroquia, ParroquiaAdmin)

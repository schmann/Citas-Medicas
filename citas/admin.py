# citas/admin.py

# Importaciones de Django
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin 
from django.http import JsonResponse
from django.urls import path, reverse, include
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import RedirectView
from .models import CitasReservadas

# Importaciones de terceros
from dateutil import rrule
import datetime
import pytz
from django.utils import timezone

# Importar modelos de la aplicación
from .models import (
    HorarioCita, Turno, Paciente, Prefijo_CIDNI, Sexo, EstadoCivil, Pais,
    Estado, Ciudad, Municipio, Parroquia, DireccionPaciente, 
    EspecialidadMedica, UsuarioMedico, DatosSeniat, MedicoEspecialidad,
    Consultorio, Banco
)

# ----------------------------------------------------
# 1. ADMIN SITE PERSONALIZADO (SIMPLIFICADO PARA JAZZMIN)
# ----------------------------------------------------
class CustomAdminSite(admin.AdminSite):
    site_header = 'Unidad Médica Admin'
    site_title = 'Unidad Médica'
    index_title = 'Administración'
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('get_ciudades/', self.admin_view(self.get_ciudades), name='get_ciudades'),
            path('get_municipios/', self.admin_view(self.get_municipios), name='get_municipios'),
            path('get_parroquias/', self.admin_view(self.get_parroquias), name='get_parroquias'),
            path('get_especialidades_medico/', self.admin_view(self.get_especialidades_medico), name='get_especialidades_medico'),
        ]
        return custom_urls + urls
        
    def calendario_view(self, request):
        # Verificar permisos
        if not request.user.is_staff:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
            
        # Verificar permiso específico
        if not request.user.has_perm('citas.view_citasreservadas'):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
            
        context = dict(
            self.each_context(request),
            title='Calendario de Citas',
            app_label='citas',
            is_popup=False,
            has_view_permission=True,
            has_add_permission=request.user.has_perm('citas.add_citasreservadas'),
            has_change_permission=request.user.has_perm('citas.change_citasreservadas'),
            has_delete_permission=request.user.has_perm('citas.delete_citasreservadas'),
        )
        from django.shortcuts import render
        return render(request, 'citas/reservas/calendario_nuevo.html', context)
        
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        
        # Verificar si el usuario tiene permiso para ver el calendario
        if request.user.has_perm('citas.view_citasreservadas'):
            # Agregar el enlace al calendario
            app_list.append({
                'name': 'Calendario',
                'app_label': 'citas_calendario',
                'models': [
                    {
                        'name': 'Reservar Cita',
                        'object_name': 'reservar_cita',
                        'admin_url': '/citas/calendario-nuevo/',
                        'view_only': True,
                    }
                ]
            })
        
        return app_list

    # Métodos de vista para AJAX
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
    
    def get_especialidades_medico(self, request):
        medico_id = request.GET.get('medico_id')
        if medico_id:
            try:
                # Obtener el médico con sus especialidades
                from django.db.models import Prefetch
                from .models import MedicoEspecialidad, EspecialidadMedica
                
                # Obtener todas las especialidades del médico, incluyendo las inactivas
                especialidades = MedicoEspecialidad.objects.filter(
                    medico_id=medico_id
                ).select_related('especialidad').order_by('especialidad__Espacialidad_Medica')
                
                # Preparar los datos para la respuesta
                especialidades_data = []
                for especialidad in especialidades:
                    especialidades_data.append({
                        'id': especialidad.id,
                        'especialidad__id_Especialidad_Medica': especialidad.especialidad.id_Especialidad_Medica,
                        'especialidad__Espacialidad_Medica': especialidad.especialidad.Espacialidad_Medica,
                        'activo': especialidad.activo
                    })
                
                print(f"[DEBUG] Especialidades encontradas para médico {medico_id}: {len(especialidades_data)}")
                return JsonResponse(especialidades_data, safe=False)
                
            except Exception as e:
                print(f"[ERROR] Error al obtener especialidades: {str(e)}")
                return JsonResponse([], safe=False)
        return JsonResponse([], safe=False)

# Crear la instancia personalizada de AdminSite
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
    """
    Formulario para gestionar los horarios de citas con campos separados para fecha y hora.
    """
    # Campos para fecha y hora de inicio
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True,
        label='Fecha de inicio'
    )
    hora_inicio = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': '300'}),
        required=True,
        label='Hora de inicio'
    )
    
    # Campos para fecha y hora de fin
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True,
        label='Fecha de fin'
    )
    hora_fin = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': '300'}),
        required=True,
        label='Hora de fin'
    )
    
    # Campos de recurrencia
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
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = HorarioCita
        fields = '__all__'
        exclude = ('start_datetime', 'end_datetime')  # Excluimos los campos originales

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si estamos editando un objeto existente, establecer valores iniciales
        if self.instance and self.instance.pk:
            tz = timezone.get_current_timezone()
            if self.instance.start_datetime:
                local_start = timezone.localtime(self.instance.start_datetime, tz)
                self.initial['fecha_inicio'] = local_start.date()
                self.initial['hora_inicio'] = local_start.time()
            if self.instance.end_datetime:
                local_end = timezone.localtime(self.instance.end_datetime, tz)
                self.initial['fecha_fin'] = local_end.date()
                self.initial['hora_fin'] = local_end.time()

    def clean(self):
        cleaned_data = super().clean()
        tz = timezone.get_current_timezone()

        # Obtener fechas y horas del formulario
        fecha_inicio = cleaned_data.get('fecha_inicio')
        hora_inicio = cleaned_data.get('hora_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        hora_fin = cleaned_data.get('hora_fin')

        # Combinar fecha y hora
        if fecha_inicio and hora_inicio:
            start_datetime = timezone.make_aware(
                datetime.datetime.combine(fecha_inicio, hora_inicio),
                tz
            )
            cleaned_data['start_datetime'] = start_datetime

        if fecha_fin and hora_fin:
            end_datetime = timezone.make_aware(
                datetime.datetime.combine(fecha_fin, hora_fin),
                tz
            )
            cleaned_data['end_datetime'] = end_datetime

        # Validar que la fecha de fin sea posterior a la de inicio
        if 'start_datetime' in cleaned_data and 'end_datetime' in cleaned_data:
            if cleaned_data['end_datetime'] <= cleaned_data['start_datetime']:
                self.add_error('fecha_fin', 'La fecha y hora de finalización debe ser posterior a la de inicio')
                self.add_error('hora_fin', '')

        # Procesar regla de recurrencia si existe
        freq = cleaned_data.get('recurrence_frequency')
        byday = cleaned_data.get('recurrence_byday')
        until = cleaned_data.get('recurrence_until')
        
        if freq:
            # Construir la regla de recurrencia
            rrule_parts = [f"FREQ={freq}"]
            
            if freq == 'WEEKLY' and byday:
                rrule_parts.append(f"BYDAY={','.join(byday)}")
            
            if until:
                # Convertir la fecha de fin a UTC para la regla de recurrencia
                dt_until = datetime.datetime.combine(until, datetime.time(23, 59, 59))
                dt_until = timezone.make_aware(dt_until, tz).astimezone(datetime.timezone.utc)
                rrule_parts.append(f"UNTIL={dt_until.strftime('%Y%m%dT%H%M%SZ')}")
            
            cleaned_data['recurrence_rule'] = ";".join(rrule_parts)
        else:
            cleaned_data['recurrence_rule'] = None

        return cleaned_data
        
    def save(self, commit=True):
        """Asegura que los campos generados en clean se guarden correctamente."""
        instance = super().save(commit=False)
        
        # Asignar los valores de los campos calculados
        if 'start_datetime' in self.cleaned_data:
            instance.start_datetime = self.cleaned_data['start_datetime']
        if 'end_datetime' in self.cleaned_data:
            instance.end_datetime = self.cleaned_data['end_datetime']
        if 'recurrence_rule' in self.cleaned_data:
            instance.recurrence_rule = self.cleaned_data['recurrence_rule']
        
        if commit:
            instance.save()
        return instance  

class HorarioCitaAdmin(admin.ModelAdmin):
    form = HorarioCitaForm
    
    # Listado y búsqueda
    list_display = (
        'medico', 'especialidad', 'turno', 'get_fecha_inicio', 'get_hora_inicio',
        'get_fecha_fin', 'get_hora_fin', 'get_recurrence_display', 'activo', 'domicilio',
        'ver_agenda_button'
    )
    list_filter = ('activo', 'domicilio', 'especialidad', 'turno')
    search_fields = ('medico__Nombres_Medico', 'especialidad__Espacialidad_Medica')
    autocomplete_fields = ('medico', 'turno')
    date_hierarchy = 'start_datetime'
    
    class Media:
        js = (
            '//code.jquery.com/jquery-3.6.0.min.js',
            '//cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
            '//cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/i18n/es.js',
            'citas/js/horario_admin.js',  # Archivo para la funcionalidad de dependencia entre médico y especialidad
        )
        css = {
            'all': (
                '//cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
            )
        }
    
    # Configuración del formulario
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'medico', 
                'especialidad', 
                'turno', 
                'activo', 
                'domicilio',
                ('fecha_inicio', 'hora_inicio'),
                ('fecha_fin', 'hora_fin')
            )
        }),
        ('Configuración de Recurrencia (Opcional)', {
            'fields': (
                'recurrence_frequency',
                'recurrence_byday',
                'recurrence_until',
            ),
            'classes': ('wide', 'collapse'),
            'description': 'Define la regla de repetición del horario. Si deja en blanco, será un evento único.'
        }),
        ('Regla de Recurrencia Almacenada', {
            'fields': ('recurrence_rule',),
            'classes': ('collapse',),
        }),
    )
    
    # Métodos para mostrar fechas y horas en la lista
    def get_fecha_inicio(self, obj):
        return obj.start_datetime.strftime('%d/%m/%Y') if obj.start_datetime else '-'
    get_fecha_inicio.short_description = 'Fecha Inicio'
    get_fecha_inicio.admin_order_field = 'start_datetime'

    def get_hora_inicio(self, obj):
        return obj.start_datetime.strftime('%H:%M') if obj.start_datetime else '-'
    get_hora_inicio.short_description = 'Hora Inicio'
    get_hora_inicio.admin_order_field = 'start_datetime'

    def get_fecha_fin(self, obj):
        return obj.end_datetime.strftime('%d/%m/%Y') if obj.end_datetime else '-'
    get_fecha_fin.short_description = 'Fecha Fin'
    get_fecha_fin.admin_order_field = 'end_datetime'

    def get_hora_fin(self, obj):
        return obj.end_datetime.strftime('%H:%M') if obj.end_datetime else '-'
    get_hora_fin.short_description = 'Hora Fin'
    get_hora_fin.admin_order_field = 'end_datetime'
    
    # Botón para ver agenda en la lista
    def ver_agenda_button(self, obj):
        if obj.medico_id:
            try:
                agenda_url = reverse('citas:agenda_medico')
                return mark_safe(
                    f'<a href="{agenda_url}" class="button" style="padding: 5px 10px; background: #417690; color: white; text-decoration: none; border-radius: 3px;">📅 Ver Agenda</a>'
                )
            except Exception as e:
                print(f"Error generando URL de agenda: {e}")
                return "URL no configurada"
        return "-"
    ver_agenda_button.short_description = 'Acciones'
    ver_agenda_button.allow_tags = True
    
    # Cambios en el formulario de edición
    change_form_template = 'citas/agenda/change_form.html'
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        
        if obj and obj.medico_id:
            try:
                agenda_url = reverse('citas:agenda_medico')
                extra_context['agenda_url'] = agenda_url
                extra_context['medico_nombre'] = f"{obj.medico.Nombres_Medico} {obj.medico.Apellidos_Medicos}"
            except Exception as e:
                print(f"Error generando URL de agenda: {e}")
        
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
    
    def get_recurrence_display(self, obj):
        """Muestra la regla de recurrencia de forma legible en la lista."""
        return obj.recurrence_rule if obj.recurrence_rule else 'Evento Único'
    get_recurrence_display.short_description = 'Repetición'

class TurnoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'hora_inicio', 'hora_fin')
    search_fields = ('nombre', 'hora_inicio', 'hora_fin')
    list_filter = ()
    ordering = ('hora_inicio',)
    
    class Media:
        js = (
            '//code.jquery.com/jquery-3.6.0.min.js',
            '//cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
            '//cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/i18n/es.js',
            'citas/js/horario_admin.js',  # Archivo para la funcionalidad de dependencia entre médico y especialidad
        )
        css = {
            'all': (
                '//cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
            )
        }

# ----------------------------------------------------
# 3. DEFINICIONES DE MEDICO (UsuarioMedico) y ESPECIALIDAD
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

# Registrar modelos en el CustomAdminSite (admin_site)
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

# Modelos de Apoyo
admin_site.register(Prefijo_CIDNI)
admin_site.register(Sexo)
admin_site.register(EstadoCivil)

# Registrar modelos con sus respectivas clases de administración
admin_site.register(Turno, TurnoAdmin)
admin_site.register(UsuarioMedico, UsuarioMedicoAdmin)
admin_site.register(EspecialidadMedica, EspecialidadMedicaAdmin)
admin_site.register(MedicoEspecialidad, MedicoEspecialidadAdmin)
admin_site.register(Paciente, PacienteAdmin)
admin_site.register(Consultorio, ConsultorioAdmin)
admin_site.register(Banco, BancoAdmin)

# Importar y registrar el CalendarioAdmin después de definir todos los modelos
#from .admin_calendario import CalendarioAdmin
admin_site.register(Pais, PaisAdmin)
admin_site.register(Estado, EstadoAdmin)
admin_site.register(Ciudad, CiudadAdmin)
admin_site.register(Municipio, MunicipioAdmin)
admin_site.register(Parroquia, ParroquiaAdmin)

# Verificar si el modelo ya está registrado antes de registrarlo
if not admin_site.is_registered(HorarioCita):
   admin_site.register(HorarioCita, HorarioCitaAdmin)

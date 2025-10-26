# citas/forms.py

from django import forms
from django.contrib import admin
from django.db import transaction
from django.utils import timezone
import datetime
from .models import (
    HorarioCita, Paciente, DireccionPaciente, Prefijo_CIDNI, Sexo, 
    EstadoCivil, Pais, Estado, Ciudad, Municipio, Parroquia, Banco,
    EspecialidadMedica, MedicoEspecialidad, UsuarioMedico, DatosSeniat, Consultorio
)

# -------------------------------------------------------------
# CLASES AUXILIARES
# -------------------------------------------------------------

class FieldSeparator(forms.Field):
    """Campo invisible que solo sirve para mostrar un título de sección."""
    def __init__(self, label=None, *args, **kwargs):
        kwargs['required'] = False
        super().__init__(*args, **kwargs)
        # Usamos HiddenInput para que no se muestre como campo de texto
        self.widget = forms.HiddenInput() 

# -------------------------------------------------------------
# FORMULARIO PRINCIPAL (Maneja Paciente + DireccionPaciente)
# -------------------------------------------------------------

class RegistroPacienteForm(forms.ModelForm):
    # Definición de campos de DireccionPaciente (Manually added fields)
    
    # 1. Separador
    separador_datos = FieldSeparator(label='Datos de Contacto y Residencia')

    # 2. Contacto
    celular = forms.CharField(max_length=20, label="Teléfono Móvil")
    correo = forms.EmailField(max_length=200, label="Correo Electrónico")
    telefono = forms.CharField(max_length=20, label="Teléfono Fijo", required=False)
    
    # 3. Ubicación (ModelChoiceField para los dropdowns)
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label="Estado",
        empty_label="Seleccione un estado",
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'data-level': 'estados',
            'data-next-combo': 'id_ciudad'
        }) 
    )

    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.none(),
        label="Ciudad",
        empty_label="Seleccione una ciudad",
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'data-level': 'ciudades', 
            'disabled': True,
            'data-next-combo': 'id_municipio'
        })
    )

    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.none(), 
        label="Municipio",
        empty_label="Seleccione un municipio",
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'data-level': 'municipios', 
            'disabled': True,
            'data-next-combo': 'id_parroquia'
        })
    )

    parroquia = forms.ModelChoiceField(
        queryset=Parroquia.objects.none(), 
        label="Parroquia",
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'disabled': True
        })
    )
    
    # 4. Dirección Completa
    direccion = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Dirección Completa")
    numero_casa = forms.CharField(max_length=50, label="Número de Casa/Apto", required=False)


    class Meta:
        model = Paciente
        # Lista de TODOS los campos (Paciente + DireccionPaciente) para el fieldsets de admin
        fields = [
            'Nombres_Paciente', 'Apellidos_Paciente', 'Prefijo_CIDNI', 'CIDNI', 
            'Fecha_Nacimiento_Paciente', 'Pais', 'Sexo', 'estado_civil_new', 
            
            'separador_datos', # Separador
            
            'celular', 'correo', 'telefono', 
            'estado', 'ciudad', 'municipio', 'parroquia', 
            'direccion', 'numero_casa'
        ]
        widgets = {
            'Fecha_Nacimiento_Paciente': forms.DateInput(attrs={'type': 'date'}),
            
            # CLAVE: Sobrescribir los widgets de Foreign Key para usar Select simple (elimina iconos)
            'Prefijo_CIDNI': forms.Select(), 
            'Sexo': forms.Select(),
            'estado_civil_new': forms.Select(),
            'Pais': forms.Select(),
        }
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Inicializar los querysets de los campos dependientes
        if self.is_bound:  # Si el formulario está siendo enviado
            try:
                # Obtener los IDs de los campos del formulario
                estado_id = self.data.get('estado')
                ciudad_id = self.data.get('ciudad')
                municipio_id = self.data.get('municipio')
                
                # Configurar el queryset de ciudades si hay un estado seleccionado
                if estado_id:
                    estado_id = int(estado_id)
                    self.fields['ciudad'].queryset = Ciudad.objects.filter(estado_id=estado_id).order_by('nombre')
                    self.fields['ciudad'].widget.attrs['disabled'] = False
                    
                    # Configurar el queryset de municipios si hay un estado
                    self.fields['municipio'].queryset = Municipio.objects.filter(estado_id=estado_id).order_by('nombre')
                    self.fields['municipio'].widget.attrs['disabled'] = False
                    
                    # Configurar el queryset de parroquias si hay un municipio seleccionado
                    if municipio_id:
                        municipio_id = int(municipio_id)
                        self.fields['parroquia'].queryset = Parroquia.objects.filter(municipio_id=municipio_id).order_by('nombre')
                        self.fields['parroquia'].widget.attrs['disabled'] = False
                        
            except (ValueError, TypeError) as e:
                print(f"Error al procesar los datos del formulario: {e}")
                pass  # Ignorar errores de conversión
                
        elif self.instance and hasattr(self.instance, 'direccion'):
            # Código para cuando se está editando un registro existente
            direccion = self.instance.direccion
            if direccion.estado:
                self.fields['ciudad'].queryset = Ciudad.objects.filter(estado=direccion.estado).order_by('ciudad')
                self.fields['ciudad'].widget.attrs['disabled'] = False
                self.fields['municipio'].queryset = Municipio.objects.filter(estado=direccion.estado).order_by('municipio')
                self.fields['municipio'].widget.attrs['disabled'] = False
                if direccion.municipio:
                    self.fields['parroquia'].queryset = Parroquia.objects.filter(municipio=direccion.municipio).order_by('parroquia')
                    self.fields['parroquia'].widget.attrs['disabled'] = False

    def clean(self):
        cleaned_data = super().clean()
        
        # Solo validaciones básicas
        if cleaned_data.get('municipio') and not cleaned_data.get('ciudad'):
            self.add_error('ciudad', 'Debe seleccionar una ciudad si ha seleccionado un municipio')
            
        if cleaned_data.get('parroquia') and not cleaned_data.get('municipio'):
            self.add_error('municipio', 'Debe seleccionar un municipio si ha seleccionado una parroquia')
        
        # No convertimos los IDs a objetos, Django se encargará de eso
        
        return cleaned_data
    
    def save(self, commit=True):
        # 1. Guardar el Paciente (Modelo principal)
        try:
            # Asegurarse de que los campos requeridos estén presentes
            required_fields = ['Nombres_Paciente', 'Apellidos_Paciente', 'CIDNI', 'Fecha_Nacimiento_Paciente']
            for field in required_fields:
                if field not in self.cleaned_data or not self.cleaned_data[field]:
                    raise ValueError(f'El campo {field} es requerido')
            
            # Crear o actualizar el paciente
            paciente = super().save(commit=False)
            
            # Asegurar que los campos requeridos del modelo Paciente estén configurados
            if not hasattr(paciente, 'id_Paciente') or not paciente.id_Paciente:
                # Es un nuevo paciente, establecer valores por defecto
                paciente.Fecha_Registro = timezone.now()
                paciente.Activo = True
            
            paciente.Ultima_Actualizacion = timezone.now()
            
            if commit:
                # Guardar el paciente primero
                paciente.save()
                
                # Preparar datos para la dirección
                direccion_data = {
                    'celular': self.cleaned_data.get('celular'),
                    'correo': self.cleaned_data.get('correo'),
                    'telefono': self.cleaned_data.get('telefono', ''),
                    'direccion': self.cleaned_data.get('direccion', ''),
                    'numero_casa': self.cleaned_data.get('numero_casa', ''),
                    'estado': self.cleaned_data.get('estado'),
                    'ciudad': self.cleaned_data.get('ciudad'),
                    'municipio': self.cleaned_data.get('municipio'),
                    'parroquia': self.cleaned_data.get('parroquia'),
                }
                
                # Eliminar valores None para no sobrescribir con None los valores existentes
                direccion_data = {k: v for k, v in direccion_data.items() if v is not None}
                
                try:
                    # Usar update_or_create para manejar tanto creación como actualización
                    direccion, created = DireccionPaciente.objects.update_or_create(
                        paciente=paciente,
                        defaults=direccion_data
                    )
                    
                    # Si se creó una nueva dirección, asignarla al paciente
                    if created:
                        paciente.direccion = direccion
                        if commit:
                            paciente.save()
                    
                except Exception as e:
                    # Si hay un error al guardar la dirección, registrar el error
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f'Error al guardar la dirección del paciente: {str(e)}')
                    
                    # Si estamos en modo debug, relanzar la excepción
                    if settings.DEBUG:
                        raise
            
            return paciente
            
        except Exception as e:
            # Registrar el error
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Error al guardar el paciente: {str(e)}')
            
            # Si estamos en modo debug, relanzar la excepción
            if settings.DEBUG:
                raise
                
            # En producción, devolver un mensaje de error más amigable
            raise forms.ValidationError(f'Error al guardar el paciente: {str(e)}')

class EspecialidadMedicaForm(forms.ModelForm):
    class Meta:
        model = EspecialidadMedica
        fields = ['Espacialidad_Medica']
        labels = {
            'Espacialidad_Medica': 'Nombre de la Especialidad',
        }
        widgets = {
            'Espacialidad_Medica': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UsuarioMedicoForm(forms.ModelForm):
    # Campos adicionales
    telefono = forms.CharField(
        max_length=20, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 04141234567'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
    )
    
    # Campos de ubicación (igual que en RegistroPacienteForm)
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label="Estado",
        empty_label="Seleccione un estado",
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'data-level': 'estados',
            'required': 'required'
        }) 
    )

    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.none(),
        label="Ciudad",
        empty_label="Seleccione una ciudad",
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'data-level': 'ciudades', 
            'disabled': True,
            'required': 'required'
        })
    )

    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.none(), 
        label="Municipio",
        empty_label="Seleccione un municipio",
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'data-level': 'municipios', 
            'disabled': True,
            'required': 'required'
        })
    )

    parroquia = forms.ModelChoiceField(
        queryset=Parroquia.objects.none(), 
        label="Parroquia",
        required=False,
        empty_label="Seleccione una parroquia",
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'disabled': True
        })
    )
    
    class Meta:
        model = UsuarioMedico
        fields = [
            'Nombres_Medico', 'Apellidos_Medicos', 'Prefijo_CIDNI', 'CIDNI',
            'Fecha_Nacimiento_Medico', 'Sexo', 'Registro_MPPS', 
            'Numero_Colegio_de_Medico', 'estado_civil', 'Pais', 'estado',
            'ciudad', 'municipio', 'parroquia', 'Foto_Medico', 'activo',
            'especialidades', 'telefono', 'email'
        ]
        widgets = {
            'Nombres_Medico': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ingrese los nombres del médico',
                'required': 'required'
            }),
            'Apellidos_Medicos': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ingrese los apellidos del médico',
                'required': 'required'
            }),
            'Prefijo_CIDNI': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'CIDNI': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12345678',
                'required': 'required'
            }),
            'Fecha_Nacimiento_Medico': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date',
                'required': 'required'
            }),
            'Sexo': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'Registro_MPPS': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de registro MPPS',
                'required': 'required'
            }),
            'Numero_Colegio_de_Medico': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de colegiado',
                'required': 'required'
            }),
            'estado_civil': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'Pais': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'Foto_Medico': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'especialidades': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'multiple': 'multiple',
                'required': 'required'
            }),
        }

class DatosSeniatForm(forms.ModelForm):
    class Meta:
        model = DatosSeniat
        fields = [
            'RIF', 'Direccion', 'razon_social', 
            'contribuyente_especial', 'nro_licencia'
        ]
        labels = {
            'RIF': 'RIF del Médico',
            'Direccion': 'Dirección Fiscal',
            'razon_social': 'Razón Social',
            'contribuyente_especial': '¿Es Contribuyente Especial?',
            'nro_licencia': 'Número de Licencia'
        }
        widgets = {
            'RIF': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: J-12345678-9',
                'required': 'required'
            }),
            'Direccion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Ingrese la dirección fiscal completa',
                'required': 'required'
            }),
            'razon_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Razón social o nombre de la empresa',
                'required': 'required'
            }),
            'contribuyente_especial': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'nro_licencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de licencia o autorización',
                'required': 'required'
            })
        }

class MedicoEspecialidadForm(forms.ModelForm):
    class Meta:
        model = MedicoEspecialidad
        fields = ['medico', 'especialidad', 'principal', 'activo']
        widgets = {
            'medico': forms.Select(attrs={'class': 'form-control select2'}),
            'especialidad': forms.Select(attrs={'class': 'form-control select2'}),
            'principal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ConsultorioForm(forms.ModelForm):
    class Meta:
        model = Consultorio
        fields = [
            'numero_consultorio', 'Direccion', 'Telefono', 'Celular', 'Correo',
            'Especialidad_Medica', 'estado', 'ciudad', 'municipio', 'parroquia', 'Status'
        ]
        widgets = {
            'Direccion': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'Correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@dominio.com'}),
            'numero_consultorio': forms.TextInput(attrs={'class': 'form-control'}),
            'Telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'Celular': forms.TextInput(attrs={'class': 'form-control'}),
            'Especialidad_Medica': forms.Select(attrs={'class': 'form-control select2'}),
            'estado': forms.Select(attrs={
                'class': 'form-control select2', 
                'id': 'id_estado',
                'data-level': 'estados'
            }),
            'ciudad': forms.Select(attrs={
                'class': 'form-control select2', 
                'id': 'id_ciudad',
                'disabled': True,
                'data-level': 'ciudades'
            }),
            'municipio': forms.Select(attrs={
                'class': 'form-control select2', 
                'id': 'id_municipio',
                'disabled': True,
                'data-level': 'municipios'
            }),
            'parroquia': forms.Select(attrs={
                'class': 'form-control select2', 
                'id': 'id_parroquia',
                'disabled': True,
                'data-level': 'parroquias'
            }),
            'Status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Hacer que los campos de ubicación sean opcionales
        location_fields = ['estado', 'ciudad', 'municipio', 'parroquia']
        for field_name, field in self.fields.items():
            if field_name in location_fields:
                field.required = False
                field.empty_label = 'Seleccione...'
            
            # Configurar placeholders para los campos de texto
            if field_name in ['Direccion', 'Telefono', 'Celular', 'Correo']:
                field.widget.attrs['placeholder'] = field.label
        
        # Si estamos editando, cargamos las opciones correspondientes
        if self.instance and self.instance.pk:
            if self.instance.estado_id:
                self.fields['ciudad'].queryset = Ciudad.objects.filter(estado_id=self.instance.estado_id)
                self.fields['ciudad'].widget.attrs['disabled'] = False
            
            if self.instance.ciudad_id:
                self.fields['municipio'].queryset = Municipio.objects.filter(estado_id=self.instance.estado_id)
                self.fields['municipio'].widget.attrs['disabled'] = False
            if self.instance.municipio_id:
                self.fields['parroquia'].queryset = Parroquia.objects.filter(municipio_id=self.instance.municipio_id)
                self.fields['parroquia'].widget.attrs['disabled'] = False

class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = '__all__'

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
# citas/forms.py

from django import forms
from django.db import transaction
from .models import (
    Paciente, DireccionPaciente, Prefijo_CIDNI, Sexo, 
    EstadoCivil, Pais, Estado, Ciudad, Municipio, Parroquia, Banco
)
from .models import EspecialidadMedica, MedicoEspecialidad, UsuarioMedico, DatosSeniat, Consultorio

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
        widget=forms.Select(attrs={'class': 'form-control', 'data-level': 'estados'}) 
    )

    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.none(),
        label="Ciudad",
        empty_label="Seleccione una ciudad",
        widget=forms.Select(attrs={'class': 'form-control', 'data-level': 'ciudades', 'disabled': True})
    )

    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.none(), 
        label="Municipio",
        empty_label="Seleccione un municipio",
       widget=forms.Select(attrs={'class': 'form-control', 'data-level': 'municipios', 'disabled': True})
    )

    parroquia = forms.ModelChoiceField(
        queryset=Parroquia.objects.none(), 
        label="Parroquia",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'disabled': True})
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
    
    
    def save(self, commit=True):
        # 1. Guardar el Paciente (Modelo principal)
        paciente = super().save(commit=commit)
        
        if commit:
            # 2. Crear o actualizar el registro de DireccionPaciente (asumiendo que es una relación OneToOne)
            DireccionPaciente.objects.update_or_create(
                paciente=paciente,
                defaults={
                    'celular': self.cleaned_data.get('celular'),
                    'correo': self.cleaned_data.get('correo'),
                    'telefono': self.cleaned_data.get('telefono'),
                    'direccion': self.cleaned_data.get('direccion'),
                    'numero_casa': self.cleaned_data.get('numero_casa'),
                    
                    'estado': self.cleaned_data.get('estado'),
                    'ciudad': self.cleaned_data.get('ciudad'),
                    'municipio': self.cleaned_data.get('municipio'),
                    'parroquia': self.cleaned_data.get('parroquia'),
                }
            )
        return paciente

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
        fields = ['Bancos', 'Activo', 'Codigo_Bancario']
        widgets = {
            'Bancos': forms.TextInput(attrs={'class': 'form-control'}),
            'Codigo_Bancario': forms.NumberInput(attrs={'class': 'form-control'}),
            'Activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Paciente(models.Model):
    # Opciones para los campos de elección
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('N', 'No especificado'),
    ]
    
    ESTADO_CIVIL_CHOICES = [
        ('S', 'Soltero/a'),
        ('C', 'Casado/a'),
        ('D', 'Divorciado/a'),
        ('V', 'Viudo/a'),
        ('U', 'Unión libre'),
    ]
    
    TIPO_SANGRE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    # Información personal
    nombre = models.CharField('Nombres', max_length=100)
    apellido = models.CharField('Apellidos', max_length=100)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento')
    genero = models.CharField('Género', max_length=1, choices=GENERO_CHOICES, default='N')
    estado_civil = models.CharField('Estado Civil', max_length=1, choices=ESTADO_CIVIL_CHOICES, blank=True, null=True)
    ocupacion = models.CharField('Ocupación', max_length=100, blank=True, null=True)
    foto = models.ImageField('Fotografía', upload_to='pacientes/fotos/', blank=True, null=True)
    
    # Información de contacto
    telefono = models.CharField('Teléfono', max_length=15)
    email = models.EmailField('Correo Electrónico', blank=True, null=True)
    direccion = models.TextField('Dirección', blank=True, null=True)
    ciudad = models.CharField('Ciudad', max_length=100, blank=True, null=True)
    estado = models.CharField('Estado', max_length=100, blank=True, null=True)
    codigo_postal = models.CharField('Código Postal', max_length=10, blank=True, null=True)
    
    # Información médica
    tipo_sangre = models.CharField('Tipo de Sangre', max_length=3, choices=TIPO_SANGRE_CHOICES, blank=True, null=True)
    alergias = models.TextField('Alergias', blank=True, null=True, help_text='Lista de alergias conocidas')
    medicamentos = models.TextField('Medicamentos', blank=True, null=True, help_text='Medicamentos actuales')
    enfermedades_cronicas = models.TextField('Enfermedades Crónicas', blank=True, null=True)
    
    # Información del seguro
    seguro_medico = models.CharField('Compañía de Seguro', max_length=100, blank=True, null=True)
    numero_seguro = models.CharField('Número de Seguro', max_length=50, blank=True, null=True)
    
    # Contacto de emergencia
    contacto_emergencia = models.CharField('Contacto de Emergencia', max_length=200, blank=True, null=True)
    telefono_emergencia = models.CharField('Teléfono de Emergencia', max_length=15, blank=True, null=True)
    
    # Fechas importantes
    fecha_ingreso = models.DateTimeField('Fecha de Ingreso', auto_now_add=True)
    fecha_egreso = models.DateField('Fecha de Egreso', blank=True, null=True)
    
    # Notas adicionales
    observaciones = models.TextField('Observaciones', blank=True, null=True)
    activo = models.BooleanField('Activo', default=True)
    
    # Campos calculados
    @property
    def edad(self):
        import datetime
        if self.fecha_nacimiento:
            today = datetime.date.today()
            return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return None
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('pacientes_detail', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        # Aquí puedes agregar lógica adicional antes de guardar
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['apellido', 'nombre']
        indexes = [
            models.Index(fields=['apellido', 'nombre']),
            models.Index(fields=['fecha_ingreso']),
        ]

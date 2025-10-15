from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.contrib import messages
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de pacientes
    list_display = (
        'foto_miniatura',
        'nombre_completo',
        'edad',
        'genero',
        'telefono',
        'tipo_sangre',
        'estado',
        'acciones'
    )

    # Campos por los que se puede filtrar
    list_filter = (
        'genero',
        'tipo_sangre',
        'estado_civil',
        'fecha_ingreso',
        'fecha_egreso',
    )

    # Campos por los que se puede buscar
    search_fields = (
        'nombre',
        'apellido',
        'telefono',
        'email',
        'numero_seguro',
    )

    # Campos agrupados en el formulario
    fieldsets = (
        ('Información Personal', {
            'fields': (
                ('foto', 'foto_previa'),
                ('nombre', 'apellido'),
                ('fecha_nacimiento', 'genero', 'estado_civil'),
                'ocupacion',
            )
        }),
        ('Información de Contacto', {
            'fields': (
                'telefono',
                'email',
                ('direccion', 'ciudad'),
                ('estado', 'codigo_postal'),
            )
        }),
        ('Información Médica', {
            'classes': ('collapse',),
            'fields': (
                'tipo_sangre',
                'alergias',
                'medicamentos',
                'enfermedades_cronicas',
            )
        }),
        ('Información del Seguro', {
            'classes': ('collapse',),
            'fields': (
                'seguro_medico',
                'numero_seguro',
                'contacto_emergencia',
                'telefono_emergencia',
            )
        }),
        ('Datos Adicionales', {
            'classes': ('collapse',),
            'fields': (
                'fecha_egreso',
                'observaciones',
                'activo',
            )
        }),
    )

    # Configuración básica
    list_per_page = 20
    date_hierarchy = 'fecha_ingreso'
    ordering = ('-fecha_ingreso', 'apellido', 'nombre')
    readonly_fields = ('fecha_ingreso', 'foto_previa')

    # Métodos auxiliares
    def foto_miniatura(self, obj):
        if obj.foto:
            return mark_safe(f'<img src="{obj.foto.url}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />')
        return ""
    foto_miniatura.short_description = "Foto"

    def foto_previa(self, obj):
        if obj.foto:
            return mark_safe(f'<img src="{obj.foto.url}" width="150" height="150" style="object-fit: cover; border-radius: 5px;" />')
        return "Sin imagen"
    foto_previa.short_description = "Vista previa"

    def nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"
    nombre_completo.short_description = 'Nombre Completo'
    nombre_completo.admin_order_field = 'apellido'

    def acciones(self, obj):
        return format_html(
            '<a class="button" href="{}">Ver</a>&nbsp;'
            '<a class="button" href="{}">Editar</a>',
            reverse('admin:index_paciente_change', args=[obj.id]),
            reverse('admin:index_paciente_change', args=[obj.id])
        )
    acciones.short_description = 'Acciones'
    acciones.allow_tags = True

    # Configuración del formulario
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si es una edición
            return ('fecha_ingreso', 'foto_previa')
        return ('foto_previa',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not obj:  # Si es un nuevo registro, ocultar campos de solo lectura
            fieldsets = list(fieldsets)
            for i, (name, data) in enumerate(fieldsets):
                if 'fields' in data and 'fecha_ingreso' in data['fields']:
                    fields = list(data['fields'])
                    if 'fecha_ingreso' in fields:
                        fields.remove('fecha_ingreso')
                        fieldsets[i] = (name, {**data, 'fields': tuple(fields)})
        return fieldsets

    # Acciones personalizadas
    actions = ['marcar_como_activo', 'marcar_como_inactivo', 'exportar_a_csv']

    def marcar_como_activo(self, request, queryset):
        actualizados = queryset.update(activo=True)
        self.message_user(
            request,
            f"{actualizados} pacientes marcados como activos.",
            messages.SUCCESS
        )
    marcar_como_activo.short_description = "Marcar como activo"

    def marcar_como_inactivo(self, request, queryset):
        actualizados = queryset.update(activo=False)
        self.message_user(
            request,
            f"{actualizados} pacientes marcados como inactivos.",
            messages.WARNING
        )
    marcar_como_inactivo.short_description = "Marcar como inactivo"

    def exportar_a_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        import io

        output = io.StringIO()
        writer = csv.writer(output)

        # Encabezados
        writer.writerow([
            'Nombre', 'Apellido', 'Edad', 'Género', 'Teléfono', 'Email',
            'Fecha de Nacimiento', 'Fecha de Ingreso', 'Fecha de Egreso'
        ])

        # Datos
        for paciente in queryset:
            writer.writerow([
                paciente.nombre,
                paciente.apellido,
                paciente.edad,
                paciente.get_genero_display(),
                paciente.telefono,
                paciente.email,
                paciente.fecha_nacimiento.strftime('%d/%m/%Y') if paciente.fecha_nacimiento else '',
                paciente.fecha_ingreso.strftime('%d/%m/%Y'),
                paciente.fecha_egreso.strftime('%d/%m/%Y') if paciente.fecha_egreso else ''
            ])

        output.seek(0)
        response = HttpResponse(output, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=pacientes_exportados.csv'
        return response
    exportar_a_csv.short_description = "Exportar a CSV"

    # Configuración de estilos CSS/JS
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
        js = ('js/admin_custom.js',)

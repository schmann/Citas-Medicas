from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import CitasReservadas

class CalendarioAdmin(admin.ModelAdmin):
    change_list_template = 'citas/reservas/calendario.html'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('calendario/', self.admin_site.admin_view(self.calendario_view), name='citas_calendario'),
        ]
        return custom_urls + urls
    
    @method_decorator(staff_member_required)
    def calendario_view(self, request):
        # Obtener citas
        hoy = timezone.now()
        citas = CitasReservadas.objects.filter(
            start_datetime__month=hoy.month,
            start_datetime__year=hoy.year
        ).select_related('paciente', 'horario__medico', 'horario__especialidad')
        
        # Formatear eventos para FullCalendar
        eventos = []
        for cita in citas:
            eventos.append({
                'id': cita.id,
                'title': f"{cita.paciente.Nombres_Paciente} - {getattr(cita.horario.especialidad, 'Espacialidad_Medica', 'Sin especialidad')}",
                'start': cita.start_datetime.isoformat(),
                'end': cita.end_datetime.isoformat(),
                'extendedProps': {
                    'paciente': f"{cita.paciente.Nombres_Paciente} {getattr(cita.paciente, 'Apellidos_Paciente', '')}",
                    'medico': f"{cita.horario.medico.Nombres_Medico} {getattr(cita.horario.medico, 'Apellidos_Medicos', '')}",
                    'especialidad': getattr(cita.horario.especialidad, 'Espacialidad_Medica', 'Sin especialidad'),
                    'estado': getattr(cita, 'get_estado_display', lambda: 'No especificado')(),
                    'nota': getattr(cita, 'nota', ''),
                    'costo': float(cita.costo) if hasattr(cita, 'costo') and cita.costo is not None else None,
                    'descripcion': f"Paciente: {cita.paciente}\nMédico: {cita.horario.medico}"
                },
                'backgroundColor': self._get_color_estado(getattr(cita, 'estado', 'pendiente')),
                'borderColor': self._get_border_color(getattr(cita, 'estado', 'pendiente')),
                'textColor': '#ffffff',
                'className': 'fc-event-custom'  # Clase adicional para estilos personalizados
            })
        
        # Serializar los eventos a JSON
        eventos_json = json.dumps(eventos, cls=DjangoJSONEncoder, ensure_ascii=False)
        
        context = {
            **self.admin_site.each_context(request),
            'title': 'Calendario de Citas',
            'opts': self.model._meta,
            'has_permission': True,
            'eventos_json': eventos_json,
            'is_popup': False,
            'save_as': False,
            'save_on_top': False,
            'show_save': False,
            'show_save_as_new': False,
            'show_save_and_add_another': False,
            'show_save_and_continue': False,
        }
        
        return TemplateResponse(request, self.change_list_template, context)
    
    def _get_color_estado(self, estado):
        colores = {
            'pendiente': '#ffc107',  # Amarillo
            'confirmada': '#17a2b8',  # Azul claro
            'completada': '#28a745',  # Verde
            'cancelada': '#dc3545',   # Rojo
            'no_asistio': '#6c757d',  # Gris
        }
        return colores.get(estado.lower(), '#6c757d')
    
    def _get_border_color(self, estado):
        # Puedes personalizar los colores del borde si es necesario
        return self._get_color_estado(estado)

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
    
    @method_decorator(staff_member_required)
  
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

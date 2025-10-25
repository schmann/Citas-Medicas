# citas/views.py
import logging
import traceback

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
import json

from .forms import RegistroPacienteForm
from .models import (
    Ciudad, Municipio, Parroquia, Estado, Pais,
    EspecialidadMedica, HorarioCita, MedicoEspecialidad,
    CitasReservadas, Paciente, UsuarioMedico
)
from .forms import EspecialidadMedicaForm
from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from .models import UsuarioMedico, DatosSeniat, Banco
from .forms import UsuarioMedicoForm, DatosSeniatForm, BancoForm
from .forms import MedicoEspecialidadForm
from .models import MedicoEspecialidad, Banco
from .forms import BancoForm
import datetime 
from django.utils import timezone 
from dateutil import rrule
import pytz
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
from django.core import serializers

# Configuración de Logging
logger = logging.getLogger(__name__)

# -------------------------------------------------------------
# VISTAS PRINCIPALES
# -------------------------------------------------------------

def calendario_nuevo_view(request):
    """
    Vista para el nuevo calendario de citas con interfaz mejorada.
    """
    # Verificar si el usuario está autenticado
    if not request.user.is_authenticated:
        return redirect('admin:login')  # Redirigir al login de admin
    
    # Obtener la lista de especialidades para llenar el combo de filtrado
    especialidades = EspecialidadMedica.objects.all().order_by('Espacialidad_Medica')
    
    # Obtener la lista de médicos para llenar el combo en la modal
    # Aquí cargamos los médicos que tienen especialidades asociadas y están activos.
    medicos_activos = UsuarioMedico.objects.filter(
        usuario__is_active=True,
        medicoespecialidad__isnull=False
    ).distinct().order_by('Apellidos_Medicos', 'Nombres_Medico')
    
    context = {
        'especialidades': especialidades,
        'medicos_activos': medicos_activos,
        'user_is_staff': request.user.is_staff or request.user.is_superuser,
    }
    return render(request, 'citas/calendario_nuevo.html', context)


# -------------------------------------------------------------
# VISTAS PARA OBTENER DATOS VIA AJAX
# -------------------------------------------------------------

@require_http_methods(["GET"])
def obtener_pacientes(request):
    """
    Vista para obtener la lista de pacientes activos en formato JSON.
    """
    try:
        # Filtra pacientes activos y selecciona los campos requeridos
        pacientes = Paciente.objects.filter(Activo=True).values('id', 'Nombres_Paciente', 'Apellidos_Paciente').order_by('Apellidos_Paciente', 'Nombres_Paciente')
        pacientes_list = list(pacientes)
        return JsonResponse({'pacientes': pacientes_list}, status=200)
    except Exception as e:
        logger.error(f"ERROR en obtener_pacientes: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def obtener_medico_especialidad_json(request):
    """
    Devuelve un JSON con la lista de médicos y sus especialidades.
    Se usa para llenar los select en el frontend.
    """
    try:
        # El .distinct('medico') garantiza que cada médico aparezca una sola vez
        medicos_con_especialidades = MedicoEspecialidad.objects.filter(
            medico__usuario__is_active=True # Solo médicos activos
        ).order_by('medico').distinct('medico') 
        
        medicos_list = []
        for me in medicos_con_especialidades:
            # Obtener las especialidades de cada médico
            especialidades = MedicoEspecialidad.objects.filter(medico=me.medico).select_related('especialidad')
            especialidades_str = ", ".join([e.especialidad.Espacialidad_Medica for e in especialidades])

            medicos_list.append({
                'id': me.medico.id,
                'nombre_completo': f"{me.medico.Apellidos_Medicos} {me.medico.Nombres_Medico}",
                'especialidades_str': especialidades_str
            })

        return JsonResponse({'medicos': medicos_list}, safe=False)
    except Exception as e:
        logger.error(f"ERROR en obtener_medico_especialidad_json: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def obtener_horarios_disponibles(request):
    """
    Vista para obtener los horarios de disponibilidad de los médicos.
    """
    try:
        medico_id = request.GET.get('medico_id')
        especialidad_id = request.GET.get('especialidad_id')
        fecha_inicio_str = request.GET.get('start')
        fecha_fin_str = request.GET.get('end')

        if not fecha_inicio_str or not fecha_fin_str:
            return JsonResponse({'error': 'Fechas de inicio y fin son requeridas'}, status=400)
        
        # Convertir a datetime y asegurarse de que estén en UTC si no tienen zona horaria
        # FullCalendar usa ISO 8601, que a menudo está en UTC.
        fecha_inicio = datetime.strptime(fecha_inicio_str.split('T')[0], '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin_str.split('T')[0], '%Y-%m-%d').date()
        
        # 1. Obtener todos los horarios de disponibilidad activos
        horarios_disponibles = HorarioCita.objects.filter(Activo=True)

        if medico_id:
            # Si se selecciona un médico, filtramos solo por él
            horarios_disponibles = horarios_disponibles.filter(medico__id=medico_id)

        # -------------------------------------------------------------------------
        # CORRECCIÓN SOLICITADA: Se elimina el filtro de especialidad para que 
        # el médico (a través de sus horarios) no se restrinja por la especialidad 
        # seleccionada en el combo box, a menos que se haya seleccionado un médico.
        # -------------------------------------------------------------------------
        # if especialidad_id and not medico_id:
        #     horarios_disponibles = horarios_disponibles.filter(especialidad__id=especialidad_id)
        # -------------------------------------------------------------------------

        # 2. Obtener las citas ya reservadas en el rango de fechas
        citas_reservadas = CitasReservadas.objects.filter(
            fecha_hora_inicio__date__gte=fecha_inicio,
            fecha_hora_inicio__date__lte=fecha_fin,
            horario__Activo=True,
        ).exclude(estado__in=['cancelada', 'no_asistio']) # Excluir estados que liberan el slot

        # Si se seleccionó un médico, filtrar las citas reservadas por ese médico
        if medico_id:
             citas_reservadas = citas_reservadas.filter(horario__medico__id=medico_id)
        
        eventos = []
        zona_horaria_medico = pytz.timezone('America/Caracas') # Asumiendo la zona horaria del sistema o del médico

        # 3. Procesar horarios recurrentes (FullCalendar no maneja recurrencia simple, generamos las fechas)
        for horario in horarios_disponibles:
            # Lógica para manejar la recurrencia RRule. 
            # Esto debe ser refinado para usar timezone de Django/Pyzt.
            
            # Convertir la hora de inicio y fin al formato requerido por FullCalendar
            time_start = horario.hora_inicio
            time_end = horario.hora_fin
            
            # Crear una regla de recurrencia que va desde la fecha de inicio del horario
            # hasta la fecha de fin del rango visible en el calendario.
            regla = rrule.rrule(
                rrule.DAILY, 
                dtstart=datetime.datetime.combine(horario.fecha_inicio, time_start, tzinfo=zona_horaria_medico),
                until=datetime.datetime.combine(fecha_fin, datetime.time(23, 59, 59), tzinfo=zona_horaria_medico),
                interval=horario.intervalo_dias,
                byweekday=horario.get_dias_semana_rrule() # Método a definir en el modelo para obtener BYDAY
            )
            
            # El límite inferior para la generación es la fecha de inicio del calendario
            fecha_limite_inferior = datetime.datetime.combine(fecha_inicio, datetime.time(0, 0, 0), tzinfo=zona_horaria_medico)

            for dt in regla:
                # Si la fecha generada está dentro del rango visible del calendario
                if dt >= fecha_limite_inferior and dt.date() <= fecha_fin:
                    fecha_inicio_slot = dt.date()
                    
                    # Calcular la hora de fin del slot
                    dt_end = dt.replace(hour=time_end.hour, minute=time_end.minute, second=time_end.second)
                    
                    # Combinar fecha y hora para la comparación
                    dt_inicio_slot = zona_horaria_medico.localize(datetime.datetime.combine(fecha_inicio_slot, time_start))
                    dt_fin_slot = zona_horaria_medico.localize(datetime.datetime.combine(fecha_inicio_slot, time_end))

                    # 4. Verificar si hay citas reservadas en este slot
                    citas_en_slot = citas_reservadas.filter(
                        horario=horario,
                        fecha_hora_inicio=dt_inicio_slot,
                        fecha_hora_fin=dt_fin_slot
                    ).count()
                    
                    # Si no hay citas reservadas, es un slot disponible
                    if citas_en_slot == 0:
                        eventos.append({
                            'title': 'Disponible',
                            'start': dt_inicio_slot.isoformat(),
                            'end': dt_fin_slot.isoformat(),
                            'resourceId': horario.medico.id, 
                            'extendedProps': {
                                'medico_id': horario.medico.id,
                                'medico': f"{horario.medico.Nombres_Medico} {horario.medico.Apellidos_Medicos}",
                                'especialidad': horario.especialidad.Espacialidad_Medica if horario.especialidad else 'General',
                                'horario_id': horario.id,
                                'tipo': 'disponibilidad'
                            },
                            'classNames': ['disponible-slot'],
                            'backgroundColor': '#e8f5e9', # Fondo verde claro
                            'borderColor': '#1b5e20',
                            'editable': False, # No se edita desde FullCalendar
                        })

        # 5. Agregar las citas reservadas como eventos fijos
        for cita in citas_reservadas:
            # Asegurar que las fechas estén en la zona horaria correcta
            start_local = cita.fecha_hora_inicio.astimezone(zona_horaria_medico)
            end_local = cita.fecha_hora_fin.astimezone(zona_horaria_medico)
            
            eventos.append({
                'title': f"Cita - {cita.paciente.Nombres_Paciente} {cita.paciente.Apellidos_Paciente}",
                'start': start_local.isoformat(),
                'end': end_local.isoformat(),
                'resourceId': cita.horario.medico.id,
                'extendedProps': {
                    'tipo': 'cita',
                    'estado': cita.estado,
                    'medico_id': cita.horario.medico.id,
                    'medico': f"{cita.horario.medico.Nombres_Medico} {cita.horario.medico.Apellidos_Medicos}",
                    'especialidad': cita.horario.especialidad.Espacialidad_Medica if cita.horario.especialidad else '',
                    'paciente': f"{cita.paciente.Nombres_Paciente} {cita.paciente.Apellidos_Paciente}",
                    'notas': cita.nota,
                    'cita_id': cita.id
                },
                'classNames': get_clase_estado(cita.estado)
            })
        
        # No necesitamos la llamada adicional a obtener_horarios_recurrentes
        # ya que ya hemos procesado los horarios recurrentes al inicio
        
        print(f"DEBUG - Total eventos a devolver: {len(eventos)}")
        return JsonResponse(eventos, safe=False)
        
    except Exception as e:
        print(f"ERROR en obtener_citas_y_disponibilidad: {str(e)}")
        # Imprimir traceback para depuración en el servidor
        logger.error("Traceback completo:", exc_info=True)
        return JsonResponse({'error': f"Error interno del servidor: {str(e)}"}, status=500)

# Funciones auxiliares para colores y clases
def get_color_estado(estado):
    """Devuelve el color según el estado de la cita"""
    colores = {
        'pendiente': '#ffc107',      # Amarillo
        'confirmada': '#28a745',     # Verde
        'completada': '#17
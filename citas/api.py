from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import UsuarioMedico, HorarioCita, CitasReservadas, EspecialidadMedica

@csrf_exempt
@require_http_methods(["GET"])
def medicos_por_especialidad(request):
    """
    API para obtener la lista de médicos por especialidad
    """
    especialidad_id = request.GET.get('especialidad_id')
    
    if not especialidad_id:
        return JsonResponse({'error': 'Se requiere el parámetro especialidad_id'}, status=400)
    
    try:
        # Obtener los médicos que tienen la especialidad seleccionada
        medicos = UsuarioMedico.objects.filter(
            especialidades__id_Especialidad_Medica=especialidad_id,
            activo=True
        ).distinct()
        
        # Formatear la respuesta
        medicos_data = [{
            'id_Medico': medico.id_Medico,
            'Nombres_Medico': medico.Nombres_Medico,
            'Apellidos_Medicos': medico.Apellidos_Medicos,
            'especialidades': [{
                'id': esp.id_Especialidad_Medica,
                'nombre': esp.Espacialidad_Medica
            } for esp in medico.especialidades.all()]
        } for medico in medicos]
        
        return JsonResponse({
            'success': True,
            'medicos': medicos_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def disponibilidad_medico(request):
    """
    API para obtener la disponibilidad de un médico en un rango de fechas
    """
    medico_id = request.GET.get('medico_id')
    start_str = request.GET.get('start')
    end_str = request.GET.get('end')
    
    if not medico_id or not start_str or not end_str:
        return JsonResponse({
            'success': False,
            'error': 'Se requieren los parámetros medico_id, start y end'
        }, status=400)
    
    try:
        # Convertir las fechas de string a objetos datetime
        start_date = timezone.make_aware(datetime.strptime(start_str, '%Y-%m-%dT%H:%M:%S%z'))
        end_date = timezone.make_aware(datetime.strptime(end_str, '%Y-%m-%dT%H:%M:%S%z'))
        
        # Obtener el médico
        try:
            medico = UsuarioMedico.objects.get(id_Medico=medico_id, activo=True)
        except UsuarioMedico.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Médico no encontrado o inactivo'
            }, status=404)
        
        # Obtener los horarios del médico
        horarios = HorarioCita.objects.filter(
            medico=medico,
            activo=True,
            dia_semana__in=[start_date.weekday() for start_date in [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]]
        )
        
        # Obtener las citas ya reservadas
        citas_reservadas = CitasReservadas.objects.filter(
            horario__medico=medico,
            start_datetime__lt=end_date,
            end_datetime__gt=start_date,
            estado__in=['pendiente', 'confirmada']
        )
        
        # Generar slots de disponibilidad
        disponibilidad = []
        current_date = start_date
        
        while current_date < end_date:
            # Verificar si es un día laborable del médico
            dia_semana = current_date.weekday()
            horarios_dia = [h for h in horarios if h.dia_semana == dia_semana]
            
            for horario in horarios_dia:
                # Calcular la hora de inicio y fin para este día
                hora_inicio = current_date.replace(
                    hour=horario.hora_inicio.hour,
                    minute=horario.hora_inicio.minute,
                    second=0,
                    microsecond=0
                )
                
                hora_fin = current_date.replace(
                    hour=horario.hora_fin.hour,
                    minute=horario.hora_fin.minute,
                    second=0,
                    microsecond=0
                )
                
                # Generar slots de 30 minutos
                slot_inicio = hora_inicio
                while slot_inicio + timedelta(minutes=30) <= hora_fin:
                    slot_fin = slot_inicio + timedelta(minutes=30)
                    
                    # Verificar si el slot está disponible (no hay citas en ese horario)
                    disponible = not any(
                        not (cita.end_datetime <= slot_inicio or cita.start_datetime >= slot_fin)
                        for cita in citas_reservadas
                    )
                    
                    # Solo agregar slots futuros
                    if slot_inicio > timezone.now():
                        disponibilidad.append({
                            'title': 'Disponible' if disponible else 'No disponible',
                            'start': slot_inicio.isoformat(),
                            'end': slot_fin.isoformat(),
                            'disponible': disponible,
                            'medico_id': medico.id_Medico,
                            'backgroundColor': '#28a745' if disponible else '#dc3545',
                            'borderColor': '#28a745' if disponible else '#dc3545',
                            'textColor': 'white'
                        })
                    
                    slot_inicio = slot_fin
            
            current_date += timedelta(days=1)
        
        return JsonResponse({
            'success': True,
            'disponibilidad': disponibilidad
        })
        
    except Exception as e:
        import traceback
        return JsonResponse({
            'success': False,
            'error': str(e),
            'trace': traceback.format_exc()
        }, status=500)

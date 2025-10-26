from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, date, time, timedelta
import json

from .models import EspecialidadMedica, UsuarioMedico, CitasReservadas, HorarioCita, Paciente


# ---------------------------------------------------------------------
# 🔹 VISTA PRINCIPAL: CREAR CITA (renderiza el calendario y formulario)
# ---------------------------------------------------------------------
@csrf_exempt
def crear_cita(request):
    """
    Muestra el formulario para crear una nueva cita médica,
    junto con la disponibilidad del médico seleccionada.
    """
    especialidades = EspecialidadMedica.objects.filter(activo=True).order_by('Espacialidad_Medica')

    paciente_id = request.GET.get('paciente_id')
    paciente = None
    if paciente_id:
        try:
            paciente = Paciente.objects.get(id_Paciente=paciente_id)
        except Paciente.DoesNotExist:
            messages.warning(request, 'El paciente especificado no existe.')

    especialidad_id = request.GET.get('especialidad_id')
    medico_id = request.GET.get('medico_id')

    medicos = UsuarioMedico.objects.none()
    especialidad = medico = None

    if especialidad_id:
        try:
            especialidad = EspecialidadMedica.objects.get(id_Especialidad_Medica=especialidad_id)
            medicos = UsuarioMedico.objects.filter(
                medicoespecialidad__especialidad=especialidad,
                activo=True
            ).distinct().order_by('Apellidos_Medicos', 'Nombres_Medico')
            if medico_id:
                medico = UsuarioMedico.objects.filter(id_Medico=medico_id, activo=True).first()
        except EspecialidadMedica.DoesNotExist:
            messages.warning(request, 'La especialidad seleccionada no existe.')

    # Petición AJAX para cargar médicos (Select dinámico)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if especialidad_id:
            medicos_data = [
                {'id': m.id_Medico, 'text': f"{m.Apellidos_Medicos}, {m.Nombres_Medico}"}
                for m in medicos
            ]
            return JsonResponse({'success': True, 'medicos': medicos_data})
        return JsonResponse({'success': False, 'error': 'No se especificó la especialidad'}, status=400)

    context = {
        'especialidades': especialidades,
        'medicos': medicos,
        'paciente': paciente,
        'especialidad_seleccionada': especialidad,
        'medico_seleccionado': medico,
        'fecha_actual': timezone.now().date(),
    }

    return render(request, 'citas/crear_cita.html', context)


# ---------------------------------------------------------------------
# 🔹 API: DISPONIBILIDAD DE UN MÉDICO
# ---------------------------------------------------------------------
@csrf_exempt
def disponibilidad_medico(request):
    """
    Devuelve la disponibilidad del médico (horarios libres) en formato JSON.
    """
    if request.method != 'GET':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    medico_id = request.GET.get('medico_id')
    especialidad_id = request.GET.get('especialidad_id')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if not all([medico_id, especialidad_id, fecha_inicio, fecha_fin]):
        return JsonResponse({
            'success': False,
            'error': 'Faltan parámetros requeridos'
        }, status=400)

    try:
        medico = UsuarioMedico.objects.get(id_Medico=medico_id, activo=True)
        especialidad = EspecialidadMedica.objects.get(id_Especialidad_Medica=especialidad_id)
    except UsuarioMedico.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Médico no encontrado'}, status=404)
    except EspecialidadMedica.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Especialidad no encontrada'}, status=404)

    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Formato de fecha inválido'}, status=400)

    # Obtener horarios configurados
    horarios = HorarioCita.objects.filter(
        medico_id=medico_id,
        especialidad_id=especialidad_id,
        activo=True
    ).select_related('medico', 'especialidad')

    if not horarios.exists():
        return JsonResponse({
            'success': True,
            'disponibilidad': {},
            'mensaje': 'No hay horarios configurados para este médico y especialidad.'
        })

    # Citas reservadas dentro del rango
    inicio = timezone.make_aware(datetime.combine(fecha_inicio_dt, time.min))
    fin = timezone.make_aware(datetime.combine(fecha_fin_dt + timedelta(days=1), time.min))
    citas_reservadas = CitasReservadas.objects.filter(
        horario__medico_id=medico_id,
        horario__especialidad_id=especialidad_id,
        start_datetime__lt=fin,
        end_datetime__gt=inicio,
        estado__in=['pendiente', 'confirmada']
    )

    # Agrupar citas reservadas por fecha/hora
    citas_ocupadas = {
        c.start_datetime.strftime('%Y-%m-%d %H:%M'): True for c in citas_reservadas
    }

    disponibilidad = {}
    tz = timezone.get_current_timezone()

    for horario in horarios:
        start = horario.start_datetime
        end = horario.end_datetime
        current = start
        while current < end:
            fecha_str = current.astimezone(tz).strftime('%Y-%m-%d')
            hora_inicio = current.astimezone(tz).strftime('%H:%M')
            hora_fin = (current + timedelta(minutes=30)).astimezone(tz).strftime('%H:%M')

            key = f"{fecha_str} {hora_inicio}"
            ocupado = key in citas_ocupadas

            slot = {
                'hora_inicio': hora_inicio,
                'hora_fin': hora_fin,
                'disponible': not ocupado,
            }

            disponibilidad.setdefault(fecha_str, []).append(slot)
            current += timedelta(minutes=30)

    return JsonResponse({'success': True, 'disponibilidad': disponibilidad})


# ---------------------------------------------------------------------
# 🔹 API: GUARDAR CITA
# ---------------------------------------------------------------------
@csrf_exempt
def guardar_cita(request):
    """
    Guarda una nueva cita enviada desde el calendario.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        required_fields = ['paciente_id', 'medico_id', 'especialidad_id', 'fecha', 'hora']
        if not all(data.get(f) for f in required_fields):
            return JsonResponse({'success': False, 'error': 'Faltan campos requeridos'}, status=400)

        paciente = Paciente.objects.get(id_Paciente=data['paciente_id'])
        medico = UsuarioMedico.objects.get(id_Medico=data['medico_id'], activo=True)
        especialidad = EspecialidadMedica.objects.get(id_Especialidad_Medica=data['especialidad_id'])

        fecha_hora = datetime.strptime(f"{data['fecha']} {data['hora']}", "%Y-%m-%d %H:%M")
        fecha_hora_fin = fecha_hora + timedelta(minutes=int(data.get('duracion', 30)))

        cita = CitasReservadas.objects.create(
            paciente=paciente,
            medico=medico,
            especialidad=especialidad,
            start_datetime=timezone.make_aware(fecha_hora),
            end_datetime=timezone.make_aware(fecha_hora_fin),
            estado='pendiente',
            notas=data.get('notas', '')
        )

        return JsonResponse({'success': True, 'message': 'Cita creada exitosamente', 'cita_id': cita.id})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

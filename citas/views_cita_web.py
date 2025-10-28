#crear_vista.html

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from zoneinfo import ZoneInfo
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from datetime import datetime, date, time, timedelta, timezone as dt_timezone
from dateutil.rrule import rruleset, rrulestr, MO, TU, WE, TH, FR, SA, SU # Importar días rrule
from dateutil.relativedelta import relativedelta
import json
import traceback
import pytz

# Importar modelos desde el directorio principal de la aplicación citas
from citas.models import EspecialidadMedica, UsuarioMedico, CitasReservadas, HorarioCita, Paciente, DireccionPaciente
from citas.forms import RegistroPacienteForm

# Importar JsonResponse
from django.urls import reverse
from django.db import transaction

# Mapeo de días BYDAY a weekday de Python (0=Lunes, 6=Domingo)
RRULE_WEEKDAY_MAP = {
    'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3,
    'FR': 4, 'SA': 5, 'SU': 6
}

# Función auxiliar para parsear la regla de recurrencia y obtener días de la semana
def registrar_paciente(request):
    print("\n=== INICIO DE LA SOLICITUD REGISTRAR_PACIENTE ===")
    print(f"Método de la solicitud: {request.method}")
    print(f"¿Es AJAX? {request.headers.get('X-Requested-With') == 'XMLHttpRequest'}")
    
    # Inicializar el formulario fuera del bloque if para que esté disponible en todo el ámbito
    form = RegistroPacienteForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST':
        print("\n=== DATOS POST RECIBIDOS ===")
        # Imprimir todos los datos POST para depuración
        print("Datos POST:")
        for key, value in request.POST.items():
            print(f"  {key}: {value}")
        
        # Verificar si hay archivos en la solicitud
        print("\n=== ARCHIVOS EN LA SOLICITÚD ===")
        print(f"Número de archivos: {len(request.FILES) if hasattr(request, 'FILES') else 0}")
        
        # Crear una copia mutable de request.POST
        post_data = request.POST.copy()
        
        print("\n=== CAMPOS REQUERIDOS ===")
        print("Campos requeridos:", [name for name, field in form.fields.items() if field.required])
        
        # ✅ SOLUCIÓN: CONVERTIR CAMPOS DE UBICACIÓN A ENTEROS
        ubicacion_fields = ['pais', 'estado', 'ciudad', 'municipio', 'parroquia']
        for field in ubicacion_fields:
            if field in post_data:
                print(f"Procesando campo {field}: {post_data[field]}")
                if post_data[field]:
                    try:
                        # Convertir a entero
                        post_data[field] = int(post_data[field])
                        print(f"✅ Convertido {field} a entero: {post_data[field]}")
                    except (ValueError, TypeError):
                        print(f"❌ No se pudo convertir {field}, estableciendo a None")
                        post_data[field] = None
                else:
                    post_data[field] = None
                    print(f"⚠️ Campo {field} vacío, establecido a None")
        
        # Mostrar los datos procesados
        print("\n=== DATOS PROCESADOS PARA EL FORMULARIO ===")
        for key, value in post_data.items():
            print(f"{key}: {value} (tipo: {type(value).__name__})")
        
        # Inicializar el formulario con los datos
        form = RegistroPacienteForm(post_data, request.FILES if hasattr(request, 'FILES') else None)
        
        # Verificar si el formulario es válido
        print(f"\n=== VALIDACIÓN DEL FORMULARIO ===")
        is_valid = form.is_valid()
        print(f"Formulario válido: {is_valid}")
        
        # Mostrar datos limpios si el formulario es válido
        if is_valid:
            print("\n=== DATOS LIMPIOS DEL FORMULARIO ===")
            for field, value in form.cleaned_data.items():
                print(f"{field}: {value}")
        else:
            print("\n=== ERRORES DE VALIDACIÓN ===")
            for field, errors in form.errors.items():
                field_label = form.fields[field].label if field in form.fields else field
                print(f"- {field_label}: {', '.join(errors)}")
        
        if is_valid:
            try:
                with transaction.atomic():
                    # Guardar el paciente sin commit para manejar la dirección manualmente
                    paciente = form.save(commit=False)
                    
                    # Guardar el paciente primero para obtener un ID
                    paciente.save()
                    
                    # Obtener las instancias de los modelos relacionados
                    from citas.models import Pais, Estado, Ciudad, Municipio, Parroquia, DireccionPaciente
                    
                    try:
                        # Obtener las instancias de los modelos relacionados
                        estado = Estado.objects.get(pk=post_data.get('estado')) if post_data.get('estado') else None
                        ciudad = Ciudad.objects.get(pk=post_data.get('ciudad')) if post_data.get('ciudad') else None
                        municipio = Municipio.objects.get(pk=post_data.get('municipio')) if post_data.get('municipio') else None
                        parroquia = Parroquia.objects.get(pk=post_data.get('parroquia')) if post_data.get('parroquia') else None
                        
                        # Preparar los datos de la dirección según el modelo
                        direccion_data = {
                            'paciente': paciente,  # Asignar el paciente recién creado
                            'estado': estado,
                            'ciudad': ciudad,
                            'municipio': municipio,
                            'parroquia': parroquia,
                            'direccion': post_data.get('direccion', 'Sin dirección especificada'),
                            'telefono': post_data.get('telefono', ''),
                            'celular': post_data.get('celular', post_data.get('telefono', '')),
                            'correo': post_data.get('correo', ''),
                            'numero_casa': post_data.get('numero_casa', ''),
                        }
                        
                        # Asegurar que la dirección tenga un valor
                        if not direccion_data.get('direccion'):
                            direccion_data['direccion'] = 'Sin dirección especificada'
                            
                    except Exception as e:
                        print(f"Error al obtener datos de ubicación: {str(e)}")
                        return JsonResponse({
                            'success': False,
                            'message': f'Error al procesar la ubicación: {str(e)}'
                        }, status=400)
                    
                    # Crear o actualizar la dirección
                    from citas.models import DireccionPaciente
                    
                    if hasattr(paciente, 'direccion') and paciente.direccion:
                        # Actualizar dirección existente
                        direccion = paciente.direccion
                        for key, value in direccion_data.items():
                            if hasattr(direccion, key):
                                setattr(direccion, key, value)
                        direccion.save()
                    else:
                        # Crear nueva dirección
                        direccion = DireccionPaciente(**direccion_data)
                        direccion.save()
                        paciente.direccion = direccion
                        paciente.save()
                    
                    print(f"ID del paciente: {getattr(paciente, 'id_Paciente', 'N/A')}")
                    print("\n=== DIRECCIÓN DEL PACIENTE ===")
                    print(f"ID de dirección: {getattr(direccion, 'id_Direccion_Paciente', 'Ninguna')}")
                    print(f"Dirección: {getattr(direccion, 'direccion', 'No especificada')}")
                    
                    # Construir la URL de redirección a la página de solicitud de cita con el ID del paciente
                    from django.urls import reverse
                    redirect_url = f"/citas/?paciente_id={paciente.id_Paciente}"  # URL directa con el ID del paciente página de solicitud de cita
                    
                    # Si es una petición AJAX, devolver JSON
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': True,
                            'message': 'Paciente registrado exitosamente',
                            'paciente_id': paciente.id_Paciente,
                            'nombre_completo': f"{paciente.Nombres_Paciente} {paciente.Apellidos_Paciente}",
                            'cedula': paciente.CIDNI,
                            'redirect_url': redirect_url  # Agregar la URL de redirección
                        })
                    
                    # Si no es AJAX, redirigir a la página de éxito
                    messages.success(request, 'Paciente registrado exitosamente')
                    return redirect('citas:home')
            except Exception as e:
                print(f"\n=== ERROR AL GUARDAR EL PACIENTE ===")
                print(f"Tipo de error: {type(e).__name__}")
                print(f"Mensaje: {str(e)}")
                print("\nTraceback completo:")
                import traceback
                traceback.print_exc()
                
                # Si es AJAX, devolver error en JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': f'Error al procesar el formulario: {str(e)}',
                        'errors': form.errors
                    }, status=400)
                
                # Si no es AJAX, volver a mostrar el formulario con errores
                messages.error(request, f'Error al procesar el formulario: {str(e)}')
        else:
            # Si el formulario no es válido, devolver los errores
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Por favor corrija los errores del formulario',
                    'errors': form.errors
                }, status=400)
    else:
        # Si es GET, mostrar el formulario vacío
        form = RegistroPacienteForm()
    
    # Si llegamos aquí, mostrar el formulario (ya sea vacío o con errores)
    return render(request, 'citas/cita_web/registro.html', {
        'form': form,
        'titulo': 'Registro de Paciente'
    })

def get_especialidades_medico(request, medico_id):
    """
    Obtiene todas las especialidades asignadas a un médico específico.
    Retorna tanto especialidades activas como inactivas para que el frontend filtre.
    """
    from django.http import JsonResponse
    from citas.models import UsuarioMedico, MedicoEspecialidad
    import traceback
    
    print(f"[DEBUG] get_especialidades_medico - Iniciando para médico_id: {medico_id}")
    
    try:
        # Verificar que el médico existe
        if not UsuarioMedico.objects.filter(id_Medico=medico_id).exists():
            print(f"[DEBUG] Médico con ID {medico_id} no encontrado")
            return JsonResponse({
                'success': False,
                'error': f'Médico con ID {medico_id} no encontrado',
                'especialidades': []
            }, status=404)
            
        # Obtener todas las especialidades del médico con la relación
        especialidades_medico = MedicoEspecialidad.objects.filter(
            medico_id=medico_id
        ).select_related('especialidad').order_by('especialidad__Espacialidad_Medica')
        
        if not especialidades_medico.exists():
            print(f"[DEBUG] No se encontraron especialidades para el médico {medico_id}")
            return JsonResponse({
                'success': True,
                'especialidades': [],
                'advertencia': 'El médico no tiene especialidades asignadas',
                'debug': {
                    'medico_id': medico_id,
                    'query': str(especialidades_medico.query)
                }
            })
        
        # Crear la lista de especialidades con el formato correcto
        especialidades_list = []
        for me in especialidades_medico:
            especialidad_data = {
                'id': me.especialidad.id_Especialidad_Medica,
                'nombre': me.especialidad.Espacialidad_Medica,
                'activo': me.activo
            }
            especialidades_list.append(especialidad_data)
            print(f"[DEBUG] Agregando especialidad: {especialidad_data}")
        
        print(f"[DEBUG] Total de especialidades encontradas: {len(especialidades_list)}")
        
        # Retornar las especialidades
        response_data = {
            'success': True,
            'especialidades': especialidades_list,
            'total': len(especialidades_list),
            'debug': {
                'medico_id': medico_id,
                'especialidades_count': len(especialidades_list)
            }
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        error_msg = str(e)
        trace = traceback.format_exc()
        print(f"[ERROR] Error en get_especialidades_medico: {error_msg}")
        print(f"[TRACE] {trace}")
        
        return JsonResponse({
            'success': False,
            'error': 'Error al obtener las especialidades del médico',
            'detalle': error_msg,
            'trace': trace if hasattr(request.user, 'is_staff') and request.user.is_staff else None
        }, status=500)

def get_rrule_days(recurrence_rule):
    dias_laborales = []
    if recurrence_rule:
        try:
            rrule_parts = recurrence_rule.split(';')
            byday_part = next((p for p in rrule_parts if p.startswith('BYDAY=')), None)
            if byday_part:
                dias_laborales_abbr = byday_part.split('=')[1].split(',')
                dias_laborales = [RRULE_WEEKDAY_MAP[abbr] for abbr in dias_laborales_abbr if abbr in RRULE_WEEKDAY_MAP]
        except Exception as e:
            print(f"Error al parsear regla de recurrencia: {e}")
    return dias_laborales

def obtener_horas_disponibles(request, medico_id, especialidad_id, fecha):
    """
    Obtiene las horas disponibles para un médico, especialidad y fecha específicos.
    """
    from django.http import JsonResponse
    from django.utils import timezone
    from datetime import datetime, time, timedelta
    import pytz
    
    try:
        # Validar parámetros
        if not all([medico_id, especialidad_id, fecha]):
            return JsonResponse({
                'success': False,
                'error': 'Faltan parámetros requeridos',
                'horas_disponibles': []
            }, status=400)
        
        # Convertir la fecha de string a objeto date
        try:
            fecha_consulta = datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({
                'success': False,
                'error': 'Formato de fecha inválido. Use YYYY-MM-DD',
                'horas_disponibles': []
            }, status=400)
        
        # Obtener el día de la semana (0=Lunes, 6=Domingo)
        dia_semana = fecha_consulta.weekday()
        
        # Obtener el horario del médico para ese día
        from citas.models import HorarioCita, CitasReservadas, UsuarioMedico, MedicoEspecialidad
        
        # Verificar que el médico existe
        try:
            medico = UsuarioMedico.objects.get(id_Medico=medico_id)
        except UsuarioMedico.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Médico no encontrado',
                'horas_disponibles': []
            }, status=404)
        
        # Verificar que la especialidad existe y está asignada al médico
        try:
            medico_especialidad = MedicoEspecialidad.objects.get(
                medico_id=medico_id,
                especialidad_id=especialidad_id,
                activo=True
            )
        except MedicoEspecialidad.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Especialidad no encontrada o no asignada al médico',
                'horas_disponibles': []
            }, status=404)
        
        # Obtener el horario para el día de la semana
        horarios = HorarioCita.objects.filter(
            medico_id=medico_id,
            dia_semana=dia_semana,
            activo=True
        )
        
        if not horarios.exists():
            return JsonResponse({
                'success': True,
                'horas_disponibles': [],
                'mensaje': 'No hay horario disponible para este día',
                'debug': {
                    'medico_id': medico_id,
                    'especialidad_id': especialidad_id,
                    'fecha': fecha,
                    'dia_semana': dia_semana
                }
            })
        
        # Obtener las citas ya agendadas para esta fecha
        fecha_inicio = datetime.combine(fecha_consulta, time.min)
        fecha_fin = datetime.combine(fecha_consulta, time.max)
        
        citas_agendadas = CitasReservadas.objects.filter(
            medico_id=medico_id,
            fecha_hora__gte=fecha_inicio,
            fecha_hora__lte=fecha_fin,
            estado__in=['PENDIENTE', 'CONFIRMADA']
        ).values_list('fecha_hora', flat=True)
        
        # Convertir a la zona horaria del servidor para comparación
        tz = timezone.get_current_timezone()
        ahora = timezone.now()
        
        # Generar horas disponibles
        horas_disponibles = []
        
        for horario in horarios:
            hora_actual = datetime.combine(fecha_consulta, horario.hora_inicio)
            hora_fin = datetime.combine(fecha_consulta, horario.hora_fin)
            
            # Ajustar a la zona horaria usando timezone.make_aware
            hora_actual = timezone.make_aware(hora_actual, timezone=tz)
            hora_fin = timezone.make_aware(hora_fin, timezone=tz)
            
            # Si la hora actual es anterior a ahora, comenzar desde ahora + 1 hora
            if hora_actual < ahora:
                hora_actual = ahora.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            
            # Si después de ajustar, la hora actual es mayor a la hora de fin, continuar
            if hora_actual >= hora_fin:
                continue
                
            # Generar slots de tiempo según la duración de la cita
            while hora_actual + timedelta(minutes=medico_especialidad.duracion_cita) <= hora_fin:
                slot_fin = hora_actual + timedelta(minutes=medico_especialidad.duracion_cita)
                
                # Verificar si el slot está disponible (no hay citas agendadas en ese horario)
                slot_disponible = True
                
                for cita_hora in citas_agendadas:
                    cita_inicio = cita_hora
                    cita_fin = cita_inicio + timedelta(minutes=medico_especialidad.duracion_cita)
                    
                    # Verificar superposición de horarios
                    if (hora_actual < cita_fin and slot_fin > cita_inicio):
                        slot_disponible = False
                        break
                
                if slot_disponible:
                    horas_disponibles.append({
                        'hora_inicio': hora_actual.astimezone(tz).strftime('%H:%M'),
                        'hora_fin': slot_fin.astimezone(tz).strftime('%H:%M'),
                        'fecha': fecha_consulta.strftime('%Y-%m-%d'),
                        'timestamp': int(hora_actual.timestamp())
                    })
                
                # Mover al siguiente slot (intervalo de la duración de la cita)
                hora_actual = slot_fin
        
        return JsonResponse({
            'success': True,
            'horas_disponibles': horas_disponibles,
            'total': len(horas_disponibles),
            'medico': {
                'id': medico.id_Medico,
                'nombre_completo': f"{medico.user.first_name} {medico.user.last_name}".strip()
            },
            'especialidad': {
                'id': medico_especialidad.especialidad.id_Especialidad_Medica,
                'nombre': medico_especialidad.especialidad.Espacialidad_Medica
            },
            'fecha_consulta': fecha_consulta.strftime('%Y-%m-%d'),
            'duracion_cita_minutos': medico_especialidad.duracion_cita
        })
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        trace = traceback.format_exc()
        print(f"[ERROR] Error en obtener_horas_disponibles: {error_msg}")
        print(f"[TRACE] {trace}")
        
        return JsonResponse({
            'success': False,
            'error': 'Error al obtener las horas disponibles',
            'detalle': error_msg,
            'trace': trace if hasattr(request.user, 'is_staff') and request.user.is_staff else None,
            'horas_disponibles': []
        }, status=500)

def obtener_citas_y_disponibilidad(request):
    """
    Obtiene tanto las citas existentes como la disponibilidad para un médico en un rango de fechas.
    Esta función es utilizada por el calendario para mostrar tanto las citas agendadas como los horarios disponibles.
    """
    from django.http import JsonResponse
    from django.utils import timezone
    from datetime import datetime, timedelta
    import json
    
    try:
        # Obtener parámetros de la solicitud
        data = json.loads(request.body) if request.body else {}
        medico_id = data.get('medico_id')
        especialidad_id = data.get('especialidad_id')
        start_date = data.get('start')
        end_date = data.get('end')
        
        # Validar parámetros requeridos
        if not all([medico_id, especialidad_id, start_date, end_date]):
            return JsonResponse({
                'success': False,
                'error': 'Faltan parámetros requeridos (medico_id, especialidad_id, start, end)',
                'citas': [],
                'disponibilidad': []
            }, status=400)
        
        # Configurar la zona horaria de Venezuela
        tz = pytz.timezone('America/Caracas')  # Usando pytz para compatibilidad
        
        # Convertir fechas de string a objetos datetime con la zona horaria correcta
        try:
            # Parsear fechas sin zona horaria
            start_naive = datetime.strptime(start_date, '%Y-%m-%d')
            end_naive = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Asignar la zona horaria de Venezuela usando localize para manejar correctamente DST
            start = tz.localize(start_naive)
            end = tz.localize(end_naive) + timedelta(days=1)  # Incluir el día completo
            
            print(f"Rango de fechas solicitado: {start.isoformat()} a {end.isoformat()} (Venezuela Time)")
            
        except (ValueError, pytz.exceptions.AmbiguousTimeError, pytz.exceptions.NonExistentTimeError) as e:
            return JsonResponse({
                'success': False,
                'error': f'Formato de fecha inválido. Use YYYY-MM-DD. Error: {str(e)}',
                'citas': [],
                'disponibilidad': []
            }, status=400)
        
        # Importar modelos necesarios
        from citas.models import CitasReservadas, HorarioCita, MedicoEspecialidad
        
        # 1. Obtener las citas existentes en el rango de fechas para el médico y especialidad específicos
        citas = CitasReservadas.objects.filter(
            horario__medico_id=medico_id,
            horario__especialidad_id=especialidad_id,  # Filtrar por especialidad
            start_datetime__gte=start,
            end_datetime__lte=end,
            estado__in=['PENDIENTE', 'CONFIRMADA']  # Solo citas activas
        ).select_related('paciente', 'horario__especialidad')
        
        print(f"Citas encontradas para médico {medico_id} y especialidad {especialidad_id}: {citas.count()}")
        
        # Formatear citas para el calendario
        citas_data = []
        for cita in citas:
            # Calcular duración en minutos
            duracion = int((cita.end_datetime - cita.start_datetime).total_seconds() / 60) if cita.end_datetime else 30
            
            citas_data.append({
                'id': cita.id,
                'title': f"{getattr(cita.paciente, 'Nombres_Paciente', 'Paciente')} {getattr(cita.paciente, 'Apellidos_Paciente', '')}",
                'fecha_hora_inicio': cita.start_datetime.astimezone(tz).isoformat(),
                'fecha_hora_fin': (cita.end_datetime.astimezone(tz).isoformat() if cita.end_datetime 
                                 else (cita.start_datetime + timedelta(minutes=duracion)).astimezone(tz).isoformat()),
                'start': cita.start_datetime.astimezone(tz).isoformat(),  # Mantener para compatibilidad
                'end': (cita.end_datetime.astimezone(tz).isoformat() if cita.end_datetime 
                       else (cita.start_datetime + timedelta(minutes=duracion)).astimezone(tz).isoformat()),
                'estado': cita.estado,
                'backgroundColor': '#dc3545',  # Rojo para citas
                'borderColor': '#c82333',
                'extendedProps': {
                    'tipo': 'cita',
                    'especialidad': cita.horario.especialidad.Espacialidad_Medica if hasattr(cita.horario, 'especialidad') and hasattr(cita.horario.especialidad, 'Espacialidad_Medica') else 'Sin Especialidad',
                    'duracion': duracion,
                    'notas': cita.nota or '',
                    'paciente_nombre': f"{getattr(cita.paciente, 'Nombres_Paciente', 'Paciente')} {getattr(cita.paciente, 'Apellidos_Paciente', '')}",
                    'descripcion': f"Cita con {getattr(cita.paciente, 'Nombres_Paciente', 'Paciente')} {getattr(cita.paciente, 'Apellidos_Paciente', '')}",
                    'citaId': cita.id
                }
            })
        
        # 2. Obtener la disponibilidad para cada día en el rango
        disponibilidad_data = []
        current_date = start
        
        # Obtener la duración de la cita para esta especialidad
        try:
            # Primero intentar obtener la duración de HorarioCita
            horario = HorarioCita.objects.filter(
                medico_id=medico_id,
                especialidad_id=especialidad_id
            ).first()
            
            if horario and hasattr(horario, 'duracion'):
                duracion_cita = horario.duracion
            elif horario and hasattr(horario, 'start_datetime') and hasattr(horario, 'end_datetime') and horario.start_datetime and horario.end_datetime:
                # Calcular la duración basada en la diferencia entre start_datetime y end_datetime
                duracion_cita = int((horario.end_datetime - horario.start_datetime).total_seconds() / 60)
            else:
                # Si no se puede determinar, intentar con MedicoEspecialidad (si existe)
                try:
                    from medicos.models import MedicoEspecialidad
                    medico_especialidad = MedicoEspecialidad.objects.filter(
                        medico_id=medico_id,
                        especialidad_id=especialidad_id
                    ).first()
                    
                    if medico_especialidad and hasattr(medico_especialidad, 'duracion_cita'):
                        duracion_cita = medico_especialidad.duracion_cita
                    else:
                        raise ValueError("No se pudo determinar la duración de la cita")
                except ImportError:
                    # Si no se puede importar el modelo MedicoEspecialidad, usar un valor por defecto
                    print("Advertencia: No se pudo importar el modelo MedicoEspecialidad. Usando duración por defecto de 30 minutos.")
                    duracion_cita = 30
                    
            print(f"Duración de cita obtenida: {duracion_cita} minutos")
            
        except Exception as e:
            error_msg = f"Error al obtener duración de la cita: {str(e)}"
            print(error_msg)
            return JsonResponse({
                'success': False,
                'error': error_msg,
                'citas': [],
                'disponibilidad': []
            }, status=400)
        
        # Obtener todos los horarios activos para el médico y especialidad
        print(f"Buscando horarios para médico_id={medico_id}, especialidad_id={especialidad_id}")
        print(f"Rango de fechas solicitado: {start} a {end}")
        
        # Obtener el modelo de médico para el nombre
        try:
            # Importar el modelo UsuarioMedico desde la aplicación citas
            from citas.models import UsuarioMedico
            try:
                medico = UsuarioMedico.objects.get(id_Medico=medico_id)
                medico_nombre = f"{medico.Nombres_Medico or ''} {medico.Apellidos_Medicos or ''}".strip() or 'Médico'
            except UsuarioMedico.DoesNotExist:
                medico_nombre = 'Médico'
        except Exception as e:
            print(f"Error al obtener información del médico: {str(e)}")
            medico_nombre = 'Médico'
        
        # Obtener los días de la semana en el rango solicitado
        from dateutil.rrule import rrule, DAILY, MO, TU, WE, TH, FR, SA, SU
        from datetime import date
        
        # Mapeo de días de la semana a constantes de dateutil
        DAYS_MAP = {
            'monday': MO,
            'tuesday': TU,
            'wednesday': WE,
            'thursday': TH,
            'friday': FR,
            'saturday': SA,
            'sunday': SU
        }
        
        # Asegurar que los IDs sean enteros
        try:
            medico_id_int = int(medico_id)
            especialidad_id_int = int(especialidad_id)
        except (ValueError, TypeError) as e:
            error_msg = f"Error en los parámetros: {str(e)}"
            print(error_msg)
            return JsonResponse({
                'success': False,
                'error': error_msg,
                'citas': [],
                'disponibilidad': []
            }, status=400)

        print(f"Buscando horarios para médico_id={medico_id_int}, especialidad_id={especialidad_id_int}")
        print(f"Rango de fechas: {start} a {end}")
        
        # Obtener los horarios base que se superpongan con el rango de fechas
        # No filtramos por fechas aquí para manejar la recurrencia correctamente
        horarios_base = HorarioCita.objects.filter(
            medico_id=medico_id_int,
            especialidad_id=especialidad_id_int,
            activo=True
        ).order_by('start_datetime')
        
        print(f"Se encontraron {horarios_base.count()} horarios base para el médico {medico_id_int} y especialidad {especialidad_id_int}")
        
        print(f"Consulta SQL generada: {str(horarios_base.query)}")
        print(f"Horarios base encontrados: {horarios_base.count()}")
        
        # Si no hay horarios, retornar vacío
        if not horarios_base.exists():
            error_msg = """
            No se encontraron horarios para los criterios especificados.
            Parámetros de búsqueda:
            - Médico ID: {}
            - Especialidad ID: {}
            - Rango: {} a {}
            - Zona horaria: {}
            """.format(
                medico_id_int,
                especialidad_id_int,
                start.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
                end.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
                tz.zone
            )
            print(error_msg)
            
            return JsonResponse({
                'success': True,
                'citas': citas_data,
                'disponibilidad': [],
                'message': 'No hay horarios configurados para este médico y especialidad en el rango de fechas solicitado.',
                'debug': {
                    'rango_solicitado': f"{start.astimezone(tz)} a {end.astimezone(tz)}",
                    'zona_horaria': str(tz),
                    'hora_actual': timezone.now().astimezone(tz).isoformat(),
                    'medico_id': medico_id_int,
                    'especialidad_id': especialidad_id_int,
                    'filtros_aplicados': {
                        'medico_id': medico_id_int,
                        'especialidad_id': especialidad_id_int,
                        'start_after': start.astimezone(timezone.utc).isoformat(),
                        'end_before': end.astimezone(timezone.utc).isoformat()
                    }
                }
            })
        
        # Procesar cada horario base
        for horario in horarios_base:
            # Obtener la hora de inicio y fin del horario
            hora_inicio = horario.start_datetime.time() if horario.start_datetime else None
            hora_fin = horario.end_datetime.time() if horario.end_datetime else None
            
            if not hora_inicio or not hora_fin:
                print(f"Horario {horario.id} sin hora de inicio o fin definida, omitiendo...")
                continue
            
            # Manejar la recurrencia basada en la regla de recurrencia
            if horario.recurrence_rule:
                # Si hay una regla de recurrencia, usarla
                try:
                    # Parsear la regla de recurrencia
                    rule = rrule.rrulestr(horario.recurrence_rule, dtstart=horario.start_datetime)
                    # Obtener los días de la semana de la regla
                    dias_semana = [MO, TU, WE, TH, FR, SA, SU]  # Por defecto todos los días
                    if hasattr(rule, '_byweekday'):
                        dias_semana = list(rule._byweekday)
                except Exception as e:
                    print(f"Error al parsear la regla de recurrencia: {e}")
                    # En caso de error, usar el día de la fecha de inicio
                    dias_semana = [MO, TU, WE, TH, FR, SA, SU][horario.start_datetime.weekday():horario.start_datetime.weekday()+1]
            else:
                # Si no hay recurrencia, usar solo el día de la fecha de inicio
                dias_semana = [MO, TU, WE, TH, FR, SA, SU][horario.start_datetime.weekday():horario.start_datetime.weekday()+1]
            
            print(f"Días de la semana para el horario {horario.id}: {dias_semana}")
            
            # Generar fechas para cada día en el rango que coincida con los días de la semana
            try:
                # Asegurarse de que start y end sean timezone-aware
                start_tz = start.astimezone(tz) if timezone.is_naive(start) else start
                end_tz = end.astimezone(tz) if timezone.is_naive(end) else end
                
                # Generar las fechas en el rango
                fechas = list(rrule(
                    DAILY,
                    dtstart=start_tz,
                    until=end_tz,
                    byweekday=dias_semana
                ))
                
                print(f"Generando {len(fechas)} fechas para el horario {horario.id}")
                
                for dt in fechas:
                    try:
                        # Crear fechas completas con la hora del horario
                        fecha_hora_inicio = tz.localize(datetime.combine(dt.date(), hora_inicio))
                        fecha_hora_fin = tz.localize(datetime.combine(dt.date(), hora_fin))
                        
                        # Asegurar que las fechas sean timezone-aware
                        if timezone.is_naive(fecha_hora_inicio):
                            fecha_hora_inicio = tz.localize(fecha_hora_inicio)
                        if timezone.is_naive(fecha_hora_fin):
                            fecha_hora_fin = tz.localize(fecha_hora_fin)
                            
                        # Verificar que la fecha esté dentro del rango solicitado
                        if fecha_hora_inicio < start_tz or fecha_hora_fin > end_tz:
                            continue
                            
                        # Verificar si hay citas en este horario
                        citas_en_este_horario = CitasReservadas.objects.filter(
                            horario__medico_id=medico_id_int,
                            horario__especialidad_id=especialidad_id_int,
                            start_datetime__lt=fecha_hora_fin,
                            end_datetime__gt=fecha_hora_inicio,
                            estado__in=['PENDIENTE', 'CONFIRMADA']
                        ).exists()

                        if not citas_en_este_horario:
                            # Agregar a la disponibilidad
                            disponibilidad_data.append({
                                'id': f'disp-{horario.id}-{dt.strftime("%Y%m%d")}',
                                'title': 'Disponible',
                                'start': fecha_hora_inicio.isoformat(),
                                'end': fecha_hora_fin.isoformat(),
                                'backgroundColor': '#28a745',
                                'borderColor': '#218838',
                                'extendedProps': {
                                    'tipo': 'disponibilidad',
                                    'duracion_cita': duracion_cita,
                                    'especialidad_id': especialidad_id_int,
                                    'medico_id': medico_id_int,
                                    'medico_nombre': medico_nombre,
                                    'descripcion': f"Disponibilidad del Dr. {medico_nombre}",
                                    'dia_semana': dt.strftime('%A'),
                                    'hora_inicio': hora_inicio.strftime('%H:%M'),
                                    'hora_fin': hora_fin.strftime('%H:%M')
                                },
                                'overlap': False,
                                'constraint': 'businessHours'
                            })
                            
                    except Exception as e:
                        print(f"Error al procesar fecha {dt} para horario {horario.id}: {str(e)}")
                        continue
                        
            except Exception as e:
                print(f"Error al generar fechas para el horario {horario.id}: {str(e)}")
                continue
            
            current_date += timedelta(days=1)
        
        return JsonResponse({
            'success': True,
            'citas': citas_data,
            'disponibilidad': disponibilidad_data,
            'meta': {
                'total_citas': len(citas_data),
                'rango_fechas': {
                    'inicio': start.isoformat(),
                    'fin': end.isoformat()
                },
                'duracion_cita_minutos': duracion_cita
            }
        })
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        trace = traceback.format_exc()
        print(f"[ERROR] Error en obtener_citas_y_disponibilidad: {error_msg}")
        print(f"[TRACE] {trace}")
        
        return JsonResponse({
            'success': False,
            'error': 'Error al obtener citas y disponibilidad',
            'detalle': error_msg,
            'trace': trace if hasattr(request, 'user') and hasattr(request.user, 'is_staff') and request.user.is_staff else None,
            'citas': [],
            'disponibilidad': []
        }, status=500)

def obtener_eventos(request):
    """
    Vista que maneja las solicitudes de eventos del calendario.
    Esta función es utilizada por FullCalendar para obtener tanto las citas existentes
    como los bloques de disponibilidad en un solo endpoint.
    """
    from django.http import JsonResponse
    from django.views.decorators.http import require_http_methods
    from django.utils import timezone
    from datetime import datetime, timedelta
    import json
    
    try:
        # Obtener parámetros de la solicitud
        if request.method == 'GET':
            medico_id = request.GET.get('medico_id')
            especialidad_id = request.GET.get('especialidad_id')
            start = request.GET.get('start')
            end = request.GET.get('end')
        else:  # POST
            data = json.loads(request.body) if request.body else {}
            medico_id = data.get('medico_id')
            especialidad_id = data.get('especialidad_id')
            start = data.get('start')
            end = data.get('end')
        
        # Validar parámetros requeridos
        if not all([medico_id, especialidad_id, start]):
            return JsonResponse({
                'success': False,
                'error': 'Faltan parámetros requeridos (medico_id, especialidad_id, start)',
                'events': []
            }, status=400)
        
        # Si no se proporciona end, usar start + 1 mes
        if not end:
            start_date = datetime.strptime(start, '%Y-%m-%d')
            end_date = (start_date + timedelta(days=30)).strftime('%Y-%m-%d')
            end = end_date
        
        # Usar la función obtener_citas_y_disponibilidad para obtener los datos
        from django.test import RequestFactory
        from django.http import JsonResponse
        
        # Crear una solicitud simulada para obtener_citas_y_disponibilidad
        factory = RequestFactory()
        req_data = {
            'medico_id': medico_id,
            'especialidad_id': especialidad_id,
            'start': start,
            'end': end
        }
        
        # Llamar a obtener_citas_y_disponibilidad con los parámetros
        from .view import obtener_citas_y_disponibilidad
        req = factory.post('/api/obtener-citas-y-disponibilidad/', 
                          data=json.dumps(req_data),
                          content_type='application/json')
        
        # Configurar el usuario en la solicitud si es necesario
        if hasattr(request, 'user'):
            req.user = request.user
        
        # Obtener la respuesta
        response = obtener_citas_y_disponibilidad(req)
        
        # Si hay un error, devolverlo
        if response.status_code != 200:
            return response
        
        # Combinar citas y disponibilidad en una sola lista de eventos
        data = json.loads(response.content)
        
        if not data.get('success'):
            return JsonResponse({
                'success': False,
                'error': data.get('error', 'Error desconocido al obtener eventos'),
                'events': []
            }, status=response.status_code)
        
        # Formatear la respuesta para FullCalendar
        eventos = []
        
        # Agregar citas
        for cita in data.get('citas', []):
            eventos.append({
                'id': f"cita_{cita.get('id', '')}",
                'title': cita.get('title', 'Cita'),
                'start': cita.get('start'),
                'end': cita.get('end'),
                'color': cita.get('backgroundColor'),
                'textColor': '#ffffff',
                'borderColor': cita.get('borderColor'),
                'extendedProps': {
                    'tipo': 'cita',
                    'estado': cita.get('estado', ''),
                    **cita.get('extendedProps', {})
                }
            })
        
        # Agregar disponibilidad
        for disp in data.get('disponibilidad', []):
            eventos.append({
                'id': f"disp_{len(eventos)}",
                'title': 'Disponible',
                'start': disp.get('start'),
                'end': disp.get('end'),
                'display': 'background',
                'backgroundColor': disp.get('backgroundColor', '#dff0d8'),
                'borderColor': disp.get('borderColor', '#d6e9c6'),
                'className': 'disponible-slot',
                'extendedProps': {
                    'tipo': 'disponibilidad',
                    **disp.get('extendedProps', {})
                }
            })
        
        return JsonResponse(eventos, safe=False)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Error al decodificar el JSON de la solicitud',
            'events': []
        }, status=400)
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        trace = traceback.format_exc()
        print(f"[ERROR] Error en obtener_eventos: {error_msg}")
        print(f"[TRACE] {trace}")
        
        return JsonResponse({
            'success': False,
            'error': 'Error al obtener eventos del calendario',
            'detalle': error_msg,
            'trace': trace if hasattr(request, 'user') and hasattr(request.user, 'is_staff') and request.user.is_staff else None,
            'events': []
        }, status=500)

def editar_cita(request, cita_id):
    """
    Maneja la edición de una cita existente.
    """
    from django.http import JsonResponse
    from django.views.decorators.http import require_http_methods
    from django.utils import timezone
    from django.db import transaction
    from datetime import datetime, timedelta
    import json
    
    if request.method == 'GET':
        # Obtener los datos de la cita para mostrar en el formulario de edición
        try:
            from citas.models import CitasReservadas
            
            cita = CitasReservadas.objects.select_related(
                'medico', 'especialidad', 'paciente'
            ).get(
                id_Cita=cita_id,
                estado__in=['PENDIENTE', 'CONFIRMADA']
            )
            
            return JsonResponse({
                'success': True,
                'cita': {
                    'id': cita.id_Cita,
                    'medico_id': cita.medico_id,
                    'especialidad_id': cita.especialidad_id,
                    'paciente_id': cita.paciente_id,
                    'fecha_hora': cita.fecha_hora.isoformat(),
                    'duracion': cita.duracion or 30,
                    'estado': cita.estado,
                    'notas': cita.notas or '',
                    'fecha_creacion': cita.fecha_creacion.isoformat(),
                    'fecha_actualizacion': cita.fecha_actualizacion.isoformat(),
                    'paciente': {
                        'id': cita.paciente.id_Paciente,
                        'nombre': cita.paciente.nombre,
                        'apellido': cita.paciente.apellido,
                        'cedula': cita.paciente.cedula,
                        'telefono': cita.paciente.telefono,
                        'email': cita.paciente.email
                    },
                    'especialidad': {
                        'id': cita.especialidad.id_Especialidad_Medica,
                        'nombre': cita.especialidad.Espacialidad_Medica
                    },
                    'medico': {
                        'id': cita.medico.id_Medico,
                        'nombre': cita.medico.user.get_full_name(),
                        'especialidad': cita.especialidad.Espacialidad_Medica
                    }
                }
            })
            
        except CitasReservadas.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'La cita no existe o no se puede editar',
                'cita': None
            }, status=404)
            
        except Exception as e:
            import traceback
            error_msg = str(e)
            trace = traceback.format_exc()
            print(f"[ERROR] Error al obtener cita para editar: {error_msg}")
            print(f"[TRACE] {trace}")
            
            return JsonResponse({
                'success': False,
                'error': 'Error al obtener los datos de la cita',
                'detalle': error_msg
            }, status=500)
    
    elif request.method == 'POST':
        # Procesar la actualización de la cita
        try:
            data = json.loads(request.body) if request.body else {}
            
            # Validar datos requeridos
            required_fields = ['fecha_hora', 'duracion', 'estado']
            if not all(field in data for field in required_fields):
                return JsonResponse({
                    'success': False,
                    'error': 'Faltan campos requeridos',
                    'campos_faltantes': [f for f in required_fields if f not in data]
                }, status=400)
            
            with transaction.atomic():
                from citas.models import CitasReservadas, HorarioCita
                
                # Obtener la cita existente
                cita = CitasReservadas.objects.select_for_update().get(
                    id_Cita=cita_id,
                    estado__in=['PENDIENTE', 'CONFIRMADA']
                )
                
                # Verificar si se está cambiando la fecha/hora o duración
                nueva_fecha_hora = datetime.fromisoformat(data['fecha_hora'].replace('Z', '+00:00'))
                nueva_duracion = int(data['duracion'])
                
                # Verificar disponibilidad solo si se cambia la fecha/hora o duración
                if (cita.fecha_hora != nueva_fecha_hora or 
                    (cita.duracion or 30) != nueva_duracion):
                    
                    # Verificar que el nuevo horario esté disponible
                    hora_fin = nueva_fecha_hora + timedelta(minutes=nueva_duracion)
                    
                    # Verificar superposición con otras citas (excluyendo la actual)
                    citas_solapadas = CitasReservadas.objects.filter(
                        medico_id=cita.medico_id,
                        fecha_hora__lt=hora_fin,
                        fecha_hora__gte=nueva_fecha_hora - timedelta(minutes=59),
                        estado__in=['PENDIENTE', 'CONFIRMADA']
                    ).exclude(id_Cita=cita_id).exists()
                    
                    if citas_solapadas:
                        return JsonResponse({
                            'success': False,
                            'error': 'El horario seleccionado ya está ocupado',
                            'campo': 'fecha_hora'
                        }, status=400)
                    
                    # Verificar que el horario esté dentro del horario laboral
                    dia_semana = nueva_fecha_hoto.weekday()
                    hora_inicio_nueva = nueva_fecha_hoto.time()
                    hora_fin_nueva = (nueva_fecha_hoto + timedelta(minutes=nueva_duracion)).time()
                    
                    horario_valido = HorarioCita.objects.filter(
                        medico_id=cita.medico_id,
                        dia_semana=dia_semana,
                        hora_inicio__lte=hora_inicio_nueva,
                        hora_fin__gte=hora_fin_nueva,
                        activo=True
                    ).exists()
                    
                    if not horario_valido:
                        return JsonResponse({
                            'success': False,
                            'error': 'El horario seleccionado está fuera del horario laboral',
                            'campo': 'fecha_hora'
                        }, status=400)
                
                # Actualizar la cita
                cita.fecha_hora = nueva_fecha_hoto
                cita.duracion = nueva_duracion
                cita.estado = data['estado']
                cita.notas = data.get('notas', cita.notas)
                cita.save()
                
                return JsonResponse({
                    'success': True,
                    'mensaje': 'Cita actualizada correctamente',
                    'cita_id': cita.id_Cita,
                    'fecha_hora': cita.fecha_hora.isoformat(),
                    'estado': cita.estado
                })
                
        except CitasReservadas.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'La cita no existe o no se puede editar'
            }, status=404)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Error en el formato de los datos enviados'
            }, status=400)
            
        except Exception as e:
            import traceback
            error_msg = str(e)
            trace = traceback.format_exc()
            print(f"[ERROR] Error al actualizar la cita: {error_msg}")
            print(f"[TRACE] {trace}")
            
            return JsonResponse({
                'success': False,
                'error': 'Error al actualizar la cita',
                'detalle': error_msg
            }, status=500)
    
    else:
        return JsonResponse({
            'success': False,
            'error': 'Método no permitido',
            'metodos_permitidos': ['GET', 'POST']
        }, status=405)

def actualizar_estado_cita(request):
    """
    Actualiza el estado de una cita (CONFIRMADA, CANCELADA, COMPLETADA, etc.)
    """
    from django.http import JsonResponse
    from django.views.decorators.http import require_http_methods
    from django.db import transaction
    import json
    
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Método no permitido. Se requiere POST',
            'metodos_permitidos': ['POST']
        }, status=405)
    
    try:
        # Obtener datos de la solicitud
        data = json.loads(request.body) if request.body else {}
        cita_id = data.get('cita_id')
        nuevo_estado = data.get('estado')
        motivo_cancelacion = data.get('motivo_cancelacion', '')
        
        # Validar datos requeridos
        if not cita_id or not nuevo_estado:
            return JsonResponse({
                'success': False,
                'error': 'Faltan parámetros requeridos (cita_id, estado)',
                'campos_faltantes': [
                    f for f in ['cita_id', 'estado'] 
                    if not data.get(f)
                ]
            }, status=400)
        
        # Validar que el estado sea uno de los permitidos
        estados_permitidos = ['PENDIENTE', 'CONFIRMADA', 'CANCELADA', 'COMPLETADA', 'NO_ASISTIO']
        if nuevo_estado not in estados_permitidos:
            return JsonResponse({
                'success': False,
                'error': f'Estado no válido. Estados permitidos: {", ".join(estados_permitidos)}',
                'estado_recibido': nuevo_estado
            }, status=400)
        
        # Validar motivo de cancelación si se cancela la cita
        if nuevo_estado == 'CANCELADA' and not motivo_cancelacion:
            return JsonResponse({
                'success': False,
                'error': 'Se requiere un motivo de cancelación',
                'campo': 'motivo_cancelacion'
            }, status=400)
        
        with transaction.atomic():
            from citas.models import CitasReservadas, HistorialCambiosCita
            from django.utils import timezone
            
            # Bloquear el registro de la cita para evitar condiciones de carrera
            cita = CitasReservadas.objects.select_for_update().filter(
                id_Cita=cita_id
            ).first()
            
            if not cita:
                return JsonResponse({
                    'success': False,
                    'error': 'La cita no existe',
                    'cita_id': cita_id
                }, status=404)
            
            # Guardar el estado anterior para el historial
            estado_anterior = cita.estado
            
            # Verificar si el cambio de estado es válido
            if estado_anterior == 'CANCELADA' and nuevo_estado != 'CANCELADA':
                return JsonResponse({
                    'success': False,
                    'error': 'No se puede cambiar el estado de una cita cancelada',
                    'estado_actual': estado_anterior,
                    'nuevo_estado': nuevo_estado
                }, status=400)
                
            if estado_anterior == 'COMPLETADA':
                return JsonResponse({
                    'success': False,
                    'error': 'No se puede modificar una cita ya completada',
                    'estado_actual': estado_anterior,
                    'nuevo_estado': nuevo_estado
                }, status=400)
            
            # Actualizar el estado de la cita
            cita.estado = nuevo_estado
            
            # Si se cancela, guardar el motivo
            if nuevo_estado == 'CANCELADA':
                cita.motivo_cancelacion = motivo_cancelacion
                
                # Si hay un usuario autenticado, registrar quién canceló
                if hasattr(request, 'user') and request.user.is_authenticated:
                    cita.cancelado_por = request.user
            
            cita.save()
            
            # Registrar el cambio en el historial
            HistorialCambiosCita.objects.create(
                cita=cita,
                campo_modificado='estado',
                valor_anterior=estado_anterior,
                valor_nuevo=nuevo_estado,
                usuario=request.user if hasattr(request, 'user') and request.user.is_authenticated else None,
                motivo_cambio=f'Cambio de estado: {estado_anterior} -> {nuevo_estado}'
            )
            
            # Si se confirma una cita, podrías agregar aquí la lógica para enviar notificaciones
            if nuevo_estado == 'CONFIRMADA':
                # Ejemplo: enviar_notificacion_confirmacion(cita)
                pass
            
            return JsonResponse({
                'success': True,
                'mensaje': f'Estado de la cita actualizado a {nuevo_estado}',
                'cita_id': cita.id_Cita,
                'estado_anterior': estado_anterior,
                'nuevo_estado': nuevo_estado,
                'fecha_actualizacion': cita.fecha_actualizacion.isoformat()
            })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Error en el formato de los datos enviados. Se espera un JSON válido.'
        }, status=400)
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        trace = traceback.format_exc()
        print(f"[ERROR] Error al actualizar el estado de la cita: {error_msg}")
        print(f"[TRACE] {trace}")
        
        return JsonResponse({
            'success': False,
            'error': 'Error al actualizar el estado de la cita',
            'detalle': error_msg,
            'trace': trace if hasattr(request, 'user') and hasattr(request.user, 'is_staff') and request.user.is_staff else None
        }, status=500)

# ---------------------------------------------------------------------
# 🔹 VISTA PRINCIPAL: CREAR CITA (renderiza el calendario y formulario)
# ---------------------------------------------------------------------
@csrf_exempt
def crear_cita(request):
    """
    Muestra el formulario para crear una nueva cita médica,
    junto con la disponibilidad del médico seleccionada.
    """
    # Obtener todas las especialidades médicas ordenadas alfabéticamente
    especialidades = EspecialidadMedica.objects.all().order_by('Espacialidad_Medica')

    paciente_id = request.GET.get('paciente_id')
    paciente = None
    if paciente_id:
        try:
            paciente = Paciente.objects.get(id_Paciente=paciente_id)
            # Forzar la selección del paciente en el formulario
            request.session['paciente_seleccionado'] = paciente_id
        except Paciente.DoesNotExist:
            messages.warning(request, 'El paciente especificado no existe.')
            # Limpiar la selección si el paciente no existe
            if 'paciente_seleccionado' in request.session:
                del request.session['paciente_seleccionado']

    especialidad_id = request.GET.get('especialidad_id')
    medico_id = request.GET.get('medico_id')

    medicos = UsuarioMedico.objects.none()
    especialidad = medico = None

    if especialidad_id:
        try:
            # Usar 'id' o el campo correcto de su modelo, asumiendo id_Especialidad_Medica
            especialidad = EspecialidadMedica.objects.get(id_Especialidad_Medica=especialidad_id)
            medicos = UsuarioMedico.objects.filter(
                # Asumiendo que tiene un ManyToMany o un campo de enlace llamado medicoespecialidad
                # Si el campo es simplemente especialidad, ajuste la query
                medicoespecialidad__especialidad=especialidad,
                activo=True
            ).distinct().order_by('Apellidos_Medicos', 'Nombres_Medico')
            if medico_id:
                # Usar 'id' o el campo correcto de su modelo, asumiendo id_Medico
                medico = UsuarioMedico.objects.filter(id_Medico=medico_id, activo=True).first()
        except EspecialidadMedica.DoesNotExist:
            messages.warning(request, 'La especialidad seleccionada no existe.')
        except Exception:
             # Manejar posible error si el campo de enlace no existe
             medicos = UsuarioMedico.objects.none()

    # Petición AJAX para cargar médicos (Select dinámico)
    # Se reemplaza por la función 'api_medicos' si es necesaria, pero se deja el código original
    # para no romper la lógica existente.
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if especialidad_id:
            # Reutilizar la lógica de médicos ya cargada
            medicos_data = [
                {'id': m.id_Medico, 'text': f"{m.Apellidos_Medicos}, {m.Nombres_Medico}"}
                for m in medicos
            ]
            return JsonResponse({'success': True, 'medicos': medicos_data})
        return JsonResponse({'success': False, 'error': 'No se especificó la especialidad'}, status=400)

    # Obtener todos los pacientes para el select
    pacientes = Paciente.objects.all().order_by('Apellidos_Paciente', 'Nombres_Paciente')
    
    # Obtener el ID del paciente de la sesión o del parámetro GET
    paciente_seleccionado_id = paciente_id or request.session.get('paciente_seleccionado')
    
    context = {
        'especialidades': especialidades,
        'medicos': medicos,
        'paciente': paciente,
        'paciente_seleccionado': paciente,
        'paciente_id': paciente_seleccionado_id,
        'pacientes': pacientes,
        'especialidad_seleccionada': especialidad,
        'medico_seleccionado': medico,
        'fecha_actual': timezone.now().date(),
    }

    return render(request, 'citas/cita_web/crear_cita.html', context)


# ---------------------------------------------------------------------
# 🔹 API: DISPONIBILIDAD DE UN MÉDICO (VERSIÓN MEJORADA Y CORREGIDA)
# ---------------------------------------------------------------------
@csrf_exempt
def disponibilidad_medico(request):
    """
    Devuelve la disponibilidad del médico (horarios libres) en formato JSON.
    CORREGIDO: Manejo consistente de zonas horarias (UTC vs Local -04).
    """
    print("\n" + "=" * 60)
    print("🔹 INICIANDO DISPONIBILIDAD_MEDICO - EJECUTÁNDOSE AHORA")
    print("=" * 60)
    import time
    start_time = time.time()
    
    try:
        # Obtener parámetros de la URL
        medico_id = request.GET.get('medico_id')
        especialidad_id = request.GET.get('especialidad_id')
        fecha_inicio = request.GET.get('start')
        fecha_fin = request.GET.get('end')

        # ... (Logging de parámetros y validaciones iniciales - SE MANTIENE) ...
        if not all([medico_id, especialidad_id, fecha_inicio, fecha_fin]):
            print(f"Parametros recibidos - medico: {medico_id}, especialidad: {especialidad_id}, inicio: {fecha_inicio}, fin: {fecha_fin}")
            return JsonResponse({
                'success': False,
                'error': 'Seleccione una especialidad y un médico primero'
            }, status=400)

        # Validar y convertir fechas (FullCalendar envía formato ISO con zona horaria)
        try:
            # Obtener la zona horaria del request o usar la predeterminada
            tz_name = request.GET.get('timezone', 'America/Caracas')  # Usar valor por defecto si no se especifica
            try:
                tz = pytz.timezone(tz_name)
            except (pytz.exceptions.UnknownTimeZoneError, AttributeError):
                tz = pytz.timezone('America/Caracas')  # Valor por defecto si la zona horaria no es válida
            
            print(f"🔵 Usando zona horaria: {tz.zone}")
            
            # Decodificar la codificación URL y analizar datetime con zona horaria
            fecha_inicio_str = fecha_inicio.replace('%3A', ':')
            fecha_fin_str = fecha_fin.replace('%3A', ':')
            
            # Parsear las fechas con zona horaria
            try:
                # Intentar analizar con la zona horaria incluida
                start_dt = datetime.strptime(fecha_inicio_str, '%Y-%m-%dT%H:%M:%S%z')
                end_dt = datetime.strptime(fecha_fin_str, '%Y-%m-%dT%H:%M:%S%z')
                
                # Convertir a la zona horaria de Caracas para consistencia
                start_dt = start_dt.astimezone(tz)
                end_dt = end_dt.astimezone(tz)
                
            except ValueError:
                # Si falla, intentar sin la zona horaria y asumir que está en la zona horaria del servidor
                start_dt = datetime.strptime(fecha_inicio_str.split('+')[0], '%Y-%m-%dT%H:%M:%S')
                end_dt = datetime.strptime(fecha_fin_str.split('+')[0], '%Y-%m-%dT%H:%M:%S')
                
                # Hacer las fechas conscientes de la zona horaria y convertir a Caracas
                server_tz = timezone.get_current_timezone()
                start_dt = timezone.make_aware(start_dt, server_tz).astimezone(tz)
                end_dt = timezone.make_aware(end_dt, server_tz).astimezone(tz)
            
            # Obtener solo la fecha para el procesamiento (en la zona horaria de Caracas)
            fecha_inicio_dt = start_dt.date()
            fecha_fin_dt = end_dt.date()
            
            print(f"✅ Fechas recibidas - Inicio: {start_dt} ({start_dt.tzinfo}), Fin: {end_dt} ({end_dt.tzinfo})")
            print(f"✅ Fechas convertidas - Inicio: {fecha_inicio_dt}, Fin: {fecha_fin_dt} (Zona horaria: {tz.zone})")
        
        except Exception as e:
            error_msg = f'Error al procesar fechas: {str(e)}. Formato esperado: YYYY-MM-DDTHH:MM:SS±HH:MM.'
            print(f"❌ {error_msg}")
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'error': error_msg
            }, status=400)

        # Obtener médico y especialidad
        try:
            medico = UsuarioMedico.objects.get(id_Medico=medico_id, activo=True)
            especialidad = EspecialidadMedica.objects.get(id_Especialidad_Medica=especialidad_id)
        except UsuarioMedico.DoesNotExist:
            error_msg = 'Médico no encontrado o inactivo'
            return JsonResponse({'success': False, 'error': error_msg}, status=404)
        except EspecialidadMedica.DoesNotExist:
            error_msg = 'Especialidad no encontrada'
            return JsonResponse({'success': False, 'error': error_msg}, status=404)

        # Query final de horarios
        horarios = HorarioCita.objects.filter(
            medico_id=medico_id,
            especialidad_id=especialidad_id,
            activo=True
        ).select_related('turno')  # Asegurarse de cargar la relación turno

        print(f"🔍 Horarios encontrados: {horarios.count()}")
        for h in horarios:
            print(f"   - {h.start_datetime.strftime('%H:%M')} a {h.end_datetime.strftime('%H:%M')} (Turno: {getattr(h.turno, 'nombre', 'Sin turno')})")

        if not horarios.exists():
            print("⚠️ No hay horarios configurados para este médico y especialidad")
            return JsonResponse({
                'success': True,
                'disponibilidad': {},
                'mensaje': 'No hay horarios configurados para este médico y especialidad.'
            })
        
        # ----------------------------------------------------------------------
        # 🔑 CLAVE DE LA CORRECCIÓN DE ZONA HORARIA
        # ----------------------------------------------------------------------
        # Usar la zona horaria que ya se obtuvo del request (tz)
        print(f"🔵 Zona horaria para búsqueda: {tz.zone}")
        
        # 2. Definir el rango de búsqueda en la zona horaria local.
        inicio_local = datetime.combine(fecha_inicio_dt, datetime.min.time())
        fin_local = datetime.combine(fecha_fin_dt, datetime.max.time())
        
        # Hacer que sean conscientes de la zona horaria
        inicio_local = timezone.make_aware(inicio_local, tz)
        fin_local = timezone.make_aware(fin_local, tz)
        
        # 3. Convertir el rango de búsqueda a UTC para la consulta a la BD
        #    La BD guarda las citas en UTC.
        inicio_utc = inicio_local.astimezone(pytz.utc)
        fin_utc = fin_local.astimezone(pytz.utc)
        
        print(f"🕐 Rango de búsqueda Local: {inicio_local} a {fin_local}")
        print(f"🕐 Rango de búsqueda UTC (BD): {inicio_utc} a {fin_utc}")

        # Obtener todas las citas reservadas del médico específico (todas especialidades)
        citas_reservadas = CitasReservadas.objects.filter(
            horario__medico__id_Medico=medico_id,  # Filtrar por id del médico
            start_datetime__lt=fin_utc,
            end_datetime__gt=inicio_utc,
            estado__in=['pendiente', 'confirmada']
        ).select_related('horario')
        
        print(f"🔵 Citas reservadas encontradas: {citas_reservadas.count()}")

        # 4. Crear un diccionario de citas ocupadas basado en la HORA LOCAL
        citas_ocupadas = {}
        
        for cita in citas_reservadas:
            # Convertir de UTC a la HORA LOCAL para la comparación
            start_local = timezone.localtime(cita.start_datetime, tz)
            end_local = timezone.localtime(cita.end_datetime, tz)

            fecha_str = start_local.strftime('%Y-%m-%d')
            
            if fecha_str not in citas_ocupadas:
                citas_ocupadas[fecha_str] = set()
            
            # Marcar el slot de inicio y todos los slots intermedios
            # Redondear a los 30 minutos más cercanos
            start_minute = start_local.minute
            start_minute = (start_minute // 30) * 30  # Redondear hacia abajo al múltiplo de 30 más cercano
            
            current_slot_time = start_local.replace(minute=start_minute, second=0, microsecond=0)
            end_time = end_local.replace(second=0, microsecond=0)
            
            # Asegurarse de que al menos hay un slot
            if current_slot_time >= end_time:
                end_time = current_slot_time + timedelta(minutes=30)
            
            # Generar todos los slots de 30 minutos en el rango de la cita
            while current_slot_time < end_time:
                # Asegurarse de que estamos usando la hora local correcta
                slot_time_local = timezone.localtime(current_slot_time, tz)
                citas_ocupadas[fecha_str].add(slot_time_local.strftime('%H:%M'))
                current_slot_time += timedelta(minutes=30)
                
            print(f"🔵 Cita ocupada: {fecha_str} de {start_local.strftime('%H:%M')} a {end_local.strftime('%H:%M')}")
                
        print(f"🗓️ Citas ocupadas por fecha (Local): {dict(citas_ocupadas)}")

        disponibilidad = {}

        # Procesar cada horario
        for horario in horarios:
            dias_laborales = get_rrule_days(horario.recurrence_rule)

            # Iterar sobre el rango de fechas SOLICITADO
            fecha_actual = fecha_inicio_dt
            
            while fecha_actual <= fecha_fin_dt:
                fecha_str = fecha_actual.strftime('%Y-%m-%d')
                
                # Verificar si el día de la semana corresponde
                if not dias_laborales or fecha_actual.weekday() in dias_laborales:
                    
                    print(f"\n📅 Procesando horario para el {fecha_actual}")
                    
                    # Obtener la hora de inicio y fin del horario
                    # Asegurarse de que las horas están en la zona horaria correcta
                    hora_inicio_original = horario.start_datetime.astimezone(tz).time()
                    hora_fin_original = horario.end_datetime.astimezone(tz).time()
                    
                    print(f"   - Horario base: {hora_inicio_original} a {hora_fin_original}")
                    
                    # Crear los objetos datetime con la fecha actual y las horas del horario
                    start_dt_local = datetime.combine(fecha_actual, hora_inicio_original)
                    end_dt_local = datetime.combine(fecha_actual, hora_fin_original)
                    
                    # Hacer que sean conscientes de la zona horaria
                    start_dt_local = timezone.make_aware(start_dt_local, tz)
                    end_dt_local = timezone.make_aware(end_dt_local, tz)
                    
                    print(f"   - Rango procesado: {start_dt_local} a {end_dt_local}")
                    
                    # Procesar este día específico
                    slots_procesados = procesar_horario_mejorado(
                        horario=horario, 
                        start_dt_local=start_dt_local, 
                        end_dt_local=end_dt_local,
                        tz=tz, 
                        disponibilidad=disponibilidad, 
                        citas_ocupadas=citas_ocupadas
                    )
                    
                    print(f"   - Slots generados: {slots_procesados}")

                fecha_actual += timedelta(days=1)


        # Crear el array de events para FullCalendar
        events = []
        for fecha, slots in disponibilidad.items():
            for slot in slots:
                if slot['disponible']:
                    # Formatear las fechas en formato ISO con información de zona horaria
                    start_iso = slot['start_iso']
                    end_iso = slot['end_iso']
                    
                    events.append({
                        'title': f"Disponible - {slot['hora_inicio']}",
                        'start': start_iso,
                        'end': end_iso,
                        'allDay': False,
                        'extendedProps': {
                            'fecha': fecha,
                            'hora': slot['hora_inicio'],
                            'horario_id': slot['horario_id']
                        },
                        'backgroundColor': '#28a745',
                        'borderColor': '#218838',
                        'textColor': 'white',
                        'display': 'block'
                    })
                
        # Nota: Se eliminó la sección de fechas_con_citas ya que ahora manejamos la disponibilidad por slots

        # Ordenar los horarios por hora en cada fecha
        for fecha in disponibilidad:
            disponibilidad[fecha].sort(key=lambda x: x['hora_inicio'])

        response_data = {
            'success': True,
            'events': events,
            'disponibilidad': disponibilidad,  # Mantener para compatibilidad
            'medico': f'{medico.Nombres_Medico} {medico.Apellidos_Medicos}',
            'especialidad': especialidad.Espacialidad_Medica,
            'rango_fechas': {
                'inicio': fecha_inicio,
                'fin': fecha_fin
            },
            'total_horarios': sum(len(slots) for slots in disponibilidad.values()),
            'debug_info': {
                'horarios_encontrados': horarios.count(),
                'citas_reservadas': citas_reservadas.count(),
                'fechas_con_disponibilidad': len(disponibilidad)
            }
        }

        print(f"✅ Respuesta enviada: {response_data['total_horarios']} slots totales")
        print("=" * 60)

        return JsonResponse(response_data)

    except Exception as e:
        error_msg = f"Error al procesar la solicitud: {str(e)}\n\n{traceback.format_exc()}"
        print(f"❌ ERROR CRÍTICO: {error_msg}")
        return JsonResponse({
            'success': False,
            'error': 'Error interno del servidor al procesar la disponibilidad',
            'details': str(e)
        }, status=500)


# Se modifica la firma para recibir la fecha de fin y simplificar el cálculo
def procesar_horario_mejorado(horario, start_dt_local, end_dt_local, tz, disponibilidad, citas_ocupadas):
    """
    Genera los slots de 30 minutos entre start_dt_local y end_dt_local.
    Todos los cálculos y comparaciones se realizan en HORA LOCAL.
    
    Args:
        horario: Objeto HorarioCita
        start_dt_local: datetime con timezone para el inicio del rango
        end_dt_local: datetime con timezone para el fin del rango
        tz: timezone para las conversiones (debe ser America/Caracas)
        disponibilidad: diccionario para almacenar los slots disponibles
        citas_ocupadas: diccionario con las citas ya reservadas
    """
    slots_procesados = 0
    try:
        print(f"\n🔄 [procesar_horario_mejorado] Iniciando procesamiento")
        print(f"   - Rango solicitado: {start_dt_local} a {end_dt_local}")
        
        # Asegurarse de que las fechas tengan timezone y estén en la zona horaria correcta
        if timezone.is_naive(start_dt_local):
            start_dt_local = timezone.make_aware(start_dt_local, tz)
        else:
            start_dt_local = start_dt_local.astimezone(tz)
            
        if timezone.is_naive(end_dt_local):
            end_dt_local = timezone.make_aware(end_dt_local, tz)
        else:
            end_dt_local = end_dt_local.astimezone(tz)
        
        print(f"   - Rango en {tz.zone}: {start_dt_local} a {end_dt_local}")
        
        # Si el rango no es válido, salir
        if start_dt_local >= end_dt_local:
            print(f"   ⚠️ Rango inválido: la fecha de inicio es mayor o igual a la de fin")
            return 0
            
        # Asegurarse de que empezamos en un slot de 30 minutos
        start_minute = start_dt_local.minute
        start_minute = (start_minute // 30) * 30  # Redondear hacia abajo al múltiplo de 30 más cercano
        current = start_dt_local.replace(minute=start_minute, second=0, microsecond=0)
        
        slot_duration = timedelta(minutes=30)
        
        # Ajustar el final para que termine en un slot completo
        end_dt_local = end_dt_local.replace(second=0, microsecond=0)
        
        print(f"   - Inicio ajustado: {current}")
        print(f"   - Fin ajustado: {end_dt_local}")
        print(f"   - Duración del horario: {end_dt_local - current} (mínimo 30 minutos requeridos)")
        
        # Si después de ajustar, el rango es menor a 30 minutos, salir
        if (end_dt_local - current) < slot_duration:
            print(f"   ⚠️ El rango es menor a 30 minutos después del ajuste")
            return 0
        
        while current < end_dt_local:
            # Calcular el final del slot actual
            slot_end = current + slot_duration
            
            # No exceder el final del rango
            if slot_end > end_dt_local:
                break
                
            # Formatear fechas para el diccionario
            fecha_str = current.strftime('%Y-%m-%d')
            hora_str = current.strftime('%H:%M')
            hora_fin_str = slot_end.strftime('%H:%M')
            
            # Verificar si el slot está ocupado
            ocupado = False
            if fecha_str in citas_ocupadas and hora_str in citas_ocupadas[fecha_str]:
                ocupado = True
                print(f"   ⚠️ Slot ocupado: {fecha_str} {hora_str}")
            
            # Crear el objeto slot
            slot = {
                'hora_inicio': hora_str,
                'hora_fin': hora_fin_str,
                'disponible': not ocupado,
                'start_iso': current.isoformat(),
                'end_iso': slot_end.isoformat(),
                'turno': str(getattr(horario.turno, 'nombre', 'Sin turno') if hasattr(horario, 'turno') else 'Sin turno'),
                'domicilio': getattr(horario, 'domicilio', False),
                'fecha_completa': current.strftime('%Y-%m-%d %H:%M:%S'),
                'horario_id': horario.id,
                'timezone': str(tz)
            }
            
            print(f"   - Slot generado: {hora_str} a {hora_fin_str} - {'Disponible' if not ocupado else 'Ocupado'}")
            
            # Agregar a la disponibilidad
            if fecha_str not in disponibilidad:
                disponibilidad[fecha_str] = []
                
            # Evitar duplicados
            slot_existente = next(
                (s for s in disponibilidad[fecha_str] if s['hora_inicio'] == slot['hora_inicio']), 
                None
            )
            
            if not slot_existente:
                disponibilidad[fecha_str].append(slot)
            elif not slot_existente['disponible'] and not ocupado:
                # Actualizar si el slot existente está ocupado pero este no
                slot_existente.update(slot)
            
            current = slot_end  # Mover al siguiente slot
            slots_procesados += 1
            
        print(f"✅ [procesar_horario_mejorado] Procesados {slots_procesados} slots")
        return slots_procesados
        
    except Exception as e:
        print(f"❌ [procesar_horario_mejorado] Error: {str(e)}")
        traceback.print_exc()
        return 0
        print(f"      - Error en procesar_horario_mejorado: {str(e)}")
        traceback.print_exc()
    
    return slots_procesados


# ---------------------------------------------------------------------
# 🔹 API: GUARDAR CITA (SE MANTIENE, SÓLO SE CORRIGE LA OBTENCIÓN DE MÉDICO)
# ---------------------------------------------------------------------
@csrf_exempt
def guardar_cita(request):
    """
    Guarda una nueva cita enviada desde el calendario.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        data = request.POST
        required_fields = ['paciente_id', 'medico_id', 'especialidad_id', 'fecha', 'hora']

        # ... (Validaciones y obtención de IDs) ...
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'success': False, 'error': f'Campo requerido faltante: {field}'}, status=400)

        paciente = Paciente.objects.get(id_Paciente=data['paciente_id'])
        medico = UsuarioMedico.objects.get(id_Medico=data['medico_id'], activo=True)
        especialidad = EspecialidadMedica.objects.get(id_Especialidad_Medica=data['especialidad_id'])

        # Crear datetime objects LOCALES
        fecha_hora_str = f"{data['fecha']} {data['hora']}"
        fecha_hora = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M")
        duracion = int(data.get('duracion', 30))
        fecha_hora_fin = fecha_hora + timedelta(minutes=duracion)

        # 🔑 HACER AWARE Y CONVERTIR A UTC PARA GUARDAR EN LA BD
        tz_local = timezone.get_current_timezone()
        fecha_hora_local_aware = timezone.make_aware(fecha_hora, tz_local)
        fecha_hora_fin_local_aware = timezone.make_aware(fecha_hora_fin, tz_local)

        # Guardar en UTC (el comportamiento estándar de Django)
        fecha_hora_aware = timezone.localtime(fecha_hora_local_aware, timezone=dt_timezone.utc)
        fecha_hora_fin_aware = timezone.localtime(fecha_hora_fin_local_aware, timezone=dt_timezone.utc)

        # Verificar que no haya conflicto con otra cita del mismo médico
        cita_existente = CitasReservadas.objects.filter(
            horario__medico=medico,
            start_datetime__lt=fecha_hora_fin_aware,
            end_datetime__gt=fecha_hora_aware,
            estado__in=['pendiente', 'confirmada']
        ).exists()

        if cita_existente:
            return JsonResponse({
                'success': False,
                'error': 'El horario seleccionado ya no está disponible. Por favor seleccione otro horario.'
            }, status=400)

        # Buscar un horario específico del médico y especialidad que cubra este slot
        horario_correspondiente = HorarioCita.objects.filter(
            medico=medico,
            especialidad=especialidad,
            activo=True
        ).first()

        if not horario_correspondiente:
            return JsonResponse({
                'success': False,
                'error': 'No se encontró un horario válido para este médico y especialidad.'
            }, status=400)

        # Crear la cita (se usa el valor UTC)
        cita = CitasReservadas.objects.create(
            paciente=paciente,
            horario=horario_correspondiente,
            start_datetime=fecha_hora_aware,
            end_datetime=fecha_hora_fin_aware,
            estado='pendiente',
            notas=data.get('notas', '')
        )

        print(f"✅ Cita creada exitosamente - ID: {cita.id}")

        return JsonResponse({
            'success': True,
            'message': 'Cita creada exitosamente',
            'cita_id': cita.id
        })

    except Paciente.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Paciente no encontrado'}, status=404)
    except UsuarioMedico.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Médico no encontrado'}, status=404)
    except EspecialidadMedica.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Especialidad no encontrada'}, status=404)
    except Exception as e:
        print(f"❌ Error al guardar cita: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# ---------------------------------------------------------------------
# 🔷 API: MÉDICOS POR ESPECIALIDAD
# ---------------------------------------------------------------------
@csrf_exempt
def medicos_por_especialidad(request):
    """
    API para obtener los médicos por especialidad
    """
    print("\n" + "="*60)
    print("🩺 SOLICITUD DE MÉDICOS POR ESPECIALIDAD")
    print("="*60)
    
    especialidad_id = request.GET.get('especialidad_id')
    print(f"🔍 ID de especialidad recibido: {especialidad_id}")
    
    if not especialidad_id:
        print("❌ Error: No se proporcionó el ID de la especialidad")
        return JsonResponse({'error': 'Se requiere el ID de la especialidad'}, status=400)
    
    try:
        # Obtener médicos activos con la especialidad seleccionada
        from .models import UsuarioMedico, EspecialidadMedica
        
        print(f"🔍 Buscando médicos para la especialidad ID: {especialidad_id}")
        
        # Verificar si la especialidad existe
        if not EspecialidadMedica.objects.filter(id_Especialidad_Medica=especialidad_id).exists():
            print(f"❌ La especialidad con ID {especialidad_id} no existe")
            return JsonResponse({'error': 'Especialidad no encontrada'}, status=404)
        
        # Obtener médicos con la especialidad
        medicos = UsuarioMedico.objects.filter(
            especialidades__id_Especialidad_Medica=especialidad_id,
            activo=True
        ).distinct()
        
        print(f"✅ Se encontraron {medicos.count()} médicos para la especialidad")
        
        # Preparar la lista de médicos para la respuesta
        medicos_list = [
            {
                'id_Medico': medico.id_Medico,
                'Nombres_Medico': medico.Nombres_Medico,
                'Apellidos_Medicos': medico.Apellidos_Medicos,
                'especialidades': [e.Espacialidad_Medica for e in medico.especialidades.all()]
            }
            for medico in medicos
        ]
        
        print(f"📋 Lista de médicos preparada: {medicos_list}")
        
        return JsonResponse({
            'success': True,
            'medicos': medicos_list
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al obtener los médicos: {str(e)}'
        }, status=500)


# ---------------------------------------------------------------------
# 📅 API: HORARIOS AGENDADOS DEL MÉDICO
# ---------------------------------------------------------------------
@csrf_exempt
def horarios_agendados_medico(request):
    """
    Devuelve los horarios con estado 'agendado' del médico en formato JSON.
    Similar a disponibilidad_medico pero solo para citas agendadas.
    """
    print("\n" + "=" * 60)
    print("📅 INICIANDO HORARIOS_AGENDADOS_MEDICO - EJECUTÁNDOSE AHORA")
    print("=" * 60)
    import time
    start_time = time.time()
    
    try:
        # Obtener parámetros de la URL
        medico_id = request.GET.get('medico_id')
        especialidad_id = request.GET.get('especialidad_id')
        fecha_inicio = request.GET.get('start')
        fecha_fin = request.GET.get('end')

        # Validar parámetros requeridos
        if not all([medico_id, especialidad_id, fecha_inicio, fecha_fin]):
            print(f"Parámetros recibidos - medico: {medico_id}, especialidad: {especialidad_id}, inicio: {fecha_inicio}, fin: {fecha_fin}")
            return JsonResponse({
                'success': False,
                'error': 'Seleccione una especialidad y un médico primero'
            }, status=400)

        # Validar y convertir fechas (FullCalendar envía formato ISO con zona horaria)
        try:
            # Obtener la zona horaria del request o usar la predeterminada
            tz_name = request.GET.get('timezone', 'America/Caracas')
            try:
                tz = pytz.timezone(tz_name)
            except (pytz.exceptions.UnknownTimeZoneError, AttributeError):
                tz = pytz.timezone('America/Caracas')
            
            print(f"🔵 Usando zona horaria: {tz.zone}")
            
            # Decodificar la codificación URL y analizar datetime con zona horaria
            fecha_inicio_str = fecha_inicio.replace('%3A', ':')
            fecha_fin_str = fecha_fin.replace('%3A', ':')
            
            # Parsear las fechas con zona horaria
            try:
                # Intentar analizar con la zona horaria incluida
                start_dt = datetime.strptime(fecha_inicio_str, '%Y-%m-%dT%H:%M:%S%z')
                end_dt = datetime.strptime(fecha_fin_str, '%Y-%m-%dT%H:%M:%S%z')
                
                # Convertir a la zona horaria de Caracas para consistencia
                start_dt = start_dt.astimezone(tz)
                end_dt = end_dt.astimezone(tz)
                
            except ValueError:
                # Si falla, intentar sin la zona horaria y asumir que está en la zona horaria del servidor
                start_dt = datetime.strptime(fecha_inicio_str.split('+')[0], '%Y-%m-%dT%H:%M:%S')
                end_dt = datetime.strptime(fecha_fin_str.split('+')[0], '%Y-%m-%dT%H:%M:%S')
                
                # Hacer las fechas conscientes de la zona horaria y convertir a Caracas
                server_tz = timezone.get_current_timezone()
                start_dt = timezone.make_aware(start_dt, server_tz).astimezone(tz)
                end_dt = timezone.make_aware(end_dt, server_tz).astimezone(tz)
            
            # Obtener solo la fecha para el procesamiento (en la zona horaria de Caracas)
            fecha_inicio_dt = start_dt.date()
            fecha_fin_dt = end_dt.date()
            
            print(f"✅ Fechas recibidas - Inicio: {start_dt} ({start_dt.tzinfo}), Fin: {end_dt} ({end_dt.tzinfo})")
            print(f"✅ Fechas convertidas - Inicio: {fecha_inicio_dt}, Fin: {fecha_fin_dt} (Zona horaria: {tz.zone})")
        
        except Exception as e:
            error_msg = f'Error al procesar fechas: {str(e)}. Formato esperado: YYYY-MM-DDTHH:MM:SS±HH:MM.'
            print(f"❌ {error_msg}")
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'error': error_msg
            }, status=400)

        # Obtener médico y especialidad
        try:
            medico = UsuarioMedico.objects.get(id_Medico=medico_id, activo=True)
            especialidad = EspecialidadMedica.objects.get(id_Especialidad_Medica=especialidad_id)
        except UsuarioMedico.DoesNotExist:
            error_msg = 'Médico no encontrado o inactivo'
            return JsonResponse({'success': False, 'error': error_msg}, status=404)
        except EspecialidadMedica.DoesNotExist:
            error_msg = 'Especialidad no encontrada'
            return JsonResponse({'success': False, 'error': error_msg}, status=404)

        # Definir el rango de búsqueda en la zona horaria local
        inicio_local = datetime.combine(fecha_inicio_dt, datetime.min.time())
        fin_local = datetime.combine(fecha_fin_dt, datetime.max.time())
        
        # Hacer que sean conscientes de la zona horaria
        inicio_local = timezone.make_aware(inicio_local, tz)
        fin_local = timezone.make_aware(fin_local, tz)
        
        # Convertir el rango de búsqueda a UTC para la consulta a la BD
        inicio_utc = inicio_local.astimezone(pytz.utc)
        fin_utc = fin_local.astimezone(pytz.utc)
        
        print(f"🕐 Rango de búsqueda Local: {inicio_local} a {fin_local}")
        print(f"🕐 Rango de búsqueda UTC (BD): {inicio_utc} a {fin_utc}")

        # Obtener todas las citas AGENDADAS del médico específico
        citas_agendadas = CitasReservadas.objects.filter(
            horario__medico__id_Medico=medico_id,
            estado='agendado',  # Solo citas con estado 'agendado'
            start_datetime__lt=fin_utc,
            end_datetime__gt=inicio_utc,
        ).select_related('horario')
        
        print(f"📅 Citas agendadas encontradas: {citas_agendadas.count()}")

        # Crear un diccionario de citas agendadas basado en la HORA LOCAL
        citas_agrupadas = {}
        
        for cita in citas_agendadas:
            # Convertir de UTC a la HORA LOCAL para la comparación
            start_local = timezone.localtime(cita.start_datetime, tz)
            end_local = timezone.localtime(cita.end_datetime, tz)

            fecha_str = start_local.strftime('%Y-%m-%d')
            
            if fecha_str not in citas_agrupadas:
                citas_agrupadas[fecha_str] = []
            
            # Agregar la cita al diccionario
            citas_agrupadas[fecha_str].append({
                'start': start_local.strftime('%H:%M'),
                'end': end_local.strftime('%H:%M'),
                'titulo': f"Agendado - {start_local.strftime('%H:%M')}",
                'start_iso': start_local.isoformat(),
                'end_iso': end_local.isoformat()
            })
            
            print(f"📅 Cita agendada: {fecha_str} de {start_local.strftime('%H:%M')} a {end_local.strftime('%H:%M')}")
                
        print(f"📅 Citas agrupadas por fecha: {citas_agrupadas.keys()}")

        # Crear el array de events para FullCalendar
        events = []
        for fecha, citas in citas_agrupadas.items():
            for cita in citas:
                events.append({
                    'title': cita['titulo'],
                    'start': cita['start_iso'],
                    'end': cita['end_iso'],
                    'allDay': False,
                    'backgroundColor': '#495057',  # Gris oscuro
                    'borderColor': '#343a40',      # Gris más oscuro para el borde
                    'textColor': 'white',          # Texto en blanco para mejor contraste
                    'display': 'block',
                    'extendedProps': {
                        'estado': 'agendado',
                        'fecha': fecha,
                        'hora': cita['start']
                    }
                })

        response_data = {
            'success': True,
            'events': events,
            'medico': f'{medico.Nombres_Medico} {medico.Apellidos_Medicos}',
            'especialidad': especialidad.Espacialidad_Medica,
            'rango_fechas': {
                'inicio': fecha_inicio,
                'fin': fecha_fin
            },
            'total_citas': len(events),
            'debug_info': {
                'citas_agendadas': citas_agendadas.count(),
                'fechas_con_citas': len(citas_agrupadas)
            }
        }

        print(f"✅ Respuesta enviada: {response_data['total_citas']} citas agendadas")
        print("=" * 60)

        return JsonResponse(response_data)

    except Exception as e:
        error_msg = f"Error al procesar la solicitud: {str(e)}\n\n{traceback.format_exc()}"
        print(f"❌ ERROR CRÍTICO: {error_msg}")
        return JsonResponse({
            'success': False,
            'error': 'Error interno del servidor al obtener los horarios agendados',
            'details': str(e)
        }, status=500)
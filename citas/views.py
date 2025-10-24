# citas/views.py
import logging
import traceback

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from datetime import datetime

from .forms import RegistroPacienteForm
from .models import (
    Ciudad, Municipio, Parroquia, Estado, Pais,
    EspecialidadMedica, HorarioCita, MedicoEspecialidad
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
from dateutil import rrule # Importar rrule
from datetime import datetime, timedelta  # ✅ Agregar timedelta
import pytz
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
from django.core import serializers
import json

# -------------------------------------------------------------
# VISTAS PRINCIPALES
# -------------------------------------------------------------

def registrar_paciente(request):
    if request.method == 'POST':
        form = RegistroPacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('citas:lista_pacientes') # Ajusta el nombre de la URL según tu configuración
    else:
        form = RegistroPacienteForm()
    
    return render(request, 'citas/registro.html', {
        'form': form,
        'titulo': 'Registro de Paciente'
    })

# -------------------------------------------------------------
# VISTA AJAX PARA COMBOS DEPENDIENTES (CORREGIDA)
# -------------------------------------------------------------

@require_http_methods(["GET"])
def load_estados(request):
    pais_id = request.GET.get('pais_id')
    if not pais_id:
        return JsonResponse({'error': 'Se requiere el ID del país'}, status=400)
    
    estados = Estado.objects.filter(pais_id=pais_id).order_by('nombre')
    data = [{'id': e.id_Estado, 'nombre': e.nombre} for e in estados]
    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def load_ciudades(request):
    estado_id = request.GET.get('estado_id')
    if not estado_id:
        return JsonResponse({'error': 'Se requiere el ID del estado'}, status=400)
    
    ciudades = Ciudad.objects.filter(estado_id=estado_id).order_by('nombre')
    data = [{'id': c.id_Ciudad, 'nombre': c.nombre} for c in ciudades]
    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def load_municipios(request):
    estado_id = request.GET.get('estado_id')
    if not estado_id:
        return JsonResponse({'error': 'Se requiere el ID del estado'}, status=400)
    
    municipios = Municipio.objects.filter(estado_id=estado_id).order_by('nombre')
    data = [{'id': m.id_Municipio, 'nombre': m.nombre} for m in municipios]
    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def load_parroquias(request):
    municipio_id = request.GET.get('municipio_id')
    if not municipio_id:
        return JsonResponse({'error': 'Se requiere el ID del municipio'}, status=400)
    
    parroquias = Parroquia.objects.filter(municipio_id=municipio_id).order_by('nombre')
    data = [{'id': p.id_Parroquia, 'nombre': p.nombre} for p in parroquias]
    return JsonResponse(data, safe=False)

def cargar_ubicaciones(request):
    tipo = request.GET.get('tipo')
    estado_id = request.GET.get('estado_id')
    municipio_id = request.GET.get('municipio_id')
    
    try:
        if tipo not in ['ciudades', 'municipios', 'parroquias']:
            return JsonResponse({'error': f'Tipo de ubicación no válido: {tipo}. Use "ciudades", "municipios" o "parroquias".'}, status=400)
        
        items = []

        if tipo == 'ciudades':
            if not estado_id or not estado_id.isdigit():
                return JsonResponse({'error': 'Se requiere el ID del estado para cargar ciudades'}, status=400)
            ciudades = Ciudad.objects.filter(estado_id=int(estado_id)).order_by('nombre')
            items = [{'id': c.id_Ciudad, 'nombre': c.nombre} for c in ciudades]

        elif tipo == 'municipios':
            if not estado_id or not estado_id.isdigit():
                return JsonResponse({'error': 'Se requiere el ID del estado'}, status=400)
            municipios = Municipio.objects.filter(estado_id=int(estado_id)).order_by('nombre')
            items = [{'id': m.id_Municipio, 'nombre': m.nombre} for m in municipios]
            
        elif tipo == 'parroquias':
            if not municipio_id or not municipio_id.isdigit():
                return JsonResponse({'error': 'Se requiere el ID del municipio'}, status=400)
            parroquias = Parroquia.objects.filter(municipio_id=int(municipio_id)).order_by('nombre')
            items = [{'id': p.id_Parroquia, 'nombre': p.nombre} for p in parroquias]
        
        return JsonResponse(items, safe=False)
            
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        return JsonResponse({
            'error': 'Error interno del servidor', 
            'details': str(e),
            'traceback': error_traceback
        }, status=500)

def listar_especialidades(request):
    especialidades = EspecialidadMedica.objects.all().order_by('id_Especialidad_Medica')
    return render(request, 'citas/especialidad/listar.html', {'especialidades': especialidades})

def crear_especialidad(request):
    if request.method == 'POST':
        form = EspecialidadMedicaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialidad creada exitosamente.')
            return redirect('listar_especialidades')
    else:
        form = EspecialidadMedicaForm()
    return render(request, 'citas/especialidad/form.html', {'form': form, 'accion': 'Crear'})

def editar_especialidad(request, id):
    especialidad = get_object_or_404(EspecialidadMedica, pk=id)
    if request.method == 'POST':
        form = EspecialidadMedicaForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialidad actualizada exitosamente.')
            return redirect('listar_especialidades')
    else:
        form = EspecialidadMedicaForm(instance=especialidad)
    return render(request, 'citas/especialidad/form.html', {'form': form, 'accion': 'Editar'})

def eliminar_especialidad(request, id):
    especialidad = get_object_or_404(EspecialidadMedica, pk=id)
    if request.method == 'POST':
        especialidad.delete()
        messages.success(request, 'Especialidad eliminada exitosamente.')
        return redirect('listar_especialidades')
    return render(request, 'citas/especialidad/eliminar.html', {'especialidad': especialidad})

class UsuarioMedicoListView(LoginRequiredMixin, ListView):
    model = UsuarioMedico
    template_name = 'citas/usuariomedico/listar.html'
    context_object_name = 'medicos'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'Prefijo_CIDNI', 'Sexo', 'Pais', 'estado', 'ciudad', 'municipio', 'parroquia'
        )
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(Nombres_Medico__icontains=search) |
                Q(Apellidos_Medicos__icontains=search) |
                Q(CIDNI__icontains=search) |
                Q(Registro_MPPS__icontains=search)
            )
        return queryset.order_by('Apellidos_Medicos', 'Nombres_Medico')

class UsuarioMedicoCreateView(LoginRequiredMixin, CreateView):
    model = UsuarioMedico
    form_class = UsuarioMedicoForm
    template_name = 'citas/usuariomedico/form.html'
    success_url = reverse_lazy('listar_medicos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_seniat'] = DatosSeniatForm()
        context['titulo'] = 'Nuevo Médico'
        return context

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.save()
            
            # Guardar datos SENIAT si existen
            form_seniat = DatosSeniatForm(self.request.POST)
            if form_seniat.is_valid() and form_seniat.cleaned_data.get('RIF'):
                datos_seniat = form_seniat.save(commit=False)
                datos_seniat.Medico = self.object
                datos_seniat.save()
            
            messages.success(self.request, 'Médico creado exitosamente.')
            return super().form_valid(form)

class UsuarioMedicoUpdateView(LoginRequiredMixin, UpdateView):
    model = UsuarioMedico
    form_class = UsuarioMedicoForm
    template_name = 'citas/usuariomedico/form.html'
    success_url = reverse_lazy('listar_medicos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['form_seniat'] = DatosSeniatForm(instance=self.object.datos_seniat.first())
        except:
            context['form_seniat'] = DatosSeniatForm()
        context['titulo'] = f'Editar Médico: {self.object}'
        return context

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            
            # Actualizar o crear datos SENIAT
            form_seniat = DatosSeniatForm(
                self.request.POST,
                instance=self.object.datos_seniat.first() or None
            )
            if form_seniat.is_valid() and form_seniat.cleaned_data.get('RIF'):
                datos_seniat = form_seniat.save(commit=False)
                datos_seniat.Medico = self.object
                datos_seniat.save()
            elif form_seniat.is_valid() and self.object.datos_seniat.exists():
                # Si el RIF está vacío y existen datos SENIAT, eliminarlos
                self.object.datos_seniat.all().delete()
            
            messages.success(self.request, 'Médico actualizado exitosamente.')
            return super().form_valid(form)

class UsuarioMedicoDeleteView(LoginRequiredMixin, DeleteView):
    model = UsuarioMedico
    template_name = 'citas/usuariomedico/eliminar.html'
    success_url = reverse_lazy('listar_medicos')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Médico eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

class MedicoEspecialidadListView(ListView):
    model = MedicoEspecialidad
    template_name = 'citas/medicoEspecialidad/listar.html'
    context_object_name = 'especialidades_medicos'

    def get_queryset(self):
        return MedicoEspecialidad.objects.select_related('medico', 'especialidad').order_by('medico__Apellidos_Medicos', 'especialidad__nombre')

class MedicoEspecialidadCreateView(CreateView):
    model = MedicoEspecialidad
    form_class = MedicoEspecialidadForm
    template_name = 'citas/medicoEspecialidad/form.html'
    success_url = reverse_lazy('citas:medico_especialidad_list')

    def form_valid(self, form):
        messages.success(self.request, 'La especialidad del médico se ha creado correctamente.')
        return super().form_valid(form)

class MedicoEspecialidadUpdateView(UpdateView):
    model = MedicoEspecialidad
    form_class = MedicoEspecialidadForm
    template_name = 'citas/medicoEspecialidad/form.html'
    success_url = reverse_lazy('citas:medico_especialidad_list')

    def form_valid(self, form):
        messages.success(self.request, 'La especialidad del médico se ha actualizado correctamente.')
        return super().form_valid(form)

class MedicoEspecialidadDeleteView(DeleteView):
    model = MedicoEspecialidad
    template_name = 'citas/medicoEspecialidad/eliminar.html'
    success_url = reverse_lazy('citas:medico_especialidad_list')
    paginate_by = 10

def get_especialidades_medico(request, medico_id):
    try:
        # Obtener las especialidades del médico
        especialidades = MedicoEspecialidad.objects.filter(
            medico_id=medico_id, 
            activo=True
        ).select_related('especialidad').values(
            'especialidad__id_Especialidad_Medica', 
            'especialidad__Espacialidad_Medica'
        )
        
        # Renombrar las claves para que sean más amigables
        especialidades_list = [
            {
                'id': e['especialidad__id_Especialidad_Medica'],
                'nombre': e['especialidad__Espacialidad_Medica']
            }
            for e in especialidades
        ]
        
        # Obtener el horario del médico para cada especialidad
        horarios_especialidades = []
        for esp in especialidades_list:
            # Llamar a la función que ya tenemos para obtener los horarios
            from django.urls import reverse
            from django.test import RequestFactory
            from rest_framework.test import force_authenticate
            
            # Crear una solicitud simulada
            factory = RequestFactory()
            url = reverse('citas:get_horarios_medico_especialidad', 
                         args=[medico_id, esp['id']])
            req = factory.get(url)
            
            # Llamar a la vista de horarios
            from .views import get_horarios_medico_especialidad
            response = get_horarios_medico_especialidad(req, medico_id, esp['id'])
            
            # Si la respuesta es exitosa, obtener el mensaje de horario
            mensaje_horario = ''
            if hasattr(response, 'data') and 'mensaje_horario' in response.data:
                mensaje_horario = response.data['mensaje_horario']
            
            # Agregar el mensaje de horario a la especialidad
            esp['mensaje_horario'] = mensaje_horario
            horarios_especialidades.append(esp)
        
        # Retornar la lista de especialidades con sus horarios
        return JsonResponse({
            'especialidades': especialidades_list,
            'mensajes_horario': {e['id']: e.get('mensaje_horario', '') for e in horarios_especialidades}
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

class BancoListView(ListView):
    model = Banco
    template_name = 'citas/banco_list.html'
    context_object_name = 'bancos'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(codigo__icontains=search)
            )
        return queryset.order_by('nombre')

class BancoCreateView(CreateView):
    model = Banco
    form_class = BancoForm
    template_name = 'citas/banco_form.html'
    success_url = reverse_lazy('citas:banco_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Banco creado exitosamente.')
        return super().form_valid(form)

class BancoUpdateView(UpdateView):
    model = Banco
    form_class = BancoForm
    template_name = 'citas/banco_form.html'
    success_url = reverse_lazy('citas:banco_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Banco actualizado exitosamente.')
        return super().form_valid(form)

class BancoDeleteView(DeleteView):
    model = Banco
    template_name = 'citas/banco_confirm_delete.html'
    success_url = reverse_lazy('citas:banco_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Banco eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

# -------------------------------------------------------------
# VISTAS PARA OBTENER DATOS VIA AJAX
# -------------------------------------------------------------

def obtener_pacientes(request):
    """
    Vista para obtener la lista de pacientes activos en formato JSON
    """
    from .models import Paciente
    
    try:
        pacientes = Paciente.objects.filter(Activo=True).values('id_Paciente', 'Nombres_Paciente', 'Apellidos_Paciente')
        pacientes_list = list(pacientes)
        return JsonResponse({'pacientes': pacientes_list}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def obtener_medicos(request):
    """
    Vista para obtener la lista de médicos activos en formato JSON
    """
    from .models import UsuarioMedico
    
    try:
        medicos = UsuarioMedico.objects.filter(activo=True).values(
            'id_Medico', 
            'Nombres_Medico', 
            'Apellidos_Medicos'
        )
        medicos_list = list(medicos)
        return JsonResponse({'medicos': medicos_list}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# -------------------------------------------------------------
# VISTAS DE AGENDA Y CALENDARIO
# -------------------------------------------------------------

def calendario_view(request):
    from .models import Paciente, UsuarioMedico, EspecialidadMedica, Cita
    import json
    from datetime import timedelta
    
    # Obtener datos básicos para el formulario
    pacientes = Paciente.objects.filter(Activo=True).order_by('Apellidos_Paciente', 'Nombres_Paciente')
    medicos = UsuarioMedico.objects.filter(activo=True).order_by('Apellidos_Medicos', 'Nombres_Medico')
    especialidades = EspecialidadMedica.objects.all().order_by('Espacialidad_Medica')
    
    # Obtener citas para el calendario
    citas = Cita.objects.select_related('paciente', 'medico', 'especialidad').all()
    
    # Preparar los eventos para el calendario
    eventos = []
    for cita in citas:
        eventos.append({
            'id': cita.id,
            'title': f"{cita.paciente.Nombres_Paciente} {cita.paciente.Apellidos_Paciente}",
            'start': cita.fecha_hora.isoformat(),
            'end': (cita.fecha_hora + timedelta(minutes=cita.duracion)).isoformat(),
            'estado': cita.estado,
            'paciente': f"{cita.paciente.Nombres_Paciente} {cita.paciente.Apellidos_Paciente}",
            'medico': f"{cita.medico.Nombres_Medico} {cita.medico.Apellidos_Medicos}",
            'especialidad': cita.especialidad.Espacialidad_Medica if cita.especialidad else '',
            'notas': cita.notas or '',
            'color': get_estado_color(cita.estado)
        })
    
    # Convertir a JSON seguro para JavaScript
    eventos_json = json.dumps(eventos, ensure_ascii=False)
    
    context = {
        'pacientes': pacientes,
        'medicos': medicos,
        'especialidades': especialidades,
        'eventos_json': eventos_json,
        'opts': {'app_label': 'citas'},
        'is_popup': False,
        'has_permission': True,
        'site_url': '/',
        'site_title': 'Calendario',
        'title': 'Calendario de Citas'
    }
    
    return render(request, 'citas/reservas/calendario.html', context)

@csrf_exempt
def crear_cita(request):
    """
    Vista para crear una nueva cita en la tabla citas_reservadas.
    """
    print("\n=== INICIO DE LA SOLICITUD CREAR_CITA ===")
    print(f"Método de la solicitud: {request.method}")
    print(f"Headers: {request.headers}")
    print(f"Cuerpo de la solicitud (raw): {request.body}")
    
    if request.method != 'POST':
        error_msg = f'Método no permitido: {request.method}'
        print(f"ERROR: {error_msg}")
        return JsonResponse({'error': error_msg}, status=405)
    
    try:
        # Imprimir el cuerpo de la solicitud para depuración
        print("\n=== DATOS RECIBIDOS ===")
        print("Cuerpo de la solicitud (raw):", request.body)
        
        try:
            data = json.loads(request.body)
            print("Datos parseados:", json.dumps(data, indent=2, default=str))
        except json.JSONDecodeError as e:
            error_msg = f'Error al decodificar JSON: {str(e)}'
            print(f"ERROR: {error_msg}")
            return JsonResponse({'error': error_msg}, status=400)
        
        # Validar datos requeridos
        required_fields = ['paciente_id', 'medico_id', 'especialidad_id', 'fecha_hora', 'duracion']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            error_msg = f'Faltan campos requeridos: {missing_fields}'
            print(f"ERROR: {error_msg}")
            print("Campos recibidos:", list(data.keys()))
            return JsonResponse({'error': error_msg, 'missing_fields': missing_fields}, status=400)
            
        print("\n=== VALIDACIÓN DE CAMPOS ===")
        print("Todos los campos requeridos están presentes")
        
        from datetime import datetime, timedelta
        from django.utils import timezone
        from .models import CitasReservadas, HorarioCita, Paciente, UsuarioMedico, EspecialidadMedica
        
        # Obtener los objetos relacionados
        try:
            print("\n=== BUSCANDO REGISTROS EN LA BASE DE DATOS ===")
            print(f"Buscando paciente con ID: {data['paciente_id']}")
            paciente = Paciente.objects.get(id_Paciente=data['paciente_id'])
            print(f"Paciente encontrado: {paciente.Nombres_Paciente} {paciente.Apellidos_Paciente}")
            
            print(f"\nBuscando médico con ID: {data['medico_id']}")
            medico = UsuarioMedico.objects.get(id_Medico=data['medico_id'])
            print(f"Médico encontrado: {medico.Nombres_Medico} {medico.Apellidos_Medicos}")
            
            print(f"\nBuscando especialidad con ID: {data['especialidad_id']}")
            especialidad = EspecialidadMedica.objects.get(id_Especialidad_Medica=data['especialidad_id'])
            print(f"Especialidad encontrada: {especialidad.Espacialidad_Medica}")
            
        except Paciente.DoesNotExist:
            error_msg = f'No se encontró el paciente con ID: {data["paciente_id"]}'
            print(f"ERROR: {error_msg}")
            return JsonResponse({'error': error_msg}, status=404)
        except UsuarioMedico.DoesNotExist:
            error_msg = f'No se encontró el médico con ID: {data["medico_id"]}'
            print(f"ERROR: {error_msg}")
            return JsonResponse({'error': error_msg}, status=404)
        except EspecialidadMedica.DoesNotExist:
            error_msg = f'No se encontró la especialidad con ID: {data["especialidad_id"]}'
            print(f"ERROR: {error_msg}")
            return JsonResponse({'error': error_msg}, status=404)
        except Exception as e:
            error_msg = f'Error al obtener datos: {str(e)}'
            print(f"ERROR: {error_msg}")
            return JsonResponse({'error': error_msg}, status=400)
        
        # Convertir la fecha y hora de string a objeto datetime
        try:
            print("\n=== PROCESANDO FECHA Y HORA ===")
            print(f"Fecha/hora recibida: {data['fecha_hora']}")
            print(f"Duración recibida: {data['duracion']} minutos")
            
            # Intentar con diferentes formatos de fecha
            fecha_hora_str = data['fecha_hora']
            formatos_fecha = [
                '%Y-%m-%dT%H:%M',  # Formato estándar
                '%Y-%m-%d %H:%M',  # Formato alternativo
                '%Y-%m-%dT%H:%M:%S',  # Con segundos
                '%Y-%m-%d %H:%M:%S',  # Con segundos y espacio
                '%Y-%m-%dT%H:%M:%S.%fZ'  # Formato ISO con milisegundos y Z
            ]
            
            fecha_hora = None
            for formato in formatos_fecha:
                try:
                    fecha_hora = datetime.strptime(fecha_hora_str, formato)
                    break
                except ValueError:
                    continue
            
            if fecha_hora is None:
                raise ValueError(f"No se pudo parsear la fecha: {fecha_hora_str}")
                
            # Asegurarse de que la fecha sea consciente de la zona horaria
            if timezone.is_naive(fecha_hora):
                fecha_hora = timezone.make_aware(fecha_hora)
            
            duracion = int(data['duracion'])
            fecha_hora_fin = fecha_hora + timedelta(minutes=duracion)
            
            print(f"Fecha/hora convertida: {fecha_hora}")
            print(f"Fecha/hora de fin: {fecha_hora_fin}")
            print(f"Zona horaria: {fecha_hora.tzinfo}")
            
        except ValueError as e:
            error_msg = f'Formato de fecha o duración inválido: {str(e)}. Formato esperado: YYYY-MM-DDTHH:MM'
            print(f"ERROR: {error_msg}")
            return JsonResponse({'error': error_msg}, status=400)
        except TypeError as e:
            error_msg = f'Tipo de dato inválido: {str(e)}'
            print(f"ERROR: {error_msg}")
            return JsonResponse({'error': error_msg}, status=400)
        except Exception as e:
            error_msg = f'Error al procesar la fecha: {str(e)}'
            print(f"ERROR: {error_msg}")
            import traceback
            print(traceback.format_exc())
            return JsonResponse({'error': error_msg}, status=400)
        
        # Crear el horario de cita si no existe
        print("\n=== CREANDO O OBTENIENDO HORARIO DE CITA ===")
        try:
            horario, created = HorarioCita.objects.get_or_create(
                medico=medico,
                especialidad=especialidad,
                defaults={
                    'start_datetime': fecha_hora,
                    'end_datetime': fecha_hora_fin,
                    'activo': True,
                    'notas': data.get('notas', '')
                }
            )
            
            if created:
                print(f"Nuevo horario creado con ID: {horario.id}")
            else:
                print(f"Horario existente encontrado con ID: {horario.id}")
                
        except Exception as e:
            error_msg = f'Error al crear/obtener el horario: {str(e)}'
            print(f"ERROR: {error_msg}")
            return JsonResponse({'error': error_msg}, status=500)
        
        # Verificar si ya existe una cita en ese horario
        print("\n=== VERIFICANDO CITAS EXISTENTES ===")
        try:
            # Verificar si hay citas que se solapen con el horario solicitado
            cita_existente = CitasReservadas.objects.filter(
                horario=horario,
                paciente=paciente,
                start_datetime__lt=fecha_hora_fin,
                end_datetime__gt=fecha_hora
            ).exists()
            
            if cita_existente:
                error_msg = 'Ya existe una cita programada para este paciente que se solapa con el horario solicitado'
                print(f"ERROR: {error_msg}")
                return JsonResponse({
                    'error': error_msg,
                    'success': False
                }, status=400)
                
            print("No se encontraron citas duplicadas o solapadas")
                
        except Exception as e:
            error_msg = f'Error al verificar citas existentes: {str(e)}'
            print(f"ERROR: {error_msg}")
            return JsonResponse({'error': error_msg}, status=500)
            
        # Crear la cita reservada
        print("\n=== CREANDO NUEVA CITA ===")
        try:
            cita_data = {
                'horario': horario,
                'paciente': paciente,
                'start_datetime': fecha_hora,
                'end_datetime': fecha_hora_fin,
                'estado': 'pendiente',
                'nota': data.get('notas', ''),  # Asegurando que el campo coincida con el modelo
                'costo': float(data.get('costo', 0.00)) if data.get('costo') else 0.00
            }
            
            # Asegurarse de que los campos requeridos no sean None
            for field in ['horario', 'paciente', 'start_datetime', 'end_datetime']:
                if cita_data[field] is None:
                    error_msg = f'El campo {field} es requerido y no puede ser nulo'
                    print(f"ERROR: {error_msg}")
                    return JsonResponse({'error': error_msg}, status=400)
            
            print("Datos para crear la cita:", json.dumps({
                'horario_id': horario.id,
                'paciente_id': paciente.id_Paciente,
                'start_datetime': fecha_hora.isoformat(),
                'end_datetime': fecha_hora_fin.isoformat(),
                'estado': 'pendiente',
                'nota': data.get('notas', ''),
                'costo': float(data.get('costo', 0.00)) if data.get('costo') else 0.00
            }, indent=2, default=str))
            
            try:
                cita = CitasReservadas.objects.create(**cita_data)
                
                print(f"Cita creada exitosamente - ID: {cita.id}")
                print(f"Paciente: {paciente.Nombres_Paciente} {paciente.Apellidos_Paciente}")
                print(f"Médico: {medico.Nombres_Medico} {medico.Apellidos_Medicos}")
                print(f"Especialidad: {especialidad.Espacialidad_Medica}")
                print(f"Fecha/Hora: {fecha_hora} - {fecha_hora_fin}")
                
                # Retornar respuesta de éxito
                return JsonResponse({
                    'success': True,
                    'message': 'Cita creada exitosamente',
                    'cita_id': cita.id
                })
                
            except Exception as e:
                error_msg = f'Error al guardar la cita en la base de datos: {str(e)}'
                print(f"ERROR: {error_msg}")
                print(f"Tipo de error: {type(e).__name__}")
                if hasattr(e, '__traceback__'):
                    import traceback
                    print("Traceback:", ''.join(traceback.format_tb(e.__traceback__)))
                return JsonResponse({'error': error_msg}, status=500)
            
            response_data = {
                'success': True,
                'cita_id': cita.id,
                'message': 'Cita creada exitosamente',
                'data': {
                    'paciente': f"{paciente.Nombres_Paciente} {paciente.Apellidos_Paciente}",
                    'medico': f"{medico.Nombres_Medico} {medico.Apellidos_Medicos}",
                    'especialidad': str(especialidad.Espacialidad_Medica),
                    'fecha_hora': fecha_hora.strftime('%Y-%m-%d %H:%M'),
                    'duracion': duracion,
                    'estado': 'pendiente'
                }
            }
            
            print("\n=== RESPUESTA DEL SERVIDOR ===")
            print(json.dumps(response_data, indent=2, default=str))
            
            return JsonResponse(response_data)
            
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            error_msg = f'Error al crear la cita: {str(e)}'
            print(f"\n=== ERROR AL CREAR LA CITA ===")
            print(error_msg)
            print("\nTraza de error:", error_trace)
            
            response_data = {
                'error': 'Error al crear la cita',
                'details': str(e),
                'trace': error_trace if settings.DEBUG else None
            }
            
            print("\n=== RESPUESTA DE ERROR ===")
            print(json.dumps(response_data, indent=2, default=str))
            
            return JsonResponse(response_data, status=500)
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        error_msg = f'Error inesperado en crear_cita: {str(e)}'
        print(f"\n=== ERROR INESPERADO ===")
        print(error_msg)
        print("\nTraza de error:", error_trace)
        
        response_data = {
            'error': 'Error inesperado al procesar la solicitud',
            'details': str(e),
            'trace': error_trace if settings.DEBUG else None
        }
        
        print("\n=== RESPUESTA DE ERROR INESPERADO ===")
        print(json.dumps(response_data, indent=2, default=str))
        return JsonResponse(response_data, status=500)

def obtener_eventos(request):
    """
    Vista para obtener los eventos del calendario en formato JSON.
    """
    from .models import Cita
    
    try:
        # Obtener parámetros de filtrado (opcional)
        start = request.GET.get('start')
        end = request.GET.get('end')
        
        # Construir el queryset base
        queryset = Cita.objects.select_related('paciente', 'medico__usuario', 'especialidad')
        
        # Filtrar por rango de fechas si se proporciona
        if start and end:
            queryset = queryset.filter(
                fecha_hora__gte=start,
                fecha_hora__lte=end
            )
        
        # Convertir a formato FullCalendar
        eventos = []
        for cita in queryset:
            eventos.append({
                'id': cita.id,
                'title': f"{cita.paciente.nombres} {cita.paciente.apellidos}",
                'start': cita.fecha_hora.isoformat(),
                'end': (cita.fecha_hora + datetime.timedelta(minutes=cita.duracion)).isoformat(),
                'extendedProps': {
                    'paciente': f"{cita.paciente.nombres} {cita.paciente.apellidos}",
                    'medico': cita.medico.usuario.get_full_name() if cita.medico.usuario else str(cita.medico),
                    'especialidad': cita.especialidad.Espacialidad_Medica if cita.especialidad else '',
                    'estado': cita.estado,
                    'notas': cita.notas or '',
                },
                'color': get_estado_color(cita.estado),
                'textColor': '#ffffff'
            })
        
        return JsonResponse(eventos, safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_estado_color(estado):
    """Devuelve un color según el estado de la cita"""
    colores = {
        'Pendiente': '#ffc107',  # Amarillo
        'Confirmada': '#28a745',  # Verde
        'Cancelada': '#dc3545',   # Rojo
        'Completada': '#17a2b8',  # Azul claro
    }
    return colores.get(estado, '#6c757d')  # Gris por defecto

def agenda_medico(request):
    # Renderiza la plantilla del calendario.
    return render(request, 'citas/agenda/agenda_medico.html')

def guardar_cita(request):
    """
    Vista para guardar una nueva cita en la tabla citas_reservadas
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        from django.utils import timezone
        from datetime import timedelta
        from .models import CitasReservadas, HorarioCita, Paciente, UsuarioMedico
        
        # Obtener datos del formulario
        paciente_id = request.POST.get('paciente')
        medico_id = request.POST.get('medico')
        fecha_hora = request.POST.get('fecha_hora')
        duracion = int(request.POST.get('duracion', 30))  # 30 minutos por defecto
        notas = request.POST.get('notas', '')
        costo = request.POST.get('costo', '0.00')
        
        # Validaciones básicas
        if not all([paciente_id, medico_id, fecha_hora]):
            return JsonResponse(
                {'error': 'Faltan campos requeridos: paciente, médico o fecha/hora'}, 
                status=400
            )
        
        # Convertir la fecha/hora al formato correcto
        try:
            fecha_hora_dt = datetime.strptime(fecha_hora, '%Y-%m-%dT%H:%M')
            fecha_hora_dt = timezone.make_aware(fecha_hora_dt)
            fecha_fin_dt = fecha_hora_dt + timedelta(minutes=duracion)
        except (ValueError, TypeError) as e:
            return JsonResponse(
                {'error': f'Formato de fecha inválido: {str(e)}'}, 
                status=400
            )
        
        # Obtener el paciente y el médico
        try:
            paciente = Paciente.objects.get(id_Paciente=paciente_id)
            medico = UsuarioMedico.objects.get(id_Medico=medico_id)
        except (Paciente.DoesNotExist, UsuarioMedico.DoesNotExist) as e:
            return JsonResponse(
                {'error': 'Paciente o médico no encontrado'}, 
                status=404
            )
        
        # Buscar un horario existente o crear uno temporal
        # En una implementación real, deberías tener un horario existente
        # Aquí creamos uno temporal para el ejemplo
        horario = HorarioCita.objects.filter(
            medico=medico,
            start_datetime__lte=fecha_hora_dt,
            end_datetime__gte=fecha_fin_dt,
            activo=True
        ).first()
        
        if not horario:
            # Si no hay un horario existente, creamos uno temporal
            # En producción, deberías manejar esto de manera diferente
            horario = HorarioCita(
                medico=medico,
                especialidad=medico.especialidades.first(),  # Tomar la primera especialidad del médico
                turno_id=1,  # Asignar un turno por defecto
                start_datetime=fecha_hora_dt,
                end_datetime=fecha_fin_dt,
                activo=True
            )
            horario.save()
        
        # Crear la cita reservada
        cita = CitasReservadas(
            horario=horario,
            paciente=paciente,
            start_datetime=fecha_hora_dt,
            end_datetime=fecha_fin_dt,
            estado='pendiente',
            nota=notas,
            costo=costo
        )
        cita.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cita guardada exitosamente',
            'cita_id': cita.id
        })
        
    except Exception as e:
        import traceback
        return JsonResponse(
            {
                'error': 'Error al guardar la cita',
                'details': str(e),
                'trace': traceback.format_exc()
            }, 
            status=500
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_horarios_medico_especialidad(request, medico_id, especialidad_id):
    """
    Obtiene los horarios disponibles para un médico y especialidad específicos.
    """
    # Importaciones necesarias
    from django.utils import timezone
    import pytz
    from citas.models import UsuarioMedico, EspecialidadMedica, HorarioCita, MedicoEspecialidad
    
    logger = logging.getLogger(__name__)
    logger.info(f'[HORARIOS] Iniciando búsqueda de horarios para médico_id={medico_id}, especialidad_id={especialidad_id}')
    
    try:
        # Validar parámetros de entrada
        try:
            medico_id = int(medico_id)
            especialidad_id = int(especialidad_id)
        except (ValueError, TypeError) as e:
            logger.error(f'[HORARIOS] Error en los parámetros: {str(e)}')
            return Response({
                'error': 'Los parámetros proporcionados no son válidos.',
                'sugerencia': 'Asegúrese de proporcionar IDs numéricos válidos.',
                'codigo_error': 'PARAMETROS_INVALIDOS'
            }, status=400)
        
        # Obtener la fecha actual
        ahora = timezone.now()
        logger.info(f'[HORARIOS] Fecha actual: {ahora}')
        
        # 1. Verificar que la especialidad exista
        try:
            especialidad = EspecialidadMedica.objects.get(id_Especialidad_Medica=especialidad_id)
            logger.debug(f'[HORARIOS] Especialidad encontrada: {especialidad.Espacialidad_Medica}')
        except EspecialidadMedica.DoesNotExist:
            logger.warning(f'[HORARIOS] Especialidad no encontrada: {especialidad_id}')
            return Response({
                'error': 'La especialidad seleccionada no existe.',
                'sugerencia': 'Por favor, seleccione otra especialidad.',
                'codigo_error': 'ESPECIALIDAD_NO_ENCONTRADA'
            }, status=400)
            
        # 2. Verificar si el médico existe
        try:
            medico = UsuarioMedico.objects.get(id_Medico=medico_id, activo=True)
            logger.debug(f'[HORARIOS] Médico encontrado: {medico.Nombres_Medico} {medico.Apellidos_Medicos}')
        except UsuarioMedico.DoesNotExist:
            logger.error(f'[HORARIOS] No se encontró el médico con ID: {medico_id}')
            return Response({
                'error': 'El médico especificado no existe o no está activo.',
                'sugerencia': 'Por favor, seleccione otro médico.',
                'codigo_error': 'MEDICO_NO_ENCONTRADO'
            }, status=404)
            
        # 3. Verificar si el médico tiene la especialidad asignada
        try:
            MedicoEspecialidad.objects.get(
                medico=medico,
                especialidad=especialidad,
                activo=True
            )
            logger.debug('[HORARIOS] Relación médico-especialidad validada')
        except MedicoEspecialidad.DoesNotExist:
            logger.warning(f'[HORARIOS] El médico {medico_id} no tiene asignada la especialidad {especialidad_id}')
            return Response({
                'error': 'El médico seleccionado no tiene asignada la especialidad solicitada.',
                'sugerencia': 'Por favor, seleccione otra especialidad o consulte con el administrador.',
                'codigo_error': 'ESPECIALIDAD_NO_ASIGNADA'
            }, status=400)
            
        # 4. Obtener TODOS los horarios sin filtros para diagnóstico
        logger.info('[HORARIOS] BÚSQUEDA DE DIAGNÓSTICO: Obteniendo TODOS los horarios sin filtros')
        
        # Obtener TODOS los horarios para este médico y especialidad sin importar la fecha
        horarios = HorarioCita.objects.filter(
            medico=medico,
            especialidad=especialidad,
            activo=True
        ).select_related('medico', 'especialidad').order_by('start_datetime')
        
        # Obtener el SQL de la consulta para depuración
        from django.db import connection
        logger.info(f'[HORARIOS] Consulta SQL: {str(horarios.query)}')
        
        # Contar total de horarios encontrados
        total_horarios = horarios.count()
        logger.info(f'[HORARIOS] Total de horarios encontrados: {total_horarios}')
        
        # Mostrar información detallada de los primeros 5 horarios
        for i, h in enumerate(horarios[:5], 1):
            logger.info(f'[HORARIOS] Horario {i}:')
            logger.info(f'  - ID: {h.id}')
            logger.info(f'  - Inicio: {h.start_datetime} (naive: {timezone.is_naive(h.start_datetime)})')
            logger.info(f'  - Fin: {h.end_datetime} (naive: {timezone.is_naive(h.end_datetime) if h.end_datetime else "N/A"})')
            logger.info(f'  - Activo: {h.activo}')
            logger.info(f'  - Médico: {h.medico_id} (esperado: {medico_id})')
            logger.info(f'  - Especialidad: {h.especialidad_id} (esperado: {especialidad_id}): {getattr(h.especialidad, "Espacialidad_Medica", "Campo no encontrado")}')
        
        # Guardar el queryset original para depuración
        horarios_qs = horarios
        
        # Convertir a lista para evitar múltiples consultas
        horarios_lista = list(horarios)
        total_horarios = len(horarios_lista)
        logger.info(f'[HORARIOS] Total de horarios encontrados (con filtro de fecha): {total_horarios}')
        
        if total_horarios == 0 and total_horarios_sin_filtro > 0:
            logger.warning('[HORARIOS] ADVERTENCIA: Hay horarios en la base de datos pero ninguno cumple con el filtro de fecha')
            # Obtener el horario más reciente para diagnóstico
            ultimo_horario = HorarioCita.objects.filter(
                medico=medico,
                especialidad=especialidad,
                activo=True
            ).order_by('-start_datetime').first()
            
            if ultimo_horario:
                logger.warning(f'[HORARIOS] Último horario encontrado (sin filtro): ID={ultimo_horario.id}, ' 
                             f'Fecha: {ultimo_horario.start_datetime}, Activo: {ultimo_horario.activo}')
        
        # Mostrar información detallada de los primeros 5 horarios para diagnóstico
        for i, h in enumerate(horarios_lista[:5], 1):
            logger.info(f'[HORARIOS] Horario {i}:')
            logger.info(f'  - ID: {h.id}')
            logger.info(f'  - Inicio: {h.start_datetime} (naive: {timezone.is_naive(h.start_datetime)})')
            logger.info(f'  - Fin: {h.end_datetime} (naive: {timezone.is_naive(h.end_datetime) if h.end_datetime else "N/A"})')
            logger.info(f'  - Activo: {h.activo}')
            logger.info(f'  - Médico: {h.medico_id} (esperado: {medico_id})')
            logger.info(f'  - Especialidad: {h.especialidad_id} (esperado: {especialidad_id})')
        
        # Usar la lista para el procesamiento
        horarios = horarios_lista
        
        # Log para depuración (usando el queryset original)
        logger.info(f'[HORARIOS] Consulta SQL: {str(horarios_qs.query)}')
        logger.info(f'[HORARIOS] Total de horarios a procesar: {total_horarios}')
        
        # 5. Procesar los horarios para el frontend
        horarios_data = []
        tz = pytz.timezone('America/Caracas')
        
        # Log para depuración
        total_horarios = len(horarios)
        logger.info(f'[HORARIOS] Total de horarios a procesar: {total_horarios}')
        
        if total_horarios == 0:
            logger.warning('[HORARIOS] No se encontraron horarios para procesar')
            logger.warning(f'[HORARIOS] Parámetros de búsqueda - Médico ID: {medico_id}, Especialidad ID: {especialidad_id}')
            logger.warning('[HORARIOS] Verificar que existan horarios activos para esta combinación')
        
        for idx, horario in enumerate(horarios, 1):
            logger.info(f'[HORARIOS] Procesando horario {idx}/{total_horarios}: ID={horario.id}')
            try:
                # Debug: Mostrar información del horario actual
                logger.info(f'[HORARIOS] Datos del horario {horario.id}:')
                logger.info(f'  - Start datetime: {horario.start_datetime} (naive: {timezone.is_naive(horario.start_datetime)})')
                logger.info(f'  - End datetime: {horario.end_datetime} (naive: {timezone.is_naive(horario.end_datetime) if horario.end_datetime else "N/A"})')
                
                # Manejar fechas naive (sin zona horaria)
                try:
                    if timezone.is_naive(horario.start_datetime):
                        start_dt = timezone.make_aware(horario.start_datetime, tz)
                        logger.info(f'  - Start datetime (converted): {start_dt}')
                    else:
                        start_dt = horario.start_datetime.astimezone(tz)
                        logger.info(f'  - Start datetime (converted from tz): {start_dt}')
                        
                    if horario.end_datetime:
                        if timezone.is_naive(horario.end_datetime):
                            end_dt = timezone.make_aware(horario.end_datetime, tz)
                            logger.info(f'  - End datetime (converted): {end_dt}')
                        else:
                            end_dt = horario.end_datetime.astimezone(tz)
                            logger.info(f'  - End datetime (converted from tz): {end_dt}')
                    else:
                        end_dt = None
                        logger.warning('  - End datetime es None')
                except Exception as e:
                    logger.error(f'[HORARIOS] Error al convertir fechas: {str(e)}')
                    logger.error(traceback.format_exc())
                    continue
                
                # Formatear fechas para el frontend (formato ISO 8601)
                try:
                    start_str = start_dt.isoformat() if start_dt else None
                    end_str = end_dt.isoformat() if end_dt else None
                    logger.info(f'  - Fechas formateadas: start={start_str}, end={end_str}')
                except Exception as e:
                    logger.error(f'  - Error al formatear fechas: {str(e)}')
                    logger.error(f'  - Tipo start_dt: {type(start_dt)}, valor: {start_dt}')
                    logger.error(f'  - Tipo end_dt: {type(end_dt)}, valor: {end_dt}')
                    continue
                
                horario_data = {
                    'id': horario.id,
                    'title': f'Disponible - {horario.especialidad.Espacialidad_Medica if hasattr(horario.especialidad, "Espacialidad_Medica") else "Especialidad no disponible"}',
                    'start': start_str,
                    'end': end_str,
                    'rango_horario': f"{start_dt.strftime('%#I:%M %p')} - {end_dt.strftime('%#I:%M %p')}",  # Usamos %#I en lugar de %-I para Windows
                    'especialidad': {
                        'id': horario.especialidad.id_Especialidad_Medica,
                        'nombre': horario.especialidad.Espacialidad_Medica if hasattr(horario.especialidad, "Espacialidad_Medica") else "Especialidad no disponible"
                    },
                    'medico': {
                        'id': horario.medico.id_Medico,
                        'nombre': f"{horario.medico.Nombres_Medico} {horario.medico.Apellidos_Medicos}"
                    },
                    'disponible': True
                }
                
                # Agregar regla de recurrencia si existe
                if hasattr(horario, 'recurrence_rule') and horario.recurrence_rule:
                    horario_data['recurrence_rule'] = horario.recurrence_rule
                
                horarios_data.append(horario_data)
                logger.debug(f'[HORARIOS] Procesado horario: {horario_data}')
                
            except Exception as e:
                logger.error(f'[HORARIOS] Error al procesar horario {horario.id}: {str(e)}')
                logger.error(traceback.format_exc())
        
        # 6. Preparar respuesta exitosa
        response_data = {
            'success': True,
            'horarios': horarios_data,
            'total': len(horarios_data),
            'medico': {
                'id': medico.id_Medico,
                'nombre': f"{medico.Nombres_Medico} {medico.Apellidos_Medicos}"
            },
            'especialidad': {
                'id': especialidad.id_Especialidad_Medica,
                'nombre': especialidad.Espacialidad_Medica if hasattr(especialidad, "Espacialidad_Medica") else "Especialidad no disponible"
            },
            'fecha_consulta': ahora.isoformat(),
            'total_resultados': len(horarios_data)
        }
        
        logger.info(f'[HORARIOS] Devolviendo {len(horarios_data)} horarios')
        return Response(response_data)
        
    except Exception as e:
        error_msg = f'[HORARIOS] Error inesperado: {str(e)}'
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return Response({
            'error': 'Error inesperado al procesar la solicitud.',
            'detalle': str(e),
            'sugerencia': 'Por favor, intente nuevamente más tarde.',
            'codigo_error': 'ERROR_INTERNO_SERVIDOR',
            'hora_servidor': timezone.now().isoformat()
        }, status=500)

def horarios_json(request):
    """Versión que respeta la fecha UNTIL del RRULE"""
    try:
        eventos = []
        horarios = HorarioCita.objects.filter(activo=True).select_related('medico', 'especialidad')

        for horario in horarios:
            start_datetime = horario.start_datetime
            end_datetime = horario.end_datetime
            
            title = f'{horario.medico.Nombres_Medico} - {horario.especialidad.Espacialidad_Medica}'
            
            print(f"DEBUG - Procesando horario {horario.id}")
            print(f"DEBUG - RRULE: {horario.recurrence_rule}")

            if horario.recurrence_rule and 'BYDAY=' in horario.recurrence_rule:
                # Procesar días de la semana
                dias_map = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4, 'SA': 5, 'SU': 6}
                dias_semana = []
                
                # Extraer días del BYDAY
                byday_part = [p for p in horario.recurrence_rule.split(';') if 'BYDAY=' in p][0]
                dias_rrule = byday_part.split('=')[1].split(',')
                
                for dia in dias_rrule:
                    if dia in dias_map:
                        dias_semana.append(dias_map[dia])
                
                # Extraer fecha UNTIL si existe
                until_date = None
                if 'UNTIL=' in horario.recurrence_rule:
                    try:
                        until_part = [p for p in horario.recurrence_rule.split(';') if 'UNTIL=' in p][0]
                        until_str = until_part.split('=')[1]
                        # Convertir de UTC a fecha local
                        until_date_utc = datetime.strptime(until_str, '%Y%m%dT%H%M%SZ')
                        # Si necesitas ajustar zona horaria, hazlo aquí
                        until_date = until_date_utc.date()
                        print(f"DEBUG - Fecha UNTIL: {until_date}")
                    except Exception as e:
                        print(f"DEBUG - Error procesando UNTIL: {e}")

                print(f"DEBUG - Días encontrados: {dias_semana}")

                # Crear eventos hasta la fecha UNTIL o máximo 104 semanas (2 años)
                fecha_base = start_datetime.date()
                semana = 0
                max_semanas = 104  # Límite máximo por seguridad
                
                while semana < max_semanas:
                    for dia_num in dias_semana:
                        # Calcular fecha exacta
                        dia_base_semana = fecha_base.weekday()
                        dias_diferencia = dia_num - dia_base_semana
                        if dias_diferencia < 0:
                            dias_diferencia += 7
                        
                        evento_date = fecha_base + timedelta(weeks=semana, days=dias_diferencia)
                        
                        # Verificar si hemos pasado la fecha UNTIL
                        if until_date and evento_date > until_date:
                            continue
                        
                        # Crear evento
                        evento_start = datetime.combine(evento_date, start_datetime.time())
                        evento_end = datetime.combine(evento_date, end_datetime.time())
                        
                        if start_datetime.tzinfo:
                            evento_start = evento_start.replace(tzinfo=start_datetime.tzinfo)
                            evento_end = evento_end.replace(tzinfo=start_datetime.tzinfo)
                        
                        eventos.append({
                            'id': f"horario_{horario.id}_{evento_date}",
                            'title': title,
                            'color': '#007bff',
                            'start': evento_start.isoformat(),
                            'end': evento_end.isoformat(),
                            'extendedProps': {
                                'horario_id': horario.id, 
                                'medico_id': horario.medico_id,
                                'tipo': 'recurrente'
                            }
                        })
                        print(f"DEBUG - Evento creado: {evento_date}")
                    
                    semana += 1
                    
                    # Salir del loop si hemos pasado la fecha UNTIL
                    if until_date and (fecha_base + timedelta(weeks=semana)) > until_date:
                        break

            else:
                # Evento único
                eventos.append({
                    'id': f"horario_{horario.id}",
                    'title': title,
                    'start': start_datetime.isoformat(), 
                    'end': end_datetime.isoformat(), 
                    'color': '#28a745',
                    'extendedProps': {
                        'horario_id': horario.id, 
                        'medico_id': horario.medico_id,
                        'tipo': 'unico'
                    }
                })

        print(f"DEBUG - Total eventos creados: {len(eventos)}")
        return JsonResponse(eventos, safe=False)
        
    except Exception as e:
        print(f"ERROR en horarios_json: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
from datetime import datetime, timedelta
import json
from django.utils import timezone

from .forms import RegistroPacienteForm
from .models import (
    Ciudad, Municipio, Parroquia, Estado, Pais,
    EspecialidadMedica, HorarioCita, MedicoEspecialidad,
    Cita, CitasReservadas, Paciente, UsuarioMedico
)
from .models import (
    Ciudad, Municipio, Parroquia, Estado, Pais,
    EspecialidadMedica, HorarioCita, MedicoEspecialidad,
    Cita, CitasReservadas, Paciente, UsuarioMedico
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
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect
# -------------------------------------------------------------
# VISTAS PRINCIPALES
# -------------------------------------------------------------

def calendario_nuevo_view(request):
    """
    Vista para el nuevo calendario de citas con interfaz mejorada.
    """
    # Verificar si el usuario está autenticado
    if not request.user.is_authenticated:
        return redirect('admin:login')
    
    # Obtener la fecha actual
    hoy = timezone.now().date()
    
    try:
        print("\n=== CARGANDO DATOS PARA EL CALENDARIO ===")
        
        # Obtener todos los pacientes
        pacientes = Paciente.objects.all()
        print(f"Total de pacientes en la base de datos: {pacientes.count()}")
        
        # Obtener todos los médicos activos con sus especialidades
        medicos = UsuarioMedico.objects.filter(activo=True).prefetch_related('medicoespecialidad_set__especialidad')
        
        # Preparar la lista de médicos con sus especialidades
        medicos_con_especialidad = []
        for medico in medicos:
            # Obtener todas las especialidades del médico
            especialidades = []
            for me in medico.medicoespecialidad_set.all():
                especialidades.append({
                    'id': me.especialidad.id_Especialidad_Medica,
                    'nombre': me.especialidad.Espacialidad_Medica,
                    'activo': me.activo
                })
            
            # Agregar el médico a la lista con sus especialidades
            if especialidades:  # Solo incluir médicos con al menos una especialidad
                medicos_con_especialidad.append({
                    'id_Medico': medico.id_Medico,
                    'Nombres_Medico': medico.Nombres_Medico,
                    'Apellidos_Medicos': medico.Apellidos_Medicos,
                    'especialidades': especialidades
                })
        
        print(f"Total de médicos activos con especialidades: {len(medicos_con_especialidad)}")
        for m in medicos_con_especialidad[:5]:  # Mostrar primeros 5 para depuración
            print(f"  - {m['Nombres_Medico']} {m['Apellidos_Medicos']}: {len(m['especialidades'])} especialidades")
        
        # Obtener todas las especialidades
        especialidades = EspecialidadMedica.objects.all()
        print(f"Total de especialidades: {especialidades.count()}")
        
        # Mostrar información de los primeros 5 pacientes
        print("\nEjemplos de pacientes (primeros 5):")
        for p in pacientes[:5]:
            print(f"ID: {p.id_Paciente}, "
                  f"Nombre: {p.Nombres_Paciente} {getattr(p, 'Apellidos_Paciente', '')}, "
                  f"Cédula: {getattr(p, 'CIDNI', 'N/A')}")
        
    except Exception as e:
        print(f"\n¡ERROR al cargar datos: {str(e)}")
        import traceback
        traceback.print_exc()
        pacientes = Paciente.objects.none()
        medicos_con_especialidad = []
        especialidades = EspecialidadMedica.objects.none()
    
    # Crear contexto con los datos necesarios
    context = {
        'title': 'Nuevo Calendario de Citas',
        'hoy': hoy,
        'pacientes': pacientes,
        'medicos': medicos_con_especialidad,  # Contiene la lista de todos los médicos activos
        'especialidades': especialidades,
        'opts': {'app_label': 'citas'},
    }
    
    return render(request, 'citas/reservas/calendario_nuevo.html', context)
    
def registrar_paciente(request):
    print("\n=== INICIO DE LA SOLICITUD REGISTRAR_PACIENTE ===")
    print(f"Método de la solicitud: {request.method}")
    print(f"¿Es AJAX? {request.headers.get('X-Requested-With') == 'XMLHttpRequest'}")
    
    if request.method == 'POST':
        print("\n=== DATOS POST RECIBIDOS ===")
        # Imprimir todos los datos POST para depuración
        print("Datos POST:")
        for key, value in request.POST.items():
            print(f"  {key}: {value}")
        
        # Verificar si hay archivos en la solicitud
        print("\n=== ARCHIVOS EN LA SOLICITUD ===")
        print(f"Número de archivos: {len(request.FILES) if hasattr(request, 'FILES') else 0}")
        
        # Crear una copia mutable de request.POST
        post_data = request.POST.copy()
        
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
            from django.db import transaction
            from django.http import JsonResponse
            from django.urls import reverse
            
            try:
                with transaction.atomic():
                    # Guardar el paciente (el formulario ya maneja la dirección)
                    paciente = form.save(commit=True)  # commit=True para guardar también la dirección
                    
                    # No necesitamos asignar manualmente los campos de ubicación
                    # ya que el método save() del formulario ya los está manejando
                    print("\n=== DATOS DEL PACIENTE GUARDADOS ===")
                    print(f"ID del paciente: {getattr(paciente, 'id_Paciente', 'N/A')}")
                    
                    # Verificar si se creó la dirección
                    if hasattr(paciente, 'direccion'):
                        print("\n=== DIRECCIÓN DEL PACIENTE ===")
                        print(f"Dirección: {getattr(paciente.direccion, 'direccion', 'N/A')}")
                        print(f"Estado: {getattr(paciente.direccion.estado, 'estado', 'N/A') if getattr(paciente.direccion, 'estado', None) else 'N/A'}")
                        print(f"Ciudad: {getattr(paciente.direccion.ciudad, 'ciudad', 'N/A') if getattr(paciente.direccion, 'ciudad', None) else 'N/A'}")
                        print(f"Municipio: {getattr(paciente.direccion.municipio, 'municipio', 'N/A') if getattr(paciente.direccion, 'municipio', None) else 'N/A'}")
                        print(f"Parroquia: {getattr(paciente.direccion.parroquia, 'parroquia', 'N/A') if getattr(paciente.direccion, 'parroquia', None) else 'N/A'}")
                    
                    print(f"\n=== PACIENTE GUARDADO CON ÉXITO ===")
                    print(f"ID del paciente: {getattr(paciente, 'id_Paciente', 'N/A')}")
                    
                    # Devolver respuesta JSON exitosa
                    return JsonResponse({
                        'success': True,
                        'message': 'Paciente registrado exitosamente',
                        'paciente_id': paciente.id_Paciente,
                        'redirect_url': reverse('citas:crear_cita') + f'?paciente_id={paciente.id_Paciente}'
                    })
                    
            except Exception as e:
                import traceback
                error_trace = traceback.format_exc()
                print(f"\n=== ERROR AL GUARDAR EL PACIENTE ===")
                print(f"Error: {str(e)}")
                print("Traceback:")
                print(error_trace)
                
                # Devolver error como JSON con más detalles para depuración
                return JsonResponse({
                    'success': False,
                    'message': 'Error al guardar el paciente',
                    'error': str(e),
                    'error_type': type(e).__name__,
                    'traceback': error_trace if settings.DEBUG else None
                }, status=500, json_dumps_params={'ensure_ascii': False})
        else:
            # Si el formulario no es válido, devolver errores de validación
            from django.http import JsonResponse
            errors = {}
            for field, field_errors in form.errors.items():
                field_label = form.fields[field].label if field in form.fields else field
                errors[field] = [str(error) for error in field_errors]
            
            return JsonResponse({
                'success': False,
                'message': 'Error de validación',
                'errors': errors
            }, status=400)
    else:
        # Si no es POST, mostrar el formulario vacío
        form = RegistroPacienteForm()
        return render(request, 'citas/cita_web/registro.html', {
            'form': form,
            'titulo': 'Registro de Paciente'
        })# -------------------------------------------------------------
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
    # Aceptar tanto estado_id como parent_id para mayor compatibilidad
    estado_id = request.GET.get('estado_id') or request.GET.get('parent_id')
    # Aceptar municipio_id de los parámetros GET
    municipio_id = request.GET.get('municipio_id') or request.GET.get('parent_id')
    
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
    """
    Obtiene todas las especialidades asignadas a un médico específico.
    Retorna tanto especialidades activas como inactivas para que el frontend filtre.
    """
    print(f"[DEBUG] get_especialidades_medico - Iniciando para médico_id: {medico_id}")
    
    try:
        # Verificar que el médico existe
        from django.shortcuts import get_object_or_404
        from .models import UsuarioMedico
        
        # Solo verificar que el médico existe, pero no necesitamos el objeto
        if not UsuarioMedico.objects.filter(id_Medico=medico_id).exists():
            print(f"[DEBUG] Médico con ID {medico_id} no encontrado")
            return JsonResponse({
                'success': False,
                'error': f'Médico con ID {medico_id} no encontrado',
                'especialidades': []
            }, status=404)
            
        # Obtener todas las especialidades del médico con la relación
        from django.db.models import Q
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
        import traceback
        error_msg = str(e)
        trace = traceback.format_exc()
        print(f"[ERROR] Error en get_especialidades_medico: {error_msg}")
        print(f"[TRACE] {trace}")
        
        return JsonResponse({
            'success': False,
            'error': 'Error al obtener las especialidades del médico',
            'detalle': error_msg,
            'trace': trace if request.user.is_staff else None
        }, status=500)
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
    Vista para obtener la lista de pacientes en formato JSON
    """
    try:
        pacientes = list(Paciente.objects.all().values(
            'id_Paciente', 
            'Nombres_Paciente', 
            'Apellidos_Paciente', 
            'CIDNI',
            'Activo'
        ).order_by('Apellidos_Paciente', 'Nombres_Paciente'))
        
        return JsonResponse({
            'status': 'success', 
            'pacientes': pacientes,
            'count': len(pacientes)
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'status': 'error', 
            'message': f'Error al obtener pacientes: {str(e)}'
        }, status=500)

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
@csrf_exempt
def crear_cita(request):
    """
    Vista para crear una nueva cita con visualización de disponibilidad del médico.
    Similar al módulo de reserva de citas pero solo permite agregar nuevas citas.
    """
    # Obtener todas las especialidades médicas
    especialidades = EspecialidadMedica.objects.all().order_by('Espacialidad_Medica')
    
    # Obtener la lista de pacientes activos para el select
    pacientes = Paciente.objects.filter(Activo=True).order_by('Apellidos_Paciente', 'Nombres_Paciente')
    
    # Obtener el ID del paciente si está en los parámetros GET
    paciente_id = request.GET.get('paciente_id')
    paciente = None
    if paciente_id:
        try:
            paciente = Paciente.objects.get(id_Paciente=paciente_id)
        except Paciente.DoesNotExist:
            messages.warning(request, 'El paciente especificado no existe')
    
    # Obtener especialidad y médico si están en los parámetros
    especialidad_id = request.GET.get('especialidad_id')
    medico_id = request.GET.get('medico_id')
    
    # Inicializar variables para el contexto
    medicos = UsuarioMedico.objects.none()
    especialidad = None
    medico = None
    
    # Si hay una especialidad seleccionada, obtener los médicos
    if especialidad_id:
        try:
            especialidad = EspecialidadMedica.objects.get(id_Especialidad_Medica=especialidad_id)
            medicos = UsuarioMedico.objects.filter(
                medicoespecialidad__especialidad=especialidad,
                activo=True
            ).distinct().order_by('Apellidos_Medicos', 'Nombres_Medico')
            
            # Si hay un médico seleccionado, obtener sus datos
            if medico_id:
                try:
                    medico = UsuarioMedico.objects.get(id_Medico=medico_id, activo=True)
                except UsuarioMedico.DoesNotExist:
                    messages.warning(request, 'El médico seleccionado no existe o no está activo')
        except EspecialidadMedica.DoesNotExist:
            messages.warning(request, 'La especialidad seleccionada no existe')
    
    # Verificar si es una petición AJAX para cargar médicos
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print("Solicitud AJAX recibida para cargar médicos")
        try:
            # Obtener el ID de la especialidad de los parámetros GET
            especialidad_id = request.GET.get('especialidad_id')
            print(f"ID de especialidad recibido: {especialidad_id}")
            
            if not especialidad_id:
                print("Error: No se especificó la especialidad")
                return JsonResponse({
                    'success': False,
                    'error': 'No se especificó la especialidad'
                }, status=400)
                
            try:
                # Verificar que la especialidad existe
                print(f"Buscando especialidad con ID: {especialidad_id}")
                especialidad = EspecialidadMedica.objects.get(id_Especialidad_Medica=especialidad_id)
                print(f"Especialidad encontrada: {especialidad}")
            except EspecialidadMedica.DoesNotExist as e:
                print(f"Error: La especialidad con ID {especialidad_id} no existe")
                return JsonResponse({
                    'success': False,
                    'error': f'La especialidad con ID {especialidad_id} no existe'
                }, status=404)
            except Exception as e:
                print(f"Error al buscar especialidad: {str(e)}")
                raise
            
            try:
                # Obtener médicos para la especialidad seleccionada
                print(f"Buscando médicos para la especialidad: {especialidad_id}")
                medicos = UsuarioMedico.objects.filter(
                    especialidades__id_Especialidad_Medica=especialidad_id,
                    activo=True
                ).distinct().order_by('Apellidos_Medicos', 'Nombres_Medico')
                
                print(f"Médicos encontrados: {medicos.count()}")
                
                medicos_data = [{
                    'id': str(medico.id_Medico),  # Asegurarse de que el ID sea string
                    'text': f"{medico.Apellidos_Medicos}, {medico.Nombres_Medico}"
                } for medico in medicos]
                
                print(f"Datos de médicos preparados: {medicos_data}")
                
                return JsonResponse({
                    'success': True,
                    'medicos': medicos_data
                })
                
            except Exception as e:
                print(f"Error al obtener médicos: {str(e)}")
                raise
            
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print("="*50)
            print("ERROR EN crear_cita (AJAX)")
            print(f"Tipo de error: {type(e).__name__}")
            print(f"Mensaje: {str(e)}")
            print("Traceback completo:")
            print(error_trace)
            print("="*50)
            
            # Registrar el error en los logs del servidor
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en crear_cita (AJAX): {str(e)}\n{error_trace}")
            
            return JsonResponse({
                'success': False,
                'error': 'Error interno del servidor al cargar los médicos',
                'debug': f"{type(e).__name__}: {str(e)}"
            }, status=500)
    
    # Obtener horarios del médico si está seleccionado
    horarios_disponibles = []
    citas_reservadas = []
    
    if medico_id and especialidad_id:
        try:
            try:
                # Obtener las citas ya reservadas para este médico y especialidad
                hoy = timezone.now().date()
                fecha_fin = hoy + timedelta(days=7)  # Próximos 7 días
                
                citas_reservadas = CitasReservadas.objects.filter(
                    horario__medico_id=medico_id,
                    horario__especialidad_id=especialidad_id,
                    start_datetime__date__gte=hoy,
                    start_datetime__date__lte=fecha_fin,
                    estado__in=['pendiente', 'confirmada']  # Solo considerar citas activas
                ).values_list('start_datetime', flat=True)
                
                # Convertir a conjunto para búsqueda más rápida
                citas_reservadas = set([cita.strftime('%Y-%m-%d %H:%M') for cita in citas_reservadas])
                
                # Obtener los horarios activos del médico para la especialidad
                horarios = HorarioCita.objects.filter(
                    medico_id=medico_id,
                    especialidad_id=especialidad_id,
                    activo=True,
                    start_datetime__isnull=False,
                    end_datetime__isnull=False
                ).select_related('turno')
                
                # Si hay horarios, procesarlos
                if horarios.exists():
                    # Usar un conjunto para evitar duplicados
                    horas_unicas = set()
                    horarios_disponibles = []
                    
                    for horario in horarios:
                        # Si hay una regla de recurrencia, procesarla
                        if horario.recurrence_rule:
                            # Para simplificar, asumimos horarios fijos por ahora
                            if horario.turno and horario.turno.hora_inicio and horario.turno.hora_fin:
                                # Agregar horas en el rango del turno
                                hora_actual = horario.turno.hora_inicio
                                hora_fin = horario.turno.hora_fin
                                while hora_actual < hora_fin:
                                    horarios_disponibles.append(hora_actual.strftime('%H:%M'))
                                    hora_actual = (datetime.combine(datetime.today(), hora_actual) + timedelta(minutes=30)).time()
            
                print(f"Horarios disponibles: {horarios_disponibles}")
            
            except Exception as e:
                print(f"Error al obtener horarios: {str(e)}")
                # En caso de error, usar un horario por defecto
                horarios_disponibles = [
                    '08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
                    '11:00', '11:30', '14:00', '14:30', '15:00', '15:30',
                    '16:00', '16:30', '17:00'
                ]
        except Exception as e:
            print(f"Error al obtener horarios: {str(e)}")
            # En caso de error, usar un horario por defecto
            horarios_disponibles = [
                '08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
                '11:00', '11:30', '14:00', '14:30', '15:00', '15:30',
                '16:00', '16:30', '17:00'
            ]
    
    # Preparar el contexto para la plantilla
    context = {
        'especialidades': especialidades,
        'medicos': medicos,
        'paciente': paciente,
        'pacientes': pacientes,  
        'paciente_id': paciente.id_Paciente if paciente else '',
        'especialidad_seleccionada': especialidad,
        'medico_seleccionado': medico,
        'fecha_actual': timezone.now().date(),
        'horarios_disponibles': horarios_disponibles,
        'citas_reservadas': citas_reservadas
    }
    
    # Renderizar la plantilla con el contexto
    return render(request, 'citas/crear_cita.html', context)

@csrf_exempt
def disponibilidad_medico(request):
    """
    API para obtener la disponibilidad de un médico en un rango de fechas.
    """
    if request.method != 'GET':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
    
    try:
        medico_id = request.GET.get('medico_id')
        especialidad_id = request.GET.get('especialidad_id')
        start_date_str = request.GET.get('start')
        end_date_str = request.GET.get('end')
        
        print(f"Parámetros recibidos - médico: {medico_id}, especialidad: {especialidad_id}, inicio: {start_date_str}, fin: {end_date_str}")
        
        # Validar parámetros requeridos
        if not all([medico_id, especialidad_id, start_date_str, end_date_str]):
            return JsonResponse(
                {'success': False, 'error': 'Faltan parámetros requeridos: medico_id, especialidad_id, start, end'},
                status=400
            )
        
        # Convertir las fechas al formato correcto
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError as e:
            return JsonResponse(
                {'success': False, 'error': f'Formato de fecha inválido. Use YYYY-MM-DD. Error: {str(e)}'},
                status=400
            )
        
        print(f"Fechas convertidas - inicio: {start_date}, fin: {end_date}")
        
        # Obtener los horarios del médico para la especialidad en el rango de fechas
        horarios = HorarioCita.objects.filter(
            medico_id=medico_id,
            especialidad_id=especialidad_id,
            activo=True,
            start_datetime__date__lte=end_date,
            end_datetime__date__gte=start_date
        )
        
        print(f"Horarios encontrados: {horarios.count()}")
        
        # Si no hay horarios definidos para ese día
        if not horarios.exists():
            return JsonResponse({
                'success': True,
                'disponibilidad': [],
                'mensaje': 'No hay horarios disponibles para la fecha seleccionada'
            })
        
        # Obtener las citas ya reservadas en el rango de fechas
        citas_reservadas = CitasReservadas.objects.filter(
            horario__medico_id=medico_id,
            horario__especialidad_id=especialidad_id,
            start_datetime__date__lte=end_date,
            end_datetime__date__gte=start_date,
            estado__in=['pendiente', 'confirmada']
        )
        
        print(f"Citas reservadas encontradas: {citas_reservadas.count()}")
        
        # Convertir las citas a un formato más manejable
        citas_por_fecha_hora = {}
        for cita in citas_reservadas:
            fecha_str = cita.start_datetime.date().isoformat()
            hora_str = cita.start_datetime.time().strftime('%H:%M')
            
            if fecha_str not in citas_por_fecha_hora:
                citas_por_fecha_hora[fecha_str] = {}
                
            citas_por_fecha_hora[fecha_str][hora_str] = {
                'inicio': cita.start_datetime.strftime('%H:%M'),
                'fin': cita.end_datetime.strftime('%H:%M'),
                'estado': cita.estado,
                'paciente': f"{cita.paciente.Nombres_Paciente} {cita.paciente.Apellidos_Paciente}"
            }
        
        # Generar la disponibilidad para cada día en el rango
        disponibilidad = []
        current_date = start_date
        
        while current_date <= end_date:
            # Obtener el día de la semana (0=lunes, 6=domingo)
            dia_semana = current_date.weekday()
            fecha_str = current_date.isoformat()
            
            # Filtrar horarios para este día de la semana
            horarios_dia = [h for h in horarios if h.dia_semana == dia_semana]
            
            for horario in horarios_dia:
                hora_actual = horario.hora_inicio
                
                while hora_actual < horario.hora_fin:
                    hora_fin = (datetime.combine(current_date, hora_actual) + timedelta(minutes=30)).time()
                    if hora_fin > horario.hora_fin:
                        hora_fin = horario.hora_fin
                    
                    hora_str = hora_actual.strftime('%H:%M')
                    cita = citas_por_fecha_hora.get(fecha_str, {}).get(hora_str) if fecha_str in citas_por_fecha_hora else None
                    
                    disponibilidad.append({
                        'fecha': fecha_str,
                        'hora_inicio': hora_str,
                        'hora_fin': hora_fin.strftime('%H:%M'),
                        'disponible': cita is None,
                        'cita': cita,
                        'title': 'Disponible' if cita is None else 'Ocupado',
                        'start': f"{fecha_str}T{hora_str}",
                        'end': f"{fecha_str}T{hora_fin.strftime('%H:%M')}",
                        'backgroundColor': '#28a745' if cita is None else '#dc3545',
                        'borderColor': '#28a745' if cita is None else '#dc3545',
                        'textColor': 'white',
                        'extendedProps': {
                            'disponible': cita is None
                        }
                    })
                    
                    hora_actual = hora_fin
            
            current_date += timedelta(days=1)
        
        # Agrupar la disponibilidad por fecha para facilitar el manejo en el frontend
        disponibilidad_por_fecha = {}
        for slot in disponibilidad:
            fecha = slot['fecha']
            if fecha not in disponibilidad_por_fecha:
                disponibilidad_por_fecha[fecha] = []
            disponibilidad_por_fecha[fecha].append(slot)
        
        print(f"Disponibilidad generada para {len(disponibilidad)} slots en {len(disponibilidad_por_fecha)} días")
        
        return JsonResponse({
            'success': True,
            'disponibilidad': disponibilidad_por_fecha,
            'start_date': start_date_str,
            'end_date': end_date_str,
            'total_slots': len(disponibilidad),
            'dias_con_disponibilidad': len(disponibilidad_por_fecha)
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': f'Error al obtener la disponibilidad: {str(e)}',
            'traceback': traceback.format_exc()
        }, status=500)
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
@csrf_exempt
def guardar_cita(request):
    """
    Vista para guardar una nueva cita.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido', 'success': False}, status=405)
    
    try:
        # Obtener datos del formulario
        data = json.loads(request.body)
        print("Datos recibidos:", json.dumps(data, indent=2, default=str))
        
        # Validar campos requeridos
        required_fields = ['paciente_id', 'medico_id', 'especialidad_id', 'fecha', 'hora']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({
                    'error': f'El campo {field} es requerido',
                    'success': False
                }, status=400)
        
        # Obtener los objetos relacionados
        try:
            paciente = Paciente.objects.get(id_Paciente=data['paciente_id'])
            medico = UsuarioMedico.objects.get(id_Medico=data['medico_id'])
            especialidad = EspecialidadMedica.objects.get(id_Especialidad_Medica=data['especialidad_id'])
        except (Paciente.DoesNotExist, UsuarioMedico.DoesNotExist, EspecialidadMedica.DoesNotExist) as e:
            return JsonResponse({
                'error': f'Error al obtener los datos: {str(e)}',
                'success': False
            }, status=400)
        
        # Procesar fecha y hora
        try:
            duracion = int(data.get('duracion', 30))
            fecha_hora_str = f"{data['fecha']} {data['hora']}"
            formatos_fecha = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%dT%H:%M'
            ]
            
            fecha_hora = None
            for formato in formatos_fecha:
                try:
                    fecha_hora = datetime.strptime(fecha_hora_str, formato)
                    break
                except ValueError:
                    continue
            
            if fecha_hora is None:
                raise ValueError(f"No se pudo parsear la fecha y hora: {fecha_hora_str}")
                
            # Asegurarse de que la fecha sea consciente de la zona horaria
            if timezone.is_naive(fecha_hora):
                fecha_hora = timezone.make_aware(fecha_hora)
            
            fecha_hora_fin = fecha_hora + timedelta(minutes=duracion)
            
            print(f"Fecha/hora convertida: {fecha_hora}")
            print(f"Fecha/hora de fin: {fecha_hora_fin}")
            print(f"Zona horaria: {fecha_hora.tzinfo}")
            
        except ValueError as e:
            error_msg = f'Formato de fecha o duración inválido: {str(e)}. Formato esperado: YYYY-MM-DD HH:MM'
            print(f"ERROR: {error_msg}")
            return JsonResponse({
                'error': error_msg,
                'success': False
            }, status=400)
        
        # Verificar disponibilidad del médico
        try:
            cita_existente = CitasReservadas.objects.filter(
                horario__medico=medico,
                start_datetime__lt=fecha_hora_fin,
                end_datetime__gt=fecha_hora,
                estado__in=['pendiente', 'confirmada']
            ).exists()
            
            if cita_existente:
                error_msg = 'El médico ya tiene una cita programada en el horario seleccionado.'
                print(f"ERROR: {error_msg}")
                return JsonResponse({
                    'error': error_msg,
                    'success': False
                }, status=400)
            
            # Buscar un horario existente o crear uno temporal
            horario = HorarioCita.objects.filter(
                medico=medico,
                especialidad=especialidad,
                activo=True
            ).first()
            
            if not horario:
                # Si no hay un horario existente, crear uno temporal
                horario = HorarioCita.objects.create(
                    medico=medico,
                    especialidad=especialidad,
                    dia_semana=fecha_hora.weekday(),
                    hora_inicio=fecha_hora.time(),
                    hora_fin=(fecha_hora + timedelta(minutes=duracion)).time(),
                    activo=True,
                    domicilio=data.get('domicilio', False),
                    descripcion='Cita única programada manualmente'
                )
                print(f"Creado nuevo horario temporal con ID: {horario.id}")
            else:
                print(f"Usando horario existente con ID: {horario.id}")
            
            # Crear la cita reservada
            cita = CitasReservadas(
                horario=horario,
                paciente=paciente,
                start_datetime=fecha_hora,
                end_datetime=fecha_hora_fin,
                estado='pendiente',
                nota=data.get('nota', ''),
                costo=data.get('costo')
            )
            cita.save()
            
            print(f"\n=== CITA CREADA CON ÉXITO ===")
            print(f"ID de la cita: {cita.id}")
            print(f"Paciente: {paciente.Nombres_Paciente} {paciente.Apellidos_Paciente}")
            print(f"Médico: {medico.Nombres_Medico} {medico.Apellidos_Medicos}")
            print(f"Especialidad: {especialidad.Espacialidad_Medica}")
            print(f"Fecha/Hora: {fecha_hora}")
            print(f"Duración: {duracion} minutos")
            print(f"Nota: {data.get('nota', 'Ninguna')}")
            
            return JsonResponse({
                'success': True,
                'message': 'Cita creada exitosamente',
                'cita_id': cita.id,
                'fecha': fecha_hora.strftime('%Y-%m-%d'),
                'hora': fecha_hora.strftime('%H:%M'),
                'duracion': duracion,
                'medico': f"{medico.Nombres_Medico} {medico.Apellidos_Medicos}",
                'especialidad': especialidad.Espacialidad_Medica
            })
            
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            error_msg = f'Error al crear la cita: {str(e)}'
            print(f"\n=== ERROR AL CREAR LA CITA ===")
            print(error_msg)
            print("\nTraza de error:", error_trace)
            
            return JsonResponse({
                'error': 'Error al crear la cita',
                'details': str(e),
                'success': False
            }, status=500)
            
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

@csrf_exempt
def cancelar_cita(request, cita_id):
    """
    Cancela una cita existente.
    
    Args:
        request: Objeto de solicitud HTTP
        cita_id: ID de la cita a cancelar
        
    Returns:
        JsonResponse: Resultado de la operación
    """
    try:
        # Obtener la cita o devolver 404 si no existe
        cita = CitasReservadas.objects.get(id=cita_id)
        
        # Cambiar el estado a 'cancelada'
        cita.estado = 'cancelada'
        cita.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cita cancelada exitosamente',
            'cita_id': cita.id,
            'nuevo_estado': 'cancelada'
        })
        
    except CitasReservadas.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': f'No se encontró la cita con ID {cita_id}'
        }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al cancelar la cita: {str(e)}'
        }, status=500)

def obtener_eventos(request):
    """
    Vista para obtener los eventos del calendario en formato JSON.
    Incluye tanto las citas programadas como los horarios de disponibilidad.
    """
    from .models import CitasReservadas, HorarioCita
    from django.utils import timezone
    from datetime import timedelta
    
    try:
        # Obtener parámetros de filtrado
        start_str = request.GET.get('start')
        end_str = request.GET.get('end')
        
        # Convertir fechas de string a objetos datetime
        start = timezone.datetime.fromisoformat(start_str) if start_str else timezone.now() - timedelta(days=30)
        end = timezone.datetime.fromisoformat(end_str) if end_str else timezone.now() + timedelta(days=60)
        
        eventos = []
        
        # 1. Obtener citas programadas
        citas = CitasReservadas.objects.filter(
            start_datetime__gte=start,
            end_datetime__lte=end
        ).select_related('paciente', 'horario__medico', 'horario__especialidad')
        
        for cita in citas:
            try:
                eventos.append({
                    'id': f'cita_{cita.id}',
                    'title': f"{cita.paciente.Nombres_Paciente} {cita.paciente.Apellidos_Paciente}",
                    'start': cita.start_datetime.isoformat(),
                    'end': cita.end_datetime.isoformat(),
                    'extendedProps': {
                        'tipo': 'cita',
                        'paciente': f"{cita.paciente.Nombres_Paciente} {cita.paciente.Apellidos_Paciente}",
                        'medico': f"{cita.horario.medico.Nombres_Medico} {cita.horario.medico.Apellidos_Medicos}" if cita.horario and cita.horario.medico else 'Sin médico asignado',
                        'especialidad': cita.horario.especialidad.Espacialidad_Medica if cita.horario and cita.horario.especialidad else 'Sin especialidad',
                        'estado': cita.estado,
                        'notas': cita.nota or '',
                    },
                    'color': get_color_estado(cita.estado),
                    'textColor': '#ffffff',
                    'editable': False,
                    'startEditable': False,
                    'durationEditable': False,
                    'resourceEditable': False
                })
            except Exception as e:
                print(f"Error procesando cita {cita.id}: {str(e)}")
                continue
        
        # 2. Obtener horarios de disponibilidad
        horarios = HorarioCita.objects.filter(
            activo=True,
            start_datetime__lte=end,
            end_datetime__gte=start
        ).select_related('medico', 'especialidad')
        
        for horario in horarios:
            try:
                eventos.append({
                    'id': f'disponibilidad_{horario.id}',
                    'title': 'Disponible',
                    'start': horario.start_datetime.isoformat(),
                    'end': horario.end_datetime.isoformat(),
                    'extendedProps': {
                        'tipo': 'disponibilidad',
                        'medico': f"{horario.medico.Nombres_Medico} {horario.medico.Apellidos_Medicos}",
                        'especialidad': horario.especialidad.Espacialidad_Medica if horario.especialidad else 'Sin especialidad',
                        'estado': 'disponible',
                    },
                    'color': '#28a745',  # Verde para disponibilidad
                    'textColor': '#ffffff',
                    'editable': False,
                    'startEditable': False,
                    'durationEditable': False,
                    'resourceEditable': False
                })
            except Exception as e:
                print(f"Error procesando horario {horario.id}: {str(e)}")
                continue
        
        print(f"🔍 Eventos encontrados: {len(eventos)} (Citas: {citas.count()}, Horarios: {horarios.count()})")
        return JsonResponse(eventos, safe=False)
        
    except Exception as e:
        error_msg = f'Error al obtener eventos: {str(e)}'
        print(f"ERROR: {error_msg}")
        import traceback
        print(traceback.format_exc())
        return JsonResponse({'error': error_msg}, status=500)

def get_estado_color(estado):
    """Devuelve un color según el estado de la cita"""
    colores = {
        'pendiente': '#ffc107',  # Amarillo
        'confirmada': '#28a745',  # Verde
        'completada': '#17a2b8',  # Azul claro
        'cancelada': '#dc3545',   # Rojo
        'no_asistio': '#6c757d',  # Gris
    }
    return colores.get(estado, '#6c757d')  # Gris por defecto

def agenda_medico(request):
    """
    Vista para la agenda de médicos.
    """
    # Verificar si el usuario está autenticado
    if not request.user.is_authenticated:
        return redirect('admin:login')

    # Obtener médicos activos con sus especialidades
    medicos = UsuarioMedico.objects.filter(
        activo=True
    ).prefetch_related(
        'medicoespecialidad_set__especialidad'
    ).order_by('Apellidos_Medicos', 'Nombres_Medico')

    # Preparar la lista de médicos con sus especialidades para el contexto
    medicos_con_especialidad = []
    for medico in medicos:
        # Obtener todas las especialidades del médico
        especialidades = []
        for me in medico.medicoespecialidad_set.all():
            especialidades.append({
                'id': me.especialidad.id_Especialidad_Medica,
                'nombre': me.especialidad.Espacialidad_Medica,
                'activo': me.activo
            })

        # Agregar el médico a la lista con sus especialidades
        if especialidades:  # Solo incluir médicos con al menos una especialidad
            medicos_con_especialidad.append({
                'id_Medico': medico.id_Medico,
                'Nombres_Medico': medico.Nombres_Medico,
                'Apellidos_Medicos': medico.Apellidos_Medicos,
                'especialidades': especialidades
            })

    # Preparar el contexto para el template
    context = {
        'medicos': medicos_con_especialidad,
        'title': 'Agenda de Médicos'
    }

    return render(request, 'citas/agenda/agenda_medico.html', context)

def editar_cita(request, cita_id):
    """
    Vista para editar una cita existente en la tabla citas_reservadas
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        from django.utils import timezone
        from datetime import datetime, timedelta
        from .models import CitasReservadas, HorarioCita, Paciente, UsuarioMedico, EspecialidadMedica
        
        # Obtener la cita existente
        try:
            cita = CitasReservadas.objects.get(id=cita_id)
        except CitasReservadas.DoesNotExist:
            return JsonResponse({'error': 'Cita no encontrada'}, status=404)
        
        # Obtener datos del formulario
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
            
        # Actualizar campos de la cita
        if 'fecha' in data and 'hora' in data:
            try:
                fecha_hora_str = f"{data['fecha']}T{data['hora']}"
                fecha_hora_dt = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M')
                fecha_hora_dt = timezone.make_aware(fecha_hora_dt)
                duracion = int(data.get('duracion', 30))  # 30 minutos por defecto
                fecha_fin_dt = fecha_hora_dt + timedelta(minutes=duracion)
                
                cita.start_datetime = fecha_hora_dt
                cita.end_datetime = fecha_fin_dt
            except (ValueError, TypeError) as e:
                return JsonResponse(
                    {'error': f'Formato de fecha u hora inválido: {str(e)}'}, 
                    status=400
                )
        
        # Actualizar otros campos si se proporcionan
        if 'paciente' in data:
            try:
                cita.paciente = Paciente.objects.get(id_Paciente=data['paciente'])
            except Paciente.DoesNotExist:
                return JsonResponse({'error': 'Paciente no encontrado'}, status=404)
                
        if 'medico' in data or 'especialidad_id' in data:
            try:
                medico_id = data.get('medico', cita.horario.medico.id_Medico)
                especialidad_id = data.get('especialidad_id', cita.horario.especialidad.id_Especialidad_Medica)
                
                # Buscar un horario existente o crear uno nuevo
                horario = HorarioCita.objects.filter(
                    medico_id=medico_id,
                    especialidad_id=especialidad_id,
                    start_datetime__lte=cita.start_datetime,
                    end_datetime__gte=cita.end_datetime,
                    activo=True
                ).first()
                
                if not horario:
                    # Crear un nuevo horario si no existe uno
                    horario = HorarioCita(
                        medico_id=medico_id,
                        especialidad_id=especialidad_id,
                        turno_id=1,  # Asignar un turno por defecto
                        start_datetime=cita.start_datetime,
                        end_datetime=cita.end_datetime,
                        activo=True
                    )
                    horario.save()
                
                cita.horario = horario
                
            except (UsuarioMedico.DoesNotExist, EspecialidadMedica.DoesNotExist) as e:
                return JsonResponse(
                    {'error': 'Médico o especialidad no encontrado'}, 
                    status=404
                )
        
        # Actualizar campos adicionales
        if 'notas' in data:
            cita.nota = data['notas']
            
        if 'costo' in data:
            cita.costo = data['costo']
        
        # Guardar los cambios
        cita.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cita actualizada exitosamente',
            'cita_id': cita.id
        })
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error al actualizar cita: {str(e)}\n{error_trace}")
        
        return JsonResponse(
            {
                'success': False,
                'error': 'Error al actualizar la cita',
                'details': str(e)
            }, 
            status=500
        )

def guardar_cita(request):
    """
    Vista para guardar una nueva cita en la tabla citas_reservadas
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        import json
        from django.utils import timezone
        from datetime import datetime, timedelta
        from .models import CitasReservadas, HorarioCita, Paciente, UsuarioMedico, EspecialidadMedica
        
        # Obtener datos del formulario
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
            
        paciente_id = data.get('paciente')
        medico_id = data.get('medico')
        especialidad_id = data.get('especialidad_id')
        fecha = data.get('fecha')
        hora = data.get('hora')
        duracion = int(data.get('duracion', 30))  # 30 minutos por defecto
        notas = data.get('notas', '')
        costo = data.get('costo', '0.00')
        
        # Validaciones básicas
        if not all([paciente_id, medico_id, fecha, hora]):
            return JsonResponse(
                {'error': 'Faltan campos requeridos: paciente, médico, fecha u hora'}, 
                status=400
            )
        
        # Convertir la fecha/hora al formato correcto
        try:
            fecha_hora_str = f"{fecha}T{hora}"
            fecha_hora_dt = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M')
            fecha_hora_dt = timezone.make_aware(fecha_hora_dt)
            fecha_fin_dt = fecha_hora_dt + timedelta(minutes=duracion)
        except (ValueError, TypeError) as e:
            return JsonResponse(
                {'error': f'Formato de fecha u hora inválido: {str(e)}'}, 
                status=400
            )
        
        # Obtener el paciente, médico y especialidad
        try:
            paciente = Paciente.objects.get(id_Paciente=paciente_id)
            medico = UsuarioMedico.objects.get(id_Medico=medico_id)
            especialidad = EspecialidadMedica.objects.get(id_Especialidad_Medica=especialidad_id)
        except (Paciente.DoesNotExist, UsuarioMedico.DoesNotExist, EspecialidadMedica.DoesNotExist) as e:
            return JsonResponse(
                {'error': 'Paciente, médico o especialidad no encontrado'}, 
                status=404
            )
        
        # Buscar un horario existente o crear uno temporal
        horario = HorarioCita.objects.filter(
            medico=medico,
            especialidad=especialidad,
            start_datetime__lte=fecha_hora_dt,
            end_datetime__gte=fecha_fin_dt,
            activo=True
        ).first()
        
        if not horario:
            # Crear un nuevo horario si no existe uno
            horario = HorarioCita(
                medico=medico,
                especialidad=especialidad,
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
        error_trace = traceback.format_exc()
        print(f"Error al guardar cita: {str(e)}\n{error_trace}")
        
        return JsonResponse(
            {
                'success': False,
                'error': 'Error al guardar la cita',
                'details': str(e)
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
        
        if total_horarios == 0:
            logger.warning('[HORARIOS] No se encontraron horarios para procesar')
            logger.warning(f'[HORARIOS] Parámetros de búsqueda - Médico ID: {medico_id}, Especialidad ID: {especialidad_id}')
            logger.warning('[HORARIOS] Verificar que existan horarios activos para esta combinación')
        
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

def prueba_template(request):
    from django.contrib.auth import get_user_model
    from citas.models import EspecialidadMedica, UsuarioMedico, MedicoEspecialidad
   # from django.db.models import Prefetch
    
    # Obtener todas las especialidades
    especialidades = EspecialidadMedica.objects.all().order_by('Espacialidad_Medica')
    
    # Obtener todos los médicos activos con sus especialidades
    medicos = UsuarioMedico.objects.filter(activo=True).order_by('Nombres_Medico', 'Apellidos_Medicos')
    
    # Crear una lista de médicos con su especialidad principal
    medicos_con_especialidad = []
    for medico in medicos:
        medico_data = {
            'id_Medico': medico.id_Medico,
            'Nombres_Medico': medico.Nombres_Medico,
            'Apellidos_Medicos': medico.Apellidos_Medicos,
        }
        medicos_con_especialidad.append(medico_data)
    
    return render(request, 'citas/reservas/calendario_nuevo.html', {
        'title': 'Prueba de Calendario',
        'hoy': '2025-10-24',
        'medicos': medicos_con_especialidad,
        'especialidades': especialidades,
        'opts': {'app_label': 'citas'}
    })

@require_http_methods(["GET"])
def obtener_disponibilidad_medico(request, medico_id, especialidad_id):
    """Obtiene la disponibilidad de un médico para una especialidad específica"""
    try:
        # Obtener horarios activos del médico para la especialidad
        horarios = HorarioCita.objects.filter(
            medico_id=medico_id,
            especialidad_id=especialidad_id,
            activo=True
        ).select_related('medico', 'especialidad', 'turno')
        
        disponibilidad = []
        for horario in horarios:
            disponibilidad.append({
                'id': horario.id,
                'title': f'Disponible - {horario.medico.Nombres_Medico}',
                'start': horario.start_datetime.isoformat(),
                'end': horario.end_datetime.isoformat(),
                'color': '#28a745',  # Verde para disponibilidad
                'textColor': 'white',
                'display': 'background',
                'classNames': 'disponibilidad-medico',
                'extendedProps': {
                    'tipo': 'disponibilidad',
                    'medico_id': horario.medico_id,
                    'especialidad_id': horario.especialidad_id,
                    'domicilio': horario.domicilio,
                    'turno': horario.turno.nombre if horario.turno else ''
                }
            })
        
        return JsonResponse({'disponibilidad': disponibilidad})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def obtener_horas_disponibles(request, medico_id, especialidad_id, fecha):
    """Obtiene horas disponibles específicas para agendar cita"""
    try:
        from datetime import datetime, date, time
        import json
        
        # Convertir fecha string a objeto date
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        
        # Obtener horarios del médico para esa fecha
        horarios = HorarioCita.objects.filter(
            medico_id=medico_id,
            especialidad_id=especialidad_id,
            activo=True,
            start_datetime__date=fecha_obj
        )
        
        # Obtener citas ya agendadas para esa fecha - USAR CitasReservadas
        citas_agendadas = CitasReservadas.objects.filter(
            horario__medico_id=medico_id,
            horario__especialidad_id=especialidad_id,
            start_datetime__date=fecha_obj
        ).values_list('start_datetime', flat=True)
        
        horas_disponibles = []
        
        for horario in horarios:
            # Generar slots de tiempo disponibles
            hora_actual = horario.start_datetime
            while hora_actual < horario.end_datetime:
                # Verificar si este slot no está ocupado
                if hora_actual not in citas_agendadas:
                    horas_disponibles.append({
                        'hora': hora_actual.time().strftime('%H:%M:%S'),
                        'hora_formateada': hora_actual.time().strftime('%I:%M %p'),
                        'fecha_completa': hora_actual.isoformat()
                    })
                
                # Avanzar 30 minutos (duración estándar de cita)
                hora_actual = hora_actual + timedelta(minutes=30)
        
        return JsonResponse({'horas_disponibles': horas_disponibles})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def obtener_horarios_recurrentes(request):
    """Obtiene los horarios recurrentes procesados correctamente"""
    try:
        medico_id = request.GET.get('medico_id')
        especialidad_id = request.GET.get('especialidad_id')
        start = request.GET.get('start')
        end = request.GET.get('end')
        
        print(f"🔄 obtener_horarios_recurrentes - médico: {medico_id}, especialidad: {especialidad_id}")
        print(f"📅 Rango: {start} a {end}")
        
        eventos = []
        
        # Obtener horarios base
        horarios = HorarioCita.objects.filter(activo=True)
        
        if medico_id:
            horarios = horarios.filter(medico_id=medico_id)
        if especialidad_id:
            horarios = horarios.filter(especialidad_id=especialidad_id)
        
        print(f"🔍 Horarios encontrados: {horarios.count()}")
        
        for horario in horarios:
            start_datetime = horario.start_datetime
            end_datetime = horario.end_datetime
            
            print(f"📋 Procesando horario {horario.id}:")
            print(f"   - Inicio: {start_datetime}")
            print(f"   - Fin: {end_datetime}")
            print(f"   - Regla: {horario.recurrence_rule}")

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
                
                print(f"   - Días de la semana: {dias_semana}")
                
                # Extraer fecha UNTIL si existe
                until_date = None
                if 'UNTIL=' in horario.recurrence_rule:
                    try:
                        until_part = [p for p in horario.recurrence_rule.split(';') if 'UNTIL=' in p][0]
                        until_str = until_part.split('=')[1]
                        until_date_utc = datetime.strptime(until_str, '%Y%m%dT%H%M%SZ')
                        until_date = until_date_utc.date()
                        print(f"   - Fecha UNTIL: {until_date}")
                    except Exception as e:
                        print(f"   - Error procesando UNTIL: {e}")

                # Crear eventos recurrentes
                fecha_base = start_datetime.date()
                semana = 0
                max_semanas = 8  # Reducido a 8 semanas para pruebas
                
                # Convertir fechas de filtro
                start_date_filter = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z').date() if start else None
                end_date_filter = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z').date() if end else None
                
                print(f"   - Filtro: {start_date_filter} a {end_date_filter}")
                
                eventos_creados = 0
                
                while semana < max_semanas and eventos_creados < 50:  # Límite por seguridad
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
                            
                        # Verificar si está dentro del rango solicitado
                        if start_date_filter and end_date_filter:
                            if not (start_date_filter <= evento_date <= end_date_filter):
                                continue
                        
                        # Crear evento
                        evento_start = datetime.combine(evento_date, start_datetime.time())
                        evento_end = datetime.combine(evento_date, end_datetime.time())
                        
                        # Hacer las fechas conscientes de la zona horaria
                        if timezone.is_naive(evento_start):
                            evento_start = timezone.make_aware(evento_start)
                            evento_end = timezone.make_aware(evento_end)
                        
                        eventos.append({
                            'id': f"disp_{horario.id}_{evento_date.strftime('%Y%m%d')}",
                            'title': '⏰ Disponible',
                            'start': evento_start.isoformat(),
                            'end': evento_end.isoformat(),
                            'color': '#e8f5e8',
                            'textColor': '#2e7d32',
                            'display': 'background',
                            'extendedProps': {
                                'tipo': 'disponibilidad',
                                'medico_id': horario.medico_id,
                                'especialidad_id': horario.especialidad_id,
                                'horario_id': horario.id,
                                'recurrente': True,
                                'medico': f"{horario.medico.Nombres_Medico} {horario.medico.Apellidos_Medicos}",
                                'especialidad': horario.especialidad.Espacialidad_Medica
                            },
                            'classNames': 'disponibilidad-medico'
                        })
                        
                        eventos_creados += 1
                        print(f"   ✅ Evento creado: {evento_date} {evento_start.time()}-{evento_end.time()}")
                    
                    semana += 1
                    
                    # Salir del loop si hemos pasado la fecha UNTIL
                    if until_date and (fecha_base + timedelta(weeks=semana)) > until_date:
                        break

            else:
                # Evento único - solo si está dentro del rango
                if start and end:
                    start_date_filter = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z').date()
                    end_date_filter = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z').date()
                    if not (start_date_filter <= start_datetime.date() <= end_date_filter):
                        continue
                
                # Asegurar que las fechas sean conscientes de la zona horaria
                if timezone.is_naive(start_datetime):
                    start_datetime = timezone.make_aware(start_datetime)
                    end_datetime = timezone.make_aware(end_datetime)
                
                eventos.append({
                    'id': f"disp_{horario.id}",
                    'title': '⏰ Disponible',
                    'start': start_datetime.isoformat(),
                    'end': end_datetime.isoformat(),
                    'color': '#e8f5e8',
                    'textColor': '#2e7d32',
                    'display': 'background',
                    'extendedProps': {
                        'tipo': 'disponibilidad',
                        'medico_id': horario.medico_id,
                        'especialidad_id': horario.especialidad_id,
                        'horario_id': horario.id,
                        'recurrente': False,
                        'medico': f"{horario.medico.Nombres_Medico} {horario.medico.Apellidos_Medicos}",
                        'especialidad': horario.especialidad.Espacialidad_Medica
                    },
                    'classNames': 'disponibilidad-medico'
                })
                print(f"   ✅ Evento único creado: {start_datetime}")

        print(f"🎯 Total eventos de disponibilidad creados: {len(eventos)}")
        return JsonResponse(eventos, safe=False)
        
    except Exception as e:
        print(f"❌ ERROR en obtener_horarios_recurrentes: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
        
@require_http_methods(["GET"])
def obtener_citas_y_disponibilidad(request):
    """Obtiene tanto las citas agendadas como la disponibilidad recurrente"""
    try:
        from dateutil import rrule
        from django.utils import timezone
        
        medico_id = request.GET.get('medico_id')
        especialidad_id = request.GET.get('especialidad_id')
        start = request.GET.get('start')
        end = request.GET.get('end')
        
        eventos = []
        
        # 1. Obtener horarios de disponibilidad
        if medico_id and especialidad_id:
            # Obtener horarios regulares del médico
            horarios = HorarioCita.objects.filter(
                medico_id=medico_id,
                especialidad_id=especialidad_id,
                activo=True
            ).select_related('medico', 'especialidad')
            
            # Convertir fechas de string a datetime
            start_dt = timezone.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
            end_dt = timezone.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z')
            
            for horario in horarios:
                # Si es un horario recurrente
                if horario.recurrence_rule:
                    try:
                        rules = rrule.rrulestr(horario.recurrence_rule, dtstart=horario.start_datetime)
                        ocurrencias = list(rules.between(start_dt, end_dt, inc=True))
                        
                        for ocurrencia in ocurrencias:
                            inicio = ocurrencia
                            fin = ocurrencia + (horario.end_datetime - horario.start_datetime)
                            
                            if timezone.is_naive(inicio):
                                inicio = timezone.make_aware(inicio)
                                fin = timezone.make_aware(fin)
                            
                            eventos.append({
                                'id': f"disp_{horario.id}_{inicio.strftime('%Y%m%d%H%M')}",
                                'title': 'Disponible',
                                'start': inicio.isoformat(),
                                'end': fin.isoformat(),
                                'color': '#e8f5e9',
                                'textColor': '#1b5e20',
                                'display': 'background',
                                'extendedProps': {
                                    'tipo': 'disponibilidad',
                                    'medico_id': horario.medico_id,
                                    'especialidad_id': horario.especialidad_id,
                                    'horario_id': horario.id,
                                    'recurrente': True
                                },
                                'classNames': 'disponibilidad-medico'
                            })
                            
                    except Exception as e:
                        print(f"Error al procesar horario recurrente: {str(e)}")
                        continue
                else:
                    # Para horarios no recurrentes
                    inicio = horario.start_datetime
                    fin = horario.end_datetime
                    
                    if (inicio <= end_dt and fin >= start_dt):
                        eventos.append({
                            'id': f"disp_{horario.id}",
                            'title': 'Disponible',
                            'start': inicio.isoformat(),
                            'end': fin.isoformat(),
                            'color': '#e8f5e9',
                            'textColor': '#1b5e20',
                            'display': 'background',
                            'extendedProps': {
                                'tipo': 'disponibilidad',
                                'medico_id': horario.medico_id,
                                'especialidad_id': horario.especialidad_id,
                                'horario_id': horario.id,
                                'recurrente': False
                            },
                            'classNames': 'disponibilidad-medico'
                        })
        
        # 2. Obtener citas agendadas
        citas = CitasReservadas.objects.filter(
            start_datetime__range=(start, end)
        ).select_related('paciente', 'horario__medico', 'horario__especialidad')
        
        if medico_id:
            citas = citas.filter(horario__medico_id=medico_id)
        if especialidad_id:
            citas = citas.filter(horario__especialidad_id=especialidad_id)
            
        for cita in citas:
            eventos.append({
                'id': f"cita_{cita.id}",
                'title': f'Cita - {cita.paciente.Nombres_Paciente}',
                'start': cita.start_datetime.isoformat(),
                'end': cita.end_datetime.isoformat(),
                'color': get_color_estado(cita.estado),
                'textColor': 'white',
                'extendedProps': {
                    'tipo': 'cita',
                    'estado': cita.estado,
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
        return JsonResponse({'error': str(e)}, status=500)

# Funciones auxiliares para colores y clases
def get_color_estado(estado):
    """Devuelve el color según el estado de la cita"""
    colores = {
        'pendiente': '#ffc107',      # Amarillo
        'confirmada': '#28a745',     # Verde
        'completada': '#17a2b8',     # Azul
        'cancelada': '#dc3545',      # Rojo
        'no_asistio': '#6c757d',     # Gris
    }
    return colores.get(estado.lower(), '#6c757d')  # Gris por defecto

def get_clase_estado(estado):
    # Devuelve la clase CSS según el estado
    return f'estado-{estado.lower()}'

@csrf_exempt
def actualizar_estado_cita(request):
    """
    Vista para actualizar el estado de una cita.
    """
    print("\n=== SOLICITUD RECIBIDA EN actualizar_estado_cita ===")
    print(f"Método: {request.method}")
    print(f"Datos POST: {request.POST}")
    
    if request.method != 'POST':
        error_msg = 'Método no permitido. Se esperaba POST.'
        print(f"❌ {error_msg}")
        return JsonResponse({'estado': 'error', 'mensaje': error_msg}, status=405)
    
    try:
        # Obtener los datos de la solicitud
        cita_id = request.POST.get('id')
        nuevo_estado = request.POST.get('estado', '').upper()
        
        print(f"📝 Datos recibidos - ID: {cita_id}, Nuevo estado: {nuevo_estado}")
        
        if not cita_id:
            error_msg = 'El ID de la cita es requerido'
            print(f"❌ {error_msg}")
            return JsonResponse({'estado': 'error', 'mensaje': error_msg}, status=400)
            
        if not nuevo_estado:
            error_msg = 'El nuevo estado es requerido'
            print(f"❌ {error_msg}")
            return JsonResponse({'estado': 'error', 'mensaje': error_msg}, status=400)
        
        # Validar que el estado sea uno de los permitidos
        estados_permitidos = {
            'PENDIENTE': 'pendiente',
            'CONFIRMADA': 'confirmada',
            'CANCELADA': 'cancelada',
            'COMPLETADA': 'completada',
            'REPROGRAMADA': 'reprogramada'
        }
        
        # Convertir el estado a minúsculas para la comparación
        estado_lower = nuevo_estado.lower()
        if estado_lower not in estados_permitidos.values():
            estados_str = ", ".join([k for k in estados_permitidos.keys()])
            error_msg = f'Estado no válido. Debe ser uno de: {estados_str}'
            print(f"❌ {error_msg}")
            return JsonResponse({'estado': 'error', 'mensaje': error_msg}, status=400)
        
        # Obtener la cita
        try:
            # Manejar el formato 'cita_X' si es necesario
            if isinstance(cita_id, str) and cita_id.startswith('cita_'):
                cita_id = cita_id.replace('cita_', '')
                print(f"🔍 Formato de ID detectado, nuevo ID: {cita_id}")
            
            print(f"🔍 Buscando cita con ID: {cita_id}")
            cita_id = int(cita_id)  # Asegurarse de que sea un entero
            cita = CitasReservadas.objects.get(id=cita_id)
            print(f"✅ Cita encontrada: {cita}")
        except CitasReservadas.DoesNotExist:
            error_msg = f'No se encontró la cita con ID: {cita_id}'
            print(f"❌ {error_msg}")
            return JsonResponse({'estado': 'error', 'mensaje': error_msg}, status=404)
        except Exception as e:
            error_msg = f'Error al buscar la cita: {str(e)}'
            print(f"❌ {error_msg}")
            return JsonResponse({'estado': 'error', 'mensaje': error_msg}, status=500)
        
        # Actualizar el estado de la cita
        try:
            print(f"🔄 Actualizando estado de la cita {cita_id} a {estado_lower}")
            cita.estado = estado_lower
            cita.save()
            print("✅ Estado actualizado correctamente")
        except Exception as e:
            error_msg = f'Error al actualizar el estado: {str(e)}'
            print(f"❌ {error_msg}")
            return JsonResponse({'estado': 'error', 'mensaje': error_msg}, status=500)
        
        # Registrar el cambio de estado
        print(f"✅ Estado de la cita {cita_id} actualizado a {nuevo_estado}")
        
        return JsonResponse({
            'estado': 'success',
            'mensaje': f'Estado de la cita actualizado a {nuevo_estado}',
            'nuevo_estado': nuevo_estado,
            'clase_estado': get_clase_estado(nuevo_estado)
        })
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"\n❌ ERROR NO MANEJADO EN actualizar_estado_cita")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print(f"Traceback completo:\n{error_trace}")
        
        return JsonResponse({
            'estado': 'error',
            'mensaje': f'Error interno del servidor: {str(e)}',
            'tipo_error': type(e).__name__,
            'traceback': error_trace
        }, status=500)

# API para obtener médicos por especialidad
# Función de debug para probar la API
@csrf_exempt
@require_http_methods(["GET"])
def debug_get_especialidades(request, medico_id):
    """
    Función de debug para probar la carga de especialidades
    """
    print("\n=== DEBUG: debug_get_especialidades ===")
    print(f"Médico ID recibido: {medico_id}")

    try:
        # Verificar que el médico existe
        medico = UsuarioMedico.objects.get(id_Medico=medico_id)
        print(f"Médico encontrado: {medico.Nombres_Medico} {medico.Apellidos_Medicos}")

        # Mostrar todas las especialidades del médico
        especialidades_medico = MedicoEspecialidad.objects.filter(medico=medico).select_related('especialidad')
        print(f"Total de relaciones médico-especialidad: {especialidades_medico.count()}")

        for me in especialidades_medico:
            print(f"  - Especialidad: {me.especialidad.Espacialidad_Medica} (ID: {me.especialidad.id_Especialidad_Medica}), Activa: {me.activo}")

        # Crear la respuesta
        especialidades_list = []
        for me in especialidades_medico:
            especialidad_data = {
                'id': me.especialidad.id_Especialidad_Medica,
                'nombre': me.especialidad.Espacialidad_Medica,
                'activo': me.activo
            }
            especialidades_list.append(especialidad_data)
            print(f"Agregando especialidad: {especialidad_data}")

        response_data = {
            'success': True,
            'especialidades': especialidades_list,
            'total': len(especialidades_list),
            'medico': f"{medico.Nombres_Medico} {medico.Apellidos_Medicos}"
        }

        print(f"Respuesta final: {response_data}")
        return JsonResponse(response_data)

    except UsuarioMedico.DoesNotExist:
        print(f"ERROR: Médico con ID {medico_id} no existe")
        return JsonResponse({
            'success': False,
            'error': f'Médico con ID {medico_id} no existe'
        }, status=404)

    except Exception as e:
        print(f"ERROR inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)

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

# API para obtener la disponibilidad de un médico
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

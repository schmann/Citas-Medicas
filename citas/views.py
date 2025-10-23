# citas/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .forms import RegistroPacienteForm
from .models import Ciudad, Municipio, Parroquia, Estado, Pais
from django.contrib.auth.decorators import login_required
from .models import EspecialidadMedica, HorarioCita
from .forms import EspecialidadMedicaForm
from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
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
        especialidades = MedicoEspecialidad.objects.filter(
            medico_id=medico_id, 
            activo=True
        ).select_related('especialidad').values(
            'especialidad__id_Especialidad_Medica', 
            'especialidad__Espacialidad_Medica'
        )
        # Renombrar las claves para que sean más amigables
        especialidades = [
            {
                'id': e['especialidad__id_Especialidad_Medica'],
                'nombre': e['especialidad__Espacialidad_Medica']
            }
            for e in especialidades
        ]
        return JsonResponse(especialidades, safe=False)
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
# VISTAS DE AGENDA Y CALENDARIO
# -------------------------------------------------------------
@staff_member_required(login_url=reverse_lazy('admin:login'))
def agenda_medico(request):
    """Renderiza la plantilla del calendario."""
    return render(request, 'citas/agenda/agenda_medico.html', {})

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
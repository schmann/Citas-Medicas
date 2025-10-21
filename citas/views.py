# citas/views.py (CÓDIGO COMPLETO Y CORREGIDO)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .forms import RegistroPacienteForm
from .models import Ciudad, Municipio, Parroquia, Estado, Pais
from django.contrib.auth.decorators import login_required
from .models import EspecialidadMedica
from .forms import EspecialidadMedicaForm
from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import UsuarioMedico, DatosSeniat
from .forms import UsuarioMedicoForm, DatosSeniatForm
from .forms import MedicoEspecialidadForm
from .models import MedicoEspecialidad, Banco
from .forms import BancoForm

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

# Se recomienda usar @login_required si esta vista es accedida desde el admin de Django
# @login_required 
# Vistas AJAX para combos dependientes

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
    print("\n=== INICIO DE SOLICITUD AJAX ===")
    print("Parámetros recibidos:", request.GET)
    
    tipo = request.GET.get('tipo')
    estado_id = request.GET.get('estado_id')
    municipio_id = request.GET.get('municipio_id')
    
    print(f"Procesando: tipo={tipo}, estado_id={estado_id}, municipio_id={municipio_id}")
    
    try:
        # 1. VALIDACIÓN GENERAL DEL TIPO
        if tipo not in ['ciudades', 'municipios', 'parroquias']: # ⬅️ CORRECCIÓN CRÍTICA: Añadir 'ciudades'
            return JsonResponse({'error': f'Tipo de ubicación no válido: {tipo}. Use "ciudades", "municipios" o "parroquias".'}, status=400)
        
        # 2. LÓGICA DE CARGA DE CIUDADES
        if tipo == 'ciudades': # ⬅️ NUEVO BLOQUE DE LÓGICA
            if not estado_id:
                return JsonResponse({'error': 'Se requiere el ID del estado para cargar ciudades'}, status=400)
            if not estado_id.isdigit():
                return JsonResponse({'error': 'El ID del estado debe ser un número entero'}, status=400)
            
            print(f"Buscando ciudades para estado_id={estado_id}")
            # Usamos el mismo filtro que Municipio para asegurar consistencia
            ciudades = Ciudad.objects.filter(estado_id=int(estado_id)).order_by('nombre')
            print(f"Consulta SQL: {ciudades.query}")
            
            # Mapear al formato esperado por el frontend
            # Nota: El JS espera 'id_Ciudad' o 'id'
            items = [{'id': c.id_Ciudad, 'nombre': c.nombre} for c in ciudades]
            print(f"Ciudades encontradas: {len(items)}")

        # 3. LÓGICA DE CARGA DE MUNICIPIOS
        elif tipo == 'municipios':
            if not estado_id:
                return JsonResponse({'error': 'Se requiere el ID del estado'}, status=400)
            if not estado_id.isdigit():
                return JsonResponse({'error': 'El ID del estado debe ser un número entero'}, status=400)
            
            print(f"Buscando municipios para estado_id={estado_id}")
            # Usando filter con el nombre correcto del campo foráneo en el modelo
            municipios = Municipio.objects.filter(estado_id=int(estado_id)).order_by('nombre')
            print(f"Consulta SQL: {municipios.query}")
            
            # Mapear al formato esperado por el frontend
            items = [{'id': m.id_Municipio, 'nombre': m.nombre} for m in municipios]
            print(f"Municipios encontrados: {len(items)}")
            
        # 4. LÓGICA DE CARGA DE PARROQUIAS
        elif tipo == 'parroquias':
            if not municipio_id:
                return JsonResponse({'error': 'Se requiere el ID del municipio'}, status=400)
            if not municipio_id.isdigit():
                return JsonResponse({'error': 'El ID del municipio debe ser un número entero'}, status=400)
            
            print(f"Buscando parroquias para municipio_id={municipio_id}")
            # Usando filter con el nombre correcto del campo foráneo en el modelo
            parroquias = Parroquia.objects.filter(municipio_id=int(municipio_id)).order_by('nombre')
            print(f"Consulta SQL: {parroquias.query}")
            
            # Mapear al formato esperado por el frontend
            items = [{'id': p.id_Parroquia, 'nombre': p.nombre} for p in parroquias]
            print(f"Parroquias encontradas: {len(items)}")
        
        print(f"Enviando respuesta: {items}")
        # Retornamos los items (ciudades, municipios o parroquias)
        return JsonResponse(items, safe=False)
            
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Error: {str(e)}")
        print(f"Traceback: {error_traceback}")
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

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'La especialidad del médico se ha eliminado correctamente.')
        return super().delete(request, *args, **kwargs)

def get_especialidades_medico(request, medico_id):
    especialidades = MedicoEspecialidad.objects.filter(
        medico_id=medico_id, 
        activo=True
    ).select_related('especialidad').values('id', 'especialidad__nombre')
    return JsonResponse(list(especialidades), safe=False)

class BancoListView(ListView):
    model = Banco
    template_name = 'citas/banco_list.html'
    context_object_name = 'bancos'
    paginate_by = 10

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
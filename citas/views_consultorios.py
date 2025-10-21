from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Consultorio
from .forms import ConsultorioForm
from django.db.models import Q

# Vistas basadas en clases
class ConsultorioListView(LoginRequiredMixin, ListView):
    model = Consultorio
    template_name = 'citas/consultorios/consultorio_list.html'
    context_object_name = 'consultorios'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '').strip()
        
        if search_query:
            queryset = queryset.filter(
                Q(numero_consultorio__icontains=search_query) |
                Q(Direccion__icontains(search_query)) |
                Q(Telefono__icontains(search_query)) |
                Q(Especialidad_Medica__nombre__icontains(search_query))
            ).distinct()
            
        return queryset.order_by('numero_consultorio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ConsultorioCreateView(LoginRequiredMixin, CreateView):
    model = Consultorio
    form_class = ConsultorioForm
    template_name = 'citas/consultorios/consultorio_form.html'
    success_url = reverse_lazy('citas:consultorios')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Consultorio {self.object.numero_consultorio} creado exitosamente.')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Consultorio'
        context['action'] = 'create'
        return context


class ConsultorioUpdateView(LoginRequiredMixin, UpdateView):
    model = Consultorio
    form_class = ConsultorioForm
    template_name = 'citas/consultorios/consultorio_form.html'
    success_url = reverse_lazy('citas:consultorios')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Consultorio {self.object.numero_consultorio} actualizado exitosamente.')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar Consultorio: {self.object.numero_consultorio}'
        context['action'] = 'update'
        return context


class ConsultorioDetailView(LoginRequiredMixin, DetailView):
    model = Consultorio
    template_name = 'citas/consultorios/consultorio_detail.html'
    context_object_name = 'consultorio'


class ConsultorioDeleteView(LoginRequiredMixin, DeleteView):
    model = Consultorio
    template_name = 'citas/consultorios/consultorio_confirm_delete.html'
    success_url = reverse_lazy('citas:consultorios')
    
    def delete(self, request, *args, **kwargs):
        consultorio = self.get_object()
        messages.success(request, f'Consultorio {consultorio.numero_consultorio} eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# Vistas basadas en funciones para cambiar el estado
@login_required
def toggle_consultorio_status(request, pk):
    consultorio = get_object_or_404(Consultorio, pk=pk)
    consultorio.Status = not consultorio.Status
    consultorio.save(update_fields=['Status'])
    
    status = 'activado' if consultorio.Status else 'desactivado'
    messages.success(request, f'Consultorio {consultorio.numero_consultorio} {status} exitosamente.')
    
    return redirect('citas:consultorios')

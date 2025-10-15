from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Paciente

def home(request):
    return render(request, 'index/home.html')

def registrar_paciente(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            paciente = Paciente(
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                edad=request.POST.get('edad'),
                genero=request.POST.get('genero'),
                telefono=request.POST.get('telefono'),
                email=request.POST.get('email', ''),
                direccion=request.POST.get('direccion', ''),
                fecha_nacimiento=request.POST.get('fecha_nacimiento'),
                fecha_ingreso=timezone.now().date(),
                fecha_egreso=None
            )
            paciente.save()
            messages.success(request, '¡Paciente registrado exitosamente!')
            return redirect('registrar_paciente')
            
        except Exception as e:
            messages.error(request, f'Error al registrar el paciente: {str(e)}')
    
    return render(request, 'index/registrar_paciente.html')

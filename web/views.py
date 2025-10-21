# web/views.py

from django.shortcuts import render

# La función 'inicio' debe existir y tomar un argumento 'request'
def inicio(request):
    # Esto busca y renderiza el contenido de web/templates/web/index.html
    return render(request, 'web/index.html', {})
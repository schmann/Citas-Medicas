 
# web/urls.py
from django.urls import path
from . import views

app_name = 'web' 

urlpatterns = [
    # Mapea la URL raíz del módulo (que será la raíz del sitio) a la función 'inicio'
    path('', views.inicio, name='inicio'),
]
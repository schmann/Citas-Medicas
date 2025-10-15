from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registrar-paciente/', views.registrar_paciente, name='registrar_paciente'),
]
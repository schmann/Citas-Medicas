from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.utils.functional import SimpleLazyObject

app_name = 'citas'  # Usamos el mismo namespace que en urls.py

def get_cita_web_urls():
    # Importar las vistas de la web de citas aquí para evitar importaciones circulares
    from .views_cita_web import (
        crear_cita,
        disponibilidad_medico,
        guardar_cita,
        medicos_por_especialidad,
        horarios_agendados_medico,
        registrar_paciente,
        get_especialidades_medico as obtener_especialidades_medico,
        obtener_horas_disponibles,
        obtener_citas_y_disponibilidad,
        obtener_eventos,
        editar_cita,
        actualizar_estado_cita
    )
    
    return [
        # Página principal para crear citas
        path('', crear_cita, name='home'),
        
        # Registro de pacientes
        path('registrar/', registrar_paciente, name='registrar_paciente'),
        
        # API para el calendario y citas
        path('api/obtener-citas-y-disponibilidad/', obtener_citas_y_disponibilidad, name='obtener_citas_y_disponibilidad'),
        path('api/get-especialidades/<int:medico_id>/', obtener_especialidades_medico, name='get_especialidades_medico'),
        path('api/obtener-horas-disponibles/<int:medico_id>/<int:especialidad_id>/<str:fecha>/', 
             obtener_horas_disponibles, name='obtener_horas_disponibles'),
        path('api/crear-cita/', crear_cita, name='crear_cita'),
        path('api/eventos/', csrf_exempt(obtener_eventos), name='obtener_eventos'),
        path('api/guardar-cita/', csrf_exempt(guardar_cita), name='guardar_cita'),
        path('api/medicos/', csrf_exempt(medicos_por_especialidad), name='api_medicos'),
        path('api/disponibilidad-medico/', csrf_exempt(disponibilidad_medico), name='disponibilidad_medico'),
        path('api/horarios-agendados-medico/', csrf_exempt(horarios_agendados_medico), name='horarios_agendados_medico'),
        path('api/editar-cita/<int:cita_id>/', csrf_exempt(editar_cita), name='editar_cita'),
        path('api/actualizar-estado-cita/', csrf_exempt(actualizar_estado_cita), name='actualizar_estado_cita'),
    ]

# Usar SimpleLazyObject para cargar las URLs de manera perezosa
urlpatterns = SimpleLazyObject(get_cita_web_urls)

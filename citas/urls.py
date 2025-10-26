from django.urls import path, include
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from . import views
from .views_crear_cita import crear_cita, disponibilidad_medico, guardar_cita as guardar_cita_view
from .views_consultorios import (
    ConsultorioListView, ConsultorioCreateView, ConsultorioUpdateView,
    ConsultorioDetailView, ConsultorioDeleteView, toggle_consultorio_status
)

app_name = 'citas'

urlpatterns = [
    path('registrar/', views.registrar_paciente, name='registrar'),  # Cambiado de 'registrar_paciente' a 'registrar'
    path('ajax/cargar-ubicaciones/', views.cargar_ubicaciones, name='cargar_ubicaciones'), 
    
    # URLs para combos dependientes
    path('ajax/load-estados/', views.load_estados, name='ajax_load_estados'),
    path('ajax/load-ciudades/', views.load_ciudades, name='ajax_load_ciudades'),
    path('ajax/load-municipios/', views.load_municipios, name='ajax_load_municipios'),
    path('ajax/load-parroquias/', views.load_parroquias, name='ajax_load_parroquias'),
    
    # URLs de especialidades
    path('especialidad/listar/', views.listar_especialidades, name='listar_especialidades'),
    path('especialidad/crear/', views.crear_especialidad, name='crear_especialidad'),
    path('especialidad/editar/<int:id>/', views.editar_especialidad, name='editar_especialidad'),
    path('especialidad/eliminar/<int:id>/', views.eliminar_especialidad, name='eliminar_especialidad'),
    
    # URLs de médicos
    path('medicos/', views.UsuarioMedicoListView.as_view(), name='listar_medicos'),
    path('medicos/nuevo/', views.UsuarioMedicoCreateView.as_view(), name='crear_medico'),
    path('medicos/editar/<int:pk>/', views.UsuarioMedicoUpdateView.as_view(), name='editar_medico'),
    path('medicos/eliminar/<int:pk>/', views.UsuarioMedicoDeleteView.as_view(), name='eliminar_medico'),

    # URLs de especialidades de médicos
    path('medico-especialidad/listar/', views.MedicoEspecialidadListView.as_view(), name='medico_especialidad_list'),
    path('medico-especialidad/crear/', views.MedicoEspecialidadCreateView.as_view(), name='medico_especialidad_create'),
    path('medico-especialidad/editar/<int:pk>/', views.MedicoEspecialidadUpdateView.as_view(), name='medico_especialidad_update'),
    path('medico-especialidad/eliminar/<int:pk>/', views.MedicoEspecialidadDeleteView.as_view(), name='medico_especialidad_delete'),
    
    # URLs para Consultorios
    path('consultorios/', login_required(ConsultorioListView.as_view()), name='consultorios'),
    path('consultorios/crear/', login_required(ConsultorioCreateView.as_view()), name='consultorio_create'),
    path('consultorios/editar/<int:pk>/', login_required(ConsultorioUpdateView.as_view()), name='consultorio_update'),
    path('consultorios/ver/<int:pk>/', login_required(ConsultorioDetailView.as_view()), name='consultorio_detail'),
    path('consultorios/eliminar/<int:pk>/', login_required(ConsultorioDeleteView.as_view()), name='consultorio_delete'),
    path('consultorios/toggle-status/<int:pk>/', login_required(toggle_consultorio_status), name='consultorio_toggle_status'),

    # URL para el calendario
    path('calendario/', views.calendario_nuevo_view, name='calendario'),
    
    # URLs para la API de Citas
    path('api/actualizar-estado-cita/', csrf_exempt(views.actualizar_estado_cita), name='actualizar_estado_cita'),
    path('api/pacientes/', csrf_exempt(views.obtener_pacientes), name='obtener_pacientes'),
    
    # Vista del Calendario
    path('calendario-nuevo/', 
         staff_member_required(
             user_passes_test(
                 lambda u: u.has_perm('citas.view_citasreservadas'), 
                 login_url='admin:login'
             )(views.calendario_nuevo_view)
         ), 
         name='calendario_nuevo'),
    path('api/cancelar-cita/<int:cita_id>/', csrf_exempt(views.cancelar_cita), name='cancelar_cita'),
    
    # URLs para AJAX
    path('ajax/obtener-pacientes/', csrf_exempt(views.obtener_pacientes), name='obtener_pacientes'),
    path('ajax/obtener-medicos/', csrf_exempt(views.obtener_medicos), name='obtener_medicos'),
    
    # URLs de Bancos
    path('bancos/', views.BancoListView.as_view(), name='banco_list'),
    path('bancos/nuevo/', views.BancoCreateView.as_view(), name='banco_create'),
    path('bancos/editar/<int:pk>/', views.BancoUpdateView.as_view(), name='banco_update'),
    path('bancos/eliminar/<int:pk>/', views.BancoDeleteView.as_view(), name='banco_delete'),

    # Ruta para horarios JSON
    path('horarios-json/', csrf_exempt(views.horarios_json), name='horarios_json'),
    
    # Rutas para el calendario y gestión de citas
    path('agenda/', views.agenda_medico, name='agenda_medico'),
    path('api/horarios-medico/<int:medico_id>/<int:especialidad_id>/', csrf_exempt(views.get_horarios_medico_especialidad), name='get_horarios_medico_especialidad'),

     # URLs para el calendario con disponibilidad
    path('calendario-nuevo/', views.calendario_nuevo_view, name='calendario_nuevo'),
    path('api/obtener-citas-y-disponibilidad/', views.obtener_citas_y_disponibilidad, name='obtener_citas_y_disponibilidad'),
    path('api/obtener-horas-disponibles/<int:medico_id>/<int:especialidad_id>/<str:fecha>/', views.obtener_horas_disponibles, name='obtener_horas_disponibles'),
    path('api/crear-cita/', views.crear_cita, name='crear_cita'),

    # API para obtener eventos (citas y disponibilidad)
    path('api/eventos/', csrf_exempt(views.obtener_eventos), name='obtener_eventos'),
    
    # API para guardar citas
    path('api/guardar-cita/', csrf_exempt(views.guardar_cita), name='guardar_cita'),
    
    # API para obtener médicos por especialidad
    path('api/medicos/', csrf_exempt(views.medicos_por_especialidad), name='api_medicos'),
    
    # API para obtener disponibilidad de médico
    path('api/disponibilidad-medico/', csrf_exempt(disponibilidad_medico), name='disponibilidad_medico'),
    
    # Vista para crear una nueva cita
    path('crear-cita/', crear_cita, name='crear_cita'),
    path('api/guardar-cita-nueva/', csrf_exempt(guardar_cita_view), name='guardar_cita_nueva'),
    
    # Ruta para editar una cita existente
    path('api/editar-cita/<int:cita_id>/', csrf_exempt(views.editar_cita), name='editar_cita'),
    
    # Ruta para actualizar el estado de una cita
    path('api/actualizar-estado-cita/', csrf_exempt(views.actualizar_estado_cita), name='actualizar_estado_cita'),
]
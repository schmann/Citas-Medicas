from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views
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

    # URLs de Bancos
    path('bancos/', views.BancoListView.as_view(), name='banco_list'),
    path('bancos/nuevo/', views.BancoCreateView.as_view(), name='banco_create'),
    path('bancos/editar/<int:pk>/', views.BancoUpdateView.as_view(), name='banco_update'),
    path('bancos/eliminar/<int:pk>/', views.BancoDeleteView.as_view(), name='banco_delete'),
]
# UnidadMedica/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

# Importa tu admin personalizado
from citas.admin import admin_site as citas_admin 

urlpatterns = [
    # 1. ADMIN UNIFICADO: Todo el tráfico admin va a tu sitio personalizado.
    path('admin/', citas_admin.urls), 

    # 2. Citas
    path('citas/', include('citas.urls')), 

    # 3. Web (Página de inicio)
    path('', include('web.urls')), 

    # 4. Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Configuración de archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Configuración del admin por defecto (Estos se aplicarán si citas_admin hereda de admin.AdminSite)
admin.site.site_header = 'Unidad Médica Admin'
admin.site.site_title = 'Unidad Médica Admin'
admin.site.index_title = 'Bienvenido al Panel de Administración'
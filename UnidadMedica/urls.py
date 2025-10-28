from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

# Importa tu admin personalizado
from citas.admin import admin_site as citas_admin 

urlpatterns = [
    # Usar tu CustomAdminSite que tiene el menú organizado
    path('admin/', citas_admin.urls), 

    # 2. Citas
    path('citas/', include(('citas.urls', 'citas'), namespace='citas')),

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
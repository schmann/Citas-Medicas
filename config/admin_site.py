from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class CustomAdminSite(admin.AdminSite):
    site_header = getattr(settings, 'ADMIN_SITE_HEADER', 'Unidad Médica - Administración')
    site_title = getattr(settings, 'ADMIN_SITE_TITLE', 'Sistema de Gestión de Pacientes')
    index_title = getattr(settings, 'ADMIN_INDEX_TITLE', 'Panel de Control')

    def get_app_list(self, request, app_label=None):
        """
        Devuelve una lista ordenada de aplicaciones para mostrar en el índice del admin.
        """
        app_dict = self._build_app_dict(request)

        # Ordenar las aplicaciones
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Ordenar los modelos dentro de cada aplicación
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'].lower())

        return app_list

# Crear una instancia del admin personalizado
admin_site = CustomAdminSite(name='custom_admin')

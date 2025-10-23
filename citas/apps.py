# citas/apps.py

from django.apps import AppConfig


class CitasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'citas'
    verbose_name = 'Citas Médicas' # (Opcional, pero bueno para la administración)
    
    def ready(self):
        #ESTO ES CRUCIAL: Importar señales aquí para que se carguen.
        #import citas.signals
        pass
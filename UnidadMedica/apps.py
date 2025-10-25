# UnidadMedica/apps.py
from django.apps import AppConfig

class UnidadMedicaConfig(AppConfig):
    name = 'UnidadMedica'
    verbose_name = 'Unidad Médica'
    
    def ready(self):
        # Forzar la carga de Jazzmin al iniciar
        import django
        django.setup()
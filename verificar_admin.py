"""
Script de verificación del panel de administración
Ejecuta este script para verificar que todo esté funcionando correctamente.
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(str(Path(__file__).resolve().parent))

django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client

def verificar_configuracion():
    """Verificar que la configuración esté correcta"""
    print("=== VERIFICACIÓN DE CONFIGURACIÓN ===")

    # Verificar idioma
    print(f"Idioma configurado: {settings.LANGUAGE_CODE}")

    # Verificar zona horaria
    print(f"Zona horaria: {settings.TIME_ZONE}")

    # Verificar archivos estáticos
    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")

    # Verificar templates
    print(f"TEMPLATES DIRS: {settings.TEMPLATES[0]['DIRS']}")

    # Verificar middleware
    print(f"LocaleMiddleware presente: {'django.middleware.locale.LocaleMiddleware' in settings.MIDDLEWARE}")

    print("✓ Configuración básica verificada")

def verificar_archivos():
    """Verificar que los archivos estén en el lugar correcto"""
    print("\n=== VERIFICACIÓN DE ARCHIVOS ===")

    # Verificar CSS
    css_path = Path(settings.BASE_DIR) / 'index' / 'static' / 'css' / 'admin_custom.css'
    if css_path.exists():
        print(f"✓ Archivo CSS encontrado: {css_path}")
        print(f"  Tamaño: {css_path.stat().st_size} bytes")
    else:
        print(f"✗ Archivo CSS NO encontrado: {css_path}")

    # Verificar templates
    template_path = Path(settings.BASE_DIR) / 'index' / 'templates' / 'admin'
    if template_path.exists():
        print(f"✓ Carpeta de templates admin encontrada: {template_path}")
        # Listar archivos en la carpeta
        for file_path in template_path.rglob('*'):
            if file_path.is_file():
                print(f"  - {file_path.relative_to(settings.BASE_DIR)}")
    else:
        print(f"✗ Carpeta de templates admin NO encontrada: {template_path}")

    # Verificar archivos de traducción
    locale_path = Path(settings.BASE_DIR) / 'locale'
    if locale_path.exists():
        print(f"✓ Archivos de traducción encontrados: {locale_path}")
    else:
        print(f"ℹ Archivos de traducción no encontrados (normal para desarrollo): {locale_path}")

def verificar_urls():
    """Verificar que las URLs estén configuradas correctamente"""
    print("\n=== VERIFICACIÓN DE URLs ===")

    try:
        from config.urls import urlpatterns
        admin_urls = [url for url in urlpatterns if 'admin' in str(url.pattern)]
        if admin_urls:
            print(f"✓ URLs de admin configuradas: {len(admin_urls)} patron(es)")
        else:
            print("✗ No se encontraron URLs de admin")

    except Exception as e:
        print(f"✗ Error verificando URLs: {e}")

if __name__ == "__main__":
    try:
        verificar_configuracion()
        verificar_archivos()
        verificar_urls()

        print("\n=== RESUMEN ===")
        print("Si ves todos los ✓ verdes, el panel debería estar funcionando correctamente.")
        print("Asegúrate de:")
        print("1. Tener el servidor corriendo: python manage.py runserver")
        print("2. Limpiar la caché del navegador (Ctrl+Shift+R)")
        print("3. Acceder a: http://localhost:8000/admin/")

    except Exception as e:
        print(f"\n✗ Error durante la verificación: {e}")
        import traceback
        traceback.print_exc()

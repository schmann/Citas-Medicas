#!/usr/bin/env python
"""
Script de diagnóstico para verificar el estado del proyecto Django
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
    print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")

    # Verificar templates
    print(f"TEMPLATES DIRS: {settings.TEMPLATES[0]['DIRS']}")

    # Verificar middleware
    print(f"LocaleMiddleware presente: {'django.middleware.locale.LocaleMiddleware' in settings.MIDDLEWARE}")

    print("✓ Configuración básica verificada")

def verificar_modelos():
    """Verificar que los modelos estén correctamente registrados"""
    print("\n=== VERIFICACIÓN DE MODELOS ===")

    try:
        from index.models import Paciente
        print(f"✓ Modelo Paciente importado correctamente")

        # Verificar campos del modelo
        campos = [field.name for field in Paciente._meta.fields]
        print(f"✓ Campos del modelo: {campos[:5]}...")  # Mostrar primeros 5 campos

    except Exception as e:
        print(f"✗ Error con el modelo Paciente: {e}")

def verificar_admin():
    """Verificar que el admin esté correctamente configurado"""
    print("\n=== VERIFICACIÓN DE ADMIN ===")

    try:
        from config.admin_site import admin_site
        print("✓ Admin personalizado importado correctamente")

        # Verificar modelos registrados
        registered_models = list(admin_site._registry.keys())
        print(f"✓ Modelos registrados: {[model.__name__ for model in registered_models]}")

    except Exception as e:
        print(f"✗ Error con el admin: {e}")

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
    else:
        print(f"✗ Carpeta de templates admin NO encontrada: {template_path}")

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

def verificar_base_datos():
    """Verificar que la base de datos esté accesible"""
    print("\n=== VERIFICACIÓN DE BASE DE DATOS ===")

    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✓ Base de datos accesible")

    except Exception as e:
        print(f"✗ Error de base de datos: {e}")

if __name__ == "__main__":
    try:
        verificar_configuracion()
        verificar_modelos()
        verificar_admin()
        verificar_archivos()
        verificar_urls()
        verificar_base_datos()

        print("\n=== RESUMEN ===")
        print("Si ves todos los ✓ verdes, el proyecto debería estar funcionando correctamente.")
        print("Asegúrate de:")
        print("1. Tener el servidor corriendo: python manage.py runserver")
        print("2. Limpiar la caché del navegador (Ctrl+Shift+R)")
        print("3. Acceder a: http://localhost:8000/admin/")

    except Exception as e:
        print(f"\n✗ Error durante la verificación: {e}")
        import traceback
        traceback.print_exc()

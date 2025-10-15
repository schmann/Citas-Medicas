#!/usr/bin/env python
"""
Script de diagnóstico simple para verificar el estado del proyecto
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(str(Path(__file__).resolve().parent))

try:
    django.setup()

    from django.contrib.auth.models import User
    from django.contrib import admin

    print("=== DIAGNOSTICO DEL PROYECTO ===")

    # Verificar usuarios
    print("\n1. VERIFICACION DE USUARIOS:")
    users = User.objects.all()
    if users:
        for user in users:
            print(f"   - {user.username}: staff={user.is_staff}, superuser={user.is_superuser}")
    else:
        print("   - No hay usuarios registrados")

    # Verificar modelos en admin
    print("\n2. VERIFICACION DE MODELOS EN ADMIN:")
    try:
        from index.models import Paciente
        print(f"   - Modelo Paciente: OK")

        registry = admin.site._registry
        if Paciente in registry:
            admin_class = registry[Paciente]
            print(f"   - Paciente registrado en admin: {admin_class.__class__.__name__}")
        else:
            print("   - Paciente NO registrado en admin")

    except Exception as e:
        print(f"   - Error con modelo Paciente: {e}")

    # Verificar archivos estáticos
    print("\n3. VERIFICACION DE ARCHIVOS ESTATICOS:")
    css_path = Path(__file__).parent / 'index' / 'static' / 'css' / 'admin_custom.css'
    if css_path.exists():
        print(f"   - CSS encontrado: {css_path}")
        print(f"   - Tamaño: {css_path.stat().st_size} bytes")
    else:
        print("   - CSS NO encontrado")

    print("\n=== RESUMEN ===")
    print("Si ves 'Paciente registrado en admin: PacienteAdmin'")
    print("y tienes un usuario con permisos de administrador,")
    print("el panel deberia funcionar correctamente.")

except Exception as e:
    print(f"Error durante el diagnostico: {e}")
    import traceback
    traceback.print_exc()

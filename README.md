# Sistema de Gestión de Citas Médicas

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-brightgreen)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sistema de gestión de citas médicas desarrollado con Python y Django que permite la programación, seguimiento y administración de citas médicas de manera eficiente, con integración web y atención telefónica automatizada.

## 🚀 Características Principales

- **Gestión de Pacientes**: Registro y seguimiento de historias clínicas
- **Agendamiento de Citas**: Interfaz intuitiva para programar citas
- **Módulo Médico**: Acceso a especialistas para gestionar sus consultas
- **Sistema de Recordatorios**: Notificaciones automáticas vía correo electrónico y SMS
- **Panel de Administración**: Herramientas completas para la gestión del personal y configuración
- **API RESTful**: Para integración con otros sistemas
- **Atención Telefónica Automatizada**: Sistema IVR para gestión de citas por teléfono

## 🛠️ Requisitos Técnicos

- Python 3.8 o superior
- Django 4.2
- Base de datos PostgreSQL
- Redis (para tareas en segundo plano)
- Celery (para manejo de tareas asíncronas)

## 🚀 Instalación

1. Clonar el repositorio:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd Citas-Unidad-Medicas
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: .\venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar las variables de entorno en `.env`

5. Aplicar migraciones:
   ```bash
   python manage.py migrate
   ```

6. Crear un superusuario:
   ```bash
   python manage.py createsuperuser
   ```

7. Iniciar el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

## 📋 Estructura del Proyecto

```
Citas-Unidad-Medicas/
├── apps/
│   ├── accounts/          # Gestión de usuarios y autenticación
│   ├── appointments/      # Lógica de citas médicas
│   ├── patients/          # Gestión de pacientes
│   ├── doctors/           # Módulo de médicos
│   └── core/              # Configuraciones y utilidades centrales
├── static/               # Archivos estáticos (CSS, JS, imágenes)
├── templates/            # Plantillas HTML
└── manage.py             # Script de gestión de Django
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, lee nuestras pautas de contribución para más información.

## 📧 Contacto

Para más información, por favor contacte al equipo de desarrollo.

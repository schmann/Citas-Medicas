# 🏥 Unidad Médica - Sistema de Gestión de Citas

[![Python](https://img.shields.io/badge/Python-3.14-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.7-brightgreen)](https://www.djangoproject.com/)
[![Django Jazzmin](https://img.shields.io/badge/Django%20Jazzmin-3.0.1-0d6efd)](https://django-jazzmin.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sistema integral de gestión médica desarrollado con Python y Django, diseñado para administrar clínicas y consultorios médicos con un enfoque en la experiencia del usuario y la eficiencia operativa.

## 🌟 Características Principales

- **Gestión de Pacientes**: Registro completo de pacientes con historial médico detallado
- **Agenda Médica**: Sistema de citas con disponibilidad en tiempo real
- **Módulo de Médicos**: Perfiles profesionales con especialidades y horarios personalizables
- **Consultorios Virtuales**: Integración con plataformas de telemedicina
- **Facturación Electrónica**: Generación de facturas y recibos
- **Panel de Administración Avanzado**: Interfaz intuitiva basada en Django Jazzmin
- **API RESTful**: Para integración con otros sistemas de salud
- **Reportes y Estadísticas**: Análisis de datos en tiempo real

## 🛠️ Requisitos Técnicos

- Python 3.14
- Django 5.2.7
- PostgreSQL 15+
- Redis (para caché y tareas en segundo plano)
- Celery (para manejo de tareas asíncronas)
- Google API Client (para integración con Google Calendar)
- Pillow (para el manejo de imágenes)

## 🚀 Instalación Rápida

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/rapanuti/Citas-Unidad-Medicas.git
   cd Citas-Unidad-Medicas
   ```

2. Crear y activar entorno virtual:
   ```bash
   # Windows
   python -m venv venvum
   .\venvum\Scripts\activate

   # Linux/Mac
   python3 -m venv venvum
   source venvum/bin/activate
   ```

3. Instalar dependencias:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. Configurar variables de entorno (crear archivo `.env` en la raíz del proyecto):
   ```env
   # Configuración de Django
   DEBUG=True
   SECRET_KEY=tu_clave_secreta_aqui_genera_una_segura
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Base de datos PostgreSQL
   DB_NAME=unidad_medica
   DB_USER=tu_usuario
   DB_PASSWORD=tu_contraseña
   DB_HOST=localhost
   DB_PORT=5432
   
   # Configuración de correo (opcional)
   EMAIL_HOST=smtp.tuservidor.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=tu@email.com
   EMAIL_HOST_PASSWORD=tu_contraseña_email
   DATABASE_URL=postgres://usuario:contraseña@localhost:5432/unidad_medica
   ```

5. Aplicar migraciones:
   ```bash
   python manage.py migrate
   ```

6. Crear superusuario:
   ```bash
   python manage.py createsuperuser
   ```

7. Iniciar el servidor:
   ```bash
   python manage.py runserver
   ```

## 📂 Estructura del Proyecto

```
unidad_medica/
├── citas/                 # Aplicación principal de gestión de citas
├── web/                   # Aplicación web pública
├── static/                # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
├── templates/             # Plantillas base
├── media/                 # Archivos subidos por usuarios
├── .env                   # Variables de entorno
└── manage.py              # Script de gestión de Django
```

## 🔧 Configuración de Google Calendar

1. Habilitar Google Calendar API en Google Cloud Console
2. Descargar el archivo de credenciales JSON
3. Configurar las variables de entorno:
   ```env
   GOOGLE_OAUTH2_CLIENT_ID=tu_client_id
   GOOGLE_OAUTH2_CLIENT_SECRET=tu_client_secret
   GOOGLE_OAUTH2_REDIRECT_URI=http://localhost:8000/oauth2callback/
   ```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:
1. Haz un Fork del proyecto
2. Crea una rama con tu feature (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Haz push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📧 Soporte

Para soporte, por favor contacta a nuestro equipo de desarrollo o abre un issue en el repositorio.

---

Desarrollado con ❤️ por el equipo de Unidad Médica

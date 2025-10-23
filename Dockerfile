# Imagen base oficial de Python
FROM python:3.11-slim

# Variables de entorno básicas
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiar dependencias e instalarlas
COPY requirements.txt .
# Instalación limpia (sin la opción --system que generó error)
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Recolectar archivos estáticos (Django)
RUN python manage.py collectstatic --noinput

# Exponer el puerto
EXPOSE 8000

# Comando por defecto - USAR RUTA ABSOLUTA (/usr/local/bin/gunicorn) para garantizar que se encuentre
# Esto soluciona el error "gunicorn: not found" en entornos Linux.
CMD ["/usr/local/bin/gunicorn", "UnidadMedica.wsgi:application", "--bind", "0.0.0.0:8000"]

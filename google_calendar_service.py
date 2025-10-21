# citas/google_calendar_service.py

import os
import pickle
import logging
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings
from pytz import timezone

logger = logging.getLogger(__name__)

# Definir el alcance (scope) para Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Rutas a los archivos de autenticación
# Se asume que estos archivos están en la raíz del proyecto (BASE_DIR)
TOKEN_FILE = os.path.join(settings.BASE_DIR, 'token.pickle')
CREDENTIALS_FILE = os.path.join(settings.BASE_DIR, 'credentials.json')

def get_google_calendar_service():
    """
    Autentica y retorna el objeto de servicio de Google Calendar.
    
    NOTA: En producción, cada médico debe tener su propia autenticación/token.
    Aquí usamos un token único para el backend.
    """
    creds = None
    
    # 1. Cargar token existente (si lo hay)
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # 2. Refrescar o iniciar el flujo de autenticación
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(None)
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                logger.error(f"Archivo de credenciales no encontrado en: {CREDENTIALS_FILE}")
                print("\n❌ ERROR: EL ARCHIVO 'credentials.json' NO FUE ENCONTRADO EN LA RAÍZ DEL PROYECTO.")
                return None

            try:
                # Usamos flow.run_local_server() para la autenticación en desarrollo (Desktop App flow)
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                print("\n🌐 Por favor, sigue el enlace que aparecerá para autenticar tu cuenta de Google.")
                creds = flow.run_local_server(port=0) 
            except Exception as e:
                logger.error(f"Fallo en el flujo de autenticación: {e}")
                print(f"❌ ERROR de Autenticación: {e}")
                return None
        
        # 3. Guardar las nuevas credenciales
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    # 4. Construir y retornar el servicio
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError as error:
        logger.error(f'Ocurrió un error al construir el servicio de Calendar: {error}')
        return None

def create_calendar_event(horario_cita_instance):
    """
    Crea un evento en Google Calendar y retorna el ID del evento creado.
    Asume que el calendario del médico es su dirección de correo (email) y que existe.
    """
    service = get_google_calendar_service()
    if not service:
        return None
    
    # Asumimos que el email del médico es el ID de su calendario.
    # Debes asegurar que el modelo UsuarioMedico tiene el campo 'email'.
    calendar_id = horario_cita_instance.medico.email 
    
    # Asegurar que las fechas tienen la zona horaria de Django
    tz = timezone(settings.TIME_ZONE)
    start_time_local = horario_cita_instance.start_datetime.astimezone(tz)
    end_time_local = horario_cita_instance.end_datetime.astimezone(tz)

    event = {
        'summary': f'Horario: {horario_cita_instance.especialidad.Espacialidad_Medica} - Dr(a). {horario_cita_instance.medico.Nombres_Medico}',
        'description': f'Turno: {horario_cita_instance.turno.nombre}. Domicilio: {horario_cita_instance.domicilio}',
        'start': {
            'dateTime': start_time_local.isoformat(),
            'timeZone': settings.TIME_ZONE,
        },
        'end': {
            'dateTime': end_time_local.isoformat(),
            'timeZone': settings.TIME_ZONE,
        },
        'recurrence': [horario_cita_instance.recurrence_rule] if horario_cita_instance.recurrence_rule else None,
        'visibility': 'public',
        'transparency': 'opaque', # Bloquea el tiempo
    }

    try:
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        return event['id']
    except HttpError as error:
        # 404 significa que el calendario del médico (el email) no existe o no es accesible.
        if error.resp.status == 404:
             logger.error(f"El calendario ID '{calendar_id}' no fue encontrado o no está compartido.")
        else:
             logger.error(f'Error al crear evento para {horario_cita_instance}: {error}')
        return None

def update_calendar_event(horario_cita_instance):
    """Actualiza un evento existente en Google Calendar."""
    service = get_google_calendar_service()
    if not service:
        return False

    calendar_id = horario_cita_instance.calendar_id 
    event_id = horario_cita_instance.calendar_event_id

    # Reconstruir el cuerpo del evento con la información actualizada
    event = {
        'summary': f'Horario: {horario_cita_instance.especialidad.Espacialidad_Medica} - Dr(a). {horario_cita_instance.medico.Nombres_Medico}',
        'description': f'Turno: {horario_cita_instance.turno.nombre}. Domicilio: {horario_cita_instance.domicilio}',
        'start': {
            'dateTime': horario_cita_instance.start_datetime.isoformat(),
            'timeZone': settings.TIME_ZONE,
        },
        'end': {
            'dateTime': horario_cita_instance.end_datetime.isoformat(),
            'timeZone': settings.TIME_ZONE,
        },
        'recurrence': [horario_cita_instance.recurrence_rule] if horario_cita_instance.recurrence_rule else None,
        'transparency': 'opaque',
    }

    try:
        service.events().update(
            calendarId=calendar_id, 
            eventId=event_id, 
            body=event
        ).execute()
        return True
    except HttpError as error:
        logger.error(f'Error al actualizar evento {event_id}: {error}')
        return False


def delete_calendar_event(calendar_id, event_id):
    """Elimina un evento de Google Calendar."""
    service = get_google_calendar_service()
    if not service:
        return False
    
    try:
        service.events().delete(
            calendarId=calendar_id, 
            eventId=event_id
        ).execute()
        return True
    except HttpError as error:
        logger.error(f'Error al eliminar evento {event_id}: {error}')
        return False
# citas/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import HorarioCita
# Importamos el servicio desde la raíz del proyecto
from google_calendar_service import ( 
    create_calendar_event, 
    update_calendar_event, 
    delete_calendar_event
) 
import logging

logger = logging.getLogger(__name__)


# -----------------------------------------------------------
# POST_SAVE (Creación y Actualización)
# -----------------------------------------------------------

@receiver(post_save, sender=HorarioCita)
def sync_horario_to_google_calendar(sender, instance, created, **kwargs):
    """Maneja la creación y actualización de eventos en Google Calendar."""
    
    # 1. Lógica de CREACIÓN (Solo si se acaba de crear y no tiene ID de evento)
    if created and not instance.calendar_event_id:
        logger.info(f"Signal: Intento de CREACIÓN de evento para HorarioCita ID: {instance.pk}")
        
        event_id = create_calendar_event(instance)
        
        if event_id:
            # 1.1 Guardar el ID de vuelta en el modelo Django (evitando bucle infinito)
            post_save.disconnect(sync_horario_to_google_calendar, sender=HorarioCita)
            instance.calendar_event_id = event_id
            # El calendar_id es típicamente el email del médico, lo guardamos si lo retorna el servicio
            instance.calendar_id = instance.medico.email # Asumimos el email como calendar_id
            instance.save(update_fields=['calendar_event_id', 'calendar_id'])
            post_save.connect(sync_horario_to_google_calendar, sender=HorarioCita)
            logger.info(f"Signal: Evento CREADO exitosamente. GC ID: {event_id}")
            
    # 2. Lógica de ACTUALIZACIÓN (Si ya existe y tiene ID de evento)
    elif not created and instance.calendar_event_id:
        logger.info(f"Signal: Intento de ACTUALIZACIÓN de evento para HorarioCita ID: {instance.pk}")
        
        # Llama a la función de actualización (que implementaremos a continuación)
        is_updated = update_calendar_event(instance)
        
        if is_updated:
            logger.info(f"Signal: Evento GC ID {instance.calendar_event_id} ACTUALIZADO.")
        else:
            logger.warning(f"Signal: Fallo en la actualización de evento GC ID {instance.calendar_event_id}.")


# -----------------------------------------------------------
# POST_DELETE (Eliminación)
# -----------------------------------------------------------

@receiver(post_delete, sender=HorarioCita)
def delete_horario_from_google_calendar(sender, instance, **kwargs):
    """Maneja la eliminación de eventos en Google Calendar."""
    
    if instance.calendar_id and instance.calendar_event_id:
        logger.info(f"Signal: Intento de ELIMINACIÓN de evento GC ID: {instance.calendar_event_id}")
        
        # Llama a la función de eliminación (que implementaremos a continuación)
        is_deleted = delete_calendar_event(instance.calendar_id, instance.calendar_event_id)
        
        if is_deleted:
            logger.info(f"Signal: Evento GC ID {instance.calendar_event_id} ELIMINADO.")
        else:
            logger.warning(f"Signal: Fallo en la eliminación de evento GC ID {instance.calendar_event_id}.")
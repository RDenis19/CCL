from django.db.models.signals import post_save
from django.dispatch import receiver

from communications.models import Notificacion
from .models import SolicitudServicio


@receiver(post_save, sender=SolicitudServicio)
def crear_notificacion_estado_solicitud_servicio(sender, instance, created, **kwargs):
    """
    Crea una notificación cuando se actualiza el estado de una solicitud de servicio.
    """
    # Solo actuar cuando se actualiza, no al crearse, y si el campo 'estado' cambió
    if not created and 'estado' in (kwargs.get('update_fields') or []):
        solicitud = instance
        verbo = f"Tu solicitud para '{solicitud.recurso.nombre}' ha sido {solicitud.get_estado_display().lower()}."

        Notificacion.objects.create(
            destinatario=solicitud.solicitante,
            actor=solicitud.gestor,  # El empleado que hizo el cambio
            verbo=verbo,
            objetivo=solicitud,
            tipo=Notificacion.Tipo.SERVICIOS
        )

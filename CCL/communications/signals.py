from django.db.models.signals import post_save
from django.dispatch import receiver

from communications.models import Notificacion
from memberships.models import SolicitudAfiliacion


@receiver(post_save, sender=SolicitudAfiliacion)
def crear_notificacion_estado_solicitud(sender, instance, created, **kwargs):
    """
    Crea una notificación cuando se actualiza el estado de una solicitud.
    """
    # Solo actuar en actualizaciones, no en la creación inicial.
    if not created and 'estado' in (kwargs.get('update_fields') or []):
        solicitud = instance
        verbo = f"ha sido actualizada al estado: {solicitud.get_estado_display()}"

        Notificacion.objects.create(
            destinatario=solicitud.solicitante,
            # El actor podría ser el admin que hizo el cambio, pero lo omitimos por simplicidad.
            actor=None,
            verbo=verbo,
            objetivo=solicitud  # Esto asigna content_type y object_id automáticamente.
        )

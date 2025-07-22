from django.db.models.signals import post_save
from django.dispatch import receiver

from communications.models import Notificacion
from memberships.models import SolicitudAfiliacion
from staff_panel.models import ConfiguracionNotificacion


@receiver(post_save, sender=SolicitudAfiliacion)
def crear_notificacion_estado_solicitud(sender, instance, created, **kwargs):
    if not created:
        try:
            # Buscamos la configuración para este evento
            config = ConfiguracionNotificacion.objects.get(
                codigo_evento="SOLICITUD_ESTADO_ACTUALIZADO",
                esta_activa=True
            )

            solicitud = instance
            # Usamos la plantilla del mensaje desde la base de datos
            verbo = config.mensaje_plantilla.format(
                estado=solicitud.get_estado_display().lower()
            )

            Notificacion.objects.create(
                destinatario=solicitud.solicitante,
                verbo=verbo,
                objetivo=solicitud,
                tipo=Notificacion.Tipo.AFILIACION
            )
        except ConfiguracionNotificacion.DoesNotExist:
            # Si la configuración no existe o está inactiva, no se envía nada.
            pass

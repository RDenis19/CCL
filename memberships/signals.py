from django.db.models.signals import post_save
from django.dispatch import receiver

from communications.models import Notificacion
from memberships.models import SolicitudAfiliacion
from staff_panel.models import ConfiguracionNotificacion


# Esto significa que esta función se ejecutará CADA VEZ que una solicitud se guarde en la BD.
@receiver(post_save, sender=SolicitudAfiliacion)
def crear_notificacion_estado_solicitud(sender, instance, created, **kwargs):
    """
    Crea una notificación para el usuario cuando el estado de su
    solicitud de afiliación es actualizado por el personal.
    """
    
    # Solo quiero enviar una notificación cuando se ACTUALIZA una solicitud,
    # no cuando se crea por primera vez. 'created' es False en las actualizaciones.
    if not created:
        try:
            # Busco en la BD si hay una configuración activa para este tipo de notificación.
            # Esto me permite prender o apagar este tipo de avisos desde el panel de admin.
            config = ConfiguracionNotificacion.objects.get(
                codigo_evento="SOLICITUD_ESTADO_ACTUALIZADO",
                esta_activa=True
            )

            solicitud = instance
            # Si encuentro la configuración, uso la plantilla de mensaje que guardé en la base de datos
            # y le inserto el estado actual de la solicitud (ej: 'aprobada', 'rechazada').
            verbo = config.mensaje_plantilla.format(
                estado=solicitud.get_estado_display().lower()
            )

            # Finalmente, creo el objeto de notificación en la base de datos.
            # Este objeto será visible para el usuario en su panel de notificaciones.
            Notificacion.objects.create(
                destinatario=solicitud.solicitante,
                verbo=verbo,
                objetivo=solicitud,
                tipo=Notificacion.Tipo.AFILIACION
            )
        except ConfiguracionNotificacion.DoesNotExist:
            # Si no encuentro una configuración (o no está activa), no hago nada.
            # La notificación simplemente no se crea, y todo sigue funcionando sin errores.
            pass
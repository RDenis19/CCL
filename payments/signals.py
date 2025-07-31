from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from communications.models import Notificacion
from services.models import HorarioDisponible
from services.models import SolicitudServicio
from .models import Pago


@receiver(post_save, sender=Pago)
def confirmar_reserva_tras_verificacion(sender, instance, created, **kwargs):
    """
    Cuando un pago es marcado como VERIFICADO, esta señal se encarga de:
    1. Cambiar el estado de la SolicitudServicio a CONFIRMADA.
    2. Marcar el HorarioDisponible como reservado.
    3. Enviar una notificación al usuario.
    """
    pago = instance
    # Actuar solo cuando un pago existente es actualizado a VERIFICADO
    if not created and pago.estado == Pago.EstadoPago.VERIFICADO and 'estado' in (kwargs.get('update_fields') or []):
        solicitud = pago.solicitud_servicio

        if solicitud.estado == SolicitudServicio.Estado.PENDIENTE_VERIFICACION:
            # 1. Confirmar la solicitud
            solicitud.estado = SolicitudServicio.Estado.CONFIRMADA
            solicitud.gestor = pago.gestor  # Asigna el mismo gestor que verificó el pago
            solicitud.save(update_fields=['estado', 'gestor'])

            # 2. Reservar el horario disponible, si aplica
            try:
                horario = HorarioDisponible.objects.get(
                    recurso=solicitud.recurso,
                    fecha_hora_inicio=solicitud.fecha_hora_inicio,
                    esta_reservado=False
                )
                horario.esta_reservado = True
                horario.save(update_fields=['esta_reservado'])
            except HorarioDisponible.DoesNotExist:
                pass  # La solicitud no estaba ligada a un horario específico.

            # 3. Enviar notificación al usuario (opcional pero recomendado)
            verbo = _("Tu pago para la solicitud de '{recurso}' ha sido confirmado.").format(
                recurso=solicitud.recurso.nombre
            )
            Notificacion.objects.create(
                destinatario=solicitud.solicitante,
                actor=pago.gestor,
                verbo=verbo,
                objetivo=solicitud,
                tipo=Notificacion.Tipo.SERVICIOS
            )

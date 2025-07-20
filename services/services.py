# Archivo: services/services.py

from django.db import transaction
from .models import SolicitudServicio, HorarioDisponible


@transaction.atomic
def procesar_solicitud(solicitud, gestor, nuevo_estado, respuesta_gestor=""):
    """
    Procesa una solicitud de servicio, actualizando su estado y el del horario si aplica.
    """
    if nuevo_estado not in [SolicitudServicio.Estado.CONFIRMADA, SolicitudServicio.Estado.RECHAZADA]:
        raise ValueError("El nuevo estado no es válido.")

    solicitud.estado = nuevo_estado
    solicitud.gestor = gestor
    solicitud.respuesta_gestor = respuesta_gestor
    solicitud.save()

    # Si se rechaza una reserva, el horario vuelve a estar disponible.
    if nuevo_estado == SolicitudServicio.Estado.RECHAZADA and solicitud.horario:
        horario = solicitud.horario
        horario.esta_reservado = False
        horario.save()

    # Aquí se podría disparar una señal para notificar al usuario.

    return solicitud

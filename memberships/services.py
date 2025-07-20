from django.db import transaction
from django.utils import timezone

from users.models import Membresia
from .models import SolicitudAfiliacion


@transaction.atomic
def crear_solicitud_completa(solicitante, form_detalle, formset_beneficiarios=None):
    """
    Crea una solicitud de afiliación completa dentro de una transacción.

    Args:
        solicitante (User): El usuario que realiza la solicitud.
        form_detalle (ModelForm): El formulario con los detalles (natural o jurídico).
        formset_beneficiarios (FormSet, optional): El formset con los beneficiarios.

    Returns:
        SolicitudAfiliacion: La instancia de la solicitud creada.
    """
    # 1. Crear la solicitud principal.
    solicitud = SolicitudAfiliacion.objects.create(solicitante=solicitante)

    # 2. Guardar el detalle (sin commit) para obtener una instancia.
    detalle = form_detalle.save(commit=False)
    detalle.solicitud = solicitud
    detalle.save()

    # 3. Si hay un formset de beneficiarios, guardarlo.
    if formset_beneficiarios:
        formset_beneficiarios.instance = detalle
        formset_beneficiarios.save()

    return solicitud


@transaction.atomic
def aprobar_solicitud(solicitud, admin_user):
    """
    Aprueba una solicitud de afiliación, crea la membresía y actualiza el estado.
    """
    if solicitud.estado == SolicitudAfiliacion.Estado.APROBADA:
        raise ValueError("Esta solicitud ya ha sido aprobada.")

    # 1. Crear la membresía para el usuario
    # Usamos update_or_create por si ya existiera una membresía por alguna razón.
    Membresia.objects.update_or_create(
        usuario=solicitud.solicitante,
        defaults={
            'solicitud_origen': solicitud,
            'aprobado_por': admin_user,
            'numero_socio': f"SOCIO-{solicitud.solicitante.id}",  # Lógica simple para el número de socio
            'estado': Membresia.Estado.ACTIVA,
            'fecha_ingreso': timezone.now().date()
        }
    )

    # 2. Actualizar el estado de la solicitud
    solicitud.estado = SolicitudAfiliacion.Estado.APROBADA
    solicitud.save()

    # Aquí se podría disparar una señal para enviar un correo de bienvenida.

    return solicitud


@transaction.atomic
def rechazar_solicitud(solicitud):
    """
    Rechaza una solicitud de afiliación.
    """
    solicitud.estado = SolicitudAfiliacion.Estado.RECHAZADA
    solicitud.save()

    # Aquí se podría disparar una señal para notificar al usuario del rechazo.

    return solicitud

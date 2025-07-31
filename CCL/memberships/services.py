from django.db import transaction
from django.utils import timezone

from users.models import Membresia
from .models import SolicitudAfiliacion


@transaction.atomic
def crear_solicitud_completa(solicitante, form_detalle, formset_beneficiarios=None, formset_documentos=None):
    """
    Crea una solicitud de afiliación completa, incluyendo detalles y documentos.
    """
    # 1. Crear la solicitud principal.
    solicitud = SolicitudAfiliacion.objects.create(solicitante=solicitante)

    # 2. Guardar el detalle.
    detalle = form_detalle.save(commit=False)
    detalle.solicitud = solicitud
    detalle.save()

    # 3. Si hay un formset de beneficiarios, guardarlo.
    if formset_beneficiarios:
        formset_beneficiarios.instance = detalle
        formset_beneficiarios.save()

    # --- LÓGICA AÑADIDA PARA GUARDAR DOCUMENTOS ---
    if formset_documentos:
        # Vinculamos los documentos con la solicitud principal
        documentos = formset_documentos.save(commit=False)
        for documento in documentos:
            documento.solicitud = solicitud
            documento.save()
        # Guardar eliminaciones si las hubiera
        formset_documentos.save_m2m()

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

# Archivo: payments/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from services.models import SolicitudServicio
from .forms import ComprobantePagoForm
from .models import Pago


@login_required
def upload_comprobante_view(request, solicitud_id):
    """
    Gestiona la subida de un comprobante de pago para una solicitud de servicio.
    """
    solicitud = get_object_or_404(
        SolicitudServicio,
        id=solicitud_id,
        solicitante=request.user
    )

    # Prevenir que se suba un comprobante si el proceso ya avanzó
    if hasattr(solicitud, 'pago'):
        messages.warning(request, _("Ya existe un pago registrado para esta solicitud."))
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = ComprobantePagoForm(request.POST, request.FILES)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.solicitud_servicio = solicitud
            pago.monto = solicitud.recurso.servicio.precio
            pago.estado = Pago.EstadoPago.PENDIENTE
            pago.save()

            solicitud.estado = SolicitudServicio.Estado.PENDIENTE_VERIFICACION
            solicitud.save(update_fields=['estado'])

            messages.success(request, _("Comprobante subido. Tu solicitud será verificada por nuestro equipo."))
            return redirect('users:dashboard')
    else:
        form = ComprobantePagoForm()

    context = {
        'form': form,
        'solicitud': solicitud,
        'page_title': _("Subir Comprobante de Pago")
    }
    return render(request, 'payments/upload_comprobante.html', context)  # Debes crear esta plantilla

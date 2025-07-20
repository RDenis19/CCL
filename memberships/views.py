from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .forms import (
    DetalleSolicitudNaturalForm,
    DetalleSolicitudJuridicaForm,
    BeneficiarioPolizaFormSet
)
from .services import crear_solicitud_completa
from .models import SolicitudAfiliacion


@login_required
def solicitud_create_view(request, tipo_solicitante):
    """
    Gestiona la creación de una nueva solicitud de afiliación.
    El 'tipo_solicitante' viene de la URL ('natural' o 'juridica').
    """
    FormDetalle = DetalleSolicitudNaturalForm if tipo_solicitante == 'natural' else DetalleSolicitudJuridicaForm
    template_name = 'memberships/solicitud_form.html'

    if request.method == 'POST':
        form_detalle = FormDetalle(request.POST)
        formset_beneficiarios = None
        if tipo_solicitante == 'natural':
            formset_beneficiarios = BeneficiarioPolizaFormSet(request.POST)

        # Validar ambos formularios
        is_form_valid = form_detalle.is_valid()
        is_formset_valid = formset_beneficiarios.is_valid() if formset_beneficiarios else True

        if is_form_valid and is_formset_valid:
            try:
                crear_solicitud_completa(request.user, form_detalle, formset_beneficiarios)
                messages.success(request, _("¡Tu solicitud ha sido enviada con éxito!"))
                return redirect('memberships:solicitud-detail')
            except Exception as e:
                # En un caso real, aquí se registraría el error 'e'.
                messages.error(request, _("Ocurrió un error al procesar tu solicitud."))
        else:
            messages.error(request, _("Por favor, corrige los errores en el formulario."))

    else:
        form_detalle = FormDetalle()
        formset_beneficiarios = BeneficiarioPolizaFormSet() if tipo_solicitante == 'natural' else None

    context = {
        'form_detalle': form_detalle,
        'formset_beneficiarios': formset_beneficiarios,
        'page_title': _("Solicitud de Afiliación - Persona ") + _(tipo_solicitante.capitalize())
    }
    return render(request, template_name, context)


@login_required
def solicitud_detail_view(request):
    """
    Muestra los detalles de la última solicitud de afiliación del usuario.
    """
    try:
        # Usamos select_related para optimizar la consulta a la base de datos.
        solicitud = SolicitudAfiliacion.objects.select_related(
            'detallesolicitudnatural', 'detallesolicitudjuridica'
        ).filter(solicitante=request.user).latest('fecha_creacion')
    except SolicitudAfiliacion.DoesNotExist:
        solicitud = None

    context = {
        'solicitud': solicitud,
        'page_title': _("Detalle de mi Solicitud")
    }
    return render(request, 'memberships/solicitud_detail.html', context)


@login_required
def solicitud_selector_view(request):
    """
    Muestra una página para que el usuario elija qué tipo de
    solicitud de afiliación desea iniciar.
    """
    # Si el usuario ya tiene una solicitud o membresía, lo redirigimos a su panel.
    if hasattr(request.user, 'membresia') or request.user.solicitudes_afiliacion.exists():
        messages.info(request, _("Ya tienes una membresía o una solicitud en proceso."))
        return redirect('users:dashboard')

    context = {
        'page_title': _("Iniciar Proceso de Afiliación")
    }
    return render(request, 'memberships/solicitud_selector.html', context)

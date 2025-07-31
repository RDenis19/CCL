from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from .forms import (
    DetalleSolicitudNaturalForm,
    DetalleSolicitudJuridicaForm,
    BeneficiarioPolizaFormSet, DocumentoAdjuntoFormSet
)
from .models import SolicitudAfiliacion
from .services import crear_solicitud_completa

# se asegura de que solo usuarios autenticados puedan entrar a esta vista.
@login_required
def solicitud_create_view(request, tipo_solicitante):
    """
    Gestiona la creación de una nueva solicitud de afiliación (tanto para persona
    natural como jurídica), incluyendo los formularios para detalles, beneficiarios
    y la subida de documentos adjuntos.
    """
    # Elijo el formulario de detalles correcto dependiendo del tipo de socio.
    FormDetalle = DetalleSolicitudNaturalForm if tipo_solicitante == 'natural' else DetalleSolicitudJuridicaForm
    template_name = 'memberships/solicitud_form.html'

    # --- Lógica para cuando el usuario envía el formulario (POST) ---
    if request.method == 'POST':
        # Instancio los formularios con los datos que mandó el usuario.
        form_detalle = FormDetalle(request.POST)
        formset_documentos = DocumentoAdjuntoFormSet(request.POST, request.FILES)

        # El formset de beneficiarios solo aplica para personas naturales.
        formset_beneficiarios = None
        if tipo_solicitante == 'natural':
            formset_beneficiarios = BeneficiarioPolizaFormSet(request.POST)

        # Valido todos los formularios antes de hacer nada.
        is_form_valid = form_detalle.is_valid()
        is_formset_docs_valid = formset_documentos.is_valid()
        # Si no hay formset de beneficiarios, considero que es válido.
        is_formset_valid = formset_beneficiarios.is_valid() if formset_beneficiarios else True

        # Si todas las validaciones pasan, procedo a guardar los datos.
        if is_form_valid and is_formset_valid and is_formset_docs_valid:
            try:
                # Llamo a mi función de servicio que se encarga de toda la lógica de creación.
                crear_solicitud_completa(
                    request.user, form_detalle, formset_beneficiarios, formset_documentos
                )
                # Si todo sale bien, muestro un mensaje de éxito y redirijo al usuario.
                messages.success(request, _("¡Tu solicitud ha sido enviada con éxito!"))
                return redirect('memberships:solicitud-detail')
            except Exception as e:
                # Si ocurre un error inesperado durante el proceso, lo capturo y aviso al usuario.
                messages.error(request, _("Ocurrió un error al procesar tu solicitud."))
        else:
            # Si los formularios no son válidos, Django automáticamente mostrará los errores.
            messages.error(request, _("Por favor, corrige los errores en el formulario."))

    # --- Lógica para cuando el usuario carga la página por primera vez (GET) ---
    else:
        # Muestro los formularios vacíos.
        form_detalle = FormDetalle()
        formset_documentos = DocumentoAdjuntoFormSet()
        formset_beneficiarios = BeneficiarioPolizaFormSet() if tipo_solicitante == 'natural' else None

    # Preparo el contexto con todos los formularios y datos para la plantilla.
    context = {
        'form_detalle': form_detalle,
        'formset_beneficiarios': formset_beneficiarios,
        'formset_documentos': formset_documentos,
        'page_title': _("Solicitud de Afiliación - Persona ") + _(tipo_solicitante.capitalize())
    }
    return render(request, template_name, context)


@login_required
def solicitud_detail_view(request):
    """
    Muestra los detalles de la última solicitud de afiliación del usuario.
    """
    try:
        # Busco la última solicitud del usuario. Uso select_related para traer los detalles
        # de persona natural o jurídica en la misma consulta y ser más eficiente (evito más queries).
        solicitud = SolicitudAfiliacion.objects.select_related(
            'detallesolicitudnatural', 'detallesolicitudjuridica'
        ).filter(solicitante=request.user).latest('fecha_creacion')
    except SolicitudAfiliacion.DoesNotExist:
        # Si el usuario no tiene ninguna solicitud, la variable será None.
        solicitud = None

    context = {
        'solicitud': solicitud,
        'page_title': _("Detalle de mi Solicitud")
    }
    return render(request, 'memberships/solicitud_detail.html', context)


@login_required
def solicitud_selector_view(request):
    """
    Esta vista funciona como un "filtro" o "portero".
    Revisa varias condiciones antes de permitirle al usuario crear una nueva solicitud.
    """
    # 1. El personal de la organización no puede ser socio.
    if request.user.is_staff:
        messages.error(request, _("El personal de la organización no puede iniciar una solicitud de afiliación."))
        return redirect('staff_panel:dashboard')

    # 2. Reviso si el usuario ya tiene una membresía activa.
    if hasattr(request.user, 'membresia'):
        messages.info(request, _("Ya tienes una membresía activa."))
        return redirect('users:dashboard')

    # 3. Compruebo si ya tiene una solicitud en estado "Pendiente" o "En Revisión".
    estados_en_proceso = [
        SolicitudAfiliacion.Estado.PENDIENTE,
        SolicitudAfiliacion.Estado.EN_REVISION
    ]
    if request.user.solicitudes_afiliacion.filter(estado__in=estados_en_proceso).exists():
        messages.warning(request, _("Ya tienes una solicitud en proceso. Por favor, espera a que sea revisada."))
        return redirect('users:dashboard')

    # 4. Si pasa todas las validaciones, le muestro la página para que elija qué tipo de socio quiere ser.
    context = {
        'page_title': _("Iniciar Proceso de Afiliación")
    }
    return render(request, 'memberships/solicitud_selector.html', context)
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from memberships.models import SolicitudAfiliacion
from services.models import SolicitudServicio
from .forms import PerfilUsuarioUpdateForm, UserRegistrationForm


# Con @login_required solo usuarios autenticados vean esta página.
@login_required
def perfil_detail_view(request):
    """
    Muestra la página de perfil del usuario autenticado.
    Recupera y muestra la información del PerfilUsuario y, si existe,
    de la Membresía asociada.
    """
    # Accedo al perfil directamente desde el usuario, gracias a la relación OneToOne.
    perfil = request.user.perfil
    membresia = None

    # Reviso si el usuario tiene una membresía para no causar un error si no la tiene.
    if hasattr(request.user, 'membresia'):
        membresia = request.user.membresia

    context = {
        'perfil': perfil,
        'membresia': membresia,
        'page_title': _("Mi Perfil")
    }
    return render(request, 'users/perfil_detail.html', context)


@login_required
def perfil_update_view(request):
    """
    Gestiona la edición del perfil del usuario.
    Maneja la solicitud GET para mostrar el formulario con los datos
    actuales y la solicitud POST para procesar y guardar los cambios.
    """
    perfil_instance = request.user.perfil

    # Si la petición es POST, el usuario está enviando el formulario para guardar.
    if request.method == 'POST':
        # Paso la 'instance' para que el formulario sepa que está editando un perfil existente.
        # Es clave pasar request.FILES para que se procese la subida de la foto de perfil.
        form = PerfilUsuarioUpdateForm(
            request.POST, request.FILES, instance=perfil_instance
        )
        if form.is_valid():
            form.save()
            messages.success(request, _("¡Tu perfil ha sido actualizado con éxito!"))
            return redirect('users:perfil-detail')
        else:
            messages.error(request, _("Por favor, corrige los errores en el formulario."))
    else:
        # Si la petición es GET, solo muestro el formulario con los datos actuales del perfil.
        form = PerfilUsuarioUpdateForm(instance=perfil_instance)

    context = {
        'form': form,
        'page_title': _("Editar Perfil")
    }
    return render(request, 'users/perfil_form.html', context)


def registro_view(request):
    """
    Gestiona el registro de un nuevo usuario en el sistema.
    Esta vista es pública.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # form.save() crea el nuevo usuario en la base de datos y me lo devuelve.
            new_user = form.save()
            # Una vez registrado, inicio la sesión del usuario automáticamente para una mejor experiencia.
            login(request, new_user)
            messages.success(request, _("¡Registro exitoso! Bienvenido."))
            return redirect('users:dashboard')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
        'page_title': _("Crear una Cuenta")
    }
    return render(request, 'users/registro.html', context)


@login_required
def dashboard_view(request):
    """
    Muestra el panel principal del usuario con un resumen de su actividad.
    """
    # Traigo las últimas 3 notificaciones sin leer para mostrarlas como un resumen.
    notificaciones_no_leidas = request.user.notificaciones.filter(leida=False)[:3]

    # Busco las próximas 3 reservas que ya están confirmadas y que aún no han pasado.
    proximas_reservas = SolicitudServicio.objects.filter(
        solicitante=request.user,
        estado=SolicitudServicio.Estado.CONFIRMADA,
        fecha_hora_inicio__gte=timezone.now() # __gte significa "mayor o igual que".
    ).order_by('fecha_hora_inicio')[:3]

    # Si el usuario todavía no es miembro, busco si tiene una solicitud en proceso para recordárselo.
    solicitud_pendiente = None
    if not hasattr(request.user, 'membresia'):
        solicitud_pendiente = SolicitudAfiliacion.objects.filter(
            solicitante=request.user
        ).order_by('-fecha_creacion').first()

    context = {
        'page_title': "Mi Panel",
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'proximas_reservas': proximas_reservas,
        'solicitud_pendiente': solicitud_pendiente,
    }
    return render(request, 'users/dashboard.html', context)
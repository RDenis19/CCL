from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from memberships.models import SolicitudAfiliacion
from services.models import SolicitudServicio
from .forms import PerfilUsuarioUpdateForm, UserRegistrationForm
from .models import Membresia


@login_required
def perfil_detail_view(request):
    """
    Muestra la página de perfil del usuario autenticado.

    Recupera y muestra la información del PerfilUsuario y, si existe,
    de la Membresía asociada.
    """
    # El perfil se obtiene directamente desde la relación inversa del usuario.
    perfil = request.user.perfil
    membresia = None

    # Verificamos si el usuario tiene una membresía asociada.
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

    if request.method == 'POST':
        # Pasamos la instancia para que el formulario sepa que está editando.
        # request.FILES es necesario para manejar la subida de la imagen del avatar.
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
        # En una solicitud GET, mostramos el formulario con los datos existentes.
        form = PerfilUsuarioUpdateForm(instance=perfil_instance)

    context = {
        'form': form,
        'page_title': _("Editar Perfil")
    }
    return render(request, 'users/perfil_form.html', context)


def registro_view(request):
    """
    Gestiona el registro de un nuevo usuario en el sistema.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # Inicia sesión automáticamente al nuevo usuario
            login(request, new_user)
            messages.success(request, _("¡Registro exitoso! Bienvenido."))
            return redirect('users:perfil-detail')
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
    notificaciones_no_leidas = request.user.notificaciones.filter(leida=False)[:3]

    proximas_reservas = SolicitudServicio.objects.filter(
        solicitante=request.user,
        estado=SolicitudServicio.Estado.CONFIRMADA,
        horario__fecha_hora_inicio__gte=timezone.now()
    ).order_by('horario__fecha_hora_inicio')[:3]

    # --- LÓGICA AÑADIDA ---
    solicitud_pendiente = None
    if not hasattr(request.user, 'membresia'):
        solicitud_pendiente = SolicitudAfiliacion.objects.filter(
            solicitante=request.user
        ).order_by('-fecha_creacion').first()

    context = {
        'page_title': "Mi Panel",
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'proximas_reservas': proximas_reservas,
        'solicitud_pendiente': solicitud_pendiente,  # Pasamos la solicitud al contexto
    }
    return render(request, 'users/dashboard.html', context)

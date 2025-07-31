# Archivo: communications/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Notificacion


@login_required
def notificacion_list_view(request):
    """
    Muestra la lista de notificaciones del usuario autenticado.
    """
    notificaciones = request.user.notificaciones.all()

    context = {
        'notificaciones': notificaciones,
        'page_title': "Mis Notificaciones"
    }
    return render(request, 'communications/notificacion_list.html', context)


@login_required
def marcar_como_leida_view(request, pk):
    """
    Marca una notificación específica como leída y redirige al usuario.
    """
    notificacion = get_object_or_404(Notificacion, pk=pk, destinatario=request.user)

    if not notificacion.leida:
        notificacion.leida = True
        notificacion.save()

    # Si la notificación tiene un objeto objetivo con URL, redirige allí.
    if hasattr(notificacion.objetivo, 'get_absolute_url'):
        return redirect(notificacion.objetivo.get_absolute_url())

    # Si no, redirige a la lista de notificaciones.
    return redirect('communications:notificacion-list')


@login_required
def marcar_todas_como_leidas_view(request):
    """
    Marca todas las notificaciones no leídas del usuario como leídas.
    """
    request.user.notificaciones.filter(leida=False).update(leida=True)
    return redirect('communications:notificacion-list')

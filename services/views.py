# Archivo: services/views.py

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Servicio, RecursoServicio, HorarioDisponible, Convenio, SolicitudServicio
from .forms import SolicitudServicioForm, HorarioDisponibleForm


def servicio_list_view(request):
    """Muestra una lista de todos los servicios activos."""
    servicios = Servicio.objects.filter(activo=True).prefetch_related('recursos')
    context = {
        'servicios': servicios,
        'page_title': _("Catálogo de Servicios")
    }
    return render(request, 'services/servicio_list.html', context)


def servicio_detail_view(request, pk):
    """Muestra los detalles de un servicio y sus recursos disponibles."""
    servicio = get_object_or_404(Servicio, pk=pk, activo=True)
    recursos = servicio.recursos.all()
    context = {
        'servicio': servicio,
        'recursos': recursos,
        'page_title': servicio.nombre
    }
    return render(request, 'services/servicio_detail.html', context)


@login_required
def solicitud_create_view(request, recurso_pk, horario_pk=None):
    """Crea una solicitud para un recurso específico y un horario opcional."""
    recurso = get_object_or_404(RecursoServicio, pk=recurso_pk)
    horario = None
    if horario_pk:
        horario = get_object_or_404(HorarioDisponible, pk=horario_pk, recurso=recurso, esta_reservado=False)

    if request.method == 'POST':
        form = SolicitudServicioForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.solicitante = request.user
            solicitud.recurso = recurso
            if horario:
                # Marcar el horario como reservado y asignarlo
                horario.esta_reservado = True
                horario.save()
                solicitud.horario = horario

            solicitud.save()
            messages.success(request, _("Tu solicitud ha sido enviada con éxito."))
            return redirect('users:perfil-detail')  # Redirigir al perfil del usuario, por ejemplo
    else:
        form = SolicitudServicioForm()

    context = {
        'form': form,
        'recurso': recurso,
        'horario': horario,
        'page_title': f"Solicitar {recurso.nombre}"
    }
    return render(request, 'services/solicitud_form.html', context)


def convenio_list_view(request):
    """
    Muestra una lista de todos los convenios disponibles.
    """
    convenios = Convenio.objects.all().order_by('nombre_entidad')
    context = {
        'convenios': convenios,
        'page_title': _("Convenios y Beneficios")
    }
    return render(request, 'services/convenio_list.html', context)


def convenio_detail_view(request, pk):
    """
    Muestra los detalles y beneficios de un convenio específico.

    Usamos prefetch_related para optimizar la consulta y traer todos los
    beneficios y sus detalles en menos consultas a la base de datos.
    """
    convenio = get_object_or_404(
        Convenio.objects.prefetch_related('beneficios__detalles'),
        pk=pk
    )
    context = {
        'convenio': convenio,
        'page_title': f"Beneficios de {convenio.nombre_entidad}"
    }
    return render(request, 'services/convenio_detail.html', context)


@login_required
def mis_solicitudes_view(request):
    """
    Muestra una lista completa de todas las solicitudes de servicio
    realizadas por el usuario autenticado.
    """
    solicitudes = SolicitudServicio.objects.filter(
        solicitante=request.user
    ).select_related('recurso', 'recurso__servicio').order_by('-fecha_creacion')

    context = {
        'solicitudes': solicitudes,
        'page_title': "Mis Solicitudes de Servicio"
    }
    return render(request, 'services/mis_solicitudes.html', context)


def recurso_detail_view(request, pk):
    """
    Muestra la página de detalle de un recurso, incluyendo el calendario
    y un formulario para añadir nuevos horarios (si el usuario es staff).
    """
    recurso = get_object_or_404(RecursoServicio, pk=pk)
    form = HorarioDisponibleForm()

    if request.method == 'POST' and request.user.is_staff:
        form = HorarioDisponibleForm(request.POST)
        if form.is_valid():
            nuevo_horario = form.save(commit=False)
            nuevo_horario.recurso = recurso
            nuevo_horario.save()
            messages.success(request, "Nuevo horario de disponibilidad creado con éxito.")
            return redirect('services:recurso-detail', pk=recurso.pk)
        else:
            messages.error(request, "Hubo un error en el formulario. Revisa los datos.")

    context = {
        'recurso': recurso,
        'form_horario': form,  # Pasamos el formulario al contexto
        'page_title': f"Gestionar Horarios de {recurso.nombre}"
    }
    return render(request, 'services/recurso_detail.html', context)


def recurso_eventos_json(request, pk):
    """
    Devuelve los horarios de un recurso en formato JSON para FullCalendar.
    """
    recurso = get_object_or_404(RecursoServicio, pk=pk)
    # Filtramos solo horarios futuros
    horarios = recurso.horarios.filter(fecha_hora_inicio__gte=timezone.now())

    eventos = []
    for horario in horarios:
        eventos.append({
            'title': "Reservado" if horario.esta_reservado else "Disponible",
            'start': horario.fecha_hora_inicio.isoformat(),
            'end': horario.fecha_hora_fin.isoformat(),
            'url': reverse('services:reserva-create', kwargs={'recurso_pk': recurso.pk,
                                                              'horario_pk': horario.pk}) if not horario.esta_reservado else '',
            'color': '#dc3545' if horario.esta_reservado else '#198754'  # Rojo si está reservado, Verde si no
        })

    return JsonResponse(eventos, safe=False)

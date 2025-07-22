from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from content.models import Noticia
from memberships.models import SolicitudAfiliacion
from memberships.services import aprobar_solicitud, rechazar_solicitud
from services.forms import RespuestaSolicitudForm
from services.models import SolicitudServicio, Servicio, RecursoServicio
from services.services import procesar_solicitud
from staff_panel.forms import NoticiaForm, RecursoServicioForm, ServicioForm


@staff_member_required
def dashboard_staff_view(request):
    """
    Muestra el panel de control principal para el personal (staff).
    """
    pendientes_afiliacion = SolicitudAfiliacion.objects.filter(
        estado=SolicitudAfiliacion.Estado.PENDIENTE
    ).count()

    pendientes_servicios = SolicitudServicio.objects.filter(
        estado=SolicitudServicio.Estado.PENDIENTE
    ).count()

    context = {
        'page_title': "Panel de Gestión",
        'pendientes_afiliacion': pendientes_afiliacion,
        'pendientes_servicios': pendientes_servicios,
    }
    return render(request, 'staff_panel/dashboard.html', context)


@staff_member_required
def solicitud_afiliacion_list_view(request):
    """
    Muestra una lista de todas las solicitudes de afiliación para ser gestionadas.
    """
    solicitudes = SolicitudAfiliacion.objects.select_related('solicitante').order_by('fecha_creacion')

    # Filtro básico por estado
    estado_filtro = request.GET.get('estado')
    if estado_filtro and estado_filtro in SolicitudAfiliacion.Estado.values:
        solicitudes = solicitudes.filter(estado=estado_filtro)

    context = {
        'page_title': "Gestionar Solicitudes de Afiliación",
        'solicitudes': solicitudes,
        'estados': SolicitudAfiliacion.Estado.choices,
    }
    return render(request, 'staff_panel/solicitud_afiliacion_list.html', context)


@staff_member_required
def solicitud_afiliacion_manage_view(request, pk):
    """
    Muestra los detalles de una solicitud y permite al staff aprobarla o rechazarla.
    """
    solicitud = get_object_or_404(
        SolicitudAfiliacion.objects.select_related(
            'solicitante', 'detallesolicitudnatural', 'detallesolicitudjuridica'
        ), pk=pk
    )

    if request.method == 'POST':
        action = request.POST.get('action')

        try:
            if action == 'aprobar':
                aprobar_solicitud(solicitud, request.user)
                messages.success(request, f"La solicitud de {solicitud.solicitante.username} ha sido APROBADA.")
            elif action == 'rechazar':
                rechazar_solicitud(solicitud)
                messages.warning(request, f"La solicitud de {solicitud.solicitante.username} ha sido RECHAZADA.")

            return redirect('staff_panel:solicitud-afiliacion-list')

        except ValueError as e:
            messages.error(request, str(e))

    context = {
        'page_title': f"Detalle de Solicitud #{solicitud.id}",
        'solicitud': solicitud,
    }
    return render(request, 'staff_panel/solicitud_afiliacion_manage.html', context)


@staff_member_required
def solicitud_servicio_list_view(request):
    """
    Muestra una lista de todas las solicitudes de servicio para ser gestionadas.
    """
    solicitudes = SolicitudServicio.objects.select_related(
        'solicitante', 'recurso', 'recurso__servicio'
    ).order_by('fecha_creacion')

    context = {
        'page_title': "Gestionar Solicitudes de Servicio",
        'solicitudes': solicitudes,
    }
    return render(request, 'staff_panel/solicitud_servicio_list.html', context)


@staff_member_required
def solicitud_servicio_manage_view(request, pk):
    """
    Muestra los detalles de una solicitud de servicio y permite al staff gestionarla.
    """
    solicitud = get_object_or_404(SolicitudServicio, pk=pk)
    form = RespuestaSolicitudForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        action = request.POST.get('action')
        respuesta = form.cleaned_data['respuesta']

        try:
            if action == 'aprobar':
                procesar_solicitud(solicitud, request.user, SolicitudServicio.Estado.CONFIRMADA, respuesta)
                messages.success(request, "La solicitud ha sido APROBADA.")
            elif action == 'rechazar':
                procesar_solicitud(solicitud, request.user, SolicitudServicio.Estado.RECHAZADA, respuesta)
                messages.warning(request, "La solicitud ha sido RECHAZADA.")

            return redirect('staff_panel:solicitud-servicio-list')
        except ValueError as e:
            messages.error(request, str(e))

    context = {
        'page_title': f"Gestionar Solicitud de {solicitud.recurso.nombre}",
        'solicitud': solicitud,
        'form': form,
    }
    return render(request, 'staff_panel/solicitud_servicio_manage.html', context)


@staff_member_required
def noticia_list_view(request):
    """
    Muestra una lista de todas las noticias para que el personal las gestione.
    """
    noticias = Noticia.objects.select_related('autor', 'categoria').all()
    context = {
        'page_title': "Gestionar Noticias",
        'noticias': noticias,
    }
    return render(request, 'staff_panel/noticia_list.html', context)


@staff_member_required
def noticia_create_view(request):
    """
    Crea una nueva noticia.
    """
    if request.method == 'POST':
        form = NoticiaForm(request.POST)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.autor = request.user
            noticia.save()
            messages.success(request, "La noticia ha sido creada con éxito.")
            return redirect('staff_panel:noticia-list')
    else:
        form = NoticiaForm()

    context = {
        'form': form,
        'page_title': "Crear Nueva Noticia"
    }
    return render(request, 'staff_panel/noticia_form.html', context)


@staff_member_required
def noticia_update_view(request, pk):
    """
    Actualiza una noticia existente.
    """
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, instance=noticia)
        if form.is_valid():
            form.save()
            messages.success(request, "La noticia ha sido actualizada con éxito.")
            return redirect('staff_panel:noticia-list')
    else:
        form = NoticiaForm(instance=noticia)

    context = {
        'form': form,
        'noticia': noticia,
        'page_title': f"Editando: {noticia.titulo}"
    }
    return render(request, 'staff_panel/noticia_form.html', context)


@staff_member_required
def servicio_list_staff_view(request):
    """Muestra la lista de servicios para que el personal los gestione."""
    servicios = Servicio.objects.select_related('categoria').all()
    context = {
        'page_title': "Gestionar Catálogo de Servicios",
        'servicios': servicios,
    }
    return render(request, 'staff_panel/servicio_list_staff.html', context)


@staff_member_required
def servicio_manage_view(request, pk=None):
    """Gestiona la creación y edición de un Servicio."""
    instance = get_object_or_404(Servicio, pk=pk) if pk else None
    form = ServicioForm(request.POST or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"Servicio '{form.cleaned_data['nombre']}' guardado con éxito.")
        return redirect('staff_panel:servicio-list-staff')

    context = {
        'form': form,
        'page_title': "Editar Servicio" if instance else "Crear Nuevo Servicio"
    }
    return render(request, 'staff_panel/servicio_form.html', context)


@staff_member_required
def servicio_detail_staff_view(request, pk):
    """Muestra los recursos de un servicio específico."""
    servicio = get_object_or_404(Servicio, pk=pk)
    recursos = RecursoServicio.objects.filter(servicio=servicio)
    context = {
        'page_title': f"Gestionar Recursos de '{servicio.nombre}'",
        'servicio': servicio,
        'recursos': recursos
    }
    return render(request, 'staff_panel/servicio_detail_staff.html', context)


@staff_member_required
def recurso_manage_view(request, pk=None, servicio_pk=None):
    """Gestiona la creación y edición de un RecursoServicio."""
    # Si estamos creando, necesitamos el servicio_pk de la URL.
    if servicio_pk:
        servicio = get_object_or_404(Servicio, pk=servicio_pk)

    # Si estamos editando, obtenemos el recurso y su servicio a través de él.
    instance = get_object_or_404(RecursoServicio, pk=pk) if pk else None
    if instance:
        servicio = instance.servicio

    form = RecursoServicioForm(request.POST or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        recurso = form.save(commit=False)
        recurso.servicio = servicio
        recurso.save()
        messages.success(request, f"Recurso '{recurso.nombre}' guardado con éxito.")
        return redirect('staff_panel:servicio-detail-staff', pk=servicio.pk)

    context = {
        'form': form,
        'page_title': "Editar Recurso" if instance else "Añadir Nuevo Recurso"
    }
    return render(request, 'staff_panel/servicio_form.html', context)

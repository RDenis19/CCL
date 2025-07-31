from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.text import slugify

from content.models import Noticia, CategoriaNoticia
from memberships.models import SolicitudAfiliacion
from memberships.services import aprobar_solicitud, rechazar_solicitud
from payments.models import Pago
from services.forms import RespuestaSolicitudForm
from services.models import SolicitudServicio, Servicio, RecursoServicio
from services.services import procesar_solicitud
from staff_panel.forms import NoticiaForm, RecursoServicioForm, ServicioForm

# El decorador @staff_member_required asegura que solo usuarios marcados como "staff"
# puedan acceder a estas vistas.
@staff_member_required
def dashboard_staff_view(request):
    """
    Muestra el panel de control principal para el personal (staff).
    Calcula los contadores de tareas pendientes para un resumen rápido.
    """
    # Hago recuentos rápidos de los registros pendientes en diferentes modelos.
    pendientes_afiliacion = SolicitudAfiliacion.objects.filter(
        estado=SolicitudAfiliacion.Estado.PENDIENTE
    ).count()

    pendientes_servicios = SolicitudServicio.objects.filter(
        estado=SolicitudServicio.Estado.PENDIENTE
    ).count()

    pendientes_pagos = Pago.objects.filter(
        estado=Pago.EstadoPago.PENDIENTE
    ).count()

    # Preparo el contexto para pasar los datos a la plantilla HTML.
    context = {
        'page_title': "Panel de Gestión",
        'pendientes_afiliacion': pendientes_afiliacion,
        'pendientes_servicios': pendientes_servicios,
        'pendientes_pagos': pendientes_pagos,
    }
    return render(request, 'staff_panel/dashboard.html', context)

# --- Vistas para Gestionar Afiliaciones ---

@staff_member_required
def solicitud_afiliacion_list_view(request):
    """
    Muestra una lista de todas las solicitudes de afiliación para ser gestionadas.
    """
    # Traigo las solicitudes y sus usuarios relacionados en una sola consulta para ser más eficiente.
    solicitudes = SolicitudAfiliacion.objects.select_related('solicitante').order_by('fecha_creacion')

    # Permito filtrar la lista por estado a través de un parámetro en la URL (ej: ?estado=PENDIENTE).
    estado_filtro = request.GET.get('estado')
    if estado_filtro and estado_filtro in SolicitudAfiliacion.Estado.values:
        solicitudes = solicitudes.filter(estado=estado_filtro)

    context = {
        'page_title': "Gestionar Solicitudes de Afiliación",
        'solicitudes': solicitudes,
        'estados': SolicitudAfiliacion.Estado.choices, # Para construir los botones de filtro.
    }
    return render(request, 'staff_panel/solicitud_afiliacion_list.html', context)


@staff_member_required
def solicitud_afiliacion_manage_view(request, pk):
    """
    Muestra los detalles de una solicitud y permite al staff aprobarla o rechazarla.
    """
    # Busco la solicitud por su ID (pk). Si no la encuentro, muestro un error 404.
    # Optimizo la consulta trayendo todos los datos relacionados de una vez.
    solicitud = get_object_or_404(
        SolicitudAfiliacion.objects.select_related(
            'solicitante', 'detallesolicitudnatural', 'detallesolicitudjuridica'
        ).prefetch_related('documentos'),
        pk=pk
    )

    # Si el método es POST, significa que el staff está realizando una acción (aprobar/rechazar).
    if request.method == 'POST':
        action = request.POST.get('action')

        try:
            # La lógica pesada de aprobar o rechazar la delego a funciones en "services".
            if action == 'aprobar':
                aprobar_solicitud(solicitud, request.user)
                messages.success(request, f"La solicitud de {solicitud.solicitante.username} ha sido APROBADA.")
            elif action == 'rechazar':
                rechazar_solicitud(solicitud)
                messages.warning(request, f"La solicitud de {solicitud.solicitante.username} ha sido RECHAZADA.")

            return redirect('staff_panel:solicitud-afiliacion-list')

        except ValueError as e:
            # Si la lógica del servicio lanza un error (ej: ya estaba aprobada), lo muestro.
            messages.error(request, str(e))

    context = {
        'page_title': f"Detalle de Solicitud #{solicitud.id}",
        'solicitud': solicitud,
    }
    return render(request, 'staff_panel/solicitud_afiliacion_manage.html', context)

# --- Vistas para Gestionar Servicios ---

@staff_member_required
def solicitud_servicio_list_view(request):
    """ Muestra una lista de todas las solicitudes de servicio para ser gestionadas. """
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
    """ Muestra los detalles de una solicitud de servicio y permite al staff gestionarla. """
    solicitud = get_object_or_404(SolicitudServicio, pk=pk)
    # Este formulario es para que el staff escriba una respuesta al aprobar/rechazar.
    form = RespuestaSolicitudForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        action = request.POST.get('action')
        respuesta = form.cleaned_data['respuesta']

        try:
            # Delego la lógica a un service para mantener esta vista limpia.
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

# --- Vistas para CRUD de Noticias ---

@staff_member_required
def noticia_list_view(request):
    """ Muestra una lista de todas las noticias para que el personal las gestione. """
    noticias = Noticia.objects.select_related('autor', 'categoria').all()
    context = {
        'page_title': "Gestionar Noticias",
        'noticias': noticias,
    }
    return render(request, 'staff_panel/noticia_list.html', context)


@staff_member_required
def noticia_create_view(request):
    """ Crea una nueva noticia. """
    if request.method == 'POST':
        form = NoticiaForm(request.POST)
        if form.is_valid():
            nombre_nueva_cat = form.cleaned_data.get('nueva_categoria')
            categoria = form.cleaned_data.get('categoria')

            # Si el staff escribió en el campo "nueva categoría", la creo al instante.
            if nombre_nueva_cat:
                categoria = CategoriaNoticia.objects.create(
                    nombre=nombre_nueva_cat,
                    slug=slugify(nombre_nueva_cat)
                )

            # Guardo la noticia sin meterla a la BD todavía (commit=False).
            noticia = form.save(commit=False)
            noticia.autor = request.user # Asigno al autor actual.
            noticia.categoria = categoria # Asigno la categoría (existente o recién creada).
            noticia.save() # Ahora sí, la guardo en la BD.

            messages.success(request, "La noticia ha sido creada con éxito.")
            return redirect('staff_panel:noticia-list')
    else:
        # Si es un GET, solo muestro el formulario vacío.
        form = NoticiaForm()

    context = {
        'form': form,
        'page_title': "Crear Nueva Noticia"
    }
    return render(request, 'staff_panel/noticia_form.html', context)


@staff_member_required
def noticia_update_view(request, pk):
    """ Actualiza una noticia existente. """
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        # Al pasar 'instance=noticia', el formulario se carga con los datos existentes.
        form = NoticiaForm(request.POST, instance=noticia)
        if form.is_valid():
            form.save() # Guardar los cambios es así de simple con un ModelForm.
            messages.success(request, "La noticia ha sido actualizada con éxito.")
            return redirect('staff_panel:noticia-list')
    else:
        # Muestro el formulario precargado con los datos de la noticia a editar.
        form = NoticiaForm(instance=noticia)

    context = {
        'form': form,
        'noticia': noticia,
        'page_title': f"Editando: {noticia.titulo}"
    }
    return render(request, 'staff_panel/noticia_form.html', context)

# --- Vistas para CRUD de Catálogo de Servicios y Recursos ---

@staff_member_required
def servicio_list_staff_view(request):
    """ Muestra la lista de servicios para que el personal los gestione. """
    servicios = Servicio.objects.select_related('categoria').all()
    context = {
        'page_title': "Gestionar Catálogo de Servicios",
        'servicios': servicios,
    }
    return render(request, 'staff_panel/servicio_list_staff.html', context)


@staff_member_required
def servicio_manage_view(request, pk=None):
    """ Gestiona la creación y edición de un Servicio en una sola vista. """
    # Si viene un 'pk', estoy editando. Si no, estoy creando (instance=None).
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
    """ Muestra los recursos de un servicio específico. """
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
    """ Gestiona la creación y edición de un RecursoServicio. """
    servicio = None
    # Determino a qué servicio pertenece el recurso.
    if servicio_pk: # Si estoy creando, el ID del servicio viene en la URL.
        servicio = get_object_or_404(Servicio, pk=servicio_pk)
    
    instance = get_object_or_404(RecursoServicio, pk=pk) if pk else None
    if instance: # Si estoy editando, obtengo el servicio desde el propio recurso.
        servicio = instance.servicio

    form = RecursoServicioForm(request.POST or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        recurso = form.save(commit=False)
        recurso.servicio = servicio # Asigno el servicio padre antes de guardar.
        recurso.save()
        messages.success(request, f"Recurso '{recurso.nombre}' guardado con éxito.")
        return redirect('staff_panel:servicio-detail-staff', pk=servicio.pk)

    context = {
        'form': form,
        'page_title': "Editar Recurso" if instance else "Añadir Nuevo Recurso"
    }
    return render(request, 'staff_panel/servicio_form.html', context)


# --- Vistas para Gestionar Pagos ---

@staff_member_required
def pago_list_view(request):
    """ Muestra una lista de todos los pagos pendientes de verificación. """
    pagos_pendientes = Pago.objects.filter(
        estado=Pago.EstadoPago.PENDIENTE
    ).select_related(
        'solicitud_servicio__solicitante', 'solicitud_servicio__recurso'
    ).order_by('fecha_creacion')

    context = {
        'page_title': "Verificar Pagos de Servicios",
        'pagos': pagos_pendientes,
    }
    return render(request, 'staff_panel/pago_list.html', context)


@staff_member_required
def pago_manage_view(request, pk):
    """
    Muestra el detalle de un pago, incluyendo el comprobante, y permite al
    staff verificarlo.
    """
    # Busco un pago específico que además esté PENDIENTE.
    pago = get_object_or_404(
        Pago.objects.select_related(
            'solicitud_servicio__solicitante',
            'solicitud_servicio__recurso__servicio'
        ),
        pk=pk,
        estado=Pago.EstadoPago.PENDIENTE
    )

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'verificar_pago':
            # Actualizo el estado y los campos de auditoría.
            pago.estado = Pago.EstadoPago.VERIFICADO
            pago.gestor = request.user
            pago.fecha_verificacion = timezone.now()
            # Uso update_fields para que la consulta a la BD sea más eficiente.
            pago.save(update_fields=['estado', 'gestor', 'fecha_verificacion'])

            # Al guardar el pago, se dispara una señal que actualiza el estado de la solicitud de servicio.
            messages.success(request,
                             f"El pago para la solicitud de '{pago.solicitud_servicio.recurso.nombre}' ha sido VERIFICADO.")
            return redirect('staff_panel:pago-list')

    context = {
        'page_title': "Verificar Detalle de Pago",
        'pago': pago,
    }
    return render(request, 'staff_panel/pago_manage.html', context)

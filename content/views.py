# Archivo: content/views.py

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Noticia
from .forms import ComentarioNoticiaForm


def noticia_list_view(request):
    """Muestra una lista paginada de noticias publicadas."""
    noticias = Noticia.objects.filter(
        estado=Noticia.Estado.PUBLICADA,
        fecha_publicacion__lte=timezone.now()
    ).select_related('autor', 'categoria')

    context = {
        'noticias': noticias,
        'page_title': _("Noticias y Novedades")
    }
    return render(request, 'content/noticia_list.html', context)


def noticia_detail_view(request, slug):
    """
    Muestra una noticia en detalle, sus comentarios y un formulario
    para que los usuarios autenticados puedan comentar.
    """
    noticia = get_object_or_404(
        Noticia,
        slug=slug,
        estado=Noticia.Estado.PUBLICADA,
        fecha_publicacion__lte=timezone.now()
    )
    comentarios = noticia.comentarios.filter(aprobado=True).select_related('autor__perfil')

    # Lógica del formulario de comentarios
    form = ComentarioNoticiaForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = ComentarioNoticiaForm(request.POST)
        if form.is_valid():
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.noticia = noticia
            nuevo_comentario.autor = request.user
            nuevo_comentario.save()
            messages.success(request, _("Tu comentario ha sido publicado."))
            return redirect(noticia.get_absolute_url())
    elif request.method == 'POST' and not request.user.is_authenticated:
        messages.error(request, _("Debes iniciar sesión para poder comentar."))

    context = {
        'noticia': noticia,
        'comentarios': comentarios,
        'form_comentario': form,
        'page_title': noticia.titulo
    }
    return render(request, 'content/noticia_detail.html', context)

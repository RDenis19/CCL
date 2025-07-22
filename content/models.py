from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Referencia flexible al modelo de usuario del proyecto.
User = settings.AUTH_USER_MODEL


class CategoriaNoticia(models.Model):
    """
    Categoriza las noticias para facilitar su organización y filtrado
    """
    nombre = models.CharField(
        _("Nombre"),
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        _("Slug"),
        max_length=120,
        unique=True,
        help_text=_("Versión del nombre apta para URLs.")
    )

    class Meta:
        verbose_name = _("Categoría de Noticia")
        verbose_name_plural = _("Categorías de Noticias")
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Noticia(models.Model):
    """
    Representa una noticia individual
    """

    class Estado(models.TextChoices):
        # Permite al personal guardar noticias sin publicarlas.
        BORRADOR = "BORRADOR", _("Borrador")
        PUBLICADA = "PUBLICADA", _("Publicada")

    # El autor de la noticia, limitado a usuarios que son parte del personal.
    autor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="noticias_creadas",
        limit_choices_to={'is_staff': True}
    )

    categoria = models.ForeignKey(
        CategoriaNoticia,
        on_delete=models.SET_NULL,
        null=True,
        related_name="noticias"
    )
    titulo = models.CharField(_("Título"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=220, unique=True)
    contenido = models.TextField(_("Contenido"))

    # Controla la visibilidad de la noticia en el sitio público.
    estado = models.CharField(
        _("Estado"),
        max_length=20,
        choices=Estado.choices,
        default=Estado.BORRADOR,
        db_index=True
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    fecha_publicacion = models.DateTimeField(
        _("Fecha de Publicación"),
        null=True,
        blank=True,
        help_text=_("La noticia será visible a partir de esta fecha si el estado es 'Publicada'.")
    )

    class Meta:
        verbose_name = _("Noticia")
        verbose_name_plural = _("Noticias")
        ordering = ["-fecha_publicacion"]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        """
        Permite enlazar a la noticia de forma consistente desde cualquier
        parte de la aplicación usando {% url 'content:noticia-detail' noticia.slug %}.
        """
        return reverse("content:noticia-detail", kwargs={"slug": self.slug})


class ComentarioNoticia(models.Model):
    """
    Representa un comentario hecho por un usuario en una noticia.
    """

    noticia = models.ForeignKey(
        Noticia,
        on_delete=models.CASCADE,
        related_name="comentarios"
    )

    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comentarios_noticia"
    )
    contenido = models.TextField(_("Contenido del Comentario"))

    # Campo para moderación. Permite al personal ocultar comentarios que no cumplan con las normas de la comunidad.
    aprobado = models.BooleanField(
        _("Aprobado"),
        default=True,
        help_text=_("Los administradores pueden desactivar comentarios inapropiados.")
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Comentario de Noticia")
        verbose_name_plural = _("Comentarios de Noticias")
        ordering = ["fecha_creacion"]

    def __str__(self):
        return f"Comentario de {self.autor.username} en {self.noticia.titulo}"

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Defino una referencia al modelo de Usuario que esté activo en el proyecto.
# Es una buena práctica para no tener que importar el modelo User directamente.
User = settings.AUTH_USER_MODEL


class CategoriaNoticia(models.Model):
    """
    Categoriza las noticias para facilitar su organización y filtrado.
    Ej: 'Eventos', 'Comunicados', 'Beneficios'.
    """
    nombre = models.CharField(
        _("Nombre"),
        max_length=100,
        unique=True # Me aseguro que no haya dos categorías con el mismo nombre.
    )
    # El slug es la versión del nombre para usar en las URLs (ej: 'eventos-importantes').
    slug = models.SlugField(
        _("Slug"),
        max_length=120,
        unique=True,
        help_text=_("Nombre apto para URLs.")
    )

    # La clase Meta me permite configurar cosas del modelo.
    class Meta:
        # Nombres que se usarán en el panel de administración de Django.
        verbose_name = _("Categoría de Noticia")
        verbose_name_plural = _("Categorías de Noticias")
        # Ordeno las categorías alfabéticamente por nombre por defecto.
        ordering = ["nombre"]

    # Defino cómo se va a mostrar un objeto de esta clase (ej: en el admin).
    def __str__(self):
        return self.nombre


class Noticia(models.Model):
    """
    Representa una noticia o artículo individual del blog.
    """
    class Estado(models.TextChoices):
        # Permite al personal guardar noticias sin que sean visibles para el público.
        BORRADOR = "BORRADOR", _("Borrador")
        PUBLICADA = "PUBLICADA", _("Publicada")

    # Relación con el autor (un usuario del sistema).
    autor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # Si se borra el autor, la noticia no se borra, solo se queda sin autor.
        null=True,
        related_name="noticias_creadas",
        limit_choices_to={'is_staff': True} # Solo usuarios del staff pueden ser autores.
    )

    # Relación con la categoría.
    categoria = models.ForeignKey(
        CategoriaNoticia,
        on_delete=models.SET_NULL, # Igual que el autor, si se borra la categoría la noticia no se ve afectada.
        null=True,
        related_name="noticias"
    )
    titulo = models.CharField(_("Título"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=220, unique=True)
    contenido = models.TextField(_("Contenido")) # Aquí va el cuerpo de la noticia.

    # Campo para controlar la visibilidad de la noticia en el sitio público.
    estado = models.CharField(
        _("Estado"),
        max_length=20,
        choices=Estado.choices,
        default=Estado.BORRADOR,
        db_index=True 
    )

    # Timestamps para saber cuándo se creó y modificó.
    fecha_creacion = models.DateTimeField(auto_now_add=True) # Se guarda solo al crear.
    fecha_modificacion = models.DateTimeField(auto_now=True) # Se actualiza cada vez que se guarda.

    fecha_publicacion = models.DateTimeField(
        _("Fecha de Publicación"),
        null=True,
        blank=True,
        help_text=_("La noticia será visible a partir de esta fecha si el estado es 'Publicada'.")
    )

    # Opciones para este modelo.
    class Meta:
        verbose_name = _("Noticia")
        verbose_name_plural = _("Noticias")
        # Muestra las noticias más recientes primero.
        ordering = ["-fecha_publicacion"]

    # El __str__ es importante para que se muestre el título de la noticia.
    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        """
        Genera la URL única para una noticia específica.
        Permite enlazar a la noticia de forma consistente desde cualquier
        parte de la aplicación usando {% url 'content:noticia-detail' noticia.slug %}.
        """
        return reverse("content:noticia-detail", kwargs={"slug": self.slug})


class ComentarioNoticia(models.Model):
    """
    Representa un comentario hecho por un usuario en una noticia.
    """
    # Relaciono el comentario con la noticia.
    noticia = models.ForeignKey(
        Noticia,
        on_delete=models.CASCADE, # Si se borra la noticia, se borran todos sus comentarios.
        related_name="comentarios"
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comentarios_noticia"
    )
    contenido = models.TextField(_("Contenido del Comentario"))

    # Campo para moderación. Permite al personal ocultar comentarios.
    aprobado = models.BooleanField(
        _("Aprobado"),
        default=True, # Los comentarios son visibles por defecto.
        help_text=_("Los administradores pueden desactivar comentarios inapropiados.")
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Configuraciones del modelo ComentarioNoticia.
    class Meta:
        verbose_name = _("Comentario de Noticia")
        verbose_name_plural = _("Comentarios de Noticias")
        # Muestra los comentarios en orden cronológico, del más antiguo al más nuevo.
        ordering = ["fecha_creacion"]

    # Una representación útil para el admin.
    def __str__(self):
        return f"Comentario de {self.autor.username} en {self.noticia.titulo}"
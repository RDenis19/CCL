from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# --- Constantes y Opciones ---

# Buena práctica para referenciar el modelo de usuario de forma flexible.
User = settings.AUTH_USER_MODEL


# --- Modelos ---

class Membresia(models.Model):
    """
    Representa el registro maestro y permanente de un socio activo.

    Este modelo se crea cuando una 'SolicitudAfiliacion' es aprobada y
    contiene los datos administrativos de la membresía, como su estado
    y número de socio.
    """

    class Estado(models.TextChoices):
        ACTIVA = "ACTIVA", _("Activa")
        SUSPENDIDA = "SUSPENDIDA", _("Suspendida")
        CANCELADA = "CANCELADA", _("Cancelada")

    # Relación principal con el usuario. Una membresía pertenece a un solo usuario.
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="membresia",
        verbose_name=_("Usuario Socio")
    )

    # Trazabilidad: Vincula con la solicitud que originó esta membresía.
    # Se usa una cadena 'app.Model' para evitar importaciones circulares.
    solicitud_origen = models.OneToOneField(
        "memberships.SolicitudAfiliacion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="membresia_generada",
        verbose_name=_("Solicitud de Origen")
    )

    # Trazabilidad: Registra qué administrador aprobó la membresía.
    aprobado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="membresias_aprobadas",
        limit_choices_to={'is_staff': True},
        verbose_name=_("Aprobado por")
    )

    numero_socio = models.CharField(
        _("Número de Socio"),
        max_length=50,
        unique=True,
        help_text=_("Identificador único y permanente para el socio.")
    )
    estado = models.CharField(
        _("Estado de la Membresía"),
        max_length=20,
        choices=Estado.choices,
        default=Estado.ACTIVA,
        db_index=True
    )
    fecha_ingreso = models.DateField(
        _("Fecha de Ingreso"),
        help_text=_("Fecha oficial de inicio de la membresía.")
    )

    # Trazabilidad: Timestamps de creación y modificación del registro.
    fecha_creacion = models.DateTimeField(_("Fecha de Creación"), auto_now_add=True)
    fecha_modificacion = models.DateTimeField(_("Fecha de Modificación"), auto_now=True)

    class Meta:
        verbose_name = _("Membresía")
        verbose_name_plural = _("Membresías")
        ordering = ["-fecha_ingreso", "usuario__username"]

    def __str__(self):
        return f"Membresía de {self.usuario.get_full_name() or self.usuario.username}"


class PerfilUsuario(models.Model):
    """
    Extiende el modelo de Usuario para añadir campos de perfil adicionales.

    Este modelo almacena información pública o personal del usuario que no
    pertenece al sistema de autenticación, como su avatar y biografía.
    """
    # Relación uno a uno que define este modelo como un perfil del usuario.
    # 'primary_key=True' es una optimización para que no se cree un 'id' adicional.
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil",
        primary_key=True,
        verbose_name=_("Usuario")
    )

    avatar = models.ImageField(
        _("Avatar"),
        upload_to="perfiles/avatares/",
        null=True,
        blank=True,
        help_text=_("Imagen de perfil del usuario.")
    )
    biografia = models.TextField(_("Biografía"), blank=True)
    redes_sociales = models.JSONField(
        _("Redes Sociales"),
        null=True,
        blank=True,
        help_text=_("Ej: {'twitter': 'https://twitter.com/usuario', 'linkedin': '...'}")
    )

    # Trazabilidad: Solo se necesita la fecha de modificación.
    fecha_modificacion = models.DateTimeField(_("Última Modificación"), auto_now=True)

    class Meta:
        verbose_name = _("Perfil de Usuario")
        verbose_name_plural = _("Perfiles de Usuario")

    def __str__(self):
        return f"Perfil de {self.usuario.get_full_name() or self.usuario.username}"

# NOTA: Para crear automáticamente un 'PerfilUsuario' cuando se crea un 'User',
# la mejor práctica es usar señales (signals) de Django en un archivo 'users/signals.py'.

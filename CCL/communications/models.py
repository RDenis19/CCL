# Archivo: communications/models.py

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL


class Notificacion(models.Model):
    """
    Representa una notificación para un usuario sobre una acción en el sistema.
    """

    class Tipo(models.TextChoices):
        SISTEMA = "SISTEMA", _("Sistema")  # Ej: Inició sesión, cerró sesión
        AFILIACION = "AFILIACION", _("Afiliación")  # Ej: Solicitud aprobada
        SERVICIOS = "SERVICIOS", _("Servicios")  # Ej: Reserva confirmada
        CONTENIDO = "CONTENIDO", _("Contenido")  # Ej: Nueva noticia importante

    tipo = models.CharField(
        _("Tipo de Notificación"),
        max_length=20,
        choices=Tipo.choices,
        default=Tipo.SISTEMA,
        db_index=True
    )

    # El usuario que recibe la notificación.
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notificaciones")

    # El usuario que realizó la acción (opcional, puede ser el sistema).
    actor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                              related_name="acciones_notificadas")

    # Descripción de la acción. Ej: "aprobó tu solicitud de afiliación".
    verbo = models.CharField(_("Verbo"), max_length=255)

    # Campos para la Clave Foránea Genérica
        # --- CÓDIGO CORREGIDO ---
    # Campos para la Clave Foránea Genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    
    # CAMBIO: Cambiamos el tipo de campo para que acepte UUIDs como texto
    object_id = models.CharField(max_length=255, null=True, blank=True)
    
    objetivo = GenericForeignKey('content_type', 'object_id')
    # --- FIN DEL CÓDIGO CORREGIDO ---

    leida = models.BooleanField(_("¿Leída?"), default=False, db_index=True)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    class Meta:
        verbose_name = _("Notificación")
        verbose_name_plural = _("Notificaciones")
        ordering = ['-timestamp']

    def __str__(self):
        if self.objetivo:
            return f"{self.actor} {self.verbo} {self.objetivo}"
        return f"{self.actor} {self.verbo}"

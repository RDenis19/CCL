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
    # El usuario que recibe la notificación.
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notificaciones")

    # El usuario que realizó la acción (opcional, puede ser el sistema).
    actor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                              related_name="acciones_notificadas")

    # Descripción de la acción. Ej: "aprobó tu solicitud de afiliación".
    verbo = models.CharField(_("Verbo"), max_length=255)

    # Campos para la Clave Foránea Genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    objetivo = GenericForeignKey('content_type', 'object_id')

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

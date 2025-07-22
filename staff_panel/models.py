from django.db import models
from django.utils.translation import gettext_lazy as _


class ConfiguracionNotificacion(models.Model):
    """
    Permite al personal gestionar las notificaciones automáticas del sistema.
    """
    codigo_evento = models.CharField(
        _("Código del Evento"),
        max_length=100,
        unique=True,
        help_text=_("Identificador único para el evento, ej: SOLICITUD_APROBADA")
    )
    descripcion = models.CharField(_("Descripción"), max_length=255)
    mensaje_plantilla = models.CharField(
        _("Plantilla del Mensaje"),
        max_length=255,
        help_text=_("Usa placeholders como {solicitante} o {estado}.")
    )
    esta_activa = models.BooleanField(_("¿Está activa?"), default=True)

    class Meta:
        verbose_name = _("Configuración de Notificación")
        verbose_name_plural = _("Configuraciones de Notificaciones")

    def __str__(self):
        return self.descripcion

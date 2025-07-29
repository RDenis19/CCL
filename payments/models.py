# Archivo: payments/models.py
import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from services.models import SolicitudServicio

User = settings.AUTH_USER_MODEL


class Pago(models.Model):
    """
    Representa una transacción financiera asociada a una SolicitudServicio.
    Está diseñado para un flujo de verificación manual.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class EstadoPago(models.TextChoices):
        PENDIENTE = "PENDIENTE", _("Pendiente de Verificación")
        VERIFICADO = "VERIFICADO", _("Verificado")

    solicitud_servicio = models.OneToOneField(
        SolicitudServicio,
        on_delete=models.CASCADE,
        related_name="pago",
        verbose_name=_("Solicitud de Servicio")
    )
    monto = models.DecimalField(_("Monto del Servicio"), max_digits=10, decimal_places=2)
    estado = models.CharField(
        _("Estado del Pago"),
        max_length=20,
        choices=EstadoPago.choices,
        default=EstadoPago.PENDIENTE,
        db_index=True
    )
    comprobante = models.FileField(
        _("Comprobante de Pago"),
        upload_to='pagos/comprobantes/%Y/%m/',
        help_text=_("Archivo del comprobante subido por el usuario.")
    )

    # Trazabilidad
    gestor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="pagos_verificados",
        limit_choices_to={'is_staff': True},
        verbose_name=_("Verificado por")
    )
    fecha_creacion = models.DateTimeField(_("Fecha de Subida"), auto_now_add=True)
    fecha_verificacion = models.DateTimeField(_("Fecha de Verificación"), null=True, blank=True)

    class Meta:
        verbose_name = _("Pago")
        verbose_name_plural = _("Pagos")
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"Pago para solicitud de {self.solicitud_servicio.recurso.nombre}"

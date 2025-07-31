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
    Está diseñado para un flujo de verificación manual por parte del personal.
    """
    # Uso UUID como clave primaria para tener un ID único y no secuencial,
    # lo que puede ser más seguro y práctico.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Defino los posibles estados de un pago para tener un control claro.
    class EstadoPago(models.TextChoices):
        PENDIENTE = "PENDIENTE", _("Pendiente de Verificación")
        VERIFICADO = "VERIFICADO", _("Verificado")

    # Relaciono el pago de forma única a una solicitud de servicio.
    # Si la solicitud se elimina, el pago asociado también se eliminará.
    solicitud_servicio = models.OneToOneField(
        SolicitudServicio,
        on_delete=models.CASCADE,
        related_name="pago",
        verbose_name=_("Solicitud de Servicio")
    )
    # Uso DecimalField para guardar dinero, es la forma correcta para evitar errores.
    monto = models.DecimalField(_("Monto del Servicio"), max_digits=10, decimal_places=2)
    estado = models.CharField(
        _("Estado del Pago"),
        max_length=20,
        choices=EstadoPago.choices,
        default=EstadoPago.PENDIENTE,
        db_index=True  # Le pongo un índice porque probablemente filtraré por estado.
    )
    # Aquí el usuario sube su recibo o captura de pantalla del pago.
    # Se guardará en una carpeta organizada por año y mes.
    comprobante = models.FileField(
        _("Comprobante de Pago"),
        upload_to='pagos/comprobantes/%Y/%m/',
        help_text=_("Archivo del comprobante subido por el usuario.")
    )

    # Guardo qué miembro del staff verificó el pago.
    gestor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Si se borra el usuario gestor, el registro de pago no se borra.
        null=True, blank=True,
        related_name="pagos_verificados",
        limit_choices_to={'is_staff': True}, # Solo se pueden elegir usuarios que son staff.
        verbose_name=_("Verificado por")
    )
    fecha_creacion = models.DateTimeField(_("Fecha de Subida"), auto_now_add=True)
    fecha_verificacion = models.DateTimeField(_("Fecha de Verificación"), null=True, blank=True)

    # Opciones para el modelo, como su nombre en el admin y el orden por defecto.
    class Meta:
        verbose_name = _("Pago")
        verbose_name_plural = _("Pagos")
        # Por defecto, muestro los pagos más recientes primero.
        ordering = ["-fecha_creacion"]

    # Esto es para que en el admin de Django se vea un nombre claro y no "Pago object".
    def __str__(self):
        return f"Pago para solicitud de {self.solicitud_servicio.recurso.nombre}"
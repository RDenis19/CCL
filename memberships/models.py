# Archivo: memberships/models.py
import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL


class SolicitudAfiliacion(models.Model):
    """
    Expediente principal para una solicitud de afiliación.
    Actúa como contenedor para los detalles específicos.
    """

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", _("Pendiente")
        EN_REVISION = "EN_REVISION", _("En Revisión")
        APROBADA = "APROBADA", _("Aprobada")
        RECHAZADA = "RECHAZADA", _("Rechazada")

    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name="solicitudes_afiliacion")
    estado = models.CharField(_("Estado"), max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)

    # Atributos de trazabilidad
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Solicitud de Afiliación")
        verbose_name_plural = _("Solicitudes de Afiliación")
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Solicitud de {self.solicitante.username} ({self.get_estado_display()})"


class DetalleSolicitudNatural(models.Model):
    """
    Detalles específicos para una solicitud de Persona Natural.
    """
    solicitud = models.OneToOneField(SolicitudAfiliacion, on_delete=models.CASCADE, primary_key=True)
    nombres = models.CharField(_("Nombres"), max_length=150)
    apellidos = models.CharField(_("Apellidos"), max_length=150)
    cedula = models.CharField(_("Cédula"), max_length=10, unique=True)
    direccion = models.CharField(_("Dirección Principal"), max_length=255)
    celular = models.CharField(_("Celular"), max_length=20)

    class Meta:
        verbose_name = _("Detalle de Solicitud (P. Natural)")
        verbose_name_plural = _("Detalles de Solicitud (P. Natural)")


class DetalleSolicitudJuridica(models.Model):
    """
    Detalles específicos para una solicitud de Persona Jurídica.
    """
    solicitud = models.OneToOneField(SolicitudAfiliacion, on_delete=models.CASCADE, primary_key=True)
    razon_social = models.CharField(_("Razón Social"), max_length=255)
    ruc = models.CharField(_("RUC"), max_length=13, unique=True)
    nombre_comercial = models.CharField(_("Nombre Comercial"), max_length=255, blank=True)
    direccion = models.CharField(_("Dirección Principal"), max_length=255)
    celular_empresa = models.CharField(_("Celular de la Empresa"), max_length=20)

    class Meta:
        verbose_name = _("Detalle de Solicitud (P. Jurídica)")
        verbose_name_plural = _("Detalles de Solicitud (P. Jurídica)")


class BeneficiarioPoliza(models.Model):
    """
    Almacena un beneficiario de la póliza de vida para una Persona Natural.
    """
    solicitud_natural = models.ForeignKey(DetalleSolicitudNatural, on_delete=models.CASCADE,
                                          related_name="beneficiarios")
    nombre_completo = models.CharField(_("Nombre Completo del Beneficiario"), max_length=255)
    porcentaje = models.DecimalField(_("Porcentaje"), max_digits=5, decimal_places=2, help_text=_("Ej: 50.00 para 50%"))

    class Meta:
        verbose_name = _("Beneficiario de Póliza")
        verbose_name_plural = _("Beneficiarios de Póliza")


class DocumentoAdjunto(models.Model):
    """
    Almacena un archivo adjunto para una solicitud de afiliación.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    solicitud = models.ForeignKey(SolicitudAfiliacion, on_delete=models.CASCADE, related_name="documentos")
    nombre_documento = models.CharField(
        _("Nombre del Documento"),
        max_length=200,
        help_text=_("Ej: Copia de Cédula, RUC, Nombramiento de Representante Legal")
    )
    archivo = models.FileField(_("Archivo"), upload_to="solicitud_documentos/%Y/%m/")
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Documento Adjunto")
        verbose_name_plural = _("Documentos Adjuntos")

    def __str__(self):
        return f"{self.nombre_documento} para solicitud #{self.solicitud.id}"

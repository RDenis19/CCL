# Archivo: services/models.py

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

User = settings.AUTH_USER_MODEL


class CategoriaServicio(models.Model):
    """Categoriza los servicios y beneficios (ej: Salud, Eventos, Consultoría)."""
    nombre = models.CharField(_("Nombre"), max_length=100, unique=True)
    descripcion = models.TextField(_("Descripción"), blank=True)

    class Meta:
        verbose_name = _("Categoría de Servicio")
        verbose_name_plural = _("Categorías de Servicios")
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    """Un servicio principal ofrecido por la organización (ej: Salones Sociales)."""
    categoria = models.ForeignKey(CategoriaServicio, on_delete=models.SET_NULL, null=True, related_name="servicios")
    nombre = models.CharField(_("Nombre del Servicio"), max_length=200)
    descripcion = models.TextField(_("Descripción detallada"))
    activo = models.BooleanField(_("¿Está activo?"), default=True,
                                 help_text=_("Desmarca para ocultar este servicio del catálogo."))

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Servicio")
        verbose_name_plural = _("Servicios")
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class DetalleCobertura(models.Model):
    """Detalle específico de una cobertura para un servicio (ej: un seguro)."""
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="coberturas")
    nombre_cobertura = models.CharField(_("Nombre de la Cobertura"), max_length=255)
    valor = models.DecimalField(_("Valor o Monto"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("Detalle de Cobertura")
        verbose_name_plural = _("Detalles de Cobertura")

    def __str__(self):
        return f"{self.nombre_cobertura} (${self.valor}) para {self.servicio.nombre}"


class Convenio(models.Model):
    """Una entidad externa con la que se tiene un convenio."""
    nombre_entidad = models.CharField(_("Nombre de la Entidad"), max_length=200)
    contacto = models.TextField(_("Información de Contacto"), blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Convenio")
        verbose_name_plural = _("Convenios")

    def __str__(self):
        return self.nombre_entidad


class Beneficio(models.Model):
    """Un beneficio específico ofrecido a través de un convenio."""
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE, related_name="beneficios")
    categoria = models.ForeignKey(CategoriaServicio, on_delete=models.SET_NULL, null=True, related_name="beneficios")
    descripcion = models.TextField(_("Descripción del Beneficio"))

    class Meta:
        verbose_name = _("Beneficio")
        verbose_name_plural = _("Beneficios")

    def __str__(self):
        return f"Beneficio de {self.convenio.nombre_entidad}"


class DetalleBeneficio(models.Model):
    """Un ítem de descuento o ventaja específica de un Beneficio."""
    beneficio = models.ForeignKey(Beneficio, on_delete=models.CASCADE, related_name="detalles")
    descripcion_descuento = models.CharField(_("Descripción del Descuento"), max_length=255)

    def __str__(self):
        return self.descripcion_descuento


class RecursoServicio(models.Model):
    """Un recurso específico que puede ser solicitado o reservado (un salón, un doctor)."""

    class TipoRecurso(models.TextChoices):
        PERSONA = "PERSONA", _("Persona")
        FISICO = "FISICO", _("Recurso Físico")

    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="recursos")
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="recursos_a_cargo")
    nombre = models.CharField(_("Nombre del Recurso"), max_length=200, help_text=_("Ej: Salón A, Dr. Pérez"))
    tipo = models.CharField(_("Tipo"), max_length=20, choices=TipoRecurso.choices)

    class Meta:
        verbose_name = _("Recurso de Servicio")
        verbose_name_plural = _("Recursos de Servicio")
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class HorarioDisponible(models.Model):
    """Un bloque de tiempo en el que un RecursoServicio está disponible."""
    recurso = models.ForeignKey(RecursoServicio, on_delete=models.CASCADE, related_name="horarios")
    fecha_hora_inicio = models.DateTimeField(_("Inicio de la Disponibilidad"))
    fecha_hora_fin = models.DateTimeField(_("Fin de la Disponibilidad"))
    esta_reservado = models.BooleanField(_("¿Está reservado?"), default=False)

    class Meta:
        verbose_name = _("Horario Disponible")
        verbose_name_plural = _("Horarios Disponibles")
        ordering = ["fecha_hora_inicio"]

    def __str__(self):
        return f"{self.recurso.nombre} disponible de {self.fecha_hora_inicio} a {self.fecha_hora_fin}"


class SolicitudServicio(models.Model):
    """Una cita, reserva o solicitud de servicio hecha por un usuario."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", _("Pendiente de Aprobación")
        CONFIRMADA = "CONFIRMADA", _("Confirmada")
        RECHAZADA = "RECHAZADA", _("Rechazada")
        COMPLETADA = "COMPLETADA", _("Completada")

    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name="solicitudes_servicio")
    recurso = models.ForeignKey(RecursoServicio, on_delete=models.CASCADE, related_name="solicitudes")
    horario = models.OneToOneField(HorarioDisponible, on_delete=models.SET_NULL, null=True, blank=True,
                                   help_text=_("Llenar solo si es una reserva por tiempo."))
    gestor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="solicitudes_gestionadas", limit_choices_to={'is_staff': True})
    estado = models.CharField(_("Estado"), max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)

    notas_usuario = models.TextField(_("Notas del Usuario"), blank=True)
    respuesta_gestor = models.TextField(_("Respuesta del Gestor"), blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Solicitud de Servicio")
        verbose_name_plural = _("Solicitudes de Servicio")
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"Solicitud de {self.recurso.nombre} por {self.solicitante.username}"

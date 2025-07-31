# Archivo: payments/admin.py
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Pago


@admin.action(description=_("Marcar pagos seleccionados como Verificados"))
def marcar_como_verificado(modeladmin, request, queryset):
    """
    Acción que permite al staff verificar pagos y confirmar la reserva.
    """
    for pago in queryset.filter(estado=Pago.EstadoPago.PENDIENTE):
        pago.estado = Pago.EstadoPago.VERIFICADO
        pago.gestor = request.user
        pago.fecha_verificacion = timezone.now()
        pago.save(update_fields=['estado', 'gestor', 'fecha_verificacion'])


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Pago.
    """
    list_display = ('id', 'solicitud_servicio', 'monto', 'estado', 'fecha_creacion', 'gestor')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = (
        'solicitud_servicio__solicitante__username',
        'solicitud_servicio__recurso__nombre'
    )
    autocomplete_fields = ('solicitud_servicio',)
    readonly_fields = ('fecha_creacion', 'fecha_verificacion', 'gestor')
    actions = [marcar_como_verificado]

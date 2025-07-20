# Archivo: memberships/admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import SolicitudAfiliacion, DetalleSolicitudNatural, DetalleSolicitudJuridica


@admin.register(SolicitudAfiliacion)
class SolicitudAfiliacionAdmin(admin.ModelAdmin):
    """
    Define la interfaz de administración para las Solicitudes de Afiliación.
    """
    list_display = ("id", "solicitante", "estado", "fecha_creacion")
    list_filter = ("estado",)
    readonly_fields = ("fecha_creacion", "fecha_modificacion")
    autocomplete_fields = ("solicitante",)

    # Este campo es el requisito CLAVE para que autocomplete_fields funcione en otros modelos.
    search_fields = (
        "solicitante__username",
        "solicitante__first_name",
        "solicitante__last_name",
        "solicitante__email",
        "detallesolicitudnatural__nombres",
        "detallesolicitudjuridica__razon_social",
    )

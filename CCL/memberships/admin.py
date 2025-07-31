# Archivo: memberships/admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import SolicitudAfiliacion, DetalleSolicitudNatural, DetalleSolicitudJuridica


# registro el modelo en el sitio de administración de Django.
@admin.register(SolicitudAfiliacion)
class SolicitudAfiliacionAdmin(admin.ModelAdmin):
    """
    Define la interfaz de administración para las Solicitudes de Afiliación.
    Aquí personalizo cómo se ven y se comportan las solicitudes en el panel de admin.
    """
    list_display = ("id", "solicitante", "estado", "fecha_creacion")

    list_filter = ("estado",)

    # Hago que las fechas de creación y modificación no se puedan editar a mano.
    # Django las maneja automáticamente.
    readonly_fields = ("fecha_creacion", "fecha_modificacion")

    autocomplete_fields = ("solicitante",)

    # Defino aquí en qué campos va a buscar la barra de búsqueda principal del admin.
    search_fields = (
        "solicitante__username",
        "solicitante__first_name",
        "solicitante__last_name",
        "solicitante__email",
        "detallesolicitudnatural__nombres", # Busco por el nombre de la persona natural.
        "detallesolicitudjuridica__razon_social", # O por la razón social de la persona jurídica.
    )

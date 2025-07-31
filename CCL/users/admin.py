from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Membresia, PerfilUsuario


# Para mostrar el PerfilUsuario dentro del formulario del Usuario (más intuitivo)
class PerfilUsuarioInline(admin.StackedInline):
    """
    Define un formulario 'inline' para el PerfilUsuario, que se mostrará
    en la página de edición del modelo User.
    """
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = _("Perfil del Usuario")
    fk_name = "usuario"


# Define un nuevo UserAdmin que incluye el perfil
class UserAdmin(BaseUserAdmin):
    """
    Extiende el UserAdmin base para incluir el PerfilUsuarioInline.
    """
    inlines = (PerfilUsuarioInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    """
    Define la interfaz de administración para el modelo Membresia.
    """
    list_display = ("numero_socio", "usuario", "estado", "fecha_ingreso")
    list_filter = ("estado", "fecha_ingreso")
    search_fields = ("numero_socio", "usuario__username", "usuario__first_name", "usuario__last_name")
    readonly_fields = ("fecha_creacion", "fecha_modificacion")
    autocomplete_fields = ("usuario", "solicitud_origen", "aprobado_por")

    fieldsets = (
        (_("Información Principal"), {
            "fields": ("usuario", "numero_socio", "estado", "fecha_ingreso")
        }),
        (_("Trazabilidad"), {
            "fields": ("solicitud_origen", "aprobado_por", "fecha_creacion", "fecha_modificacion"),
            "classes": ("collapse",)
        }),
    )


# Desregistra el UserAdmin base y registra la nueva versión con el inline
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

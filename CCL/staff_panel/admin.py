from django.contrib import admin

from staff_panel.models import ConfiguracionNotificacion


@admin.register(ConfiguracionNotificacion)
class ConfiguracionNotificacionAdmin(admin.ModelAdmin):
    list_display = ('codigo_evento', 'descripcion', 'esta_activa')
    list_editable = ('esta_activa',)

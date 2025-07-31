# Archivo: communications/admin.py

from django.contrib import admin
from .models import Notificacion


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('destinatario', 'verbo', 'objetivo', 'leida', 'timestamp')
    list_filter = ('leida', 'timestamp', 'content_type')
    search_fields = ('destinatario__username', 'verbo')
    readonly_fields = ('destinatario', 'actor', 'verbo', 'objetivo', 'timestamp')

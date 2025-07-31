from django import template
from communications.models import Notificacion

register = template.Library()


@register.simple_tag
def unread_notifications_count(user):
    """
    Retorna el número de notificaciones no leídas para un usuario.
    """
    if user.is_authenticated:
        return Notificacion.objects.filter(destinatario=user, leida=False).count()
    return 0

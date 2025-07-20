from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PerfilUsuario

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """
    Crea un PerfilUsuario automáticamente cuando se crea un nuevo User.
    """
    if created:
        PerfilUsuario.objects.create(usuario=instance)

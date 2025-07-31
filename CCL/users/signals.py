from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver

from communications.models import Notificacion
from .models import PerfilUsuario, Membresia

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crea un PerfilUsuario automáticamente cuando se crea un nuevo User."""
    if created:
        PerfilUsuario.objects.create(usuario=instance)


# --- SEÑAL AÑADIDA PARA LOGIN ---
@receiver(user_logged_in)
def notificar_inicio_sesion(sender, request, user, **kwargs):
    """Crea una notificación cuando un usuario inicia sesión."""
    Notificacion.objects.create(
        destinatario=user,
        verbo="Has iniciado sesión.",
        tipo=Notificacion.Tipo.SISTEMA
    )


# --- SEÑAL AÑADIDA PARA LOGOUT ---
@receiver(user_logged_out)
def notificar_cierre_sesion(sender, request, user, **kwargs):
    """Crea una notificación cuando un usuario cierra sesión."""
    if user:  # Asegurarse de que el usuario existe
        Notificacion.objects.create(
            destinatario=user,
            verbo="Has cerrado sesión.",
            tipo=Notificacion.Tipo.SISTEMA
        )


@receiver(post_save, sender=Membresia)
def notificar_creacion_membresia(sender, instance, created, **kwargs):
    """
    Notifica al usuario cuando su membresía ha sido creada oficialmente.
    """
    if created:
        membresia = instance
        verbo = f"¡Felicidades! Tu membresía ha sido activada con el número de socio: {membresia.numero_socio}."

        Notificacion.objects.create(
            destinatario=membresia.usuario,
            verbo=verbo,
            objetivo=membresia,
            tipo=Notificacion.Tipo.AFILIACION
        )

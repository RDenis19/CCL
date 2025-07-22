from django.db.models.signals import post_save
from django.dispatch import receiver

from communications.models import Notificacion
from .models import ComentarioNoticia


@receiver(post_save, sender=ComentarioNoticia)
def notificar_nuevo_comentario(sender, instance, created, **kwargs):
    """
    Notifica al autor de una noticia cuando se crea un nuevo comentario.
    """
    if created:
        comentario = instance
        noticia = comentario.noticia

        # Evitar que el autor se notifique a sí mismo
        if noticia.autor != comentario.autor:
            verbo = f"ha comentado en tu noticia: '{noticia.titulo}'"

            Notificacion.objects.create(
                destinatario=noticia.autor,
                actor=comentario.autor,
                verbo=verbo,
                objetivo=comentario,
                tipo=Notificacion.Tipo.CONTENIDO
            )

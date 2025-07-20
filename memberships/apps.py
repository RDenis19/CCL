# Archivo: memberships/apps.py

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MembershipsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'memberships'
    verbose_name = _("Gestión de Afiliaciones")

    def ready(self):
        """
        Importa las señales de esta aplicación cuando Django está listo.

        Este es el metodo oficial para registrar las señales y asegurar
        que estén conectadas cuando la aplicación se inicie.
        """
        try:
            import memberships.signals
        except ImportError:
            pass

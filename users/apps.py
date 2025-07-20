from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = _("Gestión de Usuarios y Membresías")

    def ready(self):
        """
        Importa las señales cuando la aplicación está lista.
        """
        try:
            import users.signals
        except ImportError:
            pass
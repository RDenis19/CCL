from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class MembershipsConfig(AppConfig):
    # Configuración estándar para el tipo de clave primaria (ID) que Django creará automáticamente en los modelos.
    default_auto_field = 'django.db.models.BigAutoField'

    name = 'memberships'
    
    # Este es el nombre "bonito" y legible que se mostrará en el panel de administración
    verbose_name = _("Gestión de Afiliaciones")

    def ready(self):
        """
        Este método especial se ejecuta automáticamente en cuanto Django
        termina de cargar la aplicación. 
        """
        # Aquí le digo a Django que cargue mi archivo de señales (signals.py).
        # Esto asegura que las funciones que deben ejecutarse ante ciertos eventos
        # (como después de guardar un modelo) estén listas para funcionar.
        try:
            import memberships.signals
        except ImportError:
            # Envuelvo la importación en un try/except por si el archivo
            # signals.py no existe. Así evito que la aplicación se rompa.
            pass
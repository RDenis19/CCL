# Archivo: ccl/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # --- Panel de Administración ---
    path('admin/', admin.site.urls),

    # --- Aplicaciones Principales ---
    path('', include('core.urls', namespace='home')),
    path('usuarios/', include('users.urls', namespace='users')),
    path('afiliacion/', include('memberships.urls', namespace='memberships')),
    path('servicios/', include('services.urls', namespace='services')),
    path('noticias/', include('content.urls', namespace='content')),
    path('notificaciones/', include('communications.urls', namespace='communications')),
    path('staff/', include('staff_panel.urls', namespace='staff_panel')),
    path('', RedirectView.as_view(pattern_name='users:dashboard', permanent=False), name='home'),
]

# --- Servir archivos de medios en Desarrollo ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

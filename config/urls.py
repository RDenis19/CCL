from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('usuarios/', include('users.urls', namespace='users')),
    path('afiliacion/', include('memberships.urls', namespace='memberships')),
    path('servicios/', include('services.urls', namespace='services')),
    path('noticias/', include('content.urls', namespace='content')),
    path('notificaciones/', include('communications.urls', namespace='communications')),
    path('staff/', include('staff_panel.urls', namespace='staff_panel')),
]

# --- Servir Archivos de Medios en Desarrollo ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
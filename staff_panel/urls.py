from django.urls import path
from . import views

app_name = 'staff_panel'

urlpatterns = [
    path('', views.dashboard_staff_view, name='dashboard'),
    path('solicitudes/afiliacion/', views.solicitud_afiliacion_list_view, name='solicitud-afiliacion-list'),
    path(
        'solicitudes/afiliacion/<int:pk>/',
        views.solicitud_afiliacion_manage_view,
        name='solicitud-afiliacion-manage'
    ),
    # --- RUTAS GESTIÓN DE SERVICIOS ---
    path(
        'solicitudes/servicios/',
        views.solicitud_servicio_list_view,
        name='solicitud-servicio-list'
    ),
    path(
        'solicitudes/servicios/<uuid:pk>/',
        views.solicitud_servicio_manage_view,
        name='solicitud-servicio-manage'
    ),
]

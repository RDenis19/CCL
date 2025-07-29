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

    # --- RUTAS AÑADIDAS PARA GESTIÓN DE NOTICIAS ---
    path('noticias/', views.noticia_list_view, name='noticia-list'),
    path('noticias/crear/', views.noticia_create_view, name='noticia-create'),
    path('noticias/<int:pk>/editar/', views.noticia_update_view, name='noticia-update'),

    # --- Gestión de Catálogo de Servicios ---
    path('servicios/', views.servicio_list_staff_view, name='servicio-list-staff'),
    path('servicios/crear/', views.servicio_manage_view, name='servicio-create'),
    path('servicios/<int:pk>/editar/', views.servicio_manage_view, name='servicio-edit'),
    path('servicios/<int:pk>/recursos/', views.servicio_detail_staff_view, name='servicio-detail-staff'),
    path('servicios/<int:servicio_pk>/recursos/crear/', views.recurso_manage_view, name='recurso-create'),
    path('recursos/<int:pk>/editar/', views.recurso_manage_view, name='recurso-edit'),
    path('pagos/pendientes/', views.pago_list_view, name='pago-list'),
    path('pagos/<uuid:pk>/gestionar/', views.pago_manage_view, name='pago-manage'),
]

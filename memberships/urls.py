from django.urls import path
from . import views

app_name = 'memberships'

urlpatterns = [
    # URL para crear, que acepta el tipo de solicitante
    path(
        'solicitud/crear/<str:tipo_solicitante>/',
        views.solicitud_create_view,
        name='solicitud-create'
    ),
    # URL para ver los detalles de la solicitud
    path(
        'solicitud/detalle/',
        views.solicitud_detail_view,
        name='solicitud-detail'
    ),
    path('solicitud/iniciar/', views.solicitud_selector_view, name='solicitud-selector'),
]

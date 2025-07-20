# Archivo: services/urls.py

from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Lista de todos los servicios
    path('catalogo/', views.servicio_list_view, name='servicio-list'),

    # Detalle de un servicio específico
    path('catalogo/<int:pk>/', views.servicio_detail_view, name='servicio-detail'),

    # Crear una solicitud para un recurso (sin horario específico)
    path(
        'recurso/<int:recurso_pk>/solicitar/',
        views.solicitud_create_view,
        name='solicitud-create'
    ),

    # Crear una solicitud para un recurso (con horario específico, una reserva)
    path(
        'recurso/<int:recurso_pk>/reservar/<int:horario_pk>/',
        views.solicitud_create_view,
        name='reserva-create'
    ),
    # --- URL para Convenios y Beneficios ---
    path('convenios/', views.convenio_list_view, name='convenio-list'),
    path('convenios/<int:pk>/', views.convenio_detail_view, name='convenio-detail'),
    path('mis-solicitudes/', views.mis_solicitudes_view, name='mis-solicitudes'),

    # --- RUTAS PARA CALENDARIO ---
    path('recurso/<int:pk>/calendario/', views.recurso_detail_view, name='recurso-detail'),
    path('recurso/<int:pk>/eventos/', views.recurso_eventos_json, name='recurso-eventos-json'),
]

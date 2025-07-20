# Archivo: communications/urls.py

from django.urls import path
from . import views

app_name = 'communications'

urlpatterns = [
    path('', views.notificacion_list_view, name='notificacion-list'),
    path('<int:pk>/leer/', views.marcar_como_leida_view, name='marcar-como-leida'),
    path('leer-todas/', views.marcar_todas_como_leidas_view, name='marcar-todas-como-leidas'),
]

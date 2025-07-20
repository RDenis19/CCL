# Archivo: content/urls.py

from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('noticias/', views.noticia_list_view, name='noticia-list'),
    path('noticias/<slug:slug>/', views.noticia_detail_view, name='noticia-detail'),
]

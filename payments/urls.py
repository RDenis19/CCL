# Archivo: payments/urls.py
from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('upload/<uuid:solicitud_id>/', views.upload_comprobante_view, name='upload_comprobante'),
]

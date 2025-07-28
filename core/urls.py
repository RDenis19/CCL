from django.urls import path
from . import views
from .views import NosotrosView

app_name = 'core'

urlpatterns = [
    path('', views.landing_page_view, name='home'),
    path('nosotros/', NosotrosView.as_view(), name='nosotros'),
    path('contacto/', views.contacto_view, name='contacto'),
]


# Archivo: users/urls.py

from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # Vistas de Panel y Perfil
    path('panel/', views.dashboard_view, name='dashboard'),
    path('perfil/', views.perfil_detail_view, name='perfil-detail'),
    path('perfil/editar/', views.perfil_update_view, name='perfil-update'),
    path('registro/', views.registro_view, name='registro'),

    # Vistas de Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Vistas de Cambio de Contraseña
    path(
        'password/change/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/password_change_form.html',
            success_url=reverse_lazy('users:password_change_done')  # CORREGIDO
        ),
        name='password_change'
    ),
    path(
        'password/change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
        name='password_change_done'
    ),

    # Vistas de Reseteo de Contraseña
    path(
        'password/reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset_form.html',
            email_template_name='users/password_reset_email.html',
            success_url=reverse_lazy('users:password_reset_done')  # CORREGIDO
        ),
        name='password_reset'
    ),
    path(
        'password/reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complete')  # CORREGIDO
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]

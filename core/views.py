from django.shortcuts import render


def landing_page_view(request):
    """
    Renderiza la página de inicio principal (landing page) del sitio.
    """
    # Si el usuario ya está autenticado, lo redirigimos a su panel
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('users:dashboard')

    return render(request, 'core/landing_page.html')

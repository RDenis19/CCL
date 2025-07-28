from django.shortcuts import render, redirect
from django.views.generic import TemplateView

def landing_page_view(request):
    """
    Renderiza la página de inicio principal (landing page) del sitio.
    """
    # Si el usuario ya está autenticado, lo redirigimos a su panel
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('users:dashboard')

    return render(request, 'core/landing_page.html')

def contacto_view(request):
    """
    Renderiza la página de contacto.
    """
    # Aquí podrías añadir la lógica para procesar el formulario en el futuro
    context = {
        'page_title': 'Contacto'
    }
    return render(request, 'core/contacto.html', context)

class NosotrosView(TemplateView):
    template_name = "nosotros.html"

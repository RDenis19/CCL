from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import PerfilUsuario


class PerfilUsuarioUpdateForm(forms.ModelForm):
    """
    Formulario para que los usuarios actualicen su perfil.

    Se encarga de la validación y renderización de los campos editables
    del modelo PerfilUsuario.
    """

    class Meta:
        model = PerfilUsuario
        fields = ["avatar", "biografia", "redes_sociales"]
        help_texts = {
            'biografia': _("Escribe una breve descripción sobre ti."),
            'redes_sociales': _("Añade enlaces a tus redes sociales en formato JSON."),
        }

    def __init__(self, *args, **kwargs):
        """
        Añade clases de Bootstrap a los campos del formulario para un
        diseño consistente con Argon.
        """
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['biografia'].widget.attrs.update({'class': 'form-control', 'rows': '4'})
        # Los campos JSON no tienen un widget simple, se renderizarán como un textarea.
        self.fields['redes_sociales'].widget.attrs.update({
            'class': 'form-control',
            'rows': '3',
            'placeholder': '{\n  "twitter": "https://twitter.com/tu_usuario",\n  "linkedin": "..."\n}'
        })


class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")

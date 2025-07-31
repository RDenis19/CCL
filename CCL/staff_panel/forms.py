from django import forms
from django.utils.translation import gettext_lazy as _

from content.models import Noticia, CategoriaNoticia
from services.models import Servicio, RecursoServicio


class NoticiaForm(forms.ModelForm):
    """
    Formulario para la creación y edición de noticias, con lógica
    integrada para crear una nueva categoría al vuelo.
    """
    nueva_categoria = forms.CharField(
        label=_("O crea una nueva categoría"),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la nueva categoría'}),
    )

    class Meta:
        model = Noticia
        fields = ['titulo', 'categoria', 'estado', 'contenido', 'slug']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: nueva-alianza-con-empresa'}),
        }
        help_texts = {
            'slug': _("Este es el texto que aparecerá en la URL. Usa solo letras, números y guiones."),
        }

    def __init__(self, *args, **kwargs):
        """
        Hacemos que el campo 'categoria' no sea requerido a nivel de HTML,
        porque nuestra lógica personalizada en clean() se encargará de la validación.
        """
        super().__init__(*args, **kwargs)
        self.fields['categoria'].required = False

    def clean(self):
        """
        Aquí reside la lógica de validación principal.
        """
        cleaned_data = super().clean()
        categoria_existente = cleaned_data.get('categoria')
        nombre_nueva_categoria = cleaned_data.get('nueva_categoria')

        # Escenario 1: El usuario no seleccionó ni escribió nada.
        if not categoria_existente and not nombre_nueva_categoria:
            raise forms.ValidationError(
                _("Debes seleccionar una categoría existente o proporcionar el nombre para una nueva."),
                code='categoria_requerida'
            )

        # Escenario 2: El usuario seleccionó Y escribió. Es ambiguo.
        if categoria_existente and nombre_nueva_categoria:
            raise forms.ValidationError(
                _("Por favor, selecciona una categoría existente o crea una nueva, pero no ambas."),
                code='seleccion_ambigua'
            )

        # Validación para evitar duplicados en la nueva categoría
        if nombre_nueva_categoria and CategoriaNoticia.objects.filter(nombre__iexact=nombre_nueva_categoria).exists():
            self.add_error('nueva_categoria', _("Una categoría con este nombre ya existe."))

        return cleaned_data


class ServicioForm(forms.ModelForm):
    """Formulario para crear y editar un Servicio principal."""

    class Meta:
        model = Servicio
        fields = ['nombre', 'categoria', 'descripcion', 'precio', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RecursoServicioForm(forms.ModelForm):
    """Formulario para crear y editar un Recurso de un Servicio."""

    class Meta:
        model = RecursoServicio
        fields = ['nombre', 'tipo', 'responsable']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
        }

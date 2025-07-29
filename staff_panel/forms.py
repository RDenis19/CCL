from django import forms
from django.utils.translation import gettext_lazy as _

from content.models import Noticia
from services.models import Servicio, RecursoServicio


class NoticiaForm(forms.ModelForm):
    """
    Formulario para la creación y edición de noticias por parte del personal.
    """

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

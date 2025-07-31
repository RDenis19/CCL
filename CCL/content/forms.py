from django import forms

from .models import ComentarioNoticia


class ComentarioNoticiaForm(forms.ModelForm):
    """Formulario para que un usuario cree un comentario en una noticia."""

    class Meta:
        model = ComentarioNoticia
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe tu comentario aquí...'
            })
        }
        labels = {
            'contenido': ''
        }

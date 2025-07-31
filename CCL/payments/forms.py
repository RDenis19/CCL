# Archivo: payments/forms.py
from django import forms

from .models import Pago


# Un ModelForm se crea directamente a partir de un modelo de Django.
class ComprobantePagoForm(forms.ModelForm):
    """Formulario para que un usuario suba su comprobante de pago."""

    # La clase Meta conecta el formulario con un modelo y permite personalizar sus campos.
    class Meta:
        # Le digo al formulario que se base en mi modelo 'Pago'.
        model = Pago
        fields = ['comprobante']
        
        # Aquí personalizo cómo se ven los campos en el HTML.
        widgets = {
            'comprobante': forms.ClearableFileInput(attrs={
                # Le pongo una clase de Bootstrap para que se vea bien.
                'class': 'form-control',
            })
        }
        labels = {
            'comprobante': ''
        }
        help_texts = {
            'comprobante': 'Sube una imagen o PDF de tu comprobante de pago.'
        }

    # Uso el método __init__ para hacer modificaciones extra al formulario después de que se crea.
    def __init__(self, *args, **kwargs):
        # Es importante llamar primero al constructor de la clase padre.
        super().__init__(*args, **kwargs)
        # Hago que el campo del comprobante sea obligatorio en este formulario,
        # sin importar si en el modelo está marcado como opcional.
        self.fields['comprobante'].required = True
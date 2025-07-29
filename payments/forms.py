# Archivo: payments/forms.py
from django import forms

from .models import Pago


class ComprobantePagoForm(forms.ModelForm):
    """Formulario para que un usuario suba su comprobante de pago."""

    class Meta:
        model = Pago
        fields = ['comprobante']
        widgets = {
            'comprobante': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            })
        }
        labels = {
            'comprobante': ''
        }
        help_texts = {
            'comprobante': 'Sube una imagen o PDF de tu comprobante de pago.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comprobante'].required = True

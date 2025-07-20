from django import forms
from django.utils.translation import gettext_lazy as _

from .models import DetalleSolicitudNatural, DetalleSolicitudJuridica, BeneficiarioPoliza


class DetalleSolicitudNaturalForm(forms.ModelForm):
    """Formulario para los detalles de una solicitud de persona natural."""

    class Meta:
        model = DetalleSolicitudNatural
        # Excluimos la solicitud porque se asignará automáticamente en la vista.
        exclude = ('solicitud',)


class DetalleSolicitudJuridicaForm(forms.ModelForm):
    """Formulario para los detalles de una solicitud de persona jurídica."""

    class Meta:
        model = DetalleSolicitudJuridica
        exclude = ('solicitud',)


# FormSet para manejar múltiples beneficiarios en el mismo formulario de solicitud.
BeneficiarioPolizaFormSet = forms.inlineformset_factory(
    parent_model=DetalleSolicitudNatural,
    model=BeneficiarioPoliza,
    fields=('nombre_completo', 'porcentaje'),
    extra=1,  # Muestra un formulario de beneficiario por defecto.
    can_delete=True,
    widgets={
        'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
        'porcentaje': forms.NumberInput(attrs={'class': 'form-control'}),
    }
)

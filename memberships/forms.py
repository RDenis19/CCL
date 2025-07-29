from django import forms

from .models import DetalleSolicitudNatural, DetalleSolicitudJuridica, BeneficiarioPoliza, DocumentoAdjunto, \
    SolicitudAfiliacion


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


class DocumentoAdjuntoForm(forms.ModelForm):
    """Formulario para un único documento adjunto."""

    class Meta:
        model = DocumentoAdjunto
        fields = ['nombre_documento', 'archivo']
        widgets = {
            'nombre_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Copia de Cédula'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# Usamos un formset para permitir al usuario subir múltiples documentos
DocumentoAdjuntoFormSet = forms.inlineformset_factory(
    parent_model=SolicitudAfiliacion,
    model=DocumentoAdjunto,
    form=DocumentoAdjuntoForm,
    fields=('nombre_documento', 'archivo'),
    extra=1,  # Muestra un formulario de documento por defecto.
    can_delete=True,
)

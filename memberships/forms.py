from django import forms
from django.utils.translation import gettext_lazy as _

from .models import DetalleSolicitudNatural, DetalleSolicitudJuridica, BeneficiarioPoliza, DocumentoAdjunto, \
    SolicitudAfiliacion


class DetalleSolicitudNaturalForm(forms.ModelForm):
    """Formulario para los detalles de una solicitud de persona natural."""

    class Meta:
        model = DetalleSolicitudNatural
        fields = ['cedula', 'direccion', 'celular']

    def clean_cedula(self):
        """
        Vlida que la cédula no pertenezca a una membresía activa
        o a una solicitud en proceso.
        """
        cedula = self.cleaned_data.get('cedula')

        # Definimos los estados que consideramos "activos" o "en proceso"
        estados_activos = [
            SolicitudAfiliacion.Estado.PENDIENTE,
            SolicitudAfiliacion.Estado.EN_REVISION,
            SolicitudAfiliacion.Estado.APROBADA,
        ]

        # Buscamos si existe algún detalle con esta cédula cuya solicitud
        # esté en uno de los estados activos.
        if DetalleSolicitudNatural.objects.filter(
                cedula=cedula,
                solicitud__estado__in=estados_activos
        ).exists():
            raise forms.ValidationError(
                _("Ya existe una solicitud activa o en proceso con este número de cédula.")
            )

        return cedula


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

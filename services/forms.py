# Archivo: services/forms.py

from django import forms
from .models import SolicitudServicio, HorarioDisponible
from django.utils.translation import gettext_lazy as _


class SolicitudServicioForm(forms.ModelForm):
    """Formulario para que un usuario cree una solicitud de servicio o reserva."""

    class Meta:
        model = SolicitudServicio
        fields = ['notas_usuario']  # El resto de campos se asignan en la vista
        widgets = {
            'notas_usuario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Añade cualquier detalle o pregunta sobre tu solicitud aquí...'
            })
        }


class RespuestaSolicitudForm(forms.Form):
    respuesta = forms.CharField(
        label=_("Respuesta para el socio (opcional)"),
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        required=False
    )


class HorarioDisponibleForm(forms.ModelForm):
    """Formulario para crear un nuevo bloque de horario disponible."""

    # Usamos SplitDateTimeWidget para tener campos separados para fecha y hora
    fecha_hora_inicio = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(date_attrs={'type': 'date'}, time_attrs={'type': 'time'}))
    fecha_hora_fin = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(date_attrs={'type': 'date'}, time_attrs={'type': 'time'}))

    class Meta:
        model = HorarioDisponible
        fields = ['fecha_hora_inicio', 'fecha_hora_fin']

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get("fecha_hora_inicio")
        fin = cleaned_data.get("fecha_hora_fin")

        if inicio and fin and inicio >= fin:
            raise forms.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")

        return cleaned_data

# reservas/forms.py
from django import forms
from .models import Reserva, Comentario


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['vehiculo', 'conductor', 'fecha_inicio', 'fecha_fin', 'trayecto', 'metodo_pago']


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nombre', 'correo', 'mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 4}),
        }


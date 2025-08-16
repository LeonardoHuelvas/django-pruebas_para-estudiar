from django import forms
from core.models import Pregunta

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ["texto", "tipo", "eje"]

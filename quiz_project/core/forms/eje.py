from django import forms
from core.models import EjeTematico

class EjeForm(forms.ModelForm):
    class Meta:
        model = EjeTematico
        fields = ['nombre', 'quiz']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'quiz': forms.Select(attrs={'class': 'form-control'}),
        }
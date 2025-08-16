from django import forms
from core.models import Quiz

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["nombre", "descripcion"]


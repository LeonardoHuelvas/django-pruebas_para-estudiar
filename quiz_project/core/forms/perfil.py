from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from core.models import PerfilUsuario


# ---------- Formulario de registro ----------
class CustomUserCreationForm(UserCreationForm):
    foto = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'foto']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Si el perfil no existe, lo crea; si existe, no lanza error
            perfil, created = PerfilUsuario.objects.get_or_create(
                user=user,
                defaults={'rol': 'estudiante'}  # Rol por defecto
            )
            foto = self.cleaned_data.get('foto')
            if foto:
                perfil.foto = foto
                perfil.save(update_fields=['foto'])
        return user


# ---------- Formulario de edición de perfil ----------
class PerfilUsuarioUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PerfilUsuario
        fields = ['foto']
        widgets = {
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self._user:
            self.fields['username'].initial = self._user.username
            self.fields['email'].initial = self._user.email

    @transaction.atomic
    def save(self, commit=True):
        perfil = super().save(commit=False)

        # Actualiza también los datos del usuario
        if self._user:
            self._user.username = self.cleaned_data['username']
            self._user.email = self.cleaned_data['email']
            self._user.save(update_fields=['username', 'email'])

        if commit:
            perfil.save()
        return perfil

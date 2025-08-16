# core/views/auth.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from core.forms.perfil import CustomUserCreationForm
 
from ..models import PerfilUsuario

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenido/a {user.username}")
            return redirect('core:dashboard')
        else:
            messages.error(request, "Credenciales inválidas.")
    else:
        form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Rol por defecto estudiante
            PerfilUsuario.objects.create(user=user, rol='estudiante')
            login(request, user)
            messages.success(request, "Registro exitoso.")
            return redirect('core:dashboard')
        else:
            messages.error(request, "Verifica los errores en el formulario.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'login/register.html', {'form': form})

@login_required
def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return redirect(reverse('core:login'))

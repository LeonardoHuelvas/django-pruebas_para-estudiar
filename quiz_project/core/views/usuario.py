# core/views/usuario.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import CustomUserCreationForm, PerfilUsuarioUpdateForm
from core.models import PerfilUsuario


# ---------- Crear usuario (solo superuser) ----------
@login_required
@user_passes_test(lambda u: u.is_superuser)
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # El form crea o asegura PerfilUsuario (rol 'estudiante')
            messages.success(request, f"Usuario {user.username} creado correctamente.")
            return redirect('core:gestionar_roles')
    else:
        form = CustomUserCreationForm()

    return render(request, 'usuario/crear_usuario.html', {'form': form})


# ---------- Editar mi perfil (usuario autenticado) ----------
@login_required
def gestionar_perfil(request):
    perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PerfilUsuarioUpdateForm(
            request.POST, request.FILES,
            instance=perfil, user=request.user
        )
        if form.is_valid():
            form.save()  # guarda foto y actualiza username/email
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('core:gestionar_perfil')
    else:
        form = PerfilUsuarioUpdateForm(instance=perfil, user=request.user)

    return render(request, 'usuario/perfil.html', {'form': form, 'perfil': perfil})


# ---------- Asignar roles (solo superuser) ----------
@login_required
@user_passes_test(lambda u: u.is_superuser)
def gestionar_roles(request):
    usuarios = User.objects.exclude(is_superuser=True)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        nuevo_rol = request.POST.get('rol')

        user = get_object_or_404(User, id=user_id)
        perfil, _ = PerfilUsuario.objects.get_or_create(user=user)
        perfil.rol = nuevo_rol
        perfil.save(update_fields=['rol'])

        messages.success(request, f"Rol de {user.username} actualizado a {nuevo_rol}.")
        return redirect('core:gestionar_roles')

    return render(request, 'usuario/gestionar_roles.html', {'usuarios': usuarios})

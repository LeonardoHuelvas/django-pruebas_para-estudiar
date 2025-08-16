from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class RolRequeridoMixin(LoginRequiredMixin, UserPassesTestMixin):
    rol_requerido = None  # 'admin' o 'estudiante'

    def test_func(self):
        return self.request.user.is_authenticated and \
               self.request.user.perfilusuario.rol == self.rol_requerido

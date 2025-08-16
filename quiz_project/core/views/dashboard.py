from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from core.models import Quiz, Resultado

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'home/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        perfil = getattr(user, 'perfilusuario', None)
        rol = getattr(perfil, 'rol', 'estudiante')

        context["total_quices"] = Quiz.objects.count()
        context["quices_recientes"] = Quiz.objects.order_by('-id')[:5]
        context["rol"] = "Administrador" if rol == "admin" else "Estudiante"

        if rol == 'admin':
            context["total_resultados"] = Resultado.objects.count()
            context["resultados_recientes"] = Resultado.objects.select_related('quiz', 'usuario').order_by('-fecha')[:10]
        else:
            context["total_resultados"] = Resultado.objects.filter(usuario=user).count()
            context["mis_resultados"] = Resultado.objects.filter(usuario=user).select_related('quiz').order_by('-fecha')

        return context

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin

class StaffRequiredMixin(LoginRequiredMixin):
    """Ejemplo de autorización simple para administración del banco."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("No autorizado.")
        return super().dispatch(request, *args, **kwargs)

class BreadcrumbsMixin(ContextMixin):
    breadcrumbs = []  # [("Quices", reverse("core:quiz_list")), ...]
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["breadcrumbs"] = self.breadcrumbs
        return ctx

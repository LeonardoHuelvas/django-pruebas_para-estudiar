from django.urls import reverse
from core.models import EjeTematico, Quiz
from core.forms.eje import EjeForm  # crea este ModelForm igual que QuizForm
from core.views.base import BaseListView, BaseDetailView, BaseCreateView, BaseUpdateView, BaseDeleteView, success_url_to
from core.views.mixins import StaffRequiredMixin, BreadcrumbsMixin

class EjeListView(BreadcrumbsMixin, BaseListView):
    model = EjeTematico
    template_name = "eje/list.html"
    def get_queryset(self):
        return EjeTematico.objects.select_related("quiz").order_by("quiz__nombre","nombre")

class EjeDetailView(BreadcrumbsMixin, BaseDetailView):
    model = EjeTematico
    template_name = "eje/detail.html"
    def get_breadcrumbs(self):
        obj = self.get_object()
        return [("Quices", reverse("core:quiz_list")), (obj.quiz.nombre, reverse("core:quiz_detail", args=[obj.quiz_id])), (obj.nombre, None)]

class EjeCreateView(StaffRequiredMixin, BreadcrumbsMixin, BaseCreateView):
    model = EjeTematico
    form_class = EjeForm
    template_name = "eje/form.html"
    success_url = success_url_to("core:eje_list")

class EjeUpdateView(StaffRequiredMixin, BreadcrumbsMixin, BaseUpdateView):
    model = EjeTematico
    form_class = EjeForm
    template_name = "eje/form.html"
    success_url = success_url_to("core:eje_list")

class EjeDeleteView(StaffRequiredMixin, BreadcrumbsMixin, BaseDeleteView):
    model = EjeTematico
    template_name = "eje/confirm_delete.html"
    success_url = success_url_to("core:eje_list")

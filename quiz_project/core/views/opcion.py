from core.models import Opcion
from django import forms
from core.views.base import BaseCreateView, BaseUpdateView, BaseDeleteView, success_url_to
from core.views.mixins import StaffRequiredMixin

class OpcionForm(forms.ModelForm):
    class Meta:
        model = Opcion
        fields = ["pregunta", "texto", "es_correcta"]

class OpcionCreateView(StaffRequiredMixin, BaseCreateView):
    model = Opcion
    form_class = OpcionForm
    template_name = "opcion/form.html"
    success_url = success_url_to("core:pregunta_list")

class OpcionUpdateView(StaffRequiredMixin, BaseUpdateView):
    model = Opcion
    form_class = OpcionForm
    template_name = "opcion/form.html"
    success_url = success_url_to("core:pregunta_list")

class OpcionDeleteView(StaffRequiredMixin, BaseDeleteView):
    model = Opcion
    template_name = "opcion/confirm_delete.html"
    success_url = success_url_to("core:pregunta_list")

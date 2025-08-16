# views.py

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from core.models import Pregunta, EjeTematico, Opcion
from core.forms.pregunta import PreguntaForm
from core.views.base import BaseListView, BaseDetailView, BaseCreateView, BaseUpdateView, BaseDeleteView, success_url_to
from core.views.mixins import StaffRequiredMixin, BreadcrumbsMixin
from core.selectors.pregunta import list_preguntas_by_eje
from core.services.pregunta import crear_pregunta_unica
from django.contrib import messages
import json

class PreguntaListView(BreadcrumbsMixin, BaseListView):
    model = Pregunta
    template_name = "pregunta/list.html"
    def get_queryset(self):
        eje_id = self.kwargs.get("eje_id")
        return list_preguntas_by_eje(eje_id) if eje_id else Pregunta.objects.select_related("eje","eje__quiz")
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.kwargs.get("eje_id"):
            ctx["eje"] = EjeTematico.objects.select_related("quiz").get(pk=self.kwargs["eje_id"])
        return ctx

class PreguntaDetailView(BreadcrumbsMixin, BaseDetailView):
    model = Pregunta
    template_name = "pregunta/detail.html"
    def get_queryset(self):
        return Pregunta.objects.select_related("eje","eje__quiz").prefetch_related("opciones")

class PreguntaCreateView(StaffRequiredMixin, BreadcrumbsMixin, BaseCreateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = "pregunta/form.html"
    def form_valid(self, form):
        # Si viene tipo UNICA y el form incluyera opciones desde el POST, podrías llamar al service.
        if form.cleaned_data["tipo"] == "UNICA" and self.request.POST.getlist("op_texto"):
            opciones = list(zip(self.request.POST.getlist("op_texto"),
                                [v == "on" for v in self.request.POST.getlist("op_correcta")]))
            crear_pregunta_unica(form.cleaned_data["eje"].id, form.cleaned_data["texto"], opciones)
            return redirect("core:pregunta_list")
        return super().form_valid(form)
    def get_success_url(self):
        return reverse("core:pregunta_list")

class PreguntaUpdateView(StaffRequiredMixin, BreadcrumbsMixin, BaseUpdateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = "pregunta/form.html"
    success_url = success_url_to("core:pregunta_list")

class PreguntaDeleteView(StaffRequiredMixin, BreadcrumbsMixin, BaseDeleteView):
    model = Pregunta
    template_name = "pregunta/confirm_delete.html"
    success_url = success_url_to("core:pregunta_list")
    
@login_required
def importar_preguntas_view(request):
    if request.method == 'POST':
        eje_id = request.POST.get('eje_id')
        archivo = request.FILES.get('archivo_json')
        
        if not archivo or not archivo.name.endswith('.json'):
            messages.error(request, "Archivo no válido. Solo se aceptan archivos .json")
            return redirect("core:importar_preguntas")
        
        try:
            data = json.load(archivo)
            eje = EjeTematico.objects.get(pk=eje_id)
            creadas = 0
            errores = 0
            
            for item in data:
                try:
                    texto = item["enunciado"]
                    tipo = item["tipo"]
                    opciones = item["opciones"]
                    respuesta_correcta = item["respuesta_correcta"]
                    
                    pregunta = Pregunta.objects.create(
                        texto=texto,
                        tipo=tipo,
                        eje=eje
                    )
                    
                    # Normalizar la respuesta correcta para preguntas VF
                    if tipo == "VF":
                        respuesta_correcta_normalizada = normalizar_respuesta_vf(respuesta_correcta)
                    else:
                        respuesta_correcta_normalizada = respuesta_correcta.strip()
                    
                    for opcion_texto in opciones:
                        if tipo == "VF":
                            opcion_normalizada = normalizar_respuesta_vf(opcion_texto)
                            es_correcta = (opcion_normalizada == respuesta_correcta_normalizada)
                        else:
                            es_correcta = (opcion_texto.strip().lower() == respuesta_correcta_normalizada.lower())
                        
                        Opcion.objects.create(
                            texto=opcion_texto,
                            es_correcta=es_correcta,
                            pregunta=pregunta
                        )
                    
                    creadas += 1
                    
                except KeyError as e:
                    errores += 1
                    messages.error(request, f"Error al importar: campo faltante {e} en una pregunta.")
                    
            messages.success(request, f"{creadas} preguntas importadas correctamente.")
            if errores:
                messages.warning(request, f"{errores} preguntas no fueron importadas por errores de formato.")
            return redirect("core:importar_preguntas")
            
        except Exception as e:
            messages.error(request, f"Ocurrió un error al procesar el archivo: {e}")
            return redirect("core:importar_preguntas")
    
    ejes = EjeTematico.objects.all()
    return render(request, "pregunta/importar_masivo.html", {"ejes": ejes})

def normalizar_respuesta_vf(respuesta):
    """
    Normaliza las respuestas de Verdadero/Falso para comparación consistente
    """
    respuesta = respuesta.strip().lower()
    
    # Mapeo de posibles valores a estándar
    verdadero_valores = ['verdadero', 'true', 'v', 'si', 'sí', '1']
    falso_valores = ['falso', 'false', 'f', 'no', '0']
    
    if respuesta in verdadero_valores:
        return 'verdadero'
    elif respuesta in falso_valores:
        return 'falso'
    else:
        return respuesta  # Devolver original si no coincide


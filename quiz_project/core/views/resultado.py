from core.models import Resultado
from core.views.base import BaseListView, BaseDetailView
from core.services.resultado import top_n_por_quiz
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,  get_object_or_404

class ResultadoListView(BaseListView):
    model = Resultado
    template_name = "resultado/list.html"
    ordering = ["-fecha"]

class ResultadoDetailView(BaseDetailView):
    model = Resultado
    template_name = "resultado/detail.html"

class RankingPorQuizView(BaseListView):
    template_name = "resultado/list.html"
    def get_queryset(self):
        return top_n_por_quiz(self.kwargs["quiz_id"], n=20)


@login_required
def detalle_resultado_view(request, resultado_id):
    resultado = get_object_or_404(Resultado, id=resultado_id, usuario=request.user)

    respuestas = resultado.respuestas.select_related("pregunta", "opcion_seleccionada").all()

    # Agrupar datos por pregunta
    detalle = []
    for respuesta in respuestas:
        correctas = respuesta.pregunta.opciones.filter(es_correcta=True)
        detalle.append({
            "pregunta": respuesta.pregunta,
            "opcion_seleccionada": respuesta.opcion_seleccionada,
            "opciones": respuesta.pregunta.opciones.all(),
            "correctas": correctas,
            "es_correcta": respuesta.opcion_seleccionada in correctas
        })

    return render(request, "resultado/detalle_resultado.html", {
        "resultado": resultado,
        "detalle": detalle
    })

from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import EjeTematico, Pregunta, Opcion, Resultado, RespuestaUsuario, Quiz
from core.forms.quiz import QuizForm
from core.views.base import (
    BaseListView, BaseDetailView, BaseCreateView,
    BaseUpdateView, BaseDeleteView, success_url_to
)
from core.views.mixins import StaffRequiredMixin, BreadcrumbsMixin
from core.selectors.quiz import list_quices, get_quiz_with_ejes
import random


class QuizListView(BreadcrumbsMixin, BaseListView):
    model = Quiz
    template_name = "quiz/list.html"
    paginate_by = 20

    def get_queryset(self):
        return list_quices()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ejes'] = EjeTematico.objects.all()  # Para el modal
        return context

    breadcrumbs = [("Quices", None)]


class QuizDetailView(BreadcrumbsMixin, BaseDetailView):
    model = Quiz
    template_name = "quiz/detail.html"

    def get_object(self, queryset=None):
        return get_quiz_with_ejes(self.kwargs["pk"])

    def get_breadcrumbs(self):
        return [
            ("Quices", reverse_lazy("core:quiz_list")),
            (self.object.nombre, None)
        ]


class QuizCreateView(StaffRequiredMixin, BreadcrumbsMixin, BaseCreateView):
    model = Quiz
    form_class = QuizForm
    template_name = "quiz/form.html"
    success_url = success_url_to("core:quiz_list")
    breadcrumbs = [("Quices", reverse_lazy("core:quiz_list")), ("Crear", None)]


class QuizUpdateView(StaffRequiredMixin, BreadcrumbsMixin, BaseUpdateView):
    model = Quiz
    form_class = QuizForm
    template_name = "quiz/form.html"
    success_url = success_url_to("core:quiz_list")


class QuizDeleteView(StaffRequiredMixin, BreadcrumbsMixin, BaseDeleteView):
    model = Quiz
    template_name = "quiz/confirm_delete.html"
    success_url = success_url_to("core:quiz_list")


# @login_required
# def seleccionar_quiz_view(request):
#     ejes = EjeTematico.objects.all()

#     if request.method == "POST":
#         eje_id = request.POST.get("eje_id")
#         cantidad = request.POST.get("cantidad")
#         return redirect(f"/quiz/{eje_id}/presentar/?cantidad={cantidad}")

#     return render(request, "quiz/seleccionar_quiz.html", {"ejes": ejes})



@login_required
def presentar_quiz_view(request, eje_id):
    eje = get_object_or_404(EjeTematico, id=eje_id)
    cantidad = int(request.GET.get("cantidad", 100))

    # Generar preguntas aleatorias si no existen en la sesión
    if "preguntas_quiz" not in request.session:
        todas_preguntas = list(Pregunta.objects.filter(eje=eje).prefetch_related('opciones'))
        seleccionadas = random.sample(todas_preguntas, min(cantidad, len(todas_preguntas)))
        request.session["preguntas_quiz"] = [p.id for p in seleccionadas]
        request.session["respuestas_quiz"] = {}

    # Cargar preguntas desde sesión
    preguntas_ids = request.session.get("preguntas_quiz", [])
    preguntas_queryset = Pregunta.objects.filter(id__in=preguntas_ids).prefetch_related('opciones').order_by('id')

    # Paginación de a 5 preguntas
    paginator = Paginator(preguntas_queryset, 5)
    page_number = int(request.GET.get("page", 1))
    preguntas = paginator.get_page(page_number)

    # Procesar respuestas del POST
    if request.method == "POST":
        for pregunta in preguntas:
            seleccionada = request.POST.get(f"pregunta_{pregunta.id}")
            if seleccionada:
                request.session["respuestas_quiz"][str(pregunta.id)] = seleccionada
        request.session.modified = True

        # Si hay más páginas, redirigir a la siguiente
        if preguntas.has_next():
            next_page = preguntas.next_page_number()
            return redirect(f"{request.path}?page={next_page}&cantidad={cantidad}")

        # Evaluar todas las respuestas al finalizar
        respuestas_totales = request.session.get("respuestas_quiz", {})
        correctas = 0
        total = len(preguntas_ids)

        resultado = Resultado.objects.create(
            usuario=request.user,
            quiz=None,
            eje=eje,
            puntaje=0
        )

        for pregunta in Pregunta.objects.filter(id__in=preguntas_ids):
            seleccionada_id = respuestas_totales.get(str(pregunta.id))
            try:
                seleccionada_id = int(seleccionada_id)
            except (TypeError, ValueError):
                seleccionada_id = None

            opcion = Opcion.objects.filter(id=seleccionada_id, pregunta=pregunta).first()

            RespuestaUsuario.objects.create(
                resultado=resultado,
                pregunta=pregunta,
                opcion_seleccionada=opcion
            )

            if opcion and opcion.es_correcta:
                correctas += 1

        # Calcular y guardar el puntaje
        puntaje = round((correctas / total) * 100, 2) if total > 0 else 0
        resultado.puntaje = puntaje
        resultado.save()

        # Limpiar sesión
        request.session.pop("preguntas_quiz", None)
        request.session.pop("respuestas_quiz", None)

        return redirect("core:detalle_resultado", resultado_id=resultado.id)

    # Mostrar preguntas
    return render(request, "quiz/presentar_quiz.html", {
        "eje": eje,
        "preguntas": preguntas,
    })
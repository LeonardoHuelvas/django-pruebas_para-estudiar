from typing import Iterable
from django.db.models import Prefetch
from core.models import Quiz, EjeTematico, Pregunta

def list_quices() -> Iterable[Quiz]:
    return Quiz.objects.all().order_by("nombre")

def get_quiz_with_ejes(quiz_id: int) -> Quiz:
    return (Quiz.objects
            .prefetch_related(
                Prefetch("ejes", queryset=EjeTematico.objects.order_by("nombre")
                         .prefetch_related(Prefetch("preguntas", queryset=Pregunta.objects.only("id","texto")))))
            .get(id=quiz_id))

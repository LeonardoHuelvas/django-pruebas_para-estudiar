from typing import Iterable
from core.models import Pregunta

def list_preguntas_by_eje(eje_id: int) -> Iterable[Pregunta]:
    return Pregunta.objects.filter(eje_id=eje_id).select_related("eje").order_by("id")

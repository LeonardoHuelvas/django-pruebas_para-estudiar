from django.db import transaction
from core.models import Pregunta, Opcion

@transaction.atomic
def crear_pregunta_unica(eje_id: int, texto: str, opciones: list[tuple[str, bool]]) -> Pregunta:
    # Regla: en Opción Única debe haber exactamente 1 correcta
    correctas = sum(1 for _, ok in opciones if ok)
    if correctas != 1:
        raise ValueError("Debe marcar exactamente 1 opción correcta.")
    p = Pregunta.objects.create(eje_id=eje_id, texto=texto, tipo="UNICA")
    Opcion.objects.bulk_create([Opcion(pregunta=p, texto=t, es_correcta=ok) for t, ok in opciones])
    return p
